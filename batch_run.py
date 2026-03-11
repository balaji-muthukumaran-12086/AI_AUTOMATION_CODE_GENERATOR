"""
batch_run.py — Run all tests from tests_to_run.json sequentially.
Captures pass/fail results and writes a summary to batch_results.json.
"""
import json
import sys
import os
import re

sys.path.insert(0, os.path.dirname(__file__))

from config.project_config import (
    PROJECT_NAME, PROJECT_BIN, BASE_DIR, DEPS_DIR,
    SDP_URL, SDP_ADMIN_EMAIL, SDP_EMAIL_ID, SDP_PORTAL, SDP_ADMIN_PASS
)
from agents.runner_agent import RunnerAgent

def main():
    with open("tests_to_run.json") as f:
        data = json.load(f)

    tests = data.get("tests", [])
    print(f"\n{'='*60}")
    print(f"  Batch Run: {len(tests)} tests")
    print(f"  Project: {PROJECT_NAME}")
    print(f"  URL: {SDP_URL}")
    print(f"{'='*60}\n")

    runner = RunnerAgent(
        base_dir=BASE_DIR,
        deps_dir=DEPS_DIR,
        pre_compiled_bin_dir=PROJECT_BIN,
    )

    results = []
    for i, test in enumerate(tests, 1):
        entity_class = test["entity_class"]
        method_name = test["method_name"]
        test_id = test.get("_id", f"{entity_class}.{method_name}")

        print(f"\n[{i}/{len(tests)}] Running: {entity_class}.{method_name}")
        print("-" * 60)

        result = runner.run_test(
            entity_class=entity_class,
            method_name=method_name,
            url=SDP_URL,
            admin_mail_id=SDP_ADMIN_EMAIL,
            email_id=SDP_EMAIL_ID,
            portal_name=SDP_PORTAL,
            skip_compile=True,
            password=SDP_ADMIN_PASS,
            skip_cleanup=False,
        )

        status = "PASSED" if result.success else "FAILED"
        error_snippet = ""
        if not result.success:
            # Extract key error info
            combined = result.stdout + result.stderr
            for pattern in [r'(NoSuchElementException[^\n]*)', r'(NullPointerException[^\n]*)',
                            r'(TimeoutException[^\n]*)', r'(\$\$Failure[^\n]*)',
                            r'(AssertionException[^\n]*)', r'(WebDriverException[^\n]*)']:
                m = re.search(pattern, combined)
                if m:
                    error_snippet = m.group(1)[:200]
                    break
            if not error_snippet and result.error:
                error_snippet = result.error[:200]

        results.append({
            "index": i,
            "test_id": test_id,
            "entity_class": entity_class,
            "method_name": method_name,
            "status": status,
            "report_path": result.report_path or "",
            "error": error_snippet,
        })

        icon = "✅" if result.success else "❌"
        print(f"{icon} [{i}/{len(tests)}] {entity_class}.{method_name} → {status}")
        if error_snippet:
            print(f"   Error: {error_snippet}")

    # Write results
    with open("batch_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Summary
    passed = sum(1 for r in results if r["status"] == "PASSED")
    failed = sum(1 for r in results if r["status"] == "FAILED")

    print(f"\n{'='*60}")
    print(f"  BATCH COMPLETE: {passed} passed, {failed} failed out of {len(results)}")
    print(f"{'='*60}")

    if failed > 0:
        print(f"\n  Failed tests:")
        for r in results:
            if r["status"] == "FAILED":
                print(f"    ❌ {r['entity_class']}.{r['method_name']}")
                if r["error"]:
                    print(f"       {r['error']}")

    print(f"\n  Full results saved to: batch_results.json\n")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
