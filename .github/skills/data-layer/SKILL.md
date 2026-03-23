# Skill: Data Layer Patterns

> **When to load**: Creating *_data.json entries, using DataConstants/AnnotationConstants,
> loading test data in methods or preProcess, or working with $(custom_KEY) placeholders.

## Rule 1: JSON Format (D6, D7)

### INCORRECT — flat string for lookup field:
```json
"create_change_bad": {
    "data": {
        "title": "Test Change",
        "priority": "High",
        "change_type": "Standard"
    }
}
```

### CORRECT — proper lookup objects + wrapper + placeholders:
```json
"valid_input_general_template": {
    "data": {
        "title": "Change Live $(unique_string)",
        "template": {"name": "General Template"},
        "description": "CH Live",
        "risk": {"name": "High"},
        "change_type": {"name": "Major"},
        "change_requester": {"name": "$(user_name)"},
        "priority": {"name": "High"},
        "scheduled_start_time": {"value": "$(datetime, 2Y 10M 100D 10h 10m, false)"},
        "category": {"name": "Operating System"},
        "subcategory": {"name": "Fedora Core"}
    }
}
```

## Rule 2: Three Loading Methods — Never Mix (D5)

### Test method body → getTestCaseData(DataConstants):
```java
// CORRECT
JSONObject inputData = getTestCaseData(ChangeDataConstants.ChangeData.MY_KEY);
// FORBIDDEN
JSONObject inputData = getTestCaseData("my_key");  // raw string
```

### preProcess() → getTestCaseDataUsingCaseId(dataIds[N]):
```java
// CORRECT — inside preProcess
JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[0]);
// FORBIDDEN — getTestCaseDataUsingFilePath inside preProcess
JSONObject data = DataUtil.getTestCaseDataUsingFilePath(PATH, dataIds[0]);
```

### APIUtil (static) → DataUtil.getTestCaseDataUsingFilePath:
```java
// CORRECT — inside static APIUtil method
public final class ChangeAPIUtil extends Utilities {
    private static final String PATH = "data" + File.separator + "changes"
        + File.separator + "change" + File.separator + "change_data.json";

    public static void createDowntime(String data) throws Exception {
        JSONObject inputData = DataUtil.getTestCaseDataUsingFilePath(
            AutomaterUtil.getResourceFolderPath() + PATH, data);
        restAPI.createAndGetResponse("downtime",
            LocalStorage.getAsString("apiPath") + "/downtimes", inputData);
    }
}
```

## Rule 3: LocalStorage Pre-Seed — Reuse Instead of Duplicate (D7)

### INCORRECT — new JSON entry just for a different template:
```json
"create_change_special_template": {
    "data": {
        "title": "Change $(unique_string)",
        "template": {"name": "My Special Template"}
    }
}
```

### CORRECT — pre-seed LocalStorage, reuse existing entry:
```java
// Existing entry has: "template": {"name": "$(custom_template_name)"}
LocalStorage.store("template_name", "My Special Template");
JSONObject inputData = getTestCaseData(ChangeDataConstants.ChangeData.VALID_INPUT_GENERAL_TEMPLATE);
// $(custom_template_name) resolves from LocalStorage automatically
```

> **Caching warning**: DataUtil caches by key. Pre-seed BEFORE the first load.

## Rule 4: DataConstants Inner Class Naming (D17)

```
change_workflow_data.json  →  ChangeWorkflowData  (NOT ChangeData)
solution_data.json         →  SolutionData
request_data.json          →  RequestData
```

Always check the actual file before referencing the inner class name.

## Rule 5: AnnotationConstants vs DataConstants

| Class | Purpose | Used by |
|---|---|---|
| `{Entity}AnnotationConstants.Data.KEY` | preProcess data IDs | `@AutomaterScenario(dataIds = {...})` |
| `{Entity}DataConstants.{Inner}.KEY` | Test method UI data | `getTestCaseData(DataConstants.Inner.KEY)` |

These are **separate files**. Never interchange them.

## Rule 6: FORBIDDEN — Inline JSON Construction (D6)

```java
// FORBIDDEN — building entity data from scratch
JSONObject change = new JSONObject();
change.put("title", "Test");
change.put("priority", new JSONObject().put("name", "High"));

// ALLOWED — post-load modification
JSONObject data = DataUtil.getTestCaseDataUsingFilePath(PATH, "create_change");
data.getJSONObject("change").put("custom_field", dynamicValue);  // OK — modifying loaded data
```
