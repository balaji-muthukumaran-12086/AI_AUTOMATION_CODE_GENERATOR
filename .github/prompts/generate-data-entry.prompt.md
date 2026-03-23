---
description: "Generate a new test data JSON entry in *_data.json"
agent: "test-generator"
---

Generate a data entry for `{{input}}` using this EXACT format:

## BEFORE creating — check if a reusable entry already exists:

```bash
# List all existing keys in the data file:
python3 -c "import json; d=json.load(open('{DATA_JSON_PATH}')); [print(k) for k in d.keys()]"
# Check entity inventory for all data entries:
cat config/entity_inventory/{module}_{entity}.yaml | grep -A2 'data_json_entries'
```

**If an existing entry has $(custom_KEY) placeholders → pre-seed LocalStorage and REUSE it.**

## data.json entry — EXACT structure:

```json
"{snake_case_key}": {
    "data": {
        "title": "{Entity} $(unique_string)",
        "template": {"name": "$(custom_template_name)"},
        "priority": {"name": "High"},
        "category": {"name": "Hardware"},
        "description": "Auto-generated test data",
        "requester": {"name": "$(user_name)"}
    }
}
```

## Field format rules:

| Field type | JSON format | Example |
|---|---|---|
| Plain text | `"field": "value"` | `"title": "Test $(unique_string)"` |
| Lookup/dropdown | `"field": {"name": "Value"}` | `"priority": {"name": "High"}` |
| Boolean | `true` / `false` (JSON native) | `"is_public": false` |
| Date | `"field": {"value": "$(datetime, ...)"}` | `"start_time": {"value": "$(datetime, 1D 0M, true)"}` |
| Dynamic value | `$(custom_KEY)` | `"template": {"name": "$(custom_template)"}` |

## FORBIDDEN:

- Missing `{"data": {...}}` wrapper
- Flat string for lookups: `"priority": "High"` (MUST be `{"name": "High"}`)
- String booleans: `"is_public": "true"` (MUST be native `true`)
- Inline JSONObject in Java: `new JSONObject().put(...)` (MUST be in data.json)
