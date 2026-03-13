#!/usr/bin/env python3
"""
Batch test runner helper — runs tests individually or in batch from tests_to_run.json.

Usage:
  Single test:   python3 batch_run_helper.py <entity_class> <method_name>
  Batch run:     python3 batch_run_helper.py --batch [--json tests_to_run.json]
  Batch summary: python3 batch_run_helper.py --batch --summary-only
"""
import sys, os, re, subprocess, glob, json, time
from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from config.project_config import (PROJECT_NAME, PROJECT_BIN, BASE_DIR, DEPS_DIR,
                                   SDP_URL, SDP_ADMIN_EMAIL, SDP_EMAIL_ID, SDP_PORTAL, SDP_ADMIN_PASS)

# ── Result data class ──────────────────────────────────────────────────────

@dataclass
class TestResult:
    entity_class: str
    method_name: str
    scenario_id: str = ""
    status: str = "NOT_RUN"    # PASS | FAIL | ERROR | SKIPPED | NOT_RUN
    report_path: str = ""
    failure_info: str = ""
    attempt: int = 1
    duration_seconds: float = 0.0
    fix_applied: str = ""      # filled by self-heal phase

    @property
    def test_key(self) -> str:
        return f"{self.entity_class}.{self.method_name}"

    def to_dict(self):
        d = asdict(self)
        d["test_key"] = self.test_key
        return d


# ── Batch results container ────────────────────────────────────────────────

@dataclass
class BatchRunResults:
    phase: str = "dry_run"     # dry_run | validation_run
    started_at: str = ""
    finished_at: str = ""
    results: List[TestResult] = field(default_factory=list)

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.status == "PASS")

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.status in ("FAIL", "ERROR"))

    @property
    def skipped(self) -> int:
        return sum(1 for r in self.results if r.status == "SKIPPED")

    def failed_tests(self) -> List[TestResult]:
        return [r for r in self.results if r.status in ("FAIL", "ERROR")]

    def summary_line(self) -> str:
        return (f"[{self.phase}] Total: {self.total} | "
                f"PASS: {self.passed} | FAIL: {self.failed} | SKIP: {self.skipped}")

    def to_dict(self):
        return {
            "phase": self.phase,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "skipped": self.skipped,
            "results": [r.to_dict() for r in self.results],
        }

    def save_json(self, path: str):
        with open(path, "w") as f:
            json.dump(self.to_dict(), f, indent=2)
        print(f"[BatchRunner] Results saved to {path}")


# ── Single test execution ──────────────────────────────────────────────────

def run_single_test(entity_class, method_name):
    """Run a single test by patching run_test.py. Returns (passed, report_path, failure_info)."""
    run_test_path = os.path.join(os.path.dirname(__file__), 'run_test.py')
    with open(run_test_path, 'r') as f:
        content = f.read()

    content = re.sub(
        r'"entity_class":\s*"[^"]*"',
        f'"entity_class":  "{entity_class}"',
        content
    )
    content = re.sub(
        r'"method_name":\s*"[^"]*"',
        f'"method_name":   "{method_name}"',
        content
    )

    with open(run_test_path, 'w') as f:
        f.write(content)

    result = subprocess.run(
        [sys.executable, 'run_test.py'],
        capture_output=True, text=True, timeout=300,
        cwd=os.path.dirname(__file__)
    )

    report_pattern = os.path.join(
        os.path.dirname(__file__), PROJECT_NAME, 'reports',
        f'LOCAL_{method_name}_*', 'ScenarioReport.html'
    )
    reports = sorted(glob.glob(report_pattern))

    if reports:
        report_path = reports[-1]
        with open(report_path, 'r') as f:
            html = f.read()

        # ScenarioReport.html is the AUTHORITATIVE source of truth.
        # The HTML contains: <div class="scenario-result PASS|FAIL" ...>
        # Trust this over any stdout/stderr noise (cleanup logs, DELETE
        # messages, benign exceptions during post-process, etc.).
        passed = 'scenario-result PASS' in html and 'scenario-result FAIL' not in html

        failure_info = ""
        if not passed:
            highlights = re.findall(r'<span class="highlight">(.*?)</span>', html, re.DOTALL)
            failure_info = " | ".join([h.strip()[:100] for h in highlights[-5:]])

        return passed, report_path, failure_info
    else:
        combined = result.stdout + result.stderr
        if '$$Failure' in combined:
            return False, "", "$$Failure in output"
        if 'BUILD FAILED' in combined:
            return False, "", "BUILD FAILED"
        return False, "", "No report found"


# ── Batch execution ────────────────────────────────────────────────────────

def load_tests_to_run(json_path: str = None) -> list:
    """Load test entries from tests_to_run.json."""
    if json_path is None:
        json_path = os.path.join(os.path.dirname(__file__), "tests_to_run.json")

    with open(json_path, "r") as f:
        data = json.load(f)

    return data.get("tests", [])


