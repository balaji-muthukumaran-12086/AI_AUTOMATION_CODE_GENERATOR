"""Quick batch runner — runs tests sequentially using RunnerAgent.run_test()."""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(__file__))

from config.project_config import (PROJECT_NAME, PROJECT_BIN, BASE_DIR, DEPS_DIR,
                                   SDP_URL, SDP_ADMIN_EMAIL, SDP_EMAIL_ID,
                                   SDP_PORTAL, SDP_ADMIN_PASS)
from agents.runner_agent import RunnerAgent

BATCH = int(sys.argv[1]) if len(sys.argv) > 1 else 1
START = int(sys.argv[2]) if len(sys.argv) > 2 else 0

with open(os.path.join(os.path.dirname(__file__), PROJECT_NAME, "tests_to_run.json")) as f:
    data = json.load(f)

tests = [t for t in data["tests"] if t.get("batch") == BATCH]
print(f"Batch {BATCH}: {len(tests)} tests (starting from index {START})")

runner = RunnerAgent(base_dir=BASE_DIR, deps_dir=DEPS_DIR, pre_compiled_bin_dir=PROJECT_BIN)
results = []

for i, t in enumerate(tests[START:], START):
    entity = t["entity_class"]
    method = t["method_name"]
    print(f"\n[{i+1}/{len(tests)}] {entity}.{method} ", end="", flush=True)

    start_time = time.time()
    try:
        result = runner.run_test(
            entity_class=entity, method_name=method, url=SDP_URL,
            admin_mail_id=SDP_ADMIN_EMAIL, email_id=SDP_EMAIL_ID,
            portal_name=SDP_PORTAL, skip_compile=True, password=SDP_ADMIN_PASS,
            skip_cleanup=False,
        )
        duration = time.time() - start_time
        status = "PASS" if result.success else "FAIL"
        error = str(result.error)[:200] if result.error else ""
        if not result.success and result.stderr:
            for line in result.stderr.splitlines():
                if "REASON:" in line or "FAILURE:" in line:
                    error = line.strip()[:200]
                    break
    except Exception as e:
        duration = time.time() - start_time
        status = "FAIL"
        error = str(e)[:200]

    print(f"→ {status} ({duration:.0f}s)" + (f" | {error[:80]}" if status == "FAIL" else ""))
    results.append({"method": method, "entity": entity, "status": status,
                     "duration": round(duration), "error": error if status == "FAIL" else ""})

# Summary
passed = sum(1 for r in results if r["status"] == "PASS")
print(f"\n{'='*60}")
print(f"  BATCH {BATCH} RESULTS: {passed}/{len(results)} PASSED")
print(f"{'='*60}")
for r in results:
    mark = "PASS" if r["status"] == "PASS" else "FAIL"
    print(f"  [{mark}] {r['method']} ({r['duration']}s)")
    if r["error"]:
        print(f"         {r['error'][:100]}")

outfile = os.path.join(os.path.dirname(__file__), PROJECT_NAME, f"batch_{BATCH}_results.json")
with open(outfile, "w") as f:
    json.dump({"batch": BATCH, "results": results,
               "passed": passed, "failed": len(results) - passed}, f, indent=2)
print(f"\nSaved: {outfile}")
