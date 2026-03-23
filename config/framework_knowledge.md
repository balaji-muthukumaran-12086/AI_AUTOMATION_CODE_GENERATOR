# AutomaterSelenium Framework — Complete Knowledge Base

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

## 1b. MODULE PLACEMENT

> **Module placement table & rules**: See `copilot-instructions.md` § "MODULE PLACEMENT".
> Key rule: derive module from the use-case noun, NEVER from the currently open file.

---

## 2. TWO-LAYER CLASS ARCHITECTURE

> **Rules & pattern**: See `framework_rules.md` § "SECTION 1".

**Examples from codebase:**
- `SolutionBase extends Entity` → `Solution extends SolutionBase`
- `ProblemCommonBase extends Entity` → `Problem extends ProblemCommonBase`
- `RequestCommonBase extends Entity` → `Request extends RequestCommonBase`

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
        group       = "NoPreprocess",                 // ← "" or "NoPreprocess" when no preProcess setup needed
        priority    = Priority.HIGH,
        dataIds     = {},                             // ← {} when no data creation required
        tags        = {},
        owner       = OwnerConstants.RAJESHWARAN_A,
        runType     = ScenarioRunType.USER_BASED,   // USER_BASED = no cross-test side effects
        // Use PORTAL_BASED for scenarios that trigger side effects impacting other tests
        // in the suite (e.g. business rules, SLA, automation rules). PORTAL_BASED runs in
        // isolation — effects are scoped and cleaned up within that session.
        description = "Creating Unapproved Private solution using general template"
        // switchOn omitted → defaults to SwitchToUserSession.AFTER_PRE_PROCESS
        // Use BEFORE_PRE_PROCESS when preProcess must run in user session
        // Use NEVER when entire test must run in admin session
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

### Architecture — where preProcess() lives

`preProcess()` is an **abstract method** defined in `Entity.java`:
```java
/**
 * Used to populate data for the current entity as well as for the parent entity.
 * Group and data ids details provided in the automater annotation
 * w.r.t the function will be passed as an argument.
 */
protected abstract boolean preProcess(String group, String[] dataIds);
```

`preProcess()` is often defined in the **module parent class**, but **subclasses can and do
override it**. Always check the **subclass first** for a `preProcess()` override before
looking in the parent.

```
Change.java (parent)            → owns preProcess with all group branches by default
DetailsView extends Change      → if no override, inherits parent's preProcess
ChangeWorkflow extends Workflow  → may have its own preProcess override for workflow-specific groups

Solution.java (parent)          → owns preProcess, ends with super.preProcess(group, dataIds)
SolutionBase.java               → base helper class, not where groups are defined
```

**Discovery order (mandatory):**
1. Open the leaf/subclass file → look for its own `preProcess()` method
2. If found: that is authoritative. Check if it ends with `return super.preProcess(group, dataIds)` — if yes, also read the parent
3. If not found: open the parent class (from `extends` clause) and read its `preProcess()`

```bash
# Find parents: check extends clause in the scenario file
grep -n "class .* extends" <TargetClass>.java
# Then read preProcess() in that parent class
grep -n "equalsIgnoreCase\|case " <ParentClass>.java
```

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

**Critical rules for group + dataIds:**

| Scenario | group | dataIds | Meaning |
|---|---|---|---|
| No data creation needed at all | `""` or `"NoPreprocess"` | `{}` | preProcess either skips or returns true immediately — no API calls, no cleanup |
| Group handles data creation internally | `"create"` | `{}` | preProcess executes the matching if/else or switch block, but data creation is handled without dataIds (e.g., hardcoded API calls or data loaded from known constants inside the block) |
| Group uses passed dataIds for data creation | `"create"` | `{AnnotationConstants.Data.KEY1, ...}` | preProcess uses `getTestCaseDataUsingCaseId(dataIds[0])`, `dataIds[1]`, etc. by index |

**The purpose of `group`** is solely to match which preProcess block (if/else or switch-case) should execute.
**`dataIds`** is an optional array — some groups need them, some don't. It depends on the implementation.
**When dataIds are provided**, they must reference string constants from `<Entity>AnnotationConstants.Data`.

