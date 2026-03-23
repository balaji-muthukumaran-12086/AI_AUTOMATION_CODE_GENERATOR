---
description: "Use when editing Java test files, writing @AutomaterScenario annotations, creating Locators interfaces, writing ActionsUtil/APIUtil methods, or modifying test base classes in the AutomaterSelenium framework."
applyTo: ["**/src/**/*.java"]
---

# Java Test Conventions — AutomaterSelenium

## @AutomaterScenario — All 9 Fields Required

```java
@AutomaterScenario(
    id          = "SDPOD_AUTO_...",
    group       = "...",
    priority    = Priority.MEDIUM,
    dataIds     = {...},
    tags        = {},
    description = "...",
    owner       = OwnerConstants.RAJESHWARAN_A,
    runType     = ScenarioRunType.USER_BASED,      // NEVER omit — default is PORTAL_BASED
    switchOn    = SwitchToUserSession.AFTER_PRE_PROCESS
)
```

## Test ID Source — Use-Case Document vs Fallback

**When a use-case CSV is provided** (in `$PROJECT_NAME/Testcase/`):
- **Use the CSV's use-case ID directly** in `@AutomaterScenario(id = "...")` — this is the ONLY place the use-case ID appears
- Do NOT embed the use-case ID in method names, DataConstants names, data JSON keys, or locator names
- Method names must be descriptive of the action (e.g. `verifyDetailViewTitle`), not derived from the ID

**When no use-case document is provided** (feature description / single-line case):
- Fall back to auto-generated sequential IDs per module prefix (e.g. `SDPOD_AUTO_SOL_DV_###`)
- Grep for the next available ID before assigning:

```bash
grep -rn 'id = "SDPOD_AUTO_SOL_DV' $PROJECT_NAME/src/ | sed 's/.*id = "\([^"]*\)".*/\1/' | sort | tail -1
```

## Multi-ID Grouping — Covering Multiple Manual Cases in One Method

When multiple manual test cases from the use-case document can be covered by a single automation method, comma-separate the IDs:

```java
@AutomaterScenario(
    id = "SDPOD_AUTO_REQ_LST_UPDATED_BY_028,SDPOD_AUTO_REQ_LST_UPDATED_BY_029",
    ...
)
```

**Rules:**
- Only group cases genuinely validated within the same method — do not pad IDs
- All grouped IDs must share the same module prefix
- The `description` should summarize the combined coverage

## Boolean / Checkbox Trap

`fillInputForAnEntity` calls `getValueAsStringFromInputUsingAPIPath()` which returns `null` for JSON booleans → boolean fields are **silently skipped**. Handle checkboxes manually:
```java
actions.click(Locators.CHECKBOX_LOCATOR);  // explicit click
```

## UNIVERSAL RULE — UI-Only Test Method Bodies + Feature Under Test Separation

This is a **UI automation framework**. Test method bodies MUST only exercise UI flows (Selenium clicks, navigation, form fills, `isElementPresent`, `getText`, etc.). **API calls in test method bodies are FORBIDDEN** — they turn the test into API testing. Only `preProcess` should use API calls — and **only for raw entity creation and state setup**, NOT for performing the feature being tested.

**Critical distinction:**
- **"Data creation"** = creating entities that need to EXIST (changes, users, templates) → API in preProcess ✅
- **"State setup"** = setting entities into a state needed before the test (trash, close) → API in preProcess ✅
- **"Feature under test"** = the action/flow the test verifies (linking, associating, approval flow) → **UI in test method ONLY** ✅

```java
// ❌ FORBIDDEN — Feature under test (linking) done via API in preProcess
} else if ("createAndLinkChild".equalsIgnoreCase(group)) {
    createChangeGetResponse(dataIds[0]);
    ChangeAPIUtil.linkChildChange(sourceId, childId);  // ← Wrong! Linking IS the test
}

// ✅ CORRECT — preProcess only creates entities; test method links via UI
// In preProcess:
createChangeGetResponse(dataIds[0]);  // parent
JSONObject child = ChangeAPIUtil.createChangeGetFullResponse(dataIds[0]);  // child
LocalStorage.store("childName", child.optString("title"));
// NO linking — that's the test method's responsibility

// In test method:
ChangeActionsUtil.navigateToAssociationsTab();      // UI click
ChangeActionsUtil.openAttachPopup("Child Changes");  // UI click
ChangeActionsUtil.searchAndSelectChange(childName);  // UI interaction
ChangeActionsUtil.clickAssociateButton();             // UI click
```

