#!/usr/bin/env python3
"""
generate_batch_summary.py
-------------------------
Generates batch summary reports for both test generation and execution.

Modes:
  execution (default)  — post-run summary with pass/fail, self-healing, bug analysis
  generate             — post-generation summary with coverage, effort saved, batch overview
  usecase-analysis     — requirement analysis of use-case CSV with batch segregation

Reads:
  - $PROJECT_NAME/tests_to_run.json  → test manifest
  - ScenarioReport.html              → per-test results (execution mode only)
  - Testcase/*.csv                   → use-case document (coverage mapping)
  - config/project_config.py         → project metadata

Outputs:
  - $PROJECT_NAME/ai_reports/BATCH_SUMMARY_<timestamp>.md        (execution mode)
  - $PROJECT_NAME/ai_reports/GENERATION_SUMMARY_<timestamp>.md   (generate mode)
  - $PROJECT_NAME/ai_reports/USECASE_ANALYSIS_<timestamp>.md     (usecase-analysis mode)

Usage:
    .venv/bin/python generate_batch_summary.py                          # execution summary
    .venv/bin/python generate_batch_summary.py --mode generate          # generation summary
    .venv/bin/python generate_batch_summary.py --mode generate --start-time 1773400000  # with timing
    .venv/bin/python generate_batch_summary.py --mode usecase-analysis  # requirement analysis
"""

import argparse
import os
import re
import csv
import json
import glob
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))
from config.project_config import PROJECT_NAME, PROJECT_ROOT


# ──────────────────────────────────────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────────────────────────────────────
REPORTS_DIR = os.path.join(PROJECT_ROOT, "reports")
AI_REPORTS_DIR = os.path.join(PROJECT_ROOT, "ai_reports")
TESTCASE_DIR = os.path.join(PROJECT_ROOT, "Testcase")
TESTS_TO_RUN = os.path.join(PROJECT_ROOT, "tests_to_run.json")

# Average manual QA time per test case (minutes) — industry benchmark
MANUAL_TEST_AVG_MINUTES = 15
# Average time to write one automation test case manually (minutes)
MANUAL_AUTHORING_AVG_MINUTES = 45
# Maximum gap between self-healing retries (ms) — dirs further apart are separate sessions
SELF_HEAL_GAP_MS = 90 * 60 * 1000  # 90 minutes


# ──────────────────────────────────────────────────────────────────────────────
# Report Parser
# ──────────────────────────────────────────────────────────────────────────────
def parse_scenario_report(report_dir: str) -> dict:
    """Parse a ScenarioReport.html and extract structured test result data."""
    html_path = os.path.join(report_dir, "ScenarioReport.html")
    result = {
        "report_dir": report_dir,
        "report_exists": False,
        "result": "UNKNOWN",
        "scenario_id": "",
        "description": "",
        "total_time": "00:00",
        "total_seconds": 0,
        "steps": [],
        "failure_message": "",
        "failure_details": "",
        "screenshot_count": 0,
        "screenshots": [],
    }

    if not os.path.isfile(html_path):
        result["result"] = "NO_REPORT"
        result["failure_message"] = "ScenarioReport.html not found"
        return result

    result["report_exists"] = True

    with open(html_path, "r", encoding="utf-8", errors="replace") as f:
        html = f.read()

    # Result: class="scenario-result PASS"
    m = re.search(r'scenario-result\s+(PASS|FAIL)', html)
    if m:
        result["result"] = m.group(1)

    # Scenario ID
    m = re.search(r'Scenario Id.*?class="value">([^<]+)', html, re.DOTALL)
    if m:
        result["scenario_id"] = m.group(1).strip()

    # Description
    m = re.search(r'class="description">([^<]+)', html)
    if m:
        result["description"] = m.group(1).strip()

    # Total time
    m = re.search(r'data-totaltime="([^"]+)"', html)
    if m:
        result["total_time"] = m.group(1)
        result["total_seconds"] = _time_str_to_seconds(m.group(1))

    # Steps with screenshots
    steps = re.findall(
        r'<img[^>]*class="(PASS|FAIL)"[^>]*src="([^"]*)"[^>]*data-time="([^"]*)"',
        html
    )
    for step_result, screenshot, step_time in steps:
        result["steps"].append({
            "result": step_result,
            "screenshot": screenshot,
            "time": step_time,
        })
    result["screenshot_count"] = len(steps)
    result["screenshots"] = [s["screenshot"] for s in result["steps"]]

    # Failure details (from step messages containing Failure)
    fail_msgs = re.findall(r'Failure[^<]{0,300}', html)
    if fail_msgs:
        # Deduplicate and take unique messages
        unique = list(dict.fromkeys(m.strip() for m in fail_msgs))
        result["failure_message"] = unique[0] if unique else ""
        result["failure_details"] = "\n".join(unique[:5])

    # If still no failure message, try extracting from step messages
    if result["result"] == "FAIL" and not result["failure_message"]:
        err_msgs = re.findall(r'Not able to[^<]{0,200}|Exception[^<]{0,200}', html)
        if err_msgs:
            result["failure_message"] = err_msgs[0].strip()
            result["failure_details"] = "\n".join(m.strip() for m in err_msgs[:5])

    return result


def _extract_epoch_ms(dirname: str) -> int:
    """Extract epoch millis from a report directory name like LOCAL_method_1773469921427."""
    m = re.search(r'_(\d{13})$', os.path.basename(dirname))
    return int(m.group(1)) if m else 0


def _batch_attempt_dirs(method: str, batch_window_start_ms: int) -> list:
    """Return only the report dirs for `method` that belong to the current batch.

    Strategy: find all dirs whose timestamp >= batch_window_start_ms, then
    take only the **latest cluster** — consecutive dirs where each pair is
    within SELF_HEAL_GAP_MS of each other (working backward from the newest).
    """
    all_dirs = sorted(glob.glob(os.path.join(REPORTS_DIR, f"LOCAL_{method}_*")))
    if not all_dirs:
        return []

    # Filter to dirs within batch window
    windowed = [(d, _extract_epoch_ms(d)) for d in all_dirs if _extract_epoch_ms(d) >= batch_window_start_ms]
    if not windowed:
        return all_dirs[-1:]  # fallback: just the latest

    # Cluster from the end: walk backward, include dir if gap < SELF_HEAL_GAP_MS
    windowed.sort(key=lambda x: x[1])
    cluster = [windowed[-1][0]]
    for i in range(len(windowed) - 2, -1, -1):
        if windowed[i + 1][1] - windowed[i][1] <= SELF_HEAL_GAP_MS:
            cluster.insert(0, windowed[i][0])
        else:
            break
    return cluster


def _time_str_to_seconds(time_str: str) -> int:
    """Convert MM:SS to total seconds."""
    parts = time_str.split(":")
    if len(parts) == 2:
        return int(parts[0]) * 60 + int(parts[1])
    elif len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
    return 0


