# AutomaterSelenium — AI Code-Generation Rules
# Source: Exhaustive reading of Request.java (4873 lines), SolutionBase.java (393 KB),
#         Solution.java (3907 lines), IncidentRequest.java (3654 lines),
#         AutomaterScenario.java, AutomaterCase.java, AutomaterSuite.java,
#         SwitchToUserSession.java, ScenarioRunType.java, Priority.java,
#         RequestsRole.java, OwnerConstants.java, SolutionAnnotationConstants.java,
#         RequestDataConstants.java, SolutionDataConstants.java,
#         request_data.json, solution_data.json
#
# PURPOSE: Rules that prevent the LLM from hallucinating invalid code.
# RULE PRIORITY: FORBIDDEN rules must NEVER be violated.
#                REQUIRED rules must ALWAYS be followed.
#                PREFERRED rules are best-practice defaults.
---

## SECTION 0 — MODULE PLACEMENT (REQUIRED — check before any other rule)

### 0.1 Derive the target module from the use-case description, never from the active file

Before writing a single line of code, map the **entity noun in the scenario description** to
the correct module directory:

| Use-case noun | Module path | Typical leaf class(es) |
|---|---|---|
| incident request / IR / notes on IR | `modules/requests/request/` | `IncidentRequest`, `IncidentRequestNotes`, `RequestNotes` |
| service request / SR / notes on SR | `modules/requests/request/` | `ServiceRequest`, `ServiceRequestNotes` |
| solution | `modules/solutions/solution/` | `Solution`, `SolutionBase` |
| problem | `modules/problems/problem/` | `Problem`, `ProblemBase` |
| change | `modules/changes/change/` | `Change`, `ChangeBase` |
| task | `modules/tasks/task/` | `Task`, `TaskBase` |

### 0.2 Check for an existing leaf class before creating a new one (REQUIRED)

1. List files under `modules/<module>/`.
2. If a matching `*Notes.java`, `*DetailView.java`, etc. already exists → **add the scenario there**.
3. Only create a new file if no suitable class exists.

### 0.3 FORBIDDEN — cross-module placement

```java
// WRONG — incident-request scenario placed in SolutionBase.java
public void createIncidentRequestAndAddNotes() { ... }   // inside SolutionBase

// CORRECT — placed in RequestNotes.java / IncidentRequestNotes.java
public void createIncidentRequestAndAddNotes() { ... }   // inside RequestNotes
```

> **Root cause guard**: The currently open file is NOT a valid signal for target module.
> The use-case description is the only valid signal.

---

## SECTION 1 — CLASS ARCHITECTURE (two-layer pattern)

### 1.1 Two-layer structure (REQUIRED)
Every module has exactly two layers:

| Layer | File | Responsibility |
|-------|------|---------------|
| **Base class** | `XxxBase.java` or `Xxx.java` in a `common/` package | All UI logic, preProcess, postProcess. No `@AutomaterScenario` annotations. |
| **Leaf class** | `Xxx.java` in the module root | `@AutomaterSuite` on the class, `@AutomaterScenario` on each test method, body delegates to `super.method()` OR contains the full logic inline. |

**Example — correct leaf class structure:**
```java
@AutomaterSuite(
    role = RequestsRole.SDADMIN,
    owner = OwnerConstants.UMESH_SUDAN
)
public class IncidentRequest extends Request {

    public IncidentRequest(WebDriver driver, StringBuffer failureMessage) {
        super(driver, failureMessage);
    }

    @Override
    protected String getEntityConfigurationName() { return "request"; }

    @Override
    protected void assignPermission(String role) throws Exception { super.assignPermission(role); }

    @Override
    protected boolean preProcess(String group, String[] dataIds) {
        super.preProcess(group, dataIds);
        return true;
    }

    @AutomaterScenario(
        id = "SDP_REQ_LS_AAA001",
        group = "create",
        priority = Priority.MEDIUM,
        dataIds = {"IR_Valid_Input"},
        tags = {"RELEASE_CHECKLIST"},
        description = "Creates an Incident Request and validates it",
        owner = OwnerConstants.UMESH_SUDAN,
        runType = ScenarioRunType.USER_BASED
    )
    public void createIncidentRequest() {
        // ... logic here
    }
}
```

### 1.2 Which class gets what (REQUIRED)
- `@AutomaterSuite` → ONLY on the LEAF class declaration
- `@AutomaterScenario` → ONLY on test methods
- Logic methods (navigation, form fill, assertions) → ONLY in base class
- NEW test scenarios ALWAYS go in the LEAF class, delegating to base if needed

---

## SECTION 2 — @AutomaterScenario ANNOTATION

### 2.1 All nine fields (REQUIRED — always include all)
```java
@AutomaterScenario(
    id          = "MODULE_PREFIX_NNN",   // string — see Section 7 for format
    group       = "create",              // string — see Section 4 for valid values
    priority    = Priority.MEDIUM,       // enum — see Section 2.2
    dataIds     = {"DataKey"},           // String[] — keys into the module's data JSON
    tags        = {},                    // String[] — see Section 2.5
    description = "Human readable",      // plain English description
    owner       = OwnerConstants.NAME,   // see Section 6.2
    runType     = ScenarioRunType.USER_BASED,  // ⚠ ALWAYS set explicitly (see 2.3)
    switchOn    = SwitchToUserSession.AFTER_PRE_PROCESS  // usually the default; see 2.4
)
```

### 2.2 priority — valid values (REQUIRED, use exactly these)
```java
Priority.HIGH
Priority.MEDIUM    // most common default
Priority.LOW
```

### 2.3 runType — CRITICAL TRAP (REQUIRED)
- **Default in the annotation definition = `ScenarioRunType.PORTAL_BASED`**
- **Most tests use `ScenarioRunType.USER_BASED`**
- **ALWAYS write `runType = ScenarioRunType.USER_BASED` explicitly. Never omit it.**
- Only use `PORTAL_BASED` when specifically testing portal (requester) views.

```java
// CORRECT
runType = ScenarioRunType.USER_BASED

// WRONG — omitting it silently defaults to PORTAL_BASED
// (no runType field)
```