## FORBIDDEN — Inline JSONObject Construction for Test Data

All test data (UI form inputs AND preProcess API payloads) MUST be defined in `*_data.json` files and loaded via `getTestCaseData()` or `getTestCaseDataUsingCaseId()`. Never construct JSONObject payloads inline.

```java
// ❌ FORBIDDEN — bloated, non-reusable, bypasses placeholders
JSONObject inputData = new JSONObject();
inputData.put("title", "Test " + System.currentTimeMillis());
inputData.put("priority", new JSONObject().put("name", "High"));

// ✅ CORRECT — data in JSON file, loaded via DataConstants
JSONObject inputData = getTestCaseData(ChangeDataConstants.ChangeData.CREATE_CHANGE);
```

For dynamic values, use `$(custom_KEY)` placeholders in JSON + `LocalStorage.store("KEY", value)` before `getTestCaseData()`.

## Test Data Loading Methods — Correct Context (REQUIRED)

Three methods exist for loading test data. **Each has a specific context — mixing them is FORBIDDEN.**

| Method | Where to use | Parameter |
|--------|-------------|-----------|
| `getTestCaseData(TestCaseData)` | **Test method body** | `DataConstants` constant |
| `getTestCaseDataUsingCaseId(dataIds[N])` | **preProcess() only** | Raw string from `dataIds` array |
| `DataUtil.getTestCaseDataUsingFilePath(path, caseId)` | **APIUtil files** (static methods) | Explicit file path + case ID |

```java
// ✅ CORRECT — preProcess
JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[0]);

// ✅ CORRECT — APIUtil (static, no Entity context)
JSONObject data = DataUtil.getTestCaseDataUsingFilePath(
    AutomaterUtil.getResourceFolderPath() + PATH, caseId);

// ✅ CORRECT — test method body
JSONObject inputData = getTestCaseData(SolutionDataConstants.SolutionData.MY_KEY);

// ❌ FORBIDDEN — getTestCaseDataUsingCaseId in APIUtil (no Entity instance)
// ❌ FORBIDDEN — getTestCaseDataUsingFilePath in preProcess (use getTestCaseDataUsingCaseId)
```

## `waitForAjaxComplete()` — NEVER Add Redundantly (STRICT)

Most framework actions already call `waitForAjaxComplete()` internally. Adding it again is **dead code** that clutters methods and slows execution.

**Actions that ALREADY call `waitForAjaxComplete()` internally — NEVER add before/after these:**

| Method | Internal wait behaviour |
|--------|------------------------|
| `actions.click(locator)` | Calls `waitForAjaxComplete()` **before** the click |
| `actions.type(locator, value)` | Calls `waitForAjaxComplete()` internally |
| `actions.sendKeys(locator, value)` | Calls `waitForAjaxComplete()` internally |
| `actions.getText(locator)` | Calls `waitForAjaxComplete()` internally |
| `actions.navigate.to(locator)` | Calls `click()` + `waitForAjaxCompleteLoad()` — double-wait |
| `actions.navigate.toModule(name)` | Calls `to()` + additional `waitForAjaxComplete()` — fully waited |
| `actions.navigate.toDetailsPageUsingRecordId(id)` | Calls `waitForAnElementToAppear` + `to()` + `waitForAjaxComplete()` |
| `actions.formBuilder.submit()` | Calls `waitForAjaxComplete()` internally |
| `actions.popUp.clickByName(name)` | Calls `waitForAjaxComplete()` internally |

**The ONLY valid uses of explicit `waitForAjaxComplete()`:**
1. After `actions.executeScript(...)` that triggers AJAX
2. After `Thread.sleep(...)` where the next read depends on AJAX
3. After a `type()` into a **live-search field** where AJAX-loaded dropdown options must appear before the next `click()`

