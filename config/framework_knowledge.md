# AutomaterSelenium Framework — Complete Knowledge Base
# Learned from: Solution.java, SolutionBase.java, solution_data.json,
#               SolutionDataConstants.java, SolutionAnnotationConstants.java,
#               SolutionFields.java, SolutionLocators.java, SolutionConstants.java
#               Entity.java, FieldDetails.java, FormBuilder.java, FieldType.java,
#               ClientFrameworkActions.java, Navigate.java, ListView.java,
#               DetailsView.java, SolutionActionsUtil.java, SolutionAPIUtil.java

---

## 1. COMPLETE CODE / TEST FLOW (END TO END)

```
Runner invokes @AutomaterScenario method on <Entity>.java
  │
  ├─ Reads:  id, group, priority, dataIds[], tags, description, owner, runType
  │
  ├─► Entity.run()
  │     ├─ initializeAdminSession()
  │     ├─ loadProperties()  (loads entity conf JSON → sets fields[], module name, etc.)
  │     ├─ assignPermission(role)
  │     ├─ preProcess(group, dataIds[])   ←── REST API test data setup
  │     │     uses dataIds[0], dataIds[1] etc. as keys into DataConstants → JSON file
  │     │     stores created IDs into LocalStorage for the UI test to retrieve
  │     ├─ <scenario method body runs>    ←── actual UI test
  │     └─ postProcess(methodName)        ←── cleanup (usually empty override)
  │
  └─ Report is written throughout
```

---

## 2. TWO-LAYER CLASS ARCHITECTURE

```
Entity  (framework base class)
  └── <Entity>Base extends Entity          ← ALL IMPLEMENTATION here
        └── <Entity> extends <Entity>Base  ← ONLY @AutomaterScenario annotations here
```

**Examples from codebase:**
- `SolutionBase extends Entity` → `Solution extends SolutionBase`
- `ProblemCommonBase extends Entity` → `Problem extends ProblemCommonBase`
- `RequestCommonBase extends Entity` → `Request extends RequestCommonBase`

Both classes carry `@AutomaterSuite(role, tags, owner)` at class level.

---

## 3. FILE STRUCTURE PER ENTITY (5 files)

```
modules/<module>/<entity>/
├── <Entity>.java                    ← annotation wrapper (extends <Entity>Base)
├── <Entity>Base.java                ← implementation (extends Entity)
└── common/
    ├── <Entity>Fields.java          ← FieldDetails constants  (name, dataPath, FieldType)
    ├── <Entity>DataConstants.java   ← TestCaseData constants  (key → JSON file path)
    ├── <Entity>AnnotationConstants.java ← Group/Data string constants
    ├── <Entity>Constants.java       ← UI string constants (LISTVIEW, button labels, tabs)
    └── <Entity>Locators.java        ← Locator objects wrapping By.xpath / By.id / By.cssSelector
```

```
resources/entity/
├── conf/<module>/<entity>.json      ← entity config: fields, field_types, data_paths
└── data/<module>/<entity>/<entity>_data.json  ← test data payloads
```

---

## 4. ANNOTATION WRAPPER — `<Entity>.java` PATTERN

```java
@AutomaterSuite(
    role  = Role.SDADMIN,
    tags  = "SOLUTION TESTING",
    owner = OwnerConstants.RAJESHWARAN_A
)
public class Solution extends SolutionBase {

    public Solution(WebDriver driver, StringBuffer failureMessage) {
        super(driver, failureMessage);
    }

    @Override
    protected String getEntityConfigurationName() { return "solution"; }

    @Override
    protected void assignPermission(String role) throws Exception {
        super.assignPermission(role);
    }

    // EVERY scenario follows this exact pattern:
    @Override
    @AutomaterScenario(
        id          = "SDPOD_AUTO_SOL_CREATE_001",   // ← REQUIRED — next sequential number
        group       = "",                             // ← "" when no preProcess setup needed
        priority    = Priority.HIGH,
        dataIds     = {},                             // ← {} when group=""
        tags        = {},
        owner       = OwnerConstants.RAJESHWARAN_A,
        runType     = ScenarioRunType.USER_BASED,
        description = "Creating Unapproved Private solution using general template"
    )
    public void createUnapprovedPrivateSolutionGT() {
        super.createUnapprovedPrivateSolutionGT();  // ← ONLY THIS. No logic here.
    }

    @Override
    protected void postProcess(String method) {}
}
```

**MANDATORY rules for wrapper:**
- `@Override` AND `@AutomaterScenario` together on every scenario
- Body contains ONLY `super.methodName();` — zero logic
- `@Override protected void postProcess(String method) {}` at end of class

---

## 5. IMPLEMENTATION — `<Entity>Base.java` PATTERN

```java
public void createUnapprovedPrivateSolutionGT() {
    // ① ALWAYS FIRST LINE — no exceptions
    report.startMethodFlowInStepsToReproduce(AutomaterVariables.SCENARIO_START.apply(getMethodName()));

    try {
        // ② Optionally mark a flow step
        report.addCaseFlow("Starting solution creation");

        // ③ Load UI test data from DataConstants → JSON
        JSONObject inputData = getTestCaseData(SolutionDataConstants.SolutionData.SOL_UNAPPROVED_PRIVATE_GENERAL_TEMPLATE);

        // ④ Navigate
        actions.navigate.toModule(getModuleName());
        actions.setTableView(SolutionConstants.LISTVIEW);

        // ⑤ Open creation form
        actions.navigate.toGlobalActionInListview(SolutionConstants.ListviewGlobalActions.NEW_SOLUTION);

        // ⑥ Fill form using framework
        actions.formBuilder.fillInputForAnEntity(isClientFramework(), fields, inputData);

        // ⑦ Custom clicks (approve/unapprove, public/private)
        actions.click(SolutionLocators.SolutionCreateForm.SOLUTION_ADD);   // or SOLUTION_ADD_APPROVE

        // ⑧ Assert
        String text = AutomaterUtil.getValueAsStringFromInputUsingAPIPath(
            inputData, SolutionFields.TITLE.getDataPath());
        Boolean isEqual = actions.validate.textContent(
            ClientFrameworkLocators.DetailsViewLocators.MODULE_TITLE, text);

        if (isEqual) {
            addSuccessReport("Solution create verified for " + getRole()
                + " role using " + AutomaterUtil.getCurrentUserId() + " user");
        } else {
            addFailureReport("Solution creation failed", "Title is not same as given input");
        }

    } catch (Exception exception) {
        addFailureReport("Internal error occurred while running the test case " + getMethodName(),
            exception.getMessage());
    } finally {
        report.endMethodFlowInStepsToReproduce();   // ← ALWAYS in finally
    }
}
```

---

## 6. preProcess() PATTERN — GROUP → API SETUP MAPPING

```java
@Override
protected boolean preProcess(String group, String[] dataIds) {
    report.addCaseFlow("Populate data");
    try {
        if ("create".equalsIgnoreCase(group)) {
            // Creates solution via REST API, stores ID in LocalStorage.store(getName(), id)
            createSolution(dataIds[0]);

        } else if ("createAndGetDisplayID".equalsIgnoreCase(group)) {
            // Creates + stores display_id AND id
            JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[0]);
            JSONObject response = restAPI.createAndGetResponse(getName(), getModuleName(), getInputData(inputData));
            LocalStorage.store("display_id", AutomaterUtil.getValueAsStringFromInputUsingAPIPath(response, "display_id.display_value"));
            LocalStorage.store(getName(), AutomaterUtil.getValueAsStringFromInputUsingAPIPath(response, "id"));

        } else if ("create_topic".equalsIgnoreCase(group)) {
            // Creates a topic, stores topic ID in LocalStorage.store("topic", id)
            JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[0]);
            String topicId = SolutionAPIUtil.createSolutionTopicAndGetName("topics", inputData);
            LocalStorage.store("topic", topicId);

        } else if (SolutionAnnotationConstants.Group.CUST_SOL_TEMPLATE_GRP.equalsIgnoreCase(group)) {
            // = "create_cust_sol_temp" — creates solution template
            createSolutionTemplate(dataIds[0]);

        } else if (SolutionAnnotationConstants.Group.CREATE_CUST_TEMP_TOPIC.equalsIgnoreCase(group)) {
            // = "create_cust_temp_topic" — creates template (dataIds[0]) + topic (dataIds[1])
            createSolutionTemplate(dataIds[0]);
            JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[1]);
            String topicId = SolutionAPIUtil.createSolutionTopicAndGetName("topics", inputData);
            LocalStorage.store("topic", topicId);

        } else if ("createMultipleSolution".equalsIgnoreCase(group)) {
            // Creates N solutions, stores list in LocalStorage.store("solutions", list)
            // N comes from solution_count field in the data
        }
    } catch (Exception exception) {
        return false;
    }
    report.addCaseFlow("Data populated");
    return true;
}
```

**Critical rule:** group="" means no preProcess setup. dataIds={} when group="".
**When group is non-empty:** dataIds must reference string constants from `SolutionAnnotationConstants.Data`.

### ⭐ Group Reuse — read preProcess() body before writing new code

If an existing group already creates the entity you need and stores the IDs in LocalStorage:
- **Reuse that group** in your `@AutomaterScenario` — zero new `preProcess()` code needed.
- Read the `LocalStorage` keys set by the existing group in your test method body.

```java
// "create" group already does: createChange(dataIds[0])
//   → LocalStorage.store(getName(), changeId)
//   → LocalStorage.store("changeName", name)

// New scenario just reuses "create" and reads from LocalStorage:
@AutomaterScenario(group = "create", dataIds = {ChangeAnnotationConstants.Data.CREATE_CHANGE_API}, ...)
public void myNewTest() throws Exception {
    String id   = getEntityId();                       // works because "create" stored it
    String name = LocalStorage.fetch("changeName");   // works because "create" stored it
}
// ❌ WRONG: adding a new else-if to preProcess() for "createForMyTest" when "create" already covers it
```

---

## 7. DATA LAYER — 3 LEVELS

### Level 1: AnnotationConstants.java — string keys used in `dataIds[]`
```java
public interface SolutionAnnotationConstants {
    interface Group {
        String CREATE                   = "create";
        String CREATE_CUST_TEMP_TOPIC   = "create_cust_temp_topic";
        String CUST_SOL_TEMPLATE_GRP    = "create_cust_sol_temp";
        String CREATE_MULTIPLE_SOLUTION = "createMultipleSolution";
    }
    interface Data {
        String CREATE_PUBLIC_APP_SOL_API   = "create_pub_sol_API";
        String CREATE_PRIV_SOL_API         = "create_priv_sol_API";
        String CREATE_PUBLIC_UNAPP_SOL_API = "create_pub_unapp_sol_API";
        String CREATE_PRIV_UNAPP_SOL_API   = "create_priv_unapp_sol_API";
        String CUST_SOL_TEMPLATE           = "cust_sol_template";
        String SOL_NEW_TOPIC               = "sol_new_topic";
        // ...and more
    }
}
```

### Level 2: DataConstants.java — maps Java constant → TestCaseData(jsonKey, PATH)
```java
public final static TestCaseData SOL_UNAPPROVED_PRIVATE_GENERAL_TEMPLATE =
    new TestCaseData("sol_unapproved_private_general_template", PATH);
// PATH = "data/solutions/solution/solution_data.json"
```

