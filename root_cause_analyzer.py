#!/usr/bin/env python3
"""
root_cause_analyzer.py
----------------------
Automated Root Cause Analysis for REAL_BREAKAGE test failures.

For each REAL_BREAKAGE failure, determines:
  - AUTOMATION_BUG: The test code itself is broken (wrong locator, null data, key mismatch, etc.)
  - PRODUCT_BUG:    The product behavior doesn't match expectations (UI changed, feature broken)
  - ENVIRONMENT:    Infrastructure issue (server down, timeout, network, browser crash)
  - UNDETERMINED:   Cannot classify with available signals

Analysis pipeline:
  1. Parse the ScenarioReport.html → extract structured step log, error details, LocalStorage state
  2. Heuristic classification based on error patterns
  3. (Optional) Playwright verification — navigate to the product UI and verify element existence
  4. Generate diagnosis summary

Usage (standalone):
    .venv/bin/python root_cause_analyzer.py <method_name> [--url <sdp_url>] [--verify]

    --verify enables Playwright UI verification for ambiguous cases
"""

import json
import os
import re
import glob
from dataclasses import dataclass, field, asdict
from enum import Enum
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ── Root Cause Classification ─────────────────────────────────────────────────

class RootCause(str, Enum):
    AUTOMATION_BUG = "AUTOMATION_BUG"
    PRODUCT_BUG = "PRODUCT_BUG"
    ENVIRONMENT = "ENVIRONMENT"
    UNDETERMINED = "UNDETERMINED"


@dataclass
class Diagnosis:
    root_cause: str  # RootCause value
    confidence: str  # HIGH / MEDIUM / LOW
    summary: str     # One-line human-readable summary
    details: str     # Multi-line explanation
    evidence: List[str] = field(default_factory=list)
    playwright_verified: bool = False

    def to_dict(self):
        return asdict(self)


# ── ScenarioReport Parser ────────────────────────────────────────────────────

@dataclass
class ReportStep:
    index: int
    timestamp: str
    step_type: str     # debug, action, rest_api, storage, step, error, user_switch, bidi
    message: str
    is_error: bool = False
    failure_text: str = ""   # Extracted <b>Failure:</b> content
    reason_text: str = ""    # Extracted <b>Reason:</b> content


@dataclass
class ScreenshotInfo:
    src: str               # e.g. "screenshots/Failure_1773981614506.png"
    alt: str               # action description
    result: str            # "PASS" or "FAIL"
    time: str = ""         # relative time e.g. "01:52"


@dataclass
class ReportDetails:
    """Metadata extracted from the report's details section."""
    scenario_id: str = ""
    description: str = ""
    entity_class: str = ""
    method_name: str = ""
    role: str = ""
    run_type: str = ""
    total_time: str = ""


@dataclass
class ParsedReport:
    steps: List[ReportStep]
    errors: List[ReportStep]
    local_storage: Dict[str, str]
    api_calls: List[ReportStep]
    stages: Dict[str, List[ReportStep]]  # pre_process, scenario, post_process, clean_up
    result: str  # PASS or FAIL
    screenshots_dir: str = ""
    screenshots: List[ScreenshotInfo] = field(default_factory=list)
    fail_screenshots: List[ScreenshotInfo] = field(default_factory=list)
    details: ReportDetails = field(default_factory=ReportDetails)
    all_error_text: str = ""  # Concatenated error text from all error steps


