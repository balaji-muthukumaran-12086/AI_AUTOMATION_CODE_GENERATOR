"""
web/breakage_api.py
-------------------
Backend for the Breakage Analyzer UI. Handles:
  - GET  /api/breakage/projects     → list existing cloned projects
  - POST /api/breakage/clone        → clone a new branch from hg
  - GET  /api/breakage/clone/stream → SSE stream of clone progress
  - POST /api/breakage/upload       → upload Aalam HTML report, parse, generate manifest
  - POST /api/breakage/run          → start rerun of breakage cases in background
  - GET  /api/breakage/stream/:id   → SSE stream of live rerun progress
  - GET  /api/breakage/manifest     → return current breakage_rerun.json
  - GET  /api/breakage/results      → return breakage_results.json
  - POST /api/breakage/stop/:id     → stop a running analysis
  - GET  /api/breakage/report       → return the latest AI report HTML path
"""

import asyncio
import json
import os
import re
import shutil
import subprocess
import threading
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Query
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR

import sys
sys.path.insert(0, str(BASE_DIR))
from config.project_config import (
    PROJECT_NAME as DEFAULT_PROJECT_NAME, DEPS_DIR,
    HG_REPO_URL,
)
from root_cause_analyzer import diagnose_failure as _diagnose_failure

# ── Hardcoded credentials (common across all automation builds) ───────────────
SDP_ADMIN_EMAIL = "jaya.kumar+org1admin1t0@zohotest.com"
SDP_EMAIL_ID = "jaya.kumar+org1user1t0@zohotest.com"
SDP_PORTAL = "portal1"
SDP_ADMIN_PASS = "Zoho@135"
SDP_TEST_USER_EMAILS = (
    "jaya.kumar+uorg1user2@zohotest.com,"
    "jaya.kumar+uorg1user3@zohotest.com,"
    "jaya.kumar+uorg1user4@zohotest.com,"
    "jaya.kumar+uorg1user5@zohotest.com"
)

UPLOAD_DIR = BASE_DIR / "web" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Known prefixes for automation project folders
_PROJECT_PREFIXES = ("SDPLIVE_", "AALAM_", "MSP_", "SDP_")
_EXCLUDE_DIRS = frozenset({
    "AutomaterSeleniumFramework", "AutomaterSelenium", ".venv", "node_modules",
    "agents", "config", "docs", "web", "templates", "knowledge_base",
    "evaluation", "ingestion", "orchestrator", "dependencies",
})

# ── In-memory state ───────────────────────────────────────────────────────────
# run_id → { status, logs: [], queue, stop_event, done: bool, project_name: str }
_analyses: dict[str, dict] = {}
# clone_id → { status, logs: [], queue, done: bool }
_clones: dict[str, dict] = {}
_loop: Optional[asyncio.AbstractEventLoop] = None

router = APIRouter(prefix="/api/breakage", tags=["breakage"])


# ── Helpers ───────────────────────────────────────────────────────────────────

def _project_paths(project_name: str):
    """Derive all paths for a given project folder name."""
    root = BASE_DIR / project_name
    return {
        "root": root,
        "bin": root / "bin",
        "src": root / "src",
        "resources": root / "resources",
        "reports": root / "reports",
        "manifest": root / "breakage_rerun.json",
        "results": root / "breakage_results.json",
        "ai_reports": root / "ai_reports",
    }


def _validate_project_name(name: str) -> str:
    """Sanitize and validate a project folder name (prevent path traversal)."""
    safe = re.sub(r'[^a-zA-Z0-9_\-]', '', name)
    if safe != name or not safe:
        raise HTTPException(400, "Invalid project name")
    return safe


def _derive_project_name(branch: str) -> str:
    """Extract folder-safe name from branch: feature/SDPLIVE_FOO → SDPLIVE_FOO"""
    name = branch.rsplit("/", 1)[-1] if "/" in branch else branch
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)


# ── SSE helpers ───────────────────────────────────────────────────────────────