# ──────────────────────────────────────────────────────────────────────────────
# Coverage Mapper
# ──────────────────────────────────────────────────────────────────────────────
def load_usecase_csv() -> list:
    """Load use-case CSV and return list of use-case dicts."""
    csv_files = glob.glob(os.path.join(TESTCASE_DIR, "*.csv"))
    usecases = []
    for csv_path in csv_files:
        if "batch_progress" in csv_path or "execution_plan" in csv_path:
            continue
        try:
            with open(csv_path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    uc_id = row.get("UseCase ID", "").strip()
                    if uc_id.startswith("SDPOD_") or uc_id.startswith("SDP_"):
                        usecases.append({
                            "id": uc_id,
                            "severity": row.get("Severity", "").strip(),
                            "module": row.get("Module", "").strip(),
                            "sub_module": row.get("Sub-Module", "").strip(),
                            "description": row.get("Description", "").strip()[:200],
                            "ui_automate": row.get("UI To-be-automated", "").strip(),
                            "api_automate": row.get("API To-be-automated", "").strip(),
                            "csv_file": os.path.basename(csv_path),
                        })
        except Exception:
            continue
    return usecases


def build_coverage_map(usecases: list, automated_ids: set) -> dict:
    """Map use-case IDs to automation status."""
    total_ui = sum(1 for uc in usecases if uc["ui_automate"].lower() == "yes")
    total_api = sum(1 for uc in usecases if uc["api_automate"].lower() == "yes")
    total = len(usecases)

    covered = 0
    not_covered = []
    severity_coverage = {"Critical": {"total": 0, "covered": 0},
                         "Major": {"total": 0, "covered": 0},
                         "Minor": {"total": 0, "covered": 0}}

    for uc in usecases:
        if uc["ui_automate"].lower() != "yes":
            continue
        sev = uc["severity"] if uc["severity"] in severity_coverage else "Minor"
        severity_coverage[sev]["total"] += 1

        if uc["id"] in automated_ids:
            covered += 1
            severity_coverage[sev]["covered"] += 1
        else:
            not_covered.append(uc)

    return {
        "total_usecases": total,
        "total_ui_automatable": total_ui,
        "total_api_automatable": total_api,
        "automated_count": covered,
        "not_covered": not_covered,
        "severity_coverage": severity_coverage,
        "coverage_pct": round((covered / total_ui * 100) if total_ui > 0 else 0, 1),
    }


# ──────────────────────────────────────────────────────────────────────────────
# Batch Results Collector
# ──────────────────────────────────────────────────────────────────────────────
def collect_batch_results(tests_json_path: str = None) -> dict:
    """Collect results for all tests in the batch manifest."""
    json_path = tests_json_path or TESTS_TO_RUN
    with open(json_path, "r") as f:
        manifest = json.load(f)

    tests = manifest.get("tests", [])
    results = []

    for test in tests:
        method = test["method_name"]
        test_ids = test.get("_id", "")

        # Find latest report directory for this method
        pattern = os.path.join(REPORTS_DIR, f"LOCAL_{method}_*")
        dirs = sorted(glob.glob(pattern))
        report_dir = dirs[-1] if dirs else ""

        if report_dir:
            parsed = parse_scenario_report(report_dir)
        else:
            parsed = {
                "report_dir": "",
                "report_exists": False,
                "result": "NOT_RUN",
                "scenario_id": test_ids,
                "description": "",
                "total_time": "00:00",
                "total_seconds": 0,
                "steps": [],
                "failure_message": "Test was not executed",
                "failure_details": "",
                "screenshot_count": 0,
                "screenshots": [],
            }

        # Override scenario_id from manifest if not found in report
        if not parsed["scenario_id"]:
            parsed["scenario_id"] = test_ids

        parsed["method_name"] = method
        parsed["entity_class"] = test.get("entity_class", "")
        parsed["test_ids"] = test_ids
        results.append(parsed)

    return {
        "manifest_comment": manifest.get("_comment", ""),
        "test_count": len(tests),
        "results": results,
    }


# ──────────────────────────────────────────────────────────────────────────────
# Timing & Effort Calculator
# ──────────────────────────────────────────────────────────────────────────────
def calculate_effort(results: list, coverage: dict) -> dict:
    """Calculate time savings and effort metrics."""
    total_automation_seconds = sum(r["total_seconds"] for r in results)
    total_tests = len(results)
    passed = sum(1 for r in results if r["result"] == "PASS")
    failed = sum(1 for r in results if r["result"] == "FAIL")
    not_run = sum(1 for r in results if r["result"] in ("NOT_RUN", "NO_REPORT", "UNKNOWN"))

    # Manual equivalent time
    manual_execution_minutes = total_tests * MANUAL_TEST_AVG_MINUTES
    manual_authoring_minutes = total_tests * MANUAL_AUTHORING_AVG_MINUTES

    # Automation execution time
    automation_minutes = total_automation_seconds / 60

    # Time saved per execution cycle
    time_saved_per_cycle = manual_execution_minutes - automation_minutes

    # ROI: if you run the suite N times, break-even point for authoring investment
    if time_saved_per_cycle > 0:
        cycles_to_roi = manual_authoring_minutes / time_saved_per_cycle
    else:
        cycles_to_roi = float("inf")

    return {
        "total_tests": total_tests,
        "passed": passed,
        "failed": failed,
        "not_run": not_run,
        "pass_rate": round((passed / total_tests * 100) if total_tests > 0 else 0, 1),
        "total_automation_seconds": total_automation_seconds,
        "total_automation_time": _seconds_to_display(total_automation_seconds),
        "manual_execution_time": f"{manual_execution_minutes} min ({manual_execution_minutes // 60}h {manual_execution_minutes % 60}m)",
        "manual_authoring_time": f"{manual_authoring_minutes} min ({manual_authoring_minutes // 60}h {manual_authoring_minutes % 60}m)",
        "time_saved_per_cycle": f"{time_saved_per_cycle:.0f} min",
        "time_saved_pct": round((time_saved_per_cycle / manual_execution_minutes * 100) if manual_execution_minutes > 0 else 0, 1),
        "cycles_to_roi": f"{cycles_to_roi:.1f}" if cycles_to_roi != float("inf") else "N/A",
        "automation_coverage_pct": coverage["coverage_pct"],
    }


def _seconds_to_display(seconds: int) -> str:
    """Convert seconds to human-readable display."""
    if seconds < 60:
        return f"{seconds}s"
    minutes = seconds // 60
    secs = seconds % 60
    if minutes < 60:
        return f"{minutes}m {secs}s"
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours}h {mins}m {secs}s"


