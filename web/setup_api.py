"""
web/setup_api.py
----------------
Backend for the project setup form. Handles:
  - /api/setup/projects   → list existing project folders
  - /api/setup/run        → start the setup process (clone, .env, compile)
  - /api/setup/stream/:id → SSE stream of setup progress
  - /api/setup/owner      → receive owner selection from the modal

No LLM involvement — pure shell commands + file writes.
"""

import asyncio
import json
import os
import re
import shutil
import subprocess
import threading
import uuid
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
WORKSPACE_DIR = BASE_DIR

# ── In-memory state ───────────────────────────────────────────────────────────
# setup_id → { status, logs: [], owner_needed: bool, owner_resolved: Event, owner_value: str, done: Event, result: {} }
_setups: dict[str, dict] = {}
_loop: Optional[asyncio.AbstractEventLoop] = None

router = APIRouter(prefix="/api/setup", tags=["setup"])


# ── Request Models ────────────────────────────────────────────────────────────

class SetupRequest(BaseModel):
    mode: str  # generate_only | generate_and_run | reconfigure
    hg_username: Optional[str] = None
    hg_password: Optional[str] = None  # transient — used only for clone, never saved
    branch: Optional[str] = None
    existing_project: Optional[str] = None
    deps_path: str
    sdp_url: Optional[str] = None
    portal: Optional[str] = None
    admin_email: Optional[str] = None
    tech_email: Optional[str] = None
    test_user_emails: Optional[str] = ""
    password: Optional[str] = None
    drivers_path: Optional[str] = None


class OwnerSelection(BaseModel):
    setup_id: str
    owner: str


# ── Helper: push log to SSE queue ────────────────────────────────────────────

def _push(setup_id: str, event_type: str, data, level: str = "info"):
    """Thread-safe push to the SSE queue."""
    state = _setups.get(setup_id)
    if not state or not _loop:
        return
    if event_type == "log":
        payload = json.dumps({"type": "log", "data": data, "level": level})
    else:
        payload = json.dumps({"type": event_type, "data": data})
    state["logs"].append(payload)
    q = state.get("queue")
    if q:
        asyncio.run_coroutine_threadsafe(q.put(payload), _loop)


def _log(setup_id: str, msg: str, level: str = "info"):
    _push(setup_id, "log", msg, level)


def _done(setup_id: str, success: bool, message: str):
    _push(setup_id, "done", {"success": success, "message": message})
    state = _setups.get(setup_id)
    if state:
        state["status"] = "done"
        state["result"] = {"success": success, "message": message}
        state["done_event"].set()


# ── Helper: run shell command with live logging ──────────────────────────────

def _run_cmd(setup_id: str, cmd: str, cwd: str = None, timeout: int = 300, mask: str = None) -> tuple[int, str]:
    """Run a shell command, stream output lines to the SSE log, return (exitcode, output).
    If mask is set, that string is replaced with ●●●● in all log output."""
    log_cmd = cmd.replace(mask, '●●●●') if mask else cmd
    _log(setup_id, f"$ {log_cmd}")
    try:
        proc = subprocess.Popen(
            cmd, shell=True, cwd=cwd,
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, bufsize=1,
        )
        output_lines = []
        for line in proc.stdout:
            line = line.rstrip('\n')
            output_lines.append(line)
            _log(setup_id, line.replace(mask, '●●●●') if mask else line)
        proc.wait(timeout=timeout)
        return proc.returncode, '\n'.join(output_lines)
    except subprocess.TimeoutExpired:
        proc.kill()
        _log(setup_id, "Command timed out", "error")
        return -1, "timeout"
    except Exception as e:
        _log(setup_id, f"Command failed: {e}", "error")
        return -1, str(e)


# ── Helper: derive PROJECT_NAME from branch ──────────────────────────────────

def _derive_project_name(branch: str) -> str:
    """Extract folder-safe name from branch: feature/SDPLIVE_FOO → SDPLIVE_FOO"""
    name = branch.rsplit("/", 1)[-1] if "/" in branch else branch
    name = re.sub(r'[^a-zA-Z0-9_\-]', '_', name)
    return name


# ── Helper: update .env ──────────────────────────────────────────────────────

