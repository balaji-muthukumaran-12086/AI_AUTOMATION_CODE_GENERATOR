#!/usr/bin/env python3
"""
generate_entity_inventory.py
----------------------------
Auto-generates YAML inventory files for every entity module in the project.
These inventories give the AI complete awareness of what already exists:
  - ActionsUtil methods (name, params, purpose, locators used, LocalStorage ops)
  - APIUtil methods (name, params, API paths called, LocalStorage writes)
  - Locator interfaces + constants
  - DataConstants keys
  - AnnotationConstants groups + data keys
  - preProcess groups: full behavior (entities created, APIUtil calls, dataIds consumed, LocalStorage stores)
  - Data JSON entries: fields, placeholders, required LocalStorage keys, reuse groups

Usage:
    .venv/bin/python generate_entity_inventory.py                    # All modules (shallow)
    .venv/bin/python generate_entity_inventory.py --deep             # All modules (deep analysis)
    .venv/bin/python generate_entity_inventory.py changes/change     # Single module
    .venv/bin/python generate_entity_inventory.py --deep changes/change  # Single module (deep)

Output: config/entity_inventory/<module>_<entity>.yaml per entity
"""

import argparse
import os
import re
import sys
import yaml
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config.project_config import PROJECT_NAME, BASE_DIR


def find_modules(src_root: Path) -> list:
    """Find all entity modules under modules/, recursing into nested sub-modules."""
    modules_dir = src_root / "com" / "zoho" / "automater" / "selenium" / "modules"
    if not modules_dir.exists():
        return []

    skip_dirs = {'common', 'utils', '__pycache__'}
    results = []

    def _recurse(current_dir: Path, module_parts: list):
        """Recursively find leaf entity dirs that contain a 'common/' subfolder (Locators live there)."""
        has_common = (current_dir / "common").is_dir()
        has_child_entities = False

        for child in sorted(current_dir.iterdir()):
            if not child.is_dir() or child.name.startswith('.') or child.name in skip_dirs:
                continue
            # If a child itself has a common/ dir or deeper entity dirs, recurse
            _recurse(child, module_parts + [child.name])
            has_child_entities = True

        # Register this dir as an entity if it has a common/ folder (contains Locators/Constants)
        if has_common:
            if len(module_parts) >= 2:
                # module = top-level dir, entity = rest joined by underscore
                results.append({
                    'module': module_parts[0],
                    'entity': '_'.join(module_parts[1:]),
                    'path': current_dir,
                })
            elif len(module_parts) == 1:
                # Top-level module dirs with common/ (e.g. admin, maintenance)
                # have shared Locators/ActionsUtil — register as module-level entity
                results.append({
                    'module': module_parts[0],
                    'entity': module_parts[0],
                    'path': current_dir,
                })

    for module_dir in sorted(modules_dir.iterdir()):
        if not module_dir.is_dir() or module_dir.name.startswith('.'):
            continue
        _recurse(module_dir, [module_dir.name])

    return results


def extract_java_methods(filepath: Path) -> list:
    """Extract public static methods from a Java utility file."""
    if not filepath.exists():
        return []

    content = filepath.read_text(encoding='utf-8', errors='replace')
    methods = []

    # Match: public static <return> <name>(<params>) throws ...
    pattern = re.compile(
        r'public\s+static\s+(\w[\w<>\[\],\s]*?)\s+(\w+)\s*\(([^)]*)\)',
        re.MULTILINE
    )

    for match in pattern.finditer(content):
        return_type = match.group(1).strip()
        name = match.group(2).strip()
        params = match.group(3).strip()

        # Try to extract a one-line purpose from preceding comment or method name
        start = match.start()
        preceding = content[max(0, start - 200):start]
        purpose = ""

        # Check for single-line comment
        comment_match = re.search(r'//\s*(.+)$', preceding, re.MULTILINE)
        if comment_match:
            purpose = comment_match.group(1).strip()

        # Check for Javadoc @return or first line
        javadoc_match = re.search(r'/\*\*\s*\n?\s*\*?\s*(.+?)[\n*]', preceding)
        if javadoc_match and not purpose:
            purpose = javadoc_match.group(1).strip().rstrip('*').strip()

        methods.append({
            'name': name,
            'return_type': return_type,
            'params': params if params else "(none)",
            'purpose': purpose or "",
        })

    return methods


