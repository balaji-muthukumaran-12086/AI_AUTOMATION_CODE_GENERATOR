"""
project_config.py
-----------------
Central configuration for the AI Automation QA framework.

To switch the active test-case project folder, change PROJECT_NAME below.
All agents, runners, and indexers will automatically pick up the new value.
"""

# ── Project folder name ────────────────────────────────────────────────────
# This must match the folder name under ai-automation-qa/ that contains the
# cloned Hg branch you want to run tests against.
# Example values:
#   "SDPLIVE_LATEST_AUTOMATER_SELENIUM"
#   "SDPLIVE_UI_AUTOMATION_BRANCH"
#   "AALAM_FRAMEWORK_CHANGES"
#   "AutomaterSelenium"

PROJECT_NAME = "SDPLIVE_LATEST_AUTOMATER_SELENIUM"

# ── Mercurial integration (Phase 3) ───────────────────────────────────────
# Controls whether the HgAgent is allowed to create branches and push to the
# remote hg repository after test generation.
#
# Current status: DISABLED — pending management approval
#
# To enable after approval:
#   1. Set HG_AGENT_ENABLED = True
#   2. Optionally customise HG_BRANCH_PREFIX below
#   3. Restart the web server (if running)
#
# When False:
#   - hg_config is ignored; HgAgent is a no-op regardless of what callers pass
#   - The hg toggle in the Web UI is hidden
#   - The --hg CLI flag is silently ignored
HG_AGENT_ENABLED = False

# Branch prefix used when auto-generating branch names (only relevant when enabled)
HG_BRANCH_PREFIX = "feature/AI_GEN_"

# ── Derived paths (do not edit) ────────────────────────────────────────────
import os as _os

_BASE_DIR = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

PROJECT_ROOT    = _os.path.join(_BASE_DIR, PROJECT_NAME)
PROJECT_SRC     = _os.path.join(PROJECT_ROOT, "src")
PROJECT_BIN     = _os.path.join(PROJECT_ROOT, "bin")
PROJECT_RES     = _os.path.join(PROJECT_ROOT, "resources")
BASE_DIR        = _BASE_DIR
DEPS_DIR        = "/home/balaji-12086/Desktop/Workspace/Zide/dependencies17"

# ── SDP Test Application Credentials ────────────────────────────────────────
# Used by HealerAgent (Playwright) and RunnerAgent as fallbacks when no
# run_config is provided at runtime.
# Override any of these in .env — do NOT commit real passwords to source control.
SDP_URL         = _os.environ.get("SDP_URL",         "https://sdpodqa-auto1.csez.zohocorpin.com:9090/")
SDP_PORTAL      = _os.environ.get("SDP_PORTAL",      "portal1")
SDP_ADMIN_EMAIL = _os.environ.get("SDP_ADMIN_EMAIL", "jaya.kumar+org1admin1t0@zohotest.com")
SDP_ADMIN_PASS  = _os.environ.get("SDP_ADMIN_PASS",  "Admin@123")

# ── Phase 5 — Pipeline Monitoring ─────────────────────────────────────────
# Per-agent execution timeout in seconds. OrchestratorAgent (future) will kill
# a stuck agent after this many seconds and mark it TIMED_OUT.
AGENT_TIMEOUTS = {
    "planner":   120,
    "coverage":   60,
    "scout":     180,
    "coder":     300,
    "reviewer":   90,
    "output":     60,
    "runner":    600,
    "healer":    300,
}

# Ollama OOM recovery: retry up to OOM_RETRY_MAX times, waiting OOM_RETRY_WAIT_S seconds each.
OOM_RETRY_MAX      = 2
OOM_RETRY_WAIT_S   = 30

# How often (seconds) the server emits a heartbeat SSE event to keep connections alive.
MONITORING_HEARTBEAT_S = 10

# All past pipeline runs are persisted to this JSONL file (one JSON object per line).
# Loaded on server startup so run history survives restarts.
RUNS_LOG_PATH = _os.path.join(_BASE_DIR, "logs", "runs.jsonl")