### Level 3: solution_data.json — actual payload
```json
"sol_unapproved_private_general_template": {
    "data": {
        "title": "New UnApproved Private Solution_$(unique_string)",
        "template": {"name": "General Solution Template"},
        "topic":    {"name": "General"},
        "description": "Description_$(unique_string)"
    }
}
```

**API pre-setup data (used in preProcess via dataIds):**
```json
"create_priv_unapp_sol_API": {
    "data": {
        "template":        {"name": "General Solution Template"},
        "topic":           {"id": "$(custom_general_topic)"},
        "is_public":       false,
        "title":           "Private Solution created during Preprocess_$(unique_string)",
        "approval_status": {"name": "UnApproved"}
    }
}
```

### Runtime placeholders in JSON:
| Placeholder | Resolved to |
|---|---|
| `$(unique_string)` | Millisecond timestamp — unique per run |
| `$(custom_KEY)` | `LocalStorage.fetch("KEY")` — set by preProcess OR pre-seeded before `getTestCaseData()` |
| `$(user_name)` | Scenario user’s display name |
| `$(user_email_id)` | Scenario user’s email |
| `$(admin_email_id)` | Admin user’s email |
| `$(date, N, ahead)` | Date N days ahead (milliseconds string) |
| `$(datetime, N, ahead)` | Datetime N days ahead |

### ⭐ LocalStorage pre-seed — reuse existing JSON entries with custom values (REQUIRED TECHNIQUE)

`$(custom_KEY)` is resolved by `PlaceholderUtil` at the moment `getTestCaseData()` / `getTestCaseDataUsingCaseId()` is called.
This means: if you call `LocalStorage.store("KEY", value)` **before** `getTestCaseData()`, the placeholder will resolve to that value.

This allows reusing an existing `*_data.json` entry with a custom runtime value **without creating a new JSON entry**.

```java
// Example: Existing JSON entry has "template": {"name": "$(custom_template_name)"}
// You want to use a template that was created in preProcess.

// ❌ WRONG — creating a duplicate JSON entry:
// "create_solution_with_my_template": { "data": { "template": {"name": "My Template"} } }

// ✅ CORRECT — pre-seed LocalStorage before calling getTestCaseData():
// preProcess already stored: LocalStorage.store("solution_template", "My Template");
// Then in the test method:
JSONObject inputData = getTestCaseData(SolutionDataConstants.SolutionData.SOL_WITH_CUSTOM_TEMPLATE);
// $(custom_solution_template) resolves to "My Template" from LocalStorage
```

**When to pre-seed vs. when to create a new entry:**
- `$(custom_KEY)` placeholder exists in JSON and you have the value → `LocalStorage.store("KEY", value)` then reuse
- Entry has fixed values and all match your test → reuse as-is
- Genuinely different field combination with no matching entry → create new entry
| Placeholder | Resolved to |
|---|---|
| `$(unique_string)` | Auto unique string per run |
| `$(custom_topic)` | Topic ID stored in `LocalStorage` by `preProcess` |
| `$(custom_general_topic)` | General topic ID fetched in preProcess |
| `$(custom_solution_template)` | Template name stored in `LocalStorage` by `preProcess` |

---

## 8. FormBuilder — Complete Internal Analysis

### Call chain
```
actions.formBuilder.fillInputForAnEntity(isClientFramework(), fields, inputData)
    ↓
  for each fieldKey in fields.keySet():
      fillInputForField(fieldDetails, inputData)
          ↓ if fieldDetails.isCustom()
              fillInputForCustomField()  ← no-op default; subclass overrides if needed
          ↓ else
              fillInputForFieldInClientFW(fieldDetails, inputData)
                  ↓ switch(fieldDetails.getFieldType()):
```

### FieldType → Method mapping (complete)

| `field_type` in conf JSON | FieldType constant | Method called | What it does |
|---|---|---|---|
| `"input"` | `FieldType.INPUT` | `fillTextField(name, value)` | `actions.type(FORM_ELEMENT("input", name), value)` |
| `"select"` | `FieldType.SELECT` | `fillSelectField(name, value)` | Clicks dropdown → types in search input → clicks option |
| `"multiselect"` | `FieldType.MULTISELECT` | `fillMultiSelectField(...)` | Iterates JSON array, selects each value |
| `"html"` | `FieldType.HTML` | `fillHTMLField(name, value)` | Switches to iframe (ZE editor) → types |
| `"date"` | `FieldType.DATE` | `fillDateField(name, Long.valueOf(value))` | Calendar picker, no time |
| `"datetime"` | `FieldType.DATETIME` | `fillDateTimeField(name, Long.valueOf(value))` | Calendar + time picker |
| `"textarea"` | `FieldType.TEXTAREA` | `fillTextAreaField(name, value)` | `actions.type(FORM_ELEMENT("textarea", name), value)` |
| `"criteria"` | `FieldType.CRITERIA` | `fillCriteria(JSONArray)` | Complex filter row builder |
| `"pickList"` | `FieldType.PICKLIST` | `fillSelectField(name, value)` | Same as select |
| `"attachment"` | `FieldType.ATTACHMENT` | `actions.uploadFile(value)` | File upload (form/rhs/locator variants) |
| `is_custom: true` | — | `fillInputForCustomField()` | No-op by default; entity subclass overrides |

All other FieldType constants (`checkbox`, `radio`, `selectonly`, `selectaction`, `mappedfield`,
`systemSelect`, `selectRelationship`, `ipaddress`) exist but have no `switch` case in `fillInputForFieldInClientFW` (they fall to `default: break`).

### How value is extracted from JSON data
```java
// path = fieldDetails.getDataPath() from conf JSON
String value = AutomaterUtil.getValueAsStringFromInputUsingAPIPath(inputData, path);
// If value == null → field is SKIPPED (not filled). No error.
```
So JSON test data only needs to include fields that should actually be filled. Absent fields are silently skipped.

### Date/Datetime filling — TWO modes

**Mode A — value in JSON data** (auto-handled by `fillInputForAnEntity`):
```json
// In solution_data.json — rare, value must be a Long timestamp string
"expiry_date": { "value": "1740000000000" }
```
`fillInputForAnEntity` reads it via `data_path = "expiry_date.value"` and calls `fillDateTimeField(name, Long.valueOf(value))` automatically.

**Mode B — value computed at runtime** (needs explicit call AFTER `fillInputForAnEntity`):
```java
// This is the common pattern in SolutionBase — date NOT in JSON, computed dynamically
actions.formBuilder.fillInputForAnEntity(isClientFramework(), fields, inputData);
actions.formBuilder.fillDateField(SolutionConstants.REVIEW_DATE, PlaceholderUtil.getDateInMilliSeconds(2, 2, 1, true));
actions.formBuilder.fillDateField(SolutionConstants.EXPIRY_DATE, PlaceholderUtil.getDateInMilliSeconds(10, 2, 1, true));
```
`PlaceholderUtil.getDateInMilliSeconds(daysOffset, monthsOffset, yearsOffset, future)` returns a Long.

### submit() variants
```java
actions.formBuilder.submit();               // tries FORM_SAVE then FORM_SUBMIT locator
actions.formBuilder.submit("Save");         // clicks specific named button
// For solution-specific buttons, use actions.click(SolutionLocators.SolutionCreateForm.SOLUTION_ADD)
// or actions.click(SolutionLocators.SolutionCreateForm.SOLUTION_ADD_APPROVE)
```

### solution.json — field_type routing per field

| field name | field_type | data_path | How filled |
|---|---|---|---|
| `id` | `is_custom: true` | `id` | `fillInputForCustomField()` — no-op |
| `template` | `select` | `template.name` | Click dropdown → search → click option |
| `title` | `input` | `title` | `actions.type(input[name=title], value)` |
| `keywords` | `input` | `keywords` | `actions.type(input[name=keywords], value)` |
| `description` | `html` | `description` | Switch to ZE iframe → type |
| `is_public` | `input` | `is_public` | `actions.type(input[name=is_public], value)` |
| `topic` | `select` | `topic.name` | Click dropdown → search → click option |
| `operation_comment` | `input` | `operation_comment` | `actions.type(input[name=operation_comment], value)` |
| `expiry_date` | `datetime` | `expiry_date.value` | fillDateTimeField (if value in JSON) |
| `review_date` | `datetime` | `review_date.value` | fillDateTimeField (if value in JSON) |
| `solution_count` | `is_custom: true` | `solution_count` | `fillInputForCustomField()` — no-op |

### Key rules derived from FormBuilder analysis
1. `fillInputForAnEntity` iterates ALL fields from conf JSON. Fields absent in test data JSON → silently skipped.
2. `html` field type (description) switches to iframe — framework handles this, no special code needed.
3. `select` type uses type-and-search pattern — the dropdown must be searchable; value must match exactly.
4. Date/datetime in JSON: `data_path` must point to a numeric timestamp string (Long).
5. Date/datetime computed at runtime: call `fillDateField(name, Long)` or `fillDateTimeField(name, Long)` AFTER `fillInputForAnEntity`.
6. `is_custom: true` fields in conf JSON are ignored by default — entity subclass can override `fillInputForCustomField()`.
7. `submit()` is NOT used in SolutionBase — solution uses entity-specific `actions.click(SolutionLocators.SOLUTION_ADD)` instead.

---

## 9. TEST ID FORMAT

```
SDPOD_AUTO_<MODULE>_<AREA>_NNN

MODULE codes: SOL=Solution, PB=Problem, IR=IncidentRequest, CHG=Change, REQ=Request
AREA codes:   CREATE=Create, LV=ListView, DV=DetailView, EDIT=Edit
NNN:          Zero-padded 3-digit sequential number

Examples: SDPOD_AUTO_SOL_CREATE_059
          SDPOD_AUTO_PB_LV_023
          SDPOD_AUTO_CHG_DV_012
```

**NEVER use `SDP_` prefix.**
Always check last existing ID in the file to get next NNN.

---

## 10. KEY API METHODS IN IMPLEMENTATION METHODS

