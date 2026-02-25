"""
rag_indexer.py
--------------
Module-aware RAG Indexer for AutomaterSelenium source files.

Crawls every entity under AutomaterSelenium/src/modules/, identifies each file
by its role in the skeleton (Locators, Fields, DataConstants, Constants, Base,
Entity, APIUtil, ActionsUtil, data JSON, conf JSON), chunks the content, and
stores it in the `automater_source_files` ChromaDB collection — tagged with:

  entity      : e.g. "asset"
  module      : e.g. "assets"
  module_path : e.g. "modules/assets/asset"
  file_type   : LOCATORS | FIELDS | DATA_CONSTANTS | CONSTANTS | BASE |
                ENTITY | API_UTIL | ACTIONS_UTIL | DATA_JSON | CONF_JSON |
                SKELETON | OTHER
  file_path   : absolute path
  class_name  : Java class name (or filename for non-Java)

The skeleton templates are also indexed so the LLM always knows the canonical
file structure for any new entity.

This populates TWO collections:
  1. automater_scenarios    → semantic search over test scenario descriptions
  2. automater_source_files → semantic search over actual source code chunks

Usage (CLI):
    python knowledge_base/rag_indexer.py

Usage (Python):
    from knowledge_base.rag_indexer import RagIndexer
    indexer = RagIndexer(base_dir=".")
    indexer.run()
"""

import json
import re
import os
from pathlib import Path
from typing import Optional


MODULES_ROOT_GLOB = "AutomaterSelenium/src/com/zoho/automater/selenium/modules"
SKELETON_ROOT     = "AutomaterSelenium/src/com/zoho/automater/selenium/base/skeleton"
RESOURCES_ROOT    = "AutomaterSelenium/resources/entity"
SKELETON_RES_ROOT = "AutomaterSelenium/resources/skeleton"

# ── File type detection ────────────────────────────────────────────────────────

def _classify_file(file_path: Path) -> str:
    name = file_path.stem          # filename without extension
    ext  = file_path.suffix.lower()

    if ext == ".java":
        if name.endswith("Locators") or "Locator" in name:   return "LOCATORS"
        if name.endswith("Fields"):                           return "FIELDS"
        if name.endswith("DataConstants"):                    return "DATA_CONSTANTS"
        if name.endswith("Constants") and "Data" not in name: return "CONSTANTS"
        if "APIUtil" in name or name.endswith("Api"):         return "API_UTIL"
        if "ActionsUtil" in name or "ActionUtil" in name:     return "ACTIONS_UTIL"
        if "FormBuilder" in name or "FormUtil" in name:       return "FORM_UTIL"
        if name.endswith("Base") or "CommonBase" in name:     return "BASE"
        if "Skeleton" in name:                                return "SKELETON"
        if name.endswith("Preprocess") or name.endswith("PreProcess"):
            return "PREPROCESS"
        # Likely the thin Entity class (e.g. Asset.java, Solution.java)
        return "ENTITY"

    if ext == ".json":
        parts = file_path.parts
        if "conf" in parts:                                   return "CONF_JSON"
        if "data" in parts:                                   return "DATA_JSON"
        if "skeleton" in str(file_path):                      return "SKELETON_JSON"

    return "OTHER"


def _extract_java_class_name(content: str) -> str:
    m = re.search(r'public\s+(?:abstract\s+|final\s+)?(?:class|interface)\s+(\w+)', content)
    return m.group(1) if m else ""


def _extract_java_package(content: str) -> str:
    m = re.search(r'^package\s+([\w.]+);', content, re.MULTILINE)
    return m.group(1) if m else ""


def _extract_module_path_from_java_path(file_path: Path, src_root: Path) -> tuple[str, str, str]:
    """
    From the absolute file path, derive:
      module_path  e.g. "modules/assets/asset"
      module       e.g. "assets"
      entity       e.g. "asset"
    """
    try:
        rel = file_path.relative_to(src_root / "com/zoho/automater/selenium")
        parts = list(rel.parts)
        # parts[0] = "modules", parts[1] = module (assets), parts[2...] = sub-path
        # parts[-1] = filename (e.g. "Asset.java") — strip it
        if parts[0] != "modules" or len(parts) < 2:
            return "", "", ""

        # Use only directory parts (strip the filename)
        dir_parts = parts[:-1]  # e.g. ["modules", "assets", "asset"] or ["modules", "assets", "asset", "common"]
        module = dir_parts[1]

        # entity_parts = dir parts after "modules"
        entity_parts = dir_parts[1:]  # e.g. ["assets", "asset"] or ["assets", "asset", "common"]

        # Strip sub-dirs that aren't the entity name
        entity_parts_clean = [p for p in entity_parts
                              if p not in ("common", "utils", "roles", "skeleton")]
        entity = entity_parts_clean[-1] if entity_parts_clean else module
        module_path = "modules/" + "/".join(entity_parts_clean)
        return module_path, module, entity
    except Exception:
        return "", "", ""


