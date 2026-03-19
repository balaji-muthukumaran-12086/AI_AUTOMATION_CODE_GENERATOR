#!/usr/bin/env python3
"""
breakage_analyzer.py
--------------------
Automated Breakage vs Flaky Analyzer for Aalam Suite Runs.

Workflow:
  1. Parse Aalam HTML report → extract failed test cases (class, method, module, owner, error type, pattern)
  2. Generate breakage_rerun.json manifest for batch execution
  3. Rerun each failure N times (configurable) using RunnerAgent
  4. Classify: FLAKY (passed ≥1 of N) vs REAL_BREAKAGE (failed all N)
  5. Generate AI Analysis HTML report with verdict per test case

Usage:
    # Step 1: Parse report only (generates breakage_rerun.json without running)
    .venv/bin/python breakage_analyzer.py parse /path/to/REPORT.html

    # Step 2: Run all breakage cases from the manifest (default 3 retries)
    .venv/bin/python breakage_analyzer.py run

    # Step 2 alt: Run with custom retry count
    .venv/bin/python breakage_analyzer.py run --retries 2

    # Step 2 alt: Run starting from a specific index (resume after interruption)
    .venv/bin/python breakage_analyzer.py run --start 15

    # Full pipeline: Parse + Run + Report in one go
    .venv/bin/python breakage_analyzer.py full /path/to/REPORT.html --retries 3

    # Generate report only (from existing results)
    .venv/bin/python breakage_analyzer.py report
"""

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(__file__))
from config.project_config import (
    PROJECT_NAME, PROJECT_BIN, BASE_DIR, DEPS_DIR,
)
from root_cause_analyzer import diagnose_failure as _diagnose_failure

# ── Hardcoded credentials (common across all automation builds) ──────────────
SDP_ADMIN_EMAIL = "jaya.kumar+org1admin1t0@zohotest.com"
SDP_EMAIL_ID = "jaya.kumar+org1user1t0@zohotest.com"
SDP_PORTAL = "portal1"
SDP_ADMIN_PASS = "Zoho@135"
SDP_TEST_USER_EMAILS = (
    "jaya.kumar+uorg1user2@zohotest.com,"
    "jaya.kumar+uorg1user3@zohotest.com,"
    "jaya.kumar+uorg1user4@zohotest.com,"
    "jaya.kumar+uorg1user5@zohotest.com"
)

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), PROJECT_NAME)
MANIFEST_PATH = os.path.join(PROJECT_ROOT, "breakage_rerun.json")
RESULTS_PATH = os.path.join(PROJECT_ROOT, "breakage_results.json")
AI_REPORTS_DIR = os.path.join(PROJECT_ROOT, "ai_reports")
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 1: Parse Aalam HTML Report
# ══════════════════════════════════════════════════════════════════════════════

class AalamFailureParser(HTMLParser):
    """
    Extracts failures from the "Failed Cases — Run History" table in the Aalam report.
    Each row has: #, Module, Type(UB/PB), Method Name, Class, Pattern, Error
    Owner rows are interspersed as section headers.
    """

    def __init__(self):
        super().__init__()
        self.failures: List[Dict] = []
        self.in_failure_table = False
        self.in_tbody = False
        self.current_row: List[str] = []
        self.current_cell = ""
        self.in_td = False
        self.in_th = False
        self.current_owner = ""
        self.is_owner_row = False
        self.td_count = 0
        self.row_classes = ""
        # Track which card we're in
        self.card_depth = 0
        self.in_failed_cases_card = False
        self.found_failed_header = False

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        classes = attr_dict.get("class", "")

        # Detect the "Failed Cases" card by its heading
        if tag == "h3":
            self._h3_text = ""
            self._in_h3 = True
            return

        if tag == "div" and "card" in classes and "card-accent-red" in classes:
            self.in_failed_cases_card = True

        if self.in_failed_cases_card:
            if tag == "tbody":
                self.in_tbody = True
            elif tag == "tr" and self.in_tbody:
                self.current_row = []
                self.td_count = 0
                self.row_classes = classes
                self.is_owner_row = "owner-row" in classes
            elif tag == "td" and self.in_tbody:
                self.in_td = True
                self.current_cell = ""
                self.td_count += 1

    def handle_endtag(self, tag):
        if hasattr(self, '_in_h3') and self._in_h3 and tag == "h3":
            self._in_h3 = False
            if "Failed Cases" in getattr(self, '_h3_text', ''):
                self.found_failed_header = True
                self.in_failed_cases_card = True

        if not self.in_failed_cases_card:
            return

        if tag == "tbody":
            self.in_tbody = False
        elif tag == "td" and self.in_td:
            self.in_td = False
            self.current_row.append(self.current_cell.strip())
        elif tag == "tr" and self.in_tbody:
            if self.is_owner_row:
                # Extract owner name from the row text
                full_text = " ".join(self.current_row)
                # Owner row text format: "👤 owner.name  (N failures)"
                match = re.search(r'[\U0001F464\s]*([a-zA-Z._]+)\s*\(', full_text)
                if match:
                    self.current_owner = match.group(1).strip()
                else:
                    # Fallback — just take the text before "("
                    parts = full_text.split("(")
                    if parts:
                        self.current_owner = parts[0].strip().lstrip('\U0001F464').strip()
            elif len(self.current_row) >= 7:
                # Data row: #, Module, Type, Method, Class, Pattern, Error
                failure = {
                    "index": self.current_row[0].strip(),
                    "module": self.current_row[1].strip(),
                    "run_type": self.current_row[2].strip(),
                    "method_name": self.current_row[3].strip(),
                    "class_name": self.current_row[4].strip(),
                    "pattern": self.current_row[5].strip(),
                    "error_category": self.current_row[6].strip(),
                    "owner": self.current_owner,
                }
                self.failures.append(failure)

    def handle_data(self, data):
        if hasattr(self, '_in_h3') and self._in_h3:
            self._h3_text = getattr(self, '_h3_text', '') + data
        if self.in_td:
            self.current_cell += data


