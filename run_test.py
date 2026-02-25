"""
run_test.py
-----------
Quick CLI runner — executes a single AutomaterSelenium test case.

Usage:
    python run_test.py

Edit the RUN_CONFIG block below to change the target scenario.
"""

import sys
import os

# Make sure project root is on path
sys.path.insert(0, os.path.dirname(__file__))

from agents.runner_agent import RunnerAgent

# ── Configure here ────────────────────────────────────────────────────────

RUN_CONFIG = {
    "entity_class":  "Solution",
    "method_name":   "createUnapprovedSolutionWithCustomTopicRevDateExpDate",
    "url":           "https://sdpodqa-auto1.csez.zohocorpin.com:9090/",
    "admin_mail_id": "jaya.kumar+org1admin1t0@zohotest.com",
    "email_id":      "jaya.kumar+org1admin1t0@zohotest.com",
    "portal_name":   "portal1",
    "skip_compile":  True,   # set False to recompile first
}

DEPS_DIR            = "/home/balaji-12086/Desktop/Workspace/Zide/dependencies"
PRE_COMPILED_BIN    = "/home/balaji-12086/Desktop/Workspace/Zide/ai-automation-qa/AutomaterSelenium/bin"
BASE_DIR            = "/home/balaji-12086/Desktop/Workspace/Zide/ai-automation-qa"

# ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    runner = RunnerAgent(
        base_dir=BASE_DIR,
        deps_dir=DEPS_DIR,
        pre_compiled_bin_dir=PRE_COMPILED_BIN,
    )

    print(f"\n{'='*60}")
    print(f"  Running : {RUN_CONFIG['entity_class']}.{RUN_CONFIG['method_name']}")
    print(f"  URL     : {RUN_CONFIG['url']}")
    print(f"  Portal  : {RUN_CONFIG['portal_name']}")
    print(f"  Email   : {RUN_CONFIG['email_id']}")
    print(f"{'='*60}\n")

    result = runner.run_test(
        entity_class=RUN_CONFIG["entity_class"],
        method_name=RUN_CONFIG["method_name"],
        url=RUN_CONFIG["url"],
        admin_mail_id=RUN_CONFIG.get("admin_mail_id"),
        email_id=RUN_CONFIG.get("email_id"),
        portal_name=RUN_CONFIG.get("portal_name"),
        skip_compile=RUN_CONFIG.get("skip_compile", True),
    )

    print(f"\n{'='*60}")
    print(result.summary())
    print(f"{'='*60}\n")

    if result.stdout:
        print("── Full stdout (last 100 lines) ──────────────────────────")
        for line in result.stdout.splitlines()[-100:]:
            print(f"  {line}")

    if result.stderr:
        print("\n── Full stderr ───────────────────────────────────────────")
        for line in result.stderr.splitlines():
            print(f"  {line}")

    sys.exit(0 if result.success else 1)