def _push(run_id: str, event_type: str, data, level: str = "info", store: str = "_analyses"):
    """Thread-safe push to an SSE queue (works for both _analyses and _clones)."""
    registry = _analyses if store == "_analyses" else _clones
    state = registry.get(run_id)
    if not state or not _loop:
        return
    if event_type == "log":
        payload = json.dumps({"type": "log", "data": data, "level": level})
    elif event_type == "test_update":
        payload = json.dumps({"type": "test_update", "data": data})
    elif event_type == "done":
        payload = json.dumps({"type": "done", "data": data})
    else:
        payload = json.dumps({"type": event_type, "data": data})
    state["logs"].append(payload)
    q = state.get("queue")
    if q:
        asyncio.run_coroutine_threadsafe(q.put(payload), _loop)


def _log(run_id: str, msg: str, level: str = "info", store: str = "_analyses"):
    _push(run_id, "log", msg, level, store)


def _run_cmd(log_id: str, cmd: str, cwd: str = None, timeout: int = 300,
             mask: str = None, store: str = "_analyses") -> tuple:
    """Run a shell command, stream output to SSE, return (rc, output)."""
    _log(log_id, f"$ {cmd if not mask else cmd.replace(mask, '****')}", "info", store)
    try:
        proc = subprocess.run(
            cmd, shell=True, capture_output=True, text=True,
            cwd=cwd or str(WORKSPACE_DIR), timeout=timeout,
        )
        output = (proc.stdout + proc.stderr).strip()
        if mask:
            output = output.replace(mask, "****")
        for line in output.splitlines()[-20:]:  # Last 20 lines
            _log(log_id, line, "info" if proc.returncode == 0 else "error", store)
        return proc.returncode, output
    except subprocess.TimeoutExpired:
        _log(log_id, f"Command timed out after {timeout}s", "error", store)
        return 1, "timeout"
    except Exception as e:
        _log(log_id, f"Command failed: {e}", "error", store)
        return 1, str(e)


# ── Project Listing ───────────────────────────────────────────────────────────

@router.get("/projects")
async def list_projects():
    """List existing cloned project folders in the workspace."""
    projects = []
    for d in WORKSPACE_DIR.iterdir():
        if not d.is_dir() or d.name in _EXCLUDE_DIRS:
            continue
        if d.name.startswith(_PROJECT_PREFIXES) or (d / "src").is_dir():
            has_bin = (d / "bin").is_dir()
            has_src = (d / "src").is_dir()
            has_manifest = (d / "breakage_rerun.json").is_file()
            projects.append({
                "name": d.name,
                "has_bin": has_bin,
                "has_src": has_src,
                "has_manifest": has_manifest,
                "is_active": d.name == DEFAULT_PROJECT_NAME,
            })
    return {"projects": sorted(projects, key=lambda p: p["name"])}


# ── Clone Project ─────────────────────────────────────────────────────────────

class CloneRequest(BaseModel):
    branch: str
    hg_username: str
    hg_password: str  # transient — used only for clone


@router.post("/clone")
async def start_clone(req: CloneRequest):
    """Clone a branch from hg. Returns clone_id for SSE streaming."""
    global _loop
    if _loop is None:
        _loop = asyncio.get_running_loop()

    if not req.branch or not req.hg_username or not req.hg_password:
        raise HTTPException(400, "branch, hg_username, and hg_password are required")

    project_name = _derive_project_name(req.branch)
    project_dir = WORKSPACE_DIR / project_name

    clone_id = uuid.uuid4().hex[:12]
    _clones[clone_id] = {
        "status": "running",
        "logs": [],
        "queue": asyncio.Queue(),
        "done": False,
        "project_name": project_name,
    }

    t = threading.Thread(
        target=_execute_clone,
        args=(clone_id, req.branch, req.hg_username, req.hg_password, project_name),
        daemon=True,
    )
    t.start()

    return {"clone_id": clone_id, "project_name": project_name}