def extract_build_url(html_path: str) -> Optional[str]:
    """Extract the Build Server URL from an Aalam report.

    Looks for: Build Server: <a href="https://...">...
    """
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    match = re.search(r'Build Server:\s*<a\s+href="(https?://[^"]+)"', content)
    if match:
        return match.group(1)
    return None


def parse_aalam_report(html_path: str) -> List[Dict]:
    """Parse the Aalam HTML report and extract all failed test cases."""
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    parser = AalamFailureParser()
    parser.feed(content)

    if not parser.failures:
        # Fallback: regex-based extraction from the Failed Cases table
        print("[Parser] HTMLParser found 0 failures, trying regex fallback...")
        return _regex_parse_failures(content)

    return parser.failures


def _regex_parse_failures(html: str) -> List[Dict]:
    """Regex fallback parser for the Failed Cases table."""
    failures = []
    current_owner = ""

    # Find owner rows
    owner_pattern = re.compile(
        r'class="owner-row".*?>\s*&#128100;\s*([a-zA-Z._]+)\s', re.DOTALL
    )
    # Find data rows — extract module, type badge, method, class, pattern badge, error badge
    row_pattern = re.compile(
        r'<tr(?:\s+class="[^"]*")?>\s*'
        r'<td[^>]*>(\d+)</td>\s*'            # index
        r'<td[^>]*><b>([^<]+)</b></td>\s*'    # module
        r'<td[^>]*>.*?b-(ub|pb).*?</td>\s*'   # run type badge
        r'<td[^>]*class="mono">([^<]+)</td>\s*'  # method
        r'<td[^>]*class="mono">([^<]+)</td>\s*'  # class
        r'<td[^>]*>.*?b-(warn|fail).*?</td>\s*'  # pattern
        r'<td[^>]*>.*?b-cat">([^<]+)<',          # error
        re.DOTALL
    )

    # Split by owner rows to track ownership
    parts = re.split(r'(<tr\s+class="owner-row"[^>]*>.*?</tr>)', html, flags=re.DOTALL)

    for part in parts:
        owner_match = owner_pattern.search(part)
        if owner_match:
            current_owner = owner_match.group(1).strip()
            continue

        for match in row_pattern.finditer(part):
            pattern_text = "FLAKY" if match.group(6) == "warn" else "CONSISTENT"
            failures.append({
                "index": match.group(1),
                "module": match.group(2).strip(),
                "run_type": match.group(3).upper(),
                "method_name": match.group(4).strip(),
                "class_name": match.group(5).strip(),
                "pattern": pattern_text,
                "error_category": match.group(7).strip(),
                "owner": current_owner,
            })

    return failures


def generate_manifest(failures: List[Dict], output_path: str,
                      build_url: Optional[str] = None) -> str:
    """Generate breakage_rerun.json from parsed failures."""
    # Deduplicate: same class+method should only appear once
    seen = set()
    unique_failures = []
    for f in failures:
        key = (f["class_name"], f["method_name"])
        if key not in seen:
            seen.add(key)
            unique_failures.append(f)

    manifest = {
        "_comment": "Auto-generated by breakage_analyzer.py from Aalam report",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total_failures": len(unique_failures),
        "source_report": "",
        "build_url": build_url or "",
        "credentials": {
            "admin_email": SDP_ADMIN_EMAIL,
            "email_id": SDP_EMAIL_ID,
            "portal": SDP_PORTAL,
            "password": SDP_ADMIN_PASS,
            "test_user_emails": SDP_TEST_USER_EMAILS,
        },
        "tests": []
    }

    for i, f in enumerate(unique_failures, 1):
        manifest["tests"].append({
            "index": i,
            "entity_class": f["class_name"],
            "method_name": f["method_name"],
            "module": f["module"],
            "run_type": f["run_type"],
            "original_pattern": f["pattern"],
            "error_category": f["error_category"],
            "owner": f["owner"],
            "ai_status": "PENDING",
            "ai_runs": [],
        })

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w") as fp:
        json.dump(manifest, fp, indent=2)

    return output_path


# ══════════════════════════════════════════════════════════════════════════════
# STEP 2: Rerun Breakage Cases
# ══════════════════════════════════════════════════════════════════════════════

def _get_report_result(method_name: str) -> Optional[str]:
    """Check the latest ScenarioReport.html for a test's PASS/FAIL."""
    if not os.path.isdir(REPORTS_DIR):
        return None
    matching = sorted(
        [d for d in os.listdir(REPORTS_DIR)
         if d.startswith(f"LOCAL_{method_name}_")],
        reverse=True
    )
    if not matching:
        return None
    html_path = os.path.join(REPORTS_DIR, matching[0], "ScenarioReport.html")
    if not os.path.isfile(html_path):
        return None
    with open(html_path, "r") as f:
        content = f.read()
    if 'data-result="FAIL"' in content or "$$Failure" in content:
        return "FAIL"
    if 'data-result="PASS"' in content:
        return "PASS"
    # Fallback text-based detection
    if "Additional Specific Info" in content and "successfully" in content.lower():
        return "PASS"
    return None


