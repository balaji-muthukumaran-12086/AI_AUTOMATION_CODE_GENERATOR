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

# ── Browser Driver Paths ────────────────────────────────────────────────────
# Update these directly when deploying to a new machine.
# macOS example  : /Applications/Firefox.app/Contents/MacOS/firefox
# CI/Docker      : /usr/bin/firefox  |  /usr/bin/geckodriver
DRIVERS_DIR      = "/home/balaji-12086/Desktop/Workspace/Drivers"
FIREFOX_BINARY   = "/home/balaji-12086/Desktop/Workspace/Drivers/firefox/firefox"
GECKODRIVER_PATH = "/home/balaji-12086/Desktop/Workspace/Drivers/geckodriver"

# ── SDP Test Application Credentials ────────────────────────────────────────
# Single source of truth for server URL, portal, and credentials.
# Used by RunnerAgent (patches StandaloneDefault.java at runtime),
# HealerAgent (Playwright), and run_test.py (CLI runner).
SDP_URL         = "https://sdpod-am2.csez.zohocorpin.com:45532/"
SDP_PORTAL      = "change"
SDP_ADMIN_EMAIL = "REDACTED_EMAIL"
SDP_EMAIL_ID    = "REDACTED_EMAIL"
SDP_ADMIN_PASS  = "REDACTED_PASSWORD"

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

# ── Team Mode — Concurrent Pipeline Limits ──────────────────────────────────
# Max simultaneous pipeline runs allowed (prevents OOM when team is active).
# Queued runs wait until a slot opens. 2 is safe on 16 GB with Ollama loaded.
MAX_CONCURRENT_RUNS = 2

# ── Phase 8 — Parallel Execution & Learning ────────────────────────────────
# Number of tests to run in parallel.  Keep at 2 on a 16 GB machine with Ollama
# loaded (4.5 GB) — each JVM + Firefox takes ~1 GB.
PARALLEL_WORKERS = 2

# Path to the curated list of tests for the parallel learning runner.
TESTS_TO_RUN_PATH = _os.path.join(_BASE_DIR, "tests_to_run.json")

# How many recent learnings to inject into CoderAgent and ReviewerAgent prompts.
LEARNING_TOP_N = 10

# How many times the hands-free loop will re-run failing tests after healing.
LEARNING_RETRIES = 2

# All learnings extracted from batch runs are appended to this JSONL file.
LEARNINGS_LOG_PATH = _os.path.join(_BASE_DIR, "logs", "learnings.jsonl")

# ── Test execution timeout ─────────────────────────────────────────────────
# Maximum seconds to wait for a single Java test method to complete.
# Some scenarios (e.g. Workflow, large UDF) can take 20-30 minutes.
# Default: 1800 seconds (30 minutes) — safe upper bound for any scenario.
TEST_EXECUTION_TIMEOUT = 1800

# ── Headless browser mode ──────────────────────────────────────────────────
# When True, Firefox is launched without a visible window (no Xvfb needed).
# Useful for CI, Docker, and unattended runs on headless servers.
# Default: False (headed — shows browser window on the local desktop)
HEADLESS = False

# ── LLM Configuration ─────────────────────────────────────────────────────
# Provider: "ollama" | "openai" | "openrouter"
# Switch LLM_PROVIDER to change the active backend. All agents read from here.
LLM_PROVIDER        = "openrouter"

# OpenRouter
OPENROUTER_API_KEY  = "REDACTED_OPENROUTER_API_KEY"
OPENROUTER_MODEL    = "arcee-ai/trinity-large-preview:free"
OPENROUTER_MAX_TOKENS = 4000

# Ollama (local)
OLLAMA_MODEL        = "qwen2.5-coder:7b"
OLLAMA_BASE_URL     = "http://localhost:11434"

# OpenAI direct
OPENAI_MODEL        = "gpt-4o"
OPENAI_API_KEY      = ""   # set this if LLM_PROVIDER = "openai"