### ⭐ Minimal Group Selection (MANDATORY)
Always select the **lightest** preProcess group that satisfies the test method's actual data needs:
- Test method uses NO entity at all → `group = "NoPreprocess"`, `dataIds = {}`
- Test method ONLY uses `getEntityId()` → use simplest group (e.g., `"create"`) + single template
- Test method references extra entities (e.g., `linkChange_*_id`) → use the heavy multi-entity group

**FORBIDDEN**: Assigning the heaviest group to ALL scenarios "just in case" — wastes API calls, slows suite, creates unnecessary cleanup.

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
| `$(user_id)` | Scenario user’s entity ID |
| `$(admin_email_id)` | Admin user’s email |
| `$(admin_name)` | Admin user’s display name |
| `$(date, N, ahead)` | Date N days ahead (milliseconds string) |
| `$(datetime, N, ahead)` | Datetime N days ahead |
| `$(mspcustomer_id)` | MSP customer ID (MSP tests only) |
| `$(mspcustomer_name)` | MSP customer name (MSP tests only) |
| `$(mspcustomer_email)` | MSP customer email (MSP tests only) |
| `$(common_string)` | Timestamp + partName (unique per run) |
| `$(rest_api, method, apiPath, inputDataKey, storageKey)` | Calls REST API, stores result in LocalStorage |
| `$(local_storage, store, key, value)` | Stores value in LocalStorage at resolve time |
| `$(local_storage, get, key)` | Reads value from LocalStorage at resolve time |

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

### ⚠️ FORBIDDEN: Inline JSONObject Construction for Data Creation

NEVER build test data from scratch with `new JSONObject().put(...)` chains in Java code.
ALL entity data (UI inputs AND API payloads) MUST originate from `*_data.json` and be loaded
via `getTestCaseData()` / `getTestCaseDataUsingCaseId()` / `DataUtil.getTestCaseDataUsingFilePath()`.
This applies to **test methods, preProcess, AND APIUtil files**.

```java
// ❌ FORBIDDEN — inline JSON construction
JSONObject inputData = new JSONObject();
inputData.put("title", "My Change " + System.currentTimeMillis());
inputData.put("change_type", new JSONObject().put("name", "Standard"));

// ✅ CORRECT — load from *_data.json
JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[0]);
```

**Post-load modification IS allowed** — After loading from `*_data.json`, you MAY use `.put()` / `.remove()`
to modify the loaded data when the modification is dynamic and cannot be expressed via `$(custom_KEY)`.

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

> **Full ID rules, CSV vs fallback flow, and multi-ID grouping**: See `framework_rules.md` § "SECTION 7" and `copilot-instructions.md` § "Test ID Source".

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
```

#### ⚠️ Data Loading Methods — Correct Context (REQUIRED)

| Method | Where to use | Parameter | Auto-path? |
|--------|-------------|-----------|------------|
| `getTestCaseData(TestCaseData)` | **Test method body** | `DataConstants` constant | ✅ from TestCaseData object |
| `getTestCaseDataUsingCaseId(dataIds[N])` | **preProcess() only** | Raw string from `dataIds` array | ✅ auto from `getModuleName()`+`getName()` |
| `DataUtil.getTestCaseDataUsingFilePath(path, caseId)` | **APIUtil files** (static methods) | Explicit file path + case ID string | ❌ manual path |

**Forbidden combinations:**
- `getTestCaseDataUsingCaseId()` inside APIUtil → no Entity context in static methods
- `DataUtil.getTestCaseDataUsingFilePath()` inside preProcess → use `getTestCaseDataUsingCaseId()` instead
- `getTestCaseData("raw_string")` → never pass raw string, always use `DataConstants` constant

```java

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

> **ActionUtils/APIUtil rules (Rules 1-5), class declaration pattern, method design, test method body rules, and known utility files table**: See `framework_rules.md` § "SECTION 20" and `copilot-instructions.md` § "ActionUtils / APIUtil Pattern".
> Discovery command: `find src/com/zoho/automater/selenium/modules/<module>/<entity>/utils/ -name "*.java" | sort`


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
Every `POST` (create) call automatically registers the entity for cleanup in two structures:
- `DataUtil.cleanUpIds` — `HashMap<String, String>` mapping API path → entity ID
- `DataUtil.cleanUpCalls` — `Stack<String>` of API paths in LIFO (last-in-first-out) order

