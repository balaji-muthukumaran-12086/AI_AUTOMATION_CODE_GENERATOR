#!/usr/bin/env python3
"""
main.py
-------
CLI entrypoint for the AI Test Generation Agent.

Commands:
  ingest     - Parse repos and build the knowledge base
  index      - Build/update the vector store
  report     - Generate coverage report
  generate   - Generate test cases for a feature description
  pipeline   - Run the full agentic pipeline
"""

import sys
import os
import argparse
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

# Load .env
load_dotenv(Path(__file__).parent / '.env')

console = Console()
BASE_DIR = str(Path(__file__).resolve().parent)


def cmd_ingest(args):
    """Step 1: Parse Java repos → raw JSON knowledge base."""
    console.rule("[bold blue]Step 1: Ingestion")
    from ingestion.run_ingestion import main as run_ingestion
    run_ingestion()


def cmd_index(args):
    """Step 2: Build ChromaDB vector store from ingested data."""
    console.rule("[bold blue]Step 2: Vector Index")
    from knowledge_base.vector_store import VectorStore
    base = Path(BASE_DIR)
    kb_raw = base / 'knowledge_base' / 'raw'

    if not (kb_raw / 'scenarios_flat.json').exists():
        console.print("[red]❌ Run 'ingest' first to generate scenarios_flat.json")
        sys.exit(1)

    store = VectorStore(persist_dir=str(base / 'knowledge_base' / 'chroma_db'))
    count = store.build_from_flat_list(str(kb_raw / 'scenarios_flat.json'), reset=args.reset)
    store.build_module_summaries(str(kb_raw / 'module_index.json'))
    console.print(f"[green]✅ Indexed {count} new scenarios. Total: {store.scenario_count}")


def cmd_report(args):
    """Step 3: Generate coverage heatmap report."""
    console.rule("[bold blue]Step 3: Coverage Report")
    from evaluation.coverage_report import generate_coverage_report
    base = Path(BASE_DIR)
    report = generate_coverage_report(
        str(base / 'knowledge_base' / 'raw' / 'module_index.json'),
        str(base / 'evaluation'),
    )
    console.print(f"\n[bold]📊 Coverage Summary:")
    s = report['summary']
    console.print(f"  Modules:     {report['total_modules']}")
    console.print(f"  Scenarios:   {report['total_scenarios']}")
    console.print(f"  Avg/module:  {s['avg_scenarios_per_module']:.1f}")
    console.print(f"  [red]Critical gaps: {s['critical_gaps']}")
    console.print(f"  [yellow]High gaps:     {s['high_gaps']}")
    console.print(f"\n  Report: evaluation/coverage_report.html")


def cmd_search(args):
    """Search the knowledge base for similar test scenarios."""
    from knowledge_base.vector_store import VectorStore
    store = VectorStore(persist_dir=str(Path(BASE_DIR) / 'knowledge_base' / 'chroma_db'))

    if store.scenario_count == 0:
        console.print("[red]❌ Run 'ingest' and 'index' first.")
        sys.exit(1)

    console.print(f"\n🔍 Searching: '{args.query}'\n")
    results = store.search_scenarios(args.query, top_k=args.top_k)

    table = Table(title="Similar Test Cases")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Module", style="green")
    table.add_column("Method", style="yellow")
    table.add_column("Description")
    table.add_column("Score", style="magenta")

    for r in results:
        m = r['metadata']
        table.add_row(
            r['id'][:30],
            m.get('module_path', '')[:35],
            m.get('method_name', ''),
            m.get('description', '')[:60],
            f"{(1-r['distance']):.3f}",
        )
    console.print(table)


