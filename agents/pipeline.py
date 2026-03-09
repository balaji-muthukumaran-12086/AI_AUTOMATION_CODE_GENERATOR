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
import time
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

# ── Orchestrator client (fire-and-forget, never blocks pipeline) ─────────────
try:
    from orchestrator.client import get_client as _get_oc
except ImportError:
    _get_oc = None  # orchestrator module not available — skip all logging


def _oc_log(event_type: str, agent: str, state: AgentState, **extra):
    """Fire an orchestrator event if available. Never raises."""
    if _get_oc is None:
        return
    try:
        oc = _get_oc()
        oc._send_async(oc._build_event(
            event_type=event_type,
            agent=agent,
            module=",".join(state.get("target_modules", []))[:200] or None,
            feature_name=(state.get("feature_description") or "")[:200] or None,
            **extra,
        ))
    except Exception:
        pass


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

    def route_after_output(state: AgentState) -> Literal["runner", "hg", "__end__"]:
        """Run the test only if run_config was provided in the initial state.
        Skip directly to END (bypassing hg) when HG is disabled and there is no runner."""
        has_run_config = bool(state.get("run_config"))
        if has_run_config:
            return "runner"
        # No runner — go to hg only when enabled; otherwise straight to END
        if HG_AGENT_ENABLED:
            return "hg"
        print("[Pipeline] run_config not provided — skipping runner and hg.")
        return "__end__"

    def route_after_ingestion(state: AgentState) -> Literal["planner", "coder"]:
        """
        If the uploaded document was a test case register (proposed_scenarios already
        populated by IngestionAgent), skip Planner + Coverage + Scout and go directly
        to CoderAgent.  Otherwise, use the normal feature-doc Planner path.
        """
        if (
            state.get("generation_mode") == "from_testcases"
            and state.get("proposed_scenarios")
        ):
            print("[Pipeline] from_testcases mode → skipping Planner / Coverage / Scout ⚡")
            return "coder"
        return "planner"

    def route_after_runner(state: AgentState) -> Literal["healer", "hg", "__end__"]:
        """Activate the healer if the test failed.
        After success (or no healer needed) go to hg only when enabled."""
        run_result = state.get("run_result", {})
        if run_result and not run_result.get("success", True):
            print("[Pipeline] Test FAILED → activating HealerAgent 🩺")
            return "healer"
        return "hg" if HG_AGENT_ENABLED else "__end__"

    def route_after_review(state: AgentState) -> Literal["coder", "output"]:
        """If there are revision requests AND we haven't hit max revisions → re-run coder."""
        revision_requests = state.get('revision_requests', [])
        revision_count    = state.get('revision_count', 0)
        max_revisions     = state.get('max_revisions', 2)

        if revision_requests and revision_count <= max_revisions:
            # Inject revision instructions into test_plan so coder knows what to fix.
            # NOTE: state mutation here WON'T persist in LangGraph — the reviewer
            # node already incremented revision_count so it IS persisted.
            updated_plan = {}
            for req in revision_requests:
                mp = req['module_path']
                existing = state['test_plan'].get(mp, [])
                if not existing:
                    existing = [{'description': 'Revise generated code', 'notes': req['fix_instructions']}]
                else:
                    for sc in existing:
                        sc['_revision_notes'] = req['fix_instructions']
                updated_plan[mp] = existing
            state['test_plan'] = updated_plan   # best-effort; coder will also read revision_requests directly
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
    graph.add_conditional_edges("ingestion", route_after_ingestion, {
        "planner": "planner",
        "coder":   "coder",   # from_testcases: bypass Planner + Coverage + Scout
    })
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
        "hg":        "hg",
        "__end__":   END,
    })
    graph.add_conditional_edges("runner", route_after_runner, {
        "healer":  "healer",
        "hg":      "hg",
        "__end__": END,
    })
    graph.add_edge("healer", "hg" if HG_AGENT_ENABLED else END)
    if HG_AGENT_ENABLED:
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
        generation_mode: "new_feature" | "gap_fill" | "regression" | "from_testcases"
            "from_testcases": uploaded document is already a QA test case register
            (Excel/CSV).  IngestionAgent extracts test cases directly into
            proposed_scenarios → Planner, Coverage, and Scout are bypassed →
            CoderAgent generates Java directly from the exact test case spec.
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
    from datetime import datetime as _dt
    _t0 = time.time()
    print(f"[Pipeline] \U0001f680 Starting pipeline at {_dt.now().strftime('%H:%M:%S')} | mode={generation_mode} | modules={target_modules}", flush=True)
    _oc_log("agent_started", "pipeline", {"feature_description": feature_description, "target_modules": target_modules or []},
            metadata={"mode": generation_mode})
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
    _elapsed = int((time.time() - _t0) * 1000)
    print(f"[Pipeline] \U0001f3c1 Pipeline complete at {_dt.now().strftime('%H:%M:%S')}", flush=True)

    # ── Log pipeline completion + individual scenario outcomes ────────────
    _oc_log("agent_completed", "pipeline", final_state, duration_ms=_elapsed,
            scenarios_count=len(final_state.get("generated_code", [])),
            metadata={"files": len(final_state.get("final_output_paths", []))})

    # Log each generated scenario
    for sc in final_state.get("generated_code", []):
        _oc_log("scenario_generated", "coder", final_state,
                entity=sc.get("entity_class"),
                scenario_id=sc.get("scenario_id"),
                method_name=sc.get("method_name"))

    # Log runner result if present
    rr = final_state.get("run_result", {})
    if rr:
        evt = "scenario_passed" if rr.get("success") else "scenario_failed"
        _oc_log(evt, "runner", final_state,
                scenario_id=rr.get("scenario_id"),
                method_name=rr.get("method_name"),
                error_message=rr.get("error", "")[:500] if not rr.get("success") else None)

    # Log heal result if present
    hr = final_state.get("heal_result", {})
    if hr.get("healed"):
        _oc_log("scenario_healed", "healer", final_state,
                method_name=rr.get("method_name"),
                metadata={"iterations": hr.get("iterations")})

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