### 2.4 switchOn — valid values and when to use
```java
SwitchToUserSession.AFTER_PRE_PROCESS   // DEFAULT — switch user AFTER API data setup
SwitchToUserSession.BEFORE_PRE_PROCESS  // rare — switch user BEFORE data creation (e.g. requester tests)
SwitchToUserSession.NEVER               // no session switch at all
```
When in doubt, use `AFTER_PRE_PROCESS` (or simply omit this field and let default apply).

### 2.5 tags — valid values
```java
tags = {}                           // empty — most common for new tests
tags = {"RELEASE_CHECKLIST"}        // include in release checklist run
tags = {GlobalConstants.Tags.IN_DEVELOPMENT}  // still in development
tags = {ScenarioTagConstants.SANITY}           // sanity suite
```

### 2.6 id — empty string is allowed for WIP tests
```java
id = ""   // Acceptable for work-in-progress; assign real ID before committing
```
But see Section 7 for how to generate a real ID.

---

## SECTION 3 — @AutomaterSuite ANNOTATION

### 3.1 Placed on the LEAF class (REQUIRED)
```java
@AutomaterSuite(
    role  = RequestsRole.SDADMIN,          // required — see Section 6.1
    owner = OwnerConstants.UMESH_SUDAN,    // required — see Section 6.2
    tags  = {}                             // optional — String or String[]
)
```

### 3.2 tags — can be a single string OR an array
```java
tags = {}                   // empty array (most common)
tags = "SOLUTION TESTING"   // single string (legacy style, still valid)
tags = {"RELEASE_CHECKLIST"}
```

---

## SECTION 4 — @AutomaterCase ANNOTATION

### 4.1 @AutomaterCase is NOT for test scenarios (FORBIDDEN on new tests)
- `@AutomaterCase(description = "...")` has ONE field: `description`
- It annotates **helper sub-methods** in the BASE class that are called by multiple scenarios
- Examples: `goToRequest()`, `brNetwork()`, `goToSolution()`
- These are NOT directly run by the test runner

### 4.2 NEVER use @AutomaterCase for a new test case
```java
// WRONG — @AutomaterCase cannot run as a standalone test
@AutomaterCase(description = "My new test")
public void myNewTest() { ... }

// CORRECT — use @AutomaterScenario instead
@AutomaterScenario(id = "...", group = "...", ...)
public void myNewTest() { ... }
```

---

## SECTION 5 — preProcess GROUPS

### 5.1 What preProcess does
- Called before the UI test method runs
- Creates test data via REST API using `dataIds[]` values
- Stores created entity IDs in `LocalStorage` for the test method to retrieve
- ONLY known group strings are handled; unknown → silently falls through

### 5.2 VALID groups — Requests module
```
"create"                     → creates a single request via API
"rowColor"                   → creates request for row-color test
"customView"                 → creates list-view filter via API
"PinFavorite"                → creates pinned favorite filter
"multipleCreate"             → creates multiple requests
"detailView"                 → creates request for detail-view tests
"addTask"                    → creates request + task template
"addTaskTemplate"            → creates task template only
"BulkCreate"                 → creates requests for bulk operations
"assetRequest"               → creates request with asset linkage
"mixedCreate"                → creates mixed IR+SR requests
"differentRequest"           → creates requests of different types
"SubEntity_Resolution"       → creates resolution sub-entity
"SubEntity_Reminder"         → creates reminder sub-entity
"SubEntity_createTask"       → creates task sub-entity
"SubEntity_createTask2"      → creates second task variant
"Associations"               → creates linked associations
"copyResolution"             → creates request to copy resolution from
"delete_all_sites_create_request" → site-cleanup + request
"create_sla"                 → creates request with SLA
"requester_create"           → creates request as requester
"signature"                  → creates request for signature test
"columnchoosersitelookupfield" → creates request for column-chooser test
"NoPreprocess"               → ⚡ NO setup at all (see 5.3)
```

### 5.3 VALID groups — Solutions module
```
"create"                         → creates a solution via API
"create_cust_sol_temp"           → creates solution with custom template
"create_cust_temp_topic"         → creates solution with custom template + topic
"createMultipleSolution"         → creates multiple solutions
"create_topic"                   → creates a topic
"NoPreprocess"                   → ⚡ NO setup at all (see 5.3)
```

### 5.4 NoPreprocess — complete behavior (CONFIRMED from source)
- `Request.preProcess()` has NO if-branch for `"NoPreprocess"` → falls through all branches → returns `true`
- `Request.postProcess()` also has NO handler for `"NoPreprocess"` → does nothing
- **Result: zero API calls, zero cleanup — safe to use for pure UI tests**
- Always pair with empty `dataIds`:
```java
group   = "NoPreprocess",
dataIds = {}         // preferred
// OR
dataIds = {""}       // also acceptable (legacy style)
```

### 5.5 FORBIDDEN — inventing group names
```java
// WRONG — "createRequest" is not a valid group in Request.preProcess()
group = "createRequest"

// WRONG — "newSolution" is not in SolutionBase.preProcess()
group = "newSolution"
```
Only use the exact strings from Section 5.2 and 5.3.

---

## SECTION 6 — VALID ANNOTATION CONSTANTS

### 6.1 Role constants
**Requests module** — import `RequestsRole`:
```java
RequestsRole.SDADMIN
RequestsRole.FULL_CONTROL
RequestsRole.EDIT_ONLY
RequestsRole.VIEW_ONLY
RequestsRole.REQUESTER1
RequestsRole.REQUESTER2
RequestsRole.REQUESTER3
```

**Other modules** — import `Role` or `ModulesRoleSkeleton`:
```java
Role.SDADMIN
ModulesRoleSkeleton.SDADMIN
```

### 6.2 Owner constants (use EXACTLY these — import `OwnerConstants`)
```java
OwnerConstants.UMESH_SUDAN
OwnerConstants.ANTONYRAJAN_D
OwnerConstants.RAJESHWARAN_A
OwnerConstants.MUTHUSIVABALAN_S
OwnerConstants.VINUTHNA_K
OwnerConstants.NANTHAKUMAR_G
OwnerConstants.VIGNESH_E
OwnerConstants.RUJENDRAN
OwnerConstants.THILAK_RAJ
OwnerConstants.PURVA_RAJESH
OwnerConstants.VEERAVEL
OwnerConstants.JAYA_KUMAR
```

