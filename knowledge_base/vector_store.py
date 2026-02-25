"""
vector_store.py
---------------
ChromaDB-based vector store for AutomaterSelenium test scenarios.

Collections:
  - scenarios   : One doc per @AutomaterScenario method
  - framework   : Framework class/method docs for code generation context
  - modules     : One doc per module (for coverage queries)

Usage:
    store = VectorStore()
    store.build_from_flat_list("knowledge_base/raw/scenarios_flat.json")

    results = store.search_scenarios("create incident request with priority", top_k=5)
    context = store.get_module_context("requests/request")
"""

import json
import os
from pathlib import Path
from typing import Optional

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions


# ──────────────────────────────────────────────
# Embedding function (OpenAI or local fallback)
# ──────────────────────────────────────────────

def _get_embedding_fn():
    api_key = os.environ.get("OPENAI_API_KEY")
    if api_key:
        return embedding_functions.OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-3-small",
        )
    # Fallback: SentenceTransformer (no API key required)
    return embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )


# ──────────────────────────────────────────────
# VectorStore class
# ──────────────────────────────────────────────

class VectorStore:
    """
    Thin wrapper around ChromaDB for AutomaterSelenium knowledge base.
    """

    SCENARIOS_COLLECTION    = "automater_scenarios"
    MODULES_COLLECTION      = "automater_modules"
    FRAMEWORK_COLLECTION    = "automater_framework"
    SOURCE_FILES_COLLECTION = "automater_source_files"
    HELP_TOPICS_COLLECTION  = "automater_help_topics"

    def __init__(self, persist_dir: Optional[str] = None):
        base = Path(__file__).resolve().parent
        self.persist_dir = persist_dir or str(base / "chroma_db")
        Path(self.persist_dir).mkdir(parents=True, exist_ok=True)

        self.client = chromadb.PersistentClient(
            path=self.persist_dir,
            settings=Settings(anonymized_telemetry=False),
        )
        self._embed_fn = _get_embedding_fn()

        self._scenarios = self.client.get_or_create_collection(
            name=self.SCENARIOS_COLLECTION,
            embedding_function=self._embed_fn,
            metadata={"hnsw:space": "cosine"},
        )
        self._modules = self.client.get_or_create_collection(
            name=self.MODULES_COLLECTION,
            embedding_function=self._embed_fn,
        )
        self._framework = self.client.get_or_create_collection(
            name=self.FRAMEWORK_COLLECTION,
            embedding_function=self._embed_fn,
        )
        self._source_files = self.client.get_or_create_collection(
            name=self.SOURCE_FILES_COLLECTION,
            embedding_function=self._embed_fn,
            metadata={"hnsw:space": "cosine"},
        )
        self._help_topics = self.client.get_or_create_collection(
            name=self.HELP_TOPICS_COLLECTION,
            embedding_function=self._embed_fn,
            metadata={"hnsw:space": "cosine"},
        )

    # ── Build from flat scenario list ──────────────────────

    def build_from_flat_list(
        self,
        scenarios_json: str,
        batch_size: int = 100,
        reset: bool = False,
    ) -> int:
        """
        Ingest all scenarios into the vector store.
        Returns count of documents added.
        """
        if reset:
            self.client.delete_collection(self.SCENARIOS_COLLECTION)
            self._scenarios = self.client.get_or_create_collection(
                name=self.SCENARIOS_COLLECTION,
                embedding_function=self._embed_fn,
                metadata={"hnsw:space": "cosine"},
            )

        with open(scenarios_json, encoding='utf-8') as f:
            scenarios = json.load(f)

        existing_ids = set(self._scenarios.get()['ids'])
        # Deduplicate within the JSON itself (keep last occurrence) AND against existing
        seen: dict = {}
        for i, s in enumerate(scenarios):
            raw_id = s.get('id') or f"no_id_{i}"
            seen[str(raw_id)] = s   # last occurrence wins for duplicates
        to_add = [s for raw_id, s in seen.items() if raw_id not in existing_ids]

        print(f"  📥 Adding {len(to_add)} new scenarios to vector store...")

        for i in range(0, len(to_add), batch_size):
            batch = to_add[i:i + batch_size]
            self._scenarios.add(
                ids=[str(s['id']) if s.get('id') else f"no_id_{i + j}" for j, s in enumerate(batch)],
                documents=[s['embed_text'] for s in batch],
                metadatas=[{
                    'module_path': s['module_path'],
                    'entity': s['entity'],
                    'module': s['module'],
                    'class_name': s['class'],
                    'method_name': s['method_name'],
                    'description': s['description'],
                    'priority': s['priority'],
                    'run_type': s['run_type'],
                    'tags': ','.join(s.get('tags', [])),
                    'group': s['group'],
                } for s in batch],
            )
            print(f"    ✅ Batch {i // batch_size + 1}: {len(batch)} docs")

        return len(to_add)

    # ── Build module summaries ─────────────────────────────

    def build_module_summaries(self, module_index_json: str) -> int:
        """Build per-module summary docs for coverage-aware generation."""
        with open(module_index_json, encoding='utf-8') as f:
            index = json.load(f)

        docs, ids, metas = [], [], []
        for mp, mod in index['modules'].items():
            descriptions = [sc['description'] for sc in mod.get('scenarios', [])]
            methods = [sc['method_name'] for sc in mod.get('scenarios', [])]
            doc_text = (
                f"Module: {mp} | Entity: {mod['entity']} | "
                f"Scenario count: {mod['scenario_count']} | "
                f"Methods: {', '.join(methods[:30])} | "
                f"Descriptions: {' | '.join(descriptions[:20])}"
            )
            docs.append(doc_text)
            ids.append(mp.replace('/', '_'))
            metas.append({
                'module_path': mp,
                'entity': mod['entity'],
                'scenario_count': mod['scenario_count'],
                'suite_role': mod.get('suite_role', ''),
            })

        if docs:
            self._modules.upsert(ids=ids, documents=docs, metadatas=metas)
        print(f"  ✅ Module summaries: {len(docs)} modules indexed")
        return len(docs)

    # ── Search ─────────────────────────────────────────────

    def search_scenarios(
        self,
        query: str,
        top_k: int = 10,
        module_filter: Optional[str] = None,
    ) -> list[dict]:
        """
        Semantic search over existing test scenarios.
        Returns list of { id, description, method_name, module_path, distance }
        """
        where = {"module_path": {"$eq": module_filter}} if module_filter else None
        kwargs = {"query_texts": [query], "n_results": min(top_k, self._scenarios.count())}
        if where:
            kwargs["where"] = where

        results = self._scenarios.query(**kwargs)
        output = []
        for i, doc_id in enumerate(results['ids'][0]):
            output.append({
                'id': doc_id,
                'document': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i],
            })
        return output

    def get_module_context(self, module_path: str) -> dict:
        """Get all scenarios for a specific module (for code generation context)."""
        results = self._scenarios.get(
            where={"module_path": {"$eq": module_path}},
            include=["documents", "metadatas"],
        )
        return {
            'module_path': module_path,
            'scenarios': [
                {'id': id_, 'document': doc, 'metadata': meta}
                for id_, doc, meta in zip(
                    results['ids'],
                    results['documents'],
                    results['metadatas'],
                )
            ]
        }

    # ── Source file indexing ───────────────────────────────

    def build_from_source_files(
        self,
        docs: list[dict],
        batch_size: int = 50,
        reset: bool = False,
    ) -> int:
        """
        Ingest entity source file chunks into the `automater_source_files` collection.
        Each doc must contain: id, content, embed_text, entity, module, module_path,
        file_type, file_path, class_name, package, chunk_index, total_chunks.
        Returns count of documents added.
        """
        if reset:
            self.client.delete_collection(self.SOURCE_FILES_COLLECTION)
            self._source_files = self.client.get_or_create_collection(
                name=self.SOURCE_FILES_COLLECTION,
                embedding_function=self._embed_fn,
                metadata={"hnsw:space": "cosine"},
            )

        if not docs:
            return 0

        existing_ids = set(self._source_files.get()['ids'])
        # Deduplicate within docs list AND against existing (keep last occurrence)
        seen: dict = {}
        for d in docs:
            seen[d['id']] = d
        to_add = [d for doc_id, d in seen.items() if doc_id not in existing_ids]

        for i in range(0, len(to_add), batch_size):
            batch = to_add[i:i + batch_size]
            self._source_files.add(
                ids=[d['id'] for d in batch],
                documents=[d['embed_text'] for d in batch],
                metadatas=[{
                    'entity':       d['entity'],
                    'module':       d['module'],
                    'module_path':  d['module_path'],
                    'file_type':    d['file_type'],
                    'file_path':    d['file_path'],
                    'class_name':   d['class_name'],
                    'package':      d.get('package', ''),
                    'chunk_index':  d.get('chunk_index', 0),
                    'total_chunks': d.get('total_chunks', 1),
                    'content':      d['content'][:2000],   # store excerpt for fast retrieval
                } for d in batch],
            )
        return len(to_add)

    # ── Help topic indexing ────────────────────────────────

    def build_from_help_topics(
        self,
        help_topics_json: str,
        batch_size: int = 100,
        reset: bool = False,
    ) -> int:
        """
        Ingest SDP help guide topics into the `automater_help_topics` collection.
        Each item in help_topics_flat.json must have:
          id, topic_id, title, module, permalink, url, type, content, embed_text
        Returns count of documents added.
        """
        if reset:
            self.client.delete_collection(self.HELP_TOPICS_COLLECTION)
            self._help_topics = self.client.get_or_create_collection(
                name=self.HELP_TOPICS_COLLECTION,
                embedding_function=self._embed_fn,
                metadata={"hnsw:space": "cosine"},
            )

        with open(help_topics_json, encoding='utf-8') as f:
            items = json.load(f)

        existing_ids = set(self._help_topics.get()['ids'])
        seen: dict = {}
        for item in items:
            seen[item['id']] = item  # last occurrence wins
        to_add = [v for k, v in seen.items() if k not in existing_ids]

        print(f"  📥 Adding {len(to_add)} new help-doc records to vector store...")

        for i in range(0, len(to_add), batch_size):
            batch = to_add[i:i + batch_size]
            self._help_topics.add(
                ids=[d['id'] for d in batch],
                documents=[d.get('embed_text', d.get('content', d['title'])) for d in batch],
                metadatas=[{
                    'topic_id':  d.get('topic_id', ''),
                    'title':     d['title'][:200],
                    'module':    d['module'],
                    'permalink': d['permalink'],
                    'url':       d.get('url', ''),
                    'type':      d.get('type', 'full_text'),
                    'content':   d.get('content', '')[:2000],
                } for d in batch],
            )
            print(f"    ✅ Batch {i // batch_size + 1}: {len(batch)} docs")

        return len(to_add)

    def search_help_topics(
        self,
        query: str,
        module_filter: Optional[str] = None,
        type_filter: Optional[str] = None,
        top_k: int = 8,
    ) -> list[dict]:
        """
        Semantic search over SDP help guide topics.
        Optionally filter by module (e.g. 'requests') or type ('field'/'steps'/'full_text').
        Returns list of { id, title, module, permalink, url, type, content, distance }.
        """
        total = self._help_topics.count()
        if total == 0:
            return []

        where: dict = {}
        if module_filter and type_filter:
            where = {"$and": [
                {"module": {"$eq": module_filter}},
                {"type":   {"$eq": type_filter}},
            ]}
        elif module_filter:
            where = {"module": {"$eq": module_filter}}
        elif type_filter:
            where = {"type": {"$eq": type_filter}}

        kwargs: dict = {
            "query_texts": [query],
            "n_results": min(top_k, total),
            "include": ["metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where

        results = self._help_topics.query(**kwargs)
        output = []
        for i, doc_id in enumerate(results['ids'][0]):
            meta = results['metadatas'][0][i]
            output.append({
                'id':        doc_id,
                'title':     meta.get('title', ''),
                'module':    meta.get('module', ''),
                'permalink': meta.get('permalink', ''),
                'url':       meta.get('url', ''),
                'type':      meta.get('type', ''),
                'content':   meta.get('content', ''),
                'distance':  results['distances'][0][i],
            })
        return output

    def search_source_files(
        self,
        query: str,
        entity_filter: Optional[str] = None,
        file_type_filter: Optional[str] = None,
        top_k: int = 10,
    ) -> list[dict]:
        """
        Semantic search over source file chunks.
        Optionally filter by entity (e.g. "asset") and/or file_type (e.g. "LOCATORS").
        Returns list of { id, entity, module_path, file_type, class_name, content, distance }.
        """
        total = self._source_files.count()
        if total == 0:
            return []

        where: dict = {}
        if entity_filter and file_type_filter:
            where = {"$and": [
                {"entity": {"$eq": entity_filter}},
                {"file_type": {"$eq": file_type_filter}},
            ]}
        elif entity_filter:
            where = {"entity": {"$eq": entity_filter}}
        elif file_type_filter:
            where = {"file_type": {"$eq": file_type_filter}}

        kwargs: dict = {
            "query_texts": [query],
            "n_results": min(top_k, total),
            "include": ["metadatas", "distances"],
        }
        if where:
            kwargs["where"] = where

        results = self._source_files.query(**kwargs)
        output = []
        for i, doc_id in enumerate(results['ids'][0]):
            meta = results['metadatas'][0][i]
            output.append({
                'id':          doc_id,
                'entity':      meta.get('entity', ''),
                'module_path': meta.get('module_path', ''),
                'file_type':   meta.get('file_type', ''),
                'class_name':  meta.get('class_name', ''),
                'file_path':   meta.get('file_path', ''),
                'content':     meta.get('content', ''),
                'distance':    results['distances'][0][i],
            })
        return output

    def get_entity_full_context(self, entity: str) -> dict:
        """
        Retrieve ALL indexed source file chunks for an entity.
        Groups by file_type so the caller can present them in order.
        Returns { entity, files: { file_type: [{ class_name, file_path, content }, ...] } }
        """
        results = self._source_files.get(
            where={"entity": {"$eq": entity}},
            include=["metadatas"],
        )
        files_by_type: dict[str, list] = {}
        for meta in results.get('metadatas', []):
            ftype = meta.get('file_type', 'OTHER')
            files_by_type.setdefault(ftype, [])
            # Deduplicate by class_name + chunk_index
            entry = {
                'class_name':   meta.get('class_name', ''),
                'file_path':    meta.get('file_path', ''),
                'content':      meta.get('content', ''),
                'chunk_index':  meta.get('chunk_index', 0),
                'total_chunks': meta.get('total_chunks', 1),
            }
            files_by_type[ftype].append(entry)

        # Sort chunks within each type by chunk_index
        for ftype in files_by_type:
            files_by_type[ftype].sort(key=lambda x: x['chunk_index'])

        return {'entity': entity, 'files': files_by_type}

    def list_indexed_entities(self) -> list[str]:
        """Return all unique entity names that have source files indexed."""
        if self._source_files.count() == 0:
            return []
        results = self._source_files.get(include=["metadatas"])
        seen = set()
        entities = []
        for meta in results.get('metadatas', []):
            e = meta.get('entity', '')
            if e and e != 'skeleton' and e not in seen:
                seen.add(e)
                entities.append(e)
        return sorted(entities)

    def is_duplicate(self, description: str, threshold: float = 0.92) -> tuple[bool, list]:
        """
        Check if a described scenario already exists in the knowledge base.
        Returns (is_duplicate, similar_matches).
        """
        if self._scenarios.count() == 0:
            return False, []
        results = self.search_scenarios(description, top_k=5)
        similar = [r for r in results if (1 - r['distance']) >= threshold]
        return len(similar) > 0, similar

    @property
    def scenario_count(self) -> int:
        return self._scenarios.count()

    @property
    def source_file_count(self) -> int:
        return self._source_files.count()

    @property
    def help_topic_count(self) -> int:
        return self._help_topics.count()


# ── CLI ───────────────────────────────────────────────────

if __name__ == '__main__':
    base = Path(__file__).resolve().parents[1]
    kb_raw = base / 'knowledge_base' / 'raw'

    store = VectorStore()

    print(f"\n🧠 Building vector store from {kb_raw / 'scenarios_flat.json'}...")
    count = store.build_from_flat_list(str(kb_raw / 'scenarios_flat.json'), reset=False)
    print(f"   Added {count} new scenarios. Total: {store.scenario_count}")

    print(f"\n🗂  Building module summaries...")
    store.build_module_summaries(str(kb_raw / 'module_index.json'))

    print(f"\n🔍 Test search: 'create incident request with priority high'")
    results = store.search_scenarios("create incident request with priority high", top_k=5)
    for r in results:
        print(f"  [{r['metadata']['module_path']}] {r['metadata']['method_name']} | {r['metadata']['description'][:80]}")
