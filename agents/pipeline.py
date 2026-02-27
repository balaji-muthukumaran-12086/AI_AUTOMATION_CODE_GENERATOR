"""
pipeline.py
-----------
LangGraph pipeline: wires all agents into the agentic test generation workflow.

Flow:
  planner → coverage → scout → coder → reviewer → [revise?] → output

                ┌────────────────────────────────────────────────────────────┐
   feature ──→  │  Planner → Coverage → Scout → Coder → Reviewer            │
   description  │                         ↑        ↑         │              │
                │                    (UI surf)  (revise)   approved          │
                │                    Playwright    └─────────┘               │
                │                                      ↓                     │
                │                                 Output Agent               │
                └────────────────────────────────────────────────────────────┘

Scout = UIScoutAgent: opens a real Playwright browser, navigates the live SDP
instance, captures visible buttons/fields/checkbox state changes BEFORE the
Coder Agent generates any Java code. This prevents the LLM from making wrong
assumptions about UI behaviour (e.g. which submit buttons exist before/after
a checkbox is ticked).
"""

import os
from pathlib import Path
from typing import Literal

from langgraph.graph import StateGraph, END

from agents.state import AgentState
from agents.ingestion_agent import IngestionAgent
from agents.planner_agent import PlannerAgent
from agents.coverage_agent import CoverageAgent
from agents.coder_agent import CoderAgent
from agents.reviewer_agent import ReviewerAgent
from agents.output_agent import OutputAgent
from agents.runner_agent import RunnerAgent
from agents.healer_agent import HealerAgent
from agents.hg_agent import HgAgent
from agents.ui_scout_agent import UIScoutAgent
from agents.parallel_runner_agent import ParallelRunnerAgent
from agents.learning_agent import LearningAgent
from knowledge_base.vector_store import VectorStore
from knowledge_base.context_builder import ContextBuilder
from config.project_config import PROJECT_NAME, BASE_DIR, DEPS_DIR, HG_AGENT_ENABLED


def build_pipeline(base_dir: str = None) -> StateGraph:
    base = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]

    # Shared resources
    store = VectorStore(persist_dir=str(base / 'knowledge_base' / 'chroma_db'))
    ctx = ContextBuilder(str(base))

    # Agents
    ingestion = IngestionAgent(base_dir=str(base))
    planner   = PlannerAgent(base_dir=str(base))
    coverage  = CoverageAgent(vector_store=store, base_dir=str(base))
    coder     = CoderAgent(context_builder=ctx, vector_store=store, base_dir=str(base))
    reviewer  = ReviewerAgent(base_dir=str(base))
    output    = OutputAgent(base_dir=str(base))
    runner    = RunnerAgent(
                    base_dir=str(base),
                    deps_dir=DEPS_DIR,
                    pre_compiled_bin_dir=str(Path(BASE_DIR) / PROJECT_NAME / 'bin'),
                )
    healer    = HealerAgent(
                    base_dir=str(base),
                    deps_dir=DEPS_DIR,
                    pre_compiled_bin_dir=str(Path(BASE_DIR) / PROJECT_NAME / 'bin'),
                    headless=True,
                )
    scout     = UIScoutAgent(
                    base_dir=str(base),
                    headless=True,
                )
    hg        = HgAgent(base_dir=str(base))

    # ── Routing logic ───────────────────────────────────────

    def route_after_output(state: AgentState) -> Literal["runner", "__end__"]:
        """Run the test only if run_config was provided in the initial state."""
        return "runner" if state.get("run_config") else "__end__"

    def route_after_runner(state: AgentState) -> Literal["healer", "__end__"]:
        """Activate the healer if the test failed, otherwise end."""
        run_result = state.get("run_result", {})
        if run_result and not run_result.get("success", True):
            print("[Pipeline] Test FAILED → activating HealerAgent 🩺")
            return "healer"
        return "__end__"

    def route_after_review(state: AgentState) -> Literal["coder", "output"]:
        """If there are revision requests AND we haven't hit max revisions → re-run coder."""
        revision_requests = state.get('revision_requests', [])
        revision_count    = state.get('revision_count', 0)
        max_revisions     = state.get('max_revisions', 2)

        if revision_requests and revision_count < max_revisions:
            # Inject revision instructions into test_plan and re-run coder
            updated_plan = {}
            for req in revision_requests:
                mp = req['module_path']
                # Re-queue scenarios from revision request
                existing = state['test_plan'].get(mp, [])
                if not existing:
                    # Build a placeholder
                    existing = [{'description': 'Revise generated code', 'notes': req['fix_instructions']}]
                else:
                    for sc in existing:
                        sc['_revision_notes'] = req['fix_instructions']
                updated_plan[mp] = existing

            state['test_plan'] = updated_plan
            state['revision_count'] = revision_count + 1
            return "coder"
        return "output"

    # ── Graph definition ────────────────────────────────────

    graph = StateGraph(AgentState)

    graph.add_node("ingestion", ingestion.run)
    graph.add_node("planner",   planner.run)
    graph.add_node("coverage",  coverage.run)
    graph.add_node("scout",    scout.run)     # proactive UI observer — runs before coder
    graph.add_node("coder",    coder.run)
    graph.add_node("reviewer", reviewer.run)
    graph.add_node("output",   output.run)
    graph.add_node("runner",   runner.run)
    graph.add_node("healer",   healer.run)
    graph.add_node("hg",       hg.run)

    graph.set_entry_point("ingestion")
    graph.add_edge("ingestion", "planner")
    graph.add_edge("planner",   "coverage")
    graph.add_edge("coverage", "scout")       # scout surfs the UI first
    graph.add_edge("scout",    "coder")       # then coder generates code with live UI context
    graph.add_edge("coder",    "reviewer")
    graph.add_conditional_edges("reviewer", route_after_review, {
        "coder":  "coder",
        "output": "output",
    })
    graph.add_conditional_edges("output", route_after_output, {
        "runner":    "runner",
        "__end__":   "hg",
    })
    graph.add_conditional_edges("runner", route_after_runner, {
        "healer":  "healer",
        "__end__": "hg",
    })
    graph.add_edge("healer", "hg")
    graph.add_edge("hg", END)

    return graph.compile()