### 6.3 ScenarioRunType constants
```java
ScenarioRunType.USER_BASED    // ← use this for 95% of tests
ScenarioRunType.PORTAL_BASED
```

### 6.4 SwitchToUserSession constants
```java
SwitchToUserSession.AFTER_PRE_PROCESS   // ordinal 1 — default
SwitchToUserSession.BEFORE_PRE_PROCESS  // ordinal 0
SwitchToUserSession.NEVER               // ordinal 2
```

---

## SECTION 7 — TEST ID FORMAT

### 7.1 ID format per module
| Module | Pattern | Example |
|--------|---------|---------|
| Requests (ListView) | `SDP_REQ_LS_AAA###` | `SDP_REQ_LS_AAA001` |
| Requests (DetailView) | `SDP_REQ_DV_AAA###` | `SDP_REQ_DV_AAA114` |
| Solutions (generic) | `SDPOD_AUTO_SOL_###` | `SDPOD_AUTO_SOL_136` |
| Solutions (ListView) | `SDPOD_AUTO_SOL_LV_###` | `SDPOD_AUTO_SOL_LV_180` |
| Solutions (DetailView) | `SDPOD_AUTO_SOL_DV_###` | `SDPOD_AUTO_SOL_DV_243` |
| Changes | `SDPOD_AUTO_CH_LV_###` | `SDPOD_AUTO_CH_LV_492` |
| Problems | `SDPOD_AUTO_PB_###` | `SDPOD_AUTO_PB_###` |
| Releases | `SDPOD_AUTO_RL_###` | `SDPOD_AUTO_RL_###` |
| Purchase Orders | `SDPOD_AUTO_PURCHASE_###` | |
| CMDB/Assets | `SDPOD_AUTO_CMDB_###` | |

### 7.2 How to find the next available ID
```bash
# Example for Solutions ListView:
grep -rn 'id = "SDPOD_AUTO_SOL_LV' SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/ | \
  sed 's/.*id = "\([^"]*\)".*/\1/' | sort | tail -1
# → SDPOD_AUTO_SOL_LV_179  →  next = SDPOD_AUTO_SOL_LV_180
```

### 7.3 Last known IDs (as of rules document creation)
```
Solutions ListView  : SDPOD_AUTO_SOL_LV_179   → next: 180
Solutions DetailView: SDPOD_AUTO_SOL_DV_242   → next: 243
Solutions generic   : SDPOD_AUTO_SOL_135      → next: 136
Changes ListView    : SDPOD_AUTO_CH_LV_491    → next: 492
Requests ListView   : SDP_REQ_LS_AAA100+      (check live)
```
⚠️ **Always run the grep command above before assigning an ID to avoid duplicates.**

---

## SECTION 8 — DATA JSON FORMAT

### 8.1 Structure (REQUIRED)
Every data entry in `<entity>_data.json` must follow this exact structure:
```json
{
  "MY_DATA_KEY": {
    "data": {
      "field_name": "literal value",
      "lookup_field": {"name": "Lookup Value"},
      "boolean_field": true,
      "subject": "Test Subject $(unique_string)"
    }
  }
}
```

**Rules:**
1. Top level = the data key string (matches the `TestCaseData("key", PATH)` constructor)
2. Second level = always `{"data": { ... }}` — one wrapper layer, NO exceptions
3. Lookup/dropdown fields = always `{"name": "Value"}` object, NEVER flat string
4. Boolean fields = direct `true` / `false`, NOT `"true"` string
5. Text fields = plain string

### 8.2 Available runtime placeholders (complete PlaceholderUtil list)
```
# Date / time
$(date, delay, isAhead)              → date in milliseconds (delay=days offset, isAhead=true/false)
$(datetime, delay, isAhead)          → datetime in milliseconds

# Unique strings
$(unique_string)                     → current timestamp as string (unique per run)
$(common_string)                     → timestamp with part name (shared across parts of same run)

# User identity (resolved at runtime for the active scenario user)
$(user_name)                         → current scenario user's display ID
$(user_email_id)                     → current scenario user's email address
$(user_id)                           → current scenario user's entity ID

# Admin identity
$(admin_email_id)                    → admin's email address
$(admin_name)                        → admin's display ID

# MSP (multi-tenant) — only for MSP-mode tests
$(mspcustomer_id)                    → MSP customer ID
$(mspcustomer_name)                  → MSP customer name
$(mspcustomer_email)                 → MSP customer email

# Dynamic REST API call — advanced
$(rest_api, method, entity, url, dataId, [iterate])
    → executes a REST API call at data-load time and injects the result

# LocalStorage bridge — read a value stored by preProcess
$(local_storage, method, key, value) → stores/retrieves from LocalStorage
$(custom_KEY)                        → shorthand: returns value stored in LocalStorage as KEY
                                       e.g. $(custom_general_topic) → LocalStorage.get("general_topic")
                                       e.g. $(custom_solution_template) → LocalStorage.get("solution_template")
                                       e.g. $(custom_topic) → LocalStorage.get("topic")
```

**Key rule**: `$(custom_KEY)` maps directly to whatever string was `LocalStorage.store(KEY, value)` in preProcess.

### 8.3 Nested objects for entity lookups
```json
{
  "IR_Valid_Input": {
    "data": {
      "template":  {"name": "Default Request"},
      "subject":   "Incident Request $(unique_string)",
      "requester": {"name": "$(user_name)"},
      "priority":  {"name": "Low"},
      "status":    {"name": "Open"},
      "group":     {"name": "Network"}
    }
  }
}
```

### 8.4 FORBIDDEN — flat lookup fields
```json
// WRONG — priority must be a lookup object, not a flat string
"priority": "Low"

// CORRECT
"priority": {"name": "Low"}
```

---

## SECTION 9 — DataConstants PATTERN

### 9.1 TestCaseData declaration (REQUIRED)
Every data key used in a test must be pre-declared in the module's `*DataConstants.java`:

```java
// In RequestDataConstants.java (or equivalent)
public final static TestCaseData MY_NEW_DATA = new TestCaseData("my_new_data_key", PATH);
```

- The `PATH` constant uses `File.separator` and points to `data/<module>/<entity>/<entity>_data.json`
- The first string argument **must exactly match** the top-level key in the JSON file

