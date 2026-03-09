# AutomaterSelenium — AI Code-Generation Rules
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
- Use `PORTAL_BASED` for scenarios that have **side effects on other test cases** in the suite — e.g. business rules, SLA triggers, automation rules. These scenarios must run in **isolation**: their effects are scoped and cleaned up within their own session so they don't contaminate other tests running in the same suite.
- `USER_BASED` is for scenarios whose execution does not affect the global state seen by other test cases in the suite.

```java
// CORRECT
runType = ScenarioRunType.USER_BASED

// WRONG — omitting it silently defaults to PORTAL_BASED
// (no runType field)
```

### 2.4 switchOn — valid values and when to use

Controls **when the browser session switches from admin → scenario user** during the test lifecycle:

| Value | When session switches | Implication |
|---|---|---|
| `AFTER_PRE_PROCESS` | After `preProcess()` completes | **preProcess runs as admin** — REST API calls have full permissions. ✅ Default for almost all tests. |
| `BEFORE_PRE_PROCESS` | Before `preProcess()` runs | preProcess runs as the scenario user — only use when the scenario user must perform the setup themselves (e.g. requester creating their own request in preProcess). |
| `NEVER` | Never — stays in admin session | No session switch; both preProcess and test method run as admin. |

> ⚠️ **NPE trap with `BEFORE_PRE_PROCESS`**: If a non-admin scenario user does not have permission to create templates/topics/entities, the `sdpAPICall` JS returns null → `response` is null → NPE in preProcess. Only use `BEFORE_PRE_PROCESS` when you explicitly need preProcess in the user session.

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

### 5.1a preProcess ownership — WHERE the method lives (CRITICAL)

`preProcess()` is typically defined in the module parent class, **but subclasses can and do
override it**. Always **check the subclass first** for a `preProcess()` override before
looking in the parent. If the subclass overrides it, that is the authoritative implementation.
If no override in the subclass, fall back to the parent class.

```
Module hierarchy examples:

  Changes:    Change extends Entity          ← owns preProcess() with all group branches
              DetailsView extends Change     ← inherits preProcess() — no override needed

  Solutions:  SolutionBase extends Entity   ← base helpers/utilities
              Solution extends SolutionBase ← owns preProcess() with all group branches
                                               ends with: return super.preProcess(group, dataIds)

  Workflows:  Workflow extends Entity       ← base groups only
              ChangeWorkflow extends Workflow ← may override preProcess() for module-specific groups
```

**Rule — discover available groups (CHECK IN ORDER):**
1. Check the leaf/subclass file for a `preProcess()` override — if present, read it first.
2. If the subclass ends with `return super.preProcess(group, dataIds)`, also read the parent.
3. Check `class <Subclass> extends <Parent>` at the top of the file to find the parent.

**Rule — where to add new group else-if blocks:**
- New group needed only for a specific subclass → override in that subclass + call `super.preProcess()` at end.
- New group applicable to the whole module → add to the parent class.
- FORBIDDEN: duplicating a group branch in a subclass when the parent already handles it.

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

### 5.6 ⭐ GROUP REUSE — prefer reusing existing groups over adding new else-if blocks

Before adding a new else-if branch to `preProcess()`, **READ the existing preProcess() body** first.
If an existing group already:
1. Calls the API to create the entity type you need
2. Stores the entity ID and name in `LocalStorage` under keys you can read

→ **REUSE that group value** in your `@AutomaterScenario`. Zero new preProcess code needed.

```java
// Example: "create" group in Change.preProcess() already does:
//   ChangeAPIUtil.createChange(dataIds[0])  → stores LocalStorage(getName(), changeId)
//                                            → stores LocalStorage("changeName", name)

// ✅ CORRECT — new scenario reuses "create" group, reads LocalStorage directly:
@AutomaterScenario(id="SDPOD_AUTO_CH_DV_050", group="create", dataIds={ChangeAnnotationConstants.Data.CREATE_CHANGE_API}, ...)
public void verifyChangeDetailView() { ... }

// In the implementation method, just read LocalStorage:
String changeId   = getEntityId();                      // = LocalStorage.getAsString(getName())
String changeName = LocalStorage.fetch("changeName");

// ❌ WRONG — adds redundant else-if block when "create" already serves the purpose:
} else if ("createForDetailView".equalsIgnoreCase(group)) {   // ← FORBIDDEN duplication
    ChangeAPIUtil.createChange(dataIds[0]);
}
```

**Decision flow before writing any preProcess code:**
```
Does an existing group in preProcess() create the entity type I need
AND store the LocalStorage keys I need?
  → YES: use that group value. ZERO new preProcess code.
  → NO:  Add a new else-if block with a new group string.
```

**FORBIDDEN**: Adding a new `else-if` block for a group that is functionally identical to an existing group (same API call, same LocalStorage keys).

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
ScenarioRunType.USER_BASED    // ← use for scenarios with no cross-test side effects
ScenarioRunType.PORTAL_BASED  // ← use for isolated scenarios that affect global state
```

**When to use which:**
- `USER_BASED` — scenario does not trigger side effects that would impact other tests running in the same suite (e.g. standard CRUD scenarios).
- `PORTAL_BASED` — scenario triggers automation-level side effects (business rules, SLA, workflow automation) that could interfere with other test cases. These run in isolation: the scenario executes and its effects are cleaned up within that isolated session before the next test runs.

> ⚠️ **PORTAL_BASED in a UserBased flow is SKIPPED, not FAILED.**
> `EntityCase` checks: if `scenarioDetails.getRunType() == PORTAL_BASED` and `sessionDetails.getGroupType().equalsIgnoreCase("UserBased")` then scenario is skipped (`scenarioDetails.setRestrictRerun(true)`). This is an incompatible-run-type skip, not a test failure.

### 6.4 SwitchToUserSession constants
```java
SwitchToUserSession.AFTER_PRE_PROCESS   // ordinal 1 — default: preProcess in admin session, test method in user session
SwitchToUserSession.BEFORE_PRE_PROCESS  // ordinal 0: both preProcess AND test method run in user session
SwitchToUserSession.NEVER               // ordinal 2: no session switch — everything in admin session
```
> See Section 2.4 for full explanation and NPE trap.

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

## SECTION 8b — DATA REUSE (CRITICAL — prevents duplicate data entries)

### 8b.1 ALWAYS check existing data before creating new entries

Before creating ANY new `*_data.json` entry, `DataConstants` constant, or `AnnotationConstants.Data` constant:
1. Read the existing `*_data.json` file and list all top-level keys
2. Read the existing `*AnnotationConstants.java` → `Data` interface for all preProcess data IDs
3. Read the existing `*DataConstants.java` for all `TestCaseData` constants

### 8b.2 REUSE existing entries when field payloads match

If an existing data JSON entry provides the same entity creation data (e.g. creating a basic change,
creating a basic incident request), **REUSE that key** — do NOT create a new one.

```
# WRONG — new entry duplicates existing "create_change_API"
"create_change_for_linking_api": { "data": { "title": "...", "status": {"name": "Open"} } }

# CORRECT — reuse the existing key in dataIds and preProcess
dataIds = { ChangeAnnotationConstants.Data.CREATE_CHANGE_API }
```

### 8b.3 Only create new entries for genuinely new data

A new `*_data.json` entry is justified ONLY when:
- The field combination is meaningfully different (e.g. different template, different status)
- No existing key covers the same API setup payload
- It's UI test data (not preProcess API data) with unique assertions

### 8b.4 FORBIDDEN patterns
- Creating a new `create_<entity>_*` entry when one already exists with matching fields
- Adding new `AnnotationConstants.Data` constants that map to existing JSON keys
- Duplicating preProcess API setup data under a different name

### 8b.5 ⭐ LocalStorage pre-seed — customize an existing JSON entry without duplicating it (REQUIRED TECHNIQUE)

If a `*_data.json` entry contains `$(custom_KEY)` placeholders and you need to provide a specific
value for that placeholder, **store it in LocalStorage BEFORE calling `getTestCaseData()`**.
This lets you reuse the same JSON entry with different runtime values instead of creating a new entry.

How `$(custom_KEY)` resolution works:
```
LocalStorage.store("KEY", value)  →  $(custom_KEY) in JSON  →  resolves to value at read time
```

**In the test method body — pre-seed BEFORE `getTestCaseData()`:**
```java
// JSON entry has: "template": {"name": "$(custom_template_name)"}

// ❌ WRONG — creating a new JSON entry just for a different template:
// "create_change_special_template": { "data": { "template": {"name": "My Special Template"} } }

