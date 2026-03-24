#!/usr/bin/env python3
"""
generate_tests_to_run.py — Build tests_to_run.json from a use-case document.

Reads a use-case CSV/XLSX/XLS from $PROJECT_NAME/Testcase/, extracts scenario IDs,
scans the project's Java source for matching @AutomaterScenario annotations,
and writes tests_to_run.json ready for `@test-runner batch`.

Usage:
    .venv/bin/python generate_tests_to_run.py                    # auto-detect document
    .venv/bin/python generate_tests_to_run.py path/to/file.csv   # explicit document
    .venv/bin/python generate_tests_to_run.py --batch-size 15    # custom batch size
"""
import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(__file__))
from config.project_config import PROJECT_NAME, PROJECT_ROOT


# ---------------------------------------------------------------------------
# 1. Read use-case document  (CSV / XLSX / XLS)
# ---------------------------------------------------------------------------

def read_csv(path: str) -> list[dict]:
    """Read CSV, return list of row dicts."""
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def read_xlsx(path: str) -> list[dict]:
    """Read XLSX/XLS using openpyxl, return list of row dicts."""
    try:
        import openpyxl
    except ImportError:
        print("ERROR: openpyxl not installed. Run: pip install openpyxl", file=sys.stderr)
        sys.exit(1)

    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = []
    for sheet in wb.worksheets:
        header = None
        for row in sheet.iter_rows(values_only=True):
            cells = [str(c).strip() if c is not None else "" for c in row]
            if header is None:
                # Detect header row by looking for "UseCase ID" column
                for i, cell in enumerate(cells):
                    if "usecase" in cell.lower() and "id" in cell.lower():
                        header = cells
                        break
                continue
            if header:
                row_dict = {}
                for i, col_name in enumerate(header):
                    row_dict[col_name] = cells[i] if i < len(cells) else ""
                rows.append(row_dict)
    wb.close()
    return rows


