---
description: "Use when editing test data JSON files, creating new data entries for test scenarios, or working with placeholder values like $(unique_string) and $(custom_KEY) in the AutomaterSelenium framework."
applyTo: ["SDPLIVE_LATEST_AUTOMATER_SELENIUM/resources/entity/data/**/*.json", "AutomaterSelenium/resources/entity/data/**/*.json"]
---

# Test Data JSON Format — AutomaterSelenium

## Structure

Every data entry must follow this format:
```json
"my_data_key": {
  "data": {
    "subject":   "Test Subject $(unique_string)",
    "priority":  {"name": "High"},
    "requester": {"name": "$(user_name)"},
    "is_public": false
  }
}
```

## Rules

1. **Always wrap with `{"data": {...}}`** — no exceptions
2. **Lookup/dropdown fields** = `{"name": "Value"}` object, NEVER a flat string
3. **Boolean** = `true`/`false`, NOT the string `"true"`
4. **Key naming**: snake_case matching the `TestCaseData` constant name (e.g., `SOL_UNAPPROVED_PUB` → `sol_unapproved_pub`)

## Data Reuse (Critical)

Before creating any new entry:
1. Read ALL existing top-level keys in this file
2. Check `*AnnotationConstants.java → Data` interface for preProcess data IDs
3. Check `*DataConstants.java` for declared `TestCaseData` constants
4. **Reuse** an existing entry if it covers the same payload — only create new when field combination is genuinely different

## LocalStorage Pre-Seed (Preferred over Duplication)

If a JSON entry has `$(custom_KEY)` placeholders, pre-seed `LocalStorage` before calling `getTestCaseData()`:
```java
// Reuse existing JSON entry by providing a specific value via LocalStorage
LocalStorage.store("template_name", LocalStorage.getAsString("createdTemplateName"));
JSONObject inputData = getTestCaseData(DataConstants.CREATE_WITH_TEMPLATE);
// $(custom_template_name) resolves automatically
```

## Placeholder Reference

| Placeholder | Resolves To |
|---|---|
| `$(unique_string)` | Millisecond timestamp |
| `$(custom_KEY)` | `LocalStorage.fetch("KEY")` |
| `$(user_name)` | Scenario user's display name |
| `$(user_email_id)` | Scenario user's email |
| `$(admin_email_id)` | Admin email |
| `$(date, N, ahead)` | Date N days ahead (milliseconds) |
| `$(datetime, N, ahead)` | Datetime N days ahead (milliseconds) |
