"""
web/server.py
-------------
FastAPI backend for the AI Test Generation Web UI.

Endpoints:
  GET  /                          → serves index.html
  GET  /api/health                → health check
  POST /api/generate              → start a pipeline run (text or file upload)
  GET  /api/stream/{run_id}       → SSE stream of live log messages
  GET  /api/runs                  → list all past runs
  GET  /api/runs/{run_id}         → full details for one run
  GET  /api/runs/{run_id}/file    → download a specific generated .java file
  GET  /api/modules               → list available SDP modules from taxonomy

Run with:
  cd ai-automation-qa
  source .venv/bin/activate
  python web/server.py
  # or:
  uvicorn web.server:app --host 0.0.0.0 --port 9500 --reload
"""

import asyncio
import json
import os
import shutil
import sys
import tempfile
import threading
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

import yaml
import uvicorn
from dotenv import load_dotenv
from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles

# ── Bootstrap paths ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))
load_dotenv(BASE_DIR / ".env")

from config.project_config import BASE_DIR as PROJECT_BASE_DIR, HG_AGENT_ENABLED

# ── In-memory run store ───────────────────────────────────────────────────────
# run_id → {status, messages, errors, files, metadata, started_at, finished_at}
_runs: dict[str, dict] = {}
# run_id → asyncio.Queue  (SSE message bus)
_queues: dict[str, asyncio.Queue] = {}
# run_id → background thread (for manual stop / cancellation)
_threads: dict[str, threading.Thread] = {}
# The event loop that the server runs on (set at startup)
_loop: asyncio.AbstractEventLoop | None = None

UPLOAD_DIR = BASE_DIR / "web" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".xlsx", ".xls", ".pptx", ".txt", ".md"}