Cleanup iterates the Stack in LIFO order — child entities are deleted before parent entities (prevents foreign-key constraint errors).
Cleanup skips roles, technician, requester, and sites (no deletion needed).
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
8. **UI-only test methods + feature-under-test separation (UNIVERSAL RULE)**: This is a UI automation framework. Test method bodies must ONLY contain UI interactions (Selenium clicks, navigation, form fills, text validations). API calls in test methods turn it into API testing, which is NOT the purpose. **Critical distinction**: preProcess API is for **raw entity creation** (creating changes, users, templates that need to EXIST) and **state setup** (trashing, closing entities as prerequisite). The **feature/action being tested** (linking, associating, approval flow, status transitions) MUST be performed via UI in the test method — NEVER via API in preProcess. Example: if the test verifies "link child change", preProcess creates both changes (API), the test method performs the linking (UI). If the test verifies "trashed change not in popup", preProcess creates + trashes (API), the test method opens popup and verifies absence (UI).

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

## ASSET WORKFLOW — Special Sub-Module Pattern (CH-2320, rev 5322)

### Why Asset workflow is different
Asset workflows require a `sub_module` field in the API payload that specifies which asset type the workflow applies to (e.g., `"Computers"`, `"Printers"`, etc.). The base `Workflow.java` methods do not inject this field, so ALL Asset workflow boundary tests must `@Override` the base methods to add it.

### Key API pattern
```java
// ✅ CORRECT — inject sub_module before create
JSONObject workflowPayload = buildWorkflowPayload(...);
workflowPayload.optJSONObject("workflow").put("sub_module", "Computers");
JSONObject response = restAPI.createAndGetFullResponse("workflows", workflowPayload);
```

### `Workflow.java` stage config additions (rev 5322)
- Added `"Asset"` key to the module→stage-config mapping in `Workflow.java`
- Added `"Asset"` → `"asset_workflows"` entry to the API key mapping
- AssetWorkflow overrides: `verifyStatementTupleLimitRejectionOnOverflow()`, `verifyStatementTupleLimitAcceptedAtMaximum()`, `verifyStatementTupleLimitRejectionOnOverflow_UI()`, `verifyStatementTupleLimitAcceptedAtMaximum_UI()`, plus hybrid boundary tests

### Test IDs
`SDPOD_WF_TUPLE_LIMIT_AS_001–009` — API-reject(001), API-accept(002), UI-reject(003), UI-accept(004), hybrid tests (005–008), canvas-open-with-100-tasks (009)

### Can you have both `.git/` and `.hg/` in the same directory?
**Yes.** Running `git init` inside an existing hg repo creates `.git/` alongside `.hg/`. They do not interfere. This is a valid way to push a feature branch to GitHub when the hg remote is broken.

### Parent git repo safety
If the parent git repo (e.g., `ai-automation-qa/`) has the hg project directory in `.gitignore`, the nested `git init` inside that subdirectory is fully isolated and safe.

### Setting up a git repo inside an hg project for GitHub push
```bash
cd SDPLIVE_LATEST_AUTOMATER_SELENIUM/
git init
git checkout -b "MY_FEATURE_BRANCH_NAME"

# Create .gitignore (exclude compiled bins, hg metadata, reports)
cat > .gitignore << 'EOF'
bin/
build/
product_package/
logs/
reports/
.hg/
src.zip
EOF

git add src/ resources/ .gitignore .classpath .project .hgignore
git -c user.name="Name" -c user.email="email@example.com" \
    commit -m "Feature: description"

git remote add origin https://github.com/USERNAME/REPO.git
git push -u origin MY_FEATURE_BRANCH_NAME
```

### GitHub push authentication — Linux (no keychain)

`git credential-osxkeychain` is macOS-only — not available on Linux.