def _update_env(setup_id: str, updates: dict[str, str]):
    """Patch .env file — update existing keys or append new ones."""
    env_path = WORKSPACE_DIR / ".env"

    if env_path.exists():
        lines = env_path.read_text(encoding="utf-8").splitlines(keepends=True)
    else:
        lines = []

    patched = []
    updated_keys = set()

    for line in lines:
        replaced = False
        for key, value in updates.items():
            if re.match(rf"^{re.escape(key)}\s*=", line):
                patched.append(f"{key}={value}\n")
                updated_keys.add(key)
                replaced = True
                break
        if not replaced:
            patched.append(line if line.endswith('\n') else line + '\n')

    for key, value in updates.items():
        if key not in updated_keys:
            patched.append(f"{key}={value}\n")

    env_path.write_text("".join(patched), encoding="utf-8")
    _log(setup_id, f"Updated .env: {', '.join(updates.keys())}", "success")


# ── Helper: read owner list from OwnerConstants.java ─────────────────────────

def _read_owners(project_name: str) -> list[str]:
    """Read owner constants from the cloned project's OwnerConstants.java."""
    owner_file = WORKSPACE_DIR / project_name / "src" / "com" / "zoho" / "automater" / "selenium" / "modules" / "OwnerConstants.java"
    if not owner_file.exists():
        return []
    owners = []
    for line in owner_file.read_text(encoding="utf-8").splitlines():
        m = re.search(r'public\s+static\s+final\s+String\s+([A-Z_]+)', line)
        if m:
            owners.append(m.group(1))
    return sorted(set(owners))


# ── Helper: auto-resolve owner from hg_username ─────────────────────────────

def _auto_resolve_owner(hg_username: str) -> Optional[str]:
    """Use project_config.py to resolve owner constant from hg username."""
    try:
        result = subprocess.run(
            [str(WORKSPACE_DIR / ".venv" / "bin" / "python"), "-c",
             f"from config.project_config import resolve_owner_constant; "
             f"r = resolve_owner_constant('{hg_username}'); "
             f"print(r if r else '')"],
            capture_output=True, text=True, cwd=str(WORKSPACE_DIR), timeout=10,
        )
        val = result.stdout.strip()
        return val if val else None
    except Exception:
        return None


# ── Main setup execution (runs in background thread) ─────────────────────────

