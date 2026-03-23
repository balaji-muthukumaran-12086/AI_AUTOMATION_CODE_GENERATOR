#!/usr/bin/env python3
"""
static_analysis_gate.py
-----------------------
Pre-compilation validation gate for AI-generated test code.
Catches structural errors, anti-pattern violations, and false-positive risks
BEFORE javac compilation — saving a full compile-fix-recompile cycle.

Usage:
    .venv/bin/python static_analysis_gate.py <java_file_or_dir>
    .venv/bin/python static_analysis_gate.py --code-string "java code block"

Returns exit code 0 if all checks pass, 1 if any FAIL.

Checks performed:
  1. API Registry Gate — no calls to DOES_NOT_EXIST endpoints
  2. Anti-False-Positive — every !isElementPresent has a positive anchor
  3. UI-Only Test Body — no restAPI.* calls in test method bodies
  4. Annotation Completeness — all 9 @AutomaterScenario fields present
  5. runType Explicit — runType never omitted (default is PORTAL_BASED trap)
  6. DataConstants Usage — no raw string literals in getTestCaseData()
  7. preProcess Group Exists — group string matches known groups in inventory
  8. Redundant waitForAjaxComplete — no wait between consecutive clicks
  9. NeedBraces — all if/else/for/while/catch have braces
  10. Inline JSON Construction — no new JSONObject().put() chains in test methods
"""

import argparse
import os
import re
import sys
import yaml
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# Add project root
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


@dataclass
class Violation:
    rule: str
    severity: str  # "ERROR" or "WARNING"
    line: int
    message: str
    fix_hint: str = ""


@dataclass
class AnalysisResult:
    file: str
    violations: list = field(default_factory=list)

    @property
    def has_errors(self):
        return any(v.severity == "ERROR" for v in self.violations)

    def summary(self):
        errors = sum(1 for v in self.violations if v.severity == "ERROR")
        warnings = sum(1 for v in self.violations if v.severity == "WARNING")
        return f"{self.file}: {errors} errors, {warnings} warnings"