```java
// Navigation
actions.navigate.toModule(getModuleName());
actions.setTableView(SolutionConstants.LISTVIEW);
actions.navigate.toGlobalActionInListview(SolutionConstants.ListviewGlobalActions.NEW_SOLUTION);
actions.navigate.toDetailsPageUsingRecordId(getEntityId());
actions.navigate.toSubTabInDetailsPage(SolutionConstants.DetailsPageTabs.TAB_NAME);

// Form interaction
actions.formBuilder.fillInputForAnEntity(isClientFramework(), fields, inputData);
actions.formBuilder.fillInputForField(field, value);
actions.formBuilder.fillDateField(SolutionConstants.REVIEW_DATE, PlaceholderUtil.getDateInMilliSeconds(2, 2, 1, true));
actions.formBuilder.submit();
actions.click(SolutionLocators.SolutionCreateForm.SOLUTION_ADD);
actions.click(SolutionLocators.SolutionCreateForm.SOLUTION_ADD_APPROVE);
actions.type(SolutionLocators.Section.LOCATOR, value);

// List view operations
actions.listView.columnSearch("Column", value);                       // search by column display name + value
actions.listView.selectFilter(filterName, tableViewName);              // filterName + tableView (e.g. SolutionConstants.LISTVIEW)
actions.listView.rowAction(entityID, actionName);                      // row-level action by entity ID
actions.listView.getFieldValueFromFirstRow(field);                     // field = internal name
actions.listView.getFieldValueFromRow(field, "1");                     // 1-based row number as String
actions.listView.getRecordsInPage();                                   // int count
actions.listView.addCustomFilter(filterName, criteriaJSONArray);       // create custom view filter
actions.listView.setTableSettings(inputData, datapath);                // set sort/density/count
actions.listView.sortByColumn(colName, ascending);                     // ascending=true/false
actions.listView.columnChooser(column, enable);                        // enable/disable single column

// Validation
Boolean ok = actions.validate.textContent(Locator, expectedText);
Boolean ok = actions.validate.successMessageInAlert(SolutionConstants.Alerts.ADDED);

// Data extraction
String value = AutomaterUtil.getValueAsStringFromInputUsingAPIPath(inputData, SolutionFields.TITLE.getDataPath());
String id = LocalStorage.fetch("solution");  // fetch stored preProcess ID
String role = getRole();
String user = AutomaterUtil.getCurrentUserId();

// Report
report.addCaseFlow("Step description");
report.addCaseFlowForDebug("Debug info");
addSuccessReport("message");
addFailureReport("what failed", "why / actual value");
```

---

## 11. COMPLETE STRICT RULES FOR CODE GENERATION

1. **Two-piece output always:** wrapper in `<Entity>.java` + implementation in `<Entity>Base.java`
2. **ID format:** `SDPOD_AUTO_<MODULE>_<AREA>_NNN` — check existing file for last number
3. **@Override + super.method()** — both mandatory in annotation wrapper, NOTHING ELSE
4. **report.startMethodFlowInStepsToReproduce(AutomaterVariables.SCENARIO_START.apply(getMethodName()))** — FIRST line of implementation, NO other form
5. **report.endMethodFlowInStepsToReproduce()** — must be in `finally` block
6. **Both addSuccessReport AND addFailureReport** — both required in if/else
7. **group must exist in preProcess()** — never invent new group strings
8. **dataIds values** — must match string constants in `<Entity>AnnotationConstants.Data`
9. **Data loaded in impl** — use `getTestCaseData(DataConstants.EntityData.CONSTANT)` for UI data
10. **Data loaded in preProcess** — use `getTestCaseDataUsingCaseId(dataIds[0])` for API data
11. **No invented constants** — all Locators, Fields, Constants must exist in their respective files
12. **No hardcoded XPath/CSS/IDs** — always use Locators.java constants
13. **No System.out.println** — use `report.addCaseFlow()`
14. **LocalStorage.store(key, value)** in preProcess → **LocalStorage.fetch(key)** in implementation
15. **Datetime fields** set separately via `actions.formBuilder.fillDateField()`, not via `fillInputForAnEntity()`
16. **`actions.listView.doAction()` does NOT exist** — use `actions.listView.rowAction(entityID, actionName)` instead
17. **`actions.listView.selectRecord()` does NOT exist** — navigate via `actions.navigate.toDetailsPageUsingRecordId(id)` instead
18. **`getEntityId()`** = `LocalStorage.getAsString(getName())` — only valid AFTER preProcess stores the ID
19. **`cleanUpData()`** is automatic — REST creates via `DataUtil` auto-deleted after test
20. **`getInputData(JSONObject)`** wraps data in `{"solution": {...}}` — use for `restAPI.create()` in preProcess

````

---

## 12. Entity.java — BASE CLASS LIFECYCLE

```
run(ScenarioDetails)
  ├─ loadProperties()          → reads entity conf JSON → sets fields[], module, api path
  ├─ initializeAdminSession()  → LoginUtil.login(admin)
  ├─ assignPermission(roleId)  → createUserByRole(TECHNICIAN, moduleName, roleId, scenarioUser)
  ├─ preProcess(group, dataIds[]) → REST API setup, abstract, must return true to proceed
  ├─ process(method)           → invokes the @AutomaterScenario method body
  ├─ postProcess(group)        → abstract, override in Base (usually empty)
  └─ cleanUpData()             → auto-deletes all DataUtil.getInstance().cleanUpCalls entries
```

### Key protected methods available in `<Entity>Base.java`

```java
// Data retrieval
protected final JSONObject getTestCaseData(TestCaseData td)           // UI test data
protected final JSONObject getTestCaseDataUsingCaseId(String caseId)  // by raw case ID string
protected final JSONObject getTestCaseDataForRestAPI(TestCaseData td) // strips custom fields
protected final JSONObject getInputData(JSONObject data)              // wraps in {entityName: data}

// Entity state
protected final String getEntityId()   // = LocalStorage.getAsString(getName()) — set by preProcess
protected final String getRole()       // from @AutomaterSuite(role=...)
protected String getModuleName()       // e.g. "solutions"
protected String getName()             // e.g. "solution"

// Session
public void switchToUserSession()   // switches browser to the test user
public void switchToAdminSession()  // switches browser back to admin
```

---

## 13. FieldDetails.java — FIELD DESCRIPTOR

```java
// Constructor (6-arg form used in SolutionFields.java):
new FieldDetails(String name, String dataPath, String dataKey, String fieldType, boolean isCustom, boolean isUDF)

fd.getName()                    // "title", "template", etc.
fd.getFieldType()               // FieldType.INPUT, FieldType.SELECT, etc.
fd.getDataPath()                // "title", "template.name", "expiry_date.value"
fd.isCustom()                   // true → no-op (skipped by FormBuilder)
fd.getLocatorByName(String n)   // get associated Locator
```

---

## 14. Navigate.java — COMPLETE METHOD REFERENCE

Access via: `actions.navigate`

```java
Navigate to(Locator locator)                             // click + waitForAjaxCompleteLoad
Navigate toAdmin()                                       // admin header link
Navigate toModule(String moduleName)                     // module tab (handles More overflow)
Navigate toGlobalActionInListview(String actionName)     // global action button (toolbar) in listview
Navigate toLocalActionInListview(String actionName)      // row-level action in listview
Navigate toDetailsPageUsingRecordId(String id)           // click record row by entity ID
Navigate toDetailsPageUsingRecordIndex(String index)     // click row by "1"-based index
Navigate toGlobalActionInDetailsPage(String actionName)  // global action in details page
Navigate toLeftTabWithNoChildren(String tabName)         // left nav tab (no children)
Navigate toLeftSubTabWithChildren(String tabName)        // left nav subtab (with parent)
Navigate toSubTabInDetailsPage(String tabName)           // top subtabs (handles More)
```

### Chaining (all methods return `this`):
```java
actions.navigate.toModule(getModuleName())
                .toGlobalActionInListview(SolutionConstants.ListviewGlobalActions.NEW_SOLUTION);
```

---

## 15. ListView.java — COMPLETE METHOD REFERENCE

Access via: `actions.listView`

```java
// Filtering
void    selectFilter(String filterName, String tableViewName)   // tableViewName can be null
void    clickFilterDropDown()                                   // opens the filter dropdown
void    addCustomFilter(String filterName, JSONArray criteria)  // create custom view filter

// Searching / data reading
void    columnSearch(String column, String value)               // column = display name
int     getRecordsInPage()
String  getFieldValueFromFirstRow(String field)                 // field = internal name
String  getFieldValueFromRow(String field, String row)          // row = "1"-based String
String  getEntityIDFromListviewResponse(String entityPath, String identifier, String identifierFieldName)

// Row actions
void    rowAction(String entityID, String action)               // row three-dot menu action
void    clickSpotEditField(String recordID, String field)       // inline edit in list view

// Bulk actions
void    selectCheckBoxInListViewPage(String row)                // select one row checkbox ("1"-based)
void    selectAllCheckBoxesInListviewPage()                     // select all rows
void    clearAllCheckBoxInListviewPage()                        // deselect all rows
void    clickBulkActionButton(String buttonName)               // click bulk action in toolbar
boolean checkBulkActionsActionName(String actionName)          // check if bulk action exists

// Table settings
void    setTableSettings(JSONObject inputData, String datapath)
void    sortByColumn(String colName, boolean ascending)
void    tableSettings(JSONObject inputData, String datapath)   // alias for setTableSettings
void    columnChooser(String column, boolean enable)
void    columnChooserInTableSettings(String tableDivName, String column, boolean enable)
boolean isColumnSelected(String column)
```

---

## 16. DetailsView.java — COMPLETE METHOD REFERENCE

Access via: `actions.detailsView`

```java
void    clickSubTab(String subTabName)
void    clickFromActions(String actionName)                 // Actions dropdown → action
boolean verifyFieldInDetailsPage(String field, String value)
String  getFieldValueFromDetailsPage(String field)
String  getValueFromRhsDetails(String fieldName)
void    clickRhsDetails(String fieldName)
void    verifyRecentHistoryDescription(String description)
boolean verifyTitleInDetailsPage(String expectedString)
String  getTitle()
// ⚠️ MODULE_TITLE GOTCHA: ClientFrameworkLocators.DetailsViewLocators.MODULE_TITLE
// resolves to //div[@id='details-middle-container']/descendant::h1
// The h1 text INCLUDES the display ID prefix (e.g. "SOL-8 MyTitle", "CHG-42 MyTitle").
// actions.validate.textContent(MODULE_TITLE, "MyTitle") will FAIL because of the prefix.
// ALWAYS use verifyTitleInDetailsPage("MyTitle") — it does a contains/suffix match
// and handles the display ID prefix correctly.

// Spot edit methods:
void spotEditFieldUsingSearch(String field, String value)
void spotEditTypeField(String field, String value)
void spotEditPickList(String field, String value)
void spotEditFieldWithoutSearch(String field, String value)
void spotEditDependentField(String field, String value)
void spotEditMultiSelectField(String field, String value)
void clickSpotEditField(String field)
void clickSpotEditFieldWithInternalName(String field)
```

---

## 17. SolutionFields.java — COMPLETE CONSTANT REFERENCE

```java
// isCustom=true → SKIPPED by fillInputForAnEntity (no-op)
SolutionFields.ID                 // ("id",               "id",                INPUT,    custom=true)
SolutionFields.TEMPLATE           // ("template",         "template.name",     SELECT,   custom=false)
SolutionFields.TITLE              // ("title",            "title",             INPUT,    custom=false)
SolutionFields.KEYWORDS           // ("keywords",         "keywords",          INPUT,    custom=false)
SolutionFields.DESCRIPTION        // ("description",      "description",       HTML,     custom=false)
SolutionFields.IS_PUBLIC          // ("is_public",        "is_public",         INPUT,    custom=false)
SolutionFields.TOPIC              // ("topic",            "topic.name",        SELECT,   custom=false)
SolutionFields.OPERATION_COMMENT  // ("operation_comment","operation_comment", INPUT,    custom=false)
SolutionFields.EXPIRY_DATE        // ("expiry_date",      "expiry_date.value", DATETIME, custom=false)
SolutionFields.REVIEW_DATE        // ("review_date",      "review_date.value", DATETIME, custom=false)
SolutionFields.SOLUTION_COUNT     // ("solution_count",   "solution_count",    null,     custom=true)
```