// ✅ CORRECT — pre-seed LocalStorage, then reuse existing JSON key:
LocalStorage.store("template_name", LocalStorage.getAsString("targetTemplateName"));  // from preProcess
JSONObject inputData = getTestCaseData(ChangeDataConstants.ChangeData.CREATE_CHANGE_WITH_TEMPLATE);
// $(custom_template_name) resolves to whatever is in LocalStorage["template_name"]
```

**In preProcess (for API setup data with placeholders):**
```java
// Storing values in preProcess makes them available to any JSON with $(custom_KEY):
LocalStorage.store("solution_template", templateName);  // used by $(custom_solution_template)
LocalStorage.store("topic", topicName);                 // used by $(custom_topic)
LocalStorage.store("change_id", changeId);              // used by $(custom_change_id)
```

**Decision flow — apply before every `getTestCaseData()` call:**
```
Need a data value (template name, topic, linked entity, etc.) in your JSON?
  ↓
  1. Does an existing *_data.json entry have the right shape but with a $(custom_KEY) placeholder?
     → YES: LocalStorage.store("KEY", value)  then  getTestCaseData(EXISTING_KEY)  ← REUSE
     → NO:  Does ANY existing entry provide the same payload with fixed values?
            → YES: getTestCaseData(EXISTING_KEY)  ← REUSE AS-IS
            → NO:  Create a new *_data.json entry  ← only this case justifies a new entry
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

### 9.4 FORBIDDEN — inline JSONObject construction for test/API data (CRITICAL)

All entity test data (UI form inputs AND preProcess API payloads) MUST be defined in
`*_data.json` files and loaded via `getTestCaseData()` or `getTestCaseDataUsingCaseId()`.

**NEVER construct JSONObject payloads inline in Java code.** This bloats the test methods,
bypasses placeholder resolution (`$(unique_string)`, `$(custom_KEY)`, etc.), makes data
non-reusable across scenarios, and breaks the framework's data-driven design.

```java
// ❌ FORBIDDEN — inline JSON construction (bloated, non-reusable, no placeholders)
JSONObject inputData = new JSONObject();
inputData.put("title", "Test Change " + System.currentTimeMillis());
inputData.put("change_type", new JSONObject().put("name", "Standard"));
inputData.put("priority", new JSONObject().put("name", "High"));
inputData.put("impact", new JSONObject().put("name", "Low"));
inputData.put("status", new JSONObject().put("name", "Open"));
// ... 20 more .put() lines

// ✅ CORRECT — define in *_data.json, load via DataConstants
JSONObject inputData = getTestCaseData(ChangeDataConstants.ChangeData.CREATE_CHANGE);
// All fields, placeholders, and lookup objects are in the JSON file
```

**Same rule applies inside `preProcess()` else-if blocks:**
```java
// ❌ FORBIDDEN — inline construction inside preProcess (bloated, unreadable, non-reusable)
} else if ("createPoWithContract".equalsIgnoreCase(group)) {
    JSONObject contractInput1 = new JSONObject();
    contractInput1.put("name", "ContractAssoc1_" + ts);
    contractInput1.put("vendor", new JSONObject().put("name", LocalStorage.getAsString("PO_Vendor")));
    contractInput1.put("is_definite", true);
    contractInput1.put("active_from", new JSONObject().put("value", String.valueOf(now)));
    contractInput1.put("type", new JSONObject().put("name", "Lease"));
    contractInput1.put("owner", new JSONObject().put("name", userName).put("email_id", userEmail));
    // ... repeated for contractInput2, contractInput3 ...
    JSONObject contractResp1 = restAPI.createAndGetResponse("contract", "contracts", new JSONObject().put("contract", contractInput1));
}

// ✅ CORRECT — data in *_data.json with placeholders, loaded in preProcess via dataIds
// In contract_data.json:
// "create_contract_for_po_assoc": {
//   "data": {
//     "name": "ContractAssoc_$(unique_string)",
//     "vendor": {"name": "$(custom_PO_Vendor)"},
//     "is_definite": true,
//     "active_from": {"value": "$(date, 0, ahead)"},
//     "type": {"name": "Lease"},
//     "owner": {"name": "$(user_name)", "email_id": "$(user_email_id)"}
//   }
// }

// In preProcess:
} else if ("createPoWithContract".equalsIgnoreCase(group)) {
    PurchaseAPIUtil.createPurchase("contract_association_test");
    JSONObject contractData = getTestCaseDataUsingCaseId(dataIds[0]);
    JSONObject resp1 = restAPI.createAndGetResponse("contract", "contracts", getInputData(contractData));
    LocalStorage.store("contractId1", resp1.getString("id"));
    LocalStorage.store("contractName1", resp1.getString("name"));
}
```

**The ONLY acceptable uses of `new JSONObject()` in test code are:**
1. Small utility objects for search criteria / API query filters (not entity data)
2. Wrapping an already-loaded data object: `getInputData(inputData)` → `{"change": inputData}`
3. Overriding a single field on a loaded object: `inputData.put("status", new JSONObject().put("name", "Closed"))`

**For dynamic values**, use `$(custom_KEY)` placeholders in JSON + `LocalStorage.store("KEY", value)` before `getTestCaseData()` — see Section 8b.5.

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
// ⚠️ WARNING: MODULE_TITLE h1 text includes the display ID prefix (e.g. "SOL-8 MyTitle").
// actions.validate.textContent(MODULE_TITLE, "MyTitle") will FAIL due to the prefix.
// ALWAYS use verifyTitleInDetailsPage() which handles the prefix correctly:
Boolean ok = actions.detailsView.verifyTitleInDetailsPage(expectedTitle);

// If you must use textContent directly, include the display ID in the expected string,
// or use: actions.validate.textContent(MODULE_TITLE, displayId + " " + expectedTitle)

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

### [DON'T] Never use deprecated or non-existent methods
_Section: SECTION 2 — CODE QUALITY | Consolidated from 8 duplicate entries | Date: 2026-02-27 / 2026-03-02_

Do not use methods that have been deprecated or removed. This causes `NoSuchMethodError` at runtime.

```java
// ❌ WRONG — does not exist; was removed from the framework
LocalAutomationData.Builder.isLocal(Boolean)

// ❌ WRONG — non-existent framework method
driver.get(url); // not implemented in this Selenium wrapper
```

---

## SECTION 23 — ACTIONSUTIL / APIUTIL USAGE (REQUIRED — applies to ALL entities, ALL modules)

_Learned from: CH-286 Linking Changes refactoring — March 2026_

### 23.0 PRE-GENERATION ANALYSIS — MANDATORY WORKFLOW (4 steps, run BEFORE writing any test code)

> Every new scenario generation MUST complete all 4 steps in order. No exceptions.

**STEP 1 — Read the entity's util files in full**

```bash
# Discover util files:
find src/com/zoho/automater/selenium/modules/<module>/<entity>/utils/ -name "*.java" | sort

# List all existing methods (then READ the file to understand parameter shapes + purpose):
grep -n "public static" modules/<module>/<entity>/utils/<Entity>ActionsUtil.java
grep -n "public static" modules/<module>/<entity>/utils/<Entity>APIUtil.java
```

For every `public static` method found: note its name, parameters, and what UI operation it performs.

**STEP 2 — Map each scenario operation to a method**

Before generating a single line of scenario code, produce a decision table:

| Scenario operation | Existing method? | Decision |
|---|---|---|
| Navigate to tab | `openAssociationTab()` | REUSE |
| Link parent change | `linkParentChangeViaUI(name, id)` | REUSE |
| Some new UI flow | *(not found in util file)* | CREATE NEW |
| preProcess API create | `ChangeAPIUtil.createChange(data)` | REUSE |

**STEP 3 — Create missing methods in the util file FIRST**

For each `CREATE NEW` in the decision table:
1. Add `public static void <methodName>(...) throws Exception { ... }` to `<Entity>ActionsUtil.java`
2. One method = one complete named UI operation (not a single click; not an entire test)
3. Compile the util file before proceeding to Step 4

**STEP 4 — Generate the scenario using only util calls + assertions**

Test method body = utility calls + assertions + `addSuccessReport`/`addFailureReport` ONLY.  
If you are typing `actions.click(` directly in a test method body → STOP → move it to the util first.

### 23.1 Check entity utils BEFORE writing any UI block (REQUIRED)

### 20.2 Test method body must contain only: utility calls + assertions + report calls (REQUIRED)

