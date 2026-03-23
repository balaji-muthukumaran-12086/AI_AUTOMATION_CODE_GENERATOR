# Skill: RBAC Testing Patterns

> **When to load**: Generating test scenarios that verify role-based access control,
> permission restrictions, or user-specific behavior.

## The RBAC Lifecycle — 3 Mandatory Phases

### Phase 1: preProcess — Create user with role (admin session)

```java
// From Change.java preProcess — real production code:
} else if ("changeci".equalsIgnoreCase(group)) {
    User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
    actions.createUserByRole(AutomaterConstants.TECHNICIAN, "changes",
        "Change_FullControl_With_CMDB", user);
    LocalStorage.store("TechDisplayId", user.getDisplayId());
    createChangeGetResponse(dataIds[0]);
}
```

**Always clean up first:**
```java
actions.deleteScenarioUser(ScenarioUsers.TEST_USER_3);  // BEFORE createUserByRole
```

### Phase 2: Test method — Switch to role user

```java
// From DetailsView.java — real RBAC test:
public void verifyNoEditPermissionHidesButtons() throws Exception {
    report.startMethodFlowInStepsToReproduce(
        AutomaterUtil.getPascalValueFromCamelCase(getMethodName()));
    try {
        User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
        actions.switchUser(user);  // ← CRITICAL: all UI now runs as this role

        ChangeActionsUtil.navigateToChangesListView();
        actions.listView.columnSearch("Title", LocalStorage.getAsString("changeName"));
        actions.navigate.toDetailsPageUsingRecordId(getEntityId());
        ChangeActionsUtil.navigateToAssociationsTab();

        boolean attachVisible = actions.isElementPresent(
            ChangeLocators.LinkingChange.ATTACH_BUTTON_VISIBLE);

        switchToAdminSession();  // ← Switch back to admin

        if (!attachVisible) {
            addSuccessReport("View-only user cannot see Attach button");
        } else {
            addFailureReport("Button visible for view-only user", "Attach: " + attachVisible);
        }
    } catch (Exception exception) {
        addFailureReport("Internal error: " + getMethodName(), exception.getMessage());
    } finally {
        report.endMethodFlowInStepsToReproduce();
    }
}
```

### Phase 3: Cleanup — Switch back to admin

Always call `switchToAdminSession()` before assertions or after the role test is complete.

## createUserByRole Signature

```java
actions.createUserByRole(
    String userType,      // AutomaterConstants.TECHNICIAN or REQUESTER
    String moduleName,    // "changes", "requests", "problems", "solutions", etc.
    String roleConfigKey, // key in resources/entity/roles/{module}.json or general.json
    User userObject       // from scenarioDetails.getUser(ScenarioUsers.TEST_USER_N)
)
```

## Role JSON Location

| Module | File | Example keys |
|---|---|---|
| Changes | `resources/entity/roles/changes.json` | `SDChangeManager`, `Change_FullControl_With_CMDB` |
| Requests | `resources/entity/roles/requests.json` | `Requester`, `Full_Control`, `View_Only` |
| System | `resources/entity/roles/general.json` | `sdadmin`, `sdsite_admin`, `sdguest` |

## Adding a New Role

```json
// In resources/entity/roles/changes.json:
"Change_ViewOnly": {
    "user": {
        "roles": [{"name": "Change_ViewOnly"}],
        "default_project_role": {"name": "Project Admin"}
    },
    "custom_roles": {
        "Change_ViewOnly": {
            "permissions": [{"name": "chViewOnly"}],
            "description": "View-only access to changes"
        }
    },
    "is_technician": true
}
```

## FORBIDDEN Anti-Patterns

### Running RBAC test as admin — verifies nothing:
```java
// WRONG — admin has ALL permissions, this test proves nothing
public void verifyViewOnlyRestriction() throws Exception {
    // Missing: actions.switchUser(user)
    actions.navigate.toModule(getModuleName());
    if (!actions.isElementPresent(EDIT_BUTTON)) {
        addSuccessReport("Restricted!");  // FALSE POSITIVE — admin may just not see it
    }
}
```

### Forgetting deleteScenarioUser — stale state:
```java
// WRONG — user from prior run may still exist with different role
User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
actions.createUserByRole(AutomaterConstants.TECHNICIAN, "changes", "SDChangeManager", user);
// May fail or use stale user data
```

## Decision Flow

```
Is this scenario about role-based permissions?
  YES → 1. Does role exist in {module}.json or general.json?
        → NO: Add new role entry
        2. Does a preProcess group already create this role user?
        → YES: Reuse that group
        → NO: Add new group with deleteScenarioUser + createUserByRole
        3. Test method: switchUser → test → switchToAdminSession
  NO  → Normal test (no role switching)
```
