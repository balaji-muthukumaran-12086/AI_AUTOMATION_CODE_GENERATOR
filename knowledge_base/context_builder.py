"""
context_builder.py
------------------
Builds rich context payloads for the Coder Agent by combining:
  1. Product Discovery documents (verified via Playwright — highest authority)
  2. Module's existing test scenarios (from vector store)
  3. Actual source files: Fields.java, DataConstants.java, Locators.java
  4. Framework grammar rules
  5. Similar test cases from other modules (cross-module learning)

This context is injected into the LLM prompt so the agent generates
code that is 100% consistent with the existing codebase patterns.
"""

import json
import re
import yaml
from pathlib import Path
from typing import Optional

from knowledge_base.discovery_loader import DiscoveryLoader


class ContextBuilder:

    def __init__(self, base_dir: Optional[str] = None):
        self.base = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self.kb_raw = self.base / 'knowledge_base' / 'raw'
        self.config_dir = self.base / 'config'

        # Discovery loader for product knowledge docs
        self.discovery_loader = DiscoveryLoader(str(self.base))

        # Lazy-loaded caches
        self._module_index: Optional[dict] = None
        self._framework_grammar: Optional[dict] = None
        self._module_taxonomy: Optional[dict] = None
        self._testcases_parsed: Optional[list] = None
        self._api_registry: Optional[dict] = None
        self._entity_inventories: dict = {}

    # ── Lazy loaders ───────────────────────────────────────

    def _get_api_registry(self) -> dict:
        """Load the API registry (verified endpoints per module)."""
        if self._api_registry is None:
            reg_path = self.config_dir / 'api_registry.yaml'
            if reg_path.exists():
                self._api_registry = yaml.safe_load(reg_path.read_text())
            else:
                self._api_registry = {}
        return self._api_registry

    def _get_entity_inventory(self, module: str, entity: str) -> dict:
        """Load entity inventory YAML (methods, locators, preProcess groups)."""
        key = f"{module}_{entity}"
        if key not in self._entity_inventories:
            inv_path = self.config_dir / 'entity_inventory' / f"{key}.yaml"
            if inv_path.exists():
                self._entity_inventories[key] = yaml.safe_load(inv_path.read_text())
            else:
                self._entity_inventories[key] = {}
        return self._entity_inventories[key]

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
          'annotation_constants': '..java content..',
          'locators':      '..java content..',
          'constants':     '..java content..',
          'data_json_keys': ['key1', 'key2', ...],
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
        if mod.get('annotation_constants_file'):
            result['annotation_constants'] = self.read_source_file(mod['annotation_constants_file'])
        if mod.get('locators_file'):
            result['locators'] = self.read_source_file(mod['locators_file'])
        if mod.get('constants_file'):
            result['constants'] = self.read_source_file(mod['constants_file'])

        # Extract top-level keys from the entity's _data.json file
        if mod.get('data_json_file'):
            result['data_json_keys'] = self._extract_data_json_keys(mod['data_json_file'])

        # Sample 2 scenario files
        scenario_samples = []
        for sf in mod.get('scenario_files', [])[:2]:
            content = self.read_source_file(sf)
            if content:
                scenario_samples.append(content[:4000])  # cap at 4k chars
        result['scenario_samples'] = scenario_samples

        return result

    def _extract_data_json_keys(self, data_json_path: str) -> list[str]:
        """Extract top-level keys from an entity _data.json file."""
        try:
            p = Path(data_json_path)
            if p.exists():
                data = json.loads(p.read_text(encoding='utf-8', errors='ignore'))
                if isinstance(data, dict):
                    return list(data.keys())
        except Exception:
            pass
        return []

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

        # 4b. AnnotationConstants.java (preProcess data IDs — MUST reuse existing ones)
        if sources.get('annotation_constants'):
            lines.append("\n## Existing Annotation Constants (AnnotationConstants.java):")
            lines.append("CRITICAL: Reuse these existing Data constants in dataIds={} — do NOT invent new ones.")
            lines.append("```java")
            lines.append(sources['annotation_constants'][:2000])
            lines.append("```")

        # 4c. Existing data JSON keys (MUST reuse — do NOT create duplicates)
        if sources.get('data_json_keys'):
            keys = sources['data_json_keys']
            lines.append(f"\n## Existing Data JSON Keys ({len(keys)} entries in *_data.json):")
            lines.append("CRITICAL: REUSE these existing data entries when they match your test's needs.")
            lines.append("DO NOT create new JSON entries if an existing key provides the same entity data.")
            lines.append("Keys: " + ', '.join(keys[:80]))

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

        # 9. Product Discovery documents — HIGHEST AUTHORITY
        # These are verified via live Playwright exploration and contain proven API
        # endpoints, real UI flows, and edge cases. They override ALL other sources.
        discovery_context = self.discovery_loader.get_all_context_for_module(
            module_path.strip('/').split('/')[1] if '/' in module_path else module_path
        )
        if discovery_context:
            lines.append("\n" + discovery_context)

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

        # 10. Entity Inventory — existing methods, locators, preProcess groups
        module_parts = module_path.strip('/').split('/')
        if len(module_parts) >= 2:
            inv = self._get_entity_inventory(module_parts[0], module_parts[1])
            if inv:
                lines.append("\n## Entity Inventory (auto-generated — REUSE existing methods):")

                # ── Deep preProcess behavior (highest priority — enables group reuse) ──
                pp_deep = inv.get('preprocess_deep', [])
                if pp_deep:
                    lines.append(f"\n### preProcess Groups — Full Behavior ({len(pp_deep)} groups):")
                    lines.append("CRITICAL: REUSE these groups — do NOT add new ones if existing group provides the same entities/LocalStorage keys.")
                    for g in pp_deep:
                        ls_stores = ', '.join(f"{s['key']}({s['source_type']})" for s in g.get('local_storage_stores', []))
                        ls_reads = ', '.join(g.get('local_storage_reads', []))
                        api_calls = ', '.join(g.get('api_util_calls', []))
                        dataids = ', '.join(str(i) for i in g.get('dataids_consumed', []))
                        entities = ', '.join(g.get('entities_created', []))
                        parts = [f"group=\"{g['group']}\""]
                        if dataids:
                            parts.append(f"dataIds[{dataids}]")
                        if api_calls:
                            parts.append(f"calls: {api_calls}")
                        if entities:
                            parts.append(f"creates: {entities}")
                        if ls_stores:
                            parts.append(f"stores: [{ls_stores}]")
                        if ls_reads:
                            parts.append(f"reads: [{ls_reads}]")
                        if g.get('creates_user'):
                            role = g.get('user_role', '?')
                            parts.append(f"creates user(role={role})")
                        if g.get('calls_super'):
                            parts.append("→ chains to super")
                        lines.append(f"  - {' | '.join(parts)}")
                else:
                    # Fallback to shallow preProcess if deep not available
                    pp_groups = inv.get('preprocess_groups', [])
                    if pp_groups:
                        lines.append(f"\n### Known preProcess Groups ({len(pp_groups)}):")
                        lines.append("CRITICAL: REUSE existing groups — do NOT create new ones unless needed.")
                        for g in pp_groups:
                            ls_keys = ', '.join(g.get('local_storage_keys', [])) or 'none'
                            lines.append(f"  - group=\"{g['name']}\" → creates {g.get('creates_count', 0)} entities, "
                                         f"LocalStorage keys: [{ls_keys}]")

                # ── Deep APIUtil behavior ──
                api_deep = inv.get('api_util_deep', [])
                if api_deep:
                    lines.append(f"\n### APIUtil Methods — Behavior ({len(api_deep)} methods):")
                    for m in api_deep:
                        ret = m.get('return_type', 'void')
                        parts = [f"{ret} {m['name']}({m.get('params', '')})"]
                        if m.get('api_paths'):
                            parts.append(f"→ {','.join(m['api_paths'][:2])}")
                        if m.get('http_methods'):
                            parts.append(f"[{','.join(m['http_methods'])}]")
                        if m.get('api_path_from_parameter'):
                            parts.append("[path from caller]")
                        if m.get('local_storage_writes'):
                            parts.append(f"stores: {m['local_storage_writes']}")
                        if m.get('data_loads'):
                            # Show just the data constant reference, not full call
                            data_refs = []
                            for dl in m['data_loads'][:2]:
                                # Extract the constant name from DataUtil.getTestCaseData(Foo.Bar.BAZ)
                                const_m = re.search(r'\.(\w+)\)', dl)
                                if const_m:
                                    data_refs.append(const_m.group(1))
                                else:
                                    data_refs.append(dl[:40])
                            parts.append(f"data: {data_refs}")
                        lines.append(f"  - {' '.join(parts)}")
                else:
                    # Fallback to shallow
                    api_methods = inv.get('api_util', {}).get('methods', [])
                    if api_methods:
                        lines.append(f"\n### APIUtil Methods ({len(api_methods)} available):")
                        for m in api_methods:
                            lines.append(f"  - {m['return_type']} {m['name']}({m.get('params', '')})")

                # ── Deep ActionsUtil behavior ──
                actions_deep = inv.get('actions_util_deep', [])
                if actions_deep:
                    lines.append(f"\n### ActionsUtil Methods — Behavior ({len(actions_deep)} methods):")
                    lines.append("CRITICAL: Call these existing methods — do NOT duplicate their logic.")
                    for m in actions_deep:
                        parts = [f"{m['name']}({m.get('params', '')})"]
                        if m.get('action_chain'):
                            parts.append(f"chain: {' → '.join(m['action_chain'][:5])}")
                        if m.get('locators_used'):
                            parts.append(f"uses: {m['locators_used'][:3]}")
                        if m.get('local_storage_reads'):
                            parts.append(f"reads LS: {m['local_storage_reads']}")
                        lines.append(f"  - {' | '.join(parts)}")
                else:
                    # Fallback to shallow
                    actions_methods = inv.get('actions_util', {}).get('methods', [])
                    if actions_methods:
                        lines.append(f"\n### ActionsUtil Methods ({len(actions_methods)} available):")
                        lines.append("CRITICAL: Call these existing methods — do NOT duplicate their logic.")
                        for m in actions_methods:
                            lines.append(f"  - {m['name']}({m.get('params', '')})")

                # ── Deep data.json analysis (summary + curated entries) ──
                data_deep = inv.get('data_json_deep', {})
                if data_deep and data_deep.get('entries'):
                    all_entries = data_deep['entries']
                    lines.append(f"\n### Data JSON Entries — Summary ({data_deep.get('total_entries', 0)} total):")
                    lines.append(f"  Most common fields: {list(data_deep.get('field_frequency', {}).keys())[:10]}")
                    all_ph = data_deep.get('all_placeholders', [])
                    custom_phs = [p for p in all_ph if p.startswith('custom_')]
                    if custom_phs:
                        lines.append(f"  Custom placeholders (require LocalStorage): {custom_phs[:15]}")

                    # Show API preProcess entries (most important for group reuse)
                    api_entries = {k: v for k, v in all_entries.items()
                                  if v.get('purpose') == 'api_preprocess'}
                    if api_entries:
                        lines.append(f"\n  API/preProcess data entries ({len(api_entries)}):")
                        for k, v in list(api_entries.items())[:20]:
                            flds = ', '.join(v['fields'][:6])
                            extra = '...' if len(v['fields']) > 6 else ''
                            ls_req = ', '.join(v.get('local_storage_keys_required', []))
                            entry_line = f"    \"{k}\": [{flds}{extra}]"
                            if ls_req:
                                entry_line += f" (needs LS: {ls_req})"
                            lines.append(entry_line)

                    # Show UI form entries (limited — for test method data)
                    ui_entries = {k: v for k, v in all_entries.items()
                                 if v.get('purpose') == 'ui_form'}
                    if ui_entries:
                        lines.append(f"\n  UI form data entries ({len(ui_entries)}):")
                        for k, v in list(ui_entries.items())[:15]:
                            flds = ', '.join(v['fields'][:6])
                            extra = '...' if len(v['fields']) > 6 else ''
                            lines.append(f"    \"{k}\": [{flds}{extra}]")

        # 11. API Registry — verified endpoint availability
        registry = self._get_api_registry()
        if registry and 'modules' in registry:
            mod_key = module_parts[0] if module_parts else ''
            mod_reg = registry['modules'].get(mod_key, {})
            if mod_reg:
                lines.append(f"\n## API Registry for '{mod_key}' (VERIFIED endpoints):")
                lines.append("⚠️ Before any restAPI call, check this list:")
                for ep_name, ep_data in mod_reg.get('endpoints', {}).items():
                    status = ep_data.get('status', 'UNTESTED')
                    icon = "✅" if status == 'VERIFIED_WORKING' else "❌" if status == 'DOES_NOT_EXIST' else "❓"
                    path = ep_data.get('path', '')
                    lines.append(f"  {icon} {ep_name}: {ep_data.get('method', '?')} {path} [{status}]")
                    if status == 'DOES_NOT_EXIST' and ep_data.get('ui_alternative'):
                        lines.append(f"     → UI alternative: {ep_data['ui_alternative']}")

        # 12. Task
        lines.append(f"\n## Your Task:")
        lines.append(f"Generate test scenarios for: {feature_description}")
        lines.append("=" * 70)

        return '\n'.join(lines)

    def get_relevant_framework_sections(
        self,
        query: str,
        doc_type: Optional[str] = None,
        top_k: int = 5,
    ) -> str:
        """
        RAG-retrieve the most relevant sections from framework_rules.md /
        framework_knowledge.md for the given generation query.

        doc_type: 'rules' | 'knowledge' | None (search both)
        Returns formatted Markdown text ready for prompt injection.
        Falls back to empty string if the collection is empty (not yet indexed).
        """
        # Lazy-load VectorStore so ContextBuilder stays loosely coupled
        if not hasattr(self, '_vector_store') or self._vector_store is None:
            try:
                from knowledge_base.vector_store import VectorStore
                self._vector_store = VectorStore(
                    persist_dir=str(self.base / 'knowledge_base' / 'chroma_db')
                )
            except Exception:
                self._vector_store = None
                return ''

        try:
            results = self._vector_store.search_framework_docs(
                query, doc_type_filter=doc_type, top_k=top_k
            )
        except Exception:
            return ''

        if not results:
            return ''

        lines = []
        seen_titles: set[str] = set()
        for r in results:
            title = r['section_title']
            if title in seen_titles:
                continue
            seen_titles.add(title)
            source_label = '(rules)' if r.get('doc_type') == 'rules' else '(knowledge)'
            lines.append(f"### {title} {source_label}")
            lines.append(r['content'])
            lines.append('')
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
