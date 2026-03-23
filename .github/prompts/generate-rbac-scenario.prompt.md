---
description: "Generate an RBAC (role-based access control) test scenario"
agent: "test-generator"
---

Generate an RBAC test for `{{input}}` using this EXACT 3-part pattern:

## Part 1 — preProcess group (runs in admin session):

```java
} else if ("{rbac_group}".equalsIgnoreCase(group)) {
    // Step 0: ALWAYS clean up stale user first
    actions.deleteScenarioUser(ScenarioUsers.TEST_USER_3);

    // Step 1: Create user with the target role
    User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
    actions.createUserByRole(
        AutomaterConstants.TECHNICIAN,  // or REQUESTER
        "{moduleName}",                 // "changes", "requests", "problems", etc.
        "{roleConfigKey}",              // key in resources/entity/roles/{module}.json
        user
    );
    LocalStorage.store("techName", user.getDisplayId());

    // Step 2: Create prerequisite test data (still in admin session)
    createEntityGetResponse(dataIds[0]);
}
```

## Part 2 — Test method annotation:

```java
@AutomaterScenario(
    id          = "{ID}",
    group       = {Entity}AnnotationConstants.Group.{RBAC_GROUP},
    priority    = Priority.HIGH,
    dataIds     = {{Entity}AnnotationConstants.Data.{KEY}},
    tags        = {GlobalConstants.Tags.BOTH_SDPMSP},
    description = "Verify user with {role} permission can/cannot {action}",
    owner       = OwnerConstants.{OWNER},
    runType     = ScenarioRunType.USER_BASED
)
```

## Part 3 — Test method body (switches to role user):

```java
public void verify{Role}{Action}() throws Exception {
    report.startMethodFlowInStepsToReproduce(AutomaterUtil.getPascalValueFromCamelCase(getMethodName()));
    try {
        // Switch to the role user — ALL subsequent UI runs under their permissions
        User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
        actions.switchUser(user);

        // Navigate and test under restricted role
        actions.navigate.toModule(getModuleName());
        // ... test what this role CAN or CANNOT do ...

        // Switch back to admin when done
        switchToAdminSession();

        // Assert
        if ({condition}) {
            addSuccessReport("{ID}: Role restriction confirmed");
        } else {
            addFailureReport("{what failed}", "{detail}");
        }
    } catch (Exception exception) {
        addFailureReport("Internal error: " + getMethodName(), exception.getMessage());
    } finally {
        report.endMethodFlowInStepsToReproduce();
    }
}
```

## Role JSON lookup (resources/entity/roles/):

| Module | File | Example keys |
|---|---|---|
| Changes | changes.json | SDChangeManager, Change_FullControl_With_CMDB |
| Requests | requests.json | Requester, Full_Control, View_Only |
| System | general.json | sdadmin, sdsite_admin, sdguest |

## FORBIDDEN:

- Running RBAC tests as admin (verifies nothing about role restrictions)
- Forgetting `actions.switchUser(user)` (test runs in admin session)
- Missing `deleteScenarioUser()` before `createUserByRole()` (stale state)