# ──────────────────────────────────────────────────────────────────────────────
# Markdown Generator
# ──────────────────────────────────────────────────────────────────────────────
def generate_markdown(batch: dict, coverage: dict, effort: dict) -> str:
    """Generate the full interactive Markdown summary."""
    now = datetime.now()
    results = batch["results"]

    # Use pre-computed batch window
    batch_window_start_ms = batch.get("batch_window_start_ms", 0)
    if batch_window_start_ms == 0:
        # Fallback: compute here
        latest_timestamps = []
        for r in results:
            dirs = sorted(glob.glob(os.path.join(REPORTS_DIR, f"LOCAL_{r['method_name']}_*")))
            if dirs:
                latest_timestamps.append(_extract_epoch_ms(dirs[-1]))
        batch_window_start_ms = min(latest_timestamps) - SELF_HEAL_GAP_MS if latest_timestamps else 0

    # ── Header ──
    md = []
    md.append(f"# 🏁 Batch Execution Summary")
    md.append(f"")
    md.append(f"> **Project**: `{PROJECT_NAME}`  ")
    md.append(f"> **Generated**: {now.strftime('%B %d, %Y at %I:%M %p')}  ")
    md.append(f"> **Batch**: {batch['manifest_comment']}")
    md.append(f"")

    # ── Executive Dashboard ──
    md.append(f"---")
    md.append(f"")
    md.append(f"## 📊 Executive Dashboard")
    md.append(f"")
    md.append(f"| Metric | Value |")
    md.append(f"|--------|-------|")
    md.append(f"| **Tests Planned** | {effort['total_tests']} |")
    md.append(f"| **Passed** | ✅ {effort['passed']} |")
    md.append(f"| **Failed** | ❌ {effort['failed']} |")
    md.append(f"| **Not Run** | ⏭️ {effort['not_run']} |")
    md.append(f"| **Pass Rate** | **{effort['pass_rate']}%** |")
    md.append(f"| **Total Execution Time** | {effort['total_automation_time']} |")
    md.append(f"| **Automation Coverage** | {effort['automation_coverage_pct']}% of UI-automatable cases |")
    md.append(f"")

    # Pass rate visual bar
    filled = int(effort["pass_rate"] / 5)
    empty = 20 - filled
    bar = "█" * filled + "░" * empty
    md.append(f"**Pass Rate**: `{bar}` {effort['pass_rate']}%")
    md.append(f"")

    # ── Detailed Test Results ──
    md.append(f"---")
    md.append(f"")
    md.append(f"## 📋 Detailed Test Results")
    md.append(f"")
    md.append(f"| # | UseCase ID | Method | Result | Time | Attempts |")
    md.append(f"|---|-----------|--------|--------|------|----------|")

    for i, r in enumerate(results, 1):
        icon = "✅" if r["result"] == "PASS" else "❌" if r["result"] == "FAIL" else "⏭️"
        # Count attempts — only dirs in the current batch window
        method = r["method_name"]
        attempt_dirs = _batch_attempt_dirs(method, batch_window_start_ms)
        attempts = len(attempt_dirs)
        attempt_str = f"{attempts}" if attempts <= 1 else f"**{attempts}** (self-healed)" if r["result"] == "PASS" else f"**{attempts}**"

        uc_id = r["test_ids"]
        if len(uc_id) > 30:
            uc_id = uc_id[:27] + "..."

        md.append(f"| {i} | `{uc_id}` | `{method}` | {icon} {r['result']} | {r['total_time']} | {attempt_str} |")

    md.append(f"")

    # ── Self-Healing Summary ──
    healed_tests = []
    for r in results:
        method = r["method_name"]
        attempt_dirs = _batch_attempt_dirs(method, batch_window_start_ms)
        if len(attempt_dirs) > 1 and r["result"] == "PASS":
            healed_tests.append((r, len(attempt_dirs)))

    if healed_tests:
        md.append(f"---")
        md.append(f"")
        md.append(f"## 🔧 Self-Healing Summary")
        md.append(f"")
        md.append(f"The following tests **failed initially but were automatically fixed and re-run**:")
        md.append(f"")
        for r, attempts in healed_tests:
            md.append(f"- **`{r['method_name']}`** — {attempts} attempts → ✅ PASS")
            # Try to find what changed between attempts
            heal_dirs = _batch_attempt_dirs(r['method_name'], batch_window_start_ms)
            if len(heal_dirs) >= 2:
                first_report = parse_scenario_report(heal_dirs[0])
                if first_report.get("failure_message"):
                    md.append(f"  - Initial failure: _{first_report['failure_message'][:150]}_")
        md.append(f"")

    # ── Bug Analysis (Failed Tests) ──
    failed_tests = [r for r in results if r["result"] == "FAIL"]
    if failed_tests:
        md.append(f"---")
        md.append(f"")
        md.append(f"## 🐛 Bug Analysis — Tests Requiring Investigation")
        md.append(f"")
        md.append(f"The following {len(failed_tests)} test(s) failed after all retry attempts.")
        md.append(f"Each needs manual analysis to determine if it's a **product bug**, **environment issue**, or **test gap**.")
        md.append(f"")

        for i, r in enumerate(failed_tests, 1):
            md.append(f"### {i}. `{r['method_name']}`")
            md.append(f"")
            md.append(f"| Field | Value |")
            md.append(f"|-------|-------|")
            md.append(f"| **UseCase ID** | `{r['test_ids']}` |")
            md.append(f"| **Scenario ID** | `{r['scenario_id']}` |")
            md.append(f"| **Description** | {r['description']} |")
            md.append(f"| **Result** | ❌ FAIL |")
            md.append(f"| **Execution Time** | {r['total_time']} |")
            md.append(f"| **Screenshots** | {r['screenshot_count']} captured |")
            md.append(f"")

            if r["failure_message"]:
                md.append(f"**Failure Message:**")
                md.append(f"```")
                md.append(f"{r['failure_message'][:500]}")
                md.append(f"```")
                md.append(f"")

            if r["failure_details"] and r["failure_details"] != r["failure_message"]:
                md.append(f"<details>")
                md.append(f"<summary>Full Failure Details</summary>")
                md.append(f"")
                md.append(f"```")
                md.append(f"{r['failure_details'][:1000]}")
                md.append(f"```")
                md.append(f"</details>")
                md.append(f"")

            # Steps to reproduce
            if r["steps"]:
                md.append(f"**Steps (from execution log):**")
                md.append(f"")
                for j, step in enumerate(r["steps"], 1):
                    step_icon = "✅" if step["result"] == "PASS" else "❌"
                    md.append(f"{j}. {step_icon} Step at `{step['time']}` — [{step['screenshot']}]({r['report_dir']}/{step['screenshot']})")
                md.append(f"")

            if r["report_exists"]:
                md.append(f"📄 [Open Full Report]({r['report_dir']}/ScenarioReport.html)")
                md.append(f"")

    # ── Coverage Analysis ──
    md.append(f"---")
    md.append(f"")
    md.append(f"## 📈 Automation Coverage vs Use-Case Document")
    md.append(f"")

    if coverage["total_usecases"] > 0:
        md.append(f"| Metric | Count |")
        md.append(f"|--------|-------|")
        md.append(f"| **Total Use Cases in Document** | {coverage['total_usecases']} |")
        md.append(f"| **UI Automatable** | {coverage['total_ui_automatable']} |")
        md.append(f"| **API Automatable** | {coverage['total_api_automatable']} |")
        md.append(f"| **Automated in This Batch** | {coverage['automated_count']} |")
        md.append(f"| **Coverage %** | **{coverage['coverage_pct']}%** |")
        md.append(f"")

        # Coverage bar
        cov_filled = int(coverage["coverage_pct"] / 5)
        cov_empty = 20 - cov_filled
        cov_bar = "█" * cov_filled + "░" * cov_empty
        md.append(f"**Coverage**: `{cov_bar}` {coverage['coverage_pct']}%")
        md.append(f"")

        # Severity breakdown
        md.append(f"### Coverage by Severity")
        md.append(f"")
        md.append(f"| Severity | Automatable | Covered | % |")
        md.append(f"|----------|------------|---------|---|")
        for sev in ["Critical", "Major", "Minor"]:
            s = coverage["severity_coverage"][sev]
            pct = round((s["covered"] / s["total"] * 100) if s["total"] > 0 else 0, 1)
            md.append(f"| {sev} | {s['total']} | {s['covered']} | {pct}% |")
        md.append(f"")

        # Not yet covered
        not_covered = coverage["not_covered"]
        if not_covered:
            md.append(f"### Use Cases Not Yet Automated ({len(not_covered)} remaining)")
            md.append(f"")
            md.append(f"<details>")
            md.append(f"<summary>Click to expand ({len(not_covered)} use cases)</summary>")
            md.append(f"")
            md.append(f"| UseCase ID | Severity | Sub-Module | Description |")
            md.append(f"|-----------|----------|-----------|-------------|")
            for uc in not_covered[:100]:  # Cap at 100 rows
                desc = uc["description"][:80] + "..." if len(uc["description"]) > 80 else uc["description"]
                # Escape pipes in description
                desc = desc.replace("|", "\\|")
                md.append(f"| `{uc['id']}` | {uc['severity']} | {uc['sub_module']} | {desc} |")
            if len(not_covered) > 100:
                md.append(f"| ... | ... | ... | _({len(not_covered) - 100} more)_ |")
            md.append(f"")
            md.append(f"</details>")
            md.append(f"")
    else:
        md.append(f"_No use-case document found in `{TESTCASE_DIR}/`._")
        md.append(f"")

    # ── Time & Effort Savings ──
    md.append(f"---")
    md.append(f"")
    md.append(f"## ⏱️ Time & Effort Analysis")
    md.append(f"")
    md.append(f"| Metric | Value |")
    md.append(f"|--------|-------|")
    md.append(f"| **Automation Execution Time** | {effort['total_automation_time']} |")
    md.append(f"| **Manual Equivalent (execution)** | {effort['manual_execution_time']} |")
    md.append(f"| **Time Saved Per Run** | 🚀 **{effort['time_saved_per_cycle']}** ({effort['time_saved_pct']}% faster) |")
    md.append(f"| **Manual Test Authoring Equivalent** | {effort['manual_authoring_time']} |")
    md.append(f"| **Break-Even (runs to ROI)** | {effort['cycles_to_roi']} execution cycles |")
    md.append(f"")

    md.append(f"> **💡 Key Insight**: Each automated batch run saves approximately **{effort['time_saved_per_cycle']}** ")
    md.append(f"> compared to manual testing. After **{effort['cycles_to_roi']} runs**, the automation ")
    md.append(f"> investment pays for itself — every subsequent run is pure time savings.")
    md.append(f"")

    # Manual effort breakdown visualization
    md.append(f"### Cost Comparison")
    md.append(f"")
    md.append(f"```")
    md.append(f"Manual Testing:  {_bar_chart(100, 40)}")
    md.append(f"Automated Run:   {_bar_chart(int(100 - effort['time_saved_pct']), 40)}")
    md.append(f"                 {'─' * 42}")
    md.append(f"                 0%               50%              100%")
    md.append(f"```")
    md.append(f"")

    # ── Run History (all attempts per test) ──
    md.append(f"---")
    md.append(f"")
    md.append(f"## 📁 Run History")
    md.append(f"")
    md.append(f"<details>")
    md.append(f"<summary>Batch run directories ({_count_batch_dirs(results, batch_window_start_ms)} runs in this batch)</summary>")
    md.append(f"")
    for r in results:
        method = r["method_name"]
        dirs = _batch_attempt_dirs(method, batch_window_start_ms)
        if dirs:
            md.append(f"**`{method}`** ({len(dirs)} run{'s' if len(dirs) > 1 else ''}):")
            for d in dirs:
                ts_match = re.search(r'_(\d{13})/?$', d)
                if ts_match:
                    ts = int(ts_match.group(1))
                    dt = datetime.fromtimestamp(ts / 1000)
                    time_str = dt.strftime("%I:%M:%S %p")
                else:
                    time_str = "?"
                p = parse_scenario_report(d)
                icon = "✅" if p["result"] == "PASS" else "❌" if p["result"] == "FAIL" else "⚠️"
                md.append(f"  - {icon} `{os.path.basename(d)}` — {time_str}")
    md.append(f"")
    md.append(f"</details>")
    md.append(f"")

    # ── Footer ──
    md.append(f"---")
    md.append(f"")
    md.append(f"<sub>Generated by **AutomaterSelenium AI Test Runner** • "
              f"{now.strftime('%Y-%m-%d %H:%M:%S')} • "
              f"Project: {PROJECT_NAME}</sub>")

    return "\n".join(md)