def read_usecase_document(path: str) -> list[dict]:
    """Read a use-case document (CSV/XLSX/XLS), return row dicts."""
    ext = Path(path).suffix.lower()
    if ext == ".csv":
        return read_csv(path)
    elif ext in (".xlsx", ".xls"):
        return read_xlsx(path)
    else:
        print(f"ERROR: Unsupported file type '{ext}'. Use .csv, .xlsx, or .xls", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# 2. Extract scenario IDs from use-case document
# ---------------------------------------------------------------------------

def _find_id_column(row: dict) -> str | None:
    """Find the column name that holds scenario IDs."""
    for col in row.keys():
        normalized = col.strip().lower().replace(" ", "").replace("_", "")
        if normalized in ("usecaseid", "testcaseid", "scenarioid", "id"):
            return col
    return None


def extract_scenario_ids(rows: list[dict]) -> list[str]:
    """Extract non-empty scenario IDs from the use-case rows.

    Filters:
     - Only rows with UI To-be-automated = 'Yes' (if column exists)
     - Skips MSP rows (IS MSP/ SDP = 'MSP')
     - Skips empty IDs and section headers
    """
    if not rows:
        return []

    id_col = _find_id_column(rows[0])
    if id_col is None:
        print("ERROR: Could not find 'UseCase ID' column in the document.", file=sys.stderr)
        print(f"  Available columns: {list(rows[0].keys())}", file=sys.stderr)
        sys.exit(1)

    # Detect optional filter columns
    ui_auto_col = None
    msp_col = None
    for col in rows[0].keys():
        col_lower = col.strip().lower()
        # Must contain "ui" AND "to-be-automated" (not "API To-be-automated")
        if "ui" in col_lower and ("to-be-automated" in col_lower or "to_be_automated" in col_lower):
            ui_auto_col = col
        if "msp" in col_lower:
            msp_col = col

    ids = []
    skipped_msp = 0
    skipped_ui_no = 0
    for row in rows:
        raw_id = row.get(id_col, "").strip()
        if not raw_id:
            continue
        # Skip section headers (no underscore, typically all-caps descriptions)
        if "_" not in raw_id and not re.match(r'^[A-Z]{2,}', raw_id):
            continue

        # Skip MSP rows
        if msp_col and row.get(msp_col, "").strip().upper() == "MSP":
            skipped_msp += 1
            continue

        # Filter UI To-be-automated = Yes
        if ui_auto_col:
            ui_val = row.get(ui_auto_col, "").strip().lower()
            if ui_val != "yes":
                skipped_ui_no += 1
                continue

        ids.append(raw_id)

    if skipped_msp:
        print(f"  Skipped {skipped_msp} MSP rows")
    if skipped_ui_no:
        print(f"  Skipped {skipped_ui_no} rows (UI To-be-automated != Yes)")
    return ids


# ---------------------------------------------------------------------------
# 3. Scan Java source for @AutomaterScenario annotations
# ---------------------------------------------------------------------------

# Regex to extract id and method name from @AutomaterScenario blocks.
# Uses a two-step approach: find annotation start, then parse ahead to handle
# descriptions containing ')' characters inside string literals.
_SCENARIO_START_RE = re.compile(r'@AutomaterScenario\s*\(', re.DOTALL)


def _find_annotation_end(content: str, open_paren_pos: int) -> int:
    """Find the matching closing ')' for an annotation, respecting string literals."""
    depth = 1
    i = open_paren_pos + 1
    length = len(content)
    while i < length and depth > 0:
        ch = content[i]
        if ch == '"':
            # Skip string literal contents
            i += 1
            while i < length and content[i] != '"':
                if content[i] == '\\':
                    i += 1  # skip escaped char
                i += 1
        elif ch == '{':
            depth += 1
        elif ch == '}':
            depth -= 1
        elif ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


_METHOD_AFTER_ANNOTATION_RE = re.compile(
    r'\s*public\s+void\s+(\w+)\s*\(', re.DOTALL
)
_ID_IN_ANNOTATION_RE = re.compile(r'id\s*=\s*"([^"]+)"')


def scan_java_sources(src_dir: str) -> dict[str, list[tuple[str, str]]]:
    """Scan all .java files under src_dir for @AutomaterScenario annotations.

    Returns: {scenario_id: [(entity_class, method_name), ...]}
    A single annotation id may be comma-separated (multi-ID grouping), so each
    sub-ID also maps to the same (entity_class, method_name).
    """
    id_map: dict[str, list[tuple[str, str]]] = {}
    src_path = Path(src_dir)

    if not src_path.exists():
        print(f"ERROR: Source directory not found: {src_dir}", file=sys.stderr)
        sys.exit(1)

    java_files = list(src_path.rglob("*.java"))
    # Exclude support files (Base, Locators, Constants, etc.)
    support_suffixes = ("Base.java", "Locators.java", "Constants.java",
                        "DataConstants.java", "AnnotationConstants.java",
                        "Fields.java", "ActionsUtil.java", "APIUtil.java",
                        "ActionUtils.java")

    scanned = 0
    for java_file in java_files:
        name = java_file.name
        if name.endswith(support_suffixes):
            continue

        entity_class = name.replace(".java", "")

        try:
            content = java_file.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        scanned += 1
        for m in _SCENARIO_START_RE.finditer(content):
            # Find the matching closing paren, handling ')' inside strings
            open_pos = m.end() - 1  # position of '('
            close_pos = _find_annotation_end(content, open_pos)
            if close_pos == -1:
                continue

            annotation_body = content[open_pos + 1:close_pos]

            # Extract id
            id_match = _ID_IN_ANNOTATION_RE.search(annotation_body)
            if not id_match:
                continue

            # Extract method name after the annotation closing paren
            after = content[close_pos + 1:]
            method_match = _METHOD_AFTER_ANNOTATION_RE.match(after)
            if not method_match:
                continue

            raw_ids = id_match.group(1)
            method_name = method_match.group(1)

            # Handle comma-separated IDs (multi-ID grouping)
            for sub_id in raw_ids.split(","):
                sub_id = sub_id.strip()
                if sub_id:
                    if sub_id not in id_map:
                        id_map[sub_id] = []
                    id_map[sub_id].append((entity_class, method_name))

    print(f"  Scanned {scanned} Java files, found {len(id_map)} unique scenario IDs")
    return id_map


# ---------------------------------------------------------------------------
# 4. Match & build tests_to_run.json
# ---------------------------------------------------------------------------

def build_tests_to_run(
    usecase_ids: list[str],
    id_map: dict[str, list[tuple[str, str]]],
    batch_size: int,
) -> dict:
    """Match use-case IDs to Java annotations and build the JSON structure.

    Batch numbers are assigned sequentially based on order of appearance
    in the use-case document, grouped by batch_size.
    """
    tests = []
    seen_methods = set()  # (entity_class, method_name) to avoid duplicates
    matched_ids = set()
    unmatched_ids = []

    for uc_id in usecase_ids:
        if uc_id in id_map:
            matched_ids.add(uc_id)
            for entity_class, method_name in id_map[uc_id]:
                key = (entity_class, method_name)
                if key not in seen_methods:
                    seen_methods.add(key)
                    tests.append({
                        "entity_class": entity_class,
                        "method_name": method_name,
                    })
        else:
            unmatched_ids.append(uc_id)

    # Assign batch numbers
    for i, test in enumerate(tests):
        test["batch"] = (i // batch_size) + 1

    total_batches = (len(tests) // batch_size) + (1 if len(tests) % batch_size else 0) if tests else 0

    return {
        "tests": tests,
        "_meta": {
            "total_tests": len(tests),
            "total_batches": total_batches,
            "matched_usecase_ids": len(matched_ids),
            "unmatched_usecase_ids": len(unmatched_ids),
        },
        "_unmatched": unmatched_ids,
    }


# ---------------------------------------------------------------------------
# 5. Auto-detect use-case document
# ---------------------------------------------------------------------------

def find_usecase_document(project_dir: str) -> str | None:
    """Find a use-case CSV/XLSX/XLS in $PROJECT_NAME/Testcase/."""
    testcase_dir = Path(project_dir) / "Testcase"
    if not testcase_dir.exists():
        return None

    candidates = []
    for ext in ("*.xlsx", "*.xls", "*.csv"):
        candidates.extend(testcase_dir.glob(ext))

    if not candidates:
        return None

    # Prefer _Usecase.csv > .xlsx > .csv (by name pattern + recency)
    # Files ending with _Usecase.csv are the canonical converted format
    usecase_csvs = [c for c in candidates if c.name.endswith("_Usecase.csv")]
    if usecase_csvs:
        return str(max(usecase_csvs, key=lambda p: p.stat().st_mtime))

    xlsx_files = [c for c in candidates if c.suffix.lower() in (".xlsx", ".xls")]
    if xlsx_files:
        return str(max(xlsx_files, key=lambda p: p.stat().st_mtime))

    csv_files = [c for c in candidates if c.suffix.lower() == ".csv"
                 and not c.name.endswith(("_Coverage_Summary.csv", "_Unmapped_Gaps.csv",
                                          "_API_Mapping.csv"))]
    if csv_files:
        return str(max(csv_files, key=lambda p: p.stat().st_mtime))

    return str(max(candidates, key=lambda p: p.stat().st_mtime))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Build tests_to_run.json from a use-case document by matching "
                    "scenario IDs to existing @AutomaterScenario annotations in Java source."
    )
    parser.add_argument(
        "document", nargs="?", default=None,
        help="Path to use-case CSV/XLSX/XLS. Auto-detected from $PROJECT_NAME/Testcase/ if omitted."
    )
    parser.add_argument(
        "--batch-size", type=int, default=15,
        help="Number of tests per batch (default: 15)"
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help="Output path for tests_to_run.json (default: $PROJECT_NAME/tests_to_run.json)"
    )
    args = parser.parse_args()

    project_dir = PROJECT_ROOT  # PROJECT_ROOT already includes PROJECT_NAME
    src_dir = os.path.join(project_dir, "src")

    # --- Resolve document path ---
    if args.document:
        doc_path = args.document
    else:
        doc_path = find_usecase_document(project_dir)
        if doc_path is None:
            print(f"ERROR: No use-case document found in {project_dir}/Testcase/", file=sys.stderr)
            print("  Place a .csv, .xlsx, or .xls file there, or pass the path explicitly.", file=sys.stderr)
            sys.exit(1)

    if not os.path.isfile(doc_path):
        print(f"ERROR: File not found: {doc_path}", file=sys.stderr)
        sys.exit(1)

    # --- Resolve output path ---
    out_path = args.output or os.path.join(project_dir, "tests_to_run.json")

    print(f"\n{'='*60}")
    print(f"  generate_tests_to_run.py")
    print(f"  Project : {PROJECT_NAME}")
    print(f"  Document: {os.path.basename(doc_path)}")
    print(f"  Source  : {src_dir}")
    print(f"  Output  : {out_path}")
    print(f"  Batch sz: {args.batch_size}")
    print(f"{'='*60}\n")

    # Step 1: Read use-case document
    print("[1/4] Reading use-case document...")
    rows = read_usecase_document(doc_path)
    print(f"  {len(rows)} rows read from {Path(doc_path).name}")

    # Step 2: Extract scenario IDs
    print("[2/4] Extracting scenario IDs...")
    usecase_ids = extract_scenario_ids(rows)
    print(f"  {len(usecase_ids)} automatable scenario IDs extracted")

    if not usecase_ids:
        print("\nNo scenario IDs found. Check the document format.", file=sys.stderr)
        sys.exit(1)

    # Step 3: Scan Java sources
    print("[3/4] Scanning Java source files...")
    id_map = scan_java_sources(src_dir)

    # Step 4: Match and build output
    print("[4/4] Matching scenario IDs to Java annotations...")
    result = build_tests_to_run(usecase_ids, id_map, args.batch_size)
    meta = result.pop("_meta")
    unmatched = result.pop("_unmatched")

    # Write output (only the "tests" array — clean schema)
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    # --- Summary ---
    print(f"\n{'='*60}")
    print(f"  RESULTS")
    print(f"{'='*60}")
    print(f"  Total tests written   : {meta['total_tests']}")
    print(f"  Total batches         : {meta['total_batches']}")
    print(f"  Matched use-case IDs  : {meta['matched_usecase_ids']}")
    print(f"  Unmatched use-case IDs: {meta['unmatched_usecase_ids']}")

    if unmatched:
        print(f"\n  Unmatched IDs ({len(unmatched)}):")
        for uid in unmatched[:20]:
            print(f"    - {uid}")
        if len(unmatched) > 20:
            print(f"    ... and {len(unmatched) - 20} more")

    # Batch breakdown
    from collections import Counter
    batch_counts = Counter(t["batch"] for t in result["tests"])
    entity_counts = Counter(t["entity_class"] for t in result["tests"])

    print(f"\n  Batch breakdown:")
    for b in sorted(batch_counts.keys()):
        print(f"    Batch {b:>2}: {batch_counts[b]} tests")

    print(f"\n  Entity classes:")
    for ec in sorted(entity_counts.keys()):
        print(f"    {ec}: {entity_counts[ec]} tests")

    print(f"\n  Output: {out_path}")
    print(f"  Run with: @test-runner batch <N>  or  .venv/bin/python run_batch.py <N>\n")


if __name__ == "__main__":
    main()