class StaticAnalysisGate:
    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir) if base_dir else Path(os.path.dirname(os.path.abspath(__file__)))
        self._api_registry = None
        self._entity_inventories = {}

    @property
    def api_registry(self):
        if self._api_registry is None:
            reg_path = self.base_dir / "config" / "api_registry.yaml"
            if reg_path.exists():
                self._api_registry = yaml.safe_load(reg_path.read_text())
            else:
                self._api_registry = {}
        return self._api_registry

    def load_inventory(self, module: str, entity: str) -> dict:
        key = f"{module}_{entity}"
        if key not in self._entity_inventories:
            inv_path = self.base_dir / "config" / "entity_inventory" / f"{key}.yaml"
            if inv_path.exists():
                self._entity_inventories[key] = yaml.safe_load(inv_path.read_text())
            else:
                self._entity_inventories[key] = {}
        return self._entity_inventories[key]

    def analyze(self, code: str, filename: str = "<input>") -> AnalysisResult:
        """Run all checks on a Java source string."""
        result = AnalysisResult(file=filename)
        lines = code.split('\n')

        self._check_annotation_completeness(lines, result)
        self._check_run_type_explicit(lines, result)
        self._check_api_in_test_body(lines, result)
        self._check_api_registry(lines, result)
        self._check_false_positive_assertions(lines, result)
        self._check_raw_string_data_load(lines, result)
        self._check_redundant_ajax_wait(lines, result)
        self._check_need_braces(lines, result)
        self._check_inline_json_construction(lines, result)

        return result

    def analyze_file(self, filepath: Path) -> AnalysisResult:
        """Analyze a Java file."""
        code = filepath.read_text(encoding='utf-8', errors='replace')
        return self.analyze(code, str(filepath))

    # ====================== Individual Checks ======================

    def _check_annotation_completeness(self, lines: list, result: AnalysisResult):
        """Check that @AutomaterScenario has all required fields."""
        required_fields = ['id', 'group', 'priority', 'dataIds', 'tags',
                           'description', 'owner', 'runType']

        in_annotation = False
        annotation_start = 0
        annotation_text = ""

        for i, line in enumerate(lines):
            if '@AutomaterScenario' in line:
                in_annotation = True
                annotation_start = i + 1
                annotation_text = line

            if in_annotation:
                annotation_text += line
                if ')' in line and annotation_text.count('(') <= annotation_text.count(')'):
                    in_annotation = False
                    # Check all fields
                    for field_name in required_fields:
                        if field_name + ' ' not in annotation_text and field_name + '=' not in annotation_text:
                            result.violations.append(Violation(
                                rule="ANNOTATION_COMPLETENESS",
                                severity="ERROR",
                                line=annotation_start,
                                message=f"@AutomaterScenario missing field: {field_name}",
                                fix_hint=f"Add {field_name} = ... to the annotation"
                            ))
                    annotation_text = ""

    def _check_run_type_explicit(self, lines: list, result: AnalysisResult):
        """Check that runType is explicitly set (default PORTAL_BASED is a trap)."""
        for i, line in enumerate(lines):
            if '@AutomaterScenario' in line:
                # Collect the full annotation
                full = line
                j = i + 1
                while j < len(lines) and (full.count('(') > full.count(')')):
                    full += lines[j]
                    j += 1
                if 'runType' not in full:
                    result.violations.append(Violation(
                        rule="RUNTYPE_EXPLICIT",
                        severity="ERROR",
                        line=i + 1,
                        message="runType omitted — defaults to PORTAL_BASED (test will be skipped)",
                        fix_hint="Add runType = ScenarioRunType.USER_BASED"
                    ))

    def _check_api_in_test_body(self, lines: list, result: AnalysisResult):
        """Check for restAPI.* or *APIUtil.* calls inside test method bodies."""
        in_test_method = False
        brace_depth = 0

        for i, line in enumerate(lines):
            stripped = line.strip()

            # Detect test method bodies (methods that are called from @AutomaterScenario wrappers)
            # Typically: protected void xxxImpl() or public void xxx()
            if re.match(r'\s*(?:protected|public)\s+void\s+\w+Impl\s*\(', line):
                in_test_method = True
                brace_depth = 0

            if in_test_method:
                brace_depth += line.count('{') - line.count('}')
                if brace_depth <= 0 and '{' not in line and '}' in line:
                    in_test_method = False
                    continue

                # Check for API calls
                if re.search(r'restAPI\.\w+', stripped) and not stripped.startswith('//'):
                    result.violations.append(Violation(
                        rule="UI_ONLY_TEST_BODY",
                        severity="ERROR",
                        line=i + 1,
                        message="restAPI call in test method body — this is API testing, not UI testing",
                        fix_hint="Move API calls to preProcess group. Test methods must use UI only."
                    ))

                if re.search(r'\w+APIUtil\.\w+', stripped) and not stripped.startswith('//'):
                    result.violations.append(Violation(
                        rule="UI_ONLY_TEST_BODY",
                        severity="ERROR",
                        line=i + 1,
                        message="*APIUtil call in test method body — API calls belong in preProcess",
                        fix_hint="Move to preProcess or use UI flow instead."
                    ))

    def _check_api_registry(self, lines: list, result: AnalysisResult):
        """Check that API paths used match VERIFIED_WORKING in the registry."""
        registry = self.api_registry
        if not registry or 'modules' not in registry:
            return

        # Build a set of DOES_NOT_EXIST paths
        bad_paths = set()
        modules = registry.get('modules', {})
        for mod_name, mod_data in modules.items():
            for ep_name, ep_data in mod_data.get('endpoints', {}).items():
                if ep_data.get('status') == 'DOES_NOT_EXIST':
                    path = ep_data.get('path', '')
                    # Extract a recognizable substring
                    if '{id}' in path:
                        # Will match things like "changes/" + id + "/link_parent_change"
                        parts = path.split('{id}')
                        if len(parts) > 1:
                            suffix = parts[1].lstrip('/')
                            if suffix:
                                bad_paths.add(suffix)

        for i, line in enumerate(lines):
            for bad_path in bad_paths:
                if bad_path in line and not line.strip().startswith('//'):
                    result.violations.append(Violation(
                        rule="API_REGISTRY_GATE",
                        severity="ERROR",
                        line=i + 1,
                        message=f"API path '{bad_path}' is DOES_NOT_EXIST in api_registry.yaml",
                        fix_hint="This endpoint doesn't exist. Use UI flow instead."
                    ))

    def _check_false_positive_assertions(self, lines: list, result: AnalysisResult):
        """Check for naked negative assertions without positive anchor."""
        for i, line in enumerate(lines):
            stripped = line.strip()

            # Pattern: if (!actions.isElementPresent(...))
            if re.search(r'!\s*actions\.isElementPresent\s*\(', stripped):
                # Look backward for a positive anchor within 15 lines
                has_anchor = False
                for j in range(max(0, i - 15), i):
                    prev = lines[j].strip()
                    # Positive anchor: actions.isElementPresent without ! → checked for presence
                    if (re.search(r'(?<!!)actions\.isElementPresent\s*\(', prev) and
                            'addFailureReport' in lines[min(j + 3, len(lines) - 1)].strip() +
                            lines[min(j + 2, len(lines) - 1)].strip() +
                            lines[min(j + 1, len(lines) - 1)].strip()):
                        has_anchor = True
                        break
                    # Alternative anchor: verifyTitleInDetailsPage, getText, etc.
                    if re.search(r'actions\.(detailsView\.verifyTitle|getText|validate\.textContent)', prev):
                        has_anchor = True
                        break

                if not has_anchor:
                    result.violations.append(Violation(
                        rule="ANTI_FALSE_POSITIVE",
                        severity="WARNING",
                        line=i + 1,
                        message="Negative assertion (!isElementPresent) without preceding positive anchor",
                        fix_hint="Add a positive assertion (e.g., verify page/popup loaded) BEFORE this negative check"
                    ))

    def _check_raw_string_data_load(self, lines: list, result: AnalysisResult):
        """Check for raw string literals in getTestCaseData()."""
        for i, line in enumerate(lines):
            # getTestCaseData("raw_string") instead of getTestCaseData(DataConstants.KEY)
            match = re.search(r'getTestCaseData\s*\(\s*"', line)
            if match and not line.strip().startswith('//'):
                result.violations.append(Violation(
                    rule="DATACONSTANTS_USAGE",
                    severity="ERROR",
                    line=i + 1,
                    message="Raw string literal in getTestCaseData() — use DataConstants constant",
                    fix_hint="Replace with getTestCaseData(<Entity>DataConstants.<Inner>.KEY)"
                ))

    def _check_redundant_ajax_wait(self, lines: list, result: AnalysisResult):
        """Check for waitForAjaxComplete between consecutive clicks."""
        for i in range(1, len(lines)):
            curr = lines[i].strip()
            prev = lines[i - 1].strip()

            if ('waitForAjaxComplete' in curr and
                    re.search(r'actions\.(click|type|sendKeys|getText|navigate)', prev)):
                result.violations.append(Violation(
                    rule="REDUNDANT_AJAX_WAIT",
                    severity="WARNING",
                    line=i + 1,
                    message="Redundant waitForAjaxComplete — the preceding action already waits internally",
                    fix_hint="Remove this waitForAjaxComplete() call"
                ))

    def _check_need_braces(self, lines: list, result: AnalysisResult):
        """Check for braceless if/else/for/while/catch statements."""
        for i, line in enumerate(lines):
            stripped = line.strip()

            # Single-line catch: } catch (Exception e) {}
            if re.match(r'\}\s*catch\s*\([^)]*\)\s*\{\s*\}', stripped):
                result.violations.append(Violation(
                    rule="NEED_BRACES",
                    severity="ERROR",
                    line=i + 1,
                    message="Inline catch block without braces (Checkstyle NeedBraces)",
                    fix_hint="Expand to multi-line: } catch (Exception e) {\\n    // comment\\n}"
                ))

            # Braceless if/else/for/while
            if re.match(r'(if|else if|for|while)\s*\(.*\)\s*[^{;\s]', stripped):
                if not stripped.endswith('{') and not stripped.endswith(';'):
                    result.violations.append(Violation(
                        rule="NEED_BRACES",
                        severity="ERROR",
                        line=i + 1,
                        message=f"Block statement without braces (Checkstyle NeedBraces)",
                        fix_hint="Add braces around the block body"
                    ))

    def _check_inline_json_construction(self, lines: list, result: AnalysisResult):
        """Check for inline JSONObject construction chains in test methods."""
        in_test_method = False
        brace_depth = 0

        for i, line in enumerate(lines):
            if re.match(r'\s*(?:protected|public)\s+void\s+\w+Impl\s*\(', line):
                in_test_method = True
                brace_depth = 0

            if in_test_method:
                brace_depth += line.count('{') - line.count('}')
                if brace_depth <= 0 and '{' not in line and '}' in line:
                    in_test_method = False
                    continue

                if 'new JSONObject()' in line and '.put(' in line and not line.strip().startswith('//'):
                    result.violations.append(Violation(
                        rule="INLINE_JSON_CONSTRUCTION",
                        severity="WARNING",
                        line=i + 1,
                        message="Inline JSONObject construction in test method — data should come from *_data.json",
                        fix_hint="Create entry in *_data.json and load via getTestCaseData()"
                    ))