# ── Chunker ────────────────────────────────────────────────────────────────────

def _chunk_java_file(content: str, max_chars: int = 6000) -> list[str]:
    """
    Split a Java file into meaningful chunks:
      - First chunk: package + imports + class declaration + @AutomaterSuite
      - Subsequent chunks: groups of method definitions (split by blank lines)

    If file is small enough, return as-is.
    """
    if len(content) <= max_chars:
        return [content]

    chunks = []
    lines = content.splitlines(keepends=True)

    # Header chunk (package, imports, class decl)
    header_lines = []
    body_start = 0
    brace_depth = 0
    for i, line in enumerate(lines):
        header_lines.append(line)
        brace_depth += line.count("{") - line.count("}")
        if brace_depth > 0:
            body_start = i + 1
            break
    header = "".join(header_lines)
    chunks.append(header)

    # Body: split by method boundaries (lines starting with blank + @Override or
    # public/protected + return type + method name)
    body_text = "".join(lines[body_start:])
    method_pattern = re.compile(
        r'(?=\n\s{0,4}(?:@Override\s+)?(?:public|protected|private)\s)',
        re.MULTILINE
    )
    parts = method_pattern.split(body_text)
    current = ""
    for part in parts:
        if len(current) + len(part) > max_chars:
            if current:
                chunks.append(header[:500] + "\n// ... (continued) ...\n" + current)
            current = part
        else:
            current += part
    if current:
        chunks.append(header[:500] + "\n// ... (continued) ...\n" + current)

    return chunks


# ── RagIndexer ─────────────────────────────────────────────────────────────────