### 9.2 Usage in test method
```java
JSONObject inputData = getTestCaseData(RequestDataConstants.RequestData.MY_NEW_DATA);
```

### 9.3 FORBIDDEN — string literals as data keys
```java
// WRONG — never use a raw string
JSONObject inputData = getTestCaseData("IR_Valid_Input");

// CORRECT — always use the DataConstants constant
JSONObject inputData = getTestCaseData(RequestDataConstants.RequestData.IR_VALID_INPUT);
```

---

## SECTION 10 — IMPLEMENTATION METHOD SKELETON

### 10.1 Standard body pattern (REQUIRED — use this exact structure)
```java
@AutomaterScenario(
    id          = "MODULE_PREFIX_NNN",
    group       = "create",
    priority    = Priority.MEDIUM,
    dataIds     = {"DataConstantKey"},
    tags        = {},
    description = "Short plain-English description",
    owner       = OwnerConstants.OWNER_NAME,
    runType     = ScenarioRunType.USER_BASED
)
public void myScenarioMethod() {
    report.startMethodFlowInStepsToReproduce(AutomaterUtil.getPascalValueFromCamelCase(getMethodName()));
    try {
        JSONObject inputData = getTestCaseData(ModuleDataConstants.ModuleData.DATA_KEY);

        actions.navigate.toModule(getModuleName());
        actions.setTableView(EntityConstants.LISTVIEW);
        actions.navigate.toGlobalActionInListview(EntityConstants.ListviewGlobalActions.NEW_ENTITY);
        actions.formBuilder.fillInputForAnEntity(isClientFramework(), fields, inputData);
        actions.clickButton(GlobalConstants.Actions.SAVE);  // or module-specific submit

        String text = AutomaterUtil.getValueAsStringFromInputUsingAPIPath(inputData, EntityFields.TITLE.getDataPath());
        Boolean isEqual = actions.validate.textContent(ClientFrameworkLocators.DetailsViewLocators.MODULE_TITLE, text);

        if (isEqual) {
            addSuccessReport("Successfully verified creation for " + getRole() + " role using " + AutomaterUtil.getCurrentUserId() + " user");
        } else {
            addFailureReport("Verification failed for " + getRole() + " role", "Title does not match expected value");
        }
    } catch (Exception exception) {
        addFailureReport("Internal error occurred while running the test case " + getMethodName(), exception.getMessage());
    } finally {
        report.endMethodFlowInStepsToReproduce();
    }
}
```

### 10.2 Variant — when test has NO form submission (e.g. ListView read test)
```java
public void myListViewScenario() {
    report.startMethodFlowInStepsToReproduce(AutomaterUtil.getPascalValueFromCamelCase(getMethodName()));
    try {
        actions.navigate.toModule(getModuleName());
        // ... assertions
        addSuccessReport("...");
    } catch (Exception exception) {
        addFailureReport("Internal error occurred while running the test case " + getMethodName(), exception.getMessage());
    } finally {
        report.endMethodFlowInStepsToReproduce();
    }
}
```

### 10.3 Alternative report.startMethodFlow call (both are valid)
```java
// Style 1 — more common in newer tests
report.startMethodFlowInStepsToReproduce(AutomaterUtil.getPascalValueFromCamelCase(getMethodName()));

// Style 2 — seen in some tests
report.startMethodFlowInStepsToReproduce(AutomaterVariables.SCENARIO_START.apply(getMethodName()));
```
Both are valid. Style 1 is the preferred default.

### 10.4 addSuccessReport and addFailureReport signatures
```java
addSuccessReport(String message)
addFailureReport(String stepDescription, String expectedVsActual)
```

### 10.5 FORBIDDEN — missing try/catch/finally
```java
// WRONG — raw method body with no error handling
public void myTest() {
    actions.navigate.toModule(getModuleName());
    // ...
}

// CORRECT — always use the try/catch/finally skeleton from 10.1
```

---

## SECTION 11 — postProcess PATTERN

### 11.1 When postProcess is needed
The base class `Request.postProcess()` handles cleanup for groups: `rowColor`, `customView`, `create`, `detailview`, `addTask`, `mixedCreate`, `differentRequest`.

For groups that have a postProcess handler, the LEAF class overrides like this:
```java
@Override
protected void postProcess(String group) {
    super.postProcess(group);
}
```

### 11.2 NoPreprocess — postProcess is a no-op
`"NoPreprocess"` group → `postProcess()` has NO handler in the base → nothing happens. If generating a `NoPreprocess` test, either omit `postProcess` override or just delegate to super.

### 11.3 Solutions module — SolutionBase.postProcess() is empty
```java
// SolutionBase.java line 7426:
protected void postProcess(String method) {
}
```
For solutions, postProcess does nothing at the base level. Override only if the leaf class needs custom cleanup.

---

## SECTION 12 — TWO-PIECE LLM OUTPUT FORMAT

When generating code, the AI output MUST use this exact marker format so `OutputAgent` can parse it:

```
// ===== ADD TO: IncidentRequest.java =====
<code block for IncidentRequest.java — only the METHOD body or new method>

// ===== ADD TO: RequestDataConstants.java =====
<code block — only the new TestCaseData constant line>

// ===== ADD TO: request_data.json =====
<JSON block — only the new data entry>
```

**Rules:**
- Marker line: `// ===== ADD TO: ExactFileName.java =====`
- File name in the marker MUST match the actual file name in the repo
- Each block contains ONLY what needs to be added — not the whole file
- DO NOT output the entire file — output snippets only
- Three outputs are needed for a new test: leaf class, DataConstants class, data JSON

---

## SECTION 13 — FORBIDDEN PATTERNS (NEVER GENERATE THESE)

### 13.1 NEVER invent locator constants
```java
// WRONG — RequestLocators.Form.MY_INVENTED_LOCATOR does not exist
actions.click(RequestLocators.Form.MY_INVENTED_LOCATOR);

// CORRECT — only use locator constants that exist in the codebase
// Use semantic_search or grep to find the actual locator before referencing it
```

### 13.2 NEVER invent field path strings
```java
// WRONG — "custom_field.value" may not exist in EntityFields
String text = AutomaterUtil.getValueAsStringFromInputUsingAPIPath(inputData, "custom_field.value");

// CORRECT — use EntityFields enum's getDataPath() method
String text = AutomaterUtil.getValueAsStringFromInputUsingAPIPath(inputData, RequestFields.SUBJECT.getDataPath());
```

