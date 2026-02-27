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

**Before writing any logic in `<Entity>Base.java`, ALWAYS check `<Entity>ActionsUtil.java` first.**

- If the needed UI action already exists as a method in `SolutionActionsUtil` → **call it**, do NOT duplicate the logic.
- If the action does NOT exist → **add a new static method to `SolutionActionsUtil.java`** first, then call it from `SolutionBase.java`.
- The same rule applies to `SolutionAPIUtil.java` for any REST API helper logic.
- Never inline ActionUtil-level logic directly in a `Base.java` method body if it belongs in the util.

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