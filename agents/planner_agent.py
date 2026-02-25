"""
planner_agent.py
----------------
Planner Agent: The entry point of the agentic pipeline.

Responsibilities:
  1. Parse the feature_description (user story / feature doc text)
  2. Map it to affected AutomaterSelenium modules using module_taxonomy
  3. Identify test types needed: CRUD, validation, edge cases, roles, etc.
  4. Output a structured test_plan dict consumed by downstream agents

LLM role: Understands ITSM feature language, maps to module taxonomy,
          generates structured test plans.
"""

import json
import yaml
import os
from pathlib import Path
from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage

from agents.state import AgentState
from agents.llm_factory import get_llm


SYSTEM_PROMPT = """You are a senior QA architect for Zoho ServiceDesk Plus (SDP),
an enterprise ITSM application. You understand:
- ITIL practices (Incidents, Problems, Changes, Releases, Assets, CMDB)
- The AutomaterSelenium test framework (Java, @AutomaterSuite/@AutomaterScenario)
- All module paths in the application

Given a feature description or user story, your job is to:
1. Identify which SDP modules/entities are affected
2. Break down the feature into testable scenarios grouped by module
3. Categorize scenarios by type: CREATE, READ, UPDATE, DELETE, VALIDATE,
   ROLE_BASED, NEGATIVE, EDGE_CASE, DATA_DRIVEN, INTEGRATION

Respond ONLY with a valid JSON object in this exact format:
{
  "affected_modules": ["module/path1", "module/path2"],
  "test_plan": {
    "module/path1": [
      {
        "description": "Create a request with mandatory fields",
        "type": "CREATE",
        "group": "create",
        "priority": "HIGH",
        "run_type": "USER_BASED",
        "data_ids": ["IR_Valid_Input"],
        "tags": ["SMOKE"],
        "notes": "Validate subject appears in details view after creation"
      }
    ]
  },
  "reasoning": "Brief explanation of why these modules were selected"
}"""


class PlannerAgent:

    def __init__(self, llm: Any = None, base_dir: str = None):
        self.base = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self.llm = llm or get_llm(
            temperature=0.2,
        )

        # Load taxonomy for context injection
        taxonomy_path = self.base / 'config' / 'module_taxonomy.yaml'
        with open(taxonomy_path) as f:
            self.taxonomy = yaml.safe_load(f)

    def _build_user_prompt(self, feature_description: str, target_modules: list[str]) -> str:
        parts = [f"Feature Description:\n{feature_description}\n"]

        if target_modules:
            parts.append(f"Hint - focus on these modules: {', '.join(target_modules)}\n")

        # Inject module taxonomy as context
        module_list = []
        for top_mod, mod_def in self.taxonomy.get('top_level_modules', {}).items():
            entities = mod_def.get('entities', [])
            module_list.append(f"  {top_mod}: {', '.join(entities)}")

        parts.append("Available SDP Modules:\n" + '\n'.join(module_list))
        parts.append(
            "\nKeyword→Module hints:\n" +
            '\n'.join(f"  '{k}' → {v}" for k, v in
                      list(self.taxonomy.get('feature_keyword_map', {}).items())[:20])
        )

        return '\n'.join(parts)

    def run(self, state: AgentState) -> AgentState:
        """LangGraph node function."""
        feature_description = state.get('feature_description', '')
        target_modules = state.get('target_modules', [])

        state['messages'] = state.get('messages', []) + [
            f"[PlannerAgent] Analyzing: {feature_description[:100]}..."
        ]

        try:
            response = self.llm.invoke([
                SystemMessage(content=SYSTEM_PROMPT),
                HumanMessage(content=self._build_user_prompt(feature_description, target_modules)),
            ])

            raw = response.content.strip()
            # Strip markdown code fences if present
            if raw.startswith('```'):
                raw = raw.split('\n', 1)[1]
                raw = raw.rsplit('```', 1)[0]

            plan_data = json.loads(raw)
            state['affected_modules'] = plan_data.get('affected_modules', [])
            state['test_plan'] = plan_data.get('test_plan', {})
            state['messages'] = state.get('messages', []) + [
                f"[PlannerAgent] Plan created: {len(state['affected_modules'])} modules, "
                f"{sum(len(v) for v in state['test_plan'].values())} scenarios planned"
            ]

        except Exception as e:
            state['errors'] = state.get('errors', []) + [f"[PlannerAgent] Error: {e}"]
            # Fallback: use target_modules as affected
            state['affected_modules'] = target_modules
            state['test_plan'] = {m: [] for m in target_modules}

        return state
