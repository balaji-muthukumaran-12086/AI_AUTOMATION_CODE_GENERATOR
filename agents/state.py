"""
state.py
--------
Shared LangGraph state for the agentic test generation pipeline.
All agents read from and write to this typed state dict.
"""

from typing import TypedDict, Optional, Annotated
import operator


class AgentState(TypedDict):
    # ── Input ─────────────────────────────────────────────
    feature_description: str          # Raw feature/user story input
    target_modules: list[str]         # Resolved module paths (e.g. ["requests/request"])
    generation_mode: str              # "new_feature" | "gap_fill" | "regression"

    # ── Planner Agent output ───────────────────────────────
    test_plan: dict                   # { module_path: [ scenario_description, ... ] }
    affected_modules: list[str]

    # ── Coverage Agent output ──────────────────────────────
    coverage_gaps: list[dict]         # [{ module, description, reason }]
    duplicate_warnings: list[dict]    # [{ proposed_desc, similar_existing }]

    # ── Scenario Agent output ─────────────────────────────
    proposed_scenarios: list[dict]    # [{ module, method_name, description, group, ... }]

    # ── Coder Agent output ────────────────────────────────
    generated_code: Annotated[list[dict], operator.add]  # [{ module, class_name, code }]

    # ── Reviewer Agent output ─────────────────────────────
    review_results: list[dict]        # [{ code_ref, issues, approved }]
    revision_requests: list[dict]     # [{ code_ref, fix_instructions }]

    # ── Control flow ──────────────────────────────────────
    revision_count: int               # How many review/revise cycles have run
    max_revisions: int                # Cap on revision cycles (default: 2)
    errors: Annotated[list[str], operator.add]
    final_output_paths: list[str]     # Paths to written .java files
    generation_instructions: list[str]  # Terminal-printable copy-paste instructions
    generated_dir: str                   # Path to the timestamped run directory
    messages: Annotated[list[str], operator.add]  # Audit log

    # ── Runner Agent ──────────────────────────────────────
    run_config: dict                  # { entity_class, method_name, url, email_id, portal_name, skip_compile }
    run_result: dict                  # RunResult.to_dict() — populated after execution

    # ── UI Scout Agent ────────────────────────────────────
    ui_observations: dict             # { module_path: [UIObservation.to_dict()] } — live UI behaviour observed before code gen

    # ── Healer Agent ──────────────────────────────────────
    heal_result: dict                 # HealResult.to_dict() — populated when test fails and healer activates