def _execute_setup(setup_id: str, req: SetupRequest):
    """The main setup workflow — NO LLM, just shell commands and file writes."""
    try:
        mode = req.mode
        _log(setup_id, f"Setup mode: {mode}", "info")

        # ── Step 1: Derive project name ──────────────────────────────────
        if mode == "reconfigure":
            project_name = req.existing_project
            hg_branch = None
        else:
            hg_branch = req.branch
            project_name = _derive_project_name(hg_branch)

        _log(setup_id, f"Project name: {project_name}", "info")
        project_dir = WORKSPACE_DIR / project_name

        # ── Step 2: Clone or detect project ──────────────────────────────
        if mode != "reconfigure":
            if project_dir.exists():
                _log(setup_id, f"Folder {project_name}/ already exists — using as-is", "info")
                # Pull latest
                rc, _ = _run_cmd(setup_id, f'hg pull 2>&1 || true', cwd=str(project_dir))
                _run_cmd(setup_id, f'hg update "{hg_branch}" 2>&1 || true', cwd=str(project_dir))
            else:
                _log(setup_id, f"Cloning branch '{hg_branch}' into {project_name}/...", "info")

                # Ask for hg password via the browser UI (SSE prompt → wait for API response)
                state = _setups[setup_id]
                state["hg_password_resolved"] = threading.Event()
                state["hg_password_value"] = None

                _push(setup_id, "hg_password_prompt", {
                    "username": req.hg_username,
                    "branch": hg_branch,
                })

                _log(setup_id, "Waiting for Hg password...", "info")
                resolved = state["hg_password_resolved"].wait(timeout=300)
                if not resolved or not state["hg_password_value"]:
                    _done(setup_id, False, "Hg password not provided (timed out after 5 min)")
                    return

                hg_pass = state["hg_password_value"]
                # Clear from memory after use
                state["hg_password_value"] = None
                _log(setup_id, "Password received — starting clone...", "success")

                hg_user = req.hg_username or ""
                from urllib.parse import quote as _url_quote
                auth_url = f"https://{_url_quote(hg_user, safe='')}:{_url_quote(hg_pass, safe='')}@zrepository.zohocorpcloud.in/zohocorp/Automater/AutomaterSelenium"
                repo_url = "https://zrepository.zohocorpcloud.in/zohocorp/Automater/AutomaterSelenium"
                rc, output = _run_cmd(
                    setup_id,
                    f'hg clone --branch "{hg_branch}" "{auth_url}" "{project_name}" 2>&1',
                    cwd=str(WORKSPACE_DIR),
                    timeout=600,
                    mask=hg_pass,
                )

                if rc != 0:
                    if "unknown branch" in output.lower() or "unknown revision" in output.lower():
                        _log(setup_id, f"Branch '{hg_branch}' not found — creating from SDPLIVE_UI_AUTOMATION_BRANCH", "info")
                        # Clean up failed clone
                        if project_dir.exists():
                            shutil.rmtree(str(project_dir), ignore_errors=True)

                        rc2, _ = _run_cmd(
                            setup_id,
                            f'hg clone --branch "SDPLIVE_UI_AUTOMATION_BRANCH" "{auth_url}" "{project_name}" 2>&1',
                            cwd=str(WORKSPACE_DIR),
                            timeout=600,
                            mask=hg_pass,
                        )
                        if rc2 != 0:
                            _done(setup_id, False, "Failed to clone base branch. Check credentials and VPN.")
                            return

                        _run_cmd(setup_id, f'hg branch "{hg_branch}"', cwd=str(project_dir))
                        _run_cmd(
                            setup_id,
                            f'hg commit -m "Created branch {hg_branch} from SDPLIVE_UI_AUTOMATION_BRANCH" 2>&1',
                            cwd=str(project_dir),
                        )
                        _log(setup_id, f"Created new branch '{hg_branch}'", "success")
                    elif "authorization" in output.lower() or "401" in output:
                        _done(setup_id, False, "Authentication failed — check hg username/password")
                        return
                    else:
                        _done(setup_id, False, f"Clone failed: {output[-200:]}")
                        return
                else:
                    _log(setup_id, "Clone successful", "success")

        # Verify project dir exists
        if not project_dir.exists():
            _done(setup_id, False, f"Project folder {project_name}/ not found")
            return

        # ── Step 3: Create Testcase/ folder ──────────────────────────────
        testcase_dir = project_dir / "Testcase"
        testcase_dir.mkdir(parents=True, exist_ok=True)
        _log(setup_id, f"Created {project_name}/Testcase/", "success")

        # Convert .xlsx/.xls to .csv
        xlsx_files = list(testcase_dir.glob("*.xlsx")) + list(testcase_dir.glob("*.xls"))
        if xlsx_files:
            _log(setup_id, f"Found {len(xlsx_files)} spreadsheet(s) — converting to CSV...", "info")
            for xlf in xlsx_files:
                _run_cmd(
                    setup_id,
                    f'.venv/bin/python -c "'
                    f'import sys, csv, os; '
                    f'import openpyxl; '
                    f'wb = openpyxl.load_workbook(sys.argv[1], data_only=True); '
                    f'base = os.path.splitext(sys.argv[1])[0]; '
                    f'[csv.writer(open(base + chr(95) + s.replace(chr(32), chr(95)) + chr(46) + chr(99) + chr(115) + chr(118), chr(119), newline=chr(0)), encoding=chr(117)+chr(116)+chr(102)+chr(45)+chr(56)).writerows(wb[s].values) for s in wb.sheetnames]; '
                    f'print(len(wb.sheetnames), chr(115)+chr(104)+chr(101)+chr(101)+chr(116)+chr(115))'
                    f'" "{xlf}" 2>&1 || true',
                    cwd=str(WORKSPACE_DIR),
                )

        # Count use-case docs
        doc_count = len(list(testcase_dir.glob("*.csv"))) + len(list(testcase_dir.glob("*.md"))) + len(list(testcase_dir.glob("*.txt"))) + len(xlsx_files)
        if doc_count > 0:
            _log(setup_id, f"Found {doc_count} use-case document(s) in Testcase/", "success")
        else:
            _log(setup_id, "No use-case documents in Testcase/ — prompting for upload...", "info")

        # ── Step 3b: Use-case document gate ──────────────────────────
        # Prompt user to upload use-case docs if Testcase/ is empty
        if doc_count == 0 and mode != "reconfigure":
            state = _setups[setup_id]
            state["usecase_upload_resolved"] = threading.Event()
            state["usecase_files"] = []

            _push(setup_id, "usecase_upload_prompt", {
                "project_name": project_name,
            })

            _log(setup_id, "Waiting for use-case document upload...", "info")
            resolved = state["usecase_upload_resolved"].wait(timeout=600)
            if resolved and state.get("usecase_files"):
                uploaded = state["usecase_files"]
                _log(setup_id, f"Uploaded {len(uploaded)} file(s): {', '.join(uploaded)}", "success")

                # Re-count docs after upload
                doc_count = len(list(testcase_dir.glob("*.csv"))) + len(list(testcase_dir.glob("*.md"))) + len(list(testcase_dir.glob("*.txt")))
            elif resolved and state.get("usecase_skipped"):
                _log(setup_id, "Use-case upload skipped — you can upload later via @test-generator", "info")
            else:
                _log(setup_id, "Upload timed out — continuing without use-case docs", "info")

        # ── Step 3c: Run use-case analysis report ────────────────────
        csv_count = len(list(testcase_dir.glob("*.csv")))
        if csv_count > 0 and mode != "reconfigure":
            _log(setup_id, "Running use-case analysis...", "info")
            rc, output = _run_cmd(
                setup_id,
                f'"{WORKSPACE_DIR / ".venv" / "bin" / "python"}" generate_batch_summary.py --mode usecase-analysis 2>&1',
                cwd=str(WORKSPACE_DIR),
                timeout=120,
            )
            # Find the generated analysis report
            ai_reports_dir = project_dir / "ai_reports"
            if ai_reports_dir.exists():
                reports = sorted(ai_reports_dir.glob("USECASE_ANALYSIS_*.md"), reverse=True)
                if reports:
                    _log(setup_id, f"Analysis report: {reports[0].name}", "success")
                    # Send report content to the UI
                    try:
                        report_content = reports[0].read_text(encoding="utf-8")
                        _push(setup_id, "usecase_analysis_report", {
                            "filename": reports[0].name,
                            "content": report_content,
                        })
                    except Exception:
                        pass
            if rc != 0:
                _log(setup_id, "Analysis completed with warnings — check report", "info")
            else:
                _log(setup_id, "Use-case analysis complete", "success")

        # ── Step 4: Owner selection ──────────────────────────────────────
        hg_username = req.hg_username or ""
        auto_owner = _auto_resolve_owner(hg_username) if hg_username else None
        owners = _read_owners(project_name)

        # Fall back to _OWNER_MAP constants if OwnerConstants.java is missing in project
        if not owners:
            try:
                from config.project_config import _OWNER_MAP
                owners = sorted(set(_OWNER_MAP.values()))
            except Exception:
                owners = []

        if owners:
            state = _setups[setup_id]
            state["owner_needed"] = True
            state["owner_resolved"] = threading.Event()
            state["owner_value"] = auto_owner

            _push(setup_id, "owner_selection", {
                "owners": owners,
                "auto_detected": auto_owner,
            })

            # Wait for the user to pick an owner (up to 5 minutes)
            _log(setup_id, "Waiting for owner selection...", "info")
            resolved = state["owner_resolved"].wait(timeout=300)
            if resolved:
                selected_owner = state["owner_value"]
                _log(setup_id, f"Owner: {selected_owner}", "success")
            else:
                selected_owner = auto_owner or "BALAJI_M"
                _log(setup_id, f"Owner selection timed out — using: {selected_owner}", "info")
        else:
            selected_owner = auto_owner or "BALAJI_M"
            _log(setup_id, f"Owner: {selected_owner}", "success")

        # ── Step 5: Update .env ──────────────────────────────────────────
        _log(setup_id, "Updating .env...", "info")
        env_updates = {
            "PROJECT_NAME": project_name,
            "OWNER_CONSTANT": selected_owner,
            "DEPS_DIR": req.deps_path,
            "SETUP_MODE": mode,
        }

        if mode != "reconfigure" and hg_username:
            env_updates["HG_USERNAME"] = hg_username
        if hg_branch:
            env_updates["HG_BRANCH"] = hg_branch

        if mode in ("generate_and_run", "reconfigure"):
            env_updates.update({
                "SDP_URL": req.sdp_url or "",
                "SDP_PORTAL": req.portal or "",
                "SDP_ADMIN_EMAIL": req.admin_email or "",
                "SDP_EMAIL_ID": req.tech_email or "",
                "SDP_TEST_USER_EMAILS": req.test_user_emails or "",
                "SDP_ADMIN_PASS": req.password or "",
                "DRIVERS_DIR": req.drivers_path or "",
                "FIREFOX_BINARY": f"{req.drivers_path}/firefox/firefox" if req.drivers_path else "",
                "GECKODRIVER_PATH": f"{req.drivers_path}/geckodriver" if req.drivers_path else "",
            })

        _update_env(setup_id, env_updates)

        # ── Step 6: Add to .gitignore ────────────────────────────────────
        gitignore_path = WORKSPACE_DIR / ".gitignore"
        entry = f"{project_name}/"
        if gitignore_path.exists():
            content = gitignore_path.read_text(encoding="utf-8")
            if entry not in content:
                with open(gitignore_path, "a", encoding="utf-8") as f:
                    f.write(f"\n{entry}\n")
                _log(setup_id, f"Added {entry} to .gitignore", "success")
        else:
            _log(setup_id, ".gitignore not found — skipping", "info")

        # ── Step 7: Compile framework ────────────────────────────────────
        _log(setup_id, "Compiling framework classes...", "info")
        rc, output = _run_cmd(
            setup_id,
            "./setup_framework_bin.sh 2>&1",
            cwd=str(WORKSPACE_DIR),
            timeout=120,
        )

        if rc != 0:
            _log(setup_id, "Framework compilation had issues — check output above", "error")
            _log(setup_id, "Setup completed with warnings — framework may need manual fix", "info")
        else:
            _log(setup_id, "Framework compiled successfully", "success")

        # ── Step 8: VS Code settings ─────────────────────────────────────
        _log(setup_id, "Configuring VS Code Java classpath...", "info")
        vscode_dir = WORKSPACE_DIR / ".vscode"
        vscode_dir.mkdir(parents=True, exist_ok=True)
        settings_path = vscode_dir / "settings.json"

        settings = {}
        if settings_path.exists():
            try:
                raw = settings_path.read_text(encoding="utf-8")
                # Strip comments for parsing
                stripped = re.sub(r'//.*?$', '', raw, flags=re.MULTILINE)
                stripped = re.sub(r',\s*([}\]])', r'\1', stripped)
                settings = json.loads(stripped)
            except (json.JSONDecodeError, Exception):
                settings = {}

        settings["java.project.sourcePaths"] = [f"{project_name}/src"]
        settings["java.project.outputPath"] = f"{project_name}/bin"
        settings["java.project.referencedLibraries"] = [f"{req.deps_path}/**/*.jar"]
        settings["java.errors.incompleteClasspath.severity"] = "ignore"

        settings_path.write_text(json.dumps(settings, indent=2) + "\n", encoding="utf-8")
        _log(setup_id, "VS Code Java settings configured", "success")

        # ── Done ─────────────────────────────────────────────────────────
        summary = (
            f"Setup complete! Project: {project_name}, "
            f"Owner: {selected_owner}, Mode: {mode}"
        )
        _done(setup_id, True, summary)

    except Exception as e:
        _log(setup_id, f"Unexpected error: {e}", "error")
        _done(setup_id, False, f"Setup failed: {e}")


