"""
project_config.py
-----------------
Central configuration for the AI Automation QA framework.

PROJECT_NAME is read from the .env file (set by @setup-project from the hg branch name).
All agents, runners, and indexers will automatically pick up the new value.
"""

import os as _os
from dotenv import load_dotenv as _load_dotenv

_BASE_DIR = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_load_dotenv(_os.path.join(_BASE_DIR, ".env"))

# ── Project folder name ────────────────────────────────────────────────────
# Read from .env PROJECT_NAME key, which is set by @setup-project to the
# hg branch name provided during setup.
# Fallback to "SDPLIVE_LATEST_AUTOMATER_SELENIUM" if not set.
PROJECT_NAME = _os.environ.get("PROJECT_NAME", "SDPLIVE_LATEST_AUTOMATER_SELENIUM")

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

# ── Mercurial Repository Configuration ──────────────────────────────────────
# Default remote hg repo URL for cloning test-case branches.
# Users supply branch name + credentials at setup time; the setup-project agent
# clones the branch into a subfolder matching PROJECT_NAME.
HG_REPO_URL = "https://zrepository.zohocorpcloud.in/zohocorp/Automater/AutomaterSelenium"

# ── Derived paths (do not edit) ────────────────────────────────────────────
PROJECT_ROOT    = _os.path.join(_BASE_DIR, PROJECT_NAME)
PROJECT_SRC     = _os.path.join(PROJECT_ROOT, "src")
PROJECT_BIN     = _os.path.join(PROJECT_ROOT, "bin")
PROJECT_RES     = _os.path.join(PROJECT_ROOT, "resources")
BASE_DIR        = _BASE_DIR
DEPS_DIR        = _os.environ.get("DEPS_DIR", "/home/balaji-12086/Desktop/Workspace/Zide/dependencies17")

# ── Browser Driver Paths ────────────────────────────────────────────────────
# Update these directly when deploying to a new machine.
# macOS example  : /Applications/Firefox.app/Contents/MacOS/firefox
# CI/Docker      : /usr/bin/firefox  |  /usr/bin/geckodriver
DRIVERS_DIR      = _os.environ.get("DRIVERS_DIR", "/home/balaji-12086/Desktop/Workspace/Drivers")
FIREFOX_BINARY   = _os.environ.get("FIREFOX_BINARY", _os.path.join(DRIVERS_DIR, "firefox", "firefox"))
GECKODRIVER_PATH = _os.environ.get("GECKODRIVER_PATH", _os.path.join(DRIVERS_DIR, "geckodriver"))

# ── SDP Test Application Credentials ────────────────────────────────────────
# Single source of truth for server URL, portal, and credentials.
# Used by RunnerAgent (patches StandaloneDefault.java at runtime),
# HealerAgent (Playwright), and run_test.py (CLI runner).
SDP_URL         = _os.environ.get("SDP_URL", "")
SDP_PORTAL      = _os.environ.get("SDP_PORTAL", "")
SDP_ADMIN_EMAIL = _os.environ.get("SDP_ADMIN_EMAIL", "")
SDP_EMAIL_ID    = _os.environ.get("SDP_EMAIL_ID", SDP_ADMIN_EMAIL)
SDP_ADMIN_PASS  = _os.environ.get("SDP_ADMIN_PASS", "")

# Comma-separated test user emails for ScenarioUsers.TEST_USER_1..4
# Used by RunnerAgent to patch AutomaterSeleniumMain.setupUsers() at runtime.
# Format: "user1@test.com,user2@test.com,user3@test.com,user4@test.com"
# If fewer than 4 are provided, remaining slots reuse the last email.
# If empty, the hardcoded defaults in AutomaterSeleniumMain.java are kept.
SDP_TEST_USER_EMAILS = _os.environ.get("SDP_TEST_USER_EMAILS", "")

# ── Mercurial user → OwnerConstants mapping ─────────────────────────────────
# The hg username provided during clone is matched (case-insensitive) against
# this table.  The resolved constant is stored in .env as OWNER_CONSTANT and
# used by CoderAgent / test-generator when emitting @AutomaterScenario.
HG_USERNAME     = _os.environ.get("HG_USERNAME", "")