On Linux, two options:

**Option A — SSH key (recommended, permanent):**
```bash
# Check existing SSH key
cat ~/.ssh/id_ed25519.pub
# Add this key to: github.com → Settings → SSH and GPG keys → New SSH key
# Then switch remote to SSH:
git remote set-url origin git@github.com:USERNAME/REPO.git
# Accept GitHub host fingerprint once:
ssh-keyscan -t ed25519 github.com >> ~/.ssh/known_hosts
git push -u origin MY_BRANCH
```

**Option B — Personal Access Token (one-time):**
```bash
# 1. Create PAT at: github.com → Settings → Developer settings →
#    Personal access tokens → Tokens (classic) → Generate → select "repo"
# 2. Embed token in URL:
git remote set-url origin https://USERNAME:TOKEN@github.com/USERNAME/REPO.git
git push -u origin MY_BRANCH
# ⚠️ Remove token from URL after push (security):
git remote set-url origin https://github.com/USERNAME/REPO.git
```

### GitHub error messages interpreted
| Error | Real cause |
|-------|-----------|
| `remote: Repository not found` | EITHER repo doesn't exist OR credentials missing — GitHub gives same error for both |
| `Permission denied (publickey)` | SSH key not added to GitHub account |
| `fatal: Authentication failed` | Wrong password / revoked PAT |

---

## FRAMEWORK SOURCE ANALYSIS — Mar 2026
*Sourced from `automater-selenium-framework-*.zip` in the dependencies folder*

> **Reading framework source**: When you need to verify framework method behaviour (e.g., which
> methods call `waitForAjaxComplete()` internally), read directly from the framework ZIP:
> ```bash
> DEPS_DIR=$(python -c "from config.project_config import DEPS_DIR; print(DEPS_DIR)")
> FW_ZIP=$(find "$DEPS_DIR" -name 'automater-selenium-framework-*.zip' | head -1)
> unzip -p "$FW_ZIP" "com/zoho/automater/selenium/base/Actions.java" | grep -n "pattern"
> ```
> Key files: `Actions.java`, `Navigate.java`, `FormBuilder.java`, `Validator.java`, `SDPCloudActions.java`, `RestAPI.java`

### Methods that call `waitForAjaxComplete()` internally (VERIFIED from source)

| Method | Internal `waitForAjaxComplete()` | Implication |
|--------|--------------------------------|-------------|
| `actions.click(locator)` | ✅ BEFORE click | No manual wait needed between consecutive clicks |
| `actions.type(locator, value)` | ✅ inside | No manual wait needed before/after type |
| `actions.sendKeys(locator, value)` | ✅ inside | No manual wait needed before/after sendKeys |
| `actions.sendKeys(locator, key, value)` | ✅ inside | No manual wait needed |
| `actions.getText(locator)` | ✅ inside + 3s `waitForAnElementToAppear` | May miss slow pages — add `Thread.sleep()` if needed |
| `actions.navigate.to(locator)` | ✅ click + `waitForAjaxCompleteLoad()` | Double-waited |
| `actions.navigate.toModule(name)` | ✅ `to()` + extra `waitForAjaxComplete()` | Fully waited |
| `actions.navigate.toDetailsPageUsingRecordId(id)` | ✅ `waitForAnElementToAppear` + `to()` + `waitForAjaxComplete()` | Fully waited |
| `actions.navigate.toGlobalActionInDetailsPage(name)` | ✅ `waitForAnElementToAppear` + `to()` | Waited |
| `actions.navigate.toGlobalActionInListview(name)` | ✅ via `to()` | Waited |
| `actions.formBuilder.fillInputForAnEntity(...)` | ✅ each field fill calls waited methods | Fully waited per field |

**When you NEED manual `waitForAjaxComplete()`:**
- After `actions.type()` in a search field where AJAX populates results, and the next action reads those results
- After `executeScript()` that modifies DOM
- Before non-click reads (`getText`, `isElementPresent`) if a preceding AJAX action's response hasn't settled

---

## Complete Placeholder Reference (PlaceholderUtil.java)