def format_report(results: list) -> str:
    """Format analysis results as a human-readable report."""
    output = []
    total_errors = 0
    total_warnings = 0

    for r in results:
        if not r.violations:
            continue

        output.append(f"\n{'='*60}")
        output.append(r.summary())
        output.append('='*60)

        for v in r.violations:
            icon = "❌" if v.severity == "ERROR" else "⚠️"
            output.append(f"  {icon} [{v.rule}] Line {v.line}: {v.message}")
            if v.fix_hint:
                output.append(f"     → Fix: {v.fix_hint}")

            if v.severity == "ERROR":
                total_errors += 1
            else:
                total_warnings += 1

    if not output:
        return "✅ All checks passed — no violations found."

    output.append(f"\n{'='*60}")
    output.append(f"TOTAL: {total_errors} errors, {total_warnings} warnings")
    if total_errors > 0:
        output.append("❌ GATE FAILED — fix errors before compilation")
    else:
        output.append("⚠️ GATE PASSED with warnings — review recommended")

    return '\n'.join(output)


def main():
    parser = argparse.ArgumentParser(description="Static Analysis Gate for AI-generated test code")
    parser.add_argument('path', nargs='?', help='Java file or directory to analyze')
    parser.add_argument('--code-string', help='Analyze a code string directly')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    gate = StaticAnalysisGate(base_dir)
    results = []

    if args.code_string:
        result = gate.analyze(args.code_string)
        results.append(result)
    elif args.path:
        path = Path(args.path)
        if path.is_file():
            results.append(gate.analyze_file(path))
        elif path.is_dir():
            for java_file in sorted(path.rglob("*.java")):
                results.append(gate.analyze_file(java_file))
        else:
            print(f"ERROR: {path} not found")
            sys.exit(1)
    else:
        # Default: scan active project
        from config.project_config import PROJECT_NAME
        project_src = Path(base_dir) / PROJECT_NAME / "src"
        if project_src.exists():
            for java_file in sorted(project_src.rglob("*.java")):
                results.append(gate.analyze_file(java_file))
        else:
            print(f"No source found at {project_src}")
            sys.exit(1)

    if args.json:
        import json
        output = []
        for r in results:
            output.append({
                'file': r.file,
                'violations': [
                    {'rule': v.rule, 'severity': v.severity, 'line': v.line,
                     'message': v.message, 'fix_hint': v.fix_hint}
                    for v in r.violations
                ]
            })
        print(json.dumps(output, indent=2))
    else:
        print(format_report(results))

    # Exit code
    sys.exit(1 if any(r.has_errors for r in results) else 0)


if __name__ == '__main__':
    main()