def _execute_clone(clone_id: str, branch: str, hg_user: str, hg_pass: str, project_name: str):
    """Background thread: clone the branch, compile framework."""
    state = _clones[clone_id]
    store = "_clones"
    project_dir = WORKSPACE_DIR / project_name

    try:
        if project_dir.exists() and (project_dir / "src").is_dir():
            _log(clone_id, f"Folder {project_name}/ already exists — pulling latest...", "info", store)
            # Build auth args
            _hg_auth = (
                f'--config auth.tmp.prefix=zrepository.zohocorpcloud.in '
                f'--config auth.tmp.username="{hg_user}" '
                f'--config auth.tmp.password="{hg_pass}" '
                f'--config auth.tmp.schemes=https'
            )
            _run_cmd(clone_id, f'hg pull {_hg_auth} 2>&1 || true',
                     cwd=str(project_dir), mask=hg_pass, store=store)
            _run_cmd(clone_id, f'hg update "{branch}" 2>&1 || true',
                     cwd=str(project_dir), mask=hg_pass, store=store)
            _log(clone_id, "Updated to latest", "success", store)
        else:
            _log(clone_id, f"Cloning branch '{branch}' into {project_name}/...", "info", store)

            repo_url = HG_REPO_URL
            _hg_auth = (
                f'--config auth.tmp.prefix=zrepository.zohocorpcloud.in '
                f'--config auth.tmp.username="{hg_user}" '
                f'--config auth.tmp.password="{hg_pass}" '
                f'--config auth.tmp.schemes=https'
            )
            rc, output = _run_cmd(
                clone_id,
                f'hg clone {_hg_auth} --branch "{branch}" "{repo_url}" "{project_name}" 2>&1',
                cwd=str(WORKSPACE_DIR), timeout=600, mask=hg_pass, store=store,
            )

            if rc != 0:
                if "authorization" in output.lower() or "401" in output:
                    _push(clone_id, "done", {"success": False, "error": "Authentication failed — check hg credentials"}, store=store)
                    state["status"] = "done"
                    state["done"] = True
                    return
                else:
                    _push(clone_id, "done", {"success": False, "error": f"Clone failed: {output[-200:]}"}, store=store)
                    state["status"] = "done"
                    state["done"] = True
                    return

            _log(clone_id, "Clone successful", "success", store)

        # Compile framework for this project
        _log(clone_id, "Compiling framework classes...", "info", store)
        env = os.environ.copy()
        env["PROJECT_NAME"] = project_name
        try:
            proc = subprocess.run(
                "./setup_framework_bin.sh",
                shell=True, capture_output=True, text=True,
                cwd=str(WORKSPACE_DIR), timeout=120, env=env,
            )
            if proc.returncode == 0:
                _log(clone_id, "Framework compiled successfully", "success", store)
            else:
                _log(clone_id, "Framework compilation had issues (non-critical)", "warn", store)
                for line in (proc.stdout + proc.stderr).strip().splitlines()[-5:]:
                    _log(clone_id, line, "warn", store)
        except Exception as e:
            _log(clone_id, f"Framework compilation failed: {e}", "warn", store)

        # Compile ALL module source files into bin/ (required for test execution)
        _log(clone_id, "Compiling module classes...", "info", store)
        try:
            project_root = WORKSPACE_DIR / project_name
            src_dir = project_root / "src"
            bin_dir = project_root / "bin"
            java_files = list(src_dir.rglob("*.java"))
            _log(clone_id, f"Found {len(java_files)} source files to compile", "info", store)

            if java_files:
                # Build classpath: bin/ + all JARs
                cp_parts = [str(bin_dir)]
                for jar in DEPS_DIR.rglob("*.jar"):
                    cp_parts.append(str(jar))
                classpath = ":".join(cp_parts)

                # Write file list to temp file for javac @argfile
                import tempfile
                with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as tf:
                    for jf in java_files:
                        tf.write(str(jf) + "\n")
                    argfile = tf.name

                proc = subprocess.run(
                    ["javac", "-encoding", "UTF-8", "-cp", classpath, "-d", str(bin_dir), f"@{argfile}"],
                    capture_output=True, text=True, cwd=str(WORKSPACE_DIR), timeout=300,
                )
                os.unlink(argfile)

                if proc.returncode == 0:
                    class_count = sum(1 for _ in bin_dir.rglob("*.class"))
                    _log(clone_id, f"Module compilation successful — {class_count} classes in bin/", "success", store)
                else:
                    # Count errors vs warnings
                    error_lines = [l for l in proc.stderr.splitlines() if ": error:" in l]
                    _log(clone_id, f"Module compilation had {len(error_lines)} errors (some tests may still work)", "warn", store)
                    for line in proc.stderr.strip().splitlines()[-5:]:
                        _log(clone_id, line, "warn", store)
        except Exception as e:
            _log(clone_id, f"Module compilation failed: {e}", "warn", store)

        # Add to .gitignore if not there
        gitignore_path = WORKSPACE_DIR / ".gitignore"
        entry = f"{project_name}/"
        if gitignore_path.exists():
            content = gitignore_path.read_text(encoding="utf-8")
            if entry not in content:
                with open(gitignore_path, "a", encoding="utf-8") as f:
                    f.write(f"\n{entry}\n")

        _log(clone_id, f"Project '{project_name}' is ready", "success", store)
        _push(clone_id, "done", {"success": True, "project_name": project_name}, store=store)

    except Exception as e:
        _log(clone_id, f"Clone failed: {e}", "error", store)
        _push(clone_id, "done", {"success": False, "error": str(e)}, store=store)

    state["status"] = "done"
    state["done"] = True


