"""
run_test.py
-----------
Quick CLI runner — executes a single AutomaterSelenium test case.

Usage:
    python run_test.py

Edit the RUN_CONFIG block below to change the target scenario.

MODE:
    USE_PIPELINE = False  → RunnerAgent directly (fast, no code generation)
    USE_PIPELINE = True   → Full agents pipeline (Planner→Coverage→Coder→...→Runner)
                            Generates code from FEATURE_DESCRIPTION, then runs the
                            method in RUN_CONFIG to verify the live UI.
"""

import sys
import os

# Make sure project root is on path
sys.path.insert(0, os.path.dirname(__file__))

from config.project_config import (PROJECT_NAME, PROJECT_BIN, BASE_DIR as _BASE_DIR, DEPS_DIR as _DEPS_DIR,
                                   SDP_URL, SDP_ADMIN_EMAIL, SDP_PORTAL)

# ── Configure here ────────────────────────────────────────────────────────

# Set to True to go through the full agents pipeline (Planner→Coder→Runner)
# Set to False to invoke RunnerAgent directly (same as before)
USE_PIPELINE = False

# Feature description used by the pipeline to generate code (only when USE_PIPELINE=True)
FEATURE_DESCRIPTION = """
Copy an existing Problem record in ServiceDesk Plus and verify the copied problem
appears in the Problems listview.

Scenario: A technician navigates to the Problems module, searches for a specific
problem by title, clicks the row action gear icon, selects "Copy Problem", confirms
in the popup by clicking the submit button, and then verifies that the new copied
problem appears in the detail view with the expected title. The test also verifies
the copied problem is searchable in the Problems listview.
"""

RUN_CONFIG = {
    "entity_class":  "ChangeDetailsView",
    "method_name":   "verifyAttachParentChangePopup",
    "url":           SDP_URL,
    "admin_mail_id": SDP_ADMIN_EMAIL,
    "email_id":      SDP_ADMIN_EMAIL,
    "portal_name":   SDP_PORTAL,
    "skip_compile":  True,   # keep True — full compile is broken
}

DEPS_DIR            = _DEPS_DIR           # from config/project_config.py → dependencies17
PRE_COMPILED_BIN    = PROJECT_BIN          # from config/project_config.py → PROJECT_NAME/bin
BASE_DIR            = _BASE_DIR            # from config/project_config.py

# ─────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"  Mode    : {'AGENTS PIPELINE' if USE_PIPELINE else 'DIRECT RUNNER'}")
    print(f"  Running : {RUN_CONFIG['entity_class']}.{RUN_CONFIG['method_name']}")
    print(f"  URL     : {RUN_CONFIG['url']}")
    print(f"  Portal  : {RUN_CONFIG['portal_name']}")
    print(f"  Email   : {RUN_CONFIG['email_id']}")
    print(f"{'='*60}\n")

    if USE_PIPELINE:
        # ── Full agents pipeline: Planner → Coverage → Coder → Reviewer → Output → Runner ──
        from agents.pipeline import run_pipeline

        final_state = run_pipeline(
            feature_description=FEATURE_DESCRIPTION,
            target_modules=["solutions/solution"],
            generation_mode="new_feature",
            base_dir=BASE_DIR,
            run_config=RUN_CONFIG,
        )

        print(f"\n{'='*60}")
        print("  Pipeline Complete")
        print(f"{'='*60}")

        # Pipeline log
        for msg in final_state.get("messages", []):
            print(f"  {'✅' if '✅' in msg else '❌' if '❌' in msg.lower() else '  '} {msg}")

        # Run result
        run_result = final_state.get("run_result", {})
        if run_result:
            status = "✅ PASSED" if run_result.get("success") else "❌ FAILED"
            print(f"\n  Test Result : {status}")
            print(f"  Report      : {run_result.get('report_path', 'N/A')}")
            if run_result.get("error"):
                print(f"  Error       : {run_result['error']}")

        # Errors
        for err in final_state.get("errors", []):
            print(f"  ❌ {err}")

        # Generated files
        for p in final_state.get("final_output_paths", []):
            print(f"  📄 Generated: {p}")

        success = run_result.get("success", False) if run_result else False

    else:
        # ── Direct RunnerAgent (no code generation) ──────────────────────────
        from agents.runner_agent import RunnerAgent

        runner = RunnerAgent(
            base_dir=BASE_DIR,
            deps_dir=DEPS_DIR,
            pre_compiled_bin_dir=PRE_COMPILED_BIN,
        )

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

        success = result.success

    sys.exit(0 if success else 1)