---

## 18. SolutionLocators.java — COMPLETE REFERENCE

### SolutionLocators.SolutionListview
```java
SOL_NEW_TOPIC, SOL_NEW_TOPIC_NAME, SOL_NEW_TOPIC_SAVE, TOPIC_MOVE_SAVE
SOL_APPROVE_COMMENTS                   // id="operation_comment"
SUBMIT_APPROVAL_POPUP                  // id="toEmailSearch"
APP_ACTIONS_APPROVE, APP_ACTIONS_REJECT
CLICK_ROW_ACTIONS_WITH_ENTITYID.apply(entityId)
ACTIONS_LIST.apply(action)
SELECT_SOL_CHECKBOX_WITH_ENTITYID.apply(entityId)
```

### SolutionLocators.SolutionCreateForm
```java
SOLUTION_IS_PUBLIC, SOLUTION_KEYWORD
SOLUTION_ADD             // unapproved → "Add" button
SOLUTION_ADD_APPROVE     // approved → "Add And Approve" button
SOLUTION_SAVE            // edit → "Save" button
SOLUTION_SAVE_APPROVE    // edit → "Save and Approve" button
SOLUTION_ALL_USERGROUPS  // All users radio button
```

### SolutionLocators.SolutionDetailView
```java
DETAIL_VIEW_EDIT_BUTTON, DETAIL_VIEW_DELETE_BUTTON, DETAIL_VIEW_FORWARD_BUTTON
DETAIL_VIEW_ACTIONS                    // id="quickaction"
DETAIL_VIEW_ACTIONS_APP_SOL            // Actions → Approve
SOL_LIKE_BUTTON, SOL_DISLIKE_BUTTON, SOL_LIKE_COUNT, SOL_DISLIKE_COUNT
SOL_LIKED_TEXT, SOL_DISLIKED_TEXT
SOLUTION_COMMENTS_TAB, SOLUTION_HISTORY_TAB
SOLUTION_COMMENTS_TEXT_FIELD, SOLUTION_COMMENTS_SAVE
ATTACH_SOLUTION, DETACH_SOLUTION, LINK_SOLUTION
VERIFY_COMMENT_VALUE.apply(val), VERIFY_KEYWORD_VALUE.apply(val)
VERIFY_DESCRIPTION_CONTENT.apply(val), VERIFY_TOPIC_VALUE.apply(val)
VERIFY_IF_PUBLIC.apply(val), VERIFY_HISTORY_COMMENT.apply(val)
```

---

## 19. CRITICAL RULE — ActionUtils / ActionsUtil

**Before writing ANY test scenario, ALWAYS analyze the entity's `*ActionsUtil.java` and `*APIUtil.java` files first — then reuse existing methods or create missing ones before generating the test method.**

### Rule 0 — Pre-generation analysis workflow (REQUIRED — 4 steps, run first)

> This must run BEFORE any test method code is written. It is not optional.

```
STEP 1: READ the entity's util files
  - Find: modules/<module>/<entity>/utils/<Entity>ActionsUtil.java
  - Find: modules/<module>/<entity>/utils/<Entity>APIUtil.java
  - List ALL public static methods with signatures and purpose
  - If a file doesn't exist yet → it must be created before generating scenarios

STEP 2: Map each operation in the new scenario to a method
  For every navigation / click / form / popup step in the scenario:
    - REUSE: an existing util method covers it → call it
    - CREATE NEW: no method covers it → it goes to Step 3

STEP 3: Create missing util methods FIRST (before writing the test method)
  For each CREATE NEW operation:
    - Add public static method to <Entity>ActionsUtil.java (UI) or <Entity>APIUtil.java (API)
    - Granularity: one complete named UI operation (not a single click)
    - Compile the util file to verify before proceeding

STEP 4: Generate the scenario using only util calls + assertions
  - Test method body = utility calls + assertions + addSuccessReport/addFailureReport ONLY
  - If typing actions.click() directly in a test method body → STOP → move to util first
```

### Rule 1 — Check before writing (REQUIRED, applies to ALL entities)

```
BEFORE writing any navigation/click/form/popup code in a test method:
  1. grep -rn "public static" modules/<module>/<entity>/utils/*ActionsUtil.java
  2. If a matching method exists → CALL IT, do NOT re-inline the logic
  3. If it does NOT exist → ADD the static method to *ActionsUtil.java first, then call it
```

### Rule 2 — Where code lives (REQUIRED)

| Logic type | Where it lives | Example |
|---|---|---|
| Multi-step UI flow (tab click, popup open, search, select, confirm) | `*ActionsUtil.java` as `public static` method | `ChangeActionsUtil.linkParentChangeViaUI(name, id)` |
| REST API helper (create/update/delete/link via API) used in preProcess | `*APIUtil.java` as `public static` method | `ChangeAPIUtil.linkChildChanges(parentId, childId1)` |
| Test assertion / report call | STAYS in test method body | `addSuccessReport("SDPOD_...")` |

### Rule 3 — Class declaration (REQUIRED pattern — no exceptions)

```java
// ✅ CORRECT — every ActionsUtil class in the codebase follows this exact shape
public final class ChangeActionsUtil extends Utilities {
    // ALL methods: public static
    // extends Utilities → gives access to static fields: actions, report, restAPI
    
    public static void openAssociationTab() throws Exception {
        actions.click(ChangeLocators.LinkingChange.LHS_ASSOCIATION_TAB);
        actions.waitForAjaxComplete();
    }
}

// ❌ WRONG — non-static, not extending Utilities, not final
public class ChangeActionsUtil {
    public void openAssociationTab() { ... }  // cannot access actions/report/restAPI
}
```

### Rule 4 — Method granularity (REQUIRED)

Each method = **one complete named UI operation** (what a manual tester calls one step).

| Too granular ❌ | Correct granularity ✅ |
|---|---|
| `clickAttachDropdown()` | `openAttachParentChangePopup()` — click dropdown + click option + waitForAjax |
| `clickYesOnDialog()` | `detachParentChange()` — click detach + confirm dialog + click YES + waitForAjax |
| 6-line open+search+select+associate block | `linkParentChangeViaUI(name, id)` — all 6 lines |

### Rule 5 — Test method body rules (REQUIRED)

```java
// ✅ CORRECT — test method only contains: utility calls + assertions + report calls
public void verifySingleParentConstraint() throws Exception {
    ChangeActionsUtil.openAssociationTab();
    ChangeActionsUtil.linkParentChangeViaUI(
        LocalStorage.getAsString("targetChangeName1"), LocalStorage.getAsString("targetChangeId1")
    );
    if(actions.isElementPresent(ChangeLocators.LinkingChange.DETACH_PARENT_CHANGE)) {
        addSuccessReport("SDPOD_LINKING_CH_022: Detach button visible after parent linked");
    }
}

// ❌ WRONG — duplicate click/wait blocks inlined in test body
public void verifySingleParentConstraint() throws Exception {
    actions.click(ChangeLocators.LinkingChange.LHS_ASSOCIATION_TAB);  // should be utility call
    actions.waitForAjaxComplete();
    actions.click(ChangeLocators.LinkingChange.ATTACH_BUTTON_DROPDOWN);
    actions.click(ChangeLocators.LinkingChange.ATTACH_PARENT_CHANGE_OPTION);
    actions.waitForAjaxComplete();
    // ...
}
```

### Known entity utility files (run discovery — do NOT rely on this table alone)

> **Every module has a `utils/` folder.** The table below is a reference sample.
> Always run the discovery command for the entity you are working on:

```bash
find src/com/zoho/automater/selenium/modules/<module>/<entity>/utils/ -name "*.java" | sort
```

| Module | Entity | ActionsUtil file | APIUtil file |
|--------|--------|-----------------|-------------|
| changes | change | `changes/change/utils/ChangeActionsUtil.java` | `changes/change/utils/ChangeAPIUtil.java` |
| changes | downtime | `changes/downtime/utils/DowntimeActionsUtil.java` | `changes/downtime/utils/DowntimeAPIUtil.java` |
| solutions | solution | `solutions/solution/utils/SolutionActionsUtil.java` | `solutions/solution/utils/SolutionAPIUtil.java` |
| requests | request | `requests/request/utils/RequestAPIUtil.java` | — |
| problems | problem | `problems/problem/utils/ProblemActionsUtil.java` | `problems/problem/utils/ProblemAPIUtil.java` |
| releases | release | `releases/release/utils/ReleaseActionsUtil.java` | `releases/release/utils/ReleaseAPIUtil.java` |
| projects | project | `projects/project/utils/ProjectActionsUtil.java` | `projects/project/utils/ProjectAPIUtil.java` |
| assets | asset | `assets/asset/utils/AssetActionsUtil.java` | `assets/asset/utils/AssetAPIUtil.java` |
| general | dashboard | `general/dashboard/utils/DashboardActionsUtil.java` | `general/dashboard/utils/DashboardAPIUtil.java` |
| maintenance | — | `maintenance/utils/MaintenanceActionsUtil.java` | `maintenance/utils/MaintenanceAPIUtil.java` |
| contracts | contract | `contracts/contract/utils/ContractActionsUtil.java` | `contracts/contract/utils/ContractAPIUtil.java` |
| admin | — | `admin/utils/AdminActionsUtil.java` | `admin/utils/AdminAPIUtil.java` |

> If the entity is not listed, run the discovery command — it will have util files.

---

## 20. SolutionActionsUtil.java — COMPLETE METHOD REFERENCE

```java
// Instance method (needs SolutionActionsUtil instance):
void addValueToEditor(String message)           // types into ZE HTML editor iframe

// Static methods (call as SolutionActionsUtil.method(...)):
static void   pressEscapeKey()                  // Robot-based Escape key press
static void   uploadFile(String fileName)       // attaches a file in the detail view
static void   searchSolutionUsingId(String entityID)  // fetches title via API, does columnSearch("Title", title)
static void   selectFilter(String filterName)   // selects filter if not already selected
static void   pageSetup()                       // setTableView(LISTVIEW) + selectFilter(ALL_ACTIVE_SOLUTIONS_FILTER)
static void   navigateToSolutions(String entityID)  // toModule("solutions") + pageSetup() + optionally selects checkbox
static Boolean verifyAttachment(String fileName)    // clicks attachment count, verifies file name
```

### Key usage patterns
```java
// Standard navigation to solutions list view:
SolutionActionsUtil.pageSetup();   // or navigateToSolutions(null) for full navigation

// Navigate to solutions and navigate to specific record's details page:
actions.navigate.toModule(getModuleName());
SolutionActionsUtil.pageSetup();
actions.navigate.toDetailsPageUsingRecordId(getEntityId());

// Search for a specific solution in list view:
SolutionActionsUtil.searchSolutionUsingId(getEntityId());

// Upload attachment:
SolutionActionsUtil.uploadFile(SolutionConstants.Attachments.ATTACHMENT_PNG);

// Verify attachment:
Boolean attached = SolutionActionsUtil.verifyAttachment(SolutionConstants.Attachments.ATTACHMENT_PNG);
```

---

## 20b. ChangeActionsUtil.java — COMPLETE METHOD REFERENCE

All methods are `public static`. Class: `public final class ChangeActionsUtil extends Utilities`.