@router.get("/clone/stream/{clone_id}")
async def stream_clone(clone_id: str):
    """SSE endpoint for streaming clone progress."""
    state = _clones.get(clone_id)
    if not state:
        raise HTTPException(404, "Clone session not found")

    async def event_generator():
        q = state["queue"]
        for log_entry in list(state["logs"]):
            yield f"data: {log_entry}\n\n"
        while True:
            try:
                msg = await asyncio.wait_for(q.get(), timeout=2.0)
                yield f"data: {msg}\n\n"
                parsed = json.loads(msg)
                if parsed.get("type") == "done":
                    break
            except asyncio.TimeoutError:
                yield ": keepalive\n\n"
                if state.get("done"):
                    break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Upload & Parse ────────────────────────────────────────────────────────────

@router.post("/upload")
async def upload_report(
    file: UploadFile = File(...),
    project_name: str = Form(DEFAULT_PROJECT_NAME),
):
    """Upload an Aalam HTML report, parse it, generate breakage_rerun.json for the target project."""
    project_name = _validate_project_name(project_name)
    paths = _project_paths(project_name)

    if not paths["root"].is_dir():
        raise HTTPException(400, f"Project folder '{project_name}' does not exist")

    if not file.filename.endswith((".html", ".htm")):
        raise HTTPException(400, "Only .html files are supported")

    # Save the uploaded file
    safe_name = re.sub(r'[^a-zA-Z0-9._\-]', '_', file.filename)
    upload_path = UPLOAD_DIR / f"breakage_{safe_name}"
    content = await file.read()
    upload_path.write_bytes(content)

    # Parse using breakage_analyzer
    from breakage_analyzer import parse_aalam_report, generate_manifest, extract_build_url

    try:
        failures = parse_aalam_report(str(upload_path))
    except Exception as e:
        raise HTTPException(500, f"Failed to parse report: {e}")

    if not failures:
        raise HTTPException(400, "No failures found in the uploaded report")

    # Extract Build Server URL from the report
    build_url = extract_build_url(str(upload_path))

    # Generate manifest into the target project folder
    manifest_path = generate_manifest(failures, str(paths["manifest"]), build_url=build_url)

    # Read back the manifest for response
    with open(manifest_path) as f:
        manifest = json.load(f)

    # Build summary
    by_owner = {}
    by_module = {}
    for t in manifest["tests"]:
        by_owner[t["owner"]] = by_owner.get(t["owner"], 0) + 1
        by_module[t["module"]] = by_module.get(t["module"], 0) + 1

    return {
        "success": True,
        "project_name": project_name,
        "total_failures": manifest["total_failures"],
        "manifest_path": str(manifest_path),
        "build_url": manifest.get("build_url", ""),
        "by_owner": by_owner,
        "by_module": by_module,
        "tests": manifest["tests"],
    }


# ── Run Analysis ──────────────────────────────────────────────────────────────

