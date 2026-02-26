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

# ── Derived paths (do not edit) ────────────────────────────────────────────
import os as _os

_BASE_DIR = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

PROJECT_ROOT    = _os.path.join(_BASE_DIR, PROJECT_NAME)
PROJECT_SRC     = _os.path.join(PROJECT_ROOT, "src")
PROJECT_BIN     = _os.path.join(PROJECT_ROOT, "bin")
PROJECT_RES     = _os.path.join(PROJECT_ROOT, "resources")
BASE_DIR        = _BASE_DIR
DEPS_DIR        = "/home/balaji-12086/Desktop/Workspace/Zide/dependencies17"