```java
// ✅ CORRECT — test method is thin
public void verifySingleParentConstraint() throws Exception {
    ChangeActionsUtil.openAssociationTab();
    ChangeActionsUtil.linkParentChangeViaUI(
        LocalStorage.getAsString("targetChangeName1"), LocalStorage.getAsString("targetChangeId1")
    );
    if(actions.isElementPresent(ChangeLocators.LinkingChange.DETACH_PARENT_CHANGE)) {
        addSuccessReport("Detach button visible after parent linked");
    } else {
        addFailureReport("Detach button not found", "Missing detach");
    }
}

// ❌ WRONG — clicks/waits inlined instead of calling utility
public void verifySingleParentConstraint() throws Exception {
    actions.click(ChangeLocators.LinkingChange.LHS_ASSOCIATION_TAB);  // ← extract to openAssociationTab()
    actions.waitForAjaxComplete();
    actions.click(ChangeLocators.LinkingChange.ATTACH_BUTTON_DROPDOWN);  // ← extract to openAttachParentChangePopup()
    actions.click(ChangeLocators.LinkingChange.ATTACH_PARENT_CHANGE_OPTION);
    actions.waitForAjaxComplete();
    // ... same 6-click block appears in every other test too
}
```

### 20.3 Util methods must be generic and parameterized (REQUIRED)

**One well-parameterized method beats a family of thin duplicates.** Use method arguments to
segregate flow branches instead of creating twin methods that differ by one value.

| Thin/duplicated ❌ | Parameterized/generic ✅ |
|---|---|
| `openAttachParentChangePopup()` + `openAttachChildChangePopup()` | `openAttachChangePopup(String type)` |
| `linkChange1()` + `linkChange2()` | `linkChangeViaUI(String name, String id)` |
| `verifyParentLinkInTab()` + `verifyChildLinkInTab()` | `verifyLinkInAssociationTab(String type, String name)` |

**Decision rule before creating a new util method:**
- Will this sequence appear in more than one test? → extract + parameterize to cover all variants
- Do two existing util methods differ by only 1 argument? → merge into one parameterized method
- Is it a one-off `actions.click()` / `actions.getText()` unique to one scenario? → leave inline

### 20.4 Class declaration shape (REQUIRED — no exceptions)

```java
// Every *ActionsUtil.java in this codebase follows this exact shape:
public final class <Entity>ActionsUtil extends Utilities {
    // All methods: public static void/boolean/String
    // extends Utilities: gives access to static fields actions, report, restAPI
}
```

### 20.5 Inline actions in test body — when OK vs FORBIDDEN

**OK —** minimal `actions.click()` / `actions.getText()` inline for a **truly one-off, scenario-specific
step** that is not reused anywhere else.

**FORBIDDEN —** duplicating the same multi-step sequence (2+ lines) across multiple test methods
without extracting it to a util. Sign of violation:
```bash
grep -A5 "LHS_ASSOCIATION_TAB" DetailsView.java  # same tab click in 10+ methods → extract it
```

### 20.6 Known entity utility files — ALWAYS discover first, do NOT rely on this table alone

> **Every module in this codebase has a `utils/` folder** with `*ActionsUtil.java` and/or
> `*APIUtil.java`. There are 100+ util files. Always run discovery for the entity you're working on:

```bash
find src/com/zoho/automater/selenium/modules/<module>/<entity>/utils/ -name "*.java" | sort
```

**Module registry (sample — not exhaustive):**

| Module | Entity | ActionsUtil | APIUtil |
|--------|--------|-------------|--------|
| changes | change | `changes/change/utils/ChangeActionsUtil.java` | `changes/change/utils/ChangeAPIUtil.java` |
| changes | downtime | `changes/downtime/utils/DowntimeActionsUtil.java` | `changes/downtime/utils/DowntimeAPIUtil.java` |
| solutions | solution | `solutions/solution/utils/SolutionActionsUtil.java` | `solutions/solution/utils/SolutionAPIUtil.java` |
| requests | request | — | `requests/request/utils/RequestAPIUtil.java` |
| problems | problem | `problems/problem/utils/ProblemActionsUtil.java` | `problems/problem/utils/ProblemAPIUtil.java` |
| releases | release | `releases/release/utils/ReleaseActionsUtil.java` | `releases/release/utils/ReleaseAPIUtil.java` |
| projects | project | `projects/project/utils/ProjectActionsUtil.java` | `projects/project/utils/ProjectAPIUtil.java` |
| assets | asset | `assets/asset/utils/AssetActionsUtil.java` | `assets/asset/utils/AssetAPIUtil.java` |
| general | dashboard | `general/dashboard/utils/DashboardActionsUtil.java` | `general/dashboard/utils/DashboardAPIUtil.java` |
| maintenance | — | `maintenance/utils/MaintenanceActionsUtil.java` | `maintenance/utils/MaintenanceAPIUtil.java` |
| contracts | contract | `contracts/contract/utils/ContractActionsUtil.java` | `contracts/contract/utils/ContractAPIUtil.java` |
| admin | — | `admin/utils/AdminActionsUtil.java` | `admin/utils/AdminAPIUtil.java` |
| admin | workflows | `admin/automation/workflows/utils/WorkflowsActionsUtil.java` | `...WorkflowsAPIUtil.java` |
| admin | businessrules | `admin/automation/businessrules/utils/BusinessRulesActionsUtil.java` | `...BusinessRulesAPIUtil.java` |

> Never assume a util file doesn't exist. Run discovery first.

---

## SECTION 21 — REST API USAGE RULES

_Learned from: analysis of RestAPI.java (503 lines), Change.java preProcess patterns, ClientFrameworkActions hierarchy | Date: 2026-03-03_

> 📖 **API Reference Doc**: `docs/api-doc/SDP_API_Endpoints_Documentation.md`
> Before writing ANY `preProcess()` API call, check this doc for:
> - Exact API path (e.g. `api/v3/changes`, `api/v3/requests/{id}/notes`)
> - Input wrapper key (e.g. `{"change": {...}}`, `{"request": {...}}`)
> - Available sub-resource paths (notes, tasks, worklogs, approvals, etc.)
> This doc covers all 16 SDP modules with worked automation case examples.

### 21.1 All API calls go through browser JavaScript (REQUIRED understanding)

REST API calls in this framework use `sdpAPICall()` JavaScript function executed via Selenium `JavascriptExecutor`. There is **no direct HTTP client**.

```java
// ✅ CORRECT — Use RestAPI instance methods
JSONObject response = restAPI.createAndGetResponse(getName(), getModuleName(), getInputData(inputData));

// ❌ WRONG — Never try to use HttpClient, OkHttp, or curl
HttpClient client = HttpClient.newHttpClient();  // DOES NOT EXIST in this framework
```

### 21.2 Reuse existing entity creation methods from super class (REQUIRED)

Every entity has a standard creation method in its parent class (e.g., `Change.createChangeGetResponse()`). **Always use it** instead of creating custom API utility methods.

```java
// ✅ CORRECT — Use the parent class method
createChangeGetResponse(dataIds[0]);

// ❌ WRONG — Reinventing the creation pattern
ChangeAPIUtil.createChange(dataIds[0]);  // Unnecessary if createChangeGetResponse exists

// ✅ CORRECT — For additional entities of same type, use DataUtil for fresh placeholders
JSONObject targetData = DataUtil.getInputDataForRestAPI(getModuleName(), getName(), dataIds[0], fields);
JSONObject targetResponse = restAPI.createAndGetResponse(getName(), getModuleName(), getInputData(targetData));
```

### 21.3 preProcess runs in admin session; test methods run in user session (CRITICAL)

```java
// ✅ CORRECT — Create entities in preProcess (admin session = full permissions)
protected boolean preProcess(String group, String[] dataIds) {
    createChangeGetResponse(dataIds[0]);  // Works — admin can create
    return true;
}

// ❌ WRONG — Creating entities via API inside test method body
public void myTestMethod() {
    ChangeAPIUtil.createChange(dataId);  // May FAIL — user may lack permissions
}
```

### 21.4 Input data wrapping follows module conventions (REQUIRED)

```java
// Change module wrapping:
getInputData(inputData)  // Returns {"change": {...}}

// Request module wrapping:
new JSONObject().put("request", inputData)  // Returns {"request": {...}}

// ALWAYS use getInputData() helper — don't manually construct wrapper
```

### 21.5 Core RestAPI methods reference (use the right one)