class RagIndexer:
    """
    Scans the AutomaterSelenium source tree and builds a module-aware
    source-file vector store alongside the existing scenario vector store.
    """

    def __init__(self, base_dir: Optional[str] = None):
        self.base         = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self.modules_root = self.base / MODULES_ROOT_GLOB
        self.skeleton_root= self.base / SKELETON_ROOT
        self.resources_root = self.base / RESOURCES_ROOT
        self.skeleton_res   = self.base / SKELETON_RES_ROOT
        self.src_root       = self.base / "AutomaterSelenium/src"
        self.kb_raw         = self.base / "knowledge_base/raw"

    def run(self, reset_source_files: bool = False, reset_scenarios: bool = False,
            reset_help_topics: bool = False):
        """
        Full indexing run:
          1. Populate automater_scenarios from scenarios_flat.json
          2. Populate automater_source_files from Java source files
          3. Index skeleton templates
          4. Build module summary docs
        """
        from knowledge_base.vector_store import VectorStore

        print("\n" + "="*60)
        print("  RAG Indexer — AutomaterSelenium")
        print("="*60)

        store = VectorStore(persist_dir=str(self.base / "knowledge_base/chroma_db"))

        # ── Step 1: Scenario embeddings ───────────────────────────────
        scenarios_json = self.kb_raw / "scenarios_flat.json"
        if scenarios_json.exists():
            print(f"\n[1/4] Indexing scenarios from {scenarios_json.name}...")
            added = store.build_from_flat_list(str(scenarios_json), reset=reset_scenarios)
            print(f"      ✅ {added} new scenarios added. Total: {store.scenario_count}")
        else:
            print(f"\n[1/4] ⚠️  scenarios_flat.json not found — run ingestion first")

        # ── Step 2: Source file embeddings ─────────────────────────────
        print(f"\n[2/4] Indexing source files from modules/...")
        source_docs = self._collect_source_docs()
        added = store.build_from_source_files(source_docs, reset=reset_source_files)
        print(f"      ✅ {added} new source file chunks indexed. "
              f"Total: {store.source_file_count}")

        # ── Step 3: Skeleton template embeddings ──────────────────────
        print(f"\n[3/4] Indexing skeleton templates...")
        skeleton_docs = self._collect_skeleton_docs()
        store.build_from_source_files(skeleton_docs, reset=False)
        print(f"      ✅ {len(skeleton_docs)} skeleton template chunks indexed")

        # ── Step 4: Module summary docs ───────────────────────────────
        module_index_json = self.kb_raw / "module_index.json"
        if module_index_json.exists():
            print(f"\n[4/5] Building module summary docs...")
            store.build_module_summaries(str(module_index_json))
        else:
            print(f"\n[4/5] ⚠️  module_index.json not found — run ingestion first")

        # ── Step 5: Help topics from SDP help guide ───────────────────
        help_topics_json = self.kb_raw / "help_topics_flat.json"
        if help_topics_json.exists():
            print(f"\n[5/5] Indexing SDP help guide topics from {help_topics_json.name}...")
            added = store.build_from_help_topics(str(help_topics_json), reset=reset_help_topics)
            print(f"      ✅ {added} new help-doc records added. Total: {store.help_topic_count}")
        else:
            print(f"\n[5/5] ⚠️  help_topics_flat.json not found — run ingestion/help_doc_crawler.py first")

        print("\n" + "="*60)
        print(f"  ✅ RAG index complete!")
        print(f"     Scenarios     : {store.scenario_count}")
        print(f"     Source chunks : {store.source_file_count}")
        print(f"     Help topics   : {store.help_topic_count}")
        print("="*60 + "\n")

    def _collect_source_docs(self) -> list[dict]:
        """
        Walk all entity directories under modules/ and build document dicts
        for every Java + JSON file found.
        """
        docs = []

        if not self.modules_root.exists():
            print(f"  ⚠️  Modules root not found: {self.modules_root}")
            return docs

        # Group files by entity directory
        for java_file in sorted(self.modules_root.rglob("*.java")):
            doc = self._build_source_doc(java_file)
            if doc:
                docs.append(doc)

        # Also index data JSON files
        if self.resources_root.exists():
            for json_file in sorted(self.resources_root.rglob("*.json")):
                doc = self._build_json_doc(json_file)
                if doc:
                    docs.append(doc)

        print(f"  📂 Collected {len(docs)} source documents from modules/")
        return docs

    def _build_source_doc(self, file_path: Path) -> Optional[dict]:
        """Build a single source document dict for a Java file."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if not content.strip():
                return None

            file_type  = _classify_file(file_path)
            class_name = _extract_java_class_name(content)
            package    = _extract_java_package(content)
            module_path, module, entity = _extract_module_path_from_java_path(
                file_path, self.src_root
            )

            if not module_path:
                return None

            # Build embed text — description of what this file contains
            embed_text = self._build_embed_text(
                content=content,
                file_type=file_type,
                class_name=class_name,
                module_path=module_path,
                entity=entity,
                module=module,
            )

            # Chunk large files
            chunks = _chunk_java_file(content)
            doc_id_base = f"src_{module_path.replace('/', '_')}_{file_type}_{class_name}"

            results = []
            for i, chunk in enumerate(chunks):
                chunk_embed = embed_text if i == 0 else (
                    f"Module: {module_path} | Entity: {entity} | "
                    f"File: {class_name}.java [{file_type}] | Chunk {i+1} | "
                    + chunk[:300]
                )
                results.append({
                    "id":          f"{doc_id_base}_chunk{i}",
                    "content":     chunk,
                    "embed_text":  chunk_embed,
                    "entity":      entity,
                    "module":      module,
                    "module_path": module_path,
                    "file_type":   file_type,
                    "file_path":   str(file_path),
                    "class_name":  class_name,
                    "package":     package,
                    "chunk_index": i,
                    "total_chunks": len(chunks),
                })
            return results  # returns list — handled by caller

        except Exception as ex:
            print(f"  ⚠️  Could not index {file_path.name}: {ex}")
            return None

    def _build_json_doc(self, file_path: Path) -> Optional[dict]:
        """Build a document dict for a resource JSON file."""
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            if not content.strip() or len(content) < 10:
                return None

            file_type = _classify_file(file_path)
            # Derive entity from path
            rel_parts = file_path.relative_to(self.resources_root).parts
            # e.g. conf/assets/asset.json → module=assets, entity=asset
            module = rel_parts[1] if len(rel_parts) > 1 else "unknown"
            entity = rel_parts[2].replace(".json", "") if len(rel_parts) > 2 else module
            module_path = f"modules/{module}/{entity}"

            embed_text = (
                f"Module: {module_path} | Entity: {entity} | "
                f"File: {file_path.name} [{file_type}] | "
                f"Content preview: {content[:300]}"
            )

            return [{
                "id":          f"res_{module}_{entity}_{file_type}_{file_path.stem}",
                "content":     content[:8000],
                "embed_text":  embed_text,
                "entity":      entity,
                "module":      module,
                "module_path": module_path,
                "file_type":   file_type,
                "file_path":   str(file_path),
                "class_name":  file_path.stem,
                "package":     "",
                "chunk_index": 0,
                "total_chunks": 1,
            }]
        except Exception:
            return None

    def _collect_skeleton_docs(self) -> list[dict]:
        """Index the skeleton Java templates + JSON so the LLM knows the pattern."""
        docs = []
        for file_path in sorted(self.skeleton_root.rglob("*.java")):
            try:
                content = file_path.read_text(encoding="utf-8", errors="ignore")
                file_type = "SKELETON"
                class_name = _extract_java_class_name(content) or file_path.stem
                embed_text = (
                    f"Skeleton template | File: {file_path.name} | "
                    f"Purpose: canonical template for {file_path.stem.replace('Skeleton', '')} "
                    f"file in any entity | Content: {content[:400]}"
                )
                docs.append({
                    "id":          f"skeleton_{file_path.stem}",
                    "content":     content,
                    "embed_text":  embed_text,
                    "entity":      "skeleton",
                    "module":      "skeleton",
                    "module_path": "base/skeleton",
                    "file_type":   "SKELETON",
                    "file_path":   str(file_path),
                    "class_name":  class_name,
                    "package":     "",
                    "chunk_index": 0,
                    "total_chunks": 1,
                })
            except Exception:
                pass

        # Also skeleton JSON
        if self.skeleton_res.exists():
            for jf in self.skeleton_res.glob("*.json"):
                try:
                    content = jf.read_text(encoding="utf-8", errors="ignore")
                    docs.append({
                        "id":          f"skeleton_json_{jf.stem}",
                        "content":     content,
                        "embed_text":  f"Skeleton JSON template | {jf.name} | {content[:300]}",
                        "entity":      "skeleton",
                        "module":      "skeleton",
                        "module_path": "base/skeleton",
                        "file_type":   "SKELETON_JSON",
                        "file_path":   str(jf),
                        "class_name":  jf.stem,
                        "package":     "",
                        "chunk_index": 0,
                        "total_chunks": 1,
                    })
                except Exception:
                    pass

        return docs

    def _build_embed_text(
        self, content: str, file_type: str, class_name: str,
        module_path: str, entity: str, module: str,
    ) -> str:
        """
        Build a rich embedding string tailored to the file type.
        The more context in the embed text, the better the retrieval.
        """
        base = (
            f"Module: {module_path} | Entity: {entity} | Module: {module} | "
            f"ClassName: {class_name} | FileType: {file_type}"
        )

        if file_type == "LOCATORS":
            # Extract all Locator constant names for better retrieval
            constants = re.findall(r'Locator\s+(\w+)\s*=', content)
            return base + f" | Locator constants: {', '.join(constants[:30])}"

        if file_type == "FIELDS":
            # Extract all FieldDetails constant names
            fields = re.findall(r'FieldDetails\s+(\w+)\s*=', content)
            return base + f" | Field definitions: {', '.join(fields[:30])}"

        if file_type in ("DATA_CONSTANTS", "CONSTANTS"):
            # Extract all constant names
            consts = re.findall(r'(?:String|TestCaseData)\s+(\w+)\s*=', content)
            return base + f" | Constants: {', '.join(consts[:30])}"

        if file_type in ("BASE", "ENTITY"):
            # Extract all method names
            methods = re.findall(r'public\s+\w+\s+(\w+)\s*\(', content)
            return base + f" | Methods: {', '.join(methods[:30])}"

        if file_type in ("API_UTIL", "ACTIONS_UTIL"):
            methods = re.findall(r'public\s+(?:static\s+)?\w+\s+(\w+)\s*\(', content)
            return base + f" | Utility methods: {', '.join(methods[:30])}"

        return base + f" | Preview: {content[:400]}"


# ── Flatten nested list helper ─────────────────────────────────────────────────

def _flatten(docs: list) -> list[dict]:
    """Flatten list-of-lists returned by _build_source_doc."""
    result = []
    for item in docs:
        if item is None:
            continue
        if isinstance(item, list):
            result.extend(item)
        else:
            result.append(item)
    return result


# ── Monkey-patch collect to flatten ───────────────────────────────────────────

_orig_collect = RagIndexer._collect_source_docs

def _collect_flat(self) -> list[dict]:
    raw = []
    if not self.modules_root.exists():
        return raw
    for java_file in sorted(self.modules_root.rglob("*.java")):
        doc = self._build_source_doc(java_file)
        if doc:
            raw.append(doc)
    if self.resources_root.exists():
        for json_file in sorted(self.resources_root.rglob("*.json")):
            doc = self._build_json_doc(json_file)
            if doc:
                raw.append(doc)
    flat = _flatten(raw)
    print(f"  📂 Collected {len(flat)} source document chunks from modules/")
    return flat

RagIndexer._collect_source_docs = _collect_flat


# ── CLI entry point ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    base = Path(__file__).resolve().parents[1]
    # ensure workspace root is on the path so `knowledge_base.vector_store` resolves
    if str(base) not in sys.path:
        sys.path.insert(0, str(base))

    reset_src    = "--reset-source" in sys.argv
    reset_sc     = "--reset-scenarios" in sys.argv
    reset_help   = "--reset-help-topics" in sys.argv
    reset_all    = "--reset" in sys.argv

    indexer = RagIndexer(base_dir=str(base))
    indexer.run(
        reset_source_files=reset_src or reset_all,
        reset_scenarios=reset_sc or reset_all,
        reset_help_topics=reset_help or reset_all,
    )
