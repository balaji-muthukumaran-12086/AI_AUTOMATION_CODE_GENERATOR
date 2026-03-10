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

Always grep for the next sequential ID before assigning:
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

## `waitForAjaxComplete()` — Use Only Where Required

`actions.click()` already calls `waitForAjaxComplete()` BEFORE clicking. NEVER add it between consecutive clicks.

```java
// ❌ REDUNDANT — next click already waits
actions.click(TAB); actions.waitForAjaxComplete(); actions.click(BUTTON);

// ✅ CORRECT — no wait between clicks
actions.click(TAB); actions.click(BUTTON);

// ✅ CORRECT — wait needed before non-click read
actions.click(TAB); actions.waitForAjaxComplete(); actions.getText(CONTENT);

// ✅ CORRECT — wait needed after type triggers AJAX
actions.type(SEARCH, value); actions.waitForAjaxComplete(); actions.click(RESULT);
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

## APIUtil Data Flow (MANDATORY — NEVER construct JSON inline)

**Every new APIUtil method that sends data to an API** MUST load from `*_data.json`. NEVER build payloads with `new JSONObject().put(...)`.

**Required flow:**
1. Create a data entry in `*_data.json` with `$(custom_KEY)` placeholders for dynamic values
2. Define `PATH` constant in the APIUtil class pointing to the data file
3. Store dynamic values via `LocalStorage.store("KEY", value)` before loading
4. Load via `DataUtil.getTestCaseDataUsingFilePath(AutomaterUtil.getResourceFolderPath() + PATH, caseId)`
5. DataConstants are auto-generated on compile — callers reference `DataConstants.Data.KEY`

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

- `preProcess()` lives in the **parent class** (e.g., `Change.java`, `Solution.java`)
- Read parent's existing groups before adding new ones
- Reuse existing groups when they create the same entity type + store the same LocalStorage keys
- FORBIDDEN: Inventing group names not defined in the parent class

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