### 13.3 NEVER invent group names
Only use the exact group strings listed in Section 5.2 and 5.3.

### 13.4 NEVER invent API endpoint strings
```java
// WRONG — "my_entity" endpoint may not exist
restAPI.delete("my_entity/".concat(getEntityId()));

// CORRECT — use endpoints that appear in existing preProcess/postProcess methods
// Confirmed valid endpoints: "requests/", "solutions/", "task_templates/", "list_view_filters/"
```

### 13.5 NEVER omit runType
Always write `runType = ScenarioRunType.USER_BASED` explicitly.

### 13.6 NEVER use @AutomaterCase on a new test scenario
Only `@AutomaterScenario` goes on runnable tests.

### 13.7 NEVER use flat strings for lookup fields in data JSON
```json
"priority": "Low"         // WRONG
"priority": {"name": "Low"}  // CORRECT
```

### 13.8 NEVER reference non-existent owner constants
Only use the 12 owners listed in Section 6.2.

### 13.9 NEVER skip the {"data": {}} wrapper in JSON
```json
// WRONG — missing wrapper
"MY_KEY": {"subject": "test"}

// CORRECT
"MY_KEY": {"data": {"subject": "test"}}
```

### 13.10 NEVER hardcode test data as string literals in Java
```java
// WRONG
actions.formBuilder.fillField("subject", "My Test Subject");

// CORRECT — read from data JSON
JSONObject inputData = getTestCaseData(RequestDataConstants.RequestData.MY_KEY);
actions.formBuilder.fillInputForAnEntity(isClientFramework(), fields, inputData);
```

### 13.11 NEVER use System.currentTimeMillis() directly as a random string
```java
// WRONG
String subject = "Test Subject " + System.currentTimeMillis();

// CORRECT — use placeholder in JSON
"subject": "Test Subject $(unique_string)"
// OR — use RandomUtil in Java if you need a runtime value
String subject = "Test Subject " + RandomUtil.generateRandomString(8);
```

### 13.12 NEVER use unsupported placeholder syntax
```json
// WRONG — made-up placeholder
"requester": "$(current_user)"

// CORRECT — use the documented placeholder
"requester": {"name": "$(user_name)"}
```
Only use placeholders listed in Section 8.2.

### 13.13 NEVER call `actions.validate.textContent()` and ignore the return value for assertion
```java
// WRONG — result not checked
actions.validate.textContent(locator, expected);

// CORRECT — check result or use assert methods
Boolean ok = actions.validate.textContent(locator, expected);
if (ok) { addSuccessReport("..."); } else { addFailureReport("...", "..."); }
// OR use direct assertion methods:
actions.validate.successMessageInAlertAndClose("Saved successfully");
```

---

## SECTION 14 — REQUIRED IMPORTS REFERENCE

### 14.1 Base imports for a Requests leaf class
```java
import com.zoho.automater.selenium.base.ScenarioRunType;
import com.zoho.automater.selenium.base.annotations.AutomaterScenario;
import com.zoho.automater.selenium.base.annotations.AutomaterSuite;
import com.zoho.automater.selenium.base.common.AutomaterVariables;
import com.zoho.automater.selenium.base.common.Priority;
import com.zoho.automater.selenium.base.common.SwitchToUserSession;
import com.zoho.automater.selenium.base.utils.AutomaterUtil;
import com.zoho.automater.selenium.modules.GlobalConstants;
import com.zoho.automater.selenium.modules.OwnerConstants;
import com.zoho.automater.selenium.modules.requests.RequestsRole;
import com.zoho.automater.selenium.modules.requests.request.Request;
import com.zoho.automater.selenium.modules.requests.request.common.RequestConstants;
import com.zoho.automater.selenium.modules.requests.request.common.RequestDataConstants;
import com.zoho.automater.selenium.modules.requests.request.common.RequestFields;
import com.zoho.automater.selenium.modules.requests.request.common.RequestLocators;
import org.json.JSONObject;
import org.openqa.selenium.WebDriver;
```

### 14.2 Base imports for a Solutions leaf class
```java
import com.zoho.automater.selenium.base.ScenarioRunType;
import com.zoho.automater.selenium.base.annotations.AutomaterScenario;
import com.zoho.automater.selenium.base.annotations.AutomaterSuite;
import com.zoho.automater.selenium.base.common.AutomaterVariables;
import com.zoho.automater.selenium.base.common.Priority;
import com.zoho.automater.selenium.base.utils.AutomaterUtil;
import com.zoho.automater.selenium.modules.OwnerConstants;
import com.zoho.automater.selenium.modules.Role;
import com.zoho.automater.selenium.modules.solutions.solution.SolutionBase;
import com.zoho.automater.selenium.modules.solutions.solution.common.SolutionAnnotationConstants;
import com.zoho.automater.selenium.modules.solutions.solution.common.SolutionDataConstants;
import com.zoho.automater.selenium.modules.solutions.solution.common.SolutionFields;
import com.zoho.automater.selenium.modules.solutions.solution.common.SolutionLocators;
import org.json.JSONObject;
import org.openqa.selenium.WebDriver;
```

---

## SECTION 15 — QUICK CHECKLISTS

### 15.1 New test scenario checklist
Before generating a new `@AutomaterScenario`, verify:
- [ ] `id` is unique — run the grep from Section 7.2
- [ ] `group` is a valid string from Section 5.2 or 5.3
- [ ] `runType` is explicitly set (not relying on default)
- [ ] `owner` is from the list in Section 6.2
- [ ] `dataIds` match the constants you're declaring in DataConstants
- [ ] Data JSON has `{"data": {...}}` wrapper
- [ ] All lookup fields in JSON are `{"name": "..."}` objects
- [ ] Method body has try/catch/finally
- [ ] Report start/end calls are present

### 15.2 Two-piece output checklist
When generating the code output, verify:
- [ ] Marker format: `// ===== ADD TO: ExactFileName.java =====`
- [ ] Separate marker for: leaf class, DataConstants, JSON data file
- [ ] Each block is ONLY the new additions, not full file contents
- [ ] Locators used exist in the actual codebase