def extract_locator_interfaces(filepath: Path) -> dict:
    """Extract locator interface names and their constants from Locators.java."""
    if not filepath.exists():
        return {}

    content = filepath.read_text(encoding='utf-8', errors='replace')
    interfaces = {}

    # Find interface or inner class blocks (some Locators use 'interface', others use 'class')
    iface_pattern = re.compile(
        r'(?:interface|class)\s+(\w+)\s*(?:extends\s+\w+\s*)?\{(.*?)\}',
        re.DOTALL
    )

    for match in iface_pattern.finditer(content):
        iface_name = match.group(1)
        body = match.group(2)

        # Extract locator constants
        constants = []
        const_pattern = re.compile(r'(?:Locator|Function<String,\s*Locator>|BiFunction<.*?>)\s+(\w+)\s*=')
        for cm in const_pattern.finditer(body):
            constants.append(cm.group(1))

        interfaces[iface_name] = constants

    return interfaces


def extract_data_constants(filepath: Path) -> dict:
    """Extract inner class names and TestCaseData constants."""
    if not filepath.exists():
        return {}

    content = filepath.read_text(encoding='utf-8', errors='replace')
    result = {}

    # Find inner class/interface blocks with TestCaseData constants
    class_pattern = re.compile(
        r'(?:class|interface)\s+(\w+)\s*\{(.*?)\}',
        re.DOTALL
    )

    for match in class_pattern.finditer(content):
        class_name = match.group(1)
        body = match.group(2)

        constants = []
        const_pattern = re.compile(r'TestCaseData\s+(\w+)\s*=')
        for cm in const_pattern.finditer(body):
            constants.append(cm.group(1))

        if constants:
            result[class_name] = constants

    return result


def extract_annotation_constants(filepath: Path) -> dict:
    """Extract Group and Data constants from AnnotationConstants.java."""
    if not filepath.exists():
        return {}

    content = filepath.read_text(encoding='utf-8', errors='replace')
    result = {'groups': [], 'data': []}

    # Find Group interface
    group_match = re.search(r'interface\s+Group\s*\{(.*?)\}', content, re.DOTALL)
    if group_match:
        for m in re.finditer(r'String\s+(\w+)\s*=\s*"([^"]*)"', group_match.group(1)):
            result['groups'].append({'constant': m.group(1), 'value': m.group(2)})

    # Find Data interface
    data_match = re.search(r'interface\s+Data\s*\{(.*?)\}', content, re.DOTALL)
    if data_match:
        for m in re.finditer(r'String\s+(\w+)\s*=\s*"([^"]*)"', data_match.group(1)):
            result['data'].append({'constant': m.group(1), 'value': m.group(2)})

    return result


def extract_preprocess_groups(filepath: Path) -> list:
    """Extract preProcess groups and the LocalStorage keys they set."""
    if not filepath.exists():
        return []

    content = filepath.read_text(encoding='utf-8', errors='replace')
    groups = []

    # Find preProcess method
    pp_match = re.search(
        r'protected\s+boolean\s+preProcess\s*\(.*?\)\s*\{(.*?)(?=\n\t@Override|\n\tpublic\s|\n\tprotected\s(?!boolean\s+preProcess)|\Z)',
        content,
        re.DOTALL
    )
    if not pp_match:
        return []

    pp_body = pp_match.group(1)

    # Find each group branch
    branch_pattern = re.compile(
        r'(?:if|else\s+if)\s*\(\s*["\']?(\w+)["\']?\s*\.equalsIgnoreCase\s*\(\s*group\s*\)|'
        r'(?:if|else\s+if)\s*\(\s*group\s*\.equalsIgnoreCase\s*\(\s*"(\w+)"\s*\)',
        re.DOTALL
    )

    for match in branch_pattern.finditer(pp_body):
        group_name = match.group(1) or match.group(2)
        if not group_name:
            continue

        # Find the block after this match until next else-if or catch
        start = match.end()
        # Get ~500 chars of the block body
        block = pp_body[start:start + 1000]

        # Extract LocalStorage.store calls
        ls_keys = []
        for ls_match in re.finditer(r'LocalStorage\.store\s*\(\s*"([^"]+)"', block):
            ls_keys.append(ls_match.group(1))

        # Count entity creations
        creates = len(re.findall(r'create\w+GetResponse|createAndGetResponse|createAndGetFullResponse|createChangeGetFullResponse', block))

        groups.append({
            'name': group_name,
            'creates_count': creates,
            'local_storage_keys': ls_keys,
        })

    return groups