```java
// ❌ REDUNDANT — click already waits internally
actions.click(TAB);
actions.waitForAjaxComplete();  // DEAD CODE — remove
actions.click(BUTTON);

// ❌ REDUNDANT — trailing waitForAjaxComplete after consecutive clicks
actions.click(DROPDOWN);
actions.click(OPTION);
actions.waitForAjaxComplete();  // DEAD CODE if next line is another click or getText

// ✅ CORRECT — no unnecessary waits
actions.click(TAB);
actions.click(BUTTON);

// ✅ CORRECT — explicit wait after executeScript triggers AJAX
actions.executeScript("some.ajaxTrigger()");
actions.waitForAjaxComplete();
String text = actions.getText(RESULT);
```

> **Audit rule**: When reviewing generated code, delete every `waitForAjaxComplete()` that follows
> a `click()`, `type()`, `sendKeys()`, `getText()`, `navigate.*()`, or `submit()` call unless
> there is a non-framework action (e.g., `Thread.sleep`, `executeScript`) between them.

## ActionsUtil — Generic Parameterized Methods (MANDATORY)

> **Root cause of past bloat**: The AI created near-duplicate methods that differ only in one string
> argument (e.g., `openAttachParentChangePopup()` and `openAttachChildChangesPopup()`).
> This is **FORBIDDEN**. Always parameterize.

### Rule: One method per UI operation pattern, parameterized for variants

Before creating any new ActionsUtil method, ask: **"Does another method already do the same sequence with a different value?"** If yes → merge into one parameterized method.

```java
// ❌ FORBIDDEN — near-duplicate methods differing only by a string
public static void openAttachParentChangePopup() throws Exception {
    actions.click(ChangeLocators.LinkingChange.ATTACH_BUTTON_DROPDOWN);
    actions.click(ChangeLocators.LinkingChange.ATTACH_DROPDOWN_OPTION.apply("Parent Change"));
}
public static void openAttachChildChangesPopup() throws Exception {
    actions.click(ChangeLocators.LinkingChange.ATTACH_BUTTON_DROPDOWN);
    actions.click(ChangeLocators.LinkingChange.ATTACH_DROPDOWN_OPTION.apply("Child Changes"));
}

// ✅ CORRECT — single parameterized method
public static void openAttachPopup(String associationType) throws Exception {
    actions.click(ChangeLocators.LinkingChange.ATTACH_BUTTON_DROPDOWN);
    actions.click(ChangeLocators.LinkingChange.ATTACH_DROPDOWN_OPTION.apply(associationType));
}
```

### When to use LocalStorage as implicit params vs explicit method params:

| Pattern | Use |
|---------|-----|
| **Explicit params** (preferred) | When the caller already has the value in a variable — pass it directly |
| **LocalStorage** | When the value is set by preProcess and flows across multiple methods — read via `LocalStorage.getAsString("key")` inside the method |

```java
// ✅ Explicit param — caller has the value
ChangeActionsUtil.openAttachPopup("Parent Change");

// ✅ LocalStorage — value set by preProcess, used by multiple methods
LocalStorage.store("associationType", "Parent Change");
ChangeActionsUtil.openAttachPopup(LocalStorage.getAsString("associationType"));
```

### Decision flow for every new ActionsUtil method:

```
Does an existing method perform the same UI steps with different string values?
  → YES: Add a parameter to the existing method (or create a new parameterized one
         if the existing method is shared across projects and cannot be modified).
  → NO:  Create a new method.

Can the method be described as a single step in manual testing?
  → YES: Good granularity — proceed.
  → NO (too granular — e.g., just one click): Expand to cover the full UI operation.
  → NO (too broad — e.g., entire test flow): Split into smaller operations.
```

### Methods that should NOT exist in ActionsUtil (too thin / already framework methods):

```java
// ❌ FORBIDDEN — wrapper around a single framework call with no added logic
public static void navigateToChangesModule() throws Exception {
    actions.navigate.toModule(ModuleConstants.CHANGES);  // just call this directly
}

// ❌ FORBIDDEN — wrapper around a single click
public static void clickSaveButton() throws Exception {
    actions.click(ChangeLocators.SAVE_BUTTON);  // inline this in the caller
}

// ✅ CORRECT — multi-step operation that encapsulates a complete UI flow
public static void gotoChangeDetailsPage() throws Exception {
    actions.navigate.toModule(ModuleConstants.CHANGES);
    pageSetup();
    actions.listView.columnSearch("Title", LocalStorage.getAsString("changeName"));
    actions.navigate.toDetailsPageUsingRecordId(LocalStorage.getAsString("changeId"));
}
```