### 15.3 Data JSON checklist
- [ ] Top-level key matches `TestCaseData("key", PATH)` constructor arg
- [ ] `{"data": {...}}` wrapper present
- [ ] No flat strings for lookup fields
- [ ] Placeholders from Section 8.2 only

---

## SECTION 16 — VALIDATOR API (complete — `actions.validate`)

```java
// Text / content checks
Boolean actions.validate.textContent(Locator locator, String content)
    // compares trimmed element text to content — returns true/false, logs result

// Notification / alert checks
void actions.validate.successMessageInAlert(String message)
    // asserts a success-class notification banner contains message
void actions.validate.successMessageInAlertAndClose(String message)
    // asserts success notification then closes it
void actions.validate.errorMessageInAlert(String message)
    // asserts an error-class notification contains message
void actions.validate.errorMessageInAlertAndClose(String message)
    // asserts error notification then closes it
void actions.validate.verifyMessageInAlert(Boolean isSuccess, String message)
    // isSuccess=true → success class, false → error class
void actions.validate.verifyMessageInAlertAndClose(Boolean isSuccess, String message)
    // same + closes
boolean actions.validate.isSuccessNotification(String notificationClass)
    // low-level check: is the element with notificationClass a success element?

// Assertion helpers
void actions.validate.customAssert(String expected, String got)
    // throws AssertionError with diff message if not equal
void actions.validate.customAssert(Boolean expected, Boolean got)
    // boolean equality assertion
void actions.validate.confirmationBoxTitleAndConfirmationText(String title, String confirmText)
    // verifies confirmation dialog title and body text

// Date/datetime validation
Boolean actions.validate.validateDate(Locator locator, Long value)
    // verifies date displayed at locator matches the millisecond value
Boolean actions.validate.validateDateTime(Locator locator, Long value, boolean isTimeField)
    // same but also validates time portion when isTimeField=true

// Form validation
void actions.validate.validateFormFieldValues(Map<String, FieldDetails> fields, JSONObject inputData)
    // iterates fields and asserts each displayed value matches inputData
```

### 16.1 Most common patterns
```java
// After creating — check title in details page
Boolean ok = actions.validate.textContent(
    ClientFrameworkLocators.DetailsViewLocators.MODULE_TITLE, expectedTitle);

// After save — check success banner
actions.validate.successMessageInAlertAndClose("Record saved successfully");

// After delete — check notification
actions.validate.successMessageInAlert(SolutionConstants.AlertMessages.SOLUTIONS_DELETED_MSG);

// Assert a specific field value
boolean fieldOk = actions.detailsView.verifyFieldInDetailsPage("subject", expectedValue);
```

---

## SECTION 17 — WINDOWMANAGER API (`actions.windowManager`)

```java
// Open new tab/window and switch to it
String handle = actions.windowManager.switchToNewTab(int timeoutSeconds)
    // waits up to timeoutSeconds for a new tab/window, switches to it, returns handle
String handle = actions.windowManager.switchToNewWindow(int timeoutSeconds)  // alias

// Return to original tab
void actions.windowManager.returnToOriginalTab()
void actions.windowManager.returnToOriginalWindow()  // alias

// Switch to tab by position / title / URL
void actions.windowManager.switchToTabByIndex(int index)      // 0-based
void actions.windowManager.switchToTabByTitle(String title)   // partial match
void actions.windowManager.switchToTabByUrl(String url)       // partial match
void actions.windowManager.switchToWindowByIndex(int index)   // alias
void actions.windowManager.switchToWindowByTitle(String title)
void actions.windowManager.switchToWindowByUrl(String url)

// Close tabs
void actions.windowManager.closeTabByIndex(int index)
void actions.windowManager.closeAllTabsExceptOriginal()
void actions.windowManager.closeWindowByIndex(int index)       // alias
void actions.windowManager.closeAllWindowsExceptOriginal()     // alias
```

### 17.1 Standard multi-tab pattern
```java
// Click link that opens new tab
actions.click(SomeLocators.OPEN_IN_NEW_TAB);
actions.windowManager.switchToNewTab(10);  // wait up to 10 seconds
// ... do assertions in new tab ...
actions.windowManager.returnToOriginalTab();
```

---

## SECTION 18 — RANDOMUTIL API (`import RandomUtil`)

```java
// Generate random alphabetic string of length n
String s = RandomUtil.generateRandomString(int n)
String s = RandomUtil.generateRandomString(int n, String prefix)
    // e.g. RandomUtil.generateRandomString(8, "TEST_") → "TEST_aBcDeFgH"

// Lowercase / uppercase variants
String s = RandomUtil.generateRandomLowercaseString(int n)
String s = RandomUtil.generateRandomUppercaseString(int n, String prefix)

// Alphanumeric
String s = RandomUtil.generateRandomAlphaNumericString(int n)
String s = RandomUtil.generateRandomAlphaNumericString(int n, String prefix)

// Random element from array
String s = RandomUtil.randomChoice(String[] options)
    // e.g. RandomUtil.randomChoice(new String[]{"High","Medium","Low"})
```

### 18.1 When to use RandomUtil vs $(unique_string)
- **In JSON test data**: use `$(unique_string)` placeholder — it's evaluated at load time
- **In Java test logic** (runtime string not from JSON): use `RandomUtil.generateRandomString(8)`
- **Never** use `System.currentTimeMillis()` as a random string in Java test code

---

## SECTION 19 — FORMBUILDER COMPLETE API (`actions.formBuilder`)

```java
// Bulk fill (main entry point — uses entity configuration fields[])
void fillInputForAnEntity(boolean isClientFramework, Map<String,FieldDetails> fields, JSONObject inputData)

// Individual field fill methods
void fillTextField(String name, String value)
void fillTextAreaField(String name, String value)
void fillSelectField(String name, String value)
void typeAndSelectOption(String value)          // types into currently-focused dropdown then clicks match
void selectValueInMultiField(String name, String value)  // selects one value in multi-select
void fillMultiSelectField(FieldDetails fd, JSONObject inputData, String path)  // fills from JSON array
void fillMultiSelectField(FieldDetails fd, List<Object> values)               // fills from list
void fillHTMLField(String name, String value)
void fillCriteria(JSONArray criteria)
void fillInputForCustomField(FieldDetails fd, JSONObject inputData)  // no-op default — do NOT call

// Date / datetime
void fillDateField(String name, Long value)                                    // date-only
void fillDateTimeField(String name, Long value)                                // date + time
void fillDateTimeFieldInForm(String name, Long value, boolean isTimeField)     // in create form
void fillDateTimeFieldInSpotEdit(String name, Long value, boolean isTimeField) // in spot-edit
void fillDateTimeFieldByLocator(Locator fieldLocator, Long value, boolean isTimeField)  // by locator

// Submit
void submit()            // tries FORM_SAVE then FORM_SUBMIT
void submit(String name) // clicks button by name
```