| Method | Returns | Use when |
|--------|---------|----------|
| `create(name, path, data)` | String ID | You only need the entity ID |
| `createAndGetResponse(name, path, data)` | JSONObject entity | You need ID + title + other fields (MOST COMMON) |
| `createAndGetFullResponse(path, data)` | JSONObject raw response | You need the full response envelope |
| `get(path, data)` | JSONObject | Reading entity data |
| `update(path, data)` | JSONObject | Updating an entity |
| `delete(path)` | boolean | Deleting an entity |
| `getEntityIdUsingSearchCriteria(plural, path, data)` | String ID | Finding entity by criteria |
| `getEntityIDUsingFieldValue(path, field, value)` | String ID | Finding by specific field value |

---

## SECTION 22 — POPUP & DROPDOWN HANDLING RULES

_Learned from: analysis of PopUp.java, ListViewForPopUp.java, ClientFrameworkLocators.java, existing association tests | Date: 2026-03-03_

### 22.1 Use `actions.popUp.listView.columnSearch()` for popup table search (REQUIRED)

When searching inside any popup (regardless of popup class), use the popup-specific column search:

```java
// ✅ CORRECT — Popup column search
actions.popUp.listView.columnSearch("Title", LocalStorage.getAsString("targetChangeName1"));

// ❌ WRONG — Main listview column search (searches behind popup)
actions.listView.columnSearch("Title", LocalStorage.getAsString("targetChangeName1"));
```

### 22.2 Framework popup filter methods ONLY work for `slide-down-popup` class popups (REQUIRED)

`actions.popUp.listView.selectFilterUsingSearch()` and `selectFilterWithoutSearch()` use locators scoped to `slide-down-popup`:
```xpath
//*[contains(concat(' ', normalize-space(@class), ' '), ' slide-down-popup')][last()]
```