## ActionUtils / APIUtil Pattern (Mandatory)

Test method body = utility calls + assertions ONLY. No inline `actions.click()` sequences.

```java
// ✅ Correct
public void verifyDetailView() throws Exception {
    ChangeActionsUtil.openAssociationTab();
    ChangeActionsUtil.linkParentChangeViaUI(name, id);
    if (actions.isElementPresent(locator)) {
        addSuccessReport("ID: Description");
    }
}

// ❌ Wrong — inline actions in test body
public void verifyDetailView() throws Exception {
    actions.click(ChangeLocators.LinkingChange.LHS_ASSOCIATION_TAB);
    actions.waitForAjaxComplete();
    // ... more inline actions
}
```

## Existing Method Protection (shared across projects)

**Do NOT modify existing `public static` methods in `*ActionsUtil.java` or `*APIUtil.java`** — they are shared across projects. Altering signatures, behaviour, or return types can break callers in other projects.

**Exception**: If a method has **minimal usage** (1–2 callers, current project only), it MAY be modified if:
1. ALL callers are updated to match
2. ALL affected files compile with zero errors
3. If compilation fails → revert and create a new method instead

**Preferred**: Create a new method with a different name rather than altering an existing one.

## APIUtil Data Flow (MANDATORY — NEVER construct JSON inline)

**Every new APIUtil method that sends data to an API** MUST load from `*_data.json`. NEVER build payloads with `new JSONObject().put(...)`.

**Required flow:**
1. Create a data entry in `*_data.json` with `$(custom_KEY)` placeholders for dynamic values
2. Define `PATH` constant in the APIUtil class pointing to the data file
3. Store dynamic values via `LocalStorage.store("KEY", value)` before loading
4. Load via `DataUtil.getTestCaseDataUsingFilePath(AutomaterUtil.getResourceFolderPath() + PATH, caseId)`
5. DataConstants are auto-generated — via `./generate_constants.sh` (manual), automatically by `runner_agent.py` before test execution, or by the `@test-generator` agent's Step P0 (generate-only mode). Callers reference `DataConstants.Data.KEY`

```java
// ✅ CORRECT — data in JSON, loaded via DataUtil
public static void linkParentChange(String changeId, String targetChangeId) throws Exception {
    LocalStorage.store("target_change_id", targetChangeId);
    JSONObject inputData = DataUtil.getTestCaseDataUsingFilePath(
        AutomaterUtil.getResourceFolderPath() + PATH, "link_parent_change_api");
    restAPI.update("changes/" + changeId + "/link_parent_change", inputData);
}

// ❌ FORBIDDEN — inline JSON in APIUtil
public static void linkParentChange(String changeId, String targetChangeId) throws Exception {
    JSONObject parentChangeObj = new JSONObject().put("id", targetChangeId);
    JSONObject wrapper = new JSONObject().put("parent_change", parentChangeObj);
    // NEVER do this — all data belongs in *_data.json
}
```

> Existing codebase has legacy inline JSON in APIUtil files — do NOT follow that pattern.
> All **newly generated** APIUtil methods MUST use `*_data.json` entries.

> **Post-load modification IS allowed**: After loading from `*_data.json`, you MAY use `.put()` / `.remove()` to tweak the JSONObject (e.g., conditionally adding a field). The rule: core data **creation** lives in JSON; post-load **transformation** in Java is acceptable.

## API Reference (MANDATORY — consult before any API call)

Before writing any REST API path or input wrapper (in preProcess, APIUtil, or sdpAPICall), **read the relevant module section** in `docs/api-doc/SDP_API_Endpoints_Documentation.md`. Contains exact V3 paths, HTTP methods, input wrappers, sub-resource paths, and worked examples for all 16 modules. Do NOT guess API paths.

## preProcess Groups

