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
# Override DEPS_DIR in .env to point to a different dependencies folder.
DEPS_DIR        = _os.environ.get("DEPS_DIR", "/home/balaji-12086/Desktop/Workspace/Zide/dependencies")

# ── Browser Driver Paths ────────────────────────────────────────────────────
# Set these in .env so the project runs identically on any machine.
# Linux default  : firefox binary under Drivers/firefox/firefox
# macOS example  : /Applications/Firefox.app/Contents/MacOS/firefox
# CI/Docker      : /usr/bin/firefox  |  /usr/bin/geckodriver
_DRIVERS_DIR_DEFAULT = _os.environ.get("DRIVERS_DIR", "/home/balaji-12086/Desktop/Workspace/Drivers")
DRIVERS_DIR      = _DRIVERS_DIR_DEFAULT
FIREFOX_BINARY   = _os.environ.get("FIREFOX_BINARY",    _os.path.join(_DRIVERS_DIR_DEFAULT, "firefox", "firefox"))
GECKODRIVER_PATH = _os.environ.get("GECKODRIVER_PATH",  _os.path.join(_DRIVERS_DIR_DEFAULT, "geckodriver"))

# ── SDP Test Application Credentials ────────────────────────────────────────
# Single source of truth for server URL, portal, and credentials.
# Used by RunnerAgent (patches StandaloneDefault.java at runtime),
# HealerAgent (Playwright), and run_test.py (CLI runner).
#
# Override any of these via environment variables or .env file.
# Do NOT commit real passwords to source control — use .env for local overrides.
SDP_URL         = _os.environ.get("SDP_URL",         "https://sdpodqa-auto2.csez.zohocorpin.com:12493/")
SDP_PORTAL      = _os.environ.get("SDP_PORTAL",      "revampis")
SDP_ADMIN_EMAIL = _os.environ.get("SDP_ADMIN_EMAIL", "automater-sdpcloudqa+rs2@zohotest.com")
SDP_EMAIL_ID    = _os.environ.get("SDP_EMAIL_ID",    "automater-sdpcloudqa+rs2sdp-sdguest@zohotest.com")
SDP_ADMIN_PASS  = _os.environ.get("SDP_ADMIN_PASS",  "Sdpg2@2025")

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

# ── Phase 8 — Parallel Execution & Learning ────────────────────────────────
# Number of tests to run in parallel.  Keep at 2 on a 16 GB machine with Ollama
# loaded (4.5 GB) — each JVM + Firefox takes ~1 GB.
PARALLEL_WORKERS = int(_os.environ.get("PARALLEL_WORKERS", "2"))

# Path to the curated list of tests for the parallel learning runner.
TESTS_TO_RUN_PATH = _os.path.join(_BASE_DIR, "tests_to_run.json")

# How many recent learnings to inject into CoderAgent and ReviewerAgent prompts.
LEARNING_TOP_N = int(_os.environ.get("LEARNING_TOP_N", "10"))

# How many times the hands-free loop will re-run failing tests after healing.
LEARNING_RETRIES = int(_os.environ.get("LEARNING_RETRIES", "2"))

# All learnings extracted from batch runs are appended to this JSONL file.
LEARNINGS_LOG_PATH = _os.path.join(_BASE_DIR, "logs", "learnings.jsonl")

# ── Test execution timeout ─────────────────────────────────────────────────
# Maximum seconds to wait for a single Java test method to complete.
# Some scenarios (e.g. Workflow, large UDF) can take 20-30 minutes.
# Override in .env:  TEST_EXECUTION_TIMEOUT=3600  (for very long suites)
# Default: 1800 seconds (30 minutes) — safe upper bound for any scenario.
TEST_EXECUTION_TIMEOUT = int(_os.environ.get("TEST_EXECUTION_TIMEOUT", "1800"))

# ── Headless browser mode ──────────────────────────────────────────────────
# When True, Firefox is launched without a visible window (no Xvfb needed).
# Useful for CI, Docker, and unattended runs on headless servers.
# Override in .env:  HEADLESS=true
# Default: false (headed — shows browser window on the local desktop)
HEADLESS = _os.environ.get("HEADLESS", "false").lower() in ("1", "true", "yes")
