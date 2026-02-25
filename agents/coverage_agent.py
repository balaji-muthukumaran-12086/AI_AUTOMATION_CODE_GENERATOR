"""
coverage_agent.py
-----------------
Coverage Agent: Runs BEFORE code generation to:
  1. Check each planned scenario against the existing knowledge base
  2. Flag potential duplicates (semantic similarity > threshold)
  3. Identify genuine coverage gaps (scenarios NOT yet covered)
  4. Filter the test_plan to remove true duplicates

This ensures we don't regenerate 30,000 existing test cases and
instead focus on gaps and new feature scenarios.
"""

import os
from pathlib import Path
from typing import Any

from agents.state import AgentState
from knowledge_base.vector_store import VectorStore


DUPLICATE_THRESHOLD = 0.92   # cosine similarity >= this → likely duplicate
GAP_THRESHOLD       = 0.70   # cosine similarity < this  → genuine new scenario


class CoverageAgent:

    def __init__(self, vector_store: VectorStore = None, base_dir: str = None):
        self.base = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self.store = vector_store or VectorStore(
            persist_dir=str(self.base / 'knowledge_base' / 'chroma_db')
        )

    def _check_scenario(self, description: str, module_path: str) -> dict:
        """
        Returns:
          { status: 'duplicate'|'similar'|'new', similar: [...], score: float }
        """
        if self.store.scenario_count == 0:
            return {'status': 'new', 'similar': [], 'score': 0.0}

        results = self.store.search_scenarios(description, top_k=3, module_filter=module_path)
        if not results:
            # try without module filter
            results = self.store.search_scenarios(description, top_k=3)

        if not results:
            return {'status': 'new', 'similar': [], 'score': 0.0}

        best = results[0]
        similarity = 1 - best['distance']

        if similarity >= DUPLICATE_THRESHOLD:
            return {
                'status': 'duplicate',
                'similar': results[:3],
                'score': similarity,
            }
        elif similarity >= GAP_THRESHOLD:
            return {
                'status': 'similar',
                'similar': results[:3],
                'score': similarity,
            }
        else:
            return {
                'status': 'new',
                'similar': results[:3],
                'score': similarity,
            }

    def run(self, state: AgentState) -> AgentState:
        """LangGraph node function."""
        test_plan = state.get('test_plan', {})
        state['messages'] = state.get('messages', []) + [
            "[CoverageAgent] Checking for duplicates and coverage gaps..."
        ]

        coverage_gaps   = []
        duplicate_warnings = []
        filtered_plan   = {}

        total_planned  = 0
        total_new      = 0
        total_similar  = 0
        total_dup      = 0

        for module_path, scenarios in test_plan.items():
            filtered_plan[module_path] = []

            for sc in scenarios:
                total_planned += 1
                desc = sc.get('description', '')
                check = self._check_scenario(desc, module_path)

                if check['status'] == 'duplicate':
                    total_dup += 1
                    duplicate_warnings.append({
                        'module': module_path,
                        'proposed_description': desc,
                        'similar_existing': [
                            {
                                'id': r['metadata'].get('id', ''),
                                'description': r['metadata'].get('description', ''),
                                'method': r['metadata'].get('method_name', ''),
                                'similarity': f"{(1 - r['distance']):.2f}",
                            }
                            for r in check['similar']
                        ],
                        'action': 'SKIPPED',
                    })
                elif check['status'] == 'similar':
                    total_similar += 1
                    # Keep but tag as variation
                    sc['_coverage_note'] = (
                        f"Similar to existing (score={check['score']:.2f}): "
                        + check['similar'][0]['metadata'].get('description', '')[:80]
                        if check['similar'] else ''
                    )
                    filtered_plan[module_path].append(sc)
                    coverage_gaps.append({
                        'module': module_path,
                        'description': desc,
                        'reason': f"Similar but distinct variation (score={check['score']:.2f})",
                    })
                else:
                    total_new += 1
                    filtered_plan[module_path].append(sc)
                    coverage_gaps.append({
                        'module': module_path,
                        'description': desc,
                        'reason': 'Genuine new scenario',
                    })

        state['test_plan'] = filtered_plan
        state['coverage_gaps'] = coverage_gaps
        state['duplicate_warnings'] = duplicate_warnings
        state['messages'] = state.get('messages', []) + [
            f"[CoverageAgent] Total: {total_planned} | "
            f"New: {total_new} | Similar: {total_similar} | Duplicates skipped: {total_dup}"
        ]

        return state
