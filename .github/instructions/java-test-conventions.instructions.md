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
grep -rn 'id = "SDPOD_AUTO_SOL_DV' SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/ | sed 's/.*id = "\([^"]*\)".*/\1/' | sort | tail -1
```

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