```java
// ---- General navigation (pre-existing methods) ----
static void gotoChangeDetailsPage(String changeId)   // navigate to module → setTableView → columnSearch → toDetailsPage

// ---- File / worklog / approval (pre-existing methods) ----
static void uploadFileInChange(String fileName)
static void addWorklog(JSONObject data)
static void approveChange(String changeId)

// ---- CH-286: Linking Changes UI utilities (added Mar 2026) ----
// Search inside association-dialog-popup (NOT slide-down-popup — uses custom locators)
static void columnSearchInAssociationPopup(String column, String value) throws Exception
// → clicks POPUP_SEARCH_ICON if visible → finds column index via table headers → types in column search input

// Navigate to the LHS Association tab
static void openAssociationTab() throws Exception
// → click LHS_ASSOCIATION_TAB + waitForAjaxComplete

// Open Attach dropdown → click "Attach Parent Change" option
static void openAttachParentChangePopup() throws Exception
// → click ATTACH_BUTTON_DROPDOWN + click ATTACH_PARENT_CHANGE_OPTION + waitForAjaxComplete

// Open Attach dropdown → click "Attach Child Changes" option
static void openAttachChildChangesPopup() throws Exception
// → click ATTACH_BUTTON_DROPDOWN + click ATTACH_CHILD_CHANGES_OPTION + waitForAjaxComplete

// Search for a change by title + click its radio button + click BTN_ASSOCIATE
static void selectAndAssociateParentInPopup(String changeName, String changeId) throws Exception

// Search for a change by title + click its checkbox + click BTN_ASSOCIATE
static void selectAndAssociateChildInPopup(String changeName, String changeId) throws Exception

// Combined: openAttachParentChangePopup + selectAndAssociateParentInPopup
static void linkParentChangeViaUI(String changeName, String changeId) throws Exception

// Combined: openAttachChildChangesPopup + selectAndAssociateChildInPopup
static void linkChildChangeViaUI(String changeName, String changeId) throws Exception

// Click DETACH_PARENT_CHANGE + confirm dialog ("Confirm"/DETACH_CHANGE) + YES + waitForAjaxComplete
static void detachParentChange() throws Exception

// Click SELECT_CHILD_CHECKBOX(id) + DETACH_CHILD_CHANGES + confirm + YES + waitForAjaxComplete
static void detachChildChange(String childChangeId) throws Exception
```

### When to call which method

```java
// Full attach flow (most common — one line in test method):
ChangeActionsUtil.openAssociationTab();
ChangeActionsUtil.linkParentChangeViaUI(LocalStorage.getAsString("targetChangeName1"),
                                        LocalStorage.getAsString("targetChangeId1"));

// When you need to open popup but do custom search/selection before associating:
ChangeActionsUtil.openAssociationTab();
ChangeActionsUtil.openAttachParentChangePopup();
ChangeActionsUtil.columnSearchInAssociationPopup("Title", changeName);
actions.waitForAjaxComplete();
actions.click(ChangeLocators.LinkingChangePopup.SELECT_RADIO_WITH_ENTITYID.apply(changeId));
// ... verify something ...
actions.click(ChangeLocators.LinkingChangePopup.BTN_ASSOCIATE);

// Full detach flows:
ChangeActionsUtil.detachParentChange();                         // parent detach
ChangeActionsUtil.detachChildChange(changeId);                  // single child detach
```

⚠️ **Do NOT inline LHS_ASSOCIATION_TAB click + ATTACH_BUTTON_DROPDOWN + ATTACH_PARENT_CHANGE_OPTION directly in test methods.** These 3 lines = `openAssociationTab()` + `openAttachParentChangePopup()`.

---

## 21. SolutionAPIUtil.java — COMPLETE METHOD REFERENCE

```java
// Both methods are static:
static String createSolutionTopicAndGetName(String apiPath, JSONObject inputData)
    // POST to apiPath, returns topic name
    // apiPath = "topics"
    // Used in preProcess for group="create_topic"

static String createSolutionTemplateAndGetName(String apiPath, JSONObject inputData)
    // POST to apiPath, stores name in LocalStorage.store("solution_template_name", name), returns name
    // apiPath = "solution_templates"
    // Used in preProcess for group="create_cust_sol_temp"
```

---

## 21b. Validator.java — COMPLETE METHOD REFERENCE

Access via: `actions.validate`

```java
// Text match
Boolean textContent(Locator locator, String content)                        // trims + compares element text

// Notification banners
void    successMessageInAlert(String message)                               // assert success banner
void    successMessageInAlertAndClose(String message)                       // assert + close success banner
void    errorMessageInAlert(String message)                                 // assert error banner
void    errorMessageInAlertAndClose(String message)                         // assert + close error banner
void    verifyMessageInAlert(Boolean isSuccess, String message)             // isSuccess=true→success
void    verifyMessageInAlertAndClose(Boolean isSuccess, String message)     // same + close
boolean isSuccessNotification(String notificationClass)                     // low-level class check

// Assertion helpers
void    customAssert(String expected, String got)                           // throws on mismatch
void    customAssert(Boolean expected, Boolean got)                         // boolean assertion
void    confirmationBoxTitleAndConfirmationText(String title, String text)   // dialog verification

// Date validation
Boolean validateDate(Locator locator, Long value)                           // verify date display
Boolean validateDateTime(Locator locator, Long value, boolean isTimeField)  // verify datetime display

// Form validation
void    validateFormFieldValues(Map<String,FieldDetails> fields, JSONObject inputData)  // bulk verify
```

---

## 21c. WindowManager — COMPLETE METHOD REFERENCE

Access via: `actions.windowManager`

```java
// Open new context (tab/window)
String switchToNewTab(int timeoutSeconds)          // waits, switches to new tab, returns handle
String switchToNewWindow(int timeoutSeconds)       // alias
String switchToNewBrowserContext(int timeoutSec)   // generic alias

// Return to origin
void returnToOriginalTab()
void returnToOriginalWindow()   // alias

// Switch by index (0-based) / title / URL
void switchToTabByIndex(int index)
void switchToTabByTitle(String title)    // partial title match
void switchToTabByUrl(String url)        // partial URL match
void switchToWindowByIndex(int index)   // aliases
void switchToWindowByTitle(String title)
void switchToWindowByUrl(String url)

// Close
void closeTabByIndex(int index)
void closeAllTabsExceptOriginal()
void closeWindowByIndex(int index)          // aliases
void closeAllWindowsExceptOriginal()
```

**Pattern**:
```java
actions.click(SomeLocators.LINK_WITH_NEW_TAB);
actions.windowManager.switchToNewTab(10);
// ... assertions in new tab ...
actions.windowManager.returnToOriginalTab();
```

---

## 21d. RandomUtil — COMPLETE METHOD REFERENCE

```java
// Random alphabetic string
String RandomUtil.generateRandomString(int length)
String RandomUtil.generateRandomString(int length, String prefix)

// Case variants
String RandomUtil.generateRandomLowercaseString(int length)
String RandomUtil.generateRandomUppercaseString(int length, String prefix)

// Alphanumeric
String RandomUtil.generateRandomAlphaNumericString(int length)
String RandomUtil.generateRandomAlphaNumericString(int length, String prefix)

// Random pick
String RandomUtil.randomChoice(String[] options)
    // e.g. RandomUtil.randomChoice(new String[]{"High","Medium","Low"})
```

> Use `$(unique_string)` in JSON test data. Use `RandomUtil` in Java code when you need a runtime-generated unique value.

---

## 21e. SDPCloudActions methods (available on `actions` directly)

```java
// Buttons
void    actions.clickByName(String buttonName)        // clicks button[name=buttonName]
void    actions.clickByNameInput(String buttonName)   // clicks input[name=buttonName]
void    actions.clickByNameSubmit(String buttonName)  // clicks submit[name=buttonName]
void    actions.clickByNameSpan(String buttonName)    // clicks span with name

// Table view
void    actions.setTableView(String viewName)         // e.g. "listview", "templateview"

// File upload
void    actions.uploadFile(String fileName)           // uploads file in active form
void    actions.uploadFileInRHS(String fileName)      // uploads in RHS panel
void    actions.uploadFile(Locator locator, String fileName)

// Misc
void    actions.pressEscapeKey()                      // Robot-based ESC key
String  actions.getLoggedInUser()                     // display name of logged-in user
String  actions.getLoggedInUserMailId()               // email of logged-in user
boolean actions.isMSP()                               // true if MSP instance
Set<String> actions.jsonArrayToSet(JSONArray arr)     // convert JSONArray to Set<String>
void    actions.associateSiteToTech(String siteName)  // associate current user to site
```

---

## 22. SolutionConstants.java — COMPLETE REFERENCE

```java
// Top-level
SolutionConstants.LISTVIEW                        // "listview"
SolutionConstants.TEMPLATEVIEW                    // "templateview"
SolutionConstants.ID                              // "ID"
SolutionConstants.TITLE                           // "Title"
SolutionConstants.DISPLAY_STATUS                  // "Status"
SolutionConstants.REVIEW_DATE                     // "review_date"
SolutionConstants.EXPIRY_DATE                     // "expiry_date"
SolutionConstants.ALL_ACTIVE_SOLUTIONS_FILTER     // "All Active Solutions"

// SolutionConstants.Buttons
SolutionConstants.Buttons.OK
SolutionConstants.Buttons.CONFIRM
SolutionConstants.Buttons.ADD
SolutionConstants.Buttons.YES
SolutionConstants.Buttons.SAVE

// SolutionConstants.ListviewGlobalActions
SolutionConstants.ListviewGlobalActions.NEW_SOLUTION         // "New Solution"
SolutionConstants.ListviewGlobalActions.DELETE_SOLUTION      // "Delete"
SolutionConstants.ListviewGlobalActions.APPROVE_ACTIONS      // "Approve Actions"
SolutionConstants.ListviewGlobalActions.APPROVE_SOLUTIONS    // "Approve"
SolutionConstants.ListviewGlobalActions.REJECT_SOLUTIONS     // "Reject"
SolutionConstants.ListviewGlobalActions.MOVE_SOLUTION        // "Move"
SolutionConstants.ListviewGlobalActions.SOLUTION_ADD         // "Add"
SolutionConstants.ListviewGlobalActions.SOLUTION_ADD_APPROVE // "Add And Approve"
SolutionConstants.ListviewGlobalActions.EDIT_SOLUTION_LISTVIEW // "Edit"
SolutionConstants.ListviewGlobalActions.SUBMIT_FOR_APPROVAL_LV // "Submit for Approval"
SolutionConstants.ListviewGlobalActions.FWD_SOLUTION         // "Forward"

// SolutionConstants.AlertMessages
SolutionConstants.AlertMessages.SOLUTIONS_APPROVED_MSG       // "Solution(s) approved"
SolutionConstants.AlertMessages.SOLUTIONS_REJECTED_MSG       // "Solution(s) approval rejected"
SolutionConstants.AlertMessages.SOLUTIONS_MOVED_MSG          // "Solution(s) topic changed"
SolutionConstants.AlertMessages.SOLUTIONS_LINKED_MSG         // "Solution(s) Successfully Linked"
SolutionConstants.AlertMessages.SOLUTIONS_DETACH_MSG         // "Solution(s) Link Successfully Removed "
SolutionConstants.AlertMessages.SOLUTIONS_DELETED_MSG        // "Solution moved to trash"
SolutionConstants.AlertMessages.APPROVAL_MAIL_SENT           // "Approval Mail Sent"

// SolutionConstants.DetailsPageTabs
SolutionConstants.DetailsPageTabs.TASKS
SolutionConstants.DetailsPageTabs.ROLES
SolutionConstants.DetailsPageTabs.DETAILS
SolutionConstants.DetailsPageTabs.STATUS_COMMENTS

// SolutionConstants.Attachments
SolutionConstants.Attachments.ATTACHMENT_PNG                 // "AALAM.png"
```


