"""
rag_server.py
-------------
FastAPI RAG Server for AutomaterSelenium module-aware code context retrieval.

This server exposes a clean REST API so the Coder Agent (and any future Web UI)
can retrieve entity-specific code context before generating new test cases.

Endpoints
---------
GET  /health
     Basic liveness check.

GET  /api/rag/modules
     List all modules/entities that have source files indexed.

GET  /api/rag/entities
     Alias of /api/rag/modules.

GET  /api/rag/entity/{entity}
     Return ALL indexed source file chunks for `entity` grouped by file_type.
     e.g.  GET /api/rag/entity/asset
     Query params:
       file_type (optional) – filter by LOCATORS | FIELDS | DATA_CONSTANTS | CONSTANTS |
                               BASE | ENTITY | API_UTIL | ACTIONS_UTIL | SKELETON | …

GET  /api/rag/skeleton
     Return the canonical skeleton templates (always entity="skeleton").

POST /api/rag/query
     Semantic search across source file chunks.
     Body: { "query": "...", "entity": "asset" (optional),
             "file_type": "LOCATORS" (optional), "top_k": 10 }

POST /api/rag/scenarios/query
     Semantic search across existing test scenarios (scenario descriptions).
     Body: { "query": "...", "entity": "asset" (optional), "top_k": 10 }

POST /api/rag/generation-context
     Build a full LLM-ready generation context for an entity + feature description.
     Returns structured context: locators, fields, data-constants, existing scenarios,
     skeleton templates.
     Body: { "entity": "asset", "feature_description": "Create asset with serial number" }

POST /api/rag/index
     Trigger a full re-index.  Pass { "reset": false } to add-only.

GET  /api/rag/stats
     Return counts: { scenarios, source_files, entities }.

Usage
-----
    uvicorn knowledge_base.rag_server:app --host 0.0.0.0 --port 8765 --reload

    # or via helper script:
    python knowledge_base/rag_server.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Optional

# ── Path bootstrap ──────────────────────────────────────────────────────────
# When run as a script the workspace root must be in sys.path
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
# ────────────────────────────────────────────────────────────────────────────

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from knowledge_base.vector_store import VectorStore

# ── Lazy singletons ──────────────────────────────────────────────────────────

_store: Optional[VectorStore] = None

def get_store() -> VectorStore:
    global _store
    if _store is None:
        _store = VectorStore(persist_dir=str(_ROOT / "knowledge_base/chroma_db"))
    return _store


# ── FastAPI app ───────────────────────────────────────────────────────────────

app = FastAPI(
    title="AutomaterSelenium RAG Server",
    description="Module-aware code context retrieval for AI test-case generation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Pydantic request / response models ────────────────────────────────────────

class SourceQueryRequest(BaseModel):
    query: str = Field(..., description="Semantic search query")
    entity: Optional[str] = Field(None, description="Filter by entity (e.g. 'asset')")
    file_type: Optional[str] = Field(None, description="Filter by file type (e.g. 'LOCATORS')")
    top_k: int = Field(10, description="Max results to return")


class ScenarioQueryRequest(BaseModel):
    query: str = Field(..., description="Semantic search query over scenario descriptions")
    entity: Optional[str] = Field(None, description="Filter by entity")
    top_k: int = Field(10, description="Max results to return")


class GenerationContextRequest(BaseModel):
    entity: str = Field(..., description="Entity name (e.g. 'asset', 'solution')")
    feature_description: str = Field(
        "", description="Brief description of the new test case feature"
    )
    include_file_types: list[str] = Field(
        default_factory=list,
        description="Restrict to specific file types; empty = all",
    )
    max_scenarios: int = Field(5, description="Number of similar existing scenarios to include")


class HelpTopicQueryRequest(BaseModel):
    query: str = Field(..., description="Semantic search query over SDP help guide topics")
    module: Optional[str] = Field(None, description="Filter by module (e.g. 'requests', 'changes', 'assets')")
    type: Optional[str] = Field(None, description="Filter by record type: 'field', 'steps', or 'full_text'")
    top_k: int = Field(8, description="Max results to return")


class IndexRequest(BaseModel):
    reset: bool = Field(False, description="If true, wipe and rebuild from scratch")
    reset_scenarios: bool = Field(False, description="If true, also reset the scenarios collection")


# ── Helpers ────────────────────────────────────────────────────────────────────

FILE_TYPE_ORDER = [
    "LOCATORS", "FIELDS", "DATA_CONSTANTS", "CONSTANTS",
    "ENTITY", "BASE", "PREPROCESS", "FORM_UTIL",
    "API_UTIL", "ACTIONS_UTIL",
    "DATA_JSON", "CONF_JSON",
    "SKELETON", "SKELETON_JSON", "OTHER",
]


def _order_files(files: dict) -> dict:
    """Return files dict sorted by canonical file-type order."""
    ordered = {}
    for ft in FILE_TYPE_ORDER:
        if ft in files:
            ordered[ft] = files[ft]
    for ft in files:
        if ft not in ordered:
            ordered[ft] = files[ft]
    return ordered


def _build_generation_prompt_context(
    entity: str,
    feature_description: str,
    store: VectorStore,
    max_scenarios: int = 5,
    include_file_types: list[str] | None = None,
) -> dict:
    """
    Assemble a structured context dict for the Coder Agent LLM prompt.
    Contains:
      - source_files: { LOCATORS: [...], FIELDS: [...], ... } (full chunks)
      - similar_scenarios: [ { method_name, description, module_path, ... } ]
      - skeleton: { SKELETON: [...] }
      - meta: { entity, feature_description, scenario_count, source_file_count }
    """
    # 1. Full entity source files
    full_ctx = store.get_entity_full_context(entity)
    files = _order_files(full_ctx.get("files", {}))

    # 2. Filter by file types if requested
    if include_file_types:
        files = {ft: chunks for ft, chunks in files.items() if ft in include_file_types}

    # 3. Skeleton templates (always included)
    skeleton_ctx = store.get_entity_full_context("skeleton")
    skeleton_files = skeleton_ctx.get("files", {})

    # 4. Similar existing scenarios (semantic search)
    similar_scenarios = []
    if store.scenario_count > 0 and feature_description:
        query_text = f"{entity} {feature_description}"
        results = store.search_scenarios(query_text, top_k=max_scenarios)
        # Also try entity-specific module path filter
        entity_results = store.search_scenarios(
            query_text, top_k=max_scenarios,
            module_filter=f"modules/{entity}",
        ) if results else []
        # Merge and deduplicate
        seen_ids = set()
        for r in (entity_results + results):
            if r["id"] not in seen_ids:
                similar_scenarios.append({
                    "method_name":   r["metadata"].get("method_name", ""),
                    "description":   r["metadata"].get("description", ""),
                    "module_path":   r["metadata"].get("module_path", ""),
                    "priority":      r["metadata"].get("priority", ""),
                    "group":         r["metadata"].get("group", ""),
                    "relevance":     round(1 - r["distance"], 4),
                })
                seen_ids.add(r["id"])
                if len(similar_scenarios) >= max_scenarios:
                    break

    # 5. Help guide topics — field definitions, workflow steps, feature overview
    _MODULE_PATH_TO_HELP = {
        'purchaseorders': 'purchase',
        'admin':          'setup',
        'releasechecklist': 'releases',
    }
    help_module = _MODULE_PATH_TO_HELP.get(entity, entity)
    help_context: list[dict] = []
    if store.help_topic_count > 0 and feature_description:
        help_context = store.search_help_topics(
            feature_description, module_filter=help_module, top_k=10
        )
        if not help_context:
            help_context = store.search_help_topics(feature_description, top_k=6)

    # 6. Count total content
    total_source_chunks = sum(len(v) for v in files.values())

    return {
        "meta": {
            "entity":              entity,
            "feature_description": feature_description,
            "source_chunks":       total_source_chunks,
            "scenario_count":      len(similar_scenarios),
            "help_topic_count":    len(help_context),
        },
        "source_files":      files,
        "similar_scenarios": similar_scenarios,
        "skeleton":          skeleton_files,
        "help_context":      help_context,
    }


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/health", tags=["System"])
def health():
    """Liveness probe."""
    store = get_store()
    return {
        "status":       "ok",
        "scenarios":    store.scenario_count,
        "source_files": store.source_file_count,
        "help_topics":  store.help_topic_count,
    }


@app.get("/api/rag/stats", tags=["System"])
def stats():
    """Return collection counts."""
    store = get_store()
    entities = store.list_indexed_entities()
    return {
        "scenarios":    store.scenario_count,
        "source_files": store.source_file_count,
        "help_topics":  store.help_topic_count,
        "entities":     len(entities),
        "entity_list":  entities,
    }


@app.get("/api/rag/modules", tags=["Modules"])
@app.get("/api/rag/entities", tags=["Modules"])
def list_entities():
    """List all entities that have source files indexed in the vector store."""
    store = get_store()
    entities = store.list_indexed_entities()
    return {"entities": entities, "count": len(entities)}


@app.get("/api/rag/entity/{entity}", tags=["Context"])
def get_entity_context(entity: str, file_type: Optional[str] = None):
    """
    Return all source file chunks for an entity, optionally filtered by file_type.

    - **entity**: Entity name, e.g. `asset`, `solution`, `incident`
    - **file_type**: Optional filter — one of `LOCATORS`, `FIELDS`, `DATA_CONSTANTS`,
      `CONSTANTS`, `BASE`, `ENTITY`, `API_UTIL`, `ACTIONS_UTIL`, `SKELETON`, etc.
    """
    store = get_store()
    ctx = store.get_entity_full_context(entity)
    files = _order_files(ctx.get("files", {}))

    if file_type:
        ft = file_type.upper()
        if ft not in files:
            raise HTTPException(
                status_code=404,
                detail=f"No chunks of type '{ft}' found for entity '{entity}'. "
                       f"Available types: {list(files.keys())}",
            )
        files = {ft: files[ft]}

    total_chunks = sum(len(v) for v in files.values())
    if total_chunks == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No source files indexed for entity '{entity}'. "
                   f"Run POST /api/rag/index first.",
        )

    return {
        "entity": entity,
        "total_chunks": total_chunks,
        "files": files,
    }


@app.get("/api/rag/skeleton", tags=["Context"])
def get_skeleton():
    """Return all indexed skeleton template chunks (canonical file structure)."""
    store = get_store()
    ctx = store.get_entity_full_context("skeleton")
    files = ctx.get("files", {})
    total_chunks = sum(len(v) for v in files.values())
    return {"entity": "skeleton", "total_chunks": total_chunks, "files": files}


@app.post("/api/rag/query", tags=["Search"])
def query_source_files(req: SourceQueryRequest):
    """
    Semantic search over source file chunks.

    - **query**: Natural language query, e.g. `"locator for asset name field"`
    - **entity**: Optional entity filter, e.g. `"asset"`
    - **file_type**: Optional file-type filter, e.g. `"LOCATORS"`
    - **top_k**: Number of results (default 10)
    """
    store = get_store()
    results = store.search_source_files(
        query=req.query,
        entity_filter=req.entity,
        file_type_filter=req.file_type,
        top_k=req.top_k,
    )
    return {
        "query":    req.query,
        "filters":  {"entity": req.entity, "file_type": req.file_type},
        "results":  results,
        "count":    len(results),
    }


@app.post("/api/rag/scenarios/query", tags=["Search"])
def query_scenarios(req: ScenarioQueryRequest):
    """
    Semantic search over existing test scenario descriptions.

    - **query**: Natural language query, e.g. `"create asset with custom field"`
    - **entity**: Optional entity filter (used to build module_path prefix)
    - **top_k**: Number of results (default 10)
    """
    store = get_store()
    if store.scenario_count == 0:
        return {"query": req.query, "results": [], "count": 0,
                "warning": "No scenarios indexed yet. Run POST /api/rag/index first."}

    # Try with entity-level module path filter first
    results = []
    if req.entity:
        results = store.search_scenarios(
            req.query, top_k=req.top_k,
            module_filter=f"modules/{req.entity}",
        )
    if not results:
        results = store.search_scenarios(req.query, top_k=req.top_k)

    return {
        "query":   req.query,
        "filters": {"entity": req.entity},
        "results": [
            {
                "method_name":   r["metadata"].get("method_name", ""),
                "description":   r["metadata"].get("description", ""),
                "module_path":   r["metadata"].get("module_path", ""),
                "priority":      r["metadata"].get("priority", ""),
                "group":         r["metadata"].get("group", ""),
                "class_name":    r["metadata"].get("class_name", ""),
                "relevance":     round(1 - r["distance"], 4),
            }
            for r in results
        ],
        "count": len(results),
    }


@app.post("/api/rag/help/search", tags=["Search"])
def search_help_topics(req: HelpTopicQueryRequest):
    """
    Semantic search over the SDP help guide (fields, steps, overviews).

    - **query**: Natural language query, e.g. `"priority field options for incident"`
    - **module**: Optional module filter — `requests`, `changes`, `assets`, `solutions`, etc.
    - **type**: Optional type filter — `field`, `steps`, or `full_text`
    - **top_k**: Number of results (default 8)
    """
    store = get_store()
    if store.help_topic_count == 0:
        return {"query": req.query, "results": [], "count": 0,
                "warning": "No help topics indexed yet. Run python ingestion/help_doc_crawler.py first."}
    results = store.search_help_topics(
        query=req.query,
        module_filter=req.module,
        type_filter=req.type,
        top_k=req.top_k,
    )
    return {
        "query":   req.query,
        "filters": {"module": req.module, "type": req.type},
        "results": results,
        "count":   len(results),
    }


@app.post("/api/rag/generation-context", tags=["Generation"])
def generation_context(req: GenerationContextRequest):
    """
    Build a full, LLM-ready generation context for a given entity.

    Returns:
    - **source_files**: All source file chunks grouped by file type (LOCATORS, FIELDS, etc.)
    - **similar_scenarios**: Top-N existing scenarios most similar to the feature description
    - **skeleton**: Canonical skeleton templates
    - **meta**: Statistics about the returned context

    This is the primary endpoint used by the Coder Agent before generating new test cases.
    """
    store = get_store()
    ctx = _build_generation_prompt_context(
        entity=req.entity,
        feature_description=req.feature_description,
        store=store,
        max_scenarios=req.max_scenarios,
        include_file_types=req.include_file_types or None,
    )
    return ctx


@app.post("/api/rag/index", tags=["System"])
def trigger_index(req: IndexRequest, background_tasks: BackgroundTasks):
    """
    Trigger a full re-index of source files and scenarios.
    Runs in the background so the request returns immediately.

    - **reset**: Wipe and rebuild the `automater_source_files` collection
    - **reset_scenarios**: Also wipe and rebuild `automater_scenarios`
    """
    def _run_index():
        try:
            from knowledge_base.rag_indexer import RagIndexer
            indexer = RagIndexer(base_dir=str(_ROOT))
            indexer.run(
                reset_source_files=req.reset,
                reset_scenarios=req.reset_scenarios,
            )
            # Refresh the singleton store so counts update immediately
            global _store
            _store = VectorStore(persist_dir=str(_ROOT / "knowledge_base/chroma_db"))
        except Exception as ex:
            print(f"[RAG Index] ⚠️  Indexing failed: {ex}")

    background_tasks.add_task(_run_index)
    return {
        "status":  "indexing_started",
        "message": "Indexing is running in the background. "
                   "Check GET /api/rag/stats for progress.",
    }


# ── Script entry point ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("RAG_PORT", "8765"))
    print(f"\n🚀 Starting AutomaterSelenium RAG Server on http://0.0.0.0:{port}")
    print(f"   Docs: http://localhost:{port}/docs\n")
    uvicorn.run(
        "knowledge_base.rag_server:app",
        host="0.0.0.0",
        port=port,
        reload=False,
        log_level="info",
    )