class ScenarioReportParser(HTMLParser):
    """Parses ScenarioReport.html and extracts structured step data."""

    def __init__(self):
        super().__init__()
        self._steps: List[ReportStep] = []
        self._local_storage: Dict[str, str] = {}
        self._current_stage = ""
        self._stages: Dict[str, List[ReportStep]] = {}
        self._in_message = False
        self._in_time = False
        self._in_stage_header = False
        self._current_text = ""
        self._current_time = ""
        self._current_type = ""
        self._current_id = ""
        self._step_index = 0
        self._result = "FAIL"

        # Screenshot parsing state
        self._screenshots: List[ScreenshotInfo] = []

        # Details section parsing state
        self._details = ReportDetails()
        self._in_detail_label = False
        self._in_detail_value = False
        self._current_label = ""
        self._current_value = ""
        self._in_title_div = False
        self._in_description_div = False

        # Rich error parsing state: track <b> tags inside error messages
        self._in_bold = False
        self._bold_text = ""
        self._current_failure_text = ""
        self._current_reason_text = ""
        self._after_failure_tag = False
        self._after_reason_tag = False
        self._step_index = 0
        self._result = "FAIL"

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        cls = attr_dict.get("class", "")

        # Detect result from main container
        if tag == "div" and "main-container" in cls:
            if "PASS" in cls:
                self._result = "PASS"
            elif "FAIL" in cls:
                self._result = "FAIL"

        # Detect scenario total time from data-totaltime
        if tag == "div" and "scenario-result" in cls:
            total_time = attr_dict.get("data-totaltime", "")
            if total_time:
                self._details.total_time = total_time

        # Title div
        if tag == "div" and cls == "title":
            self._in_title_div = True
            self._current_text = ""

        # Description div (inside scenario-details or short-info)
        if tag == "div" and cls == "description":
            self._in_description_div = True
            self._current_text = ""

        # Detail labels/values inside scenario-details
        if tag == "span" and cls == "label":
            self._in_detail_label = True
            self._current_label = ""
        if tag == "span" and ("value" in cls.split()):
            self._in_detail_value = True
            self._current_value = ""

        # Screenshot <img> tags
        if tag == "img" and attr_dict.get("src", "").startswith("screenshots/"):
            screenshot = ScreenshotInfo(
                src=attr_dict.get("src", ""),
                alt=attr_dict.get("alt", ""),
                result=attr_dict.get("data-result", ""),
                time=attr_dict.get("data-time", ""),
            )
            self._screenshots.append(screenshot)

        # Stage headers
        if tag == "div" and "stage header" in cls:
            self._in_stage_header = True
            self._current_text = ""

        # Message detail divs (step entries)
        if tag == "div" and "message-detail" in cls:
            self._current_id = attr_dict.get("id", "")
            # Extract type from class: "error message-detail" → "error"
            parts = cls.split()
            self._current_type = parts[0] if parts else "unknown"
            # Reset rich error state for each new step
            self._current_failure_text = ""
            self._current_reason_text = ""
            self._after_failure_tag = False
            self._after_reason_tag = False

        # Step message content
        if tag == "div" and "automater-step-message" in cls:
            self._in_message = True
            self._current_text = ""

        # Step time
        if tag == "div" and "automater-step-time" in cls:
            self._in_time = True
            self._current_text = ""

        # Bold tags inside error messages (<b>Failure:</b>, <b>Reason:</b>)
        if tag == "b" and self._in_message:
            self._in_bold = True
            self._bold_text = ""

        # <br> tags in error messages act as separators
        if tag == "br" and self._in_message:
            self._current_text += "\n"

    def handle_endtag(self, tag):
        # Bold tag end — determine if it was Failure: or Reason:
        if tag == "b" and self._in_bold:
            self._in_bold = False
            text = self._bold_text.strip()
            if "Failure" in text:
                self._after_failure_tag = True
                self._after_reason_tag = False
            elif "Reason" in text:
                self._after_reason_tag = True
                self._after_failure_tag = False

        # Detail label/value spans
        if tag == "span":
            if self._in_detail_label:
                self._in_detail_label = False
                self._current_label = self._current_label.strip()
            if self._in_detail_value:
                self._in_detail_value = False
                val = self._current_value.strip()
                label = self._current_label.lower()
                if label == "scenario id":
                    self._details.scenario_id = val
                elif label == "description":
                    self._details.description = val
                elif label == "class":
                    self._details.entity_class = val
                elif label == "method":
                    self._details.method_name = val
                elif label == "role":
                    self._details.role = val
                elif label == "run type":
                    self._details.run_type = val

        if tag == "div":
            if self._in_title_div:
                self._in_title_div = False
            if self._in_description_div:
                self._in_description_div = False

            if self._in_message:
                self._in_message = False
                msg = self._current_text.strip()

                # Build rich error components before collapsing
                failure_t = self._current_failure_text.strip()
                reason_t = self._current_reason_text.strip()

                msg = re.sub(r'\s+', ' ', msg)  # collapse whitespace

                is_error = self._current_type == "error"
                step = ReportStep(
                    index=self._step_index,
                    timestamp=self._current_time.strip(),
                    step_type=self._current_type,
                    message=msg,
                    is_error=is_error,
                    failure_text=re.sub(r'\s+', ' ', failure_t) if failure_t else "",
                    reason_text=re.sub(r'\s+', ' ', reason_t) if reason_t else "",
                )
                self._step_index += 1
                self._steps.append(step)
                if self._current_stage:
                    self._stages.setdefault(self._current_stage, []).append(step)

                # Extract LocalStorage entries
                if self._current_type == "storage":
                    m = re.search(r'Data added for key\s+(\S+)\s+and it\'s value is\s+(.+)', msg)
                    if m:
                        self._local_storage[m.group(1)] = m.group(2)

                # Reset error tracking for next step
                self._after_failure_tag = False
                self._after_reason_tag = False

            elif self._in_time:
                self._in_time = False
                self._current_time = self._current_text.strip()

            elif self._in_stage_header:
                self._in_stage_header = False
                self._current_stage = self._current_text.strip().replace(" ", "_").lower()

    def handle_data(self, data):
        if self._in_bold:
            self._bold_text += data
        if self._in_message or self._in_time or self._in_stage_header:
            self._current_text += data
            # Track Failure/Reason text segments
            if self._in_message and self._current_type == "error":
                if self._after_failure_tag and not self._after_reason_tag:
                    self._current_failure_text += data
                elif self._after_reason_tag:
                    self._current_reason_text += data
        if self._in_detail_label:
            self._current_label += data
        if self._in_detail_value:
            self._current_value += data
        if self._in_title_div and not self._details.method_name:
            # Title is typically the method name from short-info
            pass  # Title is redundant with details section

    def get_parsed_report(self) -> ParsedReport:
        errors = [s for s in self._steps if s.is_error]
        api_calls = [s for s in self._steps if s.step_type == "rest_api"]

        # Build combined error text from all error steps
        all_error_parts = []
        for err in errors:
            all_error_parts.append(err.message)
            if err.failure_text:
                all_error_parts.append(f"FAILURE: {err.failure_text}")
            if err.reason_text:
                all_error_parts.append(f"REASON: {err.reason_text}")
        all_error_text = "\n".join(all_error_parts)

        # Separate FAIL screenshots
        fail_screenshots = [s for s in self._screenshots if s.result == "FAIL"]

        return ParsedReport(
            steps=self._steps,
            errors=errors,
            local_storage=self._local_storage,
            api_calls=api_calls,
            stages=self._stages,
            result=self._result,
            screenshots=self._screenshots,
            fail_screenshots=fail_screenshots,
            details=self._details,
            all_error_text=all_error_text,
        )


def parse_scenario_report(html_path: str) -> Optional[ParsedReport]:
    """Parse a ScenarioReport.html file into structured data."""
    if not os.path.isfile(html_path):
        return None
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()
    parser = ScenarioReportParser()
    parser.feed(content)
    report = parser.get_parsed_report()
    report.screenshots_dir = os.path.join(os.path.dirname(html_path), "screenshots")
    return report


def find_latest_report(method_name: str, reports_dir: str) -> Optional[str]:
    """Find the latest ScenarioReport.html for a given method name."""
    if not os.path.isdir(reports_dir):
        return None
    matching = sorted(
        [d for d in os.listdir(reports_dir) if d.startswith(f"LOCAL_{method_name}_")],
        reverse=True,
    )
    if not matching:
        return None
    path = os.path.join(reports_dir, matching[0], "ScenarioReport.html")
    return path if os.path.isfile(path) else None


# ── Java Source Analyzer ──────────────────────────────────────────────────────

def find_test_source(entity_class: str, src_dir: str) -> Optional[str]:
    """Find the Java source file for a given entity class."""
    pattern = os.path.join(src_dir, "**", f"{entity_class}.java")
    matches = glob.glob(pattern, recursive=True)
    return matches[0] if matches else None