---

## LEARNED PATTERNS (auto-generated by LearningAgent)

### Call Super Method
_Learned from: IncidentRequestNotes.createIncidentRequestAndAddNotes | Date: 2026-02-27_

This pattern involves calling a super class method to ensure that all necessary setup and validation are performed before executing additional steps in the test.

**Applies to:** Any test that extends a base class and needs to perform common actions defined in the superclass.

```java
public void createIncidentRequestAndAddNotes() {
	super.createIncidentRequestAndAddNotes();
}
```

### Call Super Method
_Learned from: IncidentRequestNotes.createIncidentRequestAndAddNotes | Date: 2026-02-27_

This pattern involves calling a super class method to ensure that all necessary setup and validation are performed before executing additional steps in the test.

**Applies to:** Any test that extends a base class and needs to perform common actions defined in the superclass.

```java
public void createIncidentRequestAndAddNotes() {
	super.createIncidentRequestAndAddNotes();
}
```

### Inherit and Extend Base Method
_Learned from: IncidentRequestNotes.createIncidentRequestAndAddNotes | Date: 2026-02-27_

Reuse existing test logic by inheriting from a base class method and extending it with additional functionality.

**Applies to:** Any scenario where tests need to perform common actions followed by specific steps.

```java
public void createIncidentRequestAndAddNotes() {
	super.createIncidentRequestAndAddNotes();
}
```
### IncidentRequestWorkflow.createWorkflowOfIncidentRequest
**Product Area**: Admin > Automation > Workflows > Incident Request
**Status (last run)**: FAILED ❌
**Complexity**: HIGH — multi-step, canvas drag-drop, polling, async node activation, 10-20 min typical runtime
**Preprocess Group**: `No preprocess`

**What it tests**:
End-to-end workflow creation via the Workflows canvas UI for Incident Requests. Creates a workflow with multiple node types: Notification, Field Update (impact/urgency/priority), Task, Wait-For, Fork, Join, and Approval. Then links the workflow to an Incident Template via API, creates an IR, navigates to the IR detail view, triggers each node by updating fields, and verifies: notification fired, field updates applied, tasks created, status → Closed, workflow marked complete. Finally, deletes and restores the workflow.

**Key framework methods**:
- `AdminActionsUtil.gotoentity('Workflows')          → navigates to Admin > Automation > Workflows listview`
- `WorkflowsActionsUtil.*                             → drags nodes onto canvas, connects them, configures each`
- `actions.navigate.toModule(ModuleConstants.REQUESTS) → switches to Requests module`
- `actions.navigate.toSubTabInDetailsPage()           → switches between tabs in IR details`
- `actions.formBuilder.fillSelectField()              → fills select dropdown (impact field)`
- `verifyWaitForNode()                                → polls until 'Wait For' node activates`
- `verifyNotification(title)                          → checks notification panel for expected subject`
- `verifyFieldUpdate(field, value)                    → reads field from detail view, compares to expected`
- `verifyTask(title, bool)                            → checks task created/completed in task panel`
- `verifyStatus('Closed')                             → reads status field on IR details`
- `verifyWorkflowComplete()                           → verifies workflow progress indicator shows 100%`
- `deleteAndRestoreWorkflow(name)                     → deletes then restores from recycle bin`
- `restAPI.getEntityIdUsingSearchCriteria()           → REST: searches workflow by name to get its ID`
- `IncidentTemplateAPIUtil.createIncidentTemplate()   → REST: creates incident template linked to workflow`
- `RequestAPIUtil.createIR()                          → REST: creates incident request using the template`

**Key locators**: `WorkflowsLocators.* (workflow canvas, node drag handles, connection arrows)`, `RequestLocators.Listview.PAGE_COUNT (pagination info)`, `SDPCommonLocators.ButtonLocators.BTN_BYNAME_SPAN.apply('New Incident')`
**Key data constants**: `WorkflowsDataConstants.WorkflowsData.CREATE_INCIDENT_REQUEST_WORKFLOW`, `IncidentTemplateDataConstants.IncidentTemplateData.REQUEST_TEMPLATE`, `RequestDataConstants.RequestData.CREATE_REQUEST_FOR_WORKFLOW`, `TimerDataConstants.TimerData.LIST_INFO_CRITERIA_NAME_SEARCH`
**Notes**: Thread.sleep(10000) used before priority node verification — timing-sensitive scenario

---

### AssetTrigger.checkAllAssetTriggerForAccesspoint
**Product Area**: Admin > Automation > Triggers > Asset Triggers
**Status (last run)**: FAILED ❌
**Complexity**: MEDIUM — preprocess API calls + UI create + trigger verification
**Preprocess Group**: `createAssetTrigger`

**What it tests**:
Verifies that an Asset Trigger (with Notification action) fires correctly when a new Access Point asset is created. preProcess (group='createAssetTrigger') creates:
  1. A Notification rule via API (TriggerAPIUtil.createNotificationViaAPI)
  2. A Trigger via REST API ('wftriggers') that fires on asset creation, criteria: created_by=technician
Then the test:
  1. Creates the Access Point product type via API if not exists (AssetAPIUtil.checkAndCreateProduct)
  2. Navigates to Assets listview
  3. Selects 'Access Point' product type from left accordion
  4. Clicks 'New Asset', fills form via fillInputForAnEntity and submits
  5. Calls verifyNotification() to confirm trigger fired

**Key framework methods**:
- `TriggerAPIUtil.getEntityIdforCriteriaValue()        → REST lookup of 'All Assets' product type ID`
- `TriggerAPIUtil.createNotificationViaAPI()           → REST POST to create notification rule`
- `restAPI.createAndGetAPIResponse('wftriggers', ...)  → REST POST to create trigger with criteria`
- `AssetAPIUtil.checkAndCreateProduct()                → REST: creates product type if not exists`
- `actions.navigate.toModule(ModuleConstants.ASSETS)   → navigates to Assets module`
- `AssetActionsUtil.searchAndSelectProductTypeInAccordian() → left sidebar product-type filter`
- `SDPCloudActions.isMSP()                             → checks if portal is MSP mode`
- `actions.click(AssetLocators.Listview.LISTVIEW_BUTTONS.apply('New Asset'))`
- `actions.formBuilder.fillInputForAnEntity()          → fills name, serial, type from asset_data.json`
- `formBuilder.submit()                                 → submits create form`
- `verifyNotification()                                 → checks notification bell / trigger audit`

**Key locators**: `AssetLocators.Listview.LISTVIEW_BUTTONS.apply(AssetConstants.ListviewGlobalActions.NEW_ASSET)`, `AdditionalFieldsLocators (used in MSP-mode customer selection)`, `TriggersLocators.Listview (for checking trigger status)`
**Key data constants**: `AssetDataConstants.AssetData.CREATE_ACCESS_POINT_ASSET`, `TriggersDataConstants.TriggersData.NOTIFICATION_DATA_FOR_TRIGGER_SUBENTITY`, `TriggersDataConstants.TriggersData.CUSTOM_DATA_FOR_TRIGGER_SUBENTITY_WITH_NOTIFICATION_ACTIONS_ONLY`
**Notes**: LocalStorage keys: 'technician', 'triggerName', 'triggerId', 'entityId', 'moduleName', 'criteriaCondition', 'criteriaField', 'criteriaValue'

---


### Framework-Level Test Setup and Validation
_Learned from: ProjectUDF.filterUdfByDataTypeNumeric | Date: 2026-03-02_

This pattern demonstrates setting up test data via API calls, structuring UI interactions, and validating success messages using the AutomaterSelenium framework.

**Applies to:** Tests requiring setup of test data through APIs and validation of UI interactions in the AutomaterSelenium framework.

```java
public void filterUdfByDataTypeNumeric() {
    super.filterUdfByDataTypeNumeric();
}
```
### ProjectUDF.filterUdfByDataTypeNumeric
**Product Area**: Admin > Customization > Additional Fields (UDF) > Project Module
**Status (last run)**: PASSED ✅
**Complexity**: LOW — mostly read + count verification, no drag-drop or async waiting
**Preprocess Group**: `UDF_project_group1`

**What it tests**:
Verifies the 'Filter by Data Type: Numeric' functionality on the Additional Fields listview for the Project module. Steps:
  1. Navigates to Admin > Customization > Additional Fields
  2. Selects 'Project' module from left panel (AdditionalFieldsActionsUtil.selectModule)
  3. Clicks the 'Data Type' filter dropdown
  4. Selects 'Numeric' from dropdown
  5. Reads table settings to get page count (records shown)
  6. Counts all UDF rows where the type badge = Numeric (using XPATH count)
  7. Asserts count == page count (filter shows exactly the right results)

**Key framework methods**:
- `AdminActionsUtil.gotoentity(AdminConstants.SubModule.ADDITIONALFIELDS) → navigate to UDF page`
- `AdditionalFieldsActionsUtil.selectModule(moduleName)  → click 'Project' in left panel`
- `actions.click(AdditionalFieldsLocators.DATA_TYPE_FILTER) → open filter dropdown`
- `actions.click(AdditionalFieldsLocators.DATA_TYPE_FILTER_DROPDOWN.apply('Numeric')) → select type`
- `getTestCaseData(AdditionalFieldsDataConstants.AdditionalFieldsData.FIELDFILTERS) → load filter config`
- `AutomaterUtil.getValueAsArrayFromInputUsingAPIPath()   → extract numeric subtypes list from JSON`
- `actions.listView.setTableSettings()                    → set page size to max for full count`
- `actions.getText(RequestLocators.Listview.PAGE_COUNT)   → read 'X of Y' pagination text`
- `AdditionalFieldsActionsUtil.getCount(locator)          → count matching rows by XPath`
- `addSuccessReport / addFailureReport                    → record result`

**Key locators**: `AdditionalFieldsLocators.DATA_TYPE_FILTER`, `AdditionalFieldsLocators.DATA_TYPE_FILTER_DROPDOWN.apply(filterType)`, `AdditionalFieldsLocators.UDF_WITH_SPECIFIC_TYPE_COUNT.apply(type)`, `RequestLocators.Listview.PAGE_COUNT  (shared locator reused in UDF page)`
**Key data constants**: `AdditionalFieldsDataConstants.AdditionalFieldsData.FIELDFILTERS`, `RequestDataConstants.RequestData.TABLE_SETTINGS`
**Notes**: UDF_project_group1 preProcess likely creates Numeric UDF(s) via API beforehand. Uses report.startMethodFlowInStepsToReproduce / endMethodFlowInStepsToReproduce lifecycle. PAGE_COUNT locator is shared from Requests module — demonstrating locator reuse across modules.