- `preProcess()` is an **abstract method** defined in `Entity.java`: `protected abstract boolean preProcess(String group, String[] dataIds);`
- It is often implemented in the **module parent class** (e.g., `Change.java`, `Solution.java`), but **subclasses can and do override it**
- **Discovery order (mandatory):**
  1. Check the leaf/subclass file for a `preProcess()` override — if present, that is authoritative
  2. If it ends with `return super.preProcess(group, dataIds)`, also read the parent
  3. If no override in subclass, fall back to the parent class
- Read parent's existing groups before adding new ones
- Reuse existing groups when they create the same entity type + store the same LocalStorage keys
- FORBIDDEN: Inventing group names not found in the entity's `preProcess()` if/else-if or switch/case branches
- Both `group = ""` and `group = "NoPreprocess"` are valid for no-setup scenarios (pair with `dataIds = {}`)
- `group` can have a value with empty `dataIds = {}` when the group handles data creation internally
- `preProcess()` can use either `if/else-if` chains or `switch` statements — both are valid

### ⭐ Minimal Group Selection (MANDATORY)

Always select the **lightest preProcess group** that satisfies the test method's actual data needs:

| Test method needs | group | dataIds |
|---|---|---|
| No entity at all (stubs, pure UI navigation) | `"NoPreprocess"` | `{}` |
| Only `getEntityId()` (base entity) | `"create"` or simplest group | single template constant |
| Extra entities (`linkChange_*_id`, etc.) | heavy multi-entity group | linking template constant |

**FORBIDDEN**: Assigning heavy groups (e.g., `CREATE_MULTIPLE_CHANGE_FOR_LINKING`) to scenarios that only use `getEntityId()` or no entity at all. This wastes API calls and slows the test suite.

### preProcess Exception Handling (MANDATORY for new code)

`preProcess` exception handling varies by module — some modules silently swallow exceptions (`catch(Exception) { return false; }`), causing tests to be skipped with zero visibility. **New code MUST always use `addFailureReport()` in preProcess catch blocks** — failure visibility is critical for the self-healing process.

```java
// ✅ CORRECT — failure visible in ScenarioReport:
} catch(Exception exception) {
    report.addCaseFlow("Exception occurred while pre processing: " + exception);
    addFailureReport("Pre-process failed", exception.getMessage());
    return false;
}

// ❌ FORBIDDEN in new code — silent skip, impossible to debug:
} catch(Exception exception) {
    return false;
}
```

## Select2 Dropdowns

Options render in `<div class="select2-drop">` appended to `<body>`, NOT inside parent dialog:
```java
"//div[contains(@class,'select2-result-label') and contains(text(),'...')]"
```

## Non-Existent Methods — Never Use

```java
actions.listView.doAction()        // ❌ use rowAction(entityID, actionName)
actions.listView.selectRecord()    // ❌ use navigate.toDetailsPageUsingRecordId(id)
actions.navigate.clickModule()     // ❌ use navigate.toModule(name)
```

## Reporting — addReport Smart Variant

```java
addSuccessReport("message");                     // explicit success
addFailureReport("what failed", "why");          // explicit failure — sets scenarioDetails.setSuccess(false)
addReport("message");                            // SMART — checks failureMessage.length():
                                                 //   == 0 → addSuccessReport(message)
                                                 //   >  0 → addFailureReport(message, failureMessage)
```

**`clearFailureMessage()` is called automatically** inside every `addReport()` / `addSuccessReport()` / `addFailureReport()` call (verified in EntityCase.java source). Only call `clearFailureMessage()` manually if you need to **discard** accumulated failures mid-step before reporting.

Use `addReport()` after validation blocks where `failureMessage` accumulates errors.

## DataUtil Caching — Important Warning

`DataUtil.getTestCaseDataUsingFilePath()` caches loaded JSON entries. If you call `LocalStorage.store(key, newValue)` **AFTER** the first `getTestCaseData()` call with the same `TestCaseData` key, the second call returns the **cached** result with the OLD `$(custom_KEY)` value. Always pre-seed LocalStorage BEFORE the first `getTestCaseData()` call.

## Locator Best Practices

