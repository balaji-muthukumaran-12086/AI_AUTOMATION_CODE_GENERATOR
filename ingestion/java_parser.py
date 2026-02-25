"""
java_parser.py
--------------
Parses AutomaterSelenium Java test files and AutomaterSeleniumFramework source
to extract structured metadata about:
  - @AutomaterSuite (class-level): role, owner, tags
  - @AutomaterScenario (method-level): id, group, priority, description,
    dataIds, tags, switchOn, owner, runType
  - @AutomaterCase (inline): description
  - FieldDetails declarations (Fields.java files)
  - TestCaseData declarations (DataConstants.java files)
  - Locator constants (Locators.java files)
  - Module/entity hierarchy from package path
"""

import re
import os
import json
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field, asdict


# ──────────────────────────────────────────────
# Data models
# ──────────────────────────────────────────────

@dataclass
class ScenarioMeta:
    id: str = ""
    group: str = ""
    priority: str = "MEDIUM"
    description: str = ""
    data_ids: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    switch_on: str = "AFTER_PRE_PROCESS"
    owner: str = ""
    run_type: str = "PORTAL_BASED"
    method_name: str = ""
    method_body: str = ""


@dataclass
class SuiteMeta:
    role: str = ""
    owner: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class FieldMeta:
    constant_name: str = ""
    api_name: str = ""
    data_path: str = ""
    display_name: str = ""
    field_type: str = ""
    is_mandatory: bool = False


@dataclass
class TestCaseDataMeta:
    constant_name: str = ""
    data_key: str = ""
    json_path: str = ""


@dataclass
class ParsedTestFile:
    file_path: str = ""
    package: str = ""
    class_name: str = ""
    module_path: str = ""          # e.g. modules/requests/request
    entity_name: str = ""          # e.g. request
    file_type: str = ""            # SCENARIO | FIELDS | CONSTANTS | DATA_CONSTANTS | LOCATORS | UTILS | OTHER
    suite: SuiteMeta = field(default_factory=SuiteMeta)
    scenarios: list[ScenarioMeta] = field(default_factory=list)
    fields: list[FieldMeta] = field(default_factory=list)
    test_data: list[TestCaseDataMeta] = field(default_factory=list)
    parent_class: str = ""
    raw_content: str = ""


# ──────────────────────────────────────────────
# Regex patterns
# ──────────────────────────────────────────────

# Annotation value extractors (handles multi-line annotations)
RE_SUITE = re.compile(
    r'@AutomaterSuite\s*\((.*?)\)',
    re.DOTALL
)
RE_SCENARIO = re.compile(
    r'@AutomaterScenario\s*\((.*?)\)\s*(?:public|protected|private|@Override)',
    re.DOTALL
)
RE_METHOD_AFTER_SCENARIO = re.compile(
    r'@AutomaterScenario\s*\(.*?\)\s*(?:@Override\s*)?(?:public|protected)\s+\w+\s+(\w+)\s*\(',
    re.DOTALL
)
RE_ANNOTATION_VALUE = re.compile(r'(\w+)\s*=\s*(.*?)(?=,\s*\w+\s*=|\s*\)$)', re.DOTALL)
RE_CLASS_DECL = re.compile(r'public\s+(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?')
RE_PACKAGE = re.compile(r'^package\s+([\w.]+);', re.MULTILINE)

# Fields.java: FieldDetails declarations
RE_FIELD_DETAIL = re.compile(
    r'public\s+final\s+static\s+FieldDetails\s+(\w+)\s*=\s*new\s+FieldDetails\s*\('
    r'\s*"([^"]*)"'       # api_name
    r'\s*,\s*"([^"]*)"'   # data_path
    r'\s*,\s*"([^"]*)"'   # display_name (often "")
    r'\s*,\s*([\w.]+)'    # field_type (FieldType.INPUT etc, or null)
    r'\s*,\s*(true|false)' # isMandatory
)

# DataConstants.java: TestCaseData declarations
RE_TEST_CASE_DATA = re.compile(
    r'public\s+final\s+static\s+TestCaseData\s+(\w+)\s*=\s*new\s+TestCaseData\s*\('
    r'\s*"([^"]*)"'   # data_key
    r'\s*,\s*PATH'    # references PATH constant
    r'\s*\)'
)

# String constant extraction for PATH
RE_PATH_CONST = re.compile(r'public\s+final\s+static\s+String\s+PATH\s*=\s*"([^"]*)"')


# ──────────────────────────────────────────────
# Annotation attribute parser
# ──────────────────────────────────────────────

