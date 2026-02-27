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
