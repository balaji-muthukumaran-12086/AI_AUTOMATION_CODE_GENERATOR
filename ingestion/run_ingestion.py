"""
run_ingestion.py
----------------
Master ingestion runner.  Run this once (or after pulling new test cases)
to rebuild the entire knowledge base from scratch.

Usage:
    python ingestion/run_ingestion.py
"""

import sys
import time
from pathlib import Path

# Allow running from repo root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from ingestion.java_parser import parse_all_java_files, save_parsed_results
from ingestion.module_indexer import build_module_index, build_scenario_flat_list


def main():
    base = Path(__file__).resolve().parents[1]
    kb_raw = base / 'knowledge_base' / 'raw'
    kb_raw.mkdir(parents=True, exist_ok=True)

    t0 = time.time()

    # ── Step 1: Parse Framework source ──
    print("\n🔍 Step 1: Parsing AutomaterSeleniumFramework...")
    fw_root = base / 'AutomaterSeleniumFramework' / 'src'
    fw_results = parse_all_java_files(str(fw_root))
    save_parsed_results(fw_results, str(kb_raw / 'framework_parsed.json'))

    # ── Step 2: Parse Test Cases source ──
    print("\n🔍 Step 2: Parsing AutomaterSelenium test cases...")
    tc_root = base / 'AutomaterSelenium' / 'src'
    tc_results = parse_all_java_files(str(tc_root))
    save_parsed_results(tc_results, str(kb_raw / 'testcases_parsed.json'))

    # ── Step 3: Build module index ──
    print("\n🗂  Step 3: Building module index...")
    module_index = build_module_index(
        str(kb_raw / 'testcases_parsed.json'),
        str(kb_raw / 'module_index.json')
    )

    # ── Step 4: Build flat scenario list ──
    print("\n📋 Step 4: Building flat scenario list for embeddings...")
    build_scenario_flat_list(module_index, str(kb_raw / 'scenarios_flat.json'))

    elapsed = time.time() - t0
    print(f"\n✅ Ingestion complete in {elapsed:.1f}s")
    print(f"   Outputs in: {kb_raw}")


if __name__ == '__main__':
    main()
