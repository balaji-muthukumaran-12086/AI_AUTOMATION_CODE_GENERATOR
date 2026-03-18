"""
run_batch.py — Run all tests from a specific batch in tests_to_run.json
Usage: .venv/bin/python run_batch.py <batch_number>
"""
import sys
import os
import json
import time
import subprocess

sys.path.insert(0, os.path.dirname(__file__))
from config.project_config import (PROJECT_NAME, SDP_URL, SDP_ADMIN_EMAIL,
                                   SDP_EMAIL_ID, SDP_PORTAL, SDP_ADMIN_PASS)

def run_single_test(entity_class, method_name):
    """Run a single test and return (passed, duration_seconds, error_snippet)."""
    # Dynamically update run_test.py config
    run_config = {
        "entity_class": entity_class,
        "method_name": method_name,
        "url": SDP_URL,
        "admin_mail_id": SDP_ADMIN_EMAIL,
        "email_id": SDP_EMAIL_ID,
        "portal_name": SDP_PORTAL,
        "password": SDP_ADMIN_PASS,
        "skip_compile": True,
        "skip_cleanup": False,
    }

    # Write a temp runner script
    tmp_script = f"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from config.project_config import *
from agents.runner_agent import RunnerAgent
agent = RunnerAgent()
result = agent.run({{
    "entity_class": "{entity_class}",
    "method_name": "{method_name}",
    "url": "{SDP_URL}",
    "admin_mail_id": "{SDP_ADMIN_EMAIL}",
    "email_id": "{SDP_EMAIL_ID}",
    "portal_name": "{SDP_PORTAL}",
    "password": "{SDP_ADMIN_PASS}",
    "skip_compile": True,
    "skip_cleanup": False,
}})
success = result.get("success", False)
error = result.get("error", "")
print(f"BATCH_RESULT:{{success}}:{{error[:200]}}")
"""
    tmp_path = os.path.join(os.path.dirname(__file__), "_tmp_batch_run.py")
    with open(tmp_path, "w") as f:
        f.write(tmp_script)

    start = time.time()
    try:
        proc = subprocess.run(
            [".venv/bin/python", tmp_path],
            capture_output=True, text=True, timeout=300,
            cwd=os.path.dirname(__file__)
        )
        duration = time.time() - start
        output = proc.stdout + proc.stderr

        # Parse result
        for line in output.split("\n"):
            if line.startswith("BATCH_RESULT:"):
                parts = line.split(":", 2)
                passed = parts[1].strip() == "True"
                error = parts[2] if len(parts) > 2 else ""
                return passed, duration, error

        # Fallback parsing
        if "$$Failure" in output:
            return False, duration, "$$Failure found"
        if "PASSED" in output and "FAILED" not in output:
            return True, duration, ""
        if "FAILURE:" in output or "FAILED" in output:
            # Extract failure reason
            for line in output.split("\n"):
                if "REASON:" in line:
                    return False, duration, line.strip()
                if "FAILURE:" in line:
                    return False, duration, line.strip()
            return False, duration, "Test failed (no specific reason)"

        return False, duration, "No clear result signal"
    except subprocess.TimeoutExpired:
        return False, time.time() - start, "TIMEOUT (300s)"
    except Exception as e:
        return False, time.time() - start, str(e)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def main():
    if len(sys.argv) < 2:
        print("Usage: .venv/bin/python run_batch.py <batch_number>")
        sys.exit(1)

    batch_num = int(sys.argv[1])
    tests_file = os.path.join(os.path.dirname(__file__), PROJECT_NAME, "tests_to_run.json")

    with open(tests_file) as f:
        data = json.load(f)

    batch_tests = [t for t in data["tests"] if t.get("batch") == batch_num]
    if not batch_tests:
        print(f"No tests found for batch {batch_num}")
        sys.exit(1)

    print(f"\n{'='*60}")
    print(f"  BATCH {batch_num} — {len(batch_tests)} tests")
    print(f"{'='*60}\n")

    results = []
    for i, test in enumerate(batch_tests, 1):
        entity = test["entity_class"]
        method = test["method_name"]
        print(f"[{i}/{len(batch_tests)}] {entity}.{method} ...", end=" ", flush=True)

        passed, duration, error = run_single_test(entity, method)
        status = "PASS" if passed else "FAIL"
        print(f"{status} ({duration:.0f}s)")
        if not passed and error:
            print(f"         Error: {error[:120]}")

        results.append({
            "entity_class": entity,
            "method_name": method,
            "status": status,
            "duration": round(duration, 1),
            "error": error[:200] if error else ""
        })

    # Summary
    passed_count = sum(1 for r in results if r["status"] == "PASS")
    failed_count = sum(1 for r in results if r["status"] == "FAIL")
    total_time = sum(r["duration"] for r in results)

    print(f"\n{'='*60}")
    print(f"  BATCH {batch_num} SUMMARY")
    print(f"  Passed: {passed_count}/{len(results)}")
    print(f"  Failed: {failed_count}/{len(results)}")
    print(f"  Total time: {total_time:.0f}s")
    print(f"{'='*60}")

    if failed_count > 0:
        print(f"\n  FAILED TESTS:")
        for r in results:
            if r["status"] == "FAIL":
                print(f"    - {r['method_name']}: {r['error'][:100]}")

    # Save results
    results_file = os.path.join(os.path.dirname(__file__), PROJECT_NAME,
                                f"batch_{batch_num}_results.json")
    with open(results_file, "w") as f:
        json.dump({"batch": batch_num, "results": results,
                    "summary": {"passed": passed_count, "failed": failed_count,
                                "total": len(results), "total_time": round(total_time, 1)}},
                   f, indent=2)
    print(f"\n  Results saved to: {results_file}")


if __name__ == "__main__":
    main()