# ──────────────────────────────────────────────────────────────────────────────
# Learning pipeline  (parallel execution → learn → hands-free heal loop)
# ──────────────────────────────────────────────────────────────────────────────

def build_learning_pipeline(base_dir: str = None) -> StateGraph:
    """
    Standalone pipeline for the parallel execution + learning cycle.

    Flow:
        parallel_runner  → load tests_to_run.json, run N JVMs in parallel
            ↓
        learning         → LLM extracts rules/patterns, updates knowledge files,
                           hands-free heal → re-run loop (up to LEARNING_RETRIES)
    """
    base = Path(base_dir) if base_dir else Path(BASE_DIR)

    parallel_runner = ParallelRunnerAgent(base_dir=str(base), deps_dir=DEPS_DIR)
    learner         = LearningAgent(base_dir=str(base), deps_dir=DEPS_DIR)

    graph = StateGraph(AgentState)
    graph.add_node("parallel_runner", parallel_runner.run)
    graph.add_node("learning",        learner.run)

    graph.set_entry_point("parallel_runner")
    graph.add_edge("parallel_runner", "learning")
    graph.add_edge("learning", END)

    return graph.compile()


def run_learning_pipeline(
    base_dir: str = None,
    tests_override: list[dict] = None,
) -> AgentState:
    """
    Entry point to run the parallel-execution + learning cycle.

    Args:
        base_dir       : Root of the ai-automation-qa workspace (defaults to BASE_DIR)
        tests_override : Optional list of run_config dicts; if None, reads tests_to_run.json

    Returns:
        Final AgentState with batch_run_results and learnings
    """
    pipeline = build_learning_pipeline(base_dir)
    initial_state = _build_initial_state()
    if tests_override:
        initial_state["batch_run_configs"] = tests_override
    final_state = pipeline.invoke(initial_state)
    return final_state


def run_pipeline(
    feature_description: str = "",
    target_modules: list[str] = None,
    generation_mode: str = "new_feature",
    base_dir: str = None,
    run_config: dict = None,
    source_document: str = "",
    hg_config: dict = None,
) -> AgentState:
    """
    Main entry point to run the agentic test generation pipeline.

    Args:
        feature_description: User story or feature description text
        target_modules: Optional list of module paths to focus on
        generation_mode: "new_feature" | "gap_fill" | "regression"
        base_dir: Root of the ai-automation-qa workspace
        run_config: Optional dict to trigger RunnerAgent after code generation.
            Example::

                run_config = {
                    "entity_class": "Solution",
                    "method_name":  "createAndShareApprovedPublicSolutionFromDV",
                    "url":          "http://sdpod-auto1:8080/",
                    "email_id":     "jaya.kumar+automation39@zohotest.com",
                    "portal_name":  "org2portal20",
                    "skip_compile": False,
                }

    Returns:
        Final AgentState with generated_code, final_output_paths, and run_result
    """
    pipeline = build_pipeline(base_dir)
    initial_state = _build_initial_state(
        feature_description=feature_description,
        source_document=source_document,
        target_modules=target_modules,
        generation_mode=generation_mode,
        run_config=run_config,
        hg_config=hg_config,
    )
    final_state = pipeline.invoke(initial_state)
    return final_state


def _build_initial_state(
    feature_description: str = "",
    source_document: str = "",
    target_modules: list[str] = None,
    generation_mode: str = "new_feature",
    run_config: dict = None,
    hg_config: dict = None,
) -> AgentState:
    """Build the initial state dict for a pipeline run (reusable by the web server)."""
    return {
        'feature_description': feature_description,
        'source_document':     source_document,
        'document_metadata':   {},
        'target_modules': target_modules or [],
        'generation_mode': generation_mode,
        'test_plan': {},
        'affected_modules': [],
        'coverage_gaps': [],
        'duplicate_warnings': [],
        'proposed_scenarios': [],
        'generated_code': [],
        'review_results': [],
        'revision_requests': [],
        'revision_count': 0,
        'max_revisions': 2,
        'errors': [],
        'final_output_paths': [],
        'messages': [],
        'run_config': run_config or {},
        'run_result': {},
        'hg_config':  (hg_config or {}) if HG_AGENT_ENABLED else {},
        'hg_result':  {},
        # Agent-written fields — must be initialized for LangGraph state completeness
        'generation_instructions': [],
        'generated_dir': '',
        'ui_observations': {},
        'heal_result': {},
        # Parallel runner + learning (Phase 8)
        'batch_run_configs':  [],
        'batch_run_results':  [],
        'learnings':          [],
        'learning_iteration': 0,
    }