def cmd_generate(args):
    """Run the full agentic pipeline to generate test cases."""
    console.rule("[bold green]🤖 AI Test Generator Pipeline")

    # Only require OpenAI key when actually using OpenAI as provider
    provider = os.environ.get('LLM_PROVIDER', 'ollama').lower()
    if provider == 'openai' and not os.environ.get('OPENAI_API_KEY'):
        console.print("[red]❌ OPENAI_API_KEY not set. Required when LLM_PROVIDER=openai.")
        sys.exit(1)

    from agents.pipeline import run_pipeline

    feature_description = args.feature
    if args.file:
        feature_description = Path(args.file).read_text(encoding='utf-8')

    source_document = args.doc or ""

    if not feature_description and not source_document:
        console.print("[red]❌ Provide --feature 'description', --file path.txt, or --doc path/to/document.pdf")
        sys.exit(1)

    modules = args.modules.split(',') if args.modules else []

    doc_label = Path(source_document).name if source_document else "(none)"
    console.print(Panel(
        f"[bold]Feature:[/bold] {(feature_description or '(from document)')[:300]}\n"
        f"[bold]Document:[/bold] {doc_label}\n"
        f"[bold]Entity / Modules:[/bold] {', '.join(modules) if modules else 'Auto-detect'}\n"
        f"[bold]LLM Provider:[/bold] {provider}\n"
        f"[bold]Mode:[/bold] {args.mode}",
        title="🚀 Generation Request",
        border_style="green",
    ))

    status_msg = (
        "[bold green]Running agentic pipeline (Ingestion → Planner → Coverage → Coder → Reviewer → Output)..."
        if source_document
        else "[bold green]Running agentic pipeline (Planner → Coverage → Coder → Reviewer → Output)..."
    )
    with console.status(status_msg):
        final_state = run_pipeline(
            feature_description=feature_description,
            target_modules=modules,
            generation_mode=args.mode,
            base_dir=BASE_DIR,
            source_document=source_document,
        )

    # ── Pipeline log ────────────────────────────────────────────────────────
    console.rule("Pipeline Log")
    for msg in final_state.get('messages', []):
        icon = "✅" if "✅" in msg else ("❌" if "error" in msg.lower() else "  ")
        console.print(f"  {icon} {msg}")

    # ── Errors ───────────────────────────────────────────────────────────────
    if final_state.get('errors'):
        console.rule("[red]Errors")
        for err in final_state['errors']:
            console.print(f"  [red]❌ {err}")

    # ── Generated files + copy-paste instructions ────────────────────────────
    output_paths = final_state.get('final_output_paths', [])
    instructions = final_state.get('generation_instructions', [])

    if output_paths:
        console.rule("[bold green]📋 Copy-Paste Instructions")
        if instructions:
            # Print the WHAT_TO_DO instructions directly in the terminal
            for line in instructions:
                console.print(f"  {line}")
        else:
            for p in output_paths:
                console.print(f"  📄 {p}")

        # Always print the generated directory for easy navigation
        generated_dir = final_state.get('generated_dir', '')
        if generated_dir:
            console.print(f"\n  [bold cyan]📁 All snippet files in:[/bold cyan] {generated_dir}")
    else:
        console.print("[yellow]⚠️  No files generated — check errors above or all scenarios are duplicates")

    # ── Coverage summary ─────────────────────────────────────────────────────
    gaps = final_state.get('coverage_gaps', [])
    dups = final_state.get('duplicate_warnings', [])
    console.print(f"\n📊 Coverage: [green]{len(gaps)} new scenario(s)[/green] | [yellow]{len(dups)} duplicate(s) skipped[/yellow]")


def cmd_setup(args):
    """Full setup: ingest → index → report (run once after cloning)."""
    console.rule("[bold magenta]🚀 Full Setup")
    cmd_ingest(args)
    cmd_index(args)
    cmd_report(args)
    console.print("\n[bold green]✅ Setup complete! Run 'python main.py generate --feature ...' to generate tests.")


# ── CLI parser ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        prog='ai-test-generator',
        description='AI-powered test case generator for AutomaterSelenium',
    )
    sub = parser.add_subparsers(dest='command', required=True)

    # setup
    sub.add_parser('setup', help='Full setup: ingest + index + report')

    # ingest
    sub.add_parser('ingest', help='Parse Java repos and build raw knowledge base')

    # index
    p_index = sub.add_parser('index', help='Build/update ChromaDB vector store')
    p_index.add_argument('--reset', action='store_true', help='Clear and rebuild index')

    # report
    sub.add_parser('report', help='Generate coverage heatmap HTML report')

    # search
    p_search = sub.add_parser('search', help='Search similar test scenarios')
    p_search.add_argument('query', help='Search query')
    p_search.add_argument('--top-k', type=int, default=10)

    # generate
    p_gen = sub.add_parser('generate', help='Generate test cases for a feature')
    p_gen.add_argument('--feature', '-f', type=str, help='Feature description text')
    p_gen.add_argument('--file', type=str, help='Path to feature description file (.txt/.md)')
    p_gen.add_argument('--doc', type=str, default='',
                       help='Path to a document file to ingest (PDF, DOCX, XLSX, PPTX, TXT). '
                            'The Ingestion Agent will extract and structure the content automatically.')
    p_gen.add_argument('--modules', '-m', type=str,
                       help='Comma-separated module paths to focus on')
    p_gen.add_argument('--mode', choices=['new_feature', 'gap_fill', 'regression'],
                       default='new_feature')

    args = parser.parse_args()

    commands = {
        'setup':    cmd_setup,
        'ingest':   cmd_ingest,
        'index':    cmd_index,
        'report':   cmd_report,
        'search':   cmd_search,
        'generate': cmd_generate,
    }
    commands[args.command](args)


if __name__ == '__main__':
    main()