def extract_data_json_keys(filepath: Path) -> list:
    """Extract top-level keys from a *_data.json file."""
    if not filepath.exists():
        return []

    try:
        import json
        data = json.loads(filepath.read_text(encoding='utf-8', errors='replace'))
        return sorted(data.keys()) if isinstance(data, dict) else []
    except Exception:
        return []


def build_entity_inventory(module_info: dict, src_roots: list) -> dict:
    """Build complete inventory for one entity, merging from multiple source roots."""
    module = module_info['module']
    entity = module_info['entity']

    inventory = {
        'module': module,
        'entity': entity,
        'actions_util': {'file': None, 'methods': []},
        'api_util': {'file': None, 'methods': []},
        'locators': {'file': None, 'interfaces': {}},
        'data_constants': {'file': None, 'classes': {}},
        'annotation_constants': {'file': None, 'groups': [], 'data': []},
        'preprocess_groups': [],
        'data_json_keys': [],
    }

    # Compute the real relative path from module_info (e.g. admin/automation/workflows)
    entity_real_path = module_info.get('path')  # absolute Path set by find_modules

    for src_root in src_roots:
        # Use real path if it's under this src_root; otherwise reconstruct for alternate src_roots
        if entity_real_path and str(entity_real_path).startswith(str(src_root)):
            base_path = entity_real_path
        elif entity_real_path:
            # For alternate src_roots (--include-original): extract path relative to "modules/"
            parts = entity_real_path.parts
            try:
                mod_idx = parts.index("modules")
                rel_after_modules = Path(*parts[mod_idx:])  # modules/admin/automation/workflows
                base_path = src_root / "com" / "zoho" / "automater" / "selenium" / rel_after_modules
            except ValueError:
                base_path = src_root / "com" / "zoho" / "automater" / "selenium" / "modules" / module / entity
        else:
            base_path = src_root / "com" / "zoho" / "automater" / "selenium" / "modules" / module / entity

        # Utils directory
        utils_dir = base_path / "utils"
        common_dir = base_path / "common"

        # ActionsUtil
        for pattern in [f"{entity.title()}ActionsUtil.java", f"{entity.title().replace('_', '')}ActionsUtil.java"]:
            # Also try CamelCase variations
            pass

        for f in (utils_dir.glob("*ActionsUtil.java") if utils_dir.exists() else []):
            methods = extract_java_methods(f)
            rel_path = str(f.relative_to(src_root))
            if methods and not inventory['actions_util']['methods']:
                inventory['actions_util'] = {'file': rel_path, 'methods': methods}
            elif methods:
                # Merge new methods not already present
                existing_names = {m['name'] for m in inventory['actions_util']['methods']}
                for m in methods:
                    if m['name'] not in existing_names:
                        inventory['actions_util']['methods'].append(m)

        # APIUtil
        for f in (utils_dir.glob("*APIUtil.java") if utils_dir.exists() else []):
            methods = extract_java_methods(f)
            rel_path = str(f.relative_to(src_root))
            if methods and not inventory['api_util']['methods']:
                inventory['api_util'] = {'file': rel_path, 'methods': methods}
            elif methods:
                existing_names = {m['name'] for m in inventory['api_util']['methods']}
                for m in methods:
                    if m['name'] not in existing_names:
                        inventory['api_util']['methods'].append(m)

        # Locators
        for f in (common_dir.glob("*Locators.java") if common_dir.exists() else []):
            interfaces = extract_locator_interfaces(f)
            if interfaces:
                rel_path = str(f.relative_to(src_root))
                if not inventory['locators']['interfaces']:
                    inventory['locators'] = {'file': rel_path, 'interfaces': interfaces}
                else:
                    for iface, consts in interfaces.items():
                        if iface not in inventory['locators']['interfaces']:
                            inventory['locators']['interfaces'][iface] = consts
                        else:
                            existing = set(inventory['locators']['interfaces'][iface])
                            for c in consts:
                                if c not in existing:
                                    inventory['locators']['interfaces'][iface].append(c)

        # DataConstants
        for f in (common_dir.glob("*DataConstants.java") if common_dir.exists() else []):
            classes = extract_data_constants(f)
            if classes:
                rel_path = str(f.relative_to(src_root))
                if not inventory['data_constants']['classes']:
                    inventory['data_constants'] = {'file': rel_path, 'classes': classes}

        # AnnotationConstants
        for f in (common_dir.glob("*AnnotationConstants.java") if common_dir.exists() else []):
            annot = extract_annotation_constants(f)
            if annot.get('groups') or annot.get('data'):
                rel_path = str(f.relative_to(src_root))
                if not inventory['annotation_constants']['groups']:
                    inventory['annotation_constants'] = {
                        'file': rel_path,
                        'groups': annot['groups'],
                        'data': annot['data'],
                    }

        # preProcess groups from parent entity class
        for f in base_path.glob("*.java"):
            if f.name.endswith("Base.java") or f.name.endswith("Util.java"):
                continue
            if f.name.endswith("Constants.java") or f.name.endswith("Locators.java"):
                continue
            if f.name.endswith("Fields.java") or f.name.endswith("DataConstants.java"):
                continue
            groups = extract_preprocess_groups(f)
            if groups and not inventory['preprocess_groups']:
                inventory['preprocess_groups'] = groups

        # Data JSON keys — derive path from real directory structure
        res_root = src_root.parent / "resources"
        # Build the data path matching the actual module directory structure
        if entity_real_path:
            parts = entity_real_path.parts
            try:
                mod_idx = parts.index("modules")
                rel_parts = parts[mod_idx + 1:]  # e.g. ('admin', 'automation', 'workflows')
                leaf_name = rel_parts[-1]  # actual entity dir name
                data_json = res_root / "entity" / "data" / Path(*rel_parts) / f"{leaf_name}_data.json"
            except (ValueError, IndexError):
                data_json = res_root / "entity" / "data" / module / entity / f"{entity}_data.json"
        else:
            data_json = res_root / "entity" / "data" / module / entity / f"{entity}_data.json"
        if data_json.exists():
            keys = extract_data_json_keys(data_json)
            if keys and not inventory['data_json_keys']:
                inventory['data_json_keys'] = keys

    return inventory