> **Full placeholder table**: See `copilot-instructions.md` § "Complete Runtime Placeholder Reference".

Pattern matched: `$(placeholder)` with optional nested `$(...)` inside.  
`DataUtil.getTestCaseDataUsingFilePath()` runs up to **3 refill passes** for nested placeholders.

### `$(rest_api, ...)` methods (unique — not in copilot-instructions)

| Method arg | API call | Returns |
|------------|----------|---------|
| `get` | `RestAPI.getEntityIdUsingSearchCriteria(entity, path, data)` | entity ID string |
| `post` | `RestAPI.create(entity, path, data)` | created entity ID |
| `getResponse` | `RestAPI.get(path, null)` then extracts `dataPath` field | field value |
| `search` | `RestAPI.getEntityIDUsingFieldValue(entity, path, dataId)` | entity ID |
| `getFieldValue` | `RestAPI.get(path, listInfoData)` + traverses `dataPath` array | field value |

> LocalStorage is also seeded: after any `rest_api` placeholder resolves, the value is
> automatically stored under `dataId` key in LocalStorage.

### URL `$[custom_KEY]` (square brackets) in `rest_api` paths

Inside a `$(rest_api, ...)` URL, use `$[custom_KEY]` (square brackets) to embed a LocalStorage
value into the URL itself — e.g., `requests/$[custom_request]/notes`.

---

## DataUtil Caching Behaviour

`DataUtil.getTestCaseDataUsingFilePath()` caches loaded JSON entries by `filePath_id` key in a
session-scoped singleton. If the same `TestCaseData` is called multiple times in one test run,
disk is read only once — subsequent calls return the cached (pre-placeholder-resolved) copy.

> **Implication**: If you call `LocalStorage.store(key, newValue)` AFTER the first `getTestCaseData()`
> call, and expect `$(custom_key)` to pick up the new value on a second call — it WON'T, because
> the cache returns the already-resolved string. Pre-seed LocalStorage **before** the first
> `getTestCaseData()` call for the same `TestCaseData` key.

---

## `cleanUp()` — Singletons Destroyed After Every Test

> **Full cleanup list and rules**: See `framework_rules.md` § "SECTION 27.3".

Key fact: zero state leakage between runs — `LocalStorage`, `DataUtil`, `RestAPI`, `EntityMetaDetails`, `ScenarioReport`, `DriverUtil` all destroyed in `EntityCase.cleanUp()` finally block.

---

## Report Flow — `addSuccessReport` / `addFailureReport` / `addReport`

> **Full report flow internals**: See `framework_rules.md` § "SECTION 27.1" and "SECTION 27.4".

Key: `addReport(msg)` is the smart variant — inspects `failureMessage.length()` to auto-route to success or failure.

---

## preProcess switch/case vs if/else-if — Preference Guide

> **preProcess rules, group selection, and reuse patterns**: See `framework_rules.md` § "SECTION 28".

Quick guide: 1–2 groups → `if/else-if`; 4+ groups → `switch(group)`. Always end with `return super.preProcess(group, dataIds)` to chain up.

---

## Multi-level Class Inheritance Pattern

Entity class hierarchies can be more than 2 levels deep:

```
Entity
  └─ TaskBase extends Entity
       └─ ProjectMilestoneTaskBase extends TaskBase
            └─ ProjectMilestoneTask (leaf — @AutomaterSuite, @AutomaterScenario methods)
```

Each level can override `preProcess()`, `postProcess()`, and `getEntityConfigurationName()`.
The leaf class calling `super.preProcess(group, dataIds)` chains up the hierarchy.

> Always check EVERY level of the inheritance chain when a group isn't being found.
> Use `super.preProcess()` at the end of subclass `preProcess()` to fall through to parent.

---

## @AutomaterCase vs @AutomaterScenario

> **Full comparison and when to use each**: See `framework_rules.md` § "SECTION 29".

Key: `@AutomaterScenario` = leaf class, standalone test entry; `@AutomaterCase` = Base class, reusable parameterized helper called by other methods.

---

## postProcess Conditional Cleanup Pattern

> **postProcess rules and cleanup strategy**: See `framework_rules.md` § "SECTION 28.3".

