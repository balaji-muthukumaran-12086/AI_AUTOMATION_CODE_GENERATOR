---
description: "Generate a new preProcess else-if group block for entity data setup"
agent: "test-generator"
---

Generate a new preProcess group for `{{input}}` using this EXACT pattern:

## BEFORE writing any group — check if one already exists:

```bash
# Search existing groups in the entity's preProcess:
grep -n 'equalsIgnoreCase(group)' "$SRC/com/zoho/automater/selenium/modules/{module}/{entity}/{Entity}.java"
# Check entity inventory for all known groups:
cat config/entity_inventory/{module}_{entity}.yaml | grep -A5 'preprocess_groups'
```

**If an existing group creates the same entity + stores the same LocalStorage keys → REUSE IT. Zero new code.**

## New group pattern (ONLY when truly no match exists):

```java
} else if ("{new_group_name}".equalsIgnoreCase(group)) {
    // Step 1: Clean up stale user (if RBAC scenario)
    // actions.deleteScenarioUser(ScenarioUsers.TEST_USER_3);

    // Step 2: Create prerequisite entities via API
    JSONObject response = createEntityGetResponse(dataIds[0]);
    // OR for additional entities:
    // JSONObject extraData = DataUtil.getInputDataForRestAPI(getModuleName(), getName(), dataIds[1], fields);
    // String extraId = restAPI.create(getName(), getModuleName(), getInputData(extraData));

    // Step 3: Store results in LocalStorage for test method access
    LocalStorage.store("{entityName}Id", response.optString("id"));
    LocalStorage.store("{entityName}Name", response.optString("title"));
```

## Exception handling — MANDATORY:

```java
// In the parent try-catch that wraps ALL groups:
} catch (Exception exception) {
    report.addCaseFlow("Exception occurred while pre processing: " + exception);
    addFailureReport("Pre-process failed", exception.getMessage());
    return false;
}
```

## Rules enforced:

- D2: Minimal group selection — only create what the test method actually needs
- D3: Reuse existing groups — check BEFORE adding new else-if
- D7: Data loaded from *_data.json, not inline construction
- D16: ALWAYS addFailureReport in catch — NEVER silent return false