---

## 23. REST API ARCHITECTURE — `RestAPI.java` Complete Analysis

_Source: `AutomaterSeleniumFramework/src/com/zoho/automater/selenium/base/client/api/RestAPI.java` (503 lines)_

### Architecture: Browser-Based API Execution

> **Critical**: All REST API calls go through the **browser's JavaScript engine** using Selenium `JavascriptExecutor`.
> There is NO direct HTTP client. The browser must have an **active logged-in session** for API calls to work.

```
Java: RestAPI.triggerRestAPI(method, apiPath, formData)
  │
  ├─ Maps DELETE → "del" string (SDP convention)
  ├─ Encodes formData: 'key=' + encodeURIComponent(JSON.stringify(value))
  ├─ Builds JS: "return sdpAPICall('apiPath','method','encodedData').responseJSON"
  │
  └─► Selenium executeScript(js) → browser executes synchronous XHR
       └─ Returns JSON string → parsed to JSONObject
```

### Core Public Methods

```java
// CREATE — returns entity ID string
String create(String entityName, String apiPath, JSONObject inputData)
// → POST → extracts response[entityName]["id"]
// → AUTO-REGISTERS entity in DataUtil.cleanUpIds for cleanup

// CREATE — returns full entity response object
JSONObject createAndGetResponse(String entityName, String apiPath, JSONObject inputData)
// → POST → returns response[entityName] JSONObject
// → MOST COMMON for preProcess (stores ID, name, displayID from response)

// CREATE — returns entire raw response (no unwrapping)
JSONObject createAndGetFullResponse(String apiPath, JSONObject inputData)
// → POST → returns entire response JSONObject

// READ
JSONObject get(String apiPath, JSONObject inputData)
// → GET → returns response object

// UPDATE
JSONObject update(String apiPath, JSONObject inputData)
// → PUT → returns response object

// DELETE
boolean delete(String apiPath)
// → DELETE → returns true if status_code == 2000

// SEARCH — by criteria
String getEntityIdUsingSearchCriteria(String pluralName, String apiPath, JSONObject inputData)
// → GET with search criteria → returns first matching entity ID

// SEARCH — by field value (2-step: metainfo → search)
String getEntityIDUsingFieldValue(String apiPath, String fieldName, String value)
// → First GETs metainfo to find search column name → then searches by that field
```

### Response Format
```json
{
  "entity_name": { "id": "123", "title": "...", ... },
  "response_status": { "status_code": 2000, "status": "success" }
}
```
- `status_code == 2000` → success
- `status_code != 2000` → throws `BadResponseException`

### Auto-Cleanup Mechanism
Every `POST` (create) call automatically pushes the entity ID + API path to `DataUtil.cleanUpIds` stack.
The framework's `postProcess` or test lifecycle calls cleanup on these IDs automatically.
When writing custom `postProcess`, you can also call `restAPI.delete("changes/".concat(id))` directly.

### Input Data Wrapping Pattern
```java
// Standard pattern used in Change.java:
JSONObject inputData = getTestCaseDataUsingCaseId(dataId);  // Loads from JSON file, resolves placeholders
JSONObject response = restAPI.createAndGetResponse(
    getName(),           // entity name (e.g., "change")
    getModuleName(),     // module API path (e.g., "changes")
    getInputData(inputData)  // wraps with module-specific envelope
);

// Alternative: when creating entities from other modules in preProcess
JSONObject inputData = DataUtil.getInputDataForRestAPI(getModuleName(), getName(), dataId, fields);
// → Loads JSON, resolves placeholders, wraps as {"change": {...}}
```

### Key Gotchas
1. **Session context**: preProcess runs in admin session (APIs work); method body runs in user session (user may lack permissions)
2. **Null response**: If `sdpAPICall` returns `undefined`/`null`, `responseString` is null → NPE in callers
3. **Browser required**: Must be on a valid SDP page for JS execution to work
4. **DELETE mapping**: Framework maps `DELETE` HTTP method to `"del"` string for `sdpAPICall`
5. **Form data encoding**: Values are JSON.stringify'd then encodeURIComponent'd
6. **No direct HTTP**: Cannot use RestAPI outside browser context (no curl/OkHttp)
7. **Auto-cleanup**: POST calls register for cleanup — be aware in postProcess to avoid double-delete

---

## 24. ClientFrameworkActions — Complete Component Hierarchy

_Source: `AutomaterSeleniumFramework/src/com/zoho/automater/selenium/base/client/ClientFrameworkActions.java` (88 lines)_

### Class Hierarchy
```
Actions (base)
  └── SDPCloudActions
        └── ClientFrameworkActions (final, singleton)
              ├── navigate    : Navigate
              ├── validate    : Validator
              ├── formBuilder : FormBuilder
              ├── listView    : ListView
              ├── detailsView : DetailsView
              ├── popUp       : PopUp
              │     ├── popUp.formBuilder : FormBuilderForPopUp
              │     └── popUp.listView    : ListViewForPopUp
              ├── admin       : Admin
              └── windowManager : WindowManager
```

### Access Pattern
```java
// All component access is through 'actions' instance:
actions.navigate.toModule(moduleName);
actions.validate.textContent(locator, expected);
actions.formBuilder.fillInputForAnEntity(true, fields, inputData);
actions.listView.columnSearch("Title", value);
actions.detailsView.clickSubTab("notes");
actions.popUp.listView.columnSearch("Subject", value);
actions.popUp.formBuilder.fillInputForAnEntity(true, fields, inputData);
actions.admin.navigateToAdminPage(subModule);
actions.windowManager.switchToNewTab(10);

// Direct action methods (inherited from SDPCloudActions):
actions.click(locator);
actions.type(locator, value);
actions.getText(locator);
actions.isElementPresent(locator);
actions.isElementPresent(locator, timeoutSeconds);
actions.clickByName(buttonName);
actions.clickByNameSpan(buttonName);
actions.setTableView(viewName);
actions.waitForAjaxComplete();
```

---

## 25. PopUp & ListViewForPopUp — Complete Method Reference

_Sources:_
- `AutomaterSeleniumFramework/src/.../components/popup/PopUp.java` (302 lines)
- `AutomaterSeleniumFramework/src/.../components/popup/ListViewForPopUp.java` (149 lines)
- `AutomaterSeleniumFramework/src/.../components/popup/FormBuilderForPopUp.java`

### PopUp Methods (`actions.popUp`)
```java
void clickByName(String buttonName)         // clicks button by name attribute inside popup
void clickByNameInput(String name)          // clicks input by name inside popup
void clickByNameSubmit(String name)         // clicks submit by name inside popup
void clickByNameSpan(String name)           // clicks span by name inside popup
boolean isColumnSelected(String column)     // checks if column is selected in popup
void columnChooser(String column, boolean enable)  // enable/disable column in popup
void setTableSettings(JSONObject data, String path) // configure table settings in popup
void selectFilterUsingSearch(String option)  // select filter by typing and searching
void selectFilterWithoutSearch(String option) // select filter by direct click
```

### ListViewForPopUp Methods (`actions.popUp.listView`)
```java
// Filter selection
void selectFilterUsingSearch(String option)
// → clicks PopupLocators.BTN_ALL_FILTER → actions.formBuilder.typeAndSelectOption(option)
// Uses Select2 type-and-select pattern

void selectFilterWithoutSearch(String option)
// → clicks PopupLocators.BTN_ALL_FILTER → clicks PopupLocators.FILTERVALUE.apply(option)
// Direct click on filter option text

// Column search (MOST COMMONLY USED)
void columnSearch(String column, String value)
// → clicks PopupLocators.ICON_SEARCH (search icon)
// → finds column index in TABLE_HEADER
// → types value in SEARCH_TABLE_HEADER(index) input
// Works for any popup with standard table layout
```

### Popup Locator Scoping — CRITICAL

All framework popup locators are scoped to `slide-down-popup` class:
```xpath
//*[contains(concat(' ', normalize-space(@class), ' '), ' slide-down-popup')][last()][contains(@class,'slide-down-popup')]
```

**This means framework PopUp methods work for:**
- Standard SDP attach popups (requests, problems, projects)
- Any popup using `slide-down-popup` CSS class

**This does NOT work for:**
- CH-286 association dialog (uses `association-dialog-popup changes-association` CSS class)
- Custom jQuery UI dialog popups with different class names

### When Framework Popup Methods Work vs Custom Locators

| Scenario | Framework popup methods? | Why |
|----------|------------------------|-----|
| Attach Request to Change | ✅ Yes | Uses `slide-down-popup` |
| Attach Problem to Change | ✅ Yes | Uses `slide-down-popup` |
| CH-286 Link Parent/Child Change | ⚠️ Partial | `columnSearch()` works (table structure same), but `selectFilter*()` fails (different popup class, Select2 filter not in `slide-down-popup`) |

**Pattern for CH-286 (and similar non-standard popups):**
```java
// Column search in popup — WORKS (table structure is compatible)
actions.popUp.listView.columnSearch("Title", changeName);

// Filter selection — DOES NOT WORK (popup class mismatch)
// Must use custom locators:
actions.click(ChangeLocators.LinkingChangePopup.FILTER_DROPDOWN);
actions.click(ChangeLocators.LinkingChangePopup.FILTER_OPTION.apply("All Changes"));
```

---

## 26. Select2 Dropdown Handling — Framework Patterns

### FormBuilder.typeAndSelectOption() Flow
```java
public void typeAndSelectOption(String value) throws SeleniumException {
    actions.type(TYPE_DROPDOWN_SEARCH_INPUT, value);   // xpath: //*[@id='select2-drop']//input
    actions.waitForAjaxComplete();
    actions.click(OPTION_ELEMENT.apply(value));         // xpath: //*[@id='select2-drop']//li//*[text()='value']
}
```

### Key Select2 Locators (from ClientFrameworkLocators.FormBuilderLocators)
```java
// Search input inside open Select2 dropdown
TYPE_DROPDOWN_SEARCH_INPUT = "//*[@id='select2-drop']/*[@class='select2-search']/input"

// Option element (renders at BODY level, NOT inside popup container)
OPTION_ELEMENT = "//*[@id='select2-drop']/descendant::*[@class='select2-results']//li[not(contains(@class,'unselectable'))]/descendant::*[text()='<value>']"

// Close mask (click to dismiss open dropdown)
CLOSE_POP_UP = By.id("select2-drop-mask")
```

### Select2 Behavior Notes
1. **Options render at body level**: Select2 appends its dropdown `#select2-drop` directly to `<body>`, NOT inside the parent popup/dialog — this means `OPTION_ELEMENT` works regardless of which popup opened the Select2
2. **Search triggers AJAX**: After typing, `waitForAjaxComplete()` is needed before clicking option
3. **Only one Select2 dropdown open at a time**: The framework's locator (`#select2-drop`) targets whichever one is currently open
4. **Close with mask**: Click `select2-drop-mask` to dismiss without selecting

### Reusing Select2 Locators in Custom Popups
Even when framework PopUp methods don't work (wrong popup class), you can still reuse Select2 locators:
```java
// ✅ Custom popup trigger + framework Select2 option locator
actions.click(CustomPopup.MY_SELECT2_TRIGGER);
actions.click(ClientFrameworkLocators.FormBuilderLocators.OPTION_ELEMENT.apply("All Changes"));

// ✅ Or define module-specific option locators matching the same Select2 pattern
// (This is what ChangeLocators.LinkingChangePopup.FILTER_OPTION does)
```