Key: `postProcess(String method)` receives the Java method name. Use `contains()`/`startsWith()` for selective cleanup. Always swallow exceptions — test result is already recorded.

---

## LocalSetupManager — How Local Run Detection Works

`LocalSetupManager.isLocalSetup()` checks ONLY:
```java
System.getProperty("automation.local.setup", "false")
```

This is set in `run_test.py` via the `-D` JVM argument. The class does NOT access
`CommonVariables` at all — because `CommonVariables` has a static initializer that loads
`Constants`, which depends on Aalam framework classes not present on developer machines.

```java
// ✅ Safe to call anywhere — no CommonVariables dependency:
if(LocalSetupManager.isLocalSetup()) {
    String serverUrl = LocalSetupManager.getServerUrl();
    String admin     = LocalSetupManager.getAdminUser1();
}

// ❌ NEVER do this in code that runs locally:
String serverUrl = CommonVariables.SERVER_URL_NAME;  // triggers static init → crash
```

`LocalSetupManager.configure(LocalAutomationData)` sets the local environment:
- `serverUrlName`, `adminUser1` / `adminUser1Pwd`, `portalName`
- `buildName` (= report folder name prefix)
- `browserType`, `headless`
- `localSetupBrowserPath` (geckodriver path), `localSetupChromeBrowserPath` (browser binary)
- Calls `setupReportDirectory(reportName)` — creates the `reports/LOCAL_<name>/` folder

---

## BeforeAndAfterCaseActions — Lifecycle Phase Order

Full lifecycle from `BeforeAndAfterCaseActionsFramework`:
```
1. assignConstantsToTemp()      — transfer Aalam metadata (framework)
2. assignCommonVariables()      — init CommonVariables (framework)
3. prerequisiteActions()        — resetStateVariables + configureAalam + loadSessionDetails + loadScenarioDetails + setupDownloadFolder
4. beforeBrowserLaunch()        — pre-launch validations (framework)
5. checkAndLaunchBrowser()      — launch browser if quitBrowser=true or driver=null
6. afterBrowserLaunch()         — window size set in driver class, not here
7. beforeLogin()                — INTENTIONALLY EMPTY — login handled in Entity.java
8. login()                      — INTENTIONALLY EMPTY — login handled in Entity.java/LoginUtil.java
9. afterLogin()                 — set startTime, is_logged_in=true, useCaseStarted=true
```

Login is handled by `Entity.java`'s `initializeAdminSession()` → `LoginUtil.login()` call,
NOT by the before/after lifecycle. The `BeforeAndAfterCaseActions.login()` override is a no-op.

---

## SolutionBase.createSolution() — Pattern for storing entity in LocalStorage

```java
// Standard pattern for preProcess API create + LocalStorage storage:
private void createSolution(String dataId) throws Exception {
    JSONObject inputData = getTestCaseDataUsingCaseId(dataId);
    JSONObject solutionResponse = restAPI.createAndGetResponse(getName(), getModuleName(), getInputData(inputData));
    LocalStorage.store(getName(), solutionResponse.optString("id"));    // "solution" → entity ID
    LocalStorage.store("Title",   solutionResponse.optString("title")); // human-readable title
}
```

- `getName()` → `"solution"` (from `getEntityConfigurationName()`)
- `getModuleName()` → `"solutions"` (plural, from entity config JSON)
- `getInputData(JSONObject)` wraps with the module's API input key: `{"solution": {...}}`
- `restAPI.createAndGetResponse()` returns the created entity's JSON object (not just the ID)
- Always store BOTH the ID (under `getName()`) and the display title for assertions

---

## Skeleton Scaffolding

> **Full naming rules, artifact map, generated vs manual files, and entity_skeleton.json**: See `framework_rules.md` § "SECTION 31".

Key facts unique to deep knowledge:
- `getEntityConfigurationName()` returns the snake_case entity name → lookup key for `conf/<module>/<name>.json`
- Simple entities (1-3 scenarios, no shared preProcess) skip the Base split — put `@AutomaterScenario` directly in parent
- Skeleton `preProcess` stub returns `false` (tests SKIPPED) — must replace with real implementation