# Map: lowercased hg username → OwnerConstants Java constant name
_OWNER_MAP = {
    "umesh-sudan":         "UMESH_SUDAN",
    "antonyrajan-d":       "ANTONYRAJAN_D",
    "rajeshwaran-a":       "RAJESHWARAN_A",
    "muthusivabalan-s":    "MUTHUSIVABALAN_S",
    "vinuthna-k":          "VINUTHNA_K",
    "nanthakumar-g":       "NANTHAKUMAR_G",
    "vignesh-e":           "VIGNESH_E",
    "rujendran":           "RUJENDRAN",
    "thilak-raj":          "THILAK_RAJ",
    "purva-rajesh":        "PURVA_RAJESH",
    "veeravel":            "VEERAVEL",
    "jaya-kumar":          "JAYA_KUMAR",
    "balaji-12086":        "BALAJI_M",
    "balaji-muthukumaran": "BALAJI_M",
    "subha":               "SUBHA",
    "binesh-nb":           "BINESH_N",
    "pavithra-r":          "PAVITHRA_R",
    "karuppasamy":         "KARUPPASAMY",
    "santhosh-bd":         "SANTHOSH_BD",
    "ompirakash-s":        "OMPIRAKASH",
    "abinaya-ak":          "ABINAYA_AK",
    "ranjith-n":           "RANJITH_N",
    "elango":              "ELANGO_S",
    "santhiya-pr":         "SANTHIYA_PR",
    "karthika-r":          "KARTHIKA_R",
    "surya-ramesh":        "SURYA",
    "vigneshraj-sk":       "VIGNESHRAJ",
    "tejaswini-g":         "TEJASWINI_G",
    "sivanesh-muthukumar": "SIVANESH_MUTHUKUMAR",
    "gurdeep-singh":       "GURDEEP_SINGH",
    "janaki-r":            "JANAKI_R",
    "hemapriya-s":         "HEMAPRIYA_S",
    "surendhar-gs":        "SURENDHAR_GS",
    "kasim-k":             "KASIM",
    "aishwarya-j":         "AISHWARYA_JAYASANKAR",
    "gowtham-a":           "GOWTHAM_A",
    "devirani-r":          "DEVIRANI_R",
    "balaji-mr":           "BALAJI_MR",
    "yuvan-r":             "YUVAN_R",
    "ugesh":               "UGESH",
    "kavin-kumar-r":       "KAVIN_KUMAR_R",
    "anitha-a":            "ANITHA_A",
    "nithin-k":            "NITHIN_K",
}


def resolve_owner_constant(hg_username: str | None = None) -> str | None:
    """Return the OwnerConstants.* Java constant for the given hg username.

    Falls back to OWNER_CONSTANT env var, then HG_USERNAME env var.
    Returns None if no match is found (caller should prompt the user).
    """
    username = (hg_username or _os.environ.get("OWNER_CONSTANT", "") or HG_USERNAME).strip()
    if not username:
        return None
    # Direct match (already a constant like BALAJI_M)
    if username.upper() in _OWNER_MAP.values():
        return username.upper()
    # Lookup by hg username
    return _OWNER_MAP.get(username.lower())


def fuzzy_match_owner(name: str) -> str | None:
    """Find the closest OwnerConstants match for a human name.

    Accepts inputs like 'Balaji M', 'balaji', 'Rajeshwaran', etc.
    Returns the best-matching constant or None if no reasonable match.
    """
    import difflib
    if not name or not name.strip():
        return None
    name_lower = name.strip().lower().replace(" ", "_").replace("-", "_")
    constants = list(_OWNER_MAP.values())
    # unique constants only
    unique = list(dict.fromkeys(constants))
    # Try exact substring match first
    for c in unique:
        if name_lower in c.lower() or c.lower() in name_lower:
            return c
    # Fuzzy match against constant names
    matches = difflib.get_close_matches(
        name_lower, [c.lower() for c in unique], n=1, cutoff=0.5
    )
    if matches:
        idx = [c.lower() for c in unique].index(matches[0])
        return unique[idx]
    return None


OWNER_CONSTANT = resolve_owner_constant()