@router.get("/config")
async def get_config():
    """Return current machine config (drivers path, etc.) for UI defaults."""
    from config.project_config import DRIVERS_DIR as _drv
    return {"drivers_dir": _drv}


@router.post("/run")
async def start_analysis(
    retries: int = 3,
    project_name: str = Query(DEFAULT_PROJECT_NAME),
    drivers_path: str = Query(""),
):
    """Start rerunning breakage cases from the manifest. Returns run_id for SSE."""
    global _loop
    if _loop is None:
        _loop = asyncio.get_running_loop()

    project_name = _validate_project_name(project_name)
    paths = _project_paths(project_name)

    if not paths["manifest"].exists():
        raise HTTPException(400, f"No manifest found for project '{project_name}'. Upload a report first.")

    # Check if already running
    for rid, state in _analyses.items():
        if state["status"] == "running":
            raise HTTPException(409, f"Analysis already running (id: {rid}). Stop it first.")

    run_id = uuid.uuid4().hex[:12]
    _analyses[run_id] = {
        "status": "running",
        "logs": [],
        "queue": asyncio.Queue(),
        "stop_event": threading.Event(),
        "done": False,
        "retries": retries,
        "project_name": project_name,
        "drivers_path": drivers_path.strip() or None,
        "started_at": datetime.now().isoformat(),
    }

    t = threading.Thread(target=_execute_analysis, args=(run_id, retries, project_name), daemon=True)
    t.start()

    return {"run_id": run_id, "retries": retries, "project_name": project_name}


def _build_entity_import_map_for_project(project_name: str) -> dict:
    """Build ENTITY_IMPORT_MAP for a specific project (not the default one)."""
    modules_src = (
        WORKSPACE_DIR / project_name / "src"
        / "com" / "zoho" / "automater" / "selenium" / "modules"
    )
    if not modules_src.exists():
        return {}

    src_root = modules_src.parents[4]  # .../project/src
    _skip_suffixes = ("Locators", "Constants", "DataConstants", "AnnotationConstants",
                      "Fields", "Base", "Role", "APIUtil", "ActionsUtil", "ActionUtils")
    result = {}

    for java_file in modules_src.rglob("*.java"):
        simple = java_file.stem
        if simple.endswith(_skip_suffixes):
            continue
        fqcn = str(java_file.relative_to(src_root)).replace("/", ".").replace(".java", "")
        result[simple] = fqcn

    return result