---

## AutoGenerateConstantFiles — How Constants Are Auto-Generated

> **Dispatch map, naming derivation, FieldDetails constructor, and workflow**: See `framework_rules.md` § "SECTION 32".

Key deep facts:
- `DataUtil` caching: same `filePath_id` is read from disk only once per test run. Pre-seed LocalStorage BEFORE first `getTestCaseData()` call.
- `AnnotationConstants.java` is NOT auto-generated — always hand-edited.
- Constant name = `dataId.toUpperCase()` (no camelCase splitting) — always use `snake_case` keys in `*_data.json`.

---

## createUserByRole — Role System Architecture

> **Full flow tree, role JSON structure, SDADMIN rules, and is_technician paths**: See `framework_rules.md` § "SECTION 33" and `copilot-instructions.md` § "Role Constants".

Key deep facts:
- `getRoleDetails()` reads `general.json` first (sdadmin, sdsite_admin, sdguest, helpdeskconfig) → if found, returns immediately. Module JSON is fallback only.
- `is_technician=true` → `createTechnician()` (also `checkCustomRole` + `checkProjectRole`); `false` → `createRequester()`
- SDADMIN + admin email = no session split. Both preProcess and test method run as admin.

---

## RBAC Scenario Lifecycle — Complete Pattern (MANDATORY for Role-Based Tests)

> **Root cause of ~28 failed test cases (Mar 2026 batch)**: RBAC scenarios ran as admin,
> missing the entire user-role-switch flow. Admin always has all permissions — testing
> permission restrictions as admin proves nothing.

### Required 3-Phase Lifecycle

**Phase 1 — preProcess: Create user with target role (runs in admin session)**
```java
// In parent class preProcess() — add new group for RBAC scenarios:
} else if ("createWithRole".equalsIgnoreCase(group)) {
    // Step 1: Clean slate — delete any existing scenario user from prior runs
    deleteScenarioUser(ScenarioUsers.TEST_USER_3);

    // Step 2: Create user with the target role
    User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
    actions.createUserByRole(AutomaterConstants.TECHNICIAN, getModuleName(), "SDChangeManager", user);
    LocalStorage.store("techName", user.getDisplayId());

    // Step 3: Create prerequisite data (still in admin session — full permissions)
    JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[0]);
    JSONObject response = restAPI.createAndGetResponse(getName(), getModuleName(), getInputData(inputData));
    LocalStorage.store(getName(), response.getString("id"));
    LocalStorage.store("entityName", response.getString("title"));
}
```

**Phase 2 — Test method: Switch to role user, test under their permissions**
```java
public void verifyRoleCanPerformAction() throws Exception {
    report.startMethodFlowInStepsToReproduce(AutomaterUtil.getPascalValueFromCamelCase(getMethodName()));
    try {
        // Switch to the role-specific user
        User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
        actions.switchUser(user);

        // All subsequent UI actions now run under the restricted user's permissions
        actions.navigate.toModule(getModuleName());
        // ... verify what this role CAN or CANNOT do ...

        // Switch back to admin if further admin operations needed
        switchToAdminSession();

        addSuccessReport("Verified role-based access for " + getRole());
    } catch (Exception exception) {
        addFailureReport("RBAC test failed", exception.getMessage());
    } finally {
        report.endMethodFlowInStepsToReproduce();
    }
}
```

**Phase 3 — Cleanup: `deleteScenarioUser` before creating user (avoids stale state)**
```java
// Always call deleteScenarioUser() BEFORE createUserByRole() for clean slate:
deleteScenarioUser(ScenarioUsers.TEST_USER_3);
actions.createUserByRole(AutomaterConstants.TECHNICIAN, "changes", "SDChangeManager", user);
```

### ScenarioUsers Slot Allocation