**For non-standard popups** (e.g., CH-286's `association-dialog-popup`), define custom filter locators:

```java
// ✅ CORRECT for slide-down-popup (standard Attach Request/Problem popups):
actions.popUp.listView.selectFilterWithoutSearch("All Requests");

// ✅ CORRECT for association-dialog-popup (CH-286 linking changes):
actions.click(ChangeLocators.LinkingChangePopup.FILTER_DROPDOWN);
actions.click(ChangeLocators.LinkingChangePopup.FILTER_OPTION.apply("All Changes"));

// ❌ WRONG — trying framework popup filter in non-standard popup:
actions.popUp.listView.selectFilterWithoutSearch("All Changes"); // Will fail — wrong popup class
```

### 22.3 Select2 options render at body level — reuse OPTION_ELEMENT pattern (PREFERRED)

Select2 dropdown (`#select2-drop`) is appended directly to `<body>`, not inside the popup container. This means `FormBuilderLocators.OPTION_ELEMENT` works regardless of which popup triggered the Select2:

```java
// All equivalent — Select2 options are at body level:
actions.click(ClientFrameworkLocators.FormBuilderLocators.OPTION_ELEMENT.apply("All Changes"));
// OR define custom locator with same pattern:
ChangeLocators.LinkingChangePopup.FILTER_OPTION.apply("All Changes");
// Both find: //div[contains(@class,'select2-result-label') and contains(text(),'All Changes')]
```

### 22.4 Identify popup type before choosing approach (REQUIRED check)

Before writing popup interaction code, check the popup container class:
- `slide-down-popup` → Use framework `actions.popUp.*` methods
- `association-dialog-popup` / `ui-dialog` → Use custom locators for filter/trigger, framework for table operations
- Always verify via DOM inspection (Playwright snapshot or browser devtools)

### 22.5 Existing module-specific popup locators take precedence (PREFERRED)

Each module defines its own popup locators (e.g., `ChangeLocators.Popup.*`). Follow the existing pattern:
```java
// ✅ CORRECT pattern (matches existing tests like attachDetachRequestCausedByChangeRHS):
actions.click(ChangeLocators.Popup.CLICK_LISTVIEW_FILTERS);       // Module-specific trigger
actions.click(ChangeLocators.Popup.CLICK_ALL_REQUESTS_FILTERS);   // Module-specific option
actions.popUp.listView.columnSearch("Subject", value);              // Framework table search

// This mixed approach (module locators + framework methods) is the established pattern
```

---

## SECTION 24 — LINKING CHANGES (CH-286) RULES

_Learned from: manually generating 6 test methods for 19 use cases (SDPOD_LINKING_CH_001-019) | Date: 2026-03-03_

### 24.1 LHS Association Tab vs RHS Associations (REQUIRED)

Linking Changes uses a **dedicated LHS Association tab**, NOT the RHS accordion. Always navigate via:
```java
// ✅ CORRECT — LHS tab for linking changes
actions.click(ChangeLocators.LinkingChange.LHS_ASSOCIATION_TAB);

// ❌ WRONG — RHS association pattern (used for requests-caused-by, etc.)
actions.click(ChangeLocators.AssociationTab.RHS_ASSOCIATIONS);
```

### 24.2 Parent = Radio, Child = Checkbox (REQUIRED)

Parent change popup uses **radio buttons** (single selection). Child changes popup uses **checkboxes** (multi-selection, max 25).

```java
// ✅ CORRECT — Radio for single parent
actions.click(ChangeLocators.LinkingChangePopup.SELECT_RADIO_WITH_ENTITYID.apply(parentId));

// ✅ CORRECT — Checkbox for children (can select multiple)
actions.click(ChangeLocators.LinkingChangePopup.SELECT_CHECKBOX_WITH_ENTITYID.apply(childId1));
actions.click(ChangeLocators.LinkingChangePopup.SELECT_CHECKBOX_WITH_ENTITYID.apply(childId2));

// ❌ WRONG — Using checkbox locator for parent selection
actions.click(ChangeLocators.LinkingChangePopup.SELECT_CHECKBOX_WITH_ENTITYID.apply(parentId));
```

### 24.3 Mutual Exclusion — Parent OR Child, Never Both (REQUIRED)

A change can only be a parent OR a child. After linking as one type, the other option must disappear from the Attach dropdown.

```java
// After attaching a parent change:
// ✅ CORRECT — verify child option is no longer available
boolean hasChildOption = actions.isElementPresent(ChangeLocators.LinkingChange.ATTACH_CHILD_CHANGES_OPTION);
assertFalse(hasChildOption, "Child option should be hidden after parent is linked");

// After detaching → BOTH options should return
actions.click(ChangeLocators.LinkingChange.ATTACH_BUTTON_DROPDOWN);
assertTrue(actions.isElementPresent(ChangeLocators.LinkingChange.ATTACH_PARENT_CHANGE_OPTION));
assertTrue(actions.isElementPresent(ChangeLocators.LinkingChange.ATTACH_CHILD_CHANGES_OPTION));
```

### 24.4 preProcess Must Create 3 Changes (REQUIRED for linking tests)

Linking tests need at minimum 3 changes: 1 source (navigated to in UI) + 2 targets (potential parents/children). The preProcess group `CREATE_CHANGES_FOR_LINKING` handles this.

```java
// In Change.java preProcess:
// entityId → source change (opens in details page)
// targetChangeId1, targetChangeName1, targetChangeDisplayValue1 → first target
// targetChangeId2, targetChangeName2, targetChangeDisplayValue2 → second target
// All stored in LocalStorage
```

### 24.5 Popup Column Search — Use the correct method per popup type (REQUIRED)

**Standard SDP association popups** (`slide-down-popup` class — e.g., Attach Request, Attach Problem):
```java
// ✅ CORRECT — framework popup search works for slide-down-popup
actions.popUp.listView.columnSearch("Subject", LocalStorage.getAsString("subject"));
```

**CH-286 Linking Change popups** (`association-dialog-popup` class — different container, different DOM):
```java
// ✅ CORRECT — use ChangeActionsUtil (custom implementation for this popup type)
ChangeActionsUtil.columnSearchInAssociationPopup("Title", LocalStorage.getAsString("targetChangeName1"));

// ❌ WRONG — actions.popUp.listView.columnSearch uses slide-down-popup scoped locators
// and will fail to find the search input inside association-dialog-popup
actions.popUp.listView.columnSearch("Title", LocalStorage.getAsString("targetChangeName1"));

// ❌ WRONG — searches main list view, not the popup
actions.listView.columnSearch("Title", LocalStorage.getAsString("targetChangeName1"));
```

**Rule**: always check the popup container CSS class before choosing which search method to use.

### 24.6 API Contract for Linking (REQUIRED)

Linking is done via the `rel/` sub-path under changes API:
- `PUT api/v3/changes/{id}/rel/parent_change` — link parent
- `DELETE api/v3/changes/{id}/rel/parent_change?ids={id}` — unlink parent
- `PUT api/v3/changes/{id}/rel/child_changes` — link children
- `DELETE api/v3/changes/{id}/rel/child_changes?ids={csv_ids}` — unlink children

```java
// Body for parent link:
{"parent_change":[{"parent_change":{"id":"<targetId>"}}]}

// Body for child link (multiple):
{"child_changes":[{"child_changes":{"id":"<id1>"}},{"child_changes":{"id":"<id2>"}}]}
```

---

### 24.7 Workflow Boundary Tests — Stage-Based vs Flat-Status Module Rule (CH-2320)

> **SOURCE OF TRUTH**: Applies to all workflow statement-tuple-limit boundary tests.

#### Module classification

| Module | Type | `@Override` pattern for `_UI()` tests |
|--------|------|----------------------------------------|
| Incident Request | Flat-status | ❌ Delegate to base — blank canvas has no counted nodes |
| Service Request | Flat-status | ❌ Delegate to base — blank canvas has no counted nodes |
| Problem | Flat-status | ✅ `@Override` needed — pre-creates workflow via API (blank canvas lacks status nodes required for transition loop) |
| Change | **Stage-based** | ✅ `@Override` needed — blank canvas Submission/Close FlowNodes are counted by server |
| Release | **Stage-based** | ✅ `@Override` needed — blank canvas Submission/Closure FlowNodes are counted by server |
| Asset | **Special** | ✅ `@Override` needed — requires `sub_module` injection in API payload; flat-status per sub_module, base won't inject it |

> ⚠️ **Correction from March 7, 2026**: `Problem` is flat-status but still needs `@Override`
> because `createNewBlankWorkflowInCanvas()` produces a canvas without status nodes, causing
> the FieldUpdate drag loop to fail to build valid transitions. Solution: override to pre-create
> a minimal Problem workflow with genuine status IDs via API (`resolveStatusApiPathAndName()` +
> `fetchStageStatuses()` returns `null` to trigger the flat-status builder path), then calibrate
> `baseCount` from the actual server-recorded statement count before dragging the delta.

#### Why this matters

For flat-status modules, a blank canvas opened via `createNewBlankWorkflowInCanvas()` starts
with only a Start/End marker (not counted by the server). Dragging 100 FieldUpdate nodes →
server counts 100 statements → exactly at limit → base `_UI()` works correctly.

For stage-based modules (Change, Release), the blank canvas already contains Submission +
Close/Closure stage FlowNodes that **are counted** by the server. Dragging 100 FieldUpdate nodes
gives `baseCount + 100 > 100` → always exceeds the limit → the "accept at max" test always fails.

#### Required override pattern (stage-based modules)

```java
@Override
protected void verifyStatementTupleLimitRejectionOnOverflow_UI() throws Exception {
    LocalStorage.store("workFlowModuleName", "change"); // or "release"
    // Step 1 — API pre-create a proper workflow with real stage IDs
    WorkflowsAPIUtil.createWorkflowViaAPI(
        getTestCaseData(WorkflowsDataConstants.WorkflowsData.CREATE_WORKFLOW_CHANGE_TRANSITION_VIA_API));
    String workflowId = LocalStorage.getAsString("workflowId");
    String wfName     = LocalStorage.getAsString("workFlowName");

    // Step 2 — Self-calibrate: GET the workflow to count actual server statements
    int baseCount = 4; // conservative default
    try {
        JSONObject wfResp = restAPI.get("workflows/" + workflowId, null);
        if (wfResp != null && wfResp.optJSONObject("workflow") != null) {
            org.json.JSONArray stmts = wfResp.getJSONObject("workflow").optJSONArray("statements");
            if (stmts != null) baseCount = stmts.length();
        }
    } catch (Exception ignore) {}

    // Step 3 — Drag only the delta to reach/exceed the limit
    int dragsNeeded = WorkflowsConstants.TupleLimit.DEFAULT_STATEMENT_LIMIT - baseCount + 1;
    try {
        WorkflowsActionsUtil.openExistingWorkflowInCanvas("Change", wfName); // or "Release"
        actions.click(WorkflowsLocators.Listview.WORKFLOW_RHS_TOGGLE_BUTTON);
        for (int i = 1; i <= dragsNeeded; i++) {
            // ... drag FieldUpdate node and configure ...
        }
        actions.click(WorkflowsLocators.Listview.SAVE_MORE);
        actions.click(WorkflowsLocators.Listview.SAVE_CLOSE);
        actions.waitForAjaxComplete();
        // WORKFLOW_CANCEL_LOCATOR present = canvas stayed open = rejected = PASS
        if (actions.isElementPresent(WorkflowsLocators.Listview.WORKFLOW_CANCEL_LOCATOR)) {
            addSuccessReport("...");
            actions.click(WorkflowsLocators.Listview.WORKFLOW_CANCEL_LOCATOR);
        } else {
            addFailureReport("...", "...");
        }
    } finally {
        restAPI.delete("workflows/" + workflowId);
    }
}
```

#### Verifying workflow save — ALWAYS use API, NEVER re-open by clicking name

After `createWorkflow()` saves, verifying by calling `openExistingWorkflowInCanvas()` is **fragile**:
the list-view locator `//a[contains(@class,'workflow-name') and contains(text(),'...')]` may miss
due to timing or filter state. Use API search instead:

```java
// ✅ CORRECT — API confirmation is authoritative
String workflowId = restAPI.getEntityIdUsingSearchCriteria("workflows", "workflows", searchData);
if (workflowId != null && !workflowId.isEmpty()) {
    addSuccessReport("Workflow saved — confirmed by API id=" + workflowId);
} else {
    addFailureReport("Workflow not found via API after UI creation", workflowName);
}
```

---

## SECTION 25 — ZOHO CODECHECK / CHECKSTYLE RULES

> **Root cause of hg push failures (March 7, 2026)**: Zoho uses **Checkstyle** (not PMD).
> PMD's `IfStmtsMustUseBraces` was deprecated in PMD 6.2.0. The equivalent Checkstyle rule is
> **`NeedBraces`** which covers ALL block statements: `if`, `else`, `for`, `while`, `do`,
> `try`, `catch`, `finally`.

### 25.1 `NeedBraces` — Inline catch blocks FORBIDDEN

```java
// ❌ WRONG — inline empty catch violates NeedBraces
try {
    someCall();
} catch (Exception ignore) {}

// ✅ CORRECT — multi-line with explicit braces on separate lines
try {
    someCall();
} catch (Exception ignore) {
    // intentionally empty
}
```

### 25.2 ALL single-statement if/for/while bodies must use braces

```java
// ❌ WRONG
if (condition) doSomething();

for (int i = 0; i < n; i++) doSomething(i);

// ✅ CORRECT
if (condition) {
    doSomething();
}

for (int i = 0; i < n; i++) {
    doSomething(i);
}
```

### 25.3 "Error in codecheck invocation" — what it really means

`Error in codecheck invocation` from the Zoho hg push server is a **server infrastructure
crash** (the codecheck runner itself fails before analyzing any code). It does NOT mean your
code has violations. This specific error message is NOT followed by a list of violations.

> If you see actual Checkstyle violations, they appear as a separate report listing file paths,
> line numbers, and rule names (e.g., `NeedBraces`, `MagicNumber`, etc.).
> The "invocation error" is a Zoho infra issue — escalate to the integration team.

### 25.4 Quick scan for NeedBraces violations before pushing

```bash
# Find all single-statement if/for/while/catch without braces
grep -rn "} catch (Exception[^)]*) {}" src/ --include="*.java"
grep -rn "} catch ([^)]*) {}" src/ --include="*.java"
# Also check for single-line if/else/for without braces:
grep -rn "^\s*if (.*)[^{]$\|^\s*else [^{]\|^\s*for (.*)[^{]$" src/ --include="*.java" | grep -v "//"
```

---

## SECTION 26 — TASK NODE CONNECTOR PORTS (Workflow)

### 26.1 Task nodes require specific ports when `has_error_path=true`

When a Task FlowNode is created with `has_error_path: true`, the connection ports change:

| Port name | Direction | Meaning |
|-----------|-----------|---------|
| `output_Completed` | Exit (success) | Task completed without error |
| `output_Overdue` | Exit (error) | Task overdue / error path |
| `input_Requested` | Entry | Inbound connection into the task |

Generic `input`/`output` port names only work for nodes without error paths. Using them
on `has_error_path=true` Task nodes causes the workflow API to return a connection error.

```java
// ✅ CORRECT — Task with error path
JSONObject taskConn = new JSONObject()
    .put("source", taskNodeId).put("sourcePort", "output_Completed")
    .put("target", nextNodeId).put("targetPort", "input_Requested");

// ErrorPath connection
JSONObject errorConn = new JSONObject()
    .put("source", taskNodeId).put("sourcePort", "output_Overdue")
    .put("target", errorHandlerNodeId).put("targetPort", "input_Requested");

// ❌ WRONG — generic ports fail for has_error_path=true Task nodes
JSONObject badConn = new JSONObject()
    .put("source", taskNodeId).put("sourcePort", "output")
    .put("target", nextNodeId).put("targetPort", "input");
```

### 26.2 Task connector chain fix — `createWorkflowWithNTasks()`

> Fixed in rev 5320 (March 6, 2026): The `createWorkflowWithNTasks()` helper in `Workflow.java`
> was using generic `input`/`output` ports for Task nodes that have `has_error_path=true`.
> This caused IR_007 and IR_009 (connector-limit boundary tests) to fail with API rejection.
> Fix: always use `Completed`/`Overdue` ports for Task nodes and `input_Requested` for all targets.

---

## SECTION 27 — EntityCase LIFECYCLE & REPORTING (from framework source analysis, Mar 2026)

### 27.1 `addReport(String message)` — smart single-argument variant

`EntityCase` has **three** reporting methods, not two:

```java
addSuccessReport(String message)                  // always success
addFailureReport(String message, String reason)   // always failure
addReport(String message)                         // SMART: success if no failureMessage, else failure
```

`addReport(message)` inspects `failureMessage.length()`:
- `== 0` → calls `addSuccessReport(message)` + takes success screenshot
- `> 0`  → calls `addFailureReport(message, failureMessage.toString())` + takes failure screenshot

Use `addReport(message)` after `appendFailureMessage(...)` calls to let the accumulated
failure buffer decide the outcome automatically.

### 27.2 `clearFailureMessage()` is called automatically after every `addReport()` call

`addReport()` → `clearFailureMessage()` at end. This resets the buffer so the NEXT step
starts clean. Do NOT call `clearFailureMessage()` manually unless you want to discard
accumulated failures mid-step.

### 27.3 `cleanUp()` destroys ALL singletons at end of every test

`EntityCase.cleanUp()` is called in the `finally` block of `execute()` (the Aalam runner entry point):

```
LocalStorage.destroy()          // All LocalStorage.store() data is gone
AutomaterReport.destroy()       // Report instance cleared
RestAPI.destroy()               // RestAPI instance cleared
ClientFrameworkActions.destroy()
EntityMetaDetails.destroy()     // Entity config cache cleared
DataUtil.destroy()              // JSON data cache cleared  ← important for tests that reload data
ScenarioReport.destroy()
DriverUtil.reset()
```

> **Impact**: LocalStorage is completely fresh for each test run. There is NO state leakage
> between separate test method runs. If two scenarios depend on the same data, each must
> recreate it in its own `preProcess()`.

### 27.4 `addSuccessReport()` auto-captures screenshot; skipping screenshot is framework-controlled

`addReport(..., isSuccess=true)`:
1. Calls `report.addCaseFlow(message)` — adds row to log
2. Calls `actions.captureScreenshot(message)` — takes screenshot with label = the success message

`addReport(..., isSuccess=false)`:
1. Calls `report.addCaseFlowForError(...)` — marks row red in log
2. Calls `actions.captureScreenshot(ScreenshotStatus.FAILURE, failureMessage)` — screenshot named with FAILURE prefix
3. Sets `scenarioDetails.setSuccess(false)` — marks overall test as failed

### 27.5 Local vs production constructor branch (EntityCase constructor)

```java
// Local run (LocalSetupManager.isLocalSetup() == true):
failure = LocalFailureTemplates.getInstance();          // NO CommonObject
report  = AutomaterReport.getInstance(null);
actions = ClientFrameworkActions.getInstance(driver, failure);

// Production run:
CommonObject commonObject = new CommonObject(driver, failureMessage);
failure = commonObject.getFailure();
report  = AutomaterReport.getInstance(commonObject.getReport());
actions = ClientFrameworkActions.getInstance(commonObject.getDriver(), failure);
```

> **RULE**: Never call `new CommonObject(...)` or access `CommonVariables` in code that
> must also run locally. Always check `LocalSetupManager.isLocalSetup()` first.

---

## SECTION 28 — preProcess PATTERNS (from scenario analysis, Mar 2026)

### 28.1 Use `switch(group)` for preProcess with 4+ groups

`if/else‑if` chains become hard to read beyond 3 branches. `RequestApprovalsBase.java` shows
the preferred `switch` pattern:

```java
@Override
protected boolean preProcess(String group, String[] dataIds) {
    try {
        switch(group) {
            case "IncidentRequest":
                RequestAPIUtil.createIncidentRequest(dataIds[0]);
                break;
            case "IncidentRequestWithApproval":
                RequestAPIUtil.createIncidentRequest();
                RequestApprovalsAPIUtils.submitForApprovalAPI(LocalStorage.getAsString("request"), dataIds[0]);
                break;
            // ...
        }
        return true;
    } catch(Exception exception) {
        return false;
    }
}
```

> ⚠️ The `catch` block must call `addFailureReport(...)` for visibility — returning `false`
> silently is acceptable but then the test is skipped with NO failure row in the report.

### 28.2 Prefer `addFailureReport` inside preProcess catch (not silent `return false`)

```java
// ✅ BETTER — failure visible in ScenarioReport:
} catch(Exception exception) {
    report.addCaseFlow("Exception occurred while pre processing: " + exception);
    addFailureReport("Pre-process failed", exception.getMessage());
    return false;
}

// ❌ SILENT — test is skipped; no error in report, impossible to debug remotely:
} catch(Exception exception) {
    return false;
}
```

### 28.3 postProcess can use method name pattern to conditionally clean up

```java
@Override
protected void postProcess(String method) {
    try {
        if(method.contains("Notification")) {
            NotificationRulesAPIUtil.uncheckNotificationRuleAPI();
        }
    } catch(Exception exception) {
        // cleanup failure — intentionally suppressed
    }
}
```

The `method` parameter is the **Java method name** of the test that just ran.
Use `contains()` or `startsWith()` for partial matching.

### 28.4 NoPreprocess equivalent — just `return true` unconditionally

```java
@Override
protected boolean preProcess(String arg0, String[] arg1) {
    return true;   // equivalent to group="NoPreprocess" — no API setup needed
}
```

This is valid. `NotificationsRulesBase` uses this pattern — the `group` parameter is
ignored entirely and the method always returns `true`.

---

## SECTION 29 — ANNOTATION TYPES: @AutomaterScenario vs @AutomaterCase (Mar 2026)

### 29.1 `@AutomaterScenario` — independent, self-contained test

- Placed on methods in `<Entity>.java` (the thin wrapper class)
- Each method maps to ONE test case in the Aalam runner
- Takes NO method parameters — data comes from `dataIds[]` + LocalStorage
- Has all 9 annotation fields: `id`, `group`, `priority`, `dataIds`, `tags`, `description`, `owner`, `runType`, `switchOn`
- **Called directly by framework via reflection** (no parameter injection)

### 29.2 `@AutomaterCase` — reusable parameterized sub-action

- Placed on helper methods in `*Base.java`
- Takes explicit Java parameters (e.g. `TestCaseData testCaseData, String submit`)
- Called from `@AutomaterScenario` methods or from other base methods
- Has only `description` field — no `id`, `group`, `priority`, `owner`
- The `MaintenanceBase.fillModuleTemplate(TestCaseData, String)` pattern is a good example

```java
// @AutomaterCase — parameterized helper called from test body or other scenarios
@AutomaterCase(description = "Fill the module creation form")
public void fillModuleTemplate(TestCaseData testCaseData, String submit) {
    JSONObject inputData = getTestCaseData(testCaseData);
    actions.formBuilder.fillInputForAnEntity(...);
    if(submit != null) {
        actions.click(MaintenanceLocators.Form.MODULE_FORM_SUBMIT_BUTTON.apply(submit));
    }
}
```

---

## SECTION 30 — REPORT WRAPPING PATTERN (Mar 2026)

### 30.1 Always wrap test body in `startMethodFlowInStepsToReproduce` / `endMethodFlowInStepsToReproduce`

```java
public void myTestMethod() throws Exception {
    report.startMethodFlowInStepsToReproduce(AutomaterVariables.CASE_START.apply(getMethodName()));
    try {
        // ... test logic ...
        addSuccessReport("My assertion message");
    } catch(Exception exception) {
        addFailureReport("Internal error occurred: " + getMethodName(), exception.getMessage());
    } finally {
        report.endMethodFlowInStepsToReproduce();
    }
}
```

> `CASE_START` / `SCENARIO_START` produces a formatted label. `getMethodName()` reads from
> the stack trace (2 levels up) — always call it at the FIRST line before any other method calls.

### 30.2 `getMethodName()` must be called at the OUTERMOST stack frame of the method

`EntityCase.getMethodName()` reads `Thread.currentThread().getStackTrace()[2]` — exactly
2 levels above its own frame. Call it as the FIRST thing in the test body before any delegation.

```java
// ✅ CORRECT
public void createSomething() {
    String methodName = getMethodName();  // first
    report.startMethodFlowInStepsToReproduce(AutomaterVariables.CASE_START.apply(methodName));
    // ...
}

// ❌ WRONG — calling getMethodName() inside a utility will return wrong frame
SomeUtil.doStuff(getMethodName());   // BAD if called nested
```
```
---

## SECTION 31 — SKELETON SCAFFOLDING & ENTITY FILE STRUCTURE (Mar 2026)
# Source: GenerateSkeletonForAnEntity.java + base/skeleton/ templates + esmdirectory live example

### 31.1 What the skeleton generates (required reading before creating a new entity)

`GenerateSkeletonForAnEntity.java` generates a full entity scaffold by setting two PascalCase
constants and running `main()`. It creates exactly these files:

```
modules/<module_lower>/                         ← Module root
  <MODULE_NAME>Entities.java                    ← Entity name string constants
  <MODULE_NAME>Role.java                        ← Role constants (extends Role)
  <entity_nounderscore>/                        ← Entity package (snake → no underscores)
    <ENTITY_NAME>.java                          ← Parent class (extends Entity, @AutomaterSuite)
    common/
      <ENTITY_NAME>Constants.java               ← Action/tab string constants
      <ENTITY_NAME>DataConstants.java           ← TestCaseData key constants
      <ENTITY_NAME>Fields.java                  ← FieldDetails map entries
      <ENTITY_NAME>Locators.java                ← XPath/By locator constants

resources/entity/conf/<module_lower>/
  <entity_snake>.json                           ← Field config (from entity_skeleton.json)

resources/entity/data/<module_lower>/<entity_snake>/
  <entity_snake>_data.json                      ← Test input data (empty initially)

resources/entity/roles/
  <module_lower>.json                           ← Role definitions (empty initially)
```

### 31.2 Naming derivations (how names are computed)

| Input | Conversion | Use |
|---|---|---|
| `MODULE_NAME = "Changes"` | `.toLowerCase()` → `"changes"` | Folder path |
| `ENTITY_NAME = "ChangeWorkflow"` | `UPPER_CAMEL → LOWER_UNDERSCORE` → `"change_workflow"` | Snake-case name, conf/data filenames |
| `ENTITY_NAME = "ChangeWorkflow"` | snake without underscores → `"changeworkflow"` | Java package folder name |
| `ENTITY_NAME.toUpperCase()` | `"CHANGEWORKFLOW"` (no underscore) | Constant name in Entities file — **known quirk** |

> ⚠️ **Quirk**: `ENTITY_NAME.toUpperCase()` is a raw string uppercase — it does NOT insert underscores.
> `"ChangeWorkflow"` → `"CHANGEWORKFLOW"` in `<MODULE_NAME>Entities.java`, not `"CHANGE_WORKFLOW"`.

### 31.3 Files the skeleton does NOT generate (must be added manually)

| File | Pattern | Purpose |
|------|---------|---------|
| `<ENTITY_NAME>Base.java` | `modules/<m>/<e>/<EntityNameBase.java>` | Implementation class (if parent/Base split is used) |
| `<ENTITY_NAME>AnnotationConstants.java` | `common/` | `@AutomaterScenario dataIds` constants |
| `utils/<ENTITY_NAME>ActionsUtil.java` | `utils/` | Reusable UI interaction helpers |
| `utils/<ENTITY_NAME>APIUtil.java` | `utils/` | Reusable REST API helpers |

> **Simple modules** (e.g., `esmdirectory`) skip the parent/Base split entirely — all `@AutomaterScenario`
> methods live directly in `<ENTITY_NAME>.java`. Only complex modules need a `Base` class.
> Some simple modules also place `ApiUtil` in `common/` instead of `utils/`.

### 31.4 `<ENTITY_NAME>.java` (parent class) — skeleton-generated structure

```java
@AutomaterSuite(
    role  = ModulesRoleSkeleton.SDADMIN,  // replaced with module-specific Role after setup
    owner = ""
)
public class ChangeWorkflow extends Entity {

    public ChangeWorkflow(WebDriver driver, StringBuffer failureMessage) {
        super(driver, failureMessage);
    }

    @Override
    protected String getEntityConfigurationName() {
        return "change_workflow";        // snake_case entity name — used to load conf JSON
    }

    @Override
    protected void assignPermission(String role) throws Exception {
        super.assignPermission(role);
    }

    @Override
    protected boolean preProcess(String group, String[] dataIds) {
        return false;                    // must be implemented — skeleton is a stub
    }

    @Override
    protected void postProcess(String group) {
                                         // must be implemented for cleanup
    }
}
```

### 31.5 `<ENTITY_NAME>Constants.java` — skeleton inner-class structure

The skeleton always generates these 4 inner classes (all `public final class`, NOT static):
```java
public final class ChangeConstants {
    public final class ListviewGlobalActions    { }   // e.g. "New Change", "Export"
    public final class ListviewLocalActions     { }   // e.g. "Edit", "Delete" (row actions)
    public final class DetailsPageGlobalActions { }   // e.g. "Add Task", "Approve"
    public final class DetailsPageTabs          { }   // e.g. "Notes", "Associations"
}
```

### 31.6 `<ENTITY_NAME>Locators.java` — skeleton Listview stub

```java
public final class ChangeLocators {
    public final class Listview { }   // populated manually with XPath/By locators
    // Additional groupings added manually: DetailView, Form, AssociationsTab, etc.
}
```

### 31.7 `entity_skeleton.json` — initial conf file template

```json
{
  "name":                "<entity_snake>",
  "plural_name":         "",            ← must fill (e.g. "changes")
  "module":              "<module>",
  "api_path":            "",            ← must fill (e.g. "changes")
  "is_client_framework": true,
  "field_details": [
    { "name": "id", "field_type": "input", "data_path": "id", "is_custom": true }
  ]
}
```
Fill `plural_name` and `api_path` before writing any tests. Add field_details for each UI field.

### 31.8 `<MODULE_NAME>Entities.java` — entity name registry

Used to look up entity string keys for API calls and navigation:
```java
public final class ChangesEntities {
    public final static String CHANGE          = "change";
    public final static String CHANGEWORKFLOW  = "change_workflow";  // ← no underscore in key name
}
```
`appendEntityNameInModulesFile()` auto-appends the new constant when skeleton is run.

### 31.9 `<MODULE_NAME>Role.java` — module role constants

```java
public final class ChangesRole extends Role {
    // Module-specific role constants added manually
    // E.g.: public final static String FULL_CONTROL = "Full Control";
}
```
Used in `@AutomaterSuite(role = ChangesRole.FULL_CONTROL)`.

---

## SECTION 32 — AUTO-GENERATED CONSTANT FILES (AutoGenerateConstantFiles.java, Mar 2026)
# Source: AutoGenerateConstantFiles.java (full read)
# Trigger: run `main()` after modifying any file under resources/entity/

### 32.1 What triggers what

| Modified resource file location | Generated/updated Java file |
|---|---|
| `resources/entity/conf/<module>/<entity>.json` | `<Entity>Fields.java` — fully regenerated |
| `resources/entity/data/<module>/<entity>/<entity>_data.json` | `<Entity>DataConstants.java` — inner class appended or replaced |
| `resources/entity/roles/<module>.json` | `<Module>Role.java` — fully regenerated |

The tool finds the **most recently modified** file under `resources/entity/` and dispatches.
Only one file is processed per run. Edit one file at a time, then run.

### 32.2 DataConstants inner class naming rule (CRITICAL)

The inner class name inside `*DataConstants.java` is derived from the **data filename** (not
the entity name) via `getPascalValue()` = `LOWER_UNDERSCORE → UPPER_CAMEL`:

```
change_workflow_data.json  →  inner class ChangeWorkflowData
solution_data.json         →  inner class SolutionData
request_data.json          →  inner class RequestData
```

**Inner class structure written:**
```java
public final static class ChangeWorkflowData {
    public final static String PATH = "data" + File.separator + "changes"
        + File.separator + "change_workflow" + File.separator + "change_workflow_data.json";

    public final static TestCaseData MY_TEST_KEY = new TestCaseData("my_test_key", PATH);
    // one constant per top-level key in the JSON
}
```

### 32.3 DataConstants constant naming rule

```java
// JSON key               → Java constant name
"my_test_key"             → MY_TEST_KEY              // .toUpperCase() only — underscores come from snake_case
"createChange"            → CREATECHANGE             // camelCase key loses word boundary — prefer snake_case keys!
```

**Rule**: Always use `snake_case` keys in `*_data.json` so the generated constant is readable.

### 32.4 DataConstants is idempotent — safe to re-run

- If the inner class block already exists: it is **replaced** (split on `innerClassName + " {"`)
- If it is new: it is **appended** before the last `}` of the outer class
- Running multiple times on the same file does not create duplicate inner classes

### 32.5 FieldDetails constructor — 6-parameter form (REQUIRED)

Generated by `generateEntityFiles()`:
```java
// With field_type:
public final static FieldDetails FIELD_NAME = new FieldDetails(
    "field_name",        // display/field name
    "api.path.to.value", // data_path from conf JSON
    "api_key",           // data_key from conf JSON (separate field from data_path)
    FieldType.SELECT,    // FieldType enum — uppercase of field_type string
    false,               // isCustom
    false                // isUDF
);

