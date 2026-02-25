"""
module_indexer.py
-----------------
Builds a hierarchical module index from parsed test files.
Output: knowledge_base/raw/module_index.json

Produces:
  {
    "modules": {
      "requests/request": {
        "entity": "request",
        "module": "requests",
        "scenario_files": [...],
        "fields_file": "...",
        "data_constants_file": "...",
        "locators_file": "...",
        "scenario_count": N,
        "scenarios": [{ id, method_name, description, tags, priority, group }]
      },
      ...
    },
    "stats": { "total_scenarios": N, "total_modules": N }
  }
"""

import json
from pathlib import Path
from collections import defaultdict


def build_module_index(parsed_json_path: str, output_path: str) -> dict:
    """Build module index from parsed test case JSON."""
    with open(parsed_json_path, encoding='utf-8') as f:
        records = json.load(f)

    index = defaultdict(lambda: {
        'entity': '',
        'module': '',
        'scenario_files': [],
        'fields_file': None,
        'data_constants_file': None,
        'locators_file': None,
        'constants_file': None,
        'utils_files': [],
        'scenario_count': 0,
        'scenarios': [],
        'roles': [],
        'suite_role': '',
        'suite_owner': '',
    })

    for rec in records:
        mp = rec.get('module_path', '')
        if not mp or mp.startswith('base') or mp.startswith('standalone'):
            continue

        entry = index[mp]
        parts = mp.split('/')
        entry['entity'] = rec.get('entity_name', parts[-1])
        entry['module'] = parts[1] if len(parts) > 1 else parts[0]

        ftype = rec.get('file_type', 'OTHER')
        fpath = rec.get('file_path', '')
        class_name = rec.get('class_name', '')

        if ftype == 'SCENARIO':
            if fpath not in entry['scenario_files']:
                entry['scenario_files'].append(fpath)
            entry['suite_role'] = rec.get('suite', {}).get('role', '')
            entry['suite_owner'] = rec.get('suite', {}).get('owner', '')
            for sc in rec.get('scenarios', []):
                entry['scenarios'].append({
                    'id': sc.get('id', ''),
                    'method_name': sc.get('method_name', ''),
                    'description': sc.get('description', ''),
                    'tags': sc.get('tags', []),
                    'priority': sc.get('priority', 'MEDIUM'),
                    'group': sc.get('group', ''),
                    'run_type': sc.get('run_type', ''),
                    'data_ids': sc.get('data_ids', []),
                    'class': class_name,
                })
            entry['scenario_count'] = len(entry['scenarios'])

        elif ftype == 'FIELDS':
            entry['fields_file'] = fpath
        elif ftype == 'DATA_CONSTANTS':
            entry['data_constants_file'] = fpath
        elif ftype == 'LOCATORS':
            entry['locators_file'] = fpath
        elif ftype == 'CONSTANTS':
            entry['constants_file'] = fpath
        elif ftype == 'UTILS':
            if fpath not in entry['utils_files']:
                entry['utils_files'].append(fpath)
        elif ftype == 'ROLE':
            if class_name not in entry['roles']:
                entry['roles'].append(class_name)

    total_scenarios = sum(v['scenario_count'] for v in index.values())
    result = {
        'modules': dict(index),
        'stats': {
            'total_modules': len(index),
            'total_scenarios': total_scenarios,
        }
    }

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"  ✅ Module index: {len(index)} modules, {total_scenarios} scenarios → {output_path}")
    return result


def build_scenario_flat_list(module_index: dict, output_path: str) -> list:
    """
    Flatten all scenarios to a single list for vector store ingestion.
    Each item is a chunk ready for embedding.
    """
    flat = []
    for module_path, mod in module_index['modules'].items():
        for sc in mod.get('scenarios', []):
            flat.append({
                'id': sc['id'],
                'module_path': module_path,
                'entity': mod['entity'],
                'module': mod['module'],
                'class': sc['class'],
                'method_name': sc['method_name'],
                'description': sc['description'],
                'tags': sc['tags'],
                'priority': sc['priority'],
                'group': sc['group'],
                'run_type': sc['run_type'],
                'data_ids': sc['data_ids'],
                'suite_role': mod['suite_role'],
                # Text for embedding
                'embed_text': (
                    f"Module: {module_path} | "
                    f"Entity: {mod['entity']} | "
                    f"Test ID: {sc['id']} | "
                    f"Method: {sc['method_name']} | "
                    f"Description: {sc['description']} | "
                    f"Tags: {', '.join(sc['tags'])} | "
                    f"Priority: {sc['priority']} | "
                    f"Group: {sc['group']}"
                )
            })

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(flat, f, indent=2, ensure_ascii=False)

    print(f"  ✅ Flat scenario list: {len(flat)} scenarios → {output_path}")
    return flat


if __name__ == '__main__':
    base = Path(__file__).resolve().parents[1]
    kb = base / 'knowledge_base' / 'raw'

    index = build_module_index(
        str(kb / 'testcases_parsed.json'),
        str(kb / 'module_index.json')
    )
    build_scenario_flat_list(
        index,
        str(kb / 'scenarios_flat.json')
    )