- Use `normalize-space(text())='Add'` for exact button text match (prevents matching "Add And Approve")
- Locator interfaces use `String` constants with XPath expressions
- Group locators by UI area (e.g., `SolutionCreateForm`, `SolutionDetailView`, `LinkingChange`)

## Multi-User Scenarios — ScenarioUsers & switchUser

The framework supports 5 user sessions per test run via `ScenarioUsers` enum:

| ScenarioUsers | Mapped to | Typical role |
|---|---|---|
| `MAIN_USER` | `EMAIL_ID` (tech email from config) | Technician — primary test actor |
| `TEST_USER_1` | 1st email from `SDP_TEST_USER_EMAILS` | Requester |
| `TEST_USER_2` | 2nd email | Requester / secondary tech |
| `TEST_USER_3` | 3rd email | Release manager / approver |
| `TEST_USER_4` | 4th email | Problem template user |

All 5 users share the same `DEFAULT_PASSWORD`. Emails are configured via `SDP_TEST_USER_EMAILS` in `.env` (comma-separated).

### Switching users mid-test

```java
// Get a test user object
User requester = scenarioDetails.getUser(ScenarioUsers.TEST_USER_2);

// Switch browser session to that user (clears cookies → re-login)
actions.switchUser(requester);

// ... perform actions as the requester ...

// Switch back to the main technician
actions.switchUser(scenarioDetails.getScenarioUser());
```

### Creating a user with a specific role before switching

```java
// Create TEST_USER_1 as a requester in the "requests" module
User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_1);
actions.createUserByRole(
    AutomaterConstants.REQUESTER,                   // role type
    "requests",                                      // module
    RequestConstants.CustomerIssues.CREATE_REQUESTER_WITH_VIEW_ALL_REQUESTS_PERMISSION,  // role config key
    user                                             // User object to assign the role to
);

// Now switch to that user
actions.switchUser(user);
```

### Session context rules

- `preProcess()` always runs in the **admin session**
- `switchToUserSession()` switches to `MAIN_USER` (tech email) before the test method runs
- `actions.switchUser(user)` can be called inside the test method to switch to any `TEST_USER_N`
- After switching, the browser is fully logged in as the new user — all subsequent actions run in that user's session
- API calls (`restAPI.*`) inside the test method run in the **current browser session** — if you switched to a requester, API calls execute with requester permissions

## ⚠️ RBAC (Role-Based Access Control) Scenarios — MANDATORY Pattern

> **Root cause of past miss**: Generated RBAC scenarios ran entirely as admin — assertions like
> "verify user without edit permission cannot see Attach/Detach buttons" were meaningless
> because admin always has all permissions. **RBAC tests MUST switch to the restricted role user.**

### When does this apply?

Any scenario whose description mentions roles, permissions, access control, requester, technician-specific features, owner-based access, manager-based access, stage-based restrictions, or "cannot see/do X" — these ALL require the role-based flow below.

### Required RBAC Test Flow

**Step 1 — preProcess: Create the role user (runs in admin session)**

```java
// In preProcess() — under a group like "createWithViewOnlyRole":
User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);

// Create technician/requester with specific role from <module>.json / general.json
// moduleName = "changes", "requests", "problems", "solutions", etc.
// roleConfigKey = key in resources/entity/roles/<module>.json or general.json
actions.createUserByRole(
    AutomaterConstants.TECHNICIAN,    // or AutomaterConstants.REQUESTER
    getModuleName(),                  // module for role JSON lookup (or hardcode: "changes", "requests", etc.)
    "SDChangeManager",                // role key from the module's role JSON
    user
);
LocalStorage.store("techName", user.getDisplayId());

// Also create prerequisite data while still in admin session
// (use appropriate module APIUtil: ChangeAPIUtil, RequestAPIUtil, ProblemAPIUtil, etc.)
```

**Step 2 — Test method: Switch to role user, test, then optionally switch back**