def _parse_annotation_attrs(raw: str) -> dict:
    """Parse key=value pairs from an annotation body string."""
    result = {}
    # Normalize whitespace
    raw = re.sub(r'\s+', ' ', raw.strip())

    # Split by top-level commas (not inside braces/quotes)
    depth = 0
    in_str = False
    parts = []
    current = []
    i = 0
    while i < len(raw):
        c = raw[i]
        if c == '"' and (i == 0 or raw[i-1] != '\\'):
            in_str = not in_str
        if not in_str:
            if c in '({':
                depth += 1
            elif c in ')}':
                depth -= 1
            elif c == ',' and depth == 0:
                parts.append(''.join(current).strip())
                current = []
                i += 1
                continue
        current.append(c)
        i += 1
    if current:
        parts.append(''.join(current).strip())

    for part in parts:
        if '=' not in part:
            continue
        key, _, val = part.partition('=')
        key = key.strip()
        val = val.strip()

        # Strip string quotes
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        # Parse arrays: {"a", "b"}
        elif val.startswith('{') and val.endswith('}'):
            inner = val[1:-1]
            val = [v.strip().strip('"') for v in inner.split(',') if v.strip()]
        # Enum values: Priority.MEDIUM → "MEDIUM"
        elif '.' in val:
            val = val.split('.')[-1]

        result[key] = val

    return result


# ──────────────────────────────────────────────
# Detect file type from class name
# ──────────────────────────────────────────────

def _detect_file_type(class_name: str, content: str) -> str:
    if class_name.endswith('Fields'):
        return 'FIELDS'
    if class_name.endswith('DataConstants'):
        return 'DATA_CONSTANTS'
    if class_name.endswith('Locators'):
        return 'LOCATORS'
    if class_name.endswith('Constants') and 'TestCaseData' not in content:
        return 'CONSTANTS'
    if 'APIUtil' in class_name or 'ActionsUtil' in class_name or class_name.endswith('Utils'):
        return 'UTILS'
    if '@AutomaterScenario' in content or '@AutomaterSuite' in content:
        return 'SCENARIO'
    if 'Role' in class_name and 'extends' not in content:
        return 'ROLE'
    return 'OTHER'


# ──────────────────────────────────────────────
# Module path extractor from package
# ──────────────────────────────────────────────

def _extract_module_path(package: str) -> str:
    """
    com.zoho.automater.selenium.modules.requests.request.common
    → modules/requests/request
    """
    base = 'com.zoho.automater.selenium.'
    if package.startswith(base):
        relative = package[len(base):]
        parts = relative.split('.')
        # Drop 'common', 'utils', 'roles', etc as last segment
        skip_tails = {'common', 'utils', 'roles', 'customroles', 'incident',
                      'service', 'sitebased'}
        while parts and parts[-1] in skip_tails:
            parts.pop()
        return '/'.join(parts)
    return package.replace('.', '/')


# ──────────────────────────────────────────────
# Main file parser
# ──────────────────────────────────────────────