| ScenarioUsers | Mapped to | Typical role in RBAC tests |
|---|---|---|
| `MAIN_USER` | `EMAIL_ID` (tech email from config) | Primary test actor |
| `TEST_USER_1` | 1st email from `SDP_TEST_USER_EMAILS` | Requester |
| `TEST_USER_2` | 2nd email | Secondary tech / requester |
| `TEST_USER_3` | 3rd email | Role-specific user (SDChangeManager, approver, etc.) |
| `TEST_USER_4` | 4th email | Additional role user |

All 5 users share `DEFAULT_PASSWORD`. Emails configured via `SDP_TEST_USER_EMAILS` in `.env`.

### FORBIDDEN RBAC Anti-Patterns

```java
// ❌ Testing role restrictions as admin — admin ALWAYS has all permissions → proves nothing
public void verifyNoEditPermission() throws Exception {
    // Missing: actions.switchUser(user) — runs as admin → always succeeds
    actions.navigate.toDetailsPageUsingRecordId(getEntityId());
    addSuccessReport("baseline confirmed");  // ← meaningless — admin can do everything
}

// ❌ Placeholder comments instead of actual role switching
addSuccessReport("Admin baseline — role restriction test requires non-edit user");
// This is NOT a valid test. MUST actually switch to the restricted user.
```

---

## Close Change via Stage Transitions (API Pattern)

> **Learned from Linking Changes batch (Mar 2026)**: SDP product requires SDChangeManager
> privilege to close a change. Admin user may NOT have SDChangeManager role (subscription
> admin restriction). Solution: create tech with SDChangeManager → assign as change_manager
> → advance through all 8 stages.

### SDP Change Lifecycle — All 8 Stages in Order

```
Submission → Planning → CAB Evaluation → Implementation → UAT → Release → Review → Close
```

### Stage Transition API Pattern

Each transition = PUT to `changes/<id>`:
```json
{"change": {"stage": {"name": "Planning"}, "status": {"name": "Planning In Progress"}, "comment": "Moving to Planning"}}
```

### Complete closeChange Utility Method Pattern

```java
public static void closeChangeViaAPI(RestAPI restAPI, String changeId) throws Exception {
    String[][] transitions = {
        {"Planning", "Planning In Progress"},
        {"CAB Evaluation", "CAB Evaluation In Progress"},
        {"Implementation", "Implementation In Progress"},
        {"UAT", "UAT In Progress"},
        {"Release", "Release In Progress"},
        {"Review", "Review In Progress"},
        {"Close", "Completed"}
    };
    for (String[] t : transitions) {
        JSONObject stageData = new JSONObject();
        stageData.put("stage", new JSONObject().put("name", t[0]));
        stageData.put("status", new JSONObject().put("name", t[1]));
        stageData.put("comment", "Advancing to " + t[0]);
        restAPI.update("changes/" + changeId, new JSONObject().put("change", stageData));
    }
}
```

### Critical Rules for Stage Transitions

1. **NEVER send `closure_code` field** — always returns `EXTRA_KEY_FOUND_IN_JSON` error
2. **The API may pick different statuses** than requested but DOES advance the stage correctly
3. **Tests only check `stage.name == "Close"`** — specific status within Close doesn't matter
4. **SDChangeManager role required** — admin without this role CANNOT close changes
5. **For preProcess**: create tech with SDChangeManager → set them as `change_manager` on the change → switch to tech → advance stages → switch back to admin

### preProcess Pattern for Close-Change Scenarios

```java
} else if ("createAndCloseChange".equalsIgnoreCase(group)) {
    // 1. Create tech user with SDChangeManager role
    deleteScenarioUser(ScenarioUsers.TEST_USER_3);
    User tech = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
    actions.createUserByRole(AutomaterConstants.TECHNICIAN, "changes", "SDChangeManager", tech);

    // 2. Create change with change_manager = tech user
    LocalStorage.store("change_manager_name", tech.getDisplayId());
    JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[0]);
    JSONObject response = restAPI.createAndGetResponse(getName(), getModuleName(), getInputData(inputData));
    String changeId = response.getString("id");
    LocalStorage.store(getName(), changeId);

    // 3. Switch to tech → close change → switch back
    actions.switchUser(tech);
    ChangeAPIUtil.closeChangeViaAPI(restAPI, changeId);
    switchToAdminSession();
}
```