// Without field_type (null in conf):
public final static FieldDetails FIELD_NAME = new FieldDetails(
    "field_name", "api.path", "api_key", null, false, false
);
```

> ⚠️ **`FieldDetails` takes 6 parameters**, not 4. Missing `isUDF` = compile error.

### 32.6 FieldDetails constant naming rule

```java
fieldName.replace("-", "_").replace(" ", "_").toUpperCase()
// "my-field"   → MY_FIELD
// "my field"   → MY_FIELD
// "my_field"   → MY_FIELD
```

### 32.7 FieldType enum values (from conf → generated code)

`field_type` string in conf JSON → `FieldType.<CONST>` in generated Java:

**Handled by `fillInputForAnEntity` switch statement:**
```
"input"           → FieldType.INPUT
"select"          → FieldType.SELECT
"multiselect"     → FieldType.MULTISELECT
"html"            → FieldType.HTML
"date"            → FieldType.DATE
"datetime"        → FieldType.DATETIME
"textarea"        → FieldType.TEXTAREA
"criteria"        → FieldType.CRITERIA
"pickList"        → FieldType.PICKLIST        (⚠️ camelCase value — not "picklist")
"attachment"      → FieldType.ATTACHMENT
```

**NOT handled by `fillInputForAnEntity` (no switch case — silently skipped):**
```
"checkbox"        → FieldType.CHECKBOX        (click manually via locator)
"radio"           → FieldType.RADIO            (click manually via locator)
"selectonly"      → FieldType.SELECTONLY
"selectaction"    → FieldType.SELECTACTION
"mappedfield"     → FieldType.MAPPEDFIELD
"systemSelect"    → FieldType.SYSTEMSELECT    (⚠️ camelCase value)
"selectRelationship" → FieldType.SELECTRELATIONSHIP  (⚠️ camelCase value)
"ipaddress"       → FieldType.IPADDRESS
```

```
""  / null    → null  (no FieldType argument)
```

> ⚠️ The 3 camelCase values (`"pickList"`, `"systemSelect"`, `"selectRelationship"`) must be used **exactly as-is** in conf JSON. Using all-lowercase will cause the switch to fall through silently.

### 32.8 Role constants naming rule

JSON key → constant name: `roleDetail.toUpperCase()` (no other transformation).
`"Full Control"` → `FULL CONTROL` (with space — **invalid Java identifier**).
**Rule**: Role JSON keys must use only alphanumeric + underscore. Use `"full_control"` not `"Full Control"`.

### 32.9 Workflow to add a new test data entry (complete steps)

1. Add the new key-value entry to `<entity>_data.json` (use snake_case key)
2. Run `AutoGenerateConstantFiles.main()` (or equivalent — it finds the most recently modified file)
3. The corresponding `TestCaseData` constant is auto-appended to `<Entity>DataConstants.<InnerClass>`
4. Reference in test: `<Entity>DataConstants.<InnerClass>.MY_NEW_KEY`
5. Reference in `@AutomaterScenario(dataIds = {<Entity>AnnotationConstants.Data.MY_KEY})` — this is a DIFFERENT constants class used only for preProcess dataIds

---

## SECTION 33 — ROLE SYSTEM: createUserByRole, Role JSON, SDADMIN semantics (Mar 2026)

### 33.1 createUserByRole — full internal flow

Called from `Entity.assignPermission()` in the **admin session**, before any `switchToUserSession()`:

```
assignPermission(roleId)
  └── createUserByRole("TECHNICIAN", moduleName, roleId, scenarioUser)
        ├── getRoleDetails(moduleName, roleId)         // reads general.json first, module.json as fallback
        ├── getUserId(scenarioUser)                    // searches users API by email → sets entityId on User
        ├── if entityId != null → handleExistingUserRole()
        │     ├── is_technician=true  → updateTechnician() if role mismatch, else store entityId in LocalStorage
        │     └── is_technician=false → createRequester()
        └── if entityId == null → handleNewUserRole()
              ├── is_technician=true  → createTechnician()
              └── is_technician=false → createRequester()