def extract_method_source(java_path: str, method_name: str) -> Optional[str]:
    """Extract a method's source code from a Java file (best effort)."""
    if not java_path or not os.path.isfile(java_path):
        return None
    with open(java_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Use a simple line-based search for the method signature (fast)
    sig_pattern = re.compile(
        rf'\b(?:public|protected|private)\b[^;]*\b{re.escape(method_name)}\s*\('
    )
    match = sig_pattern.search(content)
    if not match:
        return None

    # Walk backwards to capture annotations
    start = match.start()
    lines_before = content[:start].split('\n')
    while lines_before and lines_before[-1].strip() == '':
        lines_before.pop()
    # Capture preceding annotation lines
    annotation_lines = []
    for line in reversed(lines_before):
        stripped = line.strip()
        if stripped.startswith('@') or stripped.startswith(')') or stripped.endswith(','):
            annotation_lines.insert(0, line)
        elif stripped == '' and annotation_lines:
            continue
        else:
            break
    if annotation_lines:
        start = content[:start].rfind(annotation_lines[0].rstrip())
        if start < 0:
            start = match.start()

    # Track braces to find method end — find first '{' from match
    i = match.end()
    while i < len(content) and content[i] != '{':
        i += 1
    if i >= len(content):
        return None

    brace_count = 0
    while i < len(content):
        if content[i] == '{':
            brace_count += 1
        elif content[i] == '}':
            brace_count -= 1
            if brace_count == 0:
                return content[start:i + 1]
        i += 1
    return content[start:]


# ── Heuristic Root Cause Classifier ──────────────────────────────────────────

# Pattern → (root_cause, confidence, summary_template)
_ERROR_PATTERNS: List[Tuple[re.Pattern, RootCause, str, str]] = [
    # ── AUTOMATION_BUG patterns (HIGH confidence) ──
    (
        re.compile(r"Keys to send should be a not null CharSequence", re.I),
        RootCause.AUTOMATION_BUG, "HIGH",
        "Null value passed to sendKeys() — likely a LocalStorage key mismatch or missing data"
    ),
    (
        re.compile(r"NullPointerException", re.I),
        RootCause.AUTOMATION_BUG, "HIGH",
        "NullPointerException — test code received null where it expected a value"
    ),
    (
        re.compile(r"ClassNotFoundException|ClassCastException|MethodNotFoundException", re.I),
        RootCause.AUTOMATION_BUG, "HIGH",
        "Class/method not found — build or import issue in automation code"
    ),
    (
        re.compile(r"compilation\s+error|cannot find symbol|incompatible types", re.I),
        RootCause.AUTOMATION_BUG, "HIGH",
        "Compilation error — automation code has syntax or type errors"
    ),
    (
        re.compile(r"IndexOutOfBoundsException|ArrayIndexOutOfBoundsException", re.I),
        RootCause.AUTOMATION_BUG, "HIGH",
        "Index out of bounds — test code accesses invalid array/list index"
    ),
    (
        re.compile(r"JSONException|json\.org\.JSONException", re.I),
        RootCause.AUTOMATION_BUG, "MEDIUM",
        "JSON parsing error — test data format issue or unexpected API response shape"
    ),
    (
        re.compile(r"NumberFormatException", re.I),
        RootCause.AUTOMATION_BUG, "HIGH",
        "NumberFormatException — test code tries to parse non-numeric string"
    ),
    (
        re.compile(r"IllegalArgumentException", re.I),
        RootCause.AUTOMATION_BUG, "MEDIUM",
        "IllegalArgumentException — test code passed invalid argument"
    ),
    (
        re.compile(r"StackOverflowError", re.I),
        RootCause.AUTOMATION_BUG, "HIGH",
        "StackOverflowError — infinite recursion in test code"
    ),
    (
        re.compile(r"AssertionError|AssertionException", re.I),
        RootCause.AUTOMATION_BUG, "MEDIUM",
        "Assertion failed — test assertion did not hold"
    ),

    # ── ENVIRONMENT patterns ──
    (
        re.compile(r"WebDriverException.*session.*(?:deleted|not found|crashed)", re.I),
        RootCause.ENVIRONMENT, "HIGH",
        "Browser session crashed — environment/infrastructure issue"
    ),
    (
        re.compile(r"Connection\s*refused|ERR_CONNECTION_REFUSED|ECONNREFUSED", re.I),
        RootCause.ENVIRONMENT, "HIGH",
        "Connection refused — server is down or unreachable"
    ),
    (
        re.compile(r"UnreachableBrowserException|SessionNotCreatedException", re.I),
        RootCause.ENVIRONMENT, "HIGH",
        "Browser unreachable — WebDriver/browser startup failure"
    ),
    (
        re.compile(r"Read\s*timed?\s*out|SocketTimeoutException|connect\s+timed\s+out", re.I),
        RootCause.ENVIRONMENT, "HIGH",
        "Network timeout — server unresponsive or network issue"
    ),
    (
        re.compile(r"OutOfMemoryError|heap\s+space", re.I),
        RootCause.ENVIRONMENT, "HIGH",
        "Out of memory — JVM ran out of heap space"
    ),
    (
        re.compile(r"Firefox\s+(?:crashed|is\s+already\s+running)|geckodriver\s+(?:error|failed|crash|not\s+found|timed?\s*out)", re.I),
        RootCause.ENVIRONMENT, "HIGH",
        "Firefox/geckodriver issue — browser infrastructure problem"
    ),
    (
        re.compile(r"InsecureCertificateException|SSL_ERROR|certificate", re.I),
        RootCause.ENVIRONMENT, "MEDIUM",
        "SSL certificate error — environment configuration issue"
    ),

    # ── PRODUCT_BUG patterns (need context to confirm) ──
    (
        re.compile(r"Expected.*but\s+(?:got|was|found)\b", re.I),
        RootCause.PRODUCT_BUG, "MEDIUM",
        "Assertion mismatch — product returned unexpected value"
    ),
    (
        re.compile(r"successMessageInAlert.*failed|errorMessageInAlert", re.I),
        RootCause.PRODUCT_BUG, "MEDIUM",
        "Alert message validation failed — product showed unexpected message"
    ),
    (
        re.compile(r"status_code.*4000|EXTRA_KEY_FOUND_IN_JSON|INVALID_INPUT", re.I),
        RootCause.PRODUCT_BUG, "MEDIUM",
        "API returned error — product rejected valid-looking input"
    ),
    (
        re.compile(r"(?:given|expected)\b.*(?:value|text)\b.*(?:mismatched|mismatch|not match|differ)", re.I),
        RootCause.PRODUCT_BUG, "MEDIUM",
        "Value mismatch — product displayed a different value than expected"
    ),
    (
        re.compile(r"Internal (?:Server )?Error|500\s+Internal|HTTP\s+500", re.I),
        RootCause.PRODUCT_BUG, "MEDIUM",
        "Internal server error — product returned 500"
    ),
    (
        re.compile(r"feature\s+(?:not\s+)?(?:enabled|available|supported|disabled)", re.I),
        RootCause.PRODUCT_BUG, "MEDIUM",
        "Feature availability issue — product feature state unexpected"
    ),
    (
        re.compile(r"permission\s+denied|access\s+denied|unauthorized|403\s+Forbidden", re.I),
        RootCause.PRODUCT_BUG, "MEDIUM",
        "Permission/access denied — product rejected valid user action"
    ),
    (
        re.compile(r"(?:not\s+verified|verification\s+failed|failed\s+to\s+verify|is\s+not\s+working)", re.I),
        RootCause.PRODUCT_BUG, "MEDIUM",
        "Test verification failed — product behavior did not match expected result"
    ),

    # ── AMBIGUOUS patterns (NoSuchElement can be either) ──
    (
        re.compile(r"NoSuchElementException|Unable to locate element", re.I),
        RootCause.UNDETERMINED, "LOW",
        "Element not found — could be wrong locator (automation) or missing UI element (product)"
    ),
    (
        re.compile(r"TimeoutException|wait timed out", re.I),
        RootCause.UNDETERMINED, "LOW",
        "Timeout waiting for element — could be slow page (product) or wrong locator (automation)"
    ),
    (
        re.compile(r"StaleElementReferenceException", re.I),
        RootCause.UNDETERMINED, "LOW",
        "Stale element — page DOM changed during interaction (timing issue)"
    ),
    (
        re.compile(r"ElementClickInterceptedException|element click intercepted", re.I),
        RootCause.UNDETERMINED, "LOW",
        "Click intercepted — overlay or popup blocking the target element"
    ),
    (
        re.compile(r"ElementNotInteractableException|element not interactable", re.I),
        RootCause.UNDETERMINED, "LOW",
        "Element not interactable — element exists but cannot be clicked/typed into"
    ),
]

# LocalStorage key mismatch patterns (common automation bugs)
_LOCALSTORAGE_NULL_PATTERNS = [
    (re.compile(r'LocalStorage\.(?:getAsString|fetch)\("([^"]+)"\)'), "automation reads key '{key}'"),
    (re.compile(r'getTestCaseData\(.*?null'), "test data returned null"),
]


def _analyze_localstorage_mismatch(
    report: ParsedReport,
    method_source: Optional[str],
    error_msg: str,
) -> Optional[Diagnosis]:
    """
    Check if the error is caused by reading a LocalStorage key that was never set.
    This is a common automation bug pattern.
    """
    if not method_source:
        return None

    # Find all LocalStorage keys the test method tries to read
    read_keys = set()
    for m in re.finditer(r'LocalStorage\.(?:getAsString|fetch)\(\s*"([^"]+)"\s*\)', method_source):
        read_keys.add(m.group(1))

    stored_keys = set(report.local_storage.keys())
    missing_keys = read_keys - stored_keys

    if missing_keys and ("null" in error_msg.lower() or "Keys to send" in error_msg):
        return Diagnosis(
            root_cause=RootCause.AUTOMATION_BUG.value,
            confidence="HIGH",
            summary=f"LocalStorage key mismatch: test reads {missing_keys} but only {stored_keys & read_keys} were set",
            details=(
                f"The test method reads these LocalStorage keys: {sorted(read_keys)}\n"
                f"But preProcess only stored: {sorted(stored_keys)}\n"
                f"Missing keys: {sorted(missing_keys)}\n\n"
                f"This is an automation code bug — the preProcess stores data under a different key "
                f"name than what the test method expects."
            ),
            evidence=[
                f"Missing key(s): {', '.join(sorted(missing_keys))}",
                f"Stored key(s): {', '.join(sorted(stored_keys))}",
                f"Error: {error_msg[:200]}",
            ],
        )
    return None


def _analyze_api_failure_in_preprocess(report: ParsedReport) -> Optional[Diagnosis]:
    """Check if preProcess API calls returned errors — could indicate product issue."""
    pre_steps = report.stages.get("pre_process", [])
    for step in pre_steps:
        if step.is_error and "Got bad response" in step.message:
            # API call failed in preProcess
            if "status_code" in step.message:
                status_match = re.search(r'"status_code":(\d+)', step.message)
                if status_match:
                    code = int(status_match.group(1))
                    if code >= 4000:
                        return Diagnosis(
                            root_cause=RootCause.PRODUCT_BUG.value,
                            confidence="MEDIUM",
                            summary=f"API call failed in preProcess with status {code}",
                            details=(
                                f"A REST API call during preProcess returned an error response.\n"
                                f"This may indicate the product API rejected valid input, "
                                f"or a product-side change broke the API contract.\n\n"
                                f"Error step: {step.message[:300]}"
                            ),
                            evidence=[f"API error in preProcess: {step.message[:200]}"],
                        )
    return None


def _analyze_scenario_stage_error(report: ParsedReport, error_msg: str) -> Optional[Diagnosis]:
    """Analyze errors in the scenario (test execution) stage."""
    scenario_steps = report.stages.get("scenario", [])
    if not scenario_steps:
        return None

    # Count successful steps before the first error AND total action/step count
    success_count = 0
    total_actions = 0
    last_action = ""
    hit_error = False
    for step in scenario_steps:
        if step.is_error:
            hit_error = True
            continue
        if step.step_type in ("action", "step"):
            total_actions += 1
            if not hit_error:
                success_count += 1
            last_action = step.message

    # If multiple UI actions succeeded before failure, more likely a product bug or
    # a specific locator issue at a particular point in the flow
    element_not_found = re.search(
        r"NoSuchElement|Unable to locate element|Element not found|TimeoutException|wait timed out",
        error_msg, re.I,
    )
    if element_not_found and (success_count >= 5 or total_actions >= 10):
        return Diagnosis(
            root_cause=RootCause.PRODUCT_BUG.value,
            confidence="MEDIUM",
            summary=f"UI element missing after {success_count} successful steps — likely product change",
            details=(
                f"The test successfully executed {success_count} UI steps before failing "
                f"({total_actions} total actions in scenario).\n"
                f"Last successful action: {last_action[:150]}\n\n"
                f"Since the test navigated deep into the UI flow, the missing element "
                f"is more likely a product change than a fundamentally wrong locator.\n"
                f"Consider verifying with Playwright (--verify flag)."
            ),
            evidence=[
                f"Successful steps before error: {success_count}",
                f"Total actions in scenario: {total_actions}",
                f"Last action: {last_action[:150]}",
                f"Error: {error_msg[:200]}",
            ],
        )

    # Also check for generic failures with many successful steps
    if (success_count >= 3 or total_actions >= 10) and report.errors:
        first_error = report.errors[0]
        err_text = first_error.reason_text or first_error.failure_text or first_error.message
        if err_text:
            # Check if the reason matches any product-bug patterns
            for pattern, cause, confidence, summary in _ERROR_PATTERNS:
                if cause == RootCause.PRODUCT_BUG and pattern.search(err_text):
                    return Diagnosis(
                        root_cause=cause.value,
                        confidence=confidence,
                        summary=f"{summary} (after {success_count} successful steps)",
                        details=(
                            f"Test executed {success_count} steps before failing "
                            f"({total_actions} total actions).\n"
                            f"Failure: {first_error.failure_text[:200]}\n"
                            f"Reason: {first_error.reason_text[:200]}"
                        ),
                        evidence=[
                            f"Successful steps: {success_count}",
                            f"Total actions: {total_actions}",
                            f"Failure: {first_error.failure_text[:150]}",
                            f"Reason: {first_error.reason_text[:150]}",
                        ],
                    )

    return None


def _analyze_error_steps_deeply(report: ParsedReport) -> Optional[Diagnosis]:
    """
    Analyze error steps from the report with Failure/Reason decomposition.
    This catches cases where the runner stdout only had a generic wrapper like
    "WARNING: FAILURE: X failed" but the report has the actual root cause details.
    """
    if not report.errors:
        return None

    for err_step in report.errors:
        # Check the rich Failure/Reason text extracted from <b> tags
        reason = err_step.reason_text
        failure = err_step.failure_text

        # First, try to match the reason_text against known patterns (most specific)
        text_to_check = reason or failure or err_step.message
        if text_to_check:
            for pattern, cause, confidence, summary in _ERROR_PATTERNS:
                if pattern.search(text_to_check):
                    # For UNDETERMINED (e.g. NoSuchElement), try scenario stage refinement
                    if cause == RootCause.UNDETERMINED:
                        effective = report.all_error_text or text_to_check
                        refined = _analyze_scenario_stage_error(report, effective)
                        if refined:
                            return refined
                    return Diagnosis(
                        root_cause=cause.value,
                        confidence=confidence,
                        summary=summary,
                        details=(
                            f"Extracted from ScenarioReport error step #{err_step.index}:\n"
                            f"  Failure: {failure[:200]}\n"
                            f"  Reason: {reason[:200]}\n"
                            f"  Full message: {err_step.message[:300]}"
                        ),
                        evidence=[
                            f"[Report Error] Failure: {failure[:150]}",
                            f"[Report Error] Reason: {reason[:150]}",
                        ],
                    )

    # Second pass: combine all error text and try patterns on the full corpus
    combined = report.all_error_text
    if combined:
        for pattern, cause, confidence, summary in _ERROR_PATTERNS:
            if pattern.search(combined):
                # For UNDETERMINED, try scenario stage refinement first
                if cause == RootCause.UNDETERMINED:
                    refined = _analyze_scenario_stage_error(report, combined)
                    if refined:
                        return refined
                return Diagnosis(
                    root_cause=cause.value,
                    confidence=confidence,
                    summary=summary,
                    details=(
                        f"Pattern matched in combined report error text.\n"
                        f"Errors from report:\n{combined[:500]}"
                    ),
                    evidence=[f"[Report Errors] {combined[:200]}"],
                )

    return None


def _analyze_failure_stage(report: ParsedReport) -> Optional[Diagnosis]:
    """
    Determine which stage the failure occurred in and apply stage-specific heuristics.
    - pre_process failures → often AUTOMATION_BUG (API setup went wrong)
    - post_process/clean_up failures → ignore (test already completed)
    - admin_session failures → ENVIRONMENT (login/cookie issues)
    - scenario failures → analyze deeper
    """
    # Check if error only occurs in pre_process
    pre_errors = [s for s in report.stages.get("pre_process", []) if s.is_error]
    scenario_errors = [s for s in report.stages.get("scenario", []) if s.is_error]

    if pre_errors and not scenario_errors:
        err = pre_errors[0]
        # preProcess error — likely automation bug (bad API call, wrong data setup)
        # unless it's a status_code error (product API changed)
        if re.search(r'status_code.*[45]\d{3}', err.message):
            return Diagnosis(
                root_cause=RootCause.PRODUCT_BUG.value,
                confidence="MEDIUM",
                summary="preProcess API call failed — product API may have changed",
                details=(
                    f"Error occurred in preProcess stage (API setup).\n"
                    f"Error: {err.message[:300]}\n"
                    f"This suggests the product API rejected a previously valid request."
                ),
                evidence=[
                    f"[Stage: pre_process] {err.message[:200]}",
                    f"[Stage: pre_process] Failure: {err.failure_text[:150]}" if err.failure_text else "",
                ],
            )
        return Diagnosis(
            root_cause=RootCause.AUTOMATION_BUG.value,
            confidence="MEDIUM",
            summary="preProcess failed — test data setup issue",
            details=(
                f"Error occurred in preProcess stage.\n"
                f"Error: {err.message[:300]}\n"
                f"Failure: {err.failure_text[:200]}\n"
                f"Reason: {err.reason_text[:200]}"
            ),
            evidence=[
                f"[Stage: pre_process] {err.message[:200]}",
            ],
        )

    # Check if error is in admin_session stage (login issues)
    admin_errors = [s for s in report.stages.get("admin_session", []) if s.is_error]
    if admin_errors and not scenario_errors:
        return Diagnosis(
            root_cause=RootCause.ENVIRONMENT.value,
            confidence="MEDIUM",
            summary="Admin session setup failed — login or environment issue",
            details=f"Error during admin session: {admin_errors[0].message[:300]}",
            evidence=[f"[Stage: admin_session] {admin_errors[0].message[:200]}"],
        )

    return None


def _analyze_screenshot_context(report: ParsedReport) -> List[str]:
    """
    Extract evidence from screenshot metadata.
    Returns a list of evidence strings about what the screenshots reveal.
    """
    evidence = []

    if report.fail_screenshots:
        for ss in report.fail_screenshots:
            evidence.append(
                f"[FAIL Screenshot] '{ss.alt}' at {ss.time} — {ss.src}"
            )

    # Analyze screenshot sequence for context
    if report.screenshots:
        total = len(report.screenshots)
        fail_count = len(report.fail_screenshots)
        pass_count = total - fail_count
        if total > 0:
            evidence.append(
                f"[Screenshots] {pass_count} PASS + {fail_count} FAIL out of {total} total"
            )

        # Find the last PASS screenshot before the first FAIL (indicates where things went wrong)
        last_pass_before_fail = None
        for ss in report.screenshots:
            if ss.result == "FAIL":
                break
            last_pass_before_fail = ss
        if last_pass_before_fail:
            evidence.append(
                f"[Last success before failure] '{last_pass_before_fail.alt}' at {last_pass_before_fail.time}"
            )

    return evidence


def _build_effective_error_msg(error_msg: str, report: Optional[ParsedReport]) -> str:
    """
    Build the most comprehensive error text by combining:
    1. The original error_msg from runner stdout
    2. All error messages from the ScenarioReport
    3. Failure/Reason text from error steps

    This ensures pattern matching works even when the runner only captured
    a generic wrapper like "WARNING: FAILURE: X failed".
    """
    parts = [error_msg] if error_msg else []

    if report:
        # Add the combined error text from the report
        if report.all_error_text:
            parts.append(report.all_error_text)

        # Add individual failure/reason texts
        for err in report.errors:
            if err.failure_text and err.failure_text not in error_msg:
                parts.append(err.failure_text)
            if err.reason_text and err.reason_text not in error_msg:
                parts.append(err.reason_text)

    return "\n".join(parts)


def _enrich_with_localstorage_context(
    diag: Diagnosis,
    report: ParsedReport,
    method_source: str,
) -> None:
    """Add LocalStorage key evidence to an existing Diagnosis (mutates in place)."""
    read_keys = set()
    for m in re.finditer(r'LocalStorage\.(?:getAsString|fetch)\(\s*"([^"]+)"\s*\)', method_source):
        read_keys.add(m.group(1))
    if not read_keys:
        return

    stored_keys = set(report.local_storage.keys())
    missing = read_keys - stored_keys
    if missing:
        diag.evidence.append(f"LocalStorage keys read by test: {sorted(read_keys)}")
        diag.evidence.append(f"Keys stored by preProcess: {sorted(stored_keys)}")
        diag.evidence.append(f"Missing keys: {sorted(missing)}")
        diag.confidence = "HIGH"
        diag.summary += f" (missing LocalStorage keys: {', '.join(sorted(missing))})"


def classify_failure(
    error_msg: str,
    report: Optional[ParsedReport] = None,
    method_source: Optional[str] = None,
) -> Diagnosis:
    """
    Classify a test failure as AUTOMATION_BUG, PRODUCT_BUG, ENVIRONMENT, or UNDETERMINED.

    Enhanced pipeline:
      1. LocalStorage key mismatch (highest priority — very clear signal)
      2. API failures in preProcess
      3. Stage-based analysis (which lifecycle stage failed?)
      4. Pattern matching on runner error message
      5. Deep report error parsing (Failure/Reason from <b> tags in error divs)
      6. Pattern matching on combined error text (runner msg + all report errors)
      7. Scenario stage heuristics (successful-steps-before-failure analysis)
      8. Fallback: UNDETERMINED with evidence from report + screenshots
    """
    # Build the effective error text (runner msg + report errors combined)
    effective_error = _build_effective_error_msg(error_msg, report)

    # 1. Check LocalStorage mismatch (highest priority — very clear signal)
    if report and method_source:
        ls_diag = _analyze_localstorage_mismatch(report, method_source, effective_error)
        if ls_diag:
            _add_screenshot_evidence(ls_diag, report)
            return ls_diag

    # 2. Check API failures in preProcess
    if report:
        api_diag = _analyze_api_failure_in_preprocess(report)
        if api_diag:
            _add_screenshot_evidence(api_diag, report)
            return api_diag

    # 3. Stage-based analysis (pre_process vs scenario vs admin_session)
    if report:
        stage_diag = _analyze_failure_stage(report)
        if stage_diag:
            _add_screenshot_evidence(stage_diag, report)
            return stage_diag

    # 4. Pattern matching on the original runner error message
    for pattern, cause, confidence, summary in _ERROR_PATTERNS:
        if pattern.search(error_msg):
            diag = Diagnosis(
                root_cause=cause.value,
                confidence=confidence,
                summary=summary,
                details=f"Error matched pattern: {pattern.pattern}\nFull error: {error_msg[:500]}",
                evidence=[f"Error: {error_msg[:200]}"],
            )

            # Enrich with LocalStorage context if available
            if report and method_source and cause == RootCause.AUTOMATION_BUG:
                _enrich_with_localstorage_context(diag, report, method_source)

            # For UNDETERMINED, try to refine with report context
            if cause == RootCause.UNDETERMINED and report:
                refined = _analyze_scenario_stage_error(report, effective_error)
                if refined:
                    _add_screenshot_evidence(refined, report)
                    return refined

            _add_screenshot_evidence(diag, report)
            return diag

    # 5. Deep report error parsing — the runner error was too generic,
    #    but the ScenarioReport may have the actual exception/reason
    if report:
        deep_diag = _analyze_error_steps_deeply(report)
        if deep_diag:
            _add_screenshot_evidence(deep_diag, report)
            return deep_diag

    # 6. Pattern matching on the combined (effective) error text
    #    This catches cases where the actual exception is only in the report
    if effective_error != error_msg:
        for pattern, cause, confidence, summary in _ERROR_PATTERNS:
            if pattern.search(effective_error):
                # For UNDETERMINED, try scenario stage refinement first
                if cause == RootCause.UNDETERMINED and report:
                    refined = _analyze_scenario_stage_error(report, effective_error)
                    if refined:
                        _add_screenshot_evidence(refined, report)
                        return refined
                diag = Diagnosis(
                    root_cause=cause.value,
                    confidence=confidence,
                    summary=summary + " (from report error details)",
                    details=(
                        f"Pattern matched in combined error text (runner + report).\n"
                        f"Runner error: {error_msg[:200]}\n"
                        f"Report errors: {report.all_error_text[:300] if report else 'N/A'}"
                    ),
                    evidence=[
                        f"Runner error: {error_msg[:150]}",
                        f"Report errors: {report.all_error_text[:150] if report else 'N/A'}",
                    ],
                )
                _add_screenshot_evidence(diag, report)
                return diag

    # 7. Scenario stage heuristics for the combined error
    if report:
        refined = _analyze_scenario_stage_error(report, effective_error)
        if refined:
            _add_screenshot_evidence(refined, report)
            return refined

    # 8. Fallback: UNDETERMINED — but with rich evidence from report and screenshots
    evidence = [f"Error: {error_msg[:200]}"]
    details_parts = [f"No known error pattern matched.\nRunner error: {error_msg[:500]}"]

    if report:
        # Add report error details to help manual classification
        if report.all_error_text:
            details_parts.append(f"\nReport error text:\n{report.all_error_text[:500]}")
            evidence.append(f"[Report Errors] {report.all_error_text[:200]}")

        # Add stage information
        for stage_name in ["pre_process", "scenario", "post_process"]:
            stage_errors = [s for s in report.stages.get(stage_name, []) if s.is_error]
            if stage_errors:
                evidence.append(f"[{stage_name}] {len(stage_errors)} error(s)")
                for se in stage_errors[:2]:
                    if se.failure_text:
                        evidence.append(f"  Failure: {se.failure_text[:150]}")
                    if se.reason_text:
                        evidence.append(f"  Reason: {se.reason_text[:150]}")

        # Add screenshot evidence
        ss_evidence = _analyze_screenshot_context(report)
        evidence.extend(ss_evidence)

        # Add report metadata
        if report.details.scenario_id:
            evidence.append(f"Scenario: {report.details.scenario_id}")

    diag = Diagnosis(
        root_cause=RootCause.UNDETERMINED.value,
        confidence="LOW",
        summary="Could not automatically classify this failure",
        details="\n".join(details_parts),
        evidence=evidence,
    )
    return diag


def _add_screenshot_evidence(diag: Diagnosis, report: Optional[ParsedReport]) -> None:
    """Add screenshot context evidence to an existing Diagnosis."""
    if not report:
        return
    ss_evidence = _analyze_screenshot_context(report)
    diag.evidence.extend(ss_evidence)


# ── Playwright UI Verification ────────────────────────────────────────────────

def verify_with_playwright(
    sdp_url: str,
    admin_email: str,
    admin_pass: str,
    portal: str,
    diagnosis: Diagnosis,
    report: Optional[ParsedReport] = None,
) -> Diagnosis:
    """
    Use Playwright to navigate to SDP and verify if the product UI matches expectations.
    Refines the diagnosis for UNDETERMINED or LOW-confidence cases.

    Only runs for cases where Playwright can provide additional signal:
    - NoSuchElementException → check if element exists in current product UI
    - TimeoutException → check if page loads properly
    - API errors → check if the feature is accessible
    """
    # Only verify when diagnosis is ambiguous
    if diagnosis.confidence == "HIGH" and diagnosis.root_cause != RootCause.UNDETERMINED.value:
        diagnosis.playwright_verified = False
        return diagnosis

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        diagnosis.evidence.append("Playwright not installed — skipping UI verification")
        return diagnosis

    verification_result = _run_playwright_verification(
        sdp_url, admin_email, admin_pass, portal, diagnosis, report
    )
    return verification_result


def _run_playwright_verification(
    sdp_url: str,
    admin_email: str,
    admin_pass: str,
    portal: str,
    diagnosis: Diagnosis,
    report: Optional[ParsedReport],
) -> Diagnosis:
    """Execute Playwright browser session to verify product state."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        context = browser.new_context(
            ignore_https_errors=True,
            viewport={"width": 1920, "height": 1080},
        )
        page = context.new_page()

        try:
            # Login
            logged_in = _playwright_login(page, sdp_url, admin_email, admin_pass)
            if not logged_in:
                diagnosis.evidence.append("Playwright: Failed to login — cannot verify product state")
                diagnosis.playwright_verified = True
                return diagnosis

            # Wait for SDP to fully load
            page.wait_for_load_state("networkidle", timeout=30000)

            # Decide what to verify based on the error
            error_msg = diagnosis.details or ""

            if "NoSuchElement" in error_msg or "Unable to locate" in error_msg:
                _verify_element_existence(page, sdp_url, portal, diagnosis, report)
            elif "TimeoutException" in error_msg or "wait timed out" in error_msg:
                _verify_page_loads(page, sdp_url, portal, diagnosis, report)
            elif "status_code" in error_msg and "400" in error_msg:
                _verify_api_endpoint(page, diagnosis, report)
            else:
                # Generic: just check if the product is up and accessible
                _verify_product_accessible(page, sdp_url, portal, diagnosis)

            diagnosis.playwright_verified = True

        except Exception as e:
            diagnosis.evidence.append(f"Playwright verification error: {str(e)[:200]}")
            diagnosis.playwright_verified = True
        finally:
            context.close()
            browser.close()

    return diagnosis


def _playwright_login(page, sdp_url: str, admin_email: str, admin_pass: str) -> bool:
    """Login to SDP via Playwright. Returns True on success."""
    try:
        page.goto(sdp_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_timeout(2000)

        # Fill email
        email_input = page.locator('input[name="LOGIN_ID"], input[type="email"], #login_id')
        if email_input.count() > 0:
            email_input.first.fill(admin_email)
            # Click Next
            next_btn = page.locator('button:has-text("Next"), input[type="submit"]')
            if next_btn.count() > 0:
                next_btn.first.click()
                page.wait_for_timeout(2000)

            # Fill password
            pass_input = page.locator('input[name="PASSWORD"], input[type="password"]')
            if pass_input.count() > 0:
                pass_input.first.fill(admin_pass)
                signin_btn = page.locator('button:has-text("Sign in"), input[id="nextbtn"]')
                if signin_btn.count() > 0:
                    signin_btn.first.click()
                    page.wait_for_timeout(5000)

        # Check if logged in by looking for SDP UI elements
        page.wait_for_load_state("networkidle", timeout=30000)
        return True
    except Exception:
        return False


def _verify_element_existence(page, sdp_url, portal, diagnosis, report):
    """For NoSuchElementException — check if the module/page is accessible."""
    # Extract module from error or report context
    scenario_steps = report.stages.get("scenario", []) if report else []

    # Find last navigation action before error
    last_nav = ""
    for step in scenario_steps:
        if step.step_type == "action" and "Load page" in step.message:
            last_nav = step.message
        elif step.step_type == "action" and "Click" in step.message:
            last_nav = step.message

    if last_nav:
        diagnosis.evidence.append(f"Playwright: Last navigation was: {last_nav[:150]}")

    # Try to access the module page
    try:
        home_url = f"{sdp_url}/app/{portal}/HomePage.do"
        page.goto(home_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("networkidle", timeout=15000)

        # Check if the page loaded with SDP UI
        sdp_loaded = page.locator('#app-main, #sdp-main, .home-page-container, .sdp-body').count() > 0
        if sdp_loaded:
            diagnosis.evidence.append("Playwright: SDP product UI loads successfully")

            # If the error is about a specific element, check the page
            if diagnosis.root_cause == RootCause.UNDETERMINED.value:
                diagnosis.root_cause = RootCause.AUTOMATION_BUG.value
                diagnosis.confidence = "MEDIUM"
                diagnosis.summary += " — Product UI accessible; likely a locator issue in automation code"
        else:
            diagnosis.evidence.append("Playwright: SDP product UI did NOT load — possible product issue")
            diagnosis.root_cause = RootCause.PRODUCT_BUG.value
            diagnosis.confidence = "MEDIUM"
            diagnosis.summary += " — Product page failed to load"
    except Exception as e:
        diagnosis.evidence.append(f"Playwright: Page navigation failed: {str(e)[:150]}")


def _verify_page_loads(page, sdp_url, portal, diagnosis, report):
    """For TimeoutException — check if pages load within expected time."""
    try:
        home_url = f"{sdp_url}/app/{portal}/HomePage.do"
        start = page.evaluate("Date.now()")
        page.goto(home_url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_load_state("networkidle", timeout=15000)
        end = page.evaluate("Date.now()")
        load_time = (end - start) / 1000

        if load_time > 10:
            diagnosis.evidence.append(f"Playwright: Page took {load_time:.1f}s to load — product is slow")
            diagnosis.root_cause = RootCause.PRODUCT_BUG.value
            diagnosis.confidence = "MEDIUM"
            diagnosis.summary += f" — Product page slow ({load_time:.0f}s)"
        else:
            diagnosis.evidence.append(f"Playwright: Page loaded in {load_time:.1f}s — normal speed")
            if diagnosis.root_cause == RootCause.UNDETERMINED.value:
                diagnosis.root_cause = RootCause.AUTOMATION_BUG.value
                diagnosis.confidence = "LOW"
                diagnosis.summary += " — Product loads fine; likely a wait/timing issue in automation"
    except Exception as e:
        diagnosis.evidence.append(f"Playwright: {str(e)[:150]}")
        diagnosis.root_cause = RootCause.ENVIRONMENT.value
        diagnosis.confidence = "MEDIUM"
        diagnosis.summary = "Product unreachable or extremely slow"


def _verify_api_endpoint(page, diagnosis, report):
    """For API errors — check if the API endpoint responds correctly."""
    api_calls = report.api_calls if report else []
    for call_step in api_calls:
        if "bad response" in call_step.message.lower():
            # Extract API path
            path_match = re.search(r'for API call\s+(\S+)', call_step.message)
            if path_match:
                api_path = path_match.group(1)
                diagnosis.evidence.append(f"Playwright: API path that failed: {api_path}")
                break


def _verify_product_accessible(page, sdp_url, portal, diagnosis):
    """Generic check — just verify the product is up."""
    try:
        home_url = f"{sdp_url}/app/{portal}/HomePage.do"
        page.goto(home_url, wait_until="domcontentloaded", timeout=30000)
        title = page.title()
        diagnosis.evidence.append(f"Playwright: Product accessible, page title: {title}")
    except Exception as e:
        diagnosis.evidence.append(f"Playwright: Product unreachable: {str(e)[:150]}")
        if diagnosis.root_cause == RootCause.UNDETERMINED.value:
            diagnosis.root_cause = RootCause.ENVIRONMENT.value
            diagnosis.confidence = "HIGH"
            diagnosis.summary = "Product is unreachable — environment/infrastructure issue"


# ── Main Entry Point ──────────────────────────────────────────────────────────

def diagnose_failure(
    method_name: str,
    entity_class: str,
    error_msg: str,
    reports_dir: str,
    src_dir: str,
    sdp_url: Optional[str] = None,
    admin_email: Optional[str] = None,
    admin_pass: Optional[str] = None,
    portal: Optional[str] = None,
    verify: bool = False,
) -> Diagnosis:
    """
    Full diagnosis pipeline for a single test failure.

    Args:
        method_name:  Test method name
        entity_class: Entity class name (e.g. IncidentRequest)
        error_msg:    Error message from the test failure
        reports_dir:  Path to reports/ directory
        src_dir:      Path to src/ directory
        sdp_url:      SDP product URL (needed for Playwright verification)
        admin_email:  Admin email (needed for Playwright login)
        admin_pass:   Admin password (needed for Playwright login)
        portal:       Portal name (needed for Playwright login)
        verify:       If True, use Playwright to verify ambiguous cases

    Returns:
        Diagnosis object with root_cause, confidence, summary, details, evidence
    """
    # Step 1: Parse ScenarioReport
    report_path = find_latest_report(method_name, reports_dir)
    report = parse_scenario_report(report_path) if report_path else None

    # Step 1b: If error_msg is empty or too generic, extract from report
    if report and (not error_msg or len(error_msg.strip()) < 10):
        if report.errors:
            # Use the first error step's full message
            error_msg = report.errors[0].message
        elif report.all_error_text:
            error_msg = report.all_error_text[:500]

    # Step 2: Read test source code
    java_path = find_test_source(entity_class, src_dir)
    method_source = extract_method_source(java_path, method_name) if java_path else None

    # If method calls a helper, try to find and read the helper too (2 levels deep)
    if method_source and java_path:
        _SKIP_METHODS = {
            "getMethodName", "getEntityId", "addSuccessReport", "addFailureReport",
            "addReport", "clearFailureMessage", "toString", "getMessage",
            "equalsIgnoreCase", "equals", "apply", "getTestCaseData",
            "getTestCaseDataUsingCaseId", "fillInputForAnEntity",
        }
        module_dir = os.path.dirname(os.path.dirname(java_path))
        _seen_helpers = set()

        def _find_helpers(src_text: str, depth: int = 0):
            """Recursively find and append helper method sources (max 2 levels)."""
            nonlocal method_source
            if depth > 1:
                return
            # Match method calls: methodName(...) — with or without arguments
            for m in re.finditer(r'\b([a-z]\w+)\s*\(', src_text):
                helper = m.group(1)
                if helper in _SKIP_METHODS or helper in _seen_helpers:
                    continue
                _seen_helpers.add(helper)
                # Search in any Java file in the module dir
                for root_d, _, files in os.walk(module_dir):
                    found = False
                    for fname in files:
                        if fname.endswith(".java"):
                            helper_source = extract_method_source(
                                os.path.join(root_d, fname), helper
                            )
                            if helper_source:
                                method_source += f"\n// --- Helper: {helper} ---\n" + helper_source
                                _find_helpers(helper_source, depth + 1)
                                found = True
                                break
                    if found:
                        break

        _find_helpers(method_source)

    # Step 3: Heuristic classification
    diagnosis = classify_failure(error_msg, report, method_source)

    # Step 4: Optional Playwright verification for ambiguous cases
    if verify and sdp_url and admin_email and admin_pass and portal:
        if diagnosis.confidence != "HIGH" or diagnosis.root_cause == RootCause.UNDETERMINED.value:
            diagnosis = verify_with_playwright(
                sdp_url, admin_email, admin_pass, portal, diagnosis, report
            )

    return diagnosis


# ── CLI ───────────────────────────────────────────────────────────────────────

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Root Cause Analyzer for test failures")
    parser.add_argument("method_name", help="Test method name to diagnose")
    parser.add_argument("--entity", default=None, help="Entity class name")
    parser.add_argument("--error", default="", help="Error message")
    parser.add_argument("--url", default=None, help="SDP URL for Playwright verification")
    parser.add_argument("--verify", action="store_true", help="Enable Playwright UI verification")
    parser.add_argument("--project", default=None, help="Project name (default: from config)")
    args = parser.parse_args()

    from config.project_config import PROJECT_NAME as _pn
    project = args.project or _pn
    project_root = os.path.join(os.path.dirname(__file__), project)
    reports_dir = os.path.join(project_root, "reports")
    src_dir = os.path.join(project_root, "src")

    # If no error specified, try to extract from latest report
    error_msg = args.error
    if not error_msg:
        rpath = find_latest_report(args.method_name, reports_dir)
        if rpath:
            rpt = parse_scenario_report(rpath)
            if rpt and rpt.errors:
                error_msg = rpt.errors[0].message

    entity = args.entity or ""
    diagnosis = diagnose_failure(
        method_name=args.method_name,
        entity_class=entity,
        error_msg=error_msg,
        reports_dir=reports_dir,
        src_dir=src_dir,
        sdp_url=args.url,
        admin_email="jaya.kumar+org1admin1t0@zohotest.com",
        admin_pass="Zoho@135",
        portal="portal1",
        verify=args.verify,
    )

    print(f"\n{'='*70}")
    print(f"  ROOT CAUSE ANALYSIS: {args.method_name}")
    print(f"  {'─'*50}")
    print(f"  Root Cause:  {diagnosis.root_cause}")
    print(f"  Confidence:  {diagnosis.confidence}")
    print(f"  Summary:     {diagnosis.summary}")
    print(f"  Playwright:  {'Yes' if diagnosis.playwright_verified else 'No'}")
    print(f"  {'─'*50}")
    print(f"  Details:")
    for line in diagnosis.details.split('\n'):
        print(f"    {line}")
    if diagnosis.evidence:
        print(f"  {'─'*50}")
        print(f"  Evidence:")
        for ev in diagnosis.evidence:
            print(f"    • {ev}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