def register_new_owner(hg_username: str, full_name: str, email: str) -> str:
    """Register a brand-new team member in OwnerConstants.java, _OWNER_MAP, and .env.

    Args:
        hg_username: The Mercurial username (e.g. 'priya-sharma').
        full_name:   Display name (e.g. 'Priya Sharma') — converted to PRIYA_SHARMA.
        email:       Zoho Corp email (e.g. 'priya.sharma@zohocorp.com').

    Returns:
        The new constant name (e.g. 'PRIYA_SHARMA').
    """
    import re

    # Derive constant name from full_name: "Priya Sharma" → "PRIYA_SHARMA"
    constant = re.sub(r'[^a-zA-Z0-9]+', '_', full_name.strip()).strip('_').upper()
    if not constant:
        raise ValueError(f"Cannot derive constant from name: {full_name!r}")

    # ── 1. Append to OwnerConstants.java ──────────────────────────────────
    owner_java = _os.path.join(
        PROJECT_SRC,
        "com", "zoho", "automater", "selenium", "modules", "OwnerConstants.java",
    )
    if not _os.path.isfile(owner_java):
        raise FileNotFoundError(f"OwnerConstants.java not found at {owner_java}")

    with open(owner_java, "r", encoding="utf-8") as f:
        content = f.read()

    # Check if constant already exists
    if re.search(rf'\b{re.escape(constant)}\b', content):
        print(f"OwnerConstants.{constant} already exists in Java file — skipping Java edit.")
    else:
        # Insert new constant before the closing brace
        new_line = f'\n\tpublic static final String {constant} = "{email}";\n'
        content = content.rstrip()
        if content.endswith("}"):
            content = content[:-1] + new_line + "\n}\n"
        with open(owner_java, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Added OwnerConstants.{constant} to {owner_java}")

    # ── 2. Append to _OWNER_MAP in this file ──────────────────────────────
    config_py = _os.path.join(_BASE_DIR, "config", "project_config.py")
    hg_key = hg_username.strip().lower()
    if hg_key not in _OWNER_MAP:
        _OWNER_MAP[hg_key] = constant
        # Also persist to the file so future runs pick it up
        with open(config_py, "r", encoding="utf-8") as f:
            py_content = f.read()
        # Find the closing brace of _OWNER_MAP dict — insert before it
        insert_marker = '\n}\n\n\ndef resolve_owner_constant'
        new_entry = f'    "{hg_key}":{" " * max(1, 19 - len(hg_key))}"{constant}",\n'
        py_content = py_content.replace(
            insert_marker,
            f'\n    {new_entry.strip()}\n}}\n\n\ndef resolve_owner_constant',
        )
        with open(config_py, "w", encoding="utf-8") as f:
            f.write(py_content)
        print(f"Added '{hg_key}' → '{constant}' to _OWNER_MAP in project_config.py")
    else:
        print(f"'{hg_key}' already in _OWNER_MAP — skipping.")

    # ── 3. Update .env ────────────────────────────────────────────────────
    env_path = _os.path.join(_BASE_DIR, ".env")
    if _os.path.isfile(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        patched = []
        found_owner = False
        for line in lines:
            if line.startswith("OWNER_CONSTANT="):
                patched.append(f"OWNER_CONSTANT={constant}\n")
                found_owner = True
            else:
                patched.append(line)
        if not found_owner:
            patched.append(f"OWNER_CONSTANT={constant}\n")
        with open(env_path, "w", encoding="utf-8") as f:
            f.writelines(patched)
        print(f"Set OWNER_CONSTANT={constant} in .env")

    return constant

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
# Project-level so each project has its own test manifest.
TESTS_TO_RUN_PATH = _os.path.join(PROJECT_ROOT, "tests_to_run.json")

# How many recent learnings to inject into CoderAgent and ReviewerAgent prompts.
LEARNING_TOP_N = 10

# How many times the hands-free loop will re-run failing tests after healing.
LEARNING_RETRIES = 2

# ── Coverage Agent — duplicate detection thresholds ────────────────────────
# These control how aggressively CoverageAgent filters planned scenarios before
# code generation.  Raising DUPLICATE_THRESHOLD makes fewer things "duplicate"
# (useful when KB has many near-miss descriptions); lowering it filters more.
# GAP_THRESHOLD: scenarios scoring below this are considered genuinely new.
COVERAGE_DUPLICATE_THRESHOLD = float(_os.environ.get("COVERAGE_DUPLICATE_THRESHOLD", "0.90"))
COVERAGE_GAP_THRESHOLD       = float(_os.environ.get("COVERAGE_GAP_THRESHOLD",       "0.70"))

# ── HealerAgent — self-healing loop depth cap ──────────────────────────────
# Maximum times HealerAgent may attempt to heal the same test in a single
# pipeline run.  Prevents infinite patch→fail→heal loops.
HEALER_MAX_DEPTH = int(_os.environ.get("HEALER_MAX_DEPTH", "2"))

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
OPENROUTER_API_KEY  = _os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL    = _os.environ.get("OPENROUTER_MODEL", "arcee-ai/trinity-large-preview:free")
OPENROUTER_MAX_TOKENS = int(_os.environ.get("OPENROUTER_MAX_TOKENS", "4000"))

# Ollama (local)
OLLAMA_MODEL        = "qwen2.5-coder:7b"
OLLAMA_BASE_URL     = "http://localhost:11434"

# OpenAI direct
OPENAI_MODEL        = _os.environ.get("OPENAI_MODEL", "gpt-4o")
OPENAI_API_KEY      = _os.environ.get("OPENAI_API_KEY", "")


# ── Configuration validation ────────────────────────────────────────────────

class ConfigError(RuntimeError):
    """Raised when a required configuration value is missing or invalid."""


def validate_config(strict: bool = False) -> list[str]:
    """
    Check that critical config values are set before starting the pipeline.

    Args:
        strict: If True, raise ConfigError on the first missing value.
                If False (default), return a list of warning strings so callers
                can decide whether to abort or just print warnings.

    Returns:
        List of human-readable warning strings (empty = all OK).

    Raises:
        ConfigError: If strict=True and any required value is missing.
    """
    warnings_out: list[str] = []

    def _warn(msg: str) -> None:
        if strict:
            raise ConfigError(msg)
        warnings_out.append(msg)

    # SDP connection (without a URL tests cannot run)
    if not SDP_URL:
        _warn("SDP_URL is not set — tests cannot run without a target SDP instance. "
              "Set SDP_URL in your .env file.")
    if not SDP_ADMIN_EMAIL:
        _warn("SDP_ADMIN_EMAIL is not set — no admin credentials for login/API calls.")
    if not SDP_ADMIN_PASS:
        _warn("SDP_ADMIN_PASS is not set — authentication will fail at runtime.")
    if not SDP_PORTAL:
        _warn("SDP_PORTAL is not set — portal name is required to build the SDP URL.")

    # LLM provider credentials
    if LLM_PROVIDER == "openai" and not OPENAI_API_KEY:
        _warn("LLM_PROVIDER='openai' but OPENAI_API_KEY is empty — LLM calls will fail. "
              "Set OPENAI_API_KEY in your .env file.")
    if LLM_PROVIDER == "openrouter" and not OPENROUTER_API_KEY:
        _warn("LLM_PROVIDER='openrouter' but OPENROUTER_API_KEY is empty — LLM calls will fail. "
              "Set OPENROUTER_API_KEY in your .env file.")

    # Browser driver paths
    if not _os.path.isfile(FIREFOX_BINARY):
        _warn(f"FIREFOX_BINARY not found at '{FIREFOX_BINARY}'. "
              "Set FIREFOX_BINARY or DRIVERS_DIR in your .env file.")
    if not _os.path.isfile(GECKODRIVER_PATH):
        _warn(f"GECKODRIVER_PATH not found at '{GECKODRIVER_PATH}'. "
              "Set GECKODRIVER_PATH or DRIVERS_DIR in your .env file.")

    # Java dependencies
    if not _os.path.isdir(DEPS_DIR):
        _warn(f"DEPS_DIR not found at '{DEPS_DIR}'. "
              "Set DEPS_DIR in your .env file to the directory containing your JAR files.")

    # Knowledge base
    chroma_dir = _os.path.join(BASE_DIR, "knowledge_base", "chroma_db")
    if not _os.path.isdir(chroma_dir):
        _warn("ChromaDB knowledge base not found. "
              "Run 'python -m ingestion.run_ingestion' to build it before using CoverageAgent.")

    return warnings_out
