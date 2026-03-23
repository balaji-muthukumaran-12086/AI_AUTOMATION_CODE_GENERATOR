# Skill: preProcess Patterns

> **When to load**: Writing or modifying preProcess() groups, choosing group values for
> @AutomaterScenario annotations, or adding new data setup logic.

## Rule 1: Minimal Group Selection (D2)

Pick the **lightest** group that satisfies the test method's data needs.

### INCORRECT — heavy group when test only uses getEntityId():
```java
// Test method only calls getEntityId() — no extra entities needed
@AutomaterScenario(
    group = ChangeAnnotationConstants.Group.CREATE_MULTIPLE_CHANGE_FOR_LINKING,  // creates 3 changes!
    dataIds = {ChangeAnnotationConstants.Data.CREATE_CHANGE_FOR_LINKING},
    ...
)
public void verifyChangeTitle() throws Exception {
    actions.navigate.toDetailsPageUsingRecordId(getEntityId());
    // only uses base entity — heavy group wastes 2 extra API calls
}
```

### CORRECT — uses simplest group matching actual data needs:
```java
@AutomaterScenario(
    group = ChangeAnnotationConstants.Group.CREATE,  // creates 1 change only
    dataIds = {ChangeAnnotationConstants.Data.API_VALID_INPUT_GENERAL_TEMPLATE},
    ...
)
public void verifyChangeTitle() throws Exception {
    actions.navigate.toDetailsPageUsingRecordId(getEntityId());
    // only needs base entity — "create" is sufficient
}
```

## Rule 2: Reuse Existing Groups (D3)

### INCORRECT — new group duplicates existing "create" behavior:
```java
// In preProcess():
} else if ("createForDetailView".equalsIgnoreCase(group)) {
    createChangeGetResponse(dataIds[0]);  // SAME as existing "create" group!
}
```

### CORRECT — reuse "create" group, no new code:
```java
@AutomaterScenario(group = "create", ...)  // existing group already does this
```

## Rule 3: LocalStorage Pattern (from real codebase)

### CORRECT — Change.java preProcess, lines 148-165:
```java
} else if ("createAndGetDisplayID".equalsIgnoreCase(group)) {
    JSONObject response = createChangeGetResponse(dataIds[0]);
    LocalStorage.store("display_id",
        AutomaterUtil.getValueAsStringFromInputUsingAPIPath(response, "display_id.display_value"));
    LocalStorage.store(getName(),
        AutomaterUtil.getValueAsStringFromInputUsingAPIPath(response, "id"));
} else if ("createAndAddNote".equalsIgnoreCase(group)) {
    createChangeGetResponse(dataIds[0]);
    String apiPath = getModuleName() + "/" + getEntityId() + "/notes";
    JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[1]);
    String noteID = ChangeAPIUtil.createNoteAndGetId(apiPath, inputData);
    LocalStorage.store("note", noteID);
}
```

## Rule 4: Exception Handling (D16)

### INCORRECT — silent swallow:
```java
} catch (Exception exception) {
    return false;  // test skipped with ZERO visibility — impossible to debug
}
```

### CORRECT — visible failure:
```java
} catch (Exception exception) {
    report.addCaseFlow("Exception occurred while pre processing: " + exception);
    addFailureReport("Pre-process failed", exception.getMessage());
    return false;
}
```

## Decision Flow

```
Does method use any entity?
  NO  → group = "NoPreprocess", dataIds = {}
  YES → Does existing group create what I need?
        YES → REUSE that group. Zero new code.
        NO  → Add new else-if (minimal — only what this test needs)
```