def run_batch(json_path: str = None, only_methods: List[str] = None) -> BatchRunResults:
    """
    Run all tests from tests_to_run.json sequentially.

    Args:
        json_path: Path to tests_to_run.json (default: workspace root)
        only_methods: If provided, only run tests whose method_name is in this list
                      (used for validation re-runs of previously failed tests)

    Returns:
        BatchRunResults with status for every test
    """
    tests = load_tests_to_run(json_path)
    batch = BatchRunResults(
        phase="dry_run" if only_methods is None else "validation_run",
        started_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )

    total = len(tests)
    for idx, test_entry in enumerate(tests, 1):
        entity_class = test_entry.get("entity_class", "")
        method_name = test_entry.get("method_name", "")
        scenario_id = test_entry.get("_id", "")

        # Filter for validation re-runs
        if only_methods and method_name not in only_methods:
            continue

        print(f"\n{'='*60}")
        print(f"[BatchRunner] [{idx}/{total}] Running {entity_class}.{method_name}")
        print(f"{'='*60}")

        start_time = time.time()
        try:
            passed, report_path, failure_info = run_single_test(entity_class, method_name)
            duration = time.time() - start_time

            result = TestResult(
                entity_class=entity_class,
                method_name=method_name,
                scenario_id=scenario_id,
                status="PASS" if passed else "FAIL",
                report_path=report_path,
                failure_info=failure_info,
                duration_seconds=round(duration, 1),
            )
        except subprocess.TimeoutExpired:
            duration = time.time() - start_time
            result = TestResult(
                entity_class=entity_class,
                method_name=method_name,
                scenario_id=scenario_id,
                status="ERROR",
                failure_info="Test timed out (300s)",
                duration_seconds=round(duration, 1),
            )
        except Exception as e:
            duration = time.time() - start_time
            result = TestResult(
                entity_class=entity_class,
                method_name=method_name,
                scenario_id=scenario_id,
                status="ERROR",
                failure_info=str(e)[:200],
                duration_seconds=round(duration, 1),
            )

        batch.results.append(result)

        status_icon = "✅" if result.status == "PASS" else "❌"
        print(f"{status_icon} {result.test_key} → {result.status} ({result.duration_seconds}s)")
        if result.failure_info:
            print(f"   ⚠️  {result.failure_info[:150]}")

    batch.finished_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*60}")
    print(f"[BatchRunner] {batch.summary_line()}")
    print(f"{'='*60}")

    return batch


def generate_batch_summary_md(batch: BatchRunResults, output_path: str = None) -> str:
    """Generate a Markdown summary of the batch run results."""
    if output_path is None:
        output_path = os.path.join(os.path.dirname(__file__), "batch_run_results.md")

    lines = [
        f"# Batch Run Results — {batch.phase.replace('_', ' ').title()}",
        f"",
        f"**Started**: {batch.started_at}  ",
        f"**Finished**: {batch.finished_at}  ",
        f"**{batch.summary_line()}**",
        f"",
        f"---",
        f"",
        f"| # | Entity.Method | Status | Duration | Failure Info |",
        f"|---|--------------|--------|----------|--------------|",
    ]

    for i, r in enumerate(batch.results, 1):
        icon = "✅" if r.status == "PASS" else "❌" if r.status in ("FAIL", "ERROR") else "⏭️"
        info = r.failure_info[:80].replace("|", "\\|") if r.failure_info else "—"
        lines.append(
            f"| {i} | {r.test_key} | {icon} {r.status} | {r.duration_seconds}s | {info} |"
        )

    if batch.failed_tests():
        lines.extend([
            f"",
            f"## Failed Tests ({len(batch.failed_tests())})",
            f"",
        ])
        for r in batch.failed_tests():
            lines.extend([
                f"### {r.test_key}",
                f"- **Scenario ID**: {r.scenario_id}",
                f"- **Status**: {r.status}",
                f"- **Report**: `{r.report_path}`" if r.report_path else "- **Report**: (none)",
                f"- **Error**: {r.failure_info}" if r.failure_info else "",
                f"- **Fix Applied**: {r.fix_applied}" if r.fix_applied else "",
                f"",
            ])

    content = "\n".join(lines) + "\n"
    with open(output_path, "w") as f:
        f.write(content)
    print(f"[BatchRunner] Summary MD written to {output_path}")
    return output_path


# ── CLI ────────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    if len(sys.argv) >= 2 and sys.argv[1] == "--batch":
        json_path = None
        for i, arg in enumerate(sys.argv):
            if arg == "--json" and i + 1 < len(sys.argv):
                json_path = sys.argv[i + 1]

        batch = run_batch(json_path=json_path)
        results_json = os.path.join(os.path.dirname(__file__), "batch_run_results.json")
        batch.save_json(results_json)
        summary_md = generate_batch_summary_md(batch)

        # Print machine-parseable summary line
        print(f"\nBATCH_SUMMARY:TOTAL={batch.total}|PASS={batch.passed}|FAIL={batch.failed}|SKIP={batch.skipped}")

        # Exit with non-zero if any failures
        sys.exit(0 if batch.failed == 0 else 1)

    elif len(sys.argv) == 3:
        entity_class = sys.argv[1]
        method_name = sys.argv[2]

        passed, report_path, failure_info = run_single_test(entity_class, method_name)

        if passed:
            print(f"RESULT:PASS|{entity_class}.{method_name}|{report_path}")
        else:
            print(f"RESULT:FAIL|{entity_class}.{method_name}|{report_path}|{failure_info}")

    else:
        print(f"Usage:")
        print(f"  Single: {sys.argv[0]} <entity_class> <method_name>")
        print(f"  Batch:  {sys.argv[0]} --batch [--json tests_to_run.json]")
        sys.exit(1)