# ── App ───────────────────────────────────────────────────────────────────────
app = FastAPI(title="AI Test Generator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (index.html etc.) from web/static/
static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# ── Pipeline singleton (built once at startup, reused for every request) ─────
_pipeline = None   # CompiledStateGraph — populated in on_startup


# ── Startup / shutdown ───────────────────────────────────────────────────────
@app.on_event("startup")
async def on_startup():
    global _loop, _pipeline
    _loop = asyncio.get_running_loop()

    # Build the pipeline in a thread so the event loop isn't blocked
    import concurrent.futures
    from agents.pipeline import build_pipeline
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        _pipeline = await loop.run_in_executor(pool, build_pipeline, str(BASE_DIR))
    print(f"[Server] ✅ Pipeline ready (ChromaDB + agents loaded)")


# ── Helpers ───────────────────────────────────────────────────────────────────
def _push(run_id: str, event_type: str, data: Any):
    """Thread-safe push to the SSE queue for a given run."""
    q = _queues.get(run_id)
    if q and _loop:
        payload = json.dumps({"type": event_type, "data": data})
        asyncio.run_coroutine_threadsafe(q.put(payload), _loop)


def _run_pipeline_thread(
    run_id: str,
    feature_description: str,
    source_document: str,
    target_modules: list[str],
    generation_mode: str,
    hg_config: dict,
):
    """
    Runs the pipeline synchronously in a worker thread.
    Uses the pre-built _pipeline singleton (loaded at startup) — no cold-start delay.
    All log messages are pushed to the SSE queue.
    """
    run = _runs[run_id]
    run["status"] = "running"
    _threads[run_id] = threading.current_thread()

    def _log(msg: str):
        run["messages"].append(msg)
        _push(run_id, "log", msg)

    _log(f"[{datetime.now().strftime('%H:%M:%S')}] 🚀 Pipeline started")
    if source_document:
        _log(f"[{datetime.now().strftime('%H:%M:%S')}] 📄 Document: {Path(source_document).name}")
    if feature_description:
        _log(f"[{datetime.now().strftime('%H:%M:%S')}] 📝 Feature: {feature_description[:120]}...")
    _log(f"[{datetime.now().strftime('%H:%M:%S')}] 🔧 Mode: {generation_mode} | Modules: {', '.join(target_modules) or 'auto-detect'}")

    try:
        from agents.pipeline import _build_initial_state
        initial_state = _build_initial_state(
            feature_description=feature_description,
            source_document=source_document,
            target_modules=target_modules,
            generation_mode=generation_mode,
            hg_config=hg_config,
        )
        final_state = _pipeline.invoke(initial_state)

        # Stream all pipeline messages
        for msg in final_state.get("messages", []):
            _log(msg)

        # Stream errors if any
        for err in final_state.get("errors", []):
            run["errors"].append(err)
            _push(run_id, "error", err)

        # Collect generated files
        output_paths = final_state.get("final_output_paths", [])
        run["files"] = output_paths
        run["generated_dir"] = final_state.get("generated_dir", "")
        run["document_metadata"] = final_state.get("document_metadata", {})
        run["affected_modules"] = final_state.get("affected_modules", [])
        run["hg_result"] = final_state.get("hg_result", {})

        # Log hg branch if committed
        hg_res = run["hg_result"]
        if hg_res.get("branch_name"):
            branch = hg_res['branch_name']
            if hg_res.get("success"):
                _log(f"[{datetime.now().strftime('%H:%M:%S')}] 🔀 hg branch: {branch} — {hg_res.get('message','')}")
            else:
                _log(f"[{datetime.now().strftime('%H:%M:%S')}] ⚠️ hg partial: {hg_res.get('message','')}")

        file_count = len(output_paths)
        had_errors = bool(final_state.get("errors"))

        if file_count > 0:
            run["status"] = "success"
            _log(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Done — {file_count} file(s) generated")
            _push(run_id, "files", output_paths)
        elif had_errors:
            run["status"] = "failed"
            _log(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ Pipeline finished with errors — check details")
        else:
            run["status"] = "success"
            _log(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ Pipeline complete (no new files — may be duplicates)")

    except SystemExit:
        # Raised by /api/runs/{run_id}/stop endpoint via ctypes
        if run["status"] != "stopped":
            run["status"] = "stopped"
        _log(f"[{datetime.now().strftime('%H:%M:%S')}] ⏹ Generation stopped manually")

    except Exception as exc:
        run["status"] = "failed"
        err_msg = f"Pipeline error: {exc}"
        run["errors"].append(err_msg)
        _log(f"[{datetime.now().strftime('%H:%M:%S')}] ❌ {err_msg}")
        _push(run_id, "error", err_msg)

    finally:
        run["finished_at"] = datetime.now().isoformat()
        _threads.pop(run_id, None)
        _push(run_id, "done", {"status": run["status"], "files": run.get("files", []), "hg_branch": run.get("hg_result", {}).get("branch_name", "")})
        # Signal SSE stream to close
        _push(run_id, "__close__", None)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve the main Web UI."""
    html_path = Path(__file__).parent / "static" / "index.html"
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "1.0.0", "runs": len(_runs), "hg_agent_enabled": HG_AGENT_ENABLED}


@app.get("/api/modules")
async def list_modules():
    """Return available SDP modules from the taxonomy file."""
    taxonomy_path = BASE_DIR / "config" / "module_taxonomy.yaml"
    try:
        with open(taxonomy_path) as f:
            taxonomy = yaml.safe_load(f)
        modules = []
        for top_mod, mod_def in taxonomy.get("top_level_modules", {}).items():
            entities = mod_def.get("entities", [])
            for entity in entities:
                modules.append(f"{top_mod}/{entity}")
        return {"modules": sorted(modules)}
    except Exception as e:
        return {"modules": [], "error": str(e)}


@app.post("/api/generate")
async def generate(
    background_tasks: BackgroundTasks,
    feature: str = Form(default=""),
    modules: str = Form(default=""),
    mode: str = Form(default="new_feature"),
    hg_enabled: bool = Form(default=False),
    file: Optional[UploadFile] = File(default=None),
):
    """
    Start a pipeline run. Accepts either:
      - A text feature description (form field: feature)
      - A document file upload (PDF/DOCX/XLSX/PPTX/TXT)
      - Or both (document takes precedence, feature text is merged in)
    Returns immediately with a run_id. Client polls /api/stream/{run_id} for SSE.
    """
    # Validate
    if not feature.strip() and (file is None or not file.filename):
        raise HTTPException(400, "Provide a feature description or upload a document file.")

    # Handle file upload
    source_document = ""
    if file and file.filename:
        ext = Path(file.filename).suffix.lower()
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                400,
                f"Unsupported file type '{ext}'. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        save_path = UPLOAD_DIR / f"{uuid.uuid4().hex}{ext}"
        with open(save_path, "wb") as f_out:
            shutil.copyfileobj(file.file, f_out)
        source_document = str(save_path)

    # Parse modules
    target_modules = [m.strip() for m in modules.split(",") if m.strip()]

    # Build hg_config — gate on global config flag first
    hg_config = {"push": True} if (hg_enabled and HG_AGENT_ENABLED) else {}

    # Create run record
    run_id = uuid.uuid4().hex[:12]
    _runs[run_id] = {
        "run_id":          run_id,
        "status":          "queued",
        "feature":         feature[:200] if feature else "",
        "source_document": Path(source_document).name if source_document else "",
        "mode":            mode,
        "hg_enabled":      hg_enabled,
        "target_modules":  target_modules,
        "messages":        [],
        "errors":          [],
        "files":           [],
        "generated_dir":   "",
        "affected_modules":[],
        "document_metadata": {},
        "hg_result":       {},
        "started_at":      datetime.now().isoformat(),
        "finished_at":     None,
    }
    _queues[run_id] = asyncio.Queue()

    # Launch pipeline in a background thread (it's sync)
    thread = threading.Thread(
        target=_run_pipeline_thread,
        args=(run_id, feature.strip(), source_document, target_modules, mode, hg_config),
        daemon=True,
    )
    thread.start()

    return {"run_id": run_id, "status": "queued"}


@app.get("/api/stream/{run_id}")
async def stream_run(run_id: str):
    """
    Server-Sent Events stream for a running pipeline.
    Each event is a JSON string: {"type": "log"|"error"|"files"|"done", "data": ...}
    """
    if run_id not in _runs:
        raise HTTPException(404, f"Run '{run_id}' not found")

    queue = _queues.get(run_id)
    if queue is None:
        # Run already finished — stream the stored logs immediately
        run = _runs[run_id]

        async def finished_stream():
            for msg in run["messages"]:
                yield f"data: {json.dumps({'type': 'log', 'data': msg})}\n\n"
            for err in run["errors"]:
                yield f"data: {json.dumps({'type': 'error', 'data': err})}\n\n"
            yield f"data: {json.dumps({'type': 'files', 'data': run['files']})}\n\n"
            yield f"data: {json.dumps({'type': 'done', 'data': {'status': run['status'], 'files': run['files']}})}\n\n"

        return StreamingResponse(finished_stream(), media_type="text/event-stream")

    async def live_stream():
        try:
            while True:
                try:
                    payload = await asyncio.wait_for(queue.get(), timeout=30.0)
                    msg_obj = json.loads(payload)
                    yield f"data: {payload}\n\n"
                    if msg_obj.get("type") == "__close__":
                        break
                except asyncio.TimeoutError:
                    # Heartbeat to keep connection alive
                    yield f"data: {json.dumps({'type': 'heartbeat', 'data': ''})}\n\n"
        finally:
            # Clean up queue after streaming ends
            _queues.pop(run_id, None)

    return StreamingResponse(live_stream(), media_type="text/event-stream")


@app.get("/api/runs")
async def list_runs():
    """Return summary of all runs, newest first."""
    runs = sorted(_runs.values(), key=lambda r: r["started_at"], reverse=True)
    return {
        "runs": [
            {
                "run_id":          r["run_id"],
                "status":          r["status"],
                "feature":         r["feature"],
                "source_document": r["source_document"],
                "mode":            r["mode"],
                "files_count":     len(r["files"]),
                "started_at":      r["started_at"],
                "finished_at":     r["finished_at"],
            }
            for r in runs
        ]
    }


@app.post("/api/runs/{run_id}/stop")
async def stop_run(run_id: str):
    """
    Manually stop a running pipeline.
    Injects SystemExit into the worker thread via ctypes, updates status to 'stopped',
    and pushes a done event to the SSE stream.
    """
    if run_id not in _runs:
        raise HTTPException(404, f"Run '{run_id}' not found")
    run = _runs[run_id]
    if run["status"] not in ("running", "queued"):
        raise HTTPException(400, f"Run is not active (status: {run['status']})")

    # Mark stopped immediately so the thread's finally block won't overwrite it
    run["status"] = "stopped"
    run["finished_at"] = datetime.now().isoformat()

    # Inject SystemExit into the worker thread
    thread = _threads.get(run_id)
    if thread and thread.is_alive():
        import ctypes
        ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_ulong(thread.ident),
            ctypes.py_object(SystemExit),
        )

    # Push final events to SSE so the UI updates
    _push(run_id, "log", f"[{datetime.now().strftime('%H:%M:%S')}] ⏹ Generation stopped manually")
    _push(run_id, "done", {"status": "stopped", "files": run.get("files", []), "hg_branch": ""})
    _push(run_id, "__close__", None)

    return {"run_id": run_id, "status": "stopped"}


@app.get("/api/runs/{run_id}")
async def get_run(run_id: str):
    """Return full details for a run including generated file paths."""
    if run_id not in _runs:
        raise HTTPException(404, f"Run '{run_id}' not found")
    return _runs[run_id]


@app.get("/api/runs/{run_id}/file")
async def download_file(run_id: str, path: str):
    """
    Download a generated .java file.
    ?path=absolute-or-relative filepath
    """
    if run_id not in _runs:
        raise HTTPException(404, f"Run '{run_id}' not found")
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = BASE_DIR / path
    if not file_path.exists():
        raise HTTPException(404, f"File not found: {path}")
    return FileResponse(str(file_path), filename=file_path.name, media_type="text/plain")


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n🌐 AI Test Generator Web UI")
    print(f"   Open: http://localhost:9500\n")
    uvicorn.run(
        "web.server:app",
        host="0.0.0.0",
        port=9500,
        reload=False,
        log_level="info",
    )