### 19.1 Date helper — PlaceholderUtil
```java
// Date offset from today (isAhead=true → future, false → past)
Long date = PlaceholderUtil.getDateInMilliSeconds(int days, int months, int years, boolean isAhead)
    // e.g. getDateInMilliSeconds(2, 0, 0, true) → 2 days from now

// Datetime offset
Long dt = PlaceholderUtil.getDateTimeInMilliSeconds(int minutes, int hours, int days, int months, int years, boolean isAhead)

// Usage:
actions.formBuilder.fillDateField(EntityConstants.REVIEW_DATE, PlaceholderUtil.getDateInMilliSeconds(30, 0, 0, true));
```

---

## SECTION 20 — CRITICAL RUNTIME GOTCHAS (from real debugging)

### 20.1 `isClientFramework=false` = ENTIRE form fill is silently skipped (FORBIDDEN trap)
`fillInputForAnEntity(boolean isClientFramework, ...)` has this guard at line 46:
```java
if(isClientFramework) {
    // all form-fill logic inside here
}
```
If `isClientFramework=false`, the method is a **complete no-op** — nothing is filled, no error thrown.
**Always check** `entity/conf/<module>/<entity>.json` for `"is_client_framework": true/false` before trusting form fill.
- Problem module: `"is_client_framework": true` → form fill WILL execute
- If missing or false → all `fillInputForAnEntity` calls silently do nothing

### 20.2 `default: break` in `fillInputForFieldInClientFW()` = silent skip for unknown field_type
The switch statement in `FormBuilder` handles: `input`, `select`, `multiselect`, `html`, `date`, `datetime`, `textarea`, `criteria`, `picklist`, `attachment`.
**Any field with a missing or unrecognized `field_type` hits `default: break`** → silently skipped.
Known affected fields in `problem.json`:
- `"note"` — no `field_type` → never filled by `fillInputForAnEntity`
- `"known_error_details-is_known_error"` — no `field_type` → never filled
These MUST be handled manually via explicit `actions.click(locator)` or `actions.type(locator, value)`.

### 20.3 Checkbox/boolean fields — NEVER rely on `fillInputForAnEntity` (REQUIRED)
No `boolean` or `checkbox` case exists in the switch statement.
`getValueAsStringFromInputUsingAPIPath()` returns `null` for JSON booleans → field is silently skipped.
**Rule:** ALL checkbox interactions must be done explicitly:
```java
actions.click(SolutionLocators.SolutionCreateForm.SOLUTION_IS_PUBLIC_1);  // explicit click
```
Never put `"is_public": true` in entity conf and expect it to be toggled by `fillInputForAnEntity`.

### 20.4 `actions.click(locator)` already calls `waitForAjaxComplete()` BEFORE clicking
No need to add a manual `waitForAjaxComplete()` after clicking. Adding it creates a double-wait.
The wait happens BEFORE the click, not after — page transition happens after the click.
If the next action fails, add `Thread.sleep(1000)` not `waitForAjaxComplete()`.

### 20.5 `actions.getText(locator)` has a 3-second timeout (PREFERRED)
`getText` calls `waitForAnElementToAppear` with a 3-second timeout internally.
On slow-loading pages, this can miss content. If content is not found, add `Thread.sleep(2000)` before `getText`.

### 20.6 preProcess runs in ADMIN session; test method body runs in USER session (REQUIRED)
Session context during test lifecycle:
1. `initializeAdminSession()` → browser is logged in as **admin**
2. `preProcess(group, dataIds)` → REST API calls run **in admin session** (correct permissions)
3. `switchToUserSession()` → browser switches to scenario user
4. `process(method)` → test method body runs **in user session**

**CRITICAL:** Any API call (e.g., `createSolutionTemplateAndGetName()`) placed INSIDE the test method
body runs in the user session. Regular users cannot create templates/configs → `sdpAPICall` returns
null → NPE. ALL prerequisite API calls MUST be in the `preProcess` group method, NOT the test body.

### 20.7 `preProcess` exception handling varies by module
- `Solution.java`: `catch(Exception) { return false; }` — **silently swallows all exceptions**. If preProcess fails, test is skipped with zero visibility.
- `ProblemsCommonBase.java`: calls `addFailureReport(...)` before `return false` — visible in report.
Always use `addFailureReport()` in preProcess catch blocks, never silent swallow.

### 20.8 Locator ambiguity — `button[contains(text(),'X')]` vs `normalize-space(text())='X'`
Using `contains(text())` for action/submit buttons matches multiple buttons on the same page.
**REQUIRED:** For submit/action buttons, always use `normalize-space(text())='ExactText'`:
```java
// WRONG — may match "Add And Approve" button too
By.xpath("//button[contains(text(),'Add')]")

// CORRECT — exact match only
By.xpath("//button[normalize-space(text())='Add']")
```
High-risk locator patterns found in codebase (potential false-positive matches):
| File | Locator | Risk |
|------|---------|------|
| `ReleaseTaskLocators.java` | `//button[contains(text(),'X')]` | Generic match anywhere on page |
| `ProjectLocators.java` | `//button[contains(text(),'Delete')]` | Matches any Delete button |
| `ProblemLocators.java` | `//button[contains(text(),'Add Note')]` | Could match "Add Note Template" |
Scoped containers are acceptable: `//div[@id='X']/descendant::button[contains(text(),'Y')]` is OK.

### 20.9 Problem module `Actions` dropdown — key action strings
The "Actions" dropdown in Problem detail view (`ProblemLocators.Detailview.ACTIONS_MENU`) uses:
```java
ProblemConstants.Actions.ADD_NOTE      = "Add Note"
ProblemConstants.Actions.ADD_TASK      = "Add Task"
ProblemConstants.Actions.DELETE_PROBLEM = "Delete Problem"
ProblemConstants.Actions.MARK_KNOWN_ERROR = "Mark as Known Error"
```
Access via: `actions.click(ProblemLocators.Detailview.ACTIONS_MENU.apply(ProblemConstants.Actions.ADD_NOTE))`