```java
public void verifyViewOnlyUserCannotPerformAction() throws Exception {
    try {
        // Get the SAME user created in preProcess
        User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);

        // CRITICAL: Switch browser to the role-restricted user
        actions.switchUser(user);

        // Now all UI actions run under the restricted role — works for ANY module
        actions.navigate.toModule(getModuleName());
        actions.navigate.toDetailsPageUsingRecordId(getEntityId());

        // Validate what this restricted user CAN or CANNOT see/do
        boolean actionVisible = actions.isElementPresent(someLocator);

        if (!actionVisible) {
            addSuccessReport("View-only user correctly cannot see the action button");
        } else {
            addFailureReport("Action button should be hidden for view-only user", "");
        }

        // Switch back to admin if subsequent steps need admin permissions
        switchToAdminSession();
    } catch (Exception exception) {
        addFailureReport("Internal error", exception.getMessage());
    } finally {
        report.endMethodFlowInStepsToReproduce();
    }
}
```

### Role JSON — Adding New Roles

Roles are stored in `resources/entity/roles/<module>.json` (one per module). If the needed role doesn't exist, add it to the correct module's JSON file:

| Module | Role JSON file | Example roles |
|--------|---------------|---------------|
| Changes | `roles/changes.json` | `SDChangeManager`, `Change_FullControl_With_CMDB` |
| Requests | `roles/requests.json` | `Requester`, `Full_Control`, `View_Only` |
| Problems | `roles/problems.json` | Problem-specific custom roles |
| Solutions | `roles/solutions.json` | Solution-specific custom roles |
| System-wide | `roles/general.json` | `sdadmin`, `sdsite_admin`, `sdguest`, `helpdeskconfig`, `Requester` |

```json
"<Module>_ViewOnly": {
    "user": {
        "roles": [{"name": "<Module>_ViewOnly"}],
        "default_project_role": {"name": "Project Admin"}
    },
    "custom_roles": {
        "<Module>_ViewOnly": {
            "permissions": [{"name": "<modulePrefix>ViewOnly"}]
        }
    },
    "is_technician": true
}
```

- `is_technician: true` → `createTechnician()` flow; `false` → `createRequester()` flow
- `custom_roles` → framework auto-creates these custom roles in SDP if they don't exist

### Decision Flow (apply to EVERY RBAC scenario in ANY module)

```
Is the scenario about role-based permissions / access control?
  → YES:
    1. Identify the role: What kind of user is being tested? (view-only, requester, manager, etc.)
    2. Find the correct module's role JSON: resources/entity/roles/<module>.json
       Does it have a matching role key?
       → NO: Add new role entry to that module's JSON file
    3. Check existing preProcess groups: Does an existing group already create this role user?
       → YES: Reuse that group
       → NO: Add new preProcess group with deleteScenarioUser() + createUserByRole()
    4. In the test method:
       a. Get user: `scenarioDetails.getUser(ScenarioUsers.TEST_USER_N)`
       b. Switch: `actions.switchUser(user)`
       c. Test UI behavior under that role's permissions
       d. `switchToAdminSession()` if needed after role testing
  → NO: Normal test flow (no role switching needed)
```

### CRITICAL — `deleteScenarioUser` Before `createUserByRole`

Always call `deleteScenarioUser()` before `createUserByRole()` for clean state:
```java
// ✅ CORRECT — clean slate before creating role user
deleteScenarioUser(ScenarioUsers.TEST_USER_3);
actions.createUserByRole(AutomaterConstants.TECHNICIAN, "changes", "SDChangeManager", user);

// ❌ WRONG — stale user from prior run may have wrong role
actions.createUserByRole(AutomaterConstants.TECHNICIAN, "changes", "SDChangeManager", user);
```

### ❌ FORBIDDEN — RBAC Anti-Patterns

```java
// ❌ Testing role restrictions as admin — MEANINGLESS
public void verifyNoEditPermissionHidesButtons() throws Exception {
    // Running as admin — admin has ALL permissions → buttons always visible
    actions.navigate.toDetailsPageUsingRecordId(getEntityId());
    boolean attachVisible = actions.isElementPresent(ATTACH_BUTTON);
    if (attachVisible) {
        addSuccessReport("baseline confirmed");  // ← proves nothing about the role
    }
}

// ❌ Saying "admin baseline" / "role config pending" — means the test is incomplete
addSuccessReport("RBAC_001: Admin baseline — role restriction test requires non-edit user");
// This is NOT a valid test. It should ACTUALLY switch to the restricted role user.
```