def run_breakage_batch(retries: int = 3, start_index: int = 0):
    """Rerun each failure from breakage_rerun.json N times, classify results."""
    from agents.runner_agent import RunnerAgent

    if not os.path.exists(MANIFEST_PATH):
        print(f"[Error] Manifest not found: {MANIFEST_PATH}")
        print("        Run 'breakage_analyzer.py parse <report.html>' first.")
        sys.exit(1)

    with open(MANIFEST_PATH) as f:
        manifest = json.load(f)

    tests = manifest["tests"]
    total = len(tests)
    build_url = manifest.get("build_url", "") or None
    sdp_url = build_url if build_url else "http://localhost:8080"
    print(f"  Build URL: {sdp_url}")
    runner = RunnerAgent(base_dir=BASE_DIR, deps_dir=DEPS_DIR, pre_compiled_bin_dir=PROJECT_BIN)

    print(f"\n{'='*70}")
    print(f"  BREAKAGE ANALYZER — Rerunning {total} failures × {retries} retries")
    print(f"  Starting from index: {start_index}")
    print(f"{'='*70}\n")

    for i, test in enumerate(tests):
        if i < start_index:
            if test["ai_status"] == "PENDING":
                continue  # skip already-processed tests that were before start
            continue

        entity = test["entity_class"]
        method = test["method_name"]
        run_results = test.get("ai_runs", [])

        print(f"\n[{i+1}/{total}] {entity}.{method}", flush=True)
        print(f"         Module: {test['module']} | Owner: {test['owner']} | "
              f"Original: {test['original_pattern']}")

        already_passed = False
        for attempt in range(retries):
            print(f"         Attempt {attempt+1}/{retries} ... ", end="", flush=True)

            start_time = time.time()
            try:
                result = runner.run_test(
                    entity_class=entity,
                    method_name=method,
                    url=sdp_url,
                    admin_mail_id=SDP_ADMIN_EMAIL,
                    email_id=SDP_EMAIL_ID,
                    portal_name=SDP_PORTAL,
                    skip_compile=True,
                    password=SDP_ADMIN_PASS,
                    skip_cleanup=False,
                    test_user_emails=SDP_TEST_USER_EMAILS,
                )
                duration = time.time() - start_time

                # Also check ScenarioReport.html for more reliable result
                report_result = _get_report_result(method)
                if report_result:
                    passed = report_result == "PASS"
                else:
                    passed = result.success

                error = ""
                if not passed:
                    error = str(result.error)[:300] if result.error else ""
                    if result.stderr:
                        for line in result.stderr.splitlines():
                            if any(kw in line for kw in ["REASON:", "FAILURE:", "$$Failure"]):
                                error = line.strip()[:300]
                                break

            except Exception as e:
                duration = time.time() - start_time
                passed = False
                error = str(e)[:300]

            status = "PASS" if passed else "FAIL"
            run_results.append({
                "attempt": attempt + 1,
                "status": status,
                "duration": round(duration, 1),
                "error": error if not passed else "",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            })

            print(f"{status} ({duration:.0f}s)")

            if passed:
                already_passed = True
                # Early exit: one PASS is enough to classify as FLAKY
                # Fill remaining attempts as SKIPPED
                for remaining in range(attempt + 2, retries + 1):
                    run_results.append({
                        "attempt": remaining,
                        "status": "SKIPPED",
                        "duration": 0,
                        "error": "Skipped — already passed once (flaky confirmed)",
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
                break

        # Classify
        pass_count = sum(1 for r in run_results if r["status"] == "PASS")
        fail_count = sum(1 for r in run_results if r["status"] == "FAIL")

        if pass_count > 0:
            test["ai_status"] = "FLAKY"
            test["ai_verdict"] = "AI_ANALYSED: Zero Issues (Flaky)"
        else:
            test["ai_status"] = "REAL_BREAKAGE"
            test["ai_verdict"] = "AI_ANALYSED: Real Breakage — Needs Fix"

            # Root cause analysis for real breakages
            last_error = ""
            for r in reversed(run_results):
                if r.get("error"):
                    last_error = r["error"]
                    break
            try:
                diag = _diagnose_failure(
                    method_name=method,
                    entity_class=entity,
                    error_msg=last_error,
                    reports_dir=REPORTS_DIR,
                    src_dir=os.path.join(PROJECT_ROOT, "src"),
                    sdp_url=sdp_url,
                    admin_email=SDP_ADMIN_EMAIL,
                    admin_pass=SDP_ADMIN_PASS,
                    portal=SDP_PORTAL,
                    verify=False,
                )
                test["diagnosis"] = diag.to_dict()
                print(f"         Root Cause: {diag.root_cause} ({diag.confidence}) — {diag.summary[:80]}")
            except Exception as diag_err:
                test["diagnosis"] = {"root_cause": "UNDETERMINED", "confidence": "LOW",
                                     "summary": f"Diagnosis failed: {diag_err}", "details": "", "evidence": []}

        test["ai_runs"] = run_results
        test["ai_pass_count"] = pass_count
        test["ai_fail_count"] = fail_count
        test["ai_total_runs"] = len([r for r in run_results if r["status"] != "SKIPPED"])

        verdict_symbol = "\u2714 FLAKY" if test["ai_status"] == "FLAKY" else "\u2718 REAL BREAKAGE"
        print(f"         Verdict: {verdict_symbol} "
              f"({pass_count}P/{fail_count}F out of {test['ai_total_runs']} runs)")

        # Save progress after each test (resume-friendly)
        manifest["tests"] = tests
        with open(MANIFEST_PATH, "w") as fp:
            json.dump(manifest, fp, indent=2)

    # Final summary
    flaky_count = sum(1 for t in tests if t.get("ai_status") == "FLAKY")
    real_count = sum(1 for t in tests if t.get("ai_status") == "REAL_BREAKAGE")
    pending_count = sum(1 for t in tests if t.get("ai_status") == "PENDING")

    print(f"\n{'='*70}")
    print(f"  BREAKAGE ANALYSIS COMPLETE")
    print(f"  {'─'*40}")
    print(f"  FLAKY (Zero Issues):     {flaky_count}")
    print(f"  REAL BREAKAGE:           {real_count}")
    if pending_count:
        print(f"  PENDING:                 {pending_count}")
    print(f"  {'─'*40}")
    print(f"  Total:                   {total}")
    if real_count == 0:
        print(f"\n  \u2714 AI_ANALYSED: ZERO ISSUES BUILD — Safe to promote!")
    else:
        print(f"\n  \u2718 {real_count} real breakage(s) need attention before promotion.")
    print(f"{'='*70}")

    # Save final results separately
    _save_results(manifest)

    return manifest


def _save_results(manifest: Dict):
    """Save final classified results to breakage_results.json."""
    tests = manifest["tests"]
    summary = {
        "analyzed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(tests),
        "flaky": sum(1 for t in tests if t.get("ai_status") == "FLAKY"),
        "real_breakage": sum(1 for t in tests if t.get("ai_status") == "REAL_BREAKAGE"),
        "pending": sum(1 for t in tests if t.get("ai_status") == "PENDING"),
    }
    output = {"summary": summary, "tests": tests}
    with open(RESULTS_PATH, "w") as fp:
        json.dump(output, fp, indent=2)
    print(f"\n  Results saved: {RESULTS_PATH}")


# ══════════════════════════════════════════════════════════════════════════════
# STEP 3: Generate AI Analysis HTML Report
# ══════════════════════════════════════════════════════════════════════════════

def generate_report(source_html: Optional[str] = None):
    """Generate the AI Analysis HTML report from breakage_results.json."""
    if not os.path.exists(RESULTS_PATH):
        # Try to use the manifest if results don't exist yet
        if os.path.exists(MANIFEST_PATH):
            with open(MANIFEST_PATH) as f:
                manifest = json.load(f)
            tests = manifest["tests"]
        else:
            print("[Error] No results found. Run analysis first.")
            sys.exit(1)
    else:
        with open(RESULTS_PATH) as f:
            data = json.load(f)
        tests = data["tests"]

    summary = {
        "total": len(tests),
        "flaky": sum(1 for t in tests if t.get("ai_status") == "FLAKY"),
        "real_breakage": sum(1 for t in tests if t.get("ai_status") == "REAL_BREAKAGE"),
        "pending": sum(1 for t in tests if t.get("ai_status") == "PENDING"),
    }

    now = datetime.now()
    report_name = f"AI_BREAKAGE_ANALYSIS_{now.strftime('%Y_%m_%d_%H_%M')}.html"
    os.makedirs(AI_REPORTS_DIR, exist_ok=True)
    report_path = os.path.join(AI_REPORTS_DIR, report_name)

    # Group by owner
    by_owner: Dict[str, List[Dict]] = {}
    for t in tests:
        owner = t.get("owner", "unknown")
        by_owner.setdefault(owner, []).append(t)

    # Group by module
    by_module: Dict[str, Dict] = {}
    for t in tests:
        mod = t.get("module", "UNKNOWN")
        if mod not in by_module:
            by_module[mod] = {"total": 0, "flaky": 0, "real": 0}
        by_module[mod]["total"] += 1
        if t.get("ai_status") == "FLAKY":
            by_module[mod]["flaky"] += 1
        elif t.get("ai_status") == "REAL_BREAKAGE":
            by_module[mod]["real"] += 1

    # Build HTML
    html = _build_report_html(tests, summary, by_owner, by_module, now, source_html)

    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n  AI Analysis Report: {report_path}")
    return report_path


def _build_report_html(
    tests: List[Dict],
    summary: Dict,
    by_owner: Dict[str, List[Dict]],
    by_module: Dict[str, Dict],
    timestamp: datetime,
    source_html: Optional[str] = None,
) -> str:
    """Build the complete AI Analysis HTML report."""

    zero_issues = summary["real_breakage"] == 0 and summary["pending"] == 0
    verdict_class = "verdict-pass" if zero_issues else "verdict-fail"
    verdict_text = ("AI_ANALYSED: ZERO ISSUES BUILD — Safe to Promote"
                    if zero_issues
                    else f"AI_ANALYSED: {summary['real_breakage']} Real Breakage(s) — Needs Attention")

    # Root cause breakdown counts
    rc_counts = {"AUTOMATION_BUG": 0, "PRODUCT_BUG": 0, "ENVIRONMENT": 0, "UNDETERMINED": 0}
    for t in tests:
        rc = t.get("diagnosis", {}).get("root_cause", "")
        if rc in rc_counts:
            rc_counts[rc] += 1

    # Build test rows
    test_rows = []
    for t in tests:
        status = t.get("ai_status", "PENDING")
        verdict = t.get("ai_verdict", "PENDING")

        if status == "FLAKY":
            status_badge = '<span class="badge b-flaky">FLAKY</span>'
            verdict_badge = '<span class="badge b-pass-verdict">Zero Issues</span>'
        elif status == "REAL_BREAKAGE":
            status_badge = '<span class="badge b-breakage">REAL BREAKAGE</span>'
            verdict_badge = '<span class="badge b-fail-verdict">Needs Fix</span>'
        else:
            status_badge = '<span class="badge b-pending">PENDING</span>'
            verdict_badge = '<span class="badge b-pending">—</span>'

        # Run history icons
        run_icons = ""
        for r in t.get("ai_runs", []):
            if r["status"] == "PASS":
                run_icons += '<span class="run-pass" title="PASS">&#10003;</span> '
            elif r["status"] == "FAIL":
                run_icons += '<span class="run-fail" title="FAIL">&#10007;</span> '
            else:
                run_icons += '<span class="run-skip" title="SKIPPED">&#9711;</span> '

        pass_count = t.get("ai_pass_count", 0)
        fail_count = t.get("ai_fail_count", 0)
        total_runs = t.get("ai_total_runs", 0)

        original_badge = ""
        if t.get("original_pattern") == "CONSISTENT":
            original_badge = '<span class="badge b-consistent-sm">CONSISTENT</span>'
        elif t.get("original_pattern") == "FLAKY":
            original_badge = '<span class="badge b-flaky-sm">FLAKY</span>'

        # Root cause diagnosis badge
        diag = t.get("diagnosis", {})
        rc = diag.get("root_cause", "")
        rc_conf = diag.get("confidence", "")
        rc_summary = diag.get("summary", "")
        if rc == "AUTOMATION_BUG":
            rc_badge = f'<span class="badge b-auto-bug" title="{rc_summary}">AUTOMATION BUG</span>'
        elif rc == "PRODUCT_BUG":
            rc_badge = f'<span class="badge b-prod-bug" title="{rc_summary}">PRODUCT BUG</span>'
        elif rc == "ENVIRONMENT":
            rc_badge = f'<span class="badge b-env" title="{rc_summary}">ENVIRONMENT</span>'
        elif rc == "UNDETERMINED":
            rc_badge = f'<span class="badge b-undetermined" title="{rc_summary}">UNDETERMINED</span>'
        else:
            rc_badge = "—"
        rc_conf_txt = f'<span class="conf-{rc_conf.lower()}">{rc_conf}</span>' if rc_conf else ""

        test_rows.append(f"""<tr class="{'row-flaky' if status == 'FLAKY' else 'row-breakage' if status == 'REAL_BREAKAGE' else ''}">
  <td class="mono">{t.get('method_name', '')}</td>
  <td class="mono">{t.get('entity_class', '')}</td>
  <td><b>{t.get('module', '')}</b></td>
  <td>{t.get('owner', '')}</td>
  <td>{t.get('run_type', '')}</td>
  <td>{original_badge}</td>
  <td><span class="badge b-cat">{t.get('error_category', '')}</span></td>
  <td>{status_badge}</td>
  <td style="font-size:0.75rem">{run_icons}</td>
  <td>{pass_count}P / {fail_count}F</td>
  <td>{rc_badge} {rc_conf_txt}</td>
  <td>{verdict_badge}</td>
</tr>""")

    # Module rows
    module_rows = []
    for mod, stats in sorted(by_module.items()):
        rate = ((stats["flaky"] / stats["total"]) * 100) if stats["total"] > 0 else 0
        module_rows.append(f"""<tr>
  <td style="text-align:left;font-weight:700">{mod}</td>
  <td>{stats['total']}</td>
  <td style="color:#10B981;font-weight:700">{stats['flaky']}</td>
  <td style="color:#EF4444;font-weight:700">{stats['real']}</td>
  <td><span class="mod-badge {'mod-badge-green' if stats['real'] == 0 else 'mod-badge-red'}">{rate:.0f}% Flaky</span></td>
</tr>""")

    # Owner summary rows
    owner_rows = []
    for owner, owner_tests in sorted(by_owner.items()):
        flaky_c = sum(1 for t in owner_tests if t.get("ai_status") == "FLAKY")
        real_c = sum(1 for t in owner_tests if t.get("ai_status") == "REAL_BREAKAGE")
        total_c = len(owner_tests)
        owner_verdict = "Zero Issues" if real_c == 0 else f"{real_c} Real Breakage(s)"
        owner_color = "#10B981" if real_c == 0 else "#EF4444"
        owner_rows.append(f"""<tr>
  <td style="text-align:left;font-weight:700">{owner}</td>
  <td>{total_c}</td>
  <td style="color:#10B981;font-weight:700">{flaky_c}</td>
  <td style="color:#EF4444;font-weight:700">{real_c}</td>
  <td><span style="color:{owner_color};font-weight:700">{owner_verdict}</span></td>
</tr>""")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Breakage Analysis — {timestamp.strftime('%d %B %Y, %I:%M %p')}</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
:root {{
  --bg: #F8FAFB; --surface: #FFFFFF; --surface2: #F1F5F9;
  --border: #E2E8F0; --text: #1E293B; --muted: #64748B;
  --green: #10B981; --red: #EF4444; --teal: #00B2BD;
  --orange: #F59E0B; --purple: #7C3AED;
  --radius: 12px;
  --shadow: 0 1px 3px rgba(0,0,0,0.08);
  --shadow-lg: 0 4px 12px rgba(0,0,0,0.12);
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}

#banner {{
  background: linear-gradient(135deg, #0d2137 0%, #1a3a5c 50%, #0d2137 100%);
  color: white; padding: 24px 44px;
}}
#banner-inner {{ display: flex; align-items: center; gap: 32px; max-width: 1520px; margin: 0 auto; }}
.brand-name {{ font-size: 1rem; font-weight: 800; }}
.brand-sub {{ font-size: 0.64rem; color: #94A3B8; margin-top: 2px; }}
#banner-title h1 {{ font-size: 1.5rem; font-weight: 800; }}
.banner-sub {{ font-size: 0.71rem; color: #94A3B8; margin-top: 5px; }}
#banner-stats {{ display: flex; gap: 24px; margin-left: auto; }}
.banner-stat {{ text-align: center; }}
.banner-stat .bval {{ font-size: 1.4rem; font-weight: 800; line-height: 1; }}
.banner-stat .blbl {{ font-size: 0.56rem; color: #94A3B8; margin-top: 4px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; }}

#main {{ padding: 32px 44px 64px; max-width: 1520px; margin: 0 auto; }}

/* Verdict Banner */
.verdict-banner {{ padding: 20px 28px; border-radius: var(--radius); margin-bottom: 28px; font-size: 1.1rem; font-weight: 800; text-align: center; }}
.verdict-pass {{ background: linear-gradient(135deg, #D1FAE5, #A7F3D0); color: #065F46; border: 2px solid #10B981; }}
.verdict-fail {{ background: linear-gradient(135deg, #FEE2E2, #FECACA); color: #991B1B; border: 2px solid #EF4444; }}

/* Hero Stats */
.hero-stats {{ display: flex; gap: 12px; flex-wrap: wrap; margin: 0 0 22px; }}
.hero-card {{ background: var(--surface); border-radius: var(--radius); padding: 16px 22px; box-shadow: var(--shadow); border-bottom: 3px solid transparent; min-width: 140px; }}
.hero-card .val {{ font-size: 2rem; font-weight: 800; line-height: 1; margin-top: 4px; }}
.hero-card .lbl {{ font-size: 0.6rem; color: var(--muted); margin-top: 7px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; }}
.c-green .val {{ color: var(--green); }} .c-green {{ border-color: var(--green); }}
.c-red .val {{ color: var(--red); }} .c-red {{ border-color: var(--red); }}
.c-blue .val {{ color: var(--teal); }} .c-blue {{ border-color: var(--teal); }}
.c-orange .val {{ color: var(--orange); }} .c-orange {{ border-color: var(--orange); }}
.c-purple .val {{ color: var(--purple); }} .c-purple {{ border-color: var(--purple); }}

/* Cards */
.card {{ background: var(--surface); border-radius: var(--radius); box-shadow: var(--shadow); margin-bottom: 20px; overflow: hidden; }}
.card-head {{ display: flex; justify-content: space-between; align-items: center; padding: 14px 20px; cursor: pointer; }}
.card-head:hover {{ background: #EDF4F5; }}
.card-head h3 {{ font-size: 0.92rem; font-weight: 700; }}
.card-body {{ padding: 18px 20px 16px; }}
.card.collapsed .card-body {{ display: none; }}
.card-accent-green {{ border-top: 3px solid var(--green); }}
.card-accent-red {{ border-top: 3px solid var(--red); }}
.card-accent-blue {{ border-top: 3px solid var(--teal); }}
.card-accent-purple {{ border-top: 3px solid var(--purple); }}

/* Tables */
.scroll-table {{ overflow: auto; max-height: 700px; border-radius: 10px; border: 1px solid var(--border); }}
table {{ width: 100%; border-collapse: collapse; font-size: 0.79rem; }}
thead {{ position: sticky; top: 0; z-index: 2; }}
th {{ padding: 10px 12px; background: #0d2137; color: white; font-size: 0.68rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; text-align: center; }}
th:first-child {{ text-align: left; }}
td {{ padding: 8px 12px; text-align: center; border-bottom: 1px solid var(--border); }}
td:first-child {{ text-align: left; }}
tr:hover td {{ background: #EDF9FA; }}
.mono {{ font-family: 'Cascadia Code', 'Fira Code', monospace; font-size: 0.72rem; }}

/* Badges */
.badge {{ display: inline-block; padding: 3px 9px; border-radius: 6px; font-size: 0.64rem; font-weight: 700; white-space: nowrap; }}
.b-flaky {{ background: #D1FAE5; color: #065F46; }}
.b-breakage {{ background: #FEE2E2; color: #991B1B; }}
.b-pending {{ background: #F1F5F9; color: #475569; }}
.b-pass-verdict {{ background: #CCFBF1; color: #0F766E; font-size: 0.72rem; padding: 4px 12px; }}
.b-fail-verdict {{ background: #FEE2E2; color: #991B1B; font-size: 0.72rem; padding: 4px 12px; }}
.b-cat {{ background: #E0F2FE; color: #0369A1; }}
.b-consistent-sm {{ background: #FEE2E2; color: #991B1B; font-size: 0.6rem; }}
.b-flaky-sm {{ background: #FEF3C7; color: #92400E; font-size: 0.6rem; }}

/* Run history icons */
.run-pass {{ color: #10B981; font-weight: 700; }}
.run-fail {{ color: #EF4444; font-weight: 700; }}
.run-skip {{ color: #94A3B8; }}

/* Row highlights */
.row-flaky td {{ background: #F0FDF4 !important; }}
.row-breakage td {{ background: #FFF1F2 !important; }}

/* Module table */
.mod-badge {{ display: inline-block; font-size: 0.72rem; font-weight: 800; padding: 4px 14px; border-radius: 999px; }}
.mod-badge-green {{ background: #D1FAE5; color: #065F46; }}
.mod-badge-red {{ background: #FEE2E2; color: #991B1B; }}

/* Note */
.note {{ background: #EFF6FF; border-left: 4px solid var(--teal); padding: 10px 14px; border-radius: 0 8px 8px 0; font-size: 0.8rem; color: var(--text); margin-bottom: 14px; }}

/* Root Cause badges */
.b-auto-bug {{ background: #FEF3C7; color: #92400E; }}
.b-prod-bug {{ background: #FEE2E2; color: #991B1B; }}
.b-env {{ background: #E0E7FF; color: #3730A3; }}
.b-undetermined {{ background: #F1F5F9; color: #475569; }}
.conf-high {{ font-size: 0.6rem; font-weight: 700; color: #065F46; }}
.conf-medium {{ font-size: 0.6rem; font-weight: 700; color: #92400E; }}
.conf-low {{ font-size: 0.6rem; font-weight: 700; color: #94A3B8; }}
</style>
</head>
<body>

<div id="banner">
<div id="banner-inner">
  <div>
    <div class="brand-name">SDPODQA AI Automation</div>
    <div class="brand-sub">Breakage Analyzer</div>
  </div>
  <div id="banner-title">
    <h1>AI Breakage Analysis Report</h1>
    <div class="banner-sub">{timestamp.strftime('%d %B %Y, %I:%M %p')} &nbsp;|&nbsp; {summary['total']} failures analyzed</div>
  </div>
  <div id="banner-stats">
    <div class="banner-stat"><div class="bval" style="color:#10B981">{summary['flaky']}</div><div class="blbl">Flaky (Zero Issues)</div></div>
    <div class="banner-stat"><div class="bval" style="color:#EF4444">{summary['real_breakage']}</div><div class="blbl">Real Breakage</div></div>
    <div class="banner-stat"><div class="bval" style="color:#00B2BD">{summary['total']}</div><div class="blbl">Total Analyzed</div></div>
  </div>
</div>
</div>

<div id="main">

<!-- Verdict Banner -->
<div class="verdict-banner {verdict_class}">
  {verdict_text}
</div>

<!-- Hero Stats -->
<div class="hero-stats">
  <div class="hero-card c-green"><div class="val">{summary['flaky']}</div><div class="lbl">Flaky — Zero Issues</div></div>
  <div class="hero-card c-red"><div class="val">{summary['real_breakage']}</div><div class="lbl">Real Breakage</div></div>
  <div class="hero-card c-blue"><div class="val">{summary['total']}</div><div class="lbl">Total Analyzed</div></div>
  <div class="hero-card c-purple"><div class="val">{summary.get('pending', 0)}</div><div class="lbl">Pending</div></div>
</div>

<!-- Root Cause Breakdown (for real breakages) -->
{f'''<div class="hero-stats" style="margin-top:0">
  <div class="hero-card c-orange"><div class="val">{rc_counts["AUTOMATION_BUG"]}</div><div class="lbl">Automation Bug</div></div>
  <div class="hero-card c-red"><div class="val">{rc_counts["PRODUCT_BUG"]}</div><div class="lbl">Product Bug</div></div>
  <div class="hero-card c-purple"><div class="val">{rc_counts["ENVIRONMENT"]}</div><div class="lbl">Environment</div></div>
  <div class="hero-card" style="border-color:#94A3B8"><div class="val" style="color:#94A3B8">{rc_counts["UNDETERMINED"]}</div><div class="lbl">Undetermined</div></div>
</div>''' if summary['real_breakage'] > 0 else ''}

<!-- Module Breakdown -->
<div class="card card-accent-blue">
<div class="card-head" onclick="this.closest('.card').classList.toggle('collapsed')">
  <h3>&#128202; Module Breakdown</h3><span>&#9660;</span>
</div>
<div class="card-body">
<div class="scroll-table"><table>
<thead><tr><th>Module</th><th>Total Failures</th><th>Flaky</th><th>Real Breakage</th><th>Flaky Rate</th></tr></thead>
<tbody>
{''.join(module_rows)}
</tbody></table></div>
</div></div>

<!-- Owner Summary -->
<div class="card card-accent-purple">
<div class="card-head" onclick="this.closest('.card').classList.toggle('collapsed')">
  <h3>&#128100; Owner Summary</h3><span>&#9660;</span>
</div>
<div class="card-body">
<p class="note">Per-owner breakdown: if all failures for an owner are flaky, their verdict is <b>Zero Issues</b>.</p>
<div class="scroll-table"><table>
<thead><tr><th>Owner</th><th>Total Failures</th><th>Flaky</th><th>Real Breakage</th><th>Verdict</th></tr></thead>
<tbody>
{''.join(owner_rows)}
</tbody></table></div>
</div></div>

<!-- Full Results Table -->
<div class="card card-accent-red">
<div class="card-head" onclick="this.closest('.card').classList.toggle('collapsed')">
  <h3>&#128269; Full AI Analysis Results ({summary['total']} tests)</h3><span>&#9660;</span>
</div>
<div class="card-body">
<p class="note">
  <span class="badge b-flaky">FLAKY</span> = passed at least once in AI rerun &rarr; Zero Issues &nbsp;|&nbsp;
  <span class="badge b-breakage">REAL BREAKAGE</span> = failed all AI reruns &rarr; Needs Fix
</p>
<div class="scroll-table"><table>
<thead><tr>
  <th>Method Name</th><th>Class</th><th>Module</th><th>Owner</th><th>Type</th>
  <th>Aalam Pattern</th><th>Error</th><th>AI Status</th><th>AI Run History</th><th>AI Runs</th><th>Root Cause</th><th>AI Verdict</th>
</tr></thead>
<tbody>
{''.join(test_rows)}
</tbody></table></div>
</div></div>

<!-- Real Breakages Only (for quick developer action) -->
<div class="card card-accent-red">
<div class="card-head" onclick="this.closest('.card').classList.toggle('collapsed')">
  <h3>&#9888; Real Breakages — Action Required ({summary['real_breakage']})</h3><span>&#9660;</span>
</div>
<div class="card-body">
{_build_real_breakage_section(tests)}
</div></div>

</div>
<script>
function toggleCard(head) {{ head.closest('.card').classList.toggle('collapsed'); }}
</script>
</body>
</html>"""


def _build_real_breakage_section(tests: List[Dict]) -> str:
    """Build the real-breakage-only table HTML."""
    real = [t for t in tests if t.get("ai_status") == "REAL_BREAKAGE"]
    if not real:
        return '<p class="note" style="background:#D1FAE5;border-left-color:#10B981">No real breakages found!</p>'

    rows = []
    for t in real:
        error_snippets = []
        for r in t.get("ai_runs", []):
            if r.get("error"):
                error_snippets.append(r["error"][:120])
        error_text = "<br>".join(set(error_snippets[:2])) if error_snippets else "—"

        diag = t.get("diagnosis", {})
        rc = diag.get("root_cause", "")
        rc_summary = diag.get("summary", "")
        rc_conf = diag.get("confidence", "")
        if rc == "AUTOMATION_BUG":
            rc_badge = f'<span class="badge b-auto-bug">AUTOMATION BUG</span>'
        elif rc == "PRODUCT_BUG":
            rc_badge = f'<span class="badge b-prod-bug">PRODUCT BUG</span>'
        elif rc == "ENVIRONMENT":
            rc_badge = f'<span class="badge b-env">ENVIRONMENT</span>'
        elif rc == "UNDETERMINED":
            rc_badge = f'<span class="badge b-undetermined">UNDETERMINED</span>'
        else:
            rc_badge = "—"

        rows.append(f"""<tr class="row-breakage">
  <td class="mono" style="text-align:left">{t.get('method_name', '')}</td>
  <td class="mono" style="text-align:left">{t.get('entity_class', '')}</td>
  <td><b>{t.get('module', '')}</b></td>
  <td>{t.get('owner', '')}</td>
  <td><span class="badge b-cat">{t.get('error_category', '')}</span></td>
  <td>{rc_badge}<br><span style="font-size:0.64rem;color:#64748B">{rc_summary[:120]}</span></td>
  <td style="font-size:0.72rem;max-width:300px;word-break:break-word">{error_text}</td>
</tr>""")

    return f"""<div class="scroll-table"><table>
<thead><tr><th>Method</th><th>Class</th><th>Module</th><th>Owner</th><th>Error Type</th><th>Root Cause</th><th>Error Details</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>"""


# ══════════════════════════════════════════════════════════════════════════════
# CLI
# ══════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Automated Breakage vs Flaky Analyzer for Aalam Suite Runs"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # parse
    parse_cmd = subparsers.add_parser("parse", help="Parse Aalam HTML report and generate rerun manifest")
    parse_cmd.add_argument("html_path", help="Path to the Aalam HTML report file")

    # run
    run_cmd = subparsers.add_parser("run", help="Rerun breakage cases from manifest")
    run_cmd.add_argument("--retries", type=int, default=3, help="Number of reruns per test (default: 3)")
    run_cmd.add_argument("--start", type=int, default=0, help="Start from this test index (0-based)")

    # report
    report_cmd = subparsers.add_parser("report", help="Generate AI analysis HTML report from results")
    report_cmd.add_argument("--source", help="Path to original Aalam HTML report (optional)")

    # full
    full_cmd = subparsers.add_parser("full", help="Full pipeline: parse + run + report")
    full_cmd.add_argument("html_path", help="Path to the Aalam HTML report file")
    full_cmd.add_argument("--retries", type=int, default=3, help="Number of reruns per test")

    args = parser.parse_args()

    if args.command == "parse":
        print(f"\n[Step 1] Parsing Aalam report: {args.html_path}")
        failures = parse_aalam_report(args.html_path)
        print(f"         Found {len(failures)} failures")

        # Show summary
        by_owner: Dict[str, int] = {}
        by_module: Dict[str, int] = {}
        for f in failures:
            by_owner[f["owner"]] = by_owner.get(f["owner"], 0) + 1
            by_module[f["module"]] = by_module.get(f["module"], 0) + 1

        print(f"\n  By Module:")
        for mod, count in sorted(by_module.items()):
            print(f"    {mod:20s} {count}")
        print(f"\n  By Owner:")
        for owner, count in sorted(by_owner.items()):
            print(f"    {owner:25s} {count}")

        # Generate manifest
        build_url = extract_build_url(args.html_path)
        if build_url:
            print(f"\n  Build URL: {build_url}")
        manifest_path = generate_manifest(failures, MANIFEST_PATH, build_url=build_url)
        print(f"\n  Manifest saved: {manifest_path}")
        print(f"\n  Next step: .venv/bin/python breakage_analyzer.py run --retries 3")

    elif args.command == "run":
        run_breakage_batch(retries=args.retries, start_index=args.start)
        print(f"\n  Next step: .venv/bin/python breakage_analyzer.py report")

    elif args.command == "report":
        generate_report(source_html=args.source if hasattr(args, 'source') else None)

    elif args.command == "full":
        print(f"\n[Step 1] Parsing Aalam report: {args.html_path}")
        failures = parse_aalam_report(args.html_path)
        build_url = extract_build_url(args.html_path)
        if build_url:
            print(f"         Build URL: {build_url}")
        print(f"         Found {len(failures)} failures")
        generate_manifest(failures, MANIFEST_PATH, build_url=build_url)

        print(f"\n[Step 2] Running breakage batch ({args.retries} retries per test)")
        run_breakage_batch(retries=args.retries)

        print(f"\n[Step 3] Generating AI analysis report")
        generate_report(source_html=args.html_path)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