# ── Routes ────────────────────────────────────────────────────────────────────

@router.get("/projects")
async def list_projects():
    """List existing project folders in the workspace (any folder with src/ or bin/ inside)."""
    projects = []
    # Known prefixes for project folders
    known_prefixes = ("SDPLIVE_", "AALAM_", "MSP_", "SDP_")
    for d in WORKSPACE_DIR.iterdir():
        if not d.is_dir():
            continue
        # Match known prefixes OR folders that contain src/ (strong indicator of a project)
        if d.name.startswith(known_prefixes) or (d / "src").is_dir():
            # Exclude framework/config/infrastructure dirs
            if d.name in ("AutomaterSeleniumFramework", "AutomaterSelenium", ".venv", "node_modules",
                          "agents", "config", "docs", "web", "templates", "knowledge_base",
                          "evaluation", "ingestion", "orchestrator", "dependencies"):
                continue
            projects.append(d.name)
    return {"projects": sorted(projects)}


@router.post("/run")
async def start_setup(req: SetupRequest):
    """Start the setup process in a background thread. Returns a setup_id for SSE streaming."""
    global _loop
    if _loop is None:
        _loop = asyncio.get_running_loop()

    # Validate
    if req.mode not in ("generate_only", "generate_and_run", "reconfigure"):
        raise HTTPException(400, "Invalid mode")

    if req.mode != "reconfigure":
        if not req.hg_username:
            raise HTTPException(400, "hg_username is required")
        if not req.branch:
            raise HTTPException(400, "branch is required")
    else:
        if not req.existing_project:
            raise HTTPException(400, "existing_project is required for reconfigure mode")
        # Validate existing_project is a real directory name (prevent path traversal)
        safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '', req.existing_project)
        if safe_name != req.existing_project or not (WORKSPACE_DIR / req.existing_project).is_dir():
            raise HTTPException(400, "Invalid project folder")

    if not req.deps_path or not req.deps_path.startswith("/"):
        raise HTTPException(400, "deps_path must be an absolute path")

    if req.mode in ("generate_and_run", "reconfigure"):
        if not req.sdp_url or not re.match(r'^https?://', req.sdp_url):
            raise HTTPException(400, "sdp_url must start with http:// or https://")
        if not req.portal:
            raise HTTPException(400, "portal is required")
        if not req.admin_email or "@" not in req.admin_email:
            raise HTTPException(400, "admin_email must be a valid email")
        if not req.tech_email or "@" not in req.tech_email:
            raise HTTPException(400, "tech_email must be a valid email")
        if not req.password:
            raise HTTPException(400, "password is required")
        if not req.drivers_path or not req.drivers_path.startswith("/"):
            raise HTTPException(400, "drivers_path must be an absolute path")

    setup_id = uuid.uuid4().hex[:12]
    _setups[setup_id] = {
        "status": "running",
        "logs": [],
        "queue": asyncio.Queue(),
        "done_event": threading.Event(),
        "owner_needed": False,
        "owner_resolved": threading.Event(),
        "owner_value": None,
        "result": None,
    }

    t = threading.Thread(target=_execute_setup, args=(setup_id, req), daemon=True)
    t.start()

    return {"setup_id": setup_id}


