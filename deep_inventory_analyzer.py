#!/usr/bin/env python3
"""
deep_inventory_analyzer.py
--------------------------
Deep analysis of existing Java test code to extract:
  1. Data JSON entries: fields, placeholders ($(custom_X)), required LocalStorage keys
  2. ActionsUtil methods: locators used, LocalStorage reads/writes, actions chain
  3. APIUtil methods: API paths called, data keys loaded, LocalStorage writes
  4. preProcess groups: full behavior map — what they create, which APIUtil methods
     they call, which dataIds indices they consume, which LocalStorage keys they store

This gives the AI complete behavioral understanding of existing code,
not just signatures.

Usage:
    from deep_inventory_analyzer import DeepAnalyzer
    analyzer = DeepAnalyzer(src_root, resources_root)
    data_analysis = analyzer.analyze_data_json(module, entity)
    actions_analysis = analyzer.analyze_actions_util(module, entity)
    api_analysis = analyzer.analyze_api_util(module, entity)
    preprocess_analysis = analyzer.analyze_preprocess(module, entity)
"""

import json
import re
from pathlib import Path
from typing import Optional


class DeepAnalyzer:

    def __init__(self, src_roots: list, base_dir: Path):
        self.src_roots = src_roots  # List of Path objects to source roots
        self.base_dir = base_dir

    def _find_file(self, module: str, entity: str, subdir: str, pattern: str) -> Optional[Path]:
        """Find a Java file matching pattern under module/entity/subdir."""
        for src_root in self.src_roots:
            base = src_root / "com" / "zoho" / "automater" / "selenium" / "modules" / module / entity
            target_dir = base / subdir if subdir else base
            if target_dir.exists():
                for f in target_dir.glob(pattern):
                    return f
        return None

    def _find_data_json(self, module: str, entity: str) -> Optional[Path]:
        """Find the *_data.json file for an entity."""
        for src_root in self.src_roots:
            res_root = src_root.parent / "resources"
            data_json = res_root / "entity" / "data" / module / entity / f"{entity}_data.json"
            if data_json.exists():
                return data_json
        return None

    def _find_entity_classes(self, module: str, entity: str) -> list:
        """Find all Java files directly in the entity dir (parent + subclasses)."""
        results = []
        for src_root in self.src_roots:
            base = src_root / "com" / "zoho" / "automater" / "selenium" / "modules" / module / entity
            if base.exists():
                for f in base.glob("*.java"):
                    if (f.name.endswith("Constants.java") or f.name.endswith("Locators.java")
                            or f.name.endswith("Fields.java")):
                        continue
                    results.append(f)
        return results

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 1. DATA JSON DEEP ANALYSIS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def analyze_data_json(self, module: str, entity: str) -> dict:
        """
        Deep-analyze *_data.json:
        - Per entry: fields present, lookup fields, placeholders, required LocalStorage keys
        - Cross-entry: field frequency, common vs unique fields, reuse candidates
        """
        data_path = self._find_data_json(module, entity)
        if not data_path:
            return {}

        try:
            raw = json.loads(data_path.read_text(encoding='utf-8', errors='replace'))
        except Exception:
            return {}

        entries = {}
        all_fields_freq = {}  # field → count of entries using it
        all_placeholders = set()

        for key, value in raw.items():
            data = value.get('data', value) if isinstance(value, dict) else {}
            if not isinstance(data, dict):
                continue

            fields = list(data.keys())
            for f in fields:
                all_fields_freq[f] = all_fields_freq.get(f, 0) + 1

            # Find lookup fields ({"name": "..."} pattern)
            lookup_fields = []
            for f, v in data.items():
                if isinstance(v, dict) and 'name' in v and len(v) == 1:
                    lookup_fields.append(f)

            # Find all placeholders
            placeholders = []
            local_storage_keys_required = []
            self._extract_placeholders(data, placeholders, local_storage_keys_required)
            all_placeholders.update(placeholders)

            # Classify: API data vs UI data (heuristic: keys starting with api_ are API)
            purpose = "api_preprocess" if key.startswith("api_") or key.startswith("create_") else "ui_form"

            entries[key] = {
                'fields': fields,
                'field_count': len(fields),
                'lookup_fields': lookup_fields,
                'placeholders': placeholders,
                'local_storage_keys_required': local_storage_keys_required,
                'purpose': purpose,
            }

        # Find reuse groups: entries with identical field sets
        field_sig_to_keys = {}
        for key, info in entries.items():
            sig = tuple(sorted(info['fields']))
            field_sig_to_keys.setdefault(sig, []).append(key)

        reuse_groups = {
            ', '.join(keys): list(sig)
            for sig, keys in field_sig_to_keys.items()
            if len(keys) > 1
        }

        return {
            'file': str(data_path),
            'total_entries': len(entries),
            'entries': entries,
            'field_frequency': dict(sorted(all_fields_freq.items(), key=lambda x: -x[1])[:20]),
            'all_placeholders': sorted(all_placeholders),
            'reuse_groups': reuse_groups,
        }

    def _extract_placeholders(self, obj, placeholders: list, ls_keys: list):
        """Recursively extract $(placeholder) from a JSON object."""
        if isinstance(obj, str):
            for m in re.finditer(r'\$\(([^)]+)\)', obj):
                ph = m.group(1)
                placeholders.append(ph)
                # $(custom_X) requires LocalStorage key "X"
                if ph.startswith('custom_'):
                    ls_keys.append(ph[7:])  # strip 'custom_'
        elif isinstance(obj, dict):
            for v in obj.values():
                self._extract_placeholders(v, placeholders, ls_keys)
        elif isinstance(obj, list):
            for item in obj:
                self._extract_placeholders(item, placeholders, ls_keys)

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 2. ACTIONS UTIL DEEP ANALYSIS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def analyze_actions_util(self, module: str, entity: str) -> list:
        """
        Deep-analyze ActionsUtil methods:
        - Which locators each method uses
        - Which LocalStorage keys it reads/writes
        - UI actions chain (click, type, navigate, etc.)
        - Whether it returns a value
        """
        filepath = self._find_file(module, entity, "utils", "*ActionsUtil.java")
        if not filepath:
            return []

        content = filepath.read_text(encoding='utf-8', errors='replace')
        methods = self._extract_methods_with_bodies(content)

        analyzed = []
        for m in methods:
            body = m['body']

            # Extract locators used
            locators = list(set(re.findall(r'(\w+Locators\.\w+\.\w+)', body)))

            # Extract LocalStorage operations
            ls_reads = list(set(re.findall(r'LocalStorage\.(?:getAsString|fetch)\s*\(\s*"([^"]+)"', body)))
            ls_writes = list(set(re.findall(r'LocalStorage\.store\s*\(\s*"([^"]+)"', body)))

            # Extract UI action chain (search anywhere in line, not just start)
            action_chain = []
            for line in body.split('\n'):
                for action in re.finditer(r'(actions\.(?:\w+\.)*\w+)\s*\(', line):
                    call = action.group(1)
                    # Deduplicate consecutive identical calls
                    if not action_chain or action_chain[-1] != call:
                        action_chain.append(call)

            # Check for wait patterns
            has_explicit_wait = 'waitForAjaxComplete' in body or 'waitForAnElementToAppear' in body
            has_sleep = 'Thread.sleep' in body

            analyzed.append({
                'name': m['name'],
                'params': m['params'],
                'return_type': m['return_type'],
                'locators_used': sorted(locators),
                'local_storage_reads': ls_reads,
                'local_storage_writes': ls_writes,
                'action_chain': action_chain[:10],  # cap at 10 for readability
                'has_explicit_wait': has_explicit_wait,
                'has_sleep': has_sleep,
                'line_count': len(body.strip().split('\n')),
            })

        return analyzed

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 3. API UTIL DEEP ANALYSIS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def analyze_api_util(self, module: str, entity: str) -> list:
        """
        Deep-analyze APIUtil methods:
        - Which API paths each method calls
        - Which data keys it loads (from DataUtil or getTestCaseData)
        - Which LocalStorage keys it stores
        - Which restAPI methods it uses (create, get, update, delete)
        - HTTP method used (POST, GET, PUT, DELETE)
        """
        filepath = self._find_file(module, entity, "utils", "*APIUtil.java")
        if not filepath:
            return []

        content = filepath.read_text(encoding='utf-8', errors='replace')
        methods = self._extract_methods_with_bodies(content)

        analyzed = []
        for m in methods:
            body = m['body']

            # --- REST method detection (both patterns) ---
            # Pattern 1: restAPI.methodName(...)  (lowercase instance from Utilities)
            rest_methods = set(re.findall(r'restAPI\.(\w+)\s*\(', body))
            # Pattern 2: RestAPI.getInstance().methodName(...)  (static instance)
            rest_methods.update(re.findall(r'RestAPI\.getInstance\(\)\.\s*(\w+)\s*\(', body))

            # --- API paths (literal strings in REST calls) ---
            api_paths = set()

            # restAPI.create("entityName", "apiPath", inputData)
            for pm in re.finditer(r'restAPI\.(?:create|createAndGetResponse|createAndGetFullResponse|createAndGetAPIResponse)\s*\(\s*"(\w+)"\s*,\s*"([^"]*)"', body):
                api_paths.add(pm.group(2))

            # restAPI.update/get/delete("path/..." + ...) — path starts with a literal
            for pm in re.finditer(r'restAPI\.(?:update|get|delete)\s*\(\s*"([^"]*?)(?:"\s*\+|"[^+])', body):
                api_paths.add(pm.group(1))

            # RestAPI.getInstance().createAndGetResponse("entity", "apiPath", ...)
            for pm in re.finditer(r'RestAPI\.getInstance\(\)\.\s*(?:createAndGetResponse|create|createAndGetFullResponse)\s*\(\s*"(\w+)"\s*,\s*"([^"]*)"', body):
                api_paths.add(pm.group(2))

            # RestAPI.getInstance().update("path" + ...)
            for pm in re.finditer(r'RestAPI\.getInstance\(\)\.\s*(?:update|get)\s*\(\s*"([^"]*?)(?:"\s*\+|"[^+])', body):
                api_paths.add(pm.group(1))

            # restAPI.getEntityIdUsingSearchCriteria("plural", "apiPath", ...)
            for pm in re.finditer(r'restAPI\.getEntityIdUsingSearchCriteria\s*\(\s*"(\w+)"\s*,\s*"([^"]*)"', body):
                api_paths.add(pm.group(2))

            # restAPI.getDataUsingSearchCriteria("apiPath", ...)
            for pm in re.finditer(r'restAPI\.getDataUsingSearchCriteria\s*\(\s*"([^"]*)"', body):
                api_paths.add(pm.group(1))

            # Concatenated paths: "changes/" + localVar + "/notes" -> "changes/*/notes"
            for pm in re.finditer(r'"(\w+/)"\s*\+\s*\w+(?:\.\w+\([^)]*\))?\s*\+\s*"(/\w+[^"]*)"', body):
                api_paths.add(pm.group(1) + '*' + pm.group(2))

            # Detect if api path comes from parameter
            api_path_from_param = 'apiPath' in m['params'] and not api_paths

            # --- HTTP method detection ---
            http_methods = set()
            if 'Method.POST' in body or any(rm in rest_methods for rm in ('create', 'createAndGetResponse', 'createAndGetFullResponse', 'createAndGetAPIResponse')):
                http_methods.add('POST')
            if 'Method.GET' in body or 'get' in rest_methods or 'getEntityIdUsingSearchCriteria' in rest_methods:
                http_methods.add('GET')
            if 'Method.PUT' in body or 'update' in rest_methods:
                http_methods.add('PUT')
            if 'Method.DELETE' in body or 'delete' in rest_methods:
                http_methods.add('DELETE')
            # triggerRestAPIUsingInputData with Method.POST etc
            for hm in re.findall(r'io\.restassured\.http\.Method\.(\w+)', body):
                http_methods.add(hm)

            # --- Data loading (all patterns) ---
            data_loads = []
            # DataUtil.getTestCaseDataUsingCaseId(module, entity, caseId)
            data_loads.extend(re.findall(r'DataUtil\.getTestCaseDataUsingCaseId\s*\([^)]+\)', body))
            # DataUtil.getTestCaseDataUsingFilePath(path, caseId)
            data_loads.extend(re.findall(r'DataUtil\.getTestCaseDataUsingFilePath\s*\([^)]+\)', body))
            # DataUtil.getTestCaseData(DataConstants...)
            data_loads.extend(re.findall(r'DataUtil\.getTestCaseData\s*\([^)]+\)', body))
            # DataUtil.getTestCaseDataForRestAPI(fields, DataConstants...)
            data_loads.extend(re.findall(r'DataUtil\.getTestCaseDataForRestAPI\s*\([^)]+\)', body))

            # --- LocalStorage operations ---
            ls_writes = list(set(re.findall(r'LocalStorage\.store\s*\(\s*"([^"]+)"', body)))
            ls_reads = list(set(re.findall(r'LocalStorage\.(?:getAsString|fetch)\s*\(\s*"([^"]+)"', body)))

            # --- Return pattern ---
            returns_id = 'return' in body and ('getId' in body or 'optString("id")' in body)
            returns_response = 'return' in body and ('response' in body.lower() or 'getResponse' in body)

            result = {
                'name': m['name'],
                'params': m['params'],
                'return_type': m['return_type'],
                'api_paths': sorted(api_paths),
                'http_methods': sorted(http_methods),
                'rest_methods_used': sorted(rest_methods),
                'data_loads': [d.strip() for d in data_loads],
                'local_storage_writes': ls_writes,
                'local_storage_reads': ls_reads,
                'returns_id': returns_id,
                'returns_response': returns_response,
            }
            if api_path_from_param:
                result['api_path_from_parameter'] = True

            analyzed.append(result)

        return analyzed

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 4. PREPROCESS DEEP ANALYSIS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def analyze_preprocess(self, module: str, entity: str) -> list:
        """
        Deep-analyze preProcess groups from ALL entity Java files:
        - Group name
        - dataIds indices consumed (dataIds[0], dataIds[1], etc.)
        - APIUtil methods called (fully qualified)
        - restAPI direct calls
        - LocalStorage keys stored (with their source — API response field, hardcoded, etc.)
        - Entities created (types and counts)
        - Whether it calls super.preProcess at the end (chain behavior)
        """
        entity_files = self._find_entity_classes(module, entity)
        all_groups = []

        for filepath in entity_files:
            content = filepath.read_text(encoding='utf-8', errors='replace')

            # Find preProcess method body
            pp_match = re.search(
                r'protected\s+boolean\s+preProcess\s*\(\s*String\s+group\s*,\s*String\s*\[\]\s*dataIds\s*\)\s*\{',
                content
            )
            if not pp_match:
                continue

            # Extract the full preProcess body (brace-matching)
            start = pp_match.end()
            pp_body = self._extract_brace_block(content, start)
            if not pp_body:
                continue

            # Check if it calls super.preProcess
            calls_super = 'super.preProcess' in pp_body

            # Split into group branches
            branches = self._split_preprocess_branches(pp_body)

            for group_name, branch_body in branches:
                # dataIds indices consumed
                dataids_used = sorted(set(re.findall(r'dataIds\[(\d+)\]', branch_body)))

                # APIUtil calls
                api_util_calls = re.findall(r'(\w+APIUtil\.\w+)\s*\(', branch_body)

                # direct restAPI calls
                rest_calls = re.findall(r'restAPI\.(\w+)\s*\(', branch_body)

                # LocalStorage stores with context
                ls_stores = []
                for m in re.finditer(r'LocalStorage\.store\s*\(\s*"([^"]+)"\s*,\s*([^)]+)\)', branch_body):
                    key = m.group(1)
                    value_source = m.group(2).strip()
                    # Simplify value source
                    if 'optString("id")' in value_source or 'getString("id")' in value_source:
                        source_type = "entity_id"
                    elif 'optString("title")' in value_source or 'getString("title")' in value_source:
                        source_type = "entity_title"
                    elif 'display_id' in value_source:
                        source_type = "display_id"
                    elif 'getDisplayId' in value_source:
                        source_type = "user_display_id"
                    elif 'response' in value_source.lower():
                        source_type = "api_response_field"
                    elif '"' in value_source:
                        source_type = "hardcoded"
                    else:
                        source_type = "computed"
                    ls_stores.append({'key': key, 'source_type': source_type})

                # LocalStorage reads
                ls_reads = list(set(re.findall(
                    r'LocalStorage\.(?:getAsString|fetch)\s*\(\s*"([^"]+)"', branch_body)))

                # Entity creation detection
                entities_created = []
                # Pattern: restAPI.createAndGetResponse("entityName", ...)
                for em in re.finditer(r'restAPI\.(?:create|createAndGetResponse|createAndGetFullResponse)\s*\(\s*"?(\w+)"?', branch_body):
                    entities_created.append(em.group(1))
                # Pattern: <Module>APIUtil.create<Entity>(...)
                for em in re.finditer(r'(\w+)APIUtil\.create(\w+)\s*\(', branch_body):
                    entities_created.append(f"{em.group(1)}.{em.group(2)}")

                # User creation detection
                creates_user = 'createUserByRole' in branch_body or 'createTechnician' in branch_body
                user_role = None
                if creates_user:
                    role_match = re.search(r'createUserByRole\s*\([^,]+,\s*[^,]+,\s*"([^"]+)"', branch_body)
                    if role_match:
                        user_role = role_match.group(1)

                all_groups.append({
                    'group': group_name,
                    'source_file': filepath.name,
                    'dataids_consumed': [int(i) for i in dataids_used],
                    'dataids_count': len(dataids_used),
                    'api_util_calls': api_util_calls,
                    'rest_direct_calls': sorted(set(rest_calls)),
                    'local_storage_stores': ls_stores,
                    'local_storage_reads': ls_reads,
                    'entities_created': entities_created,
                    'creates_user': creates_user,
                    'user_role': user_role,
                    'calls_super': calls_super,
                })

        # Deduplicate: keep the richest entry per (group, source_file) pair
        seen = {}
        for g in all_groups:
            key = (g['group'], g['source_file'])
            if key not in seen:
                seen[key] = g
            else:
                # Keep the one with more behavioral data
                existing = seen[key]
                new_score = len(g['api_util_calls']) + len(g['local_storage_stores']) + len(g['entities_created'])
                old_score = len(existing['api_util_calls']) + len(existing['local_storage_stores']) + len(existing['entities_created'])
                if new_score > old_score:
                    seen[key] = g

        return list(seen.values())

    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # HELPERS
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    def _extract_methods_with_bodies(self, content: str) -> list:
        """Extract public static methods with their full bodies."""
        methods = []
        pattern = re.compile(
            r'public\s+static\s+(\w[\w<>\[\],\s]*?)\s+(\w+)\s*\(([^)]*)\)\s*(?:throws\s+[\w,\s]+)?\s*\{',
            re.MULTILINE
        )
        for match in pattern.finditer(content):
            return_type = match.group(1).strip()
            name = match.group(2).strip()
            params = match.group(3).strip()
            body_start = match.end()
            body = self._extract_brace_block(content, body_start)
            if body:
                methods.append({
                    'name': name,
                    'params': params if params else "(none)",
                    'return_type': return_type,
                    'body': body,
                })
        return methods

    def _extract_brace_block(self, content: str, start: int) -> Optional[str]:
        """Extract content within balanced braces starting at position start."""
        depth = 1
        i = start
        while i < len(content) and depth > 0:
            if content[i] == '{':
                depth += 1
            elif content[i] == '}':
                depth -= 1
            i += 1
        if depth == 0:
            return content[start:i - 1]
        return None

    def _split_preprocess_branches(self, pp_body: str) -> list:
        """Split preProcess body into (group_name, branch_body) tuples."""
        branches = []

        # Match: if/else-if group.equalsIgnoreCase("xxx") or "xxx".equalsIgnoreCase(group)
        pat = re.compile(
            r'(?:if|else\s*if)\s*\(\s*'
            r'(?:'
            r'"(\w+)"\s*\.equalsIgnoreCase\s*\(\s*group\s*\)'
            r'|'
            r'group\s*\.equalsIgnoreCase\s*\(\s*"(\w+)"\s*\)'
            r')',
            re.DOTALL
        )

        matches = list(pat.finditer(pp_body))
        for idx, match in enumerate(matches):
            group_name = match.group(1) or match.group(2)
            branch_start = match.end()

            # Find the end of this branch (next else-if or end of if block)
            if idx + 1 < len(matches):
                branch_end = matches[idx + 1].start()
            else:
                branch_end = len(pp_body)

            branch_body = pp_body[branch_start:branch_end]
            branches.append((group_name, branch_body))

        return branches