def parse_java_file(file_path: str) -> Optional[ParsedTestFile]:
    """Parse a single Java file and return a ParsedTestFile dataclass."""
    path = Path(file_path)
    try:
        content = path.read_text(encoding='utf-8', errors='ignore')
    except Exception:
        return None

    result = ParsedTestFile(
        file_path=str(file_path),
        raw_content=content,
    )

    # Package
    pkg_match = RE_PACKAGE.search(content)
    if pkg_match:
        result.package = pkg_match.group(1)
        result.module_path = _extract_module_path(result.package)

    # Class declaration
    cls_match = RE_CLASS_DECL.search(content)
    if cls_match:
        result.class_name = cls_match.group(1)
        result.parent_class = cls_match.group(2) or ''
    else:
        result.class_name = path.stem

    # Entity name: last meaningful segment of module_path
    parts = result.module_path.split('/')
    result.entity_name = parts[-1] if parts else result.class_name.lower()

    # File type
    result.file_type = _detect_file_type(result.class_name, content)

    # ── @AutomaterSuite ──
    suite_match = RE_SUITE.search(content)
    if suite_match:
        attrs = _parse_annotation_attrs(suite_match.group(1))
        result.suite = SuiteMeta(
            role=attrs.get('role', ''),
            owner=attrs.get('owner', ''),
            tags=attrs.get('tags', []) if isinstance(attrs.get('tags'), list) else [],
        )

    # ── @AutomaterScenario methods ──
    if result.file_type == 'SCENARIO':
        # Find all scenario annotations + their method names
        scenario_blocks = list(re.finditer(
            r'@AutomaterScenario\s*\((.*?)\)\s*(?:@Override\s*)?'
            r'(?:public|protected)\s+\w+\s+(\w+)\s*\('
            r'(.*?)\{(.*?)(?=(?:@AutomaterScenario|@AutomaterCase|@Override\s+(?:public|protected)|$))',
            content, re.DOTALL
        ))

        for m in scenario_blocks:
            attrs = _parse_annotation_attrs(m.group(1))
            method_name = m.group(2)
            method_body = m.group(4)[:2000]  # cap at 2000 chars

            scenario = ScenarioMeta(
                id=attrs.get('id', ''),
                group=attrs.get('group', ''),
                priority=attrs.get('priority', 'MEDIUM'),
                description=attrs.get('description', ''),
                data_ids=attrs.get('dataIds', []) if isinstance(attrs.get('dataIds'), list) else
                         ([attrs['dataIds']] if attrs.get('dataIds') else []),
                tags=attrs.get('tags', []) if isinstance(attrs.get('tags'), list) else [],
                switch_on=attrs.get('switchOn', 'AFTER_PRE_PROCESS'),
                owner=attrs.get('owner', result.suite.owner),
                run_type=attrs.get('runType', 'PORTAL_BASED'),
                method_name=method_name,
                method_body=method_body.strip(),
            )
            result.scenarios.append(scenario)

    # ── FieldDetails (Fields.java) ──
    if result.file_type == 'FIELDS':
        for m in RE_FIELD_DETAIL.finditer(content):
            result.fields.append(FieldMeta(
                constant_name=m.group(1),
                api_name=m.group(2),
                data_path=m.group(3),
                display_name=m.group(4),
                field_type=m.group(5).split('.')[-1] if m.group(5) != 'null' else '',
                is_mandatory=m.group(6) == 'true',
            ))

    # ── TestCaseData (DataConstants.java) ──
    if result.file_type == 'DATA_CONSTANTS':
        path_match = RE_PATH_CONST.search(content)
        json_path = path_match.group(1) if path_match else ''
        for m in RE_TEST_CASE_DATA.finditer(content):
            result.test_data.append(TestCaseDataMeta(
                constant_name=m.group(1),
                data_key=m.group(2),
                json_path=json_path,
            ))

    return result


# ──────────────────────────────────────────────
# Batch parser
# ──────────────────────────────────────────────

def parse_all_java_files(repo_root: str, progress: bool = True) -> list[ParsedTestFile]:
    """Walk the repo and parse every .java file."""
    root = Path(repo_root)
    java_files = list(root.rglob('*.java'))
    # Exclude .hg metadata (shouldn't be there but safety)
    java_files = [f for f in java_files if '.hg' not in str(f)]

    results = []
    total = len(java_files)
    for idx, jf in enumerate(java_files):
        if progress and idx % 50 == 0:
            print(f"  Parsing {idx}/{total}: {jf.name}", flush=True)
        parsed = parse_java_file(str(jf))
        if parsed:
            results.append(parsed)

    print(f"  ✅ Parsed {len(results)} Java files from {repo_root}")
    return results


def save_parsed_results(results: list[ParsedTestFile], output_path: str) -> None:
    """Serialize parsed results to JSON (excluding raw_content for size)."""
    data = []
    for r in results:
        d = asdict(r)
        d.pop('raw_content', None)  # too large for storage
        data.append(d)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  💾 Saved {len(data)} records → {output_path}")


# ──────────────────────────────────────────────
# CLI entry
# ──────────────────────────────────────────────

if __name__ == '__main__':
    import sys
    base = Path(__file__).resolve().parents[1]
    framework_root = base / 'AutomaterSeleniumFramework' / 'src'
    testcases_root = base / 'AutomaterSelenium' / 'src'

    print("📦 Parsing Framework source...")
    fw_results = parse_all_java_files(str(framework_root))
    save_parsed_results(fw_results, str(base / 'knowledge_base' / 'raw' / 'framework_parsed.json'))

    print("\n📦 Parsing Test Cases source...")
    tc_results = parse_all_java_files(str(testcases_root))
    save_parsed_results(tc_results, str(base / 'knowledge_base' / 'raw' / 'testcases_parsed.json'))

    # Quick summary
    scenarios_total = sum(len(r.scenarios) for r in tc_results)
    print(f"\n📊 Summary:")
    print(f"   Files parsed  : {len(tc_results)}")
    print(f"   Scenario methods: {scenarios_total}")
    file_types = {}
    for r in tc_results:
        file_types[r.file_type] = file_types.get(r.file_type, 0) + 1
    for ft, cnt in sorted(file_types.items()):
        print(f"   {ft:<20}: {cnt}")
