"""
context_builder.py
------------------
Builds rich context payloads for the Coder Agent by combining:
  1. Module's existing test scenarios (from vector store)
  2. Actual source files: Fields.java, DataConstants.java, Locators.java
  3. Framework grammar rules
  4. Similar test cases from other modules (cross-module learning)

This context is injected into the LLM prompt so the agent generates
code that is 100% consistent with the existing codebase patterns.
"""

import json
import yaml
from pathlib import Path
from typing import Optional


class ContextBuilder:

    def __init__(self, base_dir: Optional[str] = None):
        self.base = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self.kb_raw = self.base / 'knowledge_base' / 'raw'
        self.config_dir = self.base / 'config'

        # Lazy-loaded caches
        self._module_index: Optional[dict] = None
        self._framework_grammar: Optional[dict] = None
        self._module_taxonomy: Optional[dict] = None
        self._testcases_parsed: Optional[list] = None

    # ── Lazy loaders ───────────────────────────────────────

    def _get_module_index(self) -> dict:
        if self._module_index is None:
            idx_path = self.kb_raw / 'module_index.json'
            if idx_path.exists():
                with open(idx_path) as f:
                    self._module_index = json.load(f)
            else:
                self._module_index = {'modules': {}, 'stats': {}}
        return self._module_index

    def _get_grammar(self) -> dict:
        if self._framework_grammar is None:
            gp = self.config_dir / 'framework_grammar.yaml'
            with open(gp) as f:
                self._framework_grammar = yaml.safe_load(f)
        return self._framework_grammar

    def _get_taxonomy(self) -> dict:
        if self._module_taxonomy is None:
            tp = self.config_dir / 'module_taxonomy.yaml'
            with open(tp) as f:
                self._module_taxonomy = yaml.safe_load(f)
        return self._module_taxonomy

    def _get_parsed_files(self) -> list:
        if self._testcases_parsed is None:
            tp = self.kb_raw / 'testcases_parsed.json'
            if tp.exists():
                with open(tp) as f:
                    self._testcases_parsed = json.load(f)
            else:
                self._testcases_parsed = []
        return self._testcases_parsed

    # ── Source file readers ────────────────────────────────

    def read_source_file(self, file_path: str) -> str:
        """Read a Java source file, return its content or empty string."""
        p = Path(file_path)
        if p.exists():
            return p.read_text(encoding='utf-8', errors='ignore')
        return ''

    def get_module_source_files(self, module_path: str) -> dict:
        """
        Returns a dict of file_type → content for a given module.
        {
          'fields':        '..java content..',
          'data_constants':'..java content..',
          'locators':      '..java content..',
          'constants':     '..java content..',
          'scenario_samples': ['..java content..', ...],
        }
        """
        idx = self._get_module_index()
        mod = idx['modules'].get(module_path, {})
        result = {}

        if mod.get('fields_file'):
            result['fields'] = self.read_source_file(mod['fields_file'])
        if mod.get('data_constants_file'):
            result['data_constants'] = self.read_source_file(mod['data_constants_file'])
        if mod.get('locators_file'):
            result['locators'] = self.read_source_file(mod['locators_file'])
        if mod.get('constants_file'):
            result['constants'] = self.read_source_file(mod['constants_file'])

        # Sample 2 scenario files
        scenario_samples = []
        for sf in mod.get('scenario_files', [])[:2]:
            content = self.read_source_file(sf)
            if content:
                scenario_samples.append(content[:4000])  # cap at 4k chars
        result['scenario_samples'] = scenario_samples

        return result

    # ── Context builder ────────────────────────────────────

    def build_generation_context(
        self,
        module_path: str,
        similar_scenarios: list[dict],
        feature_description: str,
        help_context: list[dict] | None = None,
        ui_observations: list[dict] | None = None,
    ) -> str:
        """
        Build the full context string for the Coder Agent prompt.
        help_context    : optional list of dicts from search_help_topics()
        ui_observations : optional list of UIObservation.to_dict() from UIScoutAgent —
            real live UI behaviour observed by Playwright BEFORE code generation.
            This is the most authoritative source — it overrides help_context.
        """
        lines = []
        grammar = self._get_grammar()
        idx = self._get_module_index()
        mod = idx['modules'].get(module_path, {})
        sources = self.get_module_source_files(module_path)

        lines.append("=" * 70)
        lines.append("FRAMEWORK CONTEXT FOR CODE GENERATION")
        lines.append("=" * 70)

        # 1. Module metadata
        lines.append(f"\n## Target Module: {module_path}")
        lines.append(f"Entity: {mod.get('entity', '')}")
        lines.append(f"Suite Role: {mod.get('suite_role', '')}")
        lines.append(f"Suite Owner: {mod.get('suite_owner', '')}")
        lines.append(f"Existing scenario count: {mod.get('scenario_count', 0)}")

        # 2. Existing scenario method names (for ID generation and dedup)
        existing_ids = [sc['id'] for sc in mod.get('scenarios', []) if sc.get('id')]
        if existing_ids:
            lines.append(f"\nExisting Scenario IDs (do NOT reuse):")
            lines.append(', '.join(existing_ids[:30]))

        # 3. Fields.java
        if sources.get('fields'):
            lines.append("\n## Field Definitions (Fields.java):")
            lines.append("```java")
            lines.append(sources['fields'][:3000])
            lines.append("```")

        # 4. DataConstants.java
        if sources.get('data_constants'):
            lines.append("\n## Available Test Data Constants (DataConstants.java):")
            lines.append("```java")
            lines.append(sources['data_constants'][:2000])
            lines.append("```")

        # 5. Locators.java
        if sources.get('locators'):
            lines.append("\n## UI Locators (Locators.java):")
            lines.append("```java")
            lines.append(sources['locators'][:2000])
            lines.append("```")

        # 6. Sample scenario methods
        for i, sample in enumerate(sources.get('scenario_samples', [])):
            lines.append(f"\n## Existing Scenario Class Sample {i+1}:")
            lines.append("```java")
            lines.append(sample)
            lines.append("```")

        # 7. Similar scenarios from vector search
        if similar_scenarios:
            lines.append("\n## Similar Existing Test Cases (for pattern reference):")
            for r in similar_scenarios[:5]:
                m = r.get('metadata', {})
                lines.append(
                    f"  - [{m.get('module_path')}] {m.get('method_name')} : "
                    f"{m.get('description', '')}"
                )

        # 8. Framework grammar summary
        lines.append("\n## Framework Annotation Rules:")
        ann = grammar.get('annotations', {})
        for ann_name, ann_def in ann.items():
            lines.append(f"  @{ann_name}: required={[f['name'] for f in ann_def.get('required_fields', [])]}")

        # 9a. LIVE UI observations from Playwright scout — HIGHEST PRIORITY
        # These are real-time observations of the application UI, not documentation.
        # They take precedence over help guide content for understanding UI behaviour.
        if ui_observations:
            lines.append("\n## LIVE UI Behaviour Observations (observed by Playwright before code generation):")
            lines.append("CRITICAL: Use these observations to determine which buttons to click,")
            lines.append("which fields are required, and what state changes occur on interaction.")
            for obs in ui_observations:
                lines.append(f"\n  ── {obs.get('flow_name', 'observation')} ──")
                lines.append(f"  {obs.get('description', '')}")
                if obs.get('visible_buttons'):
                    lines.append(f"  Visible buttons : {obs['visible_buttons']}")
                if obs.get('visible_fields'):
                    lines.append(f"  Visible fields  : {obs['visible_fields'][:12]}")
                if obs.get('required_fields'):
                    lines.append(f"  Required fields : {obs['required_fields']}")
                for note in obs.get('notes', []):
                    lines.append(f"  ⚠ RULE: {note}")

        # 9b. SDP help guide context (fields, steps, feature overview)
        if help_context:
            lines.append("\n## SDP Application Context (official help guide):")
            lines.append("Use this to understand what each field does, valid values, and the correct UI workflow.")

            by_type: dict[str, list] = {}
            for item in help_context:
                by_type.setdefault(item.get('type', 'full_text'), []).append(item)

            # Field definitions first — most directly useful for data/assertion choices
            if by_type.get('field'):
                lines.append("\n### UI Field Definitions:")
                for item in by_type['field'][:12]:
                    lines.append(f"  [{item['title']}] {item['content'][:220]}")

            # Step-by-step workflows — teaches the LLM the correct action sequence
            if by_type.get('steps'):
                lines.append("\n### UI Workflow Steps:")
                for item in by_type['steps'][:4]:
                    lines.append(f"  Topic: {item['title']}")
                    for step_line in item['content'].split('\n')[:6]:
                        step_line = step_line.strip()
                        if step_line:
                            lines.append(f"    {step_line}")

            # Feature overview — provides the 'why' and edge cases
            if by_type.get('full_text'):
                lines.append("\n### Feature Overview:")
                for item in by_type['full_text'][:2]:
                    lines.append(f"  {item['content'][:350]}")

        # 10. Task
        lines.append(f"\n## Your Task:")
        lines.append(f"Generate test scenarios for: {feature_description}")
        lines.append("=" * 70)

        return '\n'.join(lines)

    def get_framework_rules_summary(self) -> str:
        """Short grammar rules string for system prompt."""
        grammar = self._get_grammar()
        template = grammar.get('test_case_code_template', '')
        rules = [
            "RULES FOR CODE GENERATION:",
            "1. Every test class MUST have @AutomaterSuite(role=..., owner=...) at class level.",
            "2. Every test method MUST have @AutomaterScenario with id, group, description, dataIds.",
            "3. Test IDs follow pattern: SDP_<MODULE>_<VIEW>_<ALPHA-ID>",
            "4. Always wrap logic in try/catch/finally with addSuccessReport/addFailureReport.",
            "5. Use report.startMethodFlowInStepsToReproduce() at start, endMethodFlowInStepsToReproduce() in finally.",
            "6. Actions are via: actions.navigate, actions.validate, actions.clickByName, actions.waitForAjaxComplete.",
            "7. FieldDetails come from the module's Fields.java, TestCaseData from DataConstants.java.",
            "8. NEVER hardcode locators or string values; use Locators.java and Constants.java constants.",
            f"\nCode template:\n{template}",
        ]
        return '\n'.join(rules)