```

`createTechnician()` also calls `checkCustomRole()` and `checkProjectRole()` — both create the custom/project role via UI if it doesn't exist in SDP yet.

### 33.2 getRoleDetails() lookup order

1. Reads `resources/entity/roles/general.json` (always first)
   - Contains: `sdadmin`, `sdsite_admin`, `sdguest`, `helpdeskconfig`
2. If the roleId is NOT found in general.json, reads `resources/entity/roles/<moduleName>.json`
   - If same key in both, **general.json wins** (first match returns)

Implication: if you define a custom role with the same key name as a general role, the general one silently overrides it. Use unique keys per module.

### 33.3 Role JSON structure — complete reference

```json
// Technician with custom SDP role (most common):
"Solution_FullControl": {
  "user": {
    "roles": [{"name": "Solution_FullControl"}],
    "default_project_role": {"name": "Project Admin"},
    "purchase_order_approver": "true",
    "approval_limit": "-1"
  },
  "custom_roles": {
    "Solution_FullControl": {
      "permissions": [
        {"name": "ViewSolutions"},
        {"name": "CreateSolutions"},
        {"name": "ModifySolutions"},
        {"name": "DeleteSolutions"},
        {"name": "SolutionsApprove"}
      ],
      "description": "Technician with full permissions"
    }
  },
  "is_technician": true
}