@router.get("/stream/{setup_id}")
async def stream_setup(setup_id: str):
    """SSE endpoint for streaming setup progress."""
    state = _setups.get(setup_id)
    if not state:
        raise HTTPException(404, "Setup not found")

    async def event_generator():
        q = state["queue"]
        # Replay any logs that were pushed before client connected
        for log_entry in list(state["logs"]):
            yield f"data: {log_entry}\n\n"

        while True:
            try:
                msg = await asyncio.wait_for(q.get(), timeout=1.0)
                yield f"data: {msg}\n\n"
                # Check if done
                parsed = json.loads(msg)
                if parsed.get("type") == "done":
                    break
            except asyncio.TimeoutError:
                # Send keepalive
                yield ": keepalive\n\n"
                if state["status"] == "done":
                    break

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@router.post("/owner")
async def select_owner(selection: OwnerSelection):
    """Receive the user's owner selection from the modal."""
    state = _setups.get(selection.setup_id)
    if not state:
        raise HTTPException(404, "Setup not found")

    state["owner_value"] = selection.owner
    state["owner_resolved"].set()
    return {"ok": True, "owner": selection.owner}


class HgPasswordSubmission(BaseModel):
    setup_id: str
    password: str


@router.post("/hg-password")
async def submit_hg_password(req: HgPasswordSubmission):
    """Receive the hg password from the UI modal."""
    state = _setups.get(req.setup_id)
    if not state:
        raise HTTPException(404, "Setup not found")

    state["hg_password_value"] = req.password
    state["hg_password_resolved"].set()
    return {"ok": True}


