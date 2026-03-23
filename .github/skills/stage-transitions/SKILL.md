---
applyTo: "**/*Stage*.java,**/*Workflow*.java"
---
# Skill: Change Stage Transition Patterns

> **When to load**: Writing tests that close changes, advance stages, or verify
> stage-specific behavior (e.g., Planning → CAB → Implementation → Close).

## The Close Change Pattern — Full Lifecycle

SDP changes have 8 sequential stages. Closing requires SDChangeManager privilege
and advancing through ALL stages via API.

### Stage Order (mandatory sequence)
```
Submission → Planning → CAB Evaluation → Implementation → UAT → Release → Review → Close
```

### Why Admin Can't Close Changes
- Admin (Blaze) does NOT have SDChangeManager role
- Subscription admin role can't be modified
- Solution: create a technician with SDChangeManager role

### preProcess Pattern — CORRECT
```java
// Step 0: Clean slate
deleteScenarioUser(ScenarioUsers.TEST_USER_3);

// Step 1: Create tech with SDChangeManager role
User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
actions.createUserByRole(AutomaterConstants.TECHNICIAN, "changes", "SDChangeManager", user);

// Step 2: Create change with tech as change_manager
LocalStorage.store("tech_name", user.getDisplayId());
// change_data.json entry must have: "change_manager": {"name": "$(custom_tech_name)"}
JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[0]);
JSONObject response = restAPI.createAndGetResponse(getName(), getModuleName(), getInputData(inputData));
String changeId = response.getString("id");
LocalStorage.store(getName(), changeId);

// Step 3: Switch to tech user, advance through all stages
actions.switchUser(user);
String[] stages = {"Planning", "CAB Evaluation", "Implementation", "UAT", "Release", "Review", "Close"};
for (String stage : stages) {
    JSONObject stageData = new JSONObject();
    stageData.put("change", new JSONObject()
        .put("stage", new JSONObject().put("name", stage))
        .put("status", new JSONObject().put("name", stage.equals("Close") ? "Completed" : "In Progress"))
        .put("comment", "Advancing to " + stage));
    restAPI.update("changes/" + changeId, stageData);
}
switchToAdminSession();
```

### CRITICAL Rules

| Rule | Why |
|------|-----|
| NEVER send `closure_code` field | Returns `EXTRA_KEY_FOUND_IN_JSON` error |
| SDChangeManager role required | Admin without this role CANNOT close changes |
| `change_manager` must be the tech user | Only change_manager can advance stages |
| API may pick different status | But DOES advance the stage correctly |
| Tests only check `stage.name == "Close"` | Specific status within Close doesn't matter |
| `deleteScenarioUser()` before `createUserByRole()` | Clean slate from prior runs |

### INCORRECT — Common Mistakes
```java
// ❌ Trying to close as admin — will fail
restAPI.update("changes/" + changeId, closeData);  // admin lacks SDChangeManager

// ❌ Sending closure_code
stageData.put("closure_code", new JSONObject().put("name", "Successful"));  // EXTRA_KEY error

// ❌ Skipping stages — jumping from Submission to Close
// API rejects non-sequential stage transitions
```

### Role JSON Entry (resources/entity/roles/changes.json)
```json
"SDChangeManager": {
    "user": {
        "roles": [{"name": "SDChangeManager"}, {"name": "SDAdmin"}],
        "default_project_role": {"name": "Project Admin"}
    },
    "is_technician": true
}
```