---

## 27. Existing Entity Creation Patterns — Reuse Over Reinvent

### The Standard Pattern (Change.java example)
```java
// In Change.java:
public JSONObject createChangeGetResponse(String dataId) throws Exception {
    JSONObject inputData = getTestCaseDataUsingCaseId(dataId);           // Load JSON + resolve placeholders
    JSONObject response = restAPI.createAndGetResponse(
        getName(),                // "change"
        getModuleName(),          // "changes"
        getInputData(inputData)   // Wraps as {"change": {...}}
    );
    LocalStorage.store(getName(), response.optString("id"));
    LocalStorage.store("changeId", response.optString("id"));
    LocalStorage.store("changeName", response.optString("title"));
    LocalStorage.store("changeDisplayID", ...);
    LocalStorage.store("changeDisplayValue", ...);
    return response;
}
```

### Creating Additional Entities in preProcess
When creating multiple entities of the SAME type (e.g., 3 changes for linking tests):
```java
// First change — use the standard method
createChangeGetResponse(dataIds[0]);

// Additional changes — call DataUtil.getInputDataForRestAPI() for fresh placeholder resolution
JSONObject targetData = DataUtil.getInputDataForRestAPI(getModuleName(), getName(), dataIds[0], fields);
JSONObject targetResponse = restAPI.createAndGetResponse(getName(), getModuleName(), getInputData(targetData));
// Store with numbered keys
LocalStorage.store("targetChangeId1", targetResponse.optString("id"));
LocalStorage.store("targetChangeName1", targetResponse.optString("title"));
```

**Why DataUtil.getInputDataForRestAPI?**
- Calling `getTestCaseDataUsingCaseId(dataId)` twice with the same `dataId` would return the same resolved data (same `$(unique_string)` timestamp)
- `DataUtil.getInputDataForRestAPI()` re-resolves placeholders, generating unique values each time

### RULE: Never Create Custom API Utility Methods When Standard Patterns Exist
```java
// ❌ WRONG — Creating ChangeAPIUtil.createChange() when Change.createChangeGetResponse() exists
public static void createChange(String dataId) { ... }

// ✅ CORRECT — Use the parent class method
createChangeGetResponse(dataIds[0]);

// ❌ WRONG — Manually constructing API calls in test methods
JSONObject body = new JSONObject().put("change", new JSONObject().put("title", "..."));
restAPI.triggerRestAPI(Method.POST, "changes", body);

// ✅ CORRECT — Use the framework's data layer
JSONObject inputData = getTestCaseDataUsingCaseId(dataId);
restAPI.createAndGetResponse(getName(), getModuleName(), getInputData(inputData));
```

---

## LINKING CHANGES (CH-286) — Parent-Child Association Pattern

### Feature Overview
Linking Changes allows associating changes in parent-child relationships via the LHS Association tab in Change Details. Key constraints:
- A change can be either a parent OR a child, never both (mutual exclusion)
- Max 1 parent per change, max 25 children per parent
- Parent selection uses **radio buttons** (single select); child uses **checkboxes** (multi-select)
- Popup has filters: All Changes / Open Changes / Closed Changes
- After parent linked → child option disappears; after child linked → parent option disappears
- Detach resets the tab to show both options again
- Badges appear in change title: "Parent Change" or "Child Change"

### Architecture Pattern: LHS Association Tab Tests
Unlike RHS associations (which use the right sidebar accordion), linking changes uses a **dedicated LHS tab**:

```
DetailsView.java                          ← Test methods live HERE (not in ChangeBase)
  ├─ preProcess: CREATE_CHANGES_FOR_LINKING group
  │   Creates 3 changes (1 source + 2 targets) via API
  │   Stores: entityId, changeName, targetChangeId1/2, targetChangeName1/2, targetChangeDisplayValue1/2
  ├─ Test flow: navigate → module → listview → details page → LHS Association tab → popup → validate
  └─ postProcess: Deletes target changes first, then source
```

### API Patterns for Linking
```java
// Link parent change
ChangeAPIUtil.linkParentChange(sourceChangeId, targetChangeId);
// → PUT api/v3/changes/{sourceId}/rel/parent_change  body: {"parent_change":[{"parent_change":{"id":targetId}}]}

// Unlink parent change
ChangeAPIUtil.unlinkParentChange(sourceChangeId, parentChangeId);
// → DELETE api/v3/changes/{sourceId}/rel/parent_change?ids=parentId

// Link child changes
ChangeAPIUtil.linkChildChanges(parentChangeId, childId1, childId2);
// → PUT api/v3/changes/{parentId}/rel/child_changes  body: {"child_changes":[{"child_changes":{"id":childId}},...]}

// Unlink child changes
ChangeAPIUtil.unlinkChildChanges(parentChangeId, "id1,id2");
// → DELETE api/v3/changes/{parentId}/rel/child_changes?ids=id1,id2
```

### Key Locator Patterns
- `ChangeLocators.LinkingChange.*` — LHS tab, sections, badges, attach/detach buttons
- `ChangeLocators.LinkingChangePopup.*` — Popup elements, filters, radio/checkbox selectors
- Function-based locators take entity IDs: `SELECT_RADIO_WITH_ENTITYID.apply(changeId)`, `SELECT_CHECKBOX_WITH_ENTITYID.apply(changeId)`
- `LINKED_CHANGE_ROW.apply(changeId)` — Verify a specific change is shown in association list

### Key Constants
- `ChangeAnnotationConstants.Group.CREATE_CHANGES_FOR_LINKING`
- `ChangeAnnotationConstants.Data.API_CREATE_CHANGE_FOR_LINKING`
- `ChangeConstants.PopupFilters.ALL_CHANGES / OPEN_CHANGES / CLOSED_CHANGES`
- `ChangeConstants.AlertMessages.PARENT_CHANGE_ASSOCIATED / DETACHED / CHILD_CHANGES_ASSOCIATED / DETACHED`

### Scenario Coverage (19 use cases → 6 test methods)
| Method | Use Cases | Focus |
|--------|-----------|-------|
| `verifyAssociationTabAndAttachOptionsInLHS` | 001, 005 | Tab + attach options |
| `verifyAttachParentChangePopup` | 006-011 | Parent popup UI elements |
| `attachParentChangeAndVerifyAssociation` | 012-016 | Attach parent + list view validations |
| `detachParentChangeAndVerifyReset` | 017 | Detach + reset |
| `verifyAttachChildChangePopup` | 018-019 | Child popup UI elements |
| `attachDetachChildChangesAndVerifyListView` | 002-004 | Full child flow + list view |

### Popup Pattern: CH-286 vs Standard SDP Popups

**Standard SDP association popups** (Attach Request, Problem, etc.):
- Container: `slide-down-popup` class
- Filter trigger: `requestnamecss` / `requestnameanc` class spans
- Filter options: `filter-search-menu` div with filter text spans
- Framework methods: `actions.popUp.listView.selectFilterWithoutSearch()` ✅

**CH-286 Linking Change popup** (Attach Parent/Child Change):
- Container: `association-dialog-popup changes-association` class (jQuery UI dialog)
- Filter trigger: Select2 widget (`select2-chosen` span inside dialog)
- Filter options: Select2 dropdown (`select2-result-label` div at body level)
- Framework methods: `actions.popUp.listView.columnSearch()` ✅ (table structure same), but `selectFilter*()` ❌ (different container class)

**Consequence**: Linking Change popups need custom `FILTER_DROPDOWN` and `FILTER_OPTION` locators in `ChangeLocators.LinkingChangePopup`, but can reuse `actions.popUp.listView.columnSearch()` for table search.

### Existing Association Test Pattern (from DetailsView.java line 112+)
```java
// Pattern from attachDetachRequestCausedByChangeRHS():
actions.navigate.toModule(getModuleName());
actions.setTableView(GlobalConstants.listView.LISTVIEW);
actions.listView.columnSearch("Title", LocalStorage.getAsString("changeName"));
actions.navigate.toDetailsPageUsingRecordId(getEntityId());
actions.click(ChangeLocators.ChangeDetailsview.STAGES.apply("planning"));
actions.click(ChangeLocators.ChangeDetailsview.RHS_ASSOCIATIONS.apply(REQUESTS_CAUSED_BY_CHANGE));
actions.click(ChangeLocators.ChangeDetailsview.ATTACH_DETACH_REQUEST.apply(REQUESTS_ATTACH));
actions.click(ChangeLocators.Popup.CLICK_LISTVIEW_FILTERS);       // Opens filter dropdown
actions.click(ChangeLocators.Popup.CLICK_ALL_REQUESTS_FILTERS);   // Clicks "All Requests"
actions.popUp.listView.columnSearch("Subject", LocalStorage.getAsString("subject")); // Popup column search
actions.click(ChangeLocators.ChangeListview.SELECT_CHECKBOX_WITH_ENTITYID.apply(id));
actions.clickByName(GlobalConstants.Actions.ASSOCIATE);
```

**Key difference from Linking Changes**: RHS association tests use `STAGES.apply("planning")` → `RHS_ASSOCIATIONS` pattern; Linking Changes uses LHS `LHS_ASSOCIATION_TAB` → `ATTACH_BUTTON_DROPDOWN` → `ATTACH_PARENT_CHANGE_OPTION` pattern.

### Learnings for Coder Agent
1. **LHS vs RHS**: Association tabs on LHS are navigated via `actions.click(LHS_ASSOCIATION_TAB)`, NOT via RHS accordion pattern
2. **Radio vs Checkbox**: Parent popup uses `SELECT_RADIO_WITH_ENTITYID` (radio), child uses `SELECT_CHECKBOX_WITH_ENTITYID` (checkbox). Never mix these.
3. **Mutual exclusion testing**: After linking as parent, verify child option disappears from Attach dropdown; after linking as child, verify parent option disappears
4. **preProcess creates 3 changes**: 1 source (the change we navigate to) + 2 targets (potential parents/children) — stored in LocalStorage with numbered keys
5. **Popup column search**: Use `actions.popUp.listView.columnSearch()` (not `actions.listView.columnSearch()`) when searching inside a popup
6. **Confirmation dialog pattern**: `actions.validate.confirmationBoxTitleAndConfirmationText("Confirm", "Do you want to detach")` + `actions.clickByNameSpan(GlobalConstants.Actions.YES)`
7. **Filter selection in non-standard popups**: When popup class differs from `slide-down-popup`, define custom filter locators matching the specific popup container (e.g., `association-dialog-popup`) but reuse Select2 `OPTION_ELEMENT` pattern since it renders at body level
8. **Entity creation reuse**: Always use `createChangeGetResponse(dataId)` from Change.java super class; for additional entities in preProcess, use `DataUtil.getInputDataForRestAPI()` + `restAPI.createAndGetResponse()` with numbered LocalStorage keys
9. **Existing popup locators pattern**: Each module defines its own popup locators in `ChangeLocators.Popup.*`, `ChangeLocators.LinkingChangePopup.*` etc. — these are module-specific, not framework-level

---