# ── New member registration ───────────────────────────────────────────────────

class RegisterOwnerRequest(BaseModel):
    setup_id: str
    hg_username: str
    full_name: str
    email: str


@router.post("/register-owner")
async def register_owner(req: RegisterOwnerRequest):
    """Register a new team member: updates OwnerConstants.java, _OWNER_MAP, and .env."""
    if not req.hg_username or not req.full_name or not req.email:
        raise HTTPException(400, "hg_username, full_name, and email are all required")
    if "@" not in req.email:
        raise HTTPException(400, "email must be a valid email address")

    try:
        from config.project_config import register_new_owner
        constant = register_new_owner(req.hg_username.strip(), req.full_name.strip(), req.email.strip())
    except FileNotFoundError as e:
        raise HTTPException(400, str(e))
    except ValueError as e:
        raise HTTPException(400, str(e))

    # Update the in-flight setup state so the owner is selected automatically
    state = _setups.get(req.setup_id)
    if state:
        state["owner_value"] = constant
        state["owner_resolved"].set()

    return {"ok": True, "owner": constant}


@router.get("/owners")
async def list_owners():
    """Return the full owner constant list from _OWNER_MAP (no project clone required)."""
    from config.project_config import _OWNER_MAP
    return {"owners": sorted(set(_OWNER_MAP.values()))}