// Requester (no custom_roles, no roles[]):
"Solution_Requester": {
  "user": {
    "description": "Requester with same department",
    "login_user": true,
    "requester_allowed_to_view": "own_requests",
    "purchase_order_approver": true,
    "approval_limit": -1,
    "service_request_approver": true
  },
  "is_technician": false
}
```

**Fields**:
- `is_technician: true` → `createTechnician()` path; `false` → `createRequester()` path
- `custom_roles.<name>.permissions` → framework auto-creates this custom role in SDP if absent
- `roles[].name` → the built-in SDP role to assign (SDAdmin, HelpdeskConfig, etc.)
- Requester entries: `login_user: true` required for portal login

### 33.4 SDADMIN = no session split (CRITICAL)

When `@AutomaterSuite(role = Role.SDADMIN)` and scenario user email = admin email:
- `initializeAdminSession()` → browser logged in as admin
- `preProcess()` runs in admin session ✅
- `switchToUserSession()` → calls `LoginUtil.login(this, scenarioUser)` which logs in as the same admin account again
- Test method runs in **admin session** too ✅

**Consequence**: API calls inside the test method body are **safe** when `role = Role.SDADMIN` — unlike non-admin roles where test method body runs in restricted user session.

**Consequence**: `NoPreprocess` + `Role.SDADMIN` = the simplest possible scenario: no API setup, no session switch, test method runs as admin. Use this combination for admin-only UI tests that need no prerequisite data.

### 33.5 SDADMIN vs module-specific roles — when to use each

| Role | When to use |
|------|------------|
| `Role.SDADMIN` | Testing admin-only features; no need to validate permission boundaries |
| `SolutionsRole.SOLUTION_FULLCONTROL` | Testing that a technician WITH a specific role can perform an action |
| `SolutionsRole.SOLUTION_VIEWONLY` | Testing that view-only users CANNOT perform certain actions |
| `SolutionsRole.SOLUTION_REQUESTER` | Testing requester portal experience |