def _execute_analysis(run_id: str, retries: int, project_name: str):
    """Background thread: rerun each failure N times, classify, push SSE updates."""
    from agents.runner_agent import RunnerAgent

    state = _analyses[run_id]
    stop_event = state["stop_event"]
    paths = _project_paths(project_name)

    try:
        with open(paths["manifest"]) as f:
            manifest = json.load(f)

        tests = manifest["tests"]
        total = len(tests)
        build_url = manifest.get("build_url", "") or None
        sdp_url = build_url if build_url else "http://localhost:8080"
        _log(run_id, f"Build URL: {sdp_url}")

        # Create runner and override paths for the target project
        runner = RunnerAgent(
            base_dir=str(WORKSPACE_DIR),
            deps_dir=str(DEPS_DIR),
            pre_compiled_bin_dir=str(paths["bin"]),
        )
        # Patch runner to point at the target project (not DEFAULT_PROJECT_NAME)
        runner.automater_root = paths["root"]
        runner.src_dir = paths["src"]
        runner.resources_dir = paths["resources"]
        runner._standalone_default = (
            paths["src"] / "com" / "zoho" / "automater" / "selenium"
            / "standalone" / "StandaloneDefault.java"
        )
        runner._main_class = (
            paths["src"] / "com" / "zoho" / "automater" / "selenium"
            / "standalone" / "AutomaterSeleniumMain.java"
        )
        runner._app_properties = paths["root"] / "product_package" / "conf" / "app.properties"

        # If a drivers_path was provided via the UI, override runner's browser paths
        ui_drivers_path = state.get("drivers_path")
        if ui_drivers_path:
            import agents.runner_agent as _ra_mod
            _ra_mod._DEFAULT_FIREFOX = os.path.join(ui_drivers_path, "firefox", "firefox")
            _ra_mod._DEFAULT_GECKODRIVER = os.path.join(ui_drivers_path, "geckodriver")
            _log(run_id, f"Drivers path override: {ui_drivers_path}")

        # Build entity import map for this project
        import agents.runner_agent as _ra_module
        original_map = _ra_module.ENTITY_IMPORT_MAP
        if project_name != DEFAULT_PROJECT_NAME:
            _log(run_id, f"Building entity map for project '{project_name}'...")
            _ra_module.ENTITY_IMPORT_MAP = _build_entity_import_map_for_project(project_name)
            _log(run_id, f"Discovered {len(_ra_module.ENTITY_IMPORT_MAP)} entity classes")

        _log(run_id, f"Starting breakage analysis: {total} tests × {retries} retries", "info")
        _log(run_id, f"Project: {project_name}")

        try:
            _run_analysis_loop(run_id, tests, total, retries, runner, stop_event, paths, sdp_url)
        finally:
            # Restore original entity map
            if project_name != DEFAULT_PROJECT_NAME:
                _ra_module.ENTITY_IMPORT_MAP = original_map

        # Final summary
        flaky_count = sum(1 for t in tests if t.get("ai_status") == "FLAKY")
        real_count = sum(1 for t in tests if t.get("ai_status") == "REAL_BREAKAGE")
        pending_count = sum(1 for t in tests if t.get("ai_status") == "PENDING")

        # Save final results
        summary = {
            "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "project_name": project_name,
            "total": len(tests),
            "flaky": flaky_count,
            "real_breakage": real_count,
            "pending": pending_count,
        }
        with open(paths["results"], "w") as fp:
            json.dump({"summary": summary, "tests": tests}, fp, indent=2)

        # Generate report
        try:
            from breakage_analyzer import generate_report as _gen_report, MANIFEST_PATH as _default_manifest
            # Temporarily override the module-level paths for report generation
            import breakage_analyzer as _ba_module
            _orig_manifest = _ba_module.MANIFEST_PATH
            _orig_results = _ba_module.RESULTS_PATH
            _orig_reports = _ba_module.AI_REPORTS_DIR
            _orig_reports_dir = _ba_module.REPORTS_DIR
            _ba_module.MANIFEST_PATH = str(paths["manifest"])
            _ba_module.RESULTS_PATH = str(paths["results"])
            _ba_module.AI_REPORTS_DIR = str(paths["ai_reports"])
            _ba_module.REPORTS_DIR = str(paths["reports"])
            try:
                report_path = _gen_report()
                _log(run_id, f"Report generated: {report_path}", "success")
            finally:
                _ba_module.MANIFEST_PATH = _orig_manifest
                _ba_module.RESULTS_PATH = _orig_results
                _ba_module.AI_REPORTS_DIR = _orig_reports
                _ba_module.REPORTS_DIR = _orig_reports_dir
        except Exception as e:
            _log(run_id, f"Report generation failed: {e}", "warn")

        _log(run_id, f"Analysis complete — Flaky: {flaky_count}, Real Breakage: {real_count}", "success")
        _push(run_id, "done", {
            "success": True,
            "project_name": project_name,
            "flaky": flaky_count,
            "real_breakage": real_count,
            "pending": pending_count,
            "total": len(tests),
        })

    except Exception as e:
        _log(run_id, f"Analysis failed: {e}", "error")
        _push(run_id, "done", {"success": False, "error": str(e)})

    state["status"] = "done"
    state["done"] = True