@router.post("/upload-usecase")
async def upload_usecase(
    setup_id: str = Form(...),
    project_name: str = Form(...),
    files: list[UploadFile] = File(...),
):
    """Receive use-case document uploads, save to Testcase/, convert spreadsheets to CSV."""
    # Validate project_name — prevent path traversal
    safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '', project_name)
    if safe_name != project_name:
        raise HTTPException(400, "Invalid project name")

    testcase_dir = WORKSPACE_DIR / project_name / "Testcase"
    testcase_dir.mkdir(parents=True, exist_ok=True)

    allowed_exts = {".csv", ".xlsx", ".xls", ".md", ".txt"}
    saved_files = []

    for f in files:
        ext = Path(f.filename).suffix.lower()
        if ext not in allowed_exts:
            continue
        # Sanitize filename — keep only safe chars
        safe_filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', f.filename)
        dest = testcase_dir / safe_filename
        content = await f.read()
        dest.write_bytes(content)
        saved_files.append(safe_filename)

    # Convert xlsx/xls to CSV
    xlsx_files = list(testcase_dir.glob("*.xlsx")) + list(testcase_dir.glob("*.xls"))
    for xlf in xlsx_files:
        try:
            subprocess.run(
                [str(WORKSPACE_DIR / ".venv" / "bin" / "python"), "-c",
                 "import sys, csv, os, openpyxl; "
                 "wb = openpyxl.load_workbook(sys.argv[1], data_only=True); "
                 "base = os.path.splitext(sys.argv[1])[0]; "
                 "[csv.writer(open(base + '_' + s.replace(' ', '_') + '.csv', 'w', newline='', encoding='utf-8')).writerows(wb[s].values) for s in wb.sheetnames]",
                 str(xlf)],
                capture_output=True, text=True, cwd=str(WORKSPACE_DIR), timeout=30,
            )
        except Exception:
            pass  # conversion failure is non-fatal

    # Signal the setup thread that files are uploaded
    state = _setups.get(setup_id)
    if state:
        state["usecase_files"] = saved_files
        evt = state.get("usecase_upload_resolved")
        if evt:
            evt.set()

    return {"ok": True, "files": saved_files}


@router.post("/skip-usecase-upload")
async def skip_usecase_upload(data: dict):
    """User chose to skip use-case upload — unblock the setup thread."""
    setup_id = data.get("setup_id", "")
    state = _setups.get(setup_id)
    if not state:
        raise HTTPException(404, "Setup not found")

    state["usecase_skipped"] = True
    evt = state.get("usecase_upload_resolved")
    if evt:
        evt.set()
    return {"ok": True}