def _bar_chart(pct: int, width: int) -> str:
    """Generate a text-based bar chart."""
    pct = max(0, min(100, pct))
    filled = int(pct / 100 * width)
    return "█" * filled + "░" * (width - filled) + f" {pct}%"


def _count_batch_dirs(results: list, batch_window_start_ms: int) -> int:
    """Count total report directories in the batch window across all methods."""
    count = 0
    for r in results:
        count += len(_batch_attempt_dirs(r["method_name"], batch_window_start_ms))
    return count


# ──────────────────────────────────────────────────────────────────────────────
# Main
# ──────────────────────────────────────────────────────────────────────────────
def main():
    print(f"{'=' * 60}")
    print(f"  AutomaterSelenium — Batch Summary Generator")
    print(f"  Project: {PROJECT_NAME}")
    print(f"{'=' * 60}")

    # 1. Collect batch results
    print("\n📥 Collecting batch results from reports...")
    batch = collect_batch_results()
    print(f"   Found {batch['test_count']} tests in manifest")

    passed = sum(1 for r in batch["results"] if r["result"] == "PASS")
    failed = sum(1 for r in batch["results"] if r["result"] == "FAIL")
    not_run = batch["test_count"] - passed - failed
    print(f"   Results: ✅ {passed} passed, ❌ {failed} failed, ⏭️ {not_run} not run")

    # 2. Load use-case document
    print("\n📄 Loading use-case document...")
    usecases = load_usecase_csv()
    print(f"   Found {len(usecases)} use cases")

    # 3. Build coverage map
    automated_ids = set()
    for r in batch["results"]:
        # Split comma-separated IDs
        for uid in r["test_ids"].split(","):
            uid = uid.strip()
            if uid:
                automated_ids.add(uid)

    coverage = build_coverage_map(usecases, automated_ids)
    print(f"   Coverage: {coverage['automated_count']}/{coverage['total_ui_automatable']} UI cases = {coverage['coverage_pct']}%")

    # 4. Calculate effort
    effort = calculate_effort(batch["results"], coverage)

    # 4b. Compute batch window start (earliest "latest report" minus buffer)
    latest_timestamps = []
    for r in batch["results"]:
        dirs = sorted(glob.glob(os.path.join(REPORTS_DIR, f"LOCAL_{r['method_name']}_*")))
        if dirs:
            latest_timestamps.append(_extract_epoch_ms(dirs[-1]))
    batch_window_start_ms = min(latest_timestamps) - SELF_HEAL_GAP_MS if latest_timestamps else 0
    batch["batch_window_start_ms"] = batch_window_start_ms

    # 5. Generate Markdown
    print("\n📝 Generating summary report...")
    markdown = generate_markdown(batch, coverage, effort)

    # 6. Write to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(AI_REPORTS_DIR, exist_ok=True)
    output_path = os.path.join(AI_REPORTS_DIR, f"BATCH_SUMMARY_{timestamp}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"\n✅ Summary saved to: {output_path}")
    print(f"   File size: {os.path.getsize(output_path):,} bytes")

    # Also save a JSON snapshot for programmatic access
    json_path = os.path.join(AI_REPORTS_DIR, f"BATCH_SUMMARY_{timestamp}.json")
    summary_data = {
        "generated_at": datetime.now().isoformat(),
        "project": PROJECT_NAME,
        "effort": effort,
        "coverage": {k: v for k, v in coverage.items() if k != "not_covered"},
        "results": [
            {
                "method": r["method_name"],
                "test_ids": r["test_ids"],
                "result": r["result"],
                "time": r["total_time"],
                "failure": r["failure_message"][:200] if r["failure_message"] else "",
                "attempts": len(_batch_attempt_dirs(r["method_name"], batch_window_start_ms)),
            }
            for r in batch["results"]
        ],
    }
    with open(json_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    print(f"   JSON snapshot: {json_path}")

    print(f"\n{'=' * 60}")
    print(f"  Pass Rate: {effort['pass_rate']}% | Coverage: {coverage['coverage_pct']}%")
    print(f"  Time Saved: {effort['time_saved_per_cycle']} per run")
    print(f"{'=' * 60}")

    return output_path


# ──────────────────────────────────────────────────────────────────────────────
# Generation Mode — post-generation summary (no execution data needed)
# ──────────────────────────────────────────────────────────────────────────────
def generate_generation_markdown(batch: dict, coverage: dict, gen_effort: dict) -> str:
    """Generate Markdown summary for test generation (not execution)."""
    now = datetime.now()
    tests = batch.get("results", []) or batch.get("tests", [])

    md = []
    md.append("# 🧪 Test Generation Summary")
    md.append("")
    md.append(f"> **Project**: `{PROJECT_NAME}`  ")
    md.append(f"> **Generated**: {now.strftime('%B %d, %Y at %I:%M %p')}  ")
    md.append(f"> **Batch**: {batch.get('manifest_comment', 'N/A')}")
    md.append("")

    # ── Dashboard ──
    md.append("---")
    md.append("")
    md.append("## 📊 Generation Dashboard")
    md.append("")
    md.append("| Metric | Value |")
    md.append("|--------|-------|")
    md.append(f"| **Scenarios Generated** | {gen_effort['total_scenarios']} |")
    md.append(f"| **Unique Use Cases Covered** | {gen_effort['unique_usecase_ids']} |")
    md.append(f"| **Entity Classes** | {gen_effort['entity_classes']} |")
    if gen_effort['generation_time']:
        md.append(f"| **Generation Time** | {gen_effort['generation_time']} |")
    md.append(f"| **Manual Authoring Equivalent** | {gen_effort['manual_authoring_time']} |")
    if gen_effort['time_saved']:
        md.append(f"| **Time Saved** | 🚀 **{gen_effort['time_saved']}** |")
    md.append(f"| **Automation Coverage** | {coverage['coverage_pct']}% of UI-automatable cases |")
    md.append("")

    # Coverage bar
    cov_filled = int(coverage["coverage_pct"] / 5)
    cov_empty = 20 - cov_filled
    cov_bar = "█" * cov_filled + "░" * cov_empty
    md.append(f"**Coverage**: `{cov_bar}` {coverage['coverage_pct']}%")
    md.append("")

    # ── Generated Scenarios Table ──
    md.append("---")
    md.append("")
    md.append("## 📋 Generated Scenarios")
    md.append("")
    md.append("| # | UseCase ID | Entity | Method |")
    md.append("|---|-----------|--------|--------|")

    for i, t in enumerate(tests, 1):
        uc_id = t.get("test_ids", t.get("_id", ""))
        entity = t.get("entity_class", "")
        method = t.get("method_name", "")
        if len(uc_id) > 35:
            uc_id = uc_id[:32] + "..."
        md.append(f"| {i} | `{uc_id}` | `{entity}` | `{method}` |")
    md.append("")

    # ── Coverage Analysis ──
    if coverage["total_usecases"] > 0:
        md.append("---")
        md.append("")
        md.append("## 📈 Coverage vs Use-Case Document")
        md.append("")
        md.append("| Metric | Count |")
        md.append("|--------|-------|")
        md.append(f"| **Total Use Cases** | {coverage['total_usecases']} |")
        md.append(f"| **UI Automatable** | {coverage['total_ui_automatable']} |")
        md.append(f"| **Covered by This Batch** | {coverage['automated_count']} |")
        md.append(f"| **Remaining** | {coverage['total_ui_automatable'] - coverage['automated_count']} |")
        md.append(f"| **Coverage** | **{coverage['coverage_pct']}%** |")
        md.append("")

        # Severity breakdown
        md.append("### Coverage by Severity")
        md.append("")
        md.append("| Severity | Total | Covered | % |")
        md.append("|----------|-------|---------|---|")
        for sev in ["Critical", "Major", "Minor"]:
            s = coverage["severity_coverage"][sev]
            pct = round((s["covered"] / s["total"] * 100) if s["total"] > 0 else 0, 1)
            md.append(f"| {sev} | {s['total']} | {s['covered']} | {pct}% |")
        md.append("")

        remaining = coverage['total_ui_automatable'] - coverage['automated_count']
        if remaining > 0:
            md.append(f"> **Next batch**: {remaining} UI-automatable use cases remaining. ")
            md.append(f"> Run `@test-generator` again with the same CSV to generate the next batch.")
            md.append("")

    # ── Time & Effort ──
    md.append("---")
    md.append("")
    md.append("## ⏱️ Effort Analysis")
    md.append("")
    md.append("| Metric | Value |")
    md.append("|--------|-------|")
    if gen_effort['generation_time']:
        md.append(f"| **AI Generation Time** | {gen_effort['generation_time']} |")
    md.append(f"| **Manual Authoring Equivalent** | {gen_effort['manual_authoring_time']} |")
    if gen_effort['time_saved']:
        md.append(f"| **Time Saved** | 🚀 **{gen_effort['time_saved']}** |")
        md.append(f"| **Speed-up Factor** | **{gen_effort['speedup_factor']}** |")
    md.append(f"| **Manual Execution Time (per run)** | {gen_effort['manual_execution_time']} |")
    md.append("")

    if gen_effort['time_saved']:
        md.append(f"> **💡 Key Insight**: AI generated {gen_effort['total_scenarios']} test scenarios ")
        md.append(f"> in {gen_effort['generation_time']}, saving **{gen_effort['time_saved']}** ")
        md.append(f"> compared to manual authoring ({gen_effort['speedup_factor']} faster).")
    else:
        md.append(f"> **💡 Key Insight**: Manual authoring of {gen_effort['total_scenarios']} test scenarios ")
        md.append(f"> would take approximately **{gen_effort['manual_authoring_time']}**.")
    md.append("")

    # ── Next Steps ──
    md.append("---")
    md.append("")
    md.append("## 🚀 Next Steps")
    md.append("")
    md.append(f"1. **Run the batch**: `@test-runner batch`")
    md.append(f"2. **Review execution summary**: `generate_batch_summary.py` (auto-runs after batch)")
    remaining = coverage['total_ui_automatable'] - coverage['automated_count']
    if remaining > 0:
        md.append(f"3. **Generate next batch**: {remaining} use cases remaining — re-run `@test-generator`")
    md.append("")

    # ── Footer ──
    md.append("---")
    md.append("")
    md.append(f"<sub>Generated by **AutomaterSelenium AI Test Generator** • "
              f"{now.strftime('%Y-%m-%d %H:%M:%S')} • "
              f"Project: {PROJECT_NAME}</sub>")

    return "\n".join(md)


def calculate_generation_effort(tests: list, coverage: dict, start_epoch: float = None) -> dict:
    """Calculate effort metrics for test generation."""
    total_scenarios = len(tests)
    unique_ids = set()
    entity_classes = set()
    for t in tests:
        for uid in t.get("_id", "").split(","):
            uid = uid.strip()
            if uid:
                unique_ids.add(uid)
        entity_classes.add(t.get("entity_class", "Unknown"))

    manual_authoring_minutes = total_scenarios * MANUAL_AUTHORING_AVG_MINUTES
    manual_execution_minutes = total_scenarios * MANUAL_TEST_AVG_MINUTES

    generation_time = None
    time_saved = None
    speedup_factor = None
    if start_epoch:
        elapsed_seconds = datetime.now().timestamp() - start_epoch
        elapsed_minutes = elapsed_seconds / 60
        generation_time = _seconds_to_display(int(elapsed_seconds))
        saved_minutes = manual_authoring_minutes - elapsed_minutes
        if saved_minutes > 0:
            time_saved = f"{saved_minutes:.0f} min ({saved_minutes / 60:.1f}h)"
            speedup_factor = f"{manual_authoring_minutes / elapsed_minutes:.1f}x" if elapsed_minutes > 0 else "N/A"

    return {
        "total_scenarios": total_scenarios,
        "unique_usecase_ids": len(unique_ids),
        "entity_classes": len(entity_classes),
        "generation_time": generation_time,
        "manual_authoring_time": f"{manual_authoring_minutes} min ({manual_authoring_minutes // 60}h {manual_authoring_minutes % 60}m)",
        "manual_execution_time": f"{manual_execution_minutes} min ({manual_execution_minutes // 60}h {manual_execution_minutes % 60}m)",
        "time_saved": time_saved,
        "speedup_factor": speedup_factor,
    }


def main_generate(start_epoch: float = None):
    """Generate a post-generation summary (no execution data needed)."""
    print(f"{'=' * 60}")
    print(f"  AutomaterSelenium — Generation Summary")
    print(f"  Project: {PROJECT_NAME}")
    print(f"{'=' * 60}")

    # 1. Load test manifest
    print("\n📥 Loading test manifest...")
    with open(TESTS_TO_RUN, "r") as f:
        manifest = json.load(f)
    tests = manifest.get("tests", [])
    comment = manifest.get("_comment", "")
    print(f"   Found {len(tests)} scenarios")

    # 2. Load use-case document
    print("\n📄 Loading use-case document...")
    usecases = load_usecase_csv()
    print(f"   Found {len(usecases)} use cases")

    # 3. Build coverage map
    automated_ids = set()
    for t in tests:
        for uid in t.get("_id", "").split(","):
            uid = uid.strip()
            if uid:
                automated_ids.add(uid)
    coverage = build_coverage_map(usecases, automated_ids)
    print(f"   Coverage: {coverage['automated_count']}/{coverage['total_ui_automatable']} UI cases = {coverage['coverage_pct']}%")

    # 4. Calculate generation effort
    gen_effort = calculate_generation_effort(tests, coverage, start_epoch)

    # 5. Generate Markdown
    print("\n📝 Generating generation summary...")
    batch = {
        "manifest_comment": comment,
        "test_count": len(tests),
        "tests": tests,
    }
    markdown = generate_generation_markdown(batch, coverage, gen_effort)

    # 6. Write to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(AI_REPORTS_DIR, f"GENERATION_SUMMARY_{timestamp}.md")
    os.makedirs(AI_REPORTS_DIR, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"\n✅ Summary saved to: {output_path}")
    print(f"   File size: {os.path.getsize(output_path):,} bytes")

    # JSON snapshot
    json_path = os.path.join(AI_REPORTS_DIR, f"GENERATION_SUMMARY_{timestamp}.json")
    summary_data = {
        "generated_at": datetime.now().isoformat(),
        "mode": "generate",
        "project": PROJECT_NAME,
        "generation_effort": gen_effort,
        "coverage": {k: v for k, v in coverage.items() if k != "not_covered"},
        "scenarios": [
            {"method": t["method_name"], "entity": t.get("entity_class", ""), "ids": t.get("_id", "")}
            for t in tests
        ],
    }
    with open(json_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    print(f"   JSON snapshot: {json_path}")

    print(f"\n{'=' * 60}")
    print(f"  Scenarios: {gen_effort['total_scenarios']} | Coverage: {coverage['coverage_pct']}%")
    if gen_effort['generation_time']:
        print(f"  Generation Time: {gen_effort['generation_time']} | Saved: {gen_effort['time_saved']}")
    print(f"{'=' * 60}")

    return output_path


# ──────────────────────────────────────────────────────────────────────────────
# Use-Case Analysis Mode — requirement analysis with batch segregation
# ──────────────────────────────────────────────────────────────────────────────

def _batch_size_label(count: int) -> str:
    """Return a complexity label for a batch based on case count."""
    if count <= 10:
        return "Small"
    elif count <= 25:
        return "Medium"
    else:
        return "Large"


def build_usecase_analysis(usecases: list, automated_ids: set) -> dict:
    """Build comprehensive analysis of use-case inventory."""
    from collections import Counter, defaultdict

    total = len(usecases)
    ui_yes = [uc for uc in usecases if uc["ui_automate"].lower() == "yes"]
    ui_no = [uc for uc in usecases if uc["ui_automate"].lower() == "no"]
    api_yes = [uc for uc in usecases if uc["api_automate"].lower() == "yes"]
    api_no = [uc for uc in usecases if uc["api_automate"].lower() != "yes"]

    # Severity breakdown (over all valid IDs)
    severity_all = Counter(uc["severity"] for uc in usecases if uc["severity"])
    severity_ui = Counter(uc["severity"] for uc in ui_yes if uc["severity"])

    # Module / Sub-Module breakdown (UI-automatable only)
    module_counts = Counter(uc["module"] for uc in ui_yes if uc["module"])
    submodule_counts = Counter(uc["sub_module"] for uc in ui_yes if uc["sub_module"])

    # Automation progress — which UI=Yes cases are already generated
    ui_generated = [uc for uc in ui_yes if uc["id"] in automated_ids]
    ui_pending = [uc for uc in ui_yes if uc["id"] not in automated_ids]

    # Group pending by sub-module for batch segregation
    pending_by_submodule = defaultdict(list)
    for uc in ui_pending:
        key = uc["sub_module"] if uc["sub_module"] else "(No Sub-Module)"
        pending_by_submodule[key].append(uc)

    # Build batch plan — group sub-modules into right-sized batches
    batches = []
    current_batch = {"sub_modules": [], "cases": [], "count": 0}
    # Sort sub-modules: Critical-heavy first, then by count desc
    def _submod_priority(item):
        submod, cases = item
        critical = sum(1 for c in cases if c["severity"] == "Critical")
        return (-critical, -len(cases), submod)

    for submod, cases in sorted(pending_by_submodule.items(), key=_submod_priority):
        # Start new batch if adding this sub-module would exceed 30
        if current_batch["count"] > 0 and current_batch["count"] + len(cases) > 30:
            batches.append(current_batch)
            current_batch = {"sub_modules": [], "cases": [], "count": 0}
        current_batch["sub_modules"].append(submod)
        current_batch["cases"].extend(cases)
        current_batch["count"] += len(cases)

    if current_batch["count"] > 0:
        batches.append(current_batch)

    # Severity breakdown of generated vs pending
    sev_progress = {}
    for sev in ["Critical", "Major", "Minor"]:
        sev_total = sum(1 for uc in ui_yes if uc["severity"] == sev)
        sev_done = sum(1 for uc in ui_generated if uc["severity"] == sev)
        sev_progress[sev] = {"total": sev_total, "generated": sev_done,
                             "pending": sev_total - sev_done}

    # CSV file breakdown
    csv_files = Counter(uc["csv_file"] for uc in usecases)

    return {
        "total_usecases": total,
        "ui_yes_count": len(ui_yes),
        "ui_no_count": len(ui_no),
        "api_yes_count": len(api_yes),
        "api_no_count": len(api_no),
        "severity_all": dict(severity_all),
        "severity_ui": dict(severity_ui),
        "module_counts": dict(module_counts),
        "submodule_counts": dict(submodule_counts),
        "generated_count": len(ui_generated),
        "pending_count": len(ui_pending),
        "generated_ids": sorted(uc["id"] for uc in ui_generated),
        "pending_by_submodule": {k: v for k, v in pending_by_submodule.items()},
        "batches": batches,
        "sev_progress": sev_progress,
        "csv_files": dict(csv_files),
    }


def generate_usecase_analysis_markdown(analysis: dict) -> str:
    """Generate Markdown report for use-case requirement analysis."""
    now = datetime.now()

    md = []
    md.append("# 📋 Use-Case Requirement Analysis")
    md.append("")
    md.append(f"> **Project**: `{PROJECT_NAME}`  ")
    md.append(f"> **Generated**: {now.strftime('%B %d, %Y at %H:%M')}  ")
    md.append(f"> **Source**: `$PROJECT_NAME/Testcase/*.csv`")
    md.append("")

    # ── 1. Executive Summary ──
    md.append("---")
    md.append("## 1. Executive Summary")
    md.append("")
    total = analysis["total_usecases"]
    ui_yes = analysis["ui_yes_count"]
    generated = analysis["generated_count"]
    pending = analysis["pending_count"]
    pct_done = round(generated / ui_yes * 100, 1) if ui_yes > 0 else 0
    pct_remaining = round(pending / ui_yes * 100, 1) if ui_yes > 0 else 0

    md.append(f"| Metric | Count |")
    md.append(f"|--------|-------|")
    md.append(f"| Total Use Cases (valid IDs) | **{total}** |")
    md.append(f"| UI To-be-automated = Yes | **{ui_yes}** |")
    md.append(f"| UI To-be-automated = No | {analysis['ui_no_count']} |")
    md.append(f"| API To-be-automated = Yes | {analysis['api_yes_count']} |")
    md.append(f"| Already Generated (in manifest) | **{generated}** ({pct_done}%) |")
    md.append(f"| Pending Generation | **{pending}** ({pct_remaining}%) |")
    md.append("")

    # Progress bar
    bar_len = 30
    filled = round(bar_len * pct_done / 100) if pct_done > 0 else 0
    bar = "█" * filled + "░" * (bar_len - filled)
    md.append(f"**Automation Progress**: `[{bar}]` {pct_done}%")
    md.append("")

    # ── 2. Severity Analysis ──
    md.append("---")
    md.append("## 2. Severity Distribution (UI-Automatable)")
    md.append("")
    md.append("| Severity | Total | Generated | Pending | Progress |")
    md.append("|----------|-------|-----------|---------|----------|")
    for sev in ["Critical", "Major", "Minor"]:
        sp = analysis["sev_progress"].get(sev, {"total": 0, "generated": 0, "pending": 0})
        sev_pct = round(sp["generated"] / sp["total"] * 100) if sp["total"] > 0 else 0
        icon = "🔴" if sev == "Critical" else ("🟡" if sev == "Major" else "🟢")
        md.append(f"| {icon} {sev} | {sp['total']} | {sp['generated']} | {sp['pending']} | {sev_pct}% |")
    md.append("")

    # ── 3. Module / Sub-Module Breakdown ──
    md.append("---")
    md.append("## 3. Module & Sub-Module Breakdown (UI-Automatable)")
    md.append("")
    if analysis["module_counts"]:
        md.append("### By Module")
        md.append("| Module | UI Cases |")
        md.append("|--------|----------|")
        for mod, cnt in sorted(analysis["module_counts"].items(), key=lambda x: -x[1]):
            md.append(f"| {mod} | {cnt} |")
        md.append("")

    if analysis["submodule_counts"]:
        md.append("### By Sub-Module (Top 20)")
        md.append("| Sub-Module | UI Cases |")
        md.append("|------------|----------|")
        top_subs = sorted(analysis["submodule_counts"].items(), key=lambda x: -x[1])[:20]
        for sub, cnt in top_subs:
            md.append(f"| {sub} | {cnt} |")
        md.append("")

    # ── 4. Already Automated ──
    md.append("---")
    md.append("## 4. Already Automated (Generated & In Manifest)")
    md.append("")
    gen_ids = analysis["generated_ids"]
    if gen_ids:
        md.append(f"**{len(gen_ids)} use cases** already have automation scripts generated:")
        md.append("")
        # Group by prefix pattern
        for uc_id in gen_ids:
            md.append(f"- `{uc_id}`")
        md.append("")
    else:
        md.append("_No automation scripts generated yet._")
        md.append("")

    # ── 5. Batch Segregation — Ready for Generation ──
    md.append("---")
    md.append("## 5. Pending Batches — Ready for Generation")
    md.append("")
    batches = analysis["batches"]
    if not batches:
        md.append("_All UI-automatable use cases are already generated!_ 🎉")
    else:
        md.append(f"**{analysis['pending_count']} pending cases** grouped into **{len(batches)} batches**:")
        md.append("")
        for i, batch in enumerate(batches, 1):
            cases = batch["cases"]
            severity_counts = {}
            for c in cases:
                sev = c["severity"] if c["severity"] else "Unknown"
                severity_counts[sev] = severity_counts.get(sev, 0) + 1
            sev_str = ", ".join(f"{s}: {c}" for s, c in sorted(severity_counts.items()))
            size = _batch_size_label(batch["count"])

            md.append(f"### Batch {i} — {', '.join(batch['sub_modules'])} ({size})")
            md.append("")
            md.append(f"- **Cases**: {batch['count']}")
            md.append(f"- **Severity**: {sev_str}")
            md.append(f"- **Estimated generation time**: ~{batch['count'] * 2} min (AI) vs ~{batch['count'] * MANUAL_AUTHORING_AVG_MINUTES} min (manual)")
            md.append("")
            md.append("| UseCase ID | Severity | Description |")
            md.append("|------------|----------|-------------|")
            for c in cases:
                sev_icon = "🔴" if c["severity"] == "Critical" else ("🟡" if c["severity"] == "Major" else "🟢")
                desc = c["description"][:100] + "..." if len(c["description"]) > 100 else c["description"]
                md.append(f"| `{c['id']}` | {sev_icon} {c['severity']} | {desc} |")
            md.append("")

    # ── 6. Recommended Next Steps ──
    md.append("---")
    md.append("## 6. Recommended Next Steps")
    md.append("")
    if batches:
        first_batch = batches[0]
        crit_pending = analysis["sev_progress"].get("Critical", {}).get("pending", 0)
        md.append(f"1. **Priority**: {crit_pending} Critical cases still pending — generate these first")
        md.append(f"2. **Next batch**: Batch 1 — {', '.join(first_batch['sub_modules'])} ({first_batch['count']} cases)")
        md.append(f"3. **Command**: Copy the pending use-case IDs into `$PROJECT_NAME/tests_to_run.json` and invoke `@test-generator`")
        md.append(f"4. **Total remaining effort**: ~{analysis['pending_count'] * 2} min AI generation vs ~{analysis['pending_count'] * MANUAL_AUTHORING_AVG_MINUTES} min manual")
    else:
        md.append("All UI-automatable cases are generated. Next step: execute tests with `@test-runner`.")
    md.append("")

    # ── 7. Source Files ──
    md.append("---")
    md.append("## 7. Source Files")
    md.append("")
    md.append("| CSV File | Use Cases |")
    md.append("|----------|-----------|")
    for csv_name, cnt in sorted(analysis["csv_files"].items()):
        md.append(f"| `{csv_name}` | {cnt} |")
    md.append("")

    return "\n".join(md)


def main_usecase_analysis() -> str:
    """Main entry point for use-case analysis mode."""
    print(f"{'=' * 60}")
    print(f"  📋 Use-Case Requirement Analysis — {PROJECT_NAME}")
    print(f"{'=' * 60}")

    # 1. Load use-case CSV
    print("\n📄 Loading use-case documents...")
    usecases = load_usecase_csv()
    if not usecases:
        print("❌ No use-case CSV files found in Testcase/ directory")
        return ""
    print(f"   Found {len(usecases)} use cases across {len(set(uc['csv_file'] for uc in usecases))} CSV file(s)")

    # 2. Load automated IDs from tests_to_run.json (if it exists)
    automated_ids = set()
    if os.path.exists(TESTS_TO_RUN):
        print(f"\n📦 Loading test manifest: {os.path.basename(TESTS_TO_RUN)}")
        with open(TESTS_TO_RUN, "r") as f:
            manifest = json.load(f)
        for test in manifest.get("tests", []):
            tid = test.get("_id", "")
            if "," in tid:
                automated_ids.update(t.strip() for t in tid.split(","))
            else:
                automated_ids.add(tid.strip())
        automated_ids.discard("")
        print(f"   {len(automated_ids)} unique use-case IDs in manifest")
    else:
        print(f"\n⚠️  No tests_to_run.json found — analysis will show 0% generated")

    # 3. Build analysis
    print("\n🔍 Analyzing use-case inventory...")
    analysis = build_usecase_analysis(usecases, automated_ids)

    # 4. Generate Markdown
    print("\n📝 Generating analysis report...")
    markdown = generate_usecase_analysis_markdown(analysis)

    # 5. Write to file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs(AI_REPORTS_DIR, exist_ok=True)
    output_path = os.path.join(AI_REPORTS_DIR, f"USECASE_ANALYSIS_{timestamp}.md")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"\n✅ Analysis saved to: {output_path}")
    print(f"   File size: {os.path.getsize(output_path):,} bytes")

    # JSON snapshot
    json_path = os.path.join(AI_REPORTS_DIR, f"USECASE_ANALYSIS_{timestamp}.json")
    summary_data = {
        "generated_at": datetime.now().isoformat(),
        "mode": "usecase-analysis",
        "project": PROJECT_NAME,
        "total_usecases": analysis["total_usecases"],
        "ui_automatable": analysis["ui_yes_count"],
        "generated": analysis["generated_count"],
        "pending": analysis["pending_count"],
        "severity_progress": analysis["sev_progress"],
        "batches": [
            {
                "batch_num": i + 1,
                "sub_modules": b["sub_modules"],
                "case_count": b["count"],
                "case_ids": [c["id"] for c in b["cases"]],
            }
            for i, b in enumerate(analysis["batches"])
        ],
    }
    with open(json_path, "w") as f:
        json.dump(summary_data, f, indent=2)
    print(f"   JSON snapshot: {json_path}")

    ui_yes = analysis["ui_yes_count"]
    generated = analysis["generated_count"]
    pending = analysis["pending_count"]
    pct = round(generated / ui_yes * 100, 1) if ui_yes > 0 else 0

    print(f"\n{'=' * 60}")
    print(f"  UI-Automatable: {ui_yes} | Generated: {generated} ({pct}%) | Pending: {pending}")
    print(f"  Batches Ready: {len(analysis['batches'])}")
    print(f"{'=' * 60}")

    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch summary generator")
    parser.add_argument("--mode", choices=["execution", "generate", "usecase-analysis"],
                        default="execution",
                        help="'execution' (default) for post-run summary, 'generate' for "
                             "post-generation summary, 'usecase-analysis' for requirement analysis")
    parser.add_argument("--start-time", type=float, default=None,
                        help="Epoch timestamp when generation started (for timing calculation)")
    args = parser.parse_args()

    if args.mode == "generate":
        main_generate(start_epoch=args.start_time)
    elif args.mode == "usecase-analysis":
        main_usecase_analysis()
    else:
        main()