def _run_analysis_loop(run_id, tests, total, retries, runner, stop_event, paths, sdp_url):
    """Core rerun loop — extracted for clean try/finally in caller."""
    for i, test in enumerate(tests):
        if stop_event.is_set():
            _log(run_id, "Analysis stopped by user", "warn")
            break

        # Skip already-analyzed tests (for resume)
        if test.get("ai_status") not in ("PENDING", None):
            _push(run_id, "test_update", {
                "index": i, "total": total,
                "test": test,
                "phase": "skipped",
            })
            continue

        entity = test["entity_class"]
        method = test["method_name"]

        _log(run_id, f"[{i+1}/{total}] {entity}.{method} — {test['owner']}")
        _push(run_id, "test_update", {
            "index": i, "total": total,
            "test": test,
            "phase": "running",
        })

        run_results = []

        for attempt in range(retries):
            if stop_event.is_set():
                break

            _log(run_id, f"  Attempt {attempt+1}/{retries}...")

            start_time = time.time()
            try:
                result = runner.run_test(
                    entity_class=entity,
                    method_name=method,
                    url=sdp_url,
                    admin_mail_id=SDP_ADMIN_EMAIL,
                    email_id=SDP_EMAIL_ID,
                    portal_name=SDP_PORTAL,
                    skip_compile=True,
                    password=SDP_ADMIN_PASS,
                    skip_cleanup=False,
                    test_user_emails=SDP_TEST_USER_EMAILS,
                )
                duration = time.time() - start_time

                # Check ScenarioReport for reliable result
                report_result = _get_report_result(method, paths["reports"])
                if report_result:
                    passed = report_result == "PASS"
                else:
                    passed = result.success

                error = ""
                if not passed:
                    error = str(result.error)[:300] if result.error else ""
                    if result.stderr:
                        for line in result.stderr.splitlines():
                            if any(kw in line for kw in ["REASON:", "FAILURE:", "$$Failure"]):
                                error = line.strip()[:300]
                                break

            except Exception as e:
                duration = time.time() - start_time
                passed = False
                error = str(e)[:300]

            status = "PASS" if passed else "FAIL"
            run_results.append({
                "attempt": attempt + 1,
                "status": status,
                "duration": round(duration, 1),
                "error": error if not passed else "",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

            level = "success" if passed else "error"
            _log(run_id, f"  Attempt {attempt+1}: {status} ({duration:.0f}s)", level)

            if passed:
                for remaining in range(attempt + 2, retries + 1):
                    run_results.append({
                        "attempt": remaining,
                        "status": "SKIPPED",
                        "duration": 0,
                        "error": "Skipped — already passed once (flaky confirmed)",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
                break

        # Classify
        pass_count = sum(1 for r in run_results if r["status"] == "PASS")
        fail_count = sum(1 for r in run_results if r["status"] == "FAIL")

        if pass_count > 0:
            test["ai_status"] = "FLAKY"
            test["ai_verdict"] = "AI_ANALYSED: Zero Issues (Flaky)"
        else:
            test["ai_status"] = "REAL_BREAKAGE"
            test["ai_verdict"] = "AI_ANALYSED: Real Breakage — Needs Fix"

            # Root cause analysis for real breakages
            last_error = ""
            for r in reversed(run_results):
                if r.get("error"):
                    last_error = r["error"]
                    break
            try:
                diag = _diagnose_failure(
                    method_name=test["method_name"],
                    entity_class=test["entity_class"],
                    error_msg=last_error,
                    reports_dir=str(paths["reports"]),
                    src_dir=str(paths["src"]),
                    sdp_url=sdp_url,
                    admin_email=SDP_ADMIN_EMAIL,
                    admin_pass=SDP_ADMIN_PASS,
                    portal=SDP_PORTAL,
                    verify=False,
                )
                test["diagnosis"] = diag.to_dict()
                _log(run_id, f"  Root Cause: {diag.root_cause} ({diag.confidence}) — {diag.summary[:80]}")
            except Exception as diag_err:
                test["diagnosis"] = {"root_cause": "UNDETERMINED", "confidence": "LOW",
                                     "summary": f"Diagnosis failed: {diag_err}", "details": "", "evidence": []}

        test["ai_runs"] = run_results
        test["ai_pass_count"] = pass_count
        test["ai_fail_count"] = fail_count
        test["ai_total_runs"] = len([r for r in run_results if r["status"] != "SKIPPED"])

        verdict = "FLAKY" if test["ai_status"] == "FLAKY" else "REAL_BREAKAGE"
        _log(run_id, f"  Verdict: {verdict} ({pass_count}P/{fail_count}F)",
             "success" if verdict == "FLAKY" else "error")

        # Push live update for this test
        _push(run_id, "test_update", {
            "index": i, "total": total,
            "test": test,
            "phase": "done",
        })

        # Save progress to disk (resume-friendly, preserving top-level fields)
        with open(paths["manifest"]) as fp:
            saved = json.load(fp)
        saved["tests"] = tests
        saved["total_failures"] = total
        with open(paths["manifest"], "w") as fp:
            json.dump(saved, fp, indent=2)


def _get_report_result(method_name: str, reports_path: Path) -> Optional[str]:
    """Check the latest ScenarioReport.html for a test's PASS/FAIL."""
    reports_dir = str(reports_path)
    if not os.path.isdir(reports_dir):
        return None
    matching = sorted(
        [d for d in os.listdir(reports_dir) if d.startswith(f"LOCAL_{method_name}_")],
        reverse=True,
    )
    if not matching:
        return None
    html_path = os.path.join(reports_dir, matching[0], "ScenarioReport.html")
    if not os.path.isfile(html_path):
        return None
    with open(html_path, "r") as f:
        content = f.read()
    if 'data-result="FAIL"' in content or "$$Failure" in content:
        return "FAIL"
    if 'data-result="PASS"' in content:
        return "PASS"
    if "Additional Specific Info" in content and "successfully" in content.lower():
        return "PASS"
    return None


# ── SSE Stream ────────────────────────────────────────────────────────────────

@router.get("/stream/{run_id}")
async def stream_analysis(run_id: str):
    """SSE endpoint for streaming analysis progress."""
    state = _analyses.get(run_id)
    if not state:
        raise HTTPException(404, "Analysis run not found")

    async def event_generator():
        q = state["queue"]
        # Replay existing logs for late-joining clients
        for log_entry in list(state["logs"]):
            yield f"data: {log_entry}\n\n"

        while True:
            try:
                msg = await asyncio.wait_for(q.get(), timeout=2.0)
                yield f"data: {msg}\n\n"
                parsed = json.loads(msg)
                if parsed.get("type") == "done":
                    break
            except asyncio.TimeoutError:
                yield ": keepalive\n\n"
                if state.get("done"):
                    break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Stop Analysis ─────────────────────────────────────────────────────────────

@router.post("/stop/{run_id}")
async def stop_analysis(run_id: str):
    """Stop a running analysis."""
    state = _analyses.get(run_id)
    if not state:
        raise HTTPException(404, "Analysis run not found")
    if state["status"] != "running":
        return {"message": "Analysis is not running"}
    state["stop_event"].set()
    return {"message": "Stop signal sent"}


# ── Get Manifest ──────────────────────────────────────────────────────────────

@router.get("/manifest")
async def get_manifest(project_name: str = Query(DEFAULT_PROJECT_NAME)):
    """Return the current breakage_rerun.json for a project."""
    project_name = _validate_project_name(project_name)
    paths = _project_paths(project_name)
    if not paths["manifest"].exists():
        raise HTTPException(404, "No manifest found. Upload a report first.")
    with open(paths["manifest"]) as f:
        return json.load(f)


# ── Get Results ───────────────────────────────────────────────────────────────

@router.get("/results")
async def get_results(project_name: str = Query(DEFAULT_PROJECT_NAME)):
    """Return breakage_results.json for a project."""
    project_name = _validate_project_name(project_name)
    paths = _project_paths(project_name)
    if not paths["results"].exists():
        raise HTTPException(404, "No results found. Run analysis first.")
    with open(paths["results"]) as f:
        return json.load(f)


# ── Get Report ────────────────────────────────────────────────────────────────

@router.get("/report")
async def get_report(project_name: str = Query(DEFAULT_PROJECT_NAME)):
    """Return the latest AI analysis HTML report for a project."""
    project_name = _validate_project_name(project_name)
    paths = _project_paths(project_name)
    if not paths["ai_reports"].exists():
        raise HTTPException(404, "No reports found")
    reports = sorted(paths["ai_reports"].glob("AI_BREAKAGE_ANALYSIS_*.html"), reverse=True)
    if not reports:
        raise HTTPException(404, "No analysis reports found")
    return FileResponse(reports[0], media_type="text/html")