@router.post("/upload-and-analyze")
async def upload_and_analyze(
    project_name: str = Form(...),
    files: list[UploadFile] = File(...),
):
    """Standalone: upload use-case docs to Testcase/ and run analysis. Works outside the setup flow."""
    # Validate project_name — prevent path traversal
    safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '', project_name)
    if safe_name != project_name:
        raise HTTPException(400, "Invalid project name")

    project_dir = WORKSPACE_DIR / project_name
    if not project_dir.is_dir():
        raise HTTPException(400, f"Project folder {project_name}/ not found")

    testcase_dir = project_dir / "Testcase"
    testcase_dir.mkdir(parents=True, exist_ok=True)

    allowed_exts = {".csv", ".xlsx", ".xls", ".md", ".txt"}
    saved_files = []

    for f in files:
        ext = Path(f.filename).suffix.lower()
        if ext not in allowed_exts:
            continue
        safe_filename = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', f.filename)
        dest = testcase_dir / safe_filename
        content = await f.read()
        dest.write_bytes(content)
        saved_files.append(safe_filename)

    # Convert xlsx/xls to CSV
    xlsx_files = list(testcase_dir.glob("*.xlsx")) + list(testcase_dir.glob("*.xls"))
    for xlf in xlsx_files:
        try:
            subprocess.run(
                [str(WORKSPACE_DIR / ".venv" / "bin" / "python"), "-c",
                 "import sys, csv, os, openpyxl; "
                 "wb = openpyxl.load_workbook(sys.argv[1], data_only=True); "
                 "base = os.path.splitext(sys.argv[1])[0]; "
                 "[csv.writer(open(base + '_' + s.replace(' ', '_') + '.csv', 'w', newline='', encoding='utf-8')).writerows(wb[s].values) for s in wb.sheetnames]",
                 str(xlf)],
                capture_output=True, text=True, cwd=str(WORKSPACE_DIR), timeout=30,
            )
        except Exception:
            pass

    # Run analysis — temporarily set PROJECT_NAME for the subprocess
    env = os.environ.copy()
    env["PROJECT_NAME"] = project_name
    try:
        result = subprocess.run(
            [str(WORKSPACE_DIR / ".venv" / "bin" / "python"),
             "generate_batch_summary.py", "--mode", "usecase-analysis"],
            capture_output=True, text=True, cwd=str(WORKSPACE_DIR), timeout=120, env=env,
        )
        analysis_output = result.stdout + result.stderr
    except Exception as e:
        analysis_output = f"Analysis error: {e}"

    # Find latest report
    ai_reports_dir = project_dir / "ai_reports"
    report_content = None
    report_filename = None
    if ai_reports_dir.exists():
        reports = sorted(ai_reports_dir.glob("USECASE_ANALYSIS_*.md"), reverse=True)
        if reports:
            report_filename = reports[0].name
            try:
                report_content = reports[0].read_text(encoding="utf-8")
            except Exception:
                pass

    return {
        "ok": True,
        "files": saved_files,
        "analysis_output": analysis_output,
        "report_filename": report_filename,
        "report_content": report_content,
    }


@router.post("/run-analysis")
async def run_analysis(data: dict):
    """Standalone: run use-case analysis on existing Testcase/ CSVs (no upload needed)."""
    project_name = data.get("project_name", "")
    safe_name = re.sub(r'[^a-zA-Z0-9_\-]', '', project_name)
    if safe_name != project_name or not (WORKSPACE_DIR / project_name).is_dir():
        raise HTTPException(400, "Invalid project name")

    testcase_dir = WORKSPACE_DIR / project_name / "Testcase"
    csv_count = len(list(testcase_dir.glob("*.csv"))) if testcase_dir.exists() else 0
    if csv_count == 0:
        raise HTTPException(400, "No CSV files found in Testcase/ — upload documents first")

    env = os.environ.copy()
    env["PROJECT_NAME"] = project_name
    try:
        result = subprocess.run(
            [str(WORKSPACE_DIR / ".venv" / "bin" / "python"),
             "generate_batch_summary.py", "--mode", "usecase-analysis"],
            capture_output=True, text=True, cwd=str(WORKSPACE_DIR), timeout=120, env=env,
        )
        analysis_output = result.stdout + result.stderr
    except Exception as e:
        raise HTTPException(500, f"Analysis failed: {e}")

    ai_reports_dir = WORKSPACE_DIR / project_name / "ai_reports"
    report_content = None
    report_filename = None
    if ai_reports_dir.exists():
        reports = sorted(ai_reports_dir.glob("USECASE_ANALYSIS_*.md"), reverse=True)
        if reports:
            report_filename = reports[0].name
            try:
                report_content = reports[0].read_text(encoding="utf-8")
            except Exception:
                pass

    return {
        "ok": True,
        "analysis_output": analysis_output,
        "report_filename": report_filename,
        "report_content": report_content,
    }