### 20.10 `SOLUTION_ADD` / action button disambiguation — real bug that was fixed
`SOLUTION_ADD` locator was `//button[contains(text(),'Add')]` → matched "Add And Approve" button.
Fix: changed to `//button[normalize-space(text())='Add']` — this exact fix was applied in Feb 2026.
Pattern: whenever a page has two buttons where one is a substring of the other, ALWAYS use
`normalize-space(text())='ExactName'` for the shorter-named button.

### 20.11 Problem `ACTIONS_MENU` locator (detail view actions dropdown)
```java
// In ProblemLocators.Detailview:
public static final Function<String, Locator> ACTIONS_MENU =
    (action) -> new Locator(By.xpath("//div[@class='search-menu']/descendant::a[text()='" + action + "']"), action + " action in details page");
```
This uses `text()='exact'` (already exact-match safe) — no ambiguity issue here.

### 20.12 Copy Problem flow — how to trigger copy in Problem detailview
The "Copy Problem" action is NOT in `ProblemConstants.Actions` (Actions dropdown).
It is triggered from the **listview row action gear**:
```java
// Step 1: Search for the problem in listview
actions.listView.columnSearch(ProblemConstants.ListviewColumns.TITLE, LocalStorage.getAsString("uniqueString"));
// Step 2: Click action gear for the row (by entity ID)
actions.click(ProblemLocators.Listview.ACTIONGEAR_DATAROWID.apply(getEntityId()));
// Step 3: Click "Copy Problem" option
actions.click(ProblemLocators.Listview.ACTIONGEAR_OPTIONS.apply("Copy Problem"));
// Step 4: Submit the copy popup
actions.click(ProblemLocators.Detailview.COPY_PROBLEM_SUBMIT);
// Step 5: Verify the copied problem title in detail view
```
The copy popup submit button ID is `submitCopy` (same pattern as Request/Project modules).

### 20.13 `SolutionAPIUtil` vs `ProblemAPIUtil` — different patterns
- `SolutionAPIUtil.createSolutionTemplateAndGetName(path, data)` → creates template, stores in LocalStorage
- `ProblemAPIUtil.storeProblemModuleId()` → stores module ID — called at top of every preProcess
- `ProblemAPIUtil.addNotestoProblem(entityId, data)` → adds note to problem via REST API
Key: `ProblemAPIUtil` is available as `problemAPIUtil` field in `ProblemsCommonBase`.


---

## LEARNED RULES (auto-generated by LearningAgent)

### [DON'T] Avoid using deprecated or non-existent methods
_Section: SECTION 2 — CODE QUALITY | Learned from: Solution.createUnapprovedSolutionWithCustomTopicRevDateExpDate | Date: 2026-02-27_

Do not use methods that have been deprecated or do not exist in the current version of the library. This can lead to runtime errors like NoSuchMethodError.

```java
// ❌ WRONG
LocalAutomationData.Builder.isLocal(Boolean)
```

### [DON'T] Avoid using deprecated methods
_Section: SECTION 2 — CODE QUALITY | Learned from: Solution.createAndShareApprovedPublicSolutionFromDV | Date: 2026-02-27_

Do not use methods that have been marked as deprecated or removed in the library. This can lead to runtime errors like NoSuchMethodError.

```java
// ❌ WRONG
LocalAutomationData.Builder.isLocal(Boolean)
```

### [DON'T] Avoid using deprecated or non-existent methods
_Section: SECTION 2 — CODE QUALITY | Learned from: Solution.createAndShareApprovedPublicSolutionFromDV | Date: 2026-02-27_

Do not use methods that have been removed or replaced in newer versions of the library. Always check for updates and deprecations.

```java
// ❌ WRONG
LocalAutomationData.Builder.isLocal(Boolean)
```

### [DON'T] Avoid using deprecated methods
_Section: SECTION 2 — CODE QUALITY | Learned from: Solution.createUnapprovedSolutionWithCustomTopicRevDateExpDate | Date: 2026-02-27_

Do not use methods that have been marked as deprecated or removed in the library. This can lead to runtime errors like NoSuchMethodError.

```java
// ❌ WRONG
LocalAutomationData.Builder.isLocal(Boolean)
```

### [DON'T] Avoid using deprecated or non-existent methods
_Section: SECTION 2 — CODE QUALITY | Learned from: Solution.createAndShareApprovedPublicSolutionFromDV | Date: 2026-02-27_

Do not use methods that have been deprecated or do not exist in the current version of the library. This can lead to runtime errors like NoSuchMethodError.

```java
// ❌ WRONG
LocalAutomationData.Builder.isLocal(Boolean)
```

### [DON'T] Avoid using deprecated methods
_Section: SECTION 2 — CODE QUALITY | Learned from: Solution.createUnapprovedSolutionWithCustomTopicRevDateExpDate | Date: 2026-02-27_

Do not use methods that have been marked as deprecated or removed in the library. This can lead to runtime errors like NoSuchMethodError.

```java
// ❌ WRONG
LocalAutomationData.Builder.isLocal(Boolean)
```

### [DON'T] Avoid using deprecated or non-existent methods
_Section: SECTION 2 — CODE QUALITY | Learned from: Solution.createAndShareApprovedPublicSolutionFromDV | Date: 2026-02-27_

Do not use methods that have been deprecated or do not exist in the current version of the library. This can lead to runtime errors like NoSuchMethodError.

```java
// ❌ WRONG
LocalAutomationData.Builder.isLocal(Boolean)
```

### [DON'T] Avoid using deprecated or non-existent methods
_Section: SECTION 3 — CODE QUALITY AND MAINTENANCE | Learned from: Solution.createUnapprovedSolutionWithCustomTopicRevDateExpDate | Date: 2026-02-27_

Do not use methods that have been deprecated or do not exist in the current version of the library. This can lead to runtime errors like NoSuchMethodError.

```java
// ❌ WRONG
LocalAutomationData.Builder.isLocal(Boolean)
```