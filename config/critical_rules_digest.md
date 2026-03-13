# Critical Rules Digest — MUST READ (compact extract from framework_rules.md + framework_knowledge.md)

> **Purpose**: This file extracts the ~20 most-violated rules into <300 lines so agents
> always have them in context — even when the full 2600-line `framework_rules.md` is truncated.
> For full details on any rule, see the referenced section in the parent file.

---

## D1 — REUSE EXISTING ENTITY CREATION METHODS (§21.2, §27 in knowledge)

Every entity parent class has a standard creation method (e.g., `createChangeGetResponse()`,
`createSolutionGetResponse()`). **Always use it** in `preProcess()` instead of calling
`DataUtil.getInputDataForRestAPI()` + `restAPI.createAndGetResponse()` manually.

```java
// ✅ CORRECT — parent class method
createChangeGetResponse(dataIds[0]);

// ❌ WRONG — verbose reinvention
JSONObject data = DataUtil.getInputDataForRestAPI(getModuleName(), getName(), dataIds[0], fields);
JSONObject resp = restAPI.createAndGetResponse(getName(), getModuleName(), getInputData(data));
```

For **additional** entities of the same type in the same preProcess block, use
`DataUtil.getInputDataForRestAPI()` (re-resolves `$(unique_string)` placeholders) and store
with numbered keys (`targetChangeId1`, `targetChangeName1`, etc.).

---

## D2 — MINIMAL GROUP SELECTION (§5.5)

Always pick the **lightest** preProcess group that satisfies the test method's data needs.

| Test method needs | group | dataIds |
|---|---|---|
| No entity at all | `"NoPreprocess"` | `{}` |
| Only `getEntityId()` | `"create"` (simplest) | `{single template}` |
| Extra entities beyond base | heavy multi-entity group | `{linking template}` |

**FORBIDDEN**: Defaulting all scenarios to the heaviest group "just in case."

---

## D3 — GROUP REUSE OVER NEW else-if BLOCKS (§5.6)

Before adding a new `else-if` branch to `preProcess()`, **read the existing body**.
If an existing group already creates the entity type you need AND stores the LocalStorage
keys you need → **reuse that group value**. Zero new preProcess code.

---

## D4 — runType MUST BE EXPLICIT (§2.3)

Annotation default is `PORTAL_BASED`. **Always write `runType = ScenarioRunType.USER_BASED`
explicitly.** Omitting it silently defaults to portal-based, which gets skipped in UserBased
flows. Use `PORTAL_BASED` only for scenarios with cross-test side effects (business rules,
SLA, automation).

---

## D5 — DATA LOADING METHODS — CORRECT CONTEXT (§9.2)

| Method | Where to use | When |
|--------|-------------|------|
| `getTestCaseData(TestCaseData)` | **Test method body** | Loading UI form data |
| `getTestCaseDataUsingCaseId(dataIds[N])` | **preProcess() only** | Loading API setup data |
| `DataUtil.getTestCaseDataUsingFilePath(path, caseId)` | **APIUtil static methods** | No Entity instance |

**FORBIDDEN**: Using `getTestCaseDataUsingCaseId` in APIUtil (no Entity context) or
`DataUtil.getTestCaseDataUsingFilePath` inside preProcess (use `getTestCaseDataUsingCaseId`).

---

## D6 — INLINE JSON CONSTRUCTION FORBIDDEN (§9.5)

ALL entity data (UI inputs AND API payloads) MUST originate from `*_data.json` files.
**NEVER** use `new JSONObject().put(...)` chains to build entity creation payloads from
scratch in Java code — not in test methods, not in preProcess, not in APIUtil.

Post-load modification (`.put()` / `.remove()` on a loaded JSONObject) IS allowed.
The only acceptable `new JSONObject()` uses: search criteria, API query filters, or wrapping
an already-loaded data object.

---

## D7 — DATA REUSE + LocalStorage PRE-SEED (§8b)

Before creating ANY new `*_data.json` entry:
1. Read existing `*_data.json` — list all keys
2. Read `*AnnotationConstants.java` → `Data` interface
3. Read `*DataConstants.java` for all constants

If an existing entry has `$(custom_KEY)` placeholders, pre-seed LocalStorage BEFORE
`getTestCaseData()` to reuse it with different runtime values instead of duplicating.

```java
LocalStorage.store("template_name", myTemplateName);
JSONObject inputData = getTestCaseData(ExistingDataConstants.ExistingData.EXISTING_KEY);
// $(custom_template_name) resolves from LocalStorage automatically
```

> **Caching warning**: DataUtil caches by `filePath_id`. Pre-seed LocalStorage BEFORE the first load.

---

## D8 — ACTIONSUTIL/APIUTIL PRE-GENERATION WORKFLOW (§23.0)

**MANDATORY 4-step workflow BEFORE writing any test code:**

1. **Read** the entity's `*ActionsUtil.java` + `*APIUtil.java` in full
2. **Map** each scenario operation → existing method or CREATE NEW
3. **Create** missing util methods FIRST (one method = one complete UI operation)
4. **Generate** the scenario using only util calls + assertions

Test method body = utility calls + assertions + `addSuccessReport`/`addFailureReport` ONLY.
If typing `actions.click(` in a test method → STOP → extract to util first.

---

## D9 — APIUTIL DATA FLOW (§23, copilot-instructions)

Every APIUtil method that sends data to an API must load from `*_data.json`:

```java
public final class ChangeAPIUtil extends Utilities {
    private static final String PATH = "data" + File.separator + "changes"
        + File.separator + "change" + File.separator + "change_data.json";

    public static void linkParentChange(String changeId, String targetId) throws Exception {
        LocalStorage.store("target_change_id", targetId);
        JSONObject inputData = DataUtil.getTestCaseDataUsingFilePath(
            AutomaterUtil.getResourceFolderPath() + PATH, "link_parent_change_api");
        restAPI.update("changes/" + changeId + "/link_parent_change", inputData);
    }
}
```

---

## D10 — waitForAjaxComplete() USAGE (§20.4)

`actions.click()` already calls `waitForAjaxComplete()` **before** clicking.

- Between two consecutive `actions.click()` → **NEVER** add `waitForAjaxComplete()` (redundant)
- After `actions.click()` before a non-click read (`getText`, `isElementPresent`) → ADD it
- After `actions.type()` / `actions.sendKeys()` that triggers AJAX → ADD it

---

## D11 — CHECKBOX/BOOLEAN FIELDS (§20.3)

`fillInputForAnEntity` has NO `boolean`/`checkbox` case. JSON booleans return `null` from
`getValueAsStringFromInputUsingAPIPath()` → field is silently skipped.
**ALL checkbox interactions must use explicit `actions.click(locator)`.**

---

## D12 — preProcess RUNS IN ADMIN SESSION (§20.6, §21.3)

1. `initializeAdminSession()` → admin
2. `preProcess()` runs → admin session (full permissions)
3. `switchToUserSession()` → user session
4. Test method body runs → user session

API calls in the test method body run as the scenario user — they may fail if the user
lacks permissions. Put ALL prerequisite API calls in `preProcess()`, not the test body.

---

## D13 — EXISTING UTIL METHOD PROTECTION (copilot-instructions §ActionsUtil)

ActionsUtil/APIUtil methods are shared across projects. **Do NOT modify existing public
static methods.** If a method doesn't fit, create a new one with a different name.

Before modifying an existing method:
```bash
grep -rn "methodName" $PROJECT_NAME/src/ | grep -v "utils/.*ActionsUtil\|utils/.*APIUtil" | wc -l
# If count > 2 → FORBIDDEN to modify — create a new method instead
```

---

## D14 — POPUP HANDLING (§22)

| Popup class | Search method | Filter method |
|---|---|---|
| `slide-down-popup` | `actions.popUp.listView.columnSearch()` | `actions.popUp.listView.selectFilterUsingSearch()` |
| `association-dialog-popup` / other | Custom locators | Custom locators |

**NEVER** use `actions.listView.columnSearch()` inside a popup — it searches the main page.

---

## D15 — MODULE PLACEMENT FROM USE-CASE NOUN (§0.1)

Derive module from the use-case description, **NEVER** from the currently open file.
`"create incident request"` → `modules/requests/request/`, not solutions.

---

## D16 — preProcess EXCEPTION HANDLING (§20.7, §28.2)

**ALWAYS** use `addFailureReport()` in preProcess catch blocks. Silent `return false` makes
failures invisible in ScenarioReport — impossible to debug.

```java
// ✅ CORRECT
} catch (Exception exception) {
    report.addCaseFlow("Exception while pre processing: " + exception);
    addFailureReport("Pre-process failed", exception.getMessage());
    return false;
}

// ❌ FORBIDDEN in new code
} catch (Exception exception) { return false; }
```

---

## D17 — DataConstants INNER CLASS NAMING (§32.2)

Inner class name = data filename via `LOWER_UNDERSCORE → UPPER_CAMEL`:
```
change_workflow_data.json  →  ChangeWorkflowData  (NOT ChangeData)
solution_data.json         →  SolutionData
```
Always check the actual inner class name before referencing it.

---

## D18 — LOCATOR EXACT MATCH (§20.8, §20.10)

For submit/action buttons, always use `normalize-space(text())='ExactText'`:
```java
// ❌ WRONG — matches "Add And Approve" too
By.xpath("//button[contains(text(),'Add')]")
// ✅ CORRECT
By.xpath("//button[normalize-space(text())='Add']")
```

---

## D19 — REPORT WRAPPING (§30.1)

Every test method body MUST be wrapped:
```java
report.startMethodFlowInStepsToReproduce(AutomaterUtil.getPascalValueFromCamelCase(getMethodName()));
try {
    // ... test logic ...
} catch (Exception exception) {
    addFailureReport("Internal error: " + getMethodName(), exception.getMessage());
} finally {
    report.endMethodFlowInStepsToReproduce();
}
```

---

## D20 — FORBIDDEN PATTERNS QUICK LIST (§13)

- Raw string data keys: `getTestCaseData("my_key")` → use DataConstants constant
- Flat lookup fields in JSON: `"priority": "Low"` → use `{"name": "Low"}`
- Missing `{"data": {...}}` wrapper in JSON entries
- Inventing locator constants, group names, API endpoints, or field paths
- Omitting `runType` (defaults to PORTAL_BASED — almost always wrong)
- Using `@AutomaterCase` on a new test scenario (use `@AutomaterScenario`)
- Calling `actions.validate.textContent()` without checking the return value
- `System.currentTimeMillis()` as random string → use `$(unique_string)` or `RandomUtil`

---

## D21 — FieldDetails CONSTRUCTOR (§32.5)

`FieldDetails` takes **6 parameters**: `(name, apiPath, apiKey, FieldType, isCustom, isUDF)`.
Writing 4 args compiles silently but breaks at runtime.

---

## D22 — NeedBraces CHECKSTYLE (§25)

ALL block statements require braces: `if`, `else`, `for`, `while`, `catch`, `finally`.
```java
// ❌ FORBIDDEN
} catch (Exception ignore) {}
if (x) doSomething();

// ✅ CORRECT
} catch (Exception ignore) {
    // intentionally empty
}
if (x) {
    doSomething();
}
```