def main():
    parser = argparse.ArgumentParser(description="Generate entity inventory YAML files")
    parser.add_argument('module_entity', nargs='?', help='e.g. "changes/change" — omit for all')
    parser.add_argument('--include-original', action='store_true',
                       help='Also scan SDPLIVE_UI_AUTOMATION_BRANCH for existing methods')
    parser.add_argument('--deep', action='store_true',
                       help='Enable deep analysis: data.json fields/placeholders, method internals, preProcess behavior')
    args = parser.parse_args()

    base = Path(BASE_DIR)
    output_dir = base / "config" / "entity_inventory"
    output_dir.mkdir(parents=True, exist_ok=True)

    # Source roots to scan
    src_roots = [base / PROJECT_NAME / "src"]

    if args.include_original:
        original = base / "SDPLIVE_UI_AUTOMATION_BRANCH" / "src"
        if original.exists():
            src_roots.append(original)

    # Always include original branch if it exists (merge knowledge)
    original = base / "SDPLIVE_UI_AUTOMATION_BRANCH" / "src"
    if original.exists() and original not in src_roots:
        src_roots.insert(0, original)  # Original first = baseline

    # Filter source roots to existing ones
    src_roots = [s for s in src_roots if s.exists()]
    if not src_roots:
        print(f"ERROR: No source directories found. Check PROJECT_NAME={PROJECT_NAME}")
        sys.exit(1)

    print(f"Scanning source roots: {[str(s) for s in src_roots]}")

    # Find modules from all source roots
    all_modules = {}
    for src_root in src_roots:
        for m in find_modules(src_root):
            key = f"{m['module']}/{m['entity']}"
            if key not in all_modules:
                all_modules[key] = m

    # Filter if specific module requested
    if args.module_entity:
        target = args.module_entity.strip('/')
        all_modules = {k: v for k, v in all_modules.items() if k == target}
        if not all_modules:
            print(f"ERROR: Module '{target}' not found")
            sys.exit(1)

    # Deep analyzer (optional)
    deep_analyzer = None
    if args.deep:
        from deep_inventory_analyzer import DeepAnalyzer
        deep_analyzer = DeepAnalyzer(src_roots, base)
        print("Deep analysis enabled — analyzing method bodies, data.json content, preProcess behavior")

    generated = 0
    for key, module_info in sorted(all_modules.items()):
        inventory = build_entity_inventory(module_info, src_roots)

        # Deep analysis pass
        if deep_analyzer:
            mod = module_info['module']
            ent = module_info['entity']

            # Deep data.json analysis
            data_deep = deep_analyzer.analyze_data_json(mod, ent)
            if data_deep:
                inventory['data_json_deep'] = {
                    'total_entries': data_deep['total_entries'],
                    'field_frequency': data_deep['field_frequency'],
                    'all_placeholders': data_deep['all_placeholders'],
                    'reuse_groups_count': len(data_deep.get('reuse_groups', {})),
                    'entries': {
                        k: {
                            'fields': v['fields'],
                            'placeholders': v['placeholders'],
                            'local_storage_keys_required': v['local_storage_keys_required'],
                            'purpose': v['purpose'],
                        }
                        for k, v in data_deep['entries'].items()
                    },
                }

            # Deep ActionsUtil analysis
            actions_deep = deep_analyzer.analyze_actions_util(mod, ent)
            if actions_deep:
                inventory['actions_util_deep'] = [
                    {
                        'name': m['name'],
                        'params': m['params'],
                        'locators_used': m['locators_used'],
                        'local_storage_reads': m['local_storage_reads'],
                        'local_storage_writes': m['local_storage_writes'],
                        'action_chain': m['action_chain'],
                        'line_count': m['line_count'],
                    }
                    for m in actions_deep
                ]

            # Deep APIUtil analysis
            api_deep = deep_analyzer.analyze_api_util(mod, ent)
            if api_deep:
                inventory['api_util_deep'] = [
                    {
                        'name': m['name'],
                        'params': m['params'],
                        'api_paths': m['api_paths'],
                        'rest_methods_used': m['rest_methods_used'],
                        'local_storage_writes': m['local_storage_writes'],
                        'local_storage_reads': m['local_storage_reads'],
                    }
                    for m in api_deep
                ]

            # Deep preProcess analysis
            pp_deep = deep_analyzer.analyze_preprocess(mod, ent)
            if pp_deep:
                inventory['preprocess_deep'] = pp_deep

        # Skip empty inventories
        has_content = (
            inventory['actions_util']['methods'] or
            inventory['api_util']['methods'] or
            inventory['locators']['interfaces'] or
            inventory['preprocess_groups'] or
            inventory['data_json_keys'] or
            inventory['data_constants']['classes'] or
            inventory.get('data_json_deep', {}).get('total_entries', 0) > 0
        )
        if not has_content:
            continue

        filename = f"{module_info['module']}_{module_info['entity']}.yaml"
        filepath = output_dir / filename

        # Convert to clean YAML
        with open(filepath, 'w') as f:
            yaml.dump(inventory, f, default_flow_style=False, sort_keys=False, width=120)

        methods_count = len(inventory['actions_util']['methods']) + len(inventory['api_util']['methods'])
        locators_count = sum(len(v) for v in inventory['locators']['interfaces'].values())
        pp_count = len(inventory.get('preprocess_deep', inventory.get('preprocess_groups', [])))
        data_count = inventory.get('data_json_deep', {}).get('total_entries', len(inventory.get('data_json_keys', [])))
        deep_tag = " [DEEP]" if args.deep else ""
        print(f"  ✓ {filename}: {methods_count} methods, {locators_count} locators, "
              f"{pp_count} preProcess groups, {data_count} data entries{deep_tag}")
        generated += 1

    print(f"\nDone. Generated {generated} inventory files in {output_dir}")


if __name__ == '__main__':
    main()
