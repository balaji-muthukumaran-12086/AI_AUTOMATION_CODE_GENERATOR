"""
coder_agent.py
--------------
Coder Agent: Generates actual Java test code for each planned scenario.

For each module in the test_plan it:
  1. Pulls full context from ContextBuilder (existing source files)
  2. Retrieves similar existing scenarios from VectorStore
  3. Asks the LLM to generate TWO pieces per scenario:
     - @AutomaterScenario wrapper (thin delegation in Entity class)
     - Actual implementation (in EntityCommonBase, or Entity if no CommonBase exists)

Output: state['generated_code'] list of { module, class_name, code, file_path }
"""

import os
import re
from pathlib import Path
from typing import Any

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from agents.state import AgentState
from agents.llm_factory import get_llm, supports_tool_calling
from agents.coder_tools import CODER_TOOLS
from knowledge_base.context_builder import ContextBuilder
from knowledge_base.vector_store import VectorStore


def _load_framework_rules() -> str:
    """Load the validated rules document — prevents LLM hallucination."""
    rules_path = Path(__file__).resolve().parents[1] / 'config' / 'framework_rules.md'
    try:
        return rules_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        return ''  # graceful degradation


def _load_framework_knowledge() -> str:
    """Load the deep framework knowledge doc — lifecycle, traps, LocalStorage, REST session context."""
    knowledge_path = Path(__file__).resolve().parents[1] / 'config' / 'framework_knowledge.md'
    try:
        return knowledge_path.read_text(encoding='utf-8')
    except FileNotFoundError:
        return ''  # graceful degradation


# Imported lazily to avoid circular imports (learning_agent also imports from agents.llm_factory)
def _load_recent_learnings() -> str:
    """Return latest learnings from logs/learnings.jsonl for prompt injection."""
    try:
        from agents.learning_agent import load_recent_learnings
        return load_recent_learnings()
    except Exception:
        return ''


def _get_api_reference(module_path: str) -> str:
    """
    Extract the relevant API endpoints section from SDP_API_Endpoints_Documentation.md
    for the given module_path (e.g. 'modules/changes/change').

    Returns the core endpoints table + automation cases subsection for that module,
    capped at 120 lines to stay within prompt budget. Returns '' if not found.
    """
    doc_path = Path(__file__).resolve().parents[1] / 'docs' / 'api-doc' / 'SDP_API_Endpoints_Documentation.md'
    if not doc_path.exists():
        return ''

    # Map module_path segment → doc section keyword
    _MODULE_TO_DOC_SECTION: dict[str, str] = {
        'requests':      'Module 1 — Requests',
        'request':       'Module 1 — Requests',
        'changes':       'Module 2 — Changes',
        'change':        'Module 2 — Changes',
        'problems':      'Module 3 — Problems',
        'problem':       'Module 3 — Problems',
        'releases':      'Module 4 — Releases',
        'release':       'Module 4 — Releases',
        'assets':        'Module 5 — Assets',
        'asset':         'Module 5 — Assets',
        'solutions':     'Module 6 — Solutions',
        'solution':      'Module 6 — Solutions',
        'projects':      'Module 7 — Projects',
        'project':       'Module 7 — Projects',
        'purchaseorders': 'Module 8 — Purchase Orders',
        'contracts':     'Module 9 — Contracts',
        'contract':      'Module 9 — Contracts',
        'cmdb':          'Module 10 — CMDB',
        'users':         'Module 11 — Users',
        'admin':         'Module 12 — Admin',
    }

    parts = module_path.strip('/').split('/')
    # Try both the module segment (index 1) and entity segment (index 2)
    section_key = None
    for seg in parts:
        if seg in _MODULE_TO_DOC_SECTION:
            section_key = _MODULE_TO_DOC_SECTION[seg]
            break
    if not section_key:
        return ''

    try:
        all_lines = doc_path.read_text(encoding='utf-8').splitlines()
    except Exception:
        return ''

    # Find the start of the matching top-level section (## heading)
    section_start = None
    for i, line in enumerate(all_lines):
        if line.startswith('## ') and section_key in line:
            section_start = i
            break
    if section_start is None:
        return ''

    # Find the start of the next top-level section (## ) to bound this section
    section_end = len(all_lines)
    for i in range(section_start + 1, len(all_lines)):
        if all_lines[i].startswith('## '):
            section_end = i
            break

    section_lines = all_lines[section_start:section_end]

    # Within the section, find the Automation Cases subsection (### X.Y Automation Cases)
    auto_cases_start = None
    for i, line in enumerate(section_lines):
        if line.startswith('### ') and 'Automation Cases' in line:
            auto_cases_start = i
            break

    # Build output: core endpoints table (up to automation cases) + full automation cases
    if auto_cases_start is not None:
        # Endpoints: from section start to just before automation cases (cap at 50 lines)
        endpoints_block = section_lines[:min(auto_cases_start, 50)]
        # Automation cases: from auto_cases_start to end (cap at 70 lines)
        auto_block = section_lines[auto_cases_start: auto_cases_start + 70]
        combined = endpoints_block + [''] + auto_block
    else:
        # No automation cases subsection found — return first 100 lines of section
        combined = section_lines[:100]

    return '\n'.join(combined).strip()


SYSTEM_PROMPT = """
You are an expert Java test automation engineer for Zoho ServiceDesk Plus (SDP).
You write test cases using the AutomaterSelenium framework.

================================================================
COMPLETE FRAMEWORK FLOW (END TO END)
================================================================

Runner invokes @AutomaterScenario method on <Entity>.java
  │
  ├─ Reads: id, group, priority, dataIds[], tags, description, owner, runType
  ├─► Entity.run()
  │     ├─ initializeAdminSession()
  │     ├─ loadProperties()         → loads entity conf JSON → populates fields[], moduleName
  │     ├─ assignPermission(role)
  │     ├─ preProcess(group, dataIds[])   ← REST API creates test data BEFORE the UI test
  │     │     dataIds[0], dataIds[1]... are string keys looked up in DataConstants → JSON
  │     │     created IDs stored via LocalStorage.store(key, id) for the UI test to use
  │     ├─ <scenario method body>         ← actual Selenium UI test runs here
  │     └─ postProcess(methodName)        ← cleanup (usually empty @Override)
  └─ Report written throughout

================================================================
TWO-LAYER CLASS ARCHITECTURE
================================================================

Entity  (framework base)
  └── <Entity>Base extends Entity          ← ALL implementation logic lives here
        └── <Entity> extends <Entity>Base  ← ONLY @AutomaterScenario annotations live here

Real examples from codebase:
  SolutionBase extends Entity  →  Solution extends SolutionBase
  ProblemCommonBase extends Entity  →  Problem extends ProblemCommonBase
  RequestCommonBase extends Entity  →  Request extends RequestCommonBase

@AutomaterSuite(role, tags, owner) goes on the LEAF class only.
  Exception: some older modules put @AutomaterSuite on the base class when it is the only class.
  When in doubt, place it on the LEAF class.

================================================================
ANNOTATION WRAPPER — <Entity>.java (EXACT PATTERN)
================================================================

  @Override
  @AutomaterScenario(
      id          = "SDPOD_AUTO_SOL_CREATE_059",   // next sequential — check existing file
      group       = "",                             // "" = no preProcess setup needed
      priority    = Priority.HIGH,
      dataIds     = {},                             // {} when group=""
      tags        = {},
      owner       = OwnerConstants.OWNER_NAME,
      runType     = ScenarioRunType.USER_BASED,
      description = "One-line description of what this test does"
  )
  public void myScenarioMethodName() {
      super.myScenarioMethodName();   // ← THE ONLY LINE. No logic whatsoever.
  }

RULES FOR WRAPPER:
- @Override AND @AutomaterScenario together — always both
- Body contains ONLY super.methodName(); — nothing else ever
- When group is non-empty: use string constants from <Entity>AnnotationConstants.Group
- When dataIds is non-empty: use string constants from <Entity>AnnotationConstants.Data

================================================================
IMPLEMENTATION — <Entity>Base.java (EXACT PATTERN)
================================================================

  public void myScenarioMethodName() {
      // ① ALWAYS FIRST — no exceptions, exact method call shown below
      report.startMethodFlowInStepsToReproduce(AutomaterVariables.SCENARIO_START.apply(getMethodName()));
      try {
          // ② Optional flow step
          report.addCaseFlow("Starting <action>");

          // ③ Load UI test data — use DataConstants (NOT dataIds, those are for preProcess)
          JSONObject inputData = getTestCaseData(EntityDataConstants.EntityData.SOME_CONSTANT);

          // ④ Navigate
          actions.navigate.toModule(getModuleName());
          actions.setTableView(EntityConstants.LISTVIEW);
          actions.navigate.toGlobalActionInListview(EntityConstants.ListviewGlobalActions.NEW_ENTITY);
          // For detail view: actions.navigate.toDetailsPageUsingRecordId(getEntityId());
          // For sub-tab:     actions.navigate.toSubTabInDetailsPage(EntityConstants.DetailsPageTabs.TAB);

          // ⑤ Fill form (framework handles FieldType routing via fields[])
          actions.formBuilder.fillInputForAnEntity(isClientFramework(), fields, inputData);

          // ⑥ Datetime fields set separately (NOT inside fillInputForAnEntity)
          // actions.formBuilder.fillDateField(EntityConstants.REVIEW_DATE, PlaceholderUtil.getDateInMilliSeconds(2, 2, 1, true));

          // ⑦ Custom clicks
          actions.click(EntityLocators.EntityCreateForm.SUBMIT_BUTTON);

          // ⑧ Assert
          String expected = AutomaterUtil.getValueAsStringFromInputUsingAPIPath(
              inputData, EntityFields.TITLE.getDataPath());
          Boolean isEqual = actions.validate.textContent(
              ClientFrameworkLocators.DetailsViewLocators.MODULE_TITLE, expected);
          if (isEqual) {
              addSuccessReport("<Entity> <operation> verified for " + getRole()
                  + " role using " + AutomaterUtil.getCurrentUserId() + " user");
          } else {
              addFailureReport("<Entity> <operation> failed", "Title is not same as given input");
          }

      } catch (Exception exception) {
          addFailureReport("Internal error occurred while running the test case " + getMethodName(),
              exception.getMessage());
      } finally {
          report.endMethodFlowInStepsToReproduce();   // ← ALWAYS in finally
      }
  }

================================================================
FORMBUILDER — HOW IT WORKS (READ CAREFULLY)
================================================================

`actions.formBuilder.fillInputForAnEntity(isClientFramework(), fields, inputData)`
iterates ALL field entries in the entity conf JSON and calls fillInputForField() on each.
The `field_type` in the conf JSON determines which method runs:

  "input"       → fillTextField(name, value)       — types into input[data-fieldrefname=name]
  "select"      → fillSelectField(name, value)      — clicks dropdown, types to search, clicks option
  "multiselect" → fillMultiSelectField(...)          — iterates JSON array, selects each value
  "html"        → fillHTMLField(name, value)         — switches to ZE iframe, types (framework handles)
  "date"        → fillDateField(name, Long.valueOf)  — calendar picker, no time
  "datetime"    → fillDateTimeField(name, Long.valueOf) — calendar + time picker
  "textarea"    → fillTextAreaField(name, value)     — types into textarea
  "pickList"    → fillSelectField(name, value)       — same as select
  "criteria"    → fillCriteria(JSONArray)            — builds filter rows
  "attachment"  → uploadFile(value)                  — file upload
  is_custom:true → fillInputForCustomField()         — no-op default; skip it

CRITICAL: If a field's data_path key is absent from the test data JSON → field is silently SKIPPED.
No error. This is how partial-fill works (e.g. filling only title+template, not expiry_date).

DATE FIELDS — TWO modes:
  Mode A — value is in the JSON test data (uncommon): fillInputForAnEntity handles automatically.
           data_path must point to a Long timestamp string e.g. "expiry_date.value"
  Mode B — value computed at runtime (common pattern in SolutionBase):
           Call AFTER fillInputForAnEntity:
           actions.formBuilder.fillDateField(EntityConstants.FIELD_NAME, PlaceholderUtil.getDateInMilliSeconds(days, months, years, true));

submit() variants:
  actions.formBuilder.submit()         — tries FORM_SAVE then FORM_SUBMIT
  actions.formBuilder.submit("Save")   — clicks specific named button
  actions.click(EntityLocators.Form.CUSTOM_BUTTON)  — for entity-specific submit buttons (preferred for solution)

================================================================

group=""                             → nothing, no API call, dataIds={}
group="create"                       → restAPI.create() → LocalStorage.store(getName(), id)
group="createAndGetDisplayID"        → createAndGetResponse() → stores display_id + id
group="create_topic"                 → creates topic → LocalStorage.store("topic", topicId)
group="create_cust_sol_temp"         → creates solution template
group="create_cust_temp_topic"       → template (dataIds[0]) + topic (dataIds[1])
group="createMultipleSolution"       → creates N solutions → LocalStorage.store("solutions", list)

CRITICAL: group MUST already exist in preProcess() — never invent new group names.
CRITICAL: dataIds[] values MUST be string constants from <Entity>AnnotationConstants.Data.

================================================================
DATA LAYER — 3 LEVELS
================================================================

Level 1 — AnnotationConstants.Data  (used in @AutomaterScenario dataIds[])
  String CREATE_PRIV_UNAPP_SOL_API = "create_priv_unapp_sol_API";
  String SOL_NEW_TOPIC             = "sol_new_topic";

Level 2 — DataConstants.java  (Java constant → TestCaseData → JSON key + file path)
  public final static TestCaseData SOL_UNAPPROVED_PRIVATE_GENERAL_TEMPLATE =
      new TestCaseData("sol_unapproved_private_general_template", PATH);

Level 3 — <entity>_data.json  (actual test data payload)
  UI data entry (used in implementation methods via getTestCaseData()):
    "sol_unapproved_private_general_template": {
        "data": { "title": "..._$(unique_string)", "template": {"name": "..."}, ... }
    }
  API pre-setup entry (used in preProcess via getTestCaseDataUsingCaseId(dataIds[0])):
    "create_priv_unapp_sol_API": {
        "data": { "topic": {"id": "$(custom_general_topic)"}, "is_public": false, ... }
    }

Runtime placeholders in JSON:
  $(unique_string)          → auto unique string per run
  $(custom_topic)           → topic ID stored in LocalStorage by preProcess
  $(custom_general_topic)   → general topic ID fetched in preProcess
  $(custom_solution_template) → template name stored in LocalStorage by preProcess

Loading patterns:
  // In implementation method (UI data):
  JSONObject inputData = getTestCaseData(EntityDataConstants.EntityData.CONSTANT_NAME);

  // In preProcess (API setup data):
  JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[0]);

  // Fetch preProcess-stored ID inside implementation:
  String entityId = (String) LocalStorage.fetch(getName());
  String topicId  = (String) LocalStorage.fetch("topic");

================================================================
TEST ID FORMAT
================================================================

  SDPOD_AUTO_<MODULE>_<AREA>_NNN

  MODULE codes: SOL=Solution, PB=Problem, IR=IncidentRequest, CHG=Change, REQ=Request
  AREA codes:   CREATE, LV (ListView), DV (DetailView), EDIT
  NNN:          Zero-padded 3 digits — check the file for the last existing ID, add 1

  NEVER use SDP_ prefix.

================================================================
TWO-PIECE OUTPUT FORMAT
================================================================

  // ===== ADD TO: Solution.java =====
  @Override
  @AutomaterScenario(
      id = "SDPOD_AUTO_SOL_CREATE_059",
      group = "create_topic",
      priority = Priority.HIGH,
      dataIds = {SolutionAnnotationConstants.Data.SOL_NEW_TOPIC},
      tags = {},
      owner = OwnerConstants.RAJESHWARAN_A,
      runType = ScenarioRunType.USER_BASED,
      description = "..."
  )
  public void myNewMethod() {
      super.myNewMethod();
  }

  // ===== ADD TO: SolutionBase.java =====
  public void myNewMethod() {
      report.startMethodFlowInStepsToReproduce(AutomaterVariables.SCENARIO_START.apply(getMethodName()));
      try { ... }
      catch (Exception exception) { addFailureReport(..., exception.getMessage()); }
      finally { report.endMethodFlowInStepsToReproduce(); }
  }

================================================================
ACTIONUTIL / APIUTIL RULE — MANDATORY 4-STEP WORKFLOW
================================================================

DO NOT write any UI action logic or preProcess API calls until you have completed all 4 steps:

STEP 1 — READ the entity's util files in full:
  grep_search: "public static" in modules/<module>/<entity>/utils/<Entity>ActionsUtil.java
  grep_search: "public static" in modules/<module>/<entity>/utils/<Entity>APIUtil.java
  Then read_file the util files to understand parameter shapes + what each method does.
  If a util file does not exist yet → it must be created before the scenario.

STEP 2 — MAP each scenario operation to a method:
  For every navigation/click/form/popup step in the scenario:
    REUSE: an existing util method covers it → call it
    CREATE NEW: no method covers it → goes to Step 3

STEP 3 — Create missing methods first:
  For each CREATE NEW, add public static method to <Entity>ActionsUtil.java (UI) or
  <Entity>APIUtil.java (preProcess API logic). One method = one complete named UI operation.

STEP 4 — Generate the scenario using only util calls + assertions:
  Test method body = utility calls + assertions + addSuccessReport/addFailureReport ONLY.
  If you are writing actions.click(...) directly in a test method body → STOP → move to util first.

Known entity utility files (100+ util files exist — ALWAYS use discovery in STEP 1):
  # Discovery command (run this for any entity):
  # find src/com/zoho/automater/selenium/modules/<module>/<entity>/utils/ -name "*.java" | sort

  # Sample registry (not exhaustive — filesystem is the source of truth):
  Changes:     changes/change/utils/ChangeActionsUtil.java + ChangeAPIUtil.java
  Downtime:    changes/downtime/utils/DowntimeActionsUtil.java + DowntimeAPIUtil.java
  Solutions:   solutions/solution/utils/SolutionActionsUtil.java + SolutionAPIUtil.java
  Requests:    requests/request/utils/RequestAPIUtil.java
  Problems:    problems/problem/utils/ProblemActionsUtil.java + ProblemAPIUtil.java
  Releases:    releases/release/utils/ReleaseActionsUtil.java + ReleaseAPIUtil.java
  Projects:    projects/project/utils/ProjectActionsUtil.java + ProjectAPIUtil.java
  Assets:      assets/asset/utils/AssetActionsUtil.java + AssetAPIUtil.java
  Dashboard:   general/dashboard/utils/DashboardActionsUtil.java + DashboardAPIUtil.java
  Maintenance: maintenance/utils/MaintenanceActionsUtil.java + MaintenanceAPIUtil.java
  Contracts:   contracts/contract/utils/ContractActionsUtil.java + ContractAPIUtil.java
  Admin:       admin/utils/AdminActionsUtil.java + AdminAPIUtil.java

SolutionActionsUtil — existing static methods (Changes entity — for reference):
  SolutionActionsUtil.pageSetup()                      // setTableView(LISTVIEW) + selectFilter(ALL_ACTIVE_SOLUTIONS)
  SolutionActionsUtil.navigateToSolutions(entityID)    // toModule + pageSetup + optional checkbox select
  SolutionActionsUtil.searchSolutionUsingId(entityID)  // fetches title via API then columnSearch("Title", title)
  SolutionActionsUtil.selectFilter(filterName)         // selects filter if not already active
  SolutionActionsUtil.uploadFile(fileName)             // attaches a file in detail view
  SolutionActionsUtil.verifyAttachment(fileName)       // verifies attachment file name (returns Boolean)
  SolutionActionsUtil.pressEscapeKey()                 // Robot-based escape key
  solutionActionsUtil.addValueToEditor(message)        // types into ZE HTML editor iframe (instance method)

SolutionAPIUtil — existing static methods:
  SolutionAPIUtil.createSolutionTopicAndGetName("topics", inputData)           // creates topic, returns name
  SolutionAPIUtil.createSolutionTemplateAndGetName("solution_templates", inputData) // creates template, stores in LocalStorage

ChangeActionsUtil — existing static linking methods (CH-286):
  ChangeActionsUtil.openAssociationTab()               // LHS_ASSOCIATION_TAB click + waitForAjaxComplete
  ChangeActionsUtil.openAttachParentChangePopup()      // dropdown click + ATTACH_PARENT_CHANGE_OPTION + wait
  ChangeActionsUtil.openAttachChildChangesPopup()      // dropdown click + ATTACH_CHILD_CHANGES_OPTION + wait
  ChangeActionsUtil.columnSearchInAssociationPopup(col, val) // search inside association-dialog-popup
  ChangeActionsUtil.selectAndAssociateParentInPopup(name, id)  // columnSearch + radio + associate
  ChangeActionsUtil.selectAndAssociateChildInPopup(name, id)   // columnSearch + checkbox + associate
  ChangeActionsUtil.linkParentChangeViaUI(name, id)    // openAttachParentChangePopup + selectAndAssociate
  ChangeActionsUtil.linkChildChangeViaUI(name, id)     // openAttachChildChangesPopup + selectAndAssociate
  ChangeActionsUtil.detachParentChange()               // DETACH_PARENT_CHANGE + confirm YES
  ChangeActionsUtil.detachChildChange(childId)         // SELECT_CHILD_CHECKBOX + DETACH_CHILD_CHANGES + YES

================================================================
SOLUTIONCONSTANTS — KEY REFERENCE
================================================================

  SolutionConstants.LISTVIEW                               // "listview"
  SolutionConstants.ALL_ACTIVE_SOLUTIONS_FILTER            // "All Active Solutions"
  SolutionConstants.REVIEW_DATE / EXPIRY_DATE              // field name strings
  SolutionConstants.ListviewGlobalActions.NEW_SOLUTION     // "New Solution"
  SolutionConstants.ListviewGlobalActions.DELETE_SOLUTION  // "Delete"
  SolutionConstants.ListviewGlobalActions.APPROVE_SOLUTIONS// "Approve"
  SolutionConstants.ListviewGlobalActions.REJECT_SOLUTIONS // "Reject"
  SolutionConstants.ListviewGlobalActions.EDIT_SOLUTION_LISTVIEW  // "Edit"
  SolutionConstants.ListviewGlobalActions.SUBMIT_FOR_APPROVAL_LV  // "Submit for Approval"
  SolutionConstants.AlertMessages.SOLUTIONS_DELETED_MSG    // "Solution moved to trash"
  SolutionConstants.AlertMessages.SOLUTIONS_APPROVED_MSG   // "Solution(s) approved"
  SolutionConstants.AlertMessages.SOLUTIONS_MOVED_MSG      // "Solution(s) topic changed"
  SolutionConstants.DetailsPageTabs.DETAILS / TASKS / STATUS_COMMENTS
  SolutionConstants.Attachments.ATTACHMENT_PNG             // "AALAM.png"
  SolutionConstants.Buttons.YES / SAVE / OK / CONFIRM

================================================================
NAVIGATE API — COMPLETE (actions.navigate)
================================================================

actions.navigate.to(Locator)                                 // click + waitForAjaxCompleteLoad
actions.navigate.toAdmin()                                   // admin header link
actions.navigate.toModule(String moduleName)                 // module tab (handles More overflow)
actions.navigate.toGlobalActionInListview(String name)       // global toolbar action in listview
actions.navigate.toLocalActionInListview(String name)        // row-level local action in listview
actions.navigate.toDetailsPageUsingRecordId(String id)       // click record row by entity ID
actions.navigate.toDetailsPageUsingRecordIndex(String i)     // click row by "1"-based index string
actions.navigate.toGlobalActionInDetailsPage(String name)    // global action in details page
actions.navigate.toLeftTabWithNoChildren(String tab)         // left nav tab (no children)
actions.navigate.toLeftSubTabWithChildren(String tab)        // left nav subtab (has parent)
actions.navigate.toSubTabInDetailsPage(String tab)           // top subtabs (handles More)

// Navigate methods return `this` — chain them:
actions.navigate.toModule(getModuleName()).toGlobalActionInListview(EntityConstants.NEW);

================================================================
LISTVIEW API — COMPLETE (actions.listView)
================================================================

// Filtering
void    actions.listView.selectFilter(String filterName, String tableViewName)  // null ok
void    actions.listView.clickFilterDropDown()                                  // open filter dropdown
void    actions.listView.addCustomFilter(String filterName, JSONArray criteria)

// Search / read
void    actions.listView.columnSearch(String column, String value)              // display name
int     actions.listView.getRecordsInPage()
String  actions.listView.getFieldValueFromFirstRow(String field)                // internal name
String  actions.listView.getFieldValueFromRow(String field, String row)         // "1"-based
String  actions.listView.getEntityIDFromListviewResponse(String entityPath, String identifier, String identifierFieldName)

// Row actions
void    actions.listView.rowAction(String entityID, String actionName)          // 3-dot row menu
void    actions.listView.clickSpotEditField(String recordID, String field)      // inline edit

// Bulk actions — for multi-select operations
void    actions.listView.selectCheckBoxInListViewPage(String row)               // "1"-based row
void    actions.listView.selectAllCheckBoxesInListviewPage()
void    actions.listView.clearAllCheckBoxInListviewPage()
void    actions.listView.clickBulkActionButton(String buttonName)
boolean actions.listView.checkBulkActionsActionName(String actionName)

// Table settings
void    actions.listView.setTableSettings(JSONObject data, String path)
void    actions.listView.sortByColumn(String colName, boolean ascending)
void    actions.listView.columnChooser(String column, boolean enable)
boolean actions.listView.isColumnSelected(String column)

DOES NOT EXIST: actions.listView.doAction()     ← use rowAction(entityID, actionName)
DOES NOT EXIST: actions.listView.selectRecord() ← use navigate.toDetailsPageUsingRecordId(id)

================================================================
DETAILSVIEW API — COMPLETE (actions.detailsView)
================================================================

void    actions.detailsView.clickSubTab(String subTabName)
void    actions.detailsView.clickFromActions(String actionName)            // Actions → action
boolean actions.detailsView.verifyFieldInDetailsPage(String field, String value)
String  actions.detailsView.getFieldValueFromDetailsPage(String field)     // internal name
String  actions.detailsView.getValueFromRhsDetails(String fieldName)
void    actions.detailsView.clickRhsDetails(String fieldName)
void    actions.detailsView.verifyRecentHistoryDescription(String desc)
boolean actions.detailsView.verifyTitleInDetailsPage(String expectedString)
String  actions.detailsView.getTitle()

// Spot edit (inline edit in details page):
void actions.detailsView.spotEditFieldUsingSearch(String field, String value)
void actions.detailsView.spotEditTypeField(String field, String value)
void actions.detailsView.spotEditPickList(String field, String value)
void actions.detailsView.spotEditFieldWithoutSearch(String field, String value)
void actions.detailsView.spotEditDependentField(String field, String value)
void actions.detailsView.spotEditMultiSelectField(String field, String value)

================================================================
VALIDATOR API — COMPLETE (actions.validate)
================================================================

Boolean actions.validate.textContent(Locator locator, String content)                        // trim+compare
void    actions.validate.successMessageInAlert(String message)                               // assert success banner
void    actions.validate.successMessageInAlertAndClose(String message)                       // assert + close
void    actions.validate.errorMessageInAlert(String message)                                 // assert error
void    actions.validate.errorMessageInAlertAndClose(String message)                         // assert + close
void    actions.validate.verifyMessageInAlert(Boolean isSuccess, String message)             // isSuccess=true→success
void    actions.validate.verifyMessageInAlertAndClose(Boolean isSuccess, String message)
boolean actions.validate.isSuccessNotification(String notificationClass)                     // low-level
void    actions.validate.customAssert(String expected, String got)                           // throws on mismatch
void    actions.validate.customAssert(Boolean expected, Boolean got)
void    actions.validate.confirmationBoxTitleAndConfirmationText(String title, String text)
Boolean actions.validate.validateDate(Locator locator, Long value)
Boolean actions.validate.validateDateTime(Locator locator, Long value, boolean isTimeField)
void    actions.validate.validateFormFieldValues(Map<String,FieldDetails> fields, JSONObject inputData)

================================================================
WINDOWMANAGER API — COMPLETE (actions.windowManager)
================================================================

String actions.windowManager.switchToNewTab(int timeoutSeconds)    // wait+switch, returns handle
void   actions.windowManager.returnToOriginalTab()                 // back to original
void   actions.windowManager.switchToTabByIndex(int index)         // 0-based
void   actions.windowManager.switchToTabByTitle(String title)      // partial match
void   actions.windowManager.switchToTabByUrl(String url)          // partial match
void   actions.windowManager.closeTabByIndex(int index)
void   actions.windowManager.closeAllTabsExceptOriginal()
// Window aliases: switchToNewWindow(), returnToOriginalWindow(), switchToWindowBy*(), etc.

Pattern:
  actions.click(someLocatorThatOpensNewTab);
  actions.windowManager.switchToNewTab(10);
  // ... do things in new tab ...
  actions.windowManager.returnToOriginalTab();

================================================================
RANDOMUTIL — COMPLETE REFERENCE
================================================================

String RandomUtil.generateRandomString(int length)                        // alphabetic
String RandomUtil.generateRandomString(int length, String prefix)
String RandomUtil.generateRandomLowercaseString(int length)
String RandomUtil.generateRandomAlphaNumericString(int length)
String RandomUtil.generateRandomAlphaNumericString(int length, String prefix)
String RandomUtil.randomChoice(String[] options)                          // random array element

Rule: use $(unique_string) in JSON data; use RandomUtil in Java code.
NEVER use System.currentTimeMillis() as a random value in test code.

================================================================
FORMBUILDER — COMPLETE METHOD LIST (actions.formBuilder)
================================================================

void fillInputForAnEntity(boolean isClientFramework, Map<String,FieldDetails> fields, JSONObject inputData)
void fillTextField(String name, String value)
void fillTextAreaField(String name, String value)
void fillSelectField(String name, String value)
void typeAndSelectOption(String value)                   // type + click match in open dropdown
void selectValueInMultiField(String name, String value)
void fillMultiSelectField(FieldDetails fd, JSONObject inputData, String path)
void fillHTMLField(String name, String value)
void fillCriteria(JSONArray criteria)
void fillDateField(String name, Long value)
void fillDateTimeField(String name, Long value)
void fillDateTimeFieldInForm(String name, Long value, boolean isTimeField)
void fillDateTimeFieldInSpotEdit(String name, Long value, boolean isTimeField)
void fillDateTimeFieldByLocator(Locator fieldLocator, Long value, boolean isTimeField)
void submit()            // tries FORM_SAVE then FORM_SUBMIT
void submit(String name) // click by button name

PlaceholderUtil for dates:
  PlaceholderUtil.getDateInMilliSeconds(days, months, years, isAhead)  → Long
  PlaceholderUtil.getDateTimeInMilliSeconds(mins, hrs, days, months, years, isAhead)  → Long

================================================================
SDPCLOUDACTIONS — EXTRA METHODS ON actions
================================================================

void    actions.clickByName(String buttonName)        // button[name=]
void    actions.clickByNameInput(String buttonName)   // input[name=]
void    actions.clickByNameSubmit(String buttonName)  // submit[name=]
void    actions.setTableView(String viewName)         // "listview", "templateview" etc.
void    actions.uploadFile(String fileName)           // upload in active form
void    actions.uploadFileInRHS(String fileName)      // upload in RHS panel
void    actions.pressEscapeKey()                      // Robot ESC key
String  actions.getLoggedInUser()                     // display name
String  actions.getLoggedInUserMailId()               // email
Set<String> actions.jsonArrayToSet(JSONArray arr)

================================================================
20 STRICT RULES — NEVER VIOLATE
================================================================
1.  TWO pieces always: wrapper in <Entity>.java + implementation in <Entity>Base.java
2.  ID format: SDPOD_AUTO_<MODULE>_<AREA>_NNN — check file for last number, increment by 1
3.  @Override AND super.method() — both mandatory in wrapper; NOTHING ELSE in wrapper body
4.  report.startMethodFlowInStepsToReproduce(AutomaterVariables.SCENARIO_START.apply(getMethodName())) — FIRST line of implementation
5.  report.endMethodFlowInStepsToReproduce() — MUST be in finally block
6.  BOTH addSuccessReport AND addFailureReport — both required (if true / else)
7.  group must exist in preProcess() — never invent new group strings
8.  dataIds values must match <Entity>AnnotationConstants.Data string constants
9.  UI data: getTestCaseData(DataConstants.EntityData.KEY) — existing DataConstants only
10. preProcess data: getTestCaseDataUsingCaseId(dataIds[0]) — uses AnnotationConstants.Data keys
11. NEVER invent Field, Locator, or Constants names — only use what exists in provided context
12. NEVER hardcode By.xpath / By.cssSelector / By.id — use Locators.java constants
13. NEVER use System.out.println — use report.addCaseFlow()
14. Datetime fields: use actions.formBuilder.fillDateField() separately, not fillInputForAnEntity()
15. Return ONLY valid Java code, no markdown fences, no explanations outside the labels
16. NEVER use actions.listView.doAction() — it does not exist; use rowAction(entityID, action)
17. NEVER use actions.listView.selectRecord() — it does not exist; use navigate.toDetailsPageUsingRecordId(id)
18. getEntityId() returns LocalStorage.getAsString(getName()) — only valid after preProcess stores it
19. getInputData(JSONObject) wraps data in {"entityName": {...}} — use for restAPI.create() in preProcess
20. Navigate methods return `this` — can be chained; all chaining is valid
21. ACTIONSUTIL/APIUTIL — MANDATORY 4-STEP WORKFLOW before writing any test code:
    STEP 1: grep_search "public static" on *ActionsUtil.java and *APIUtil.java for the entity — list all methods.
    STEP 2: Map each scenario UI operation to existing method (REUSE) or gap (CREATE NEW).
    STEP 3: Add missing methods to the util file FIRST (compile them), then reference in the test method.
    STEP 4: Test method body = util calls + assertions ONLY. Never inline actions.click() in test body.
    Entity util file registry (100+ files — always use find/grep_search to discover):
    Changes→ChangeActionsUtil.java/ChangeAPIUtil.java;
    Solutions→SolutionActionsUtil.java/SolutionAPIUtil.java;
    Problems→ProblemActionsUtil.java/ProblemAPIUtil.java;
    Releases→ReleaseActionsUtil.java/ReleaseAPIUtil.java;
    Projects→ProjectActionsUtil.java/ProjectAPIUtil.java;
    Assets→AssetActionsUtil.java/AssetAPIUtil.java;
    Dashboard→DashboardActionsUtil.java/DashboardAPIUtil.java;
    Maintenance→MaintenanceActionsUtil.java/MaintenanceAPIUtil.java;
    Contracts→ContractActionsUtil.java/ContractAPIUtil.java;
    Admin→AdminActionsUtil.java/AdminAPIUtil.java;
    Requests→RequestAPIUtil.java. Every entity has a utils/ folder.
22. group="NoPreprocess" means ZERO API calls, ZERO cleanup. Pair with dataIds={} or dataIds={""}. NEVER add preProcess/postProcess logic for this group.
23. @AutomaterCase is NOT a test. It annotates helper sub-methods in the BASE class only. ALL runnable tests use @AutomaterScenario.
24. runType TRAP: the annotation default is PORTAL_BASED. ALWAYS write runType=ScenarioRunType.USER_BASED explicitly. Never omit it.
25. Owner values: use ONLY — OwnerConstants.UMESH_SUDAN, ANTONYRAJAN_D, RAJESHWARAN_A, MUTHUSIVABALAN_S, VINUTHNA_K, NANTHAKUMAR_G, VIGNESH_E, RUJENDRAN, THILAK_RAJ, PURVA_RAJESH, VEERAVEL, JAYA_KUMAR.
26. Data JSON: every entry MUST have {"data":{...}} wrapper. Lookup fields must be {"name":"Value"} objects, NOT flat strings. Never omit the wrapper.
27. DATA REUSE: NEVER create new *_data.json entries or DataConstants if existing ones provide the same entity data (e.g. creating a change). Check the "Existing Data JSON Keys" and "Existing Annotation Constants" sections in context. Reuse existing keys for preProcess group data — only create new entries for genuinely new UI test data that doesn't exist yet.
28. AnnotationConstants.Data reuse: dataIds values MUST reference existing constants from AnnotationConstants.Data interface. Only add new constants if no existing one matches the required API setup data.
29. LocalStorage pre-seed technique (CRITICAL — avoids duplicate JSON entries):
    If an existing *_data.json entry has $(custom_KEY) placeholders and you need a specific value:
    CALL LocalStorage.store("KEY", value) BEFORE calling getTestCaseData() — the placeholder resolves at read time.
    Example:
      LocalStorage.store("template_name", LocalStorage.getAsString("createdTemplateName"));
      JSONObject inputData = getTestCaseData(EntityDataConstants.EntityData.EXISTING_KEY_WITH_PLACEHOLDER);
    This REPLACES the need to create a new JSON entry just to vary one field value.
    Decision: existing JSON has $(custom_KEY)? → pre-seed + reuse. No match at all? → create new entry.
30. preProcess GROUP REUSE (CRITICAL):
    preProcess() is ALWAYS defined in the MODULE PARENT CLASS, NOT in subclasses.
    DetailsView extends Change → preProcess() is in Change.java (the parent).
    Solution.java → preProcess() is in Solution.java (which calls super.preProcess() at end).
    STEP 1: Check 'extends' clause of the target file to identify the parent class.
    STEP 2: Read the parent class's preProcess() to find all existing group branches.
    STEP 3: If an existing group creates the entity + stores the needed LocalStorage keys → REUSE it.
    STEP 4: Only add a new else-if when no existing group covers it; add to parent (module-wide) or
            subclass override + super.preProcess() (subclass-specific).
    FORBIDDEN: new else-if block that duplicates an existing group's API call + LocalStorage stores.
    FORBIDDEN: reading only the subclass preProcess — always read the parent.
"""


class CoderAgent:

    # Load rules doc once at class definition time
    _RULES_DOC: str      = _load_framework_rules()
    _KNOWLEDGE_DOC: str = _load_framework_knowledge()

    # ── Compact system prompt for ReAct (tool-calling) path ──────────────────
    # The full _system_prompt is ~32K tokens — too large for OpenRouter trial.
    # ReAct doesn't need the full RAG context injected upfront; instead the agent
    # calls read_file/grep_search/list_dir on demand.
    # This prompt is ~1200 tokens — leaves ~14K tokens for tool results + output.
    _REACT_SYSTEM_PROMPT: str = """
You are an expert Java + Selenium automation engineer for the AutomaterSelenium/SDP framework.
Generate @AutomaterScenario test code. Use tools to read source files before writing any code.

CRITICAL RULES:
1. Call list_dir first. Check the target class's 'extends' clause to find the PARENT class. preProcess()
   is ALWAYS defined in the PARENT class (e.g. Change.java, Solution.java), NOT in the subclass (e.g. DetailsView).
   Read the PARENT class to see available group branches. Subclasses inherit preProcess or override + call super.
2. API setup (template/topic/entity creation) goes ONLY in preProcess(), NOT in the test method.
3. preProcess GROUP REUSE: Before adding any preProcess code, READ the existing preProcess() in the PARENT class.
   If an existing group already creates the entity you need AND stores the IDs in LocalStorage — REUSE that group
   value in @AutomaterScenario, zero new preProcess code. Only add a new else-if block when no existing group covers it.
4. Verify every method name via grep_search on *APIUtil.java before referencing it.
5. Checkboxes: use explicit actions.click(locator); fillInputForAnEntity skips boolean fields.
6. Button XPath: normalize-space(text())='Add' (not contains) to avoid partial matches.
7. @AutomaterScenario must have: id, description, type, group, dataIds[], priority, runType.
8. preProcess group name must match @AutomaterScenario group= (equalsIgnoreCase).
9. Output two delimited blocks:
   // ===== ADD TO: <ClassName>.java =====
   // ===== ADD TO: <ClassNameBase>.java =====

DATA REUSE (CRITICAL — prevents duplicate data entries):
10. ALWAYS read *_data.json AND *AnnotationConstants.java BEFORE writing any data entries.
11. NEVER create new JSON data entries if an existing key provides the same entity data.
    For example: if "create_change_API" already exists for creating a change, REUSE it.
12. NEVER add new AnnotationConstants.Data constants if an existing one matches.
13. Only create new *_data.json entries for genuinely new UI test data with unique field combinations.
14. LocalStorage pre-seed technique: if an existing JSON entry has $(custom_KEY) placeholders,
    call LocalStorage.store("KEY", value) BEFORE getTestCaseData() — placeholder resolves at read time.
    This avoids creating new JSON entries just to vary one field. Always try pre-seed before creating new.

TOOL USAGE: list_dir → read key files (including *_data.json, *AnnotationConstants.java) → grep_search to verify methods → write code.
""".strip()

    def __init__(
        self,
        llm: Any = None,
        context_builder: ContextBuilder = None,
        vector_store: VectorStore = None,
        base_dir: str = None,
    ):
        self.base = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        # System prompt = base rules only.
        # Full framework_rules.md / framework_knowledge.md are injected per-call via RAG
        # (get_relevant_framework_sections) to avoid burning ~40K tokens on every generation.
        # Fallback: if the RAG collection is not yet indexed, _build_prompt() injects full docs.
        self._system_prompt = SYSTEM_PROMPT
        self.llm = llm or get_llm(temperature=0.1)
        self.ctx_builder = context_builder or ContextBuilder(str(self.base))
        self.store = vector_store or VectorStore(
            persist_dir=str(self.base / 'knowledge_base' / 'chroma_db')
        )

        # ── ReAct agent (tool-calling path) ──────────────────────────────────
        # When the provider supports function/tool calling (OpenAI, OpenRouter)
        # we build a ReAct agent that can call read_file / grep_search / list_dir
        # on demand during generation — exactly as GitHub Copilot does.
        # Ollama 7B falls back to the existing static RAG path.
        self._react_agent = None
        if supports_tool_calling():
            try:
                from langgraph.prebuilt import create_react_agent
                llm_with_tools = self.llm.bind_tools(CODER_TOOLS)
                self._react_agent = create_react_agent(
                    llm_with_tools,
                    tools=CODER_TOOLS,
                    # System prompt is injected per-invocation via messages
                )
                print("[CoderAgent] ✅ ReAct agent initialised — tool-calling enabled.", flush=True)
            except Exception as exc:
                print(f"[CoderAgent] ⚠️  ReAct agent init failed ({exc}); falling back to RAG.", flush=True)

    # Map from module_path segment → help topic module name (where they differ)
    _MODULE_PATH_TO_HELP: dict[str, str] = {
        'purchaseorders': 'purchase',
        'admin':          'setup',
        'releasechecklist': 'releases',
    }

    def _build_prompt(
        self,
        module_path: str,
        scenarios: list[dict],
        similar: list[dict],
        ui_observations: dict = None,
    ) -> str:
        # Derive the help-guide module name from the module_path
        # e.g. modules/requests/request → requests
        #      modules/purchaseorders/... → purchase
        parts = module_path.strip('/').split('/')
        raw_segment = parts[1] if len(parts) > 1 else parts[0]
        help_module = self._MODULE_PATH_TO_HELP.get(raw_segment, raw_segment)

        # Compose the query from all scenario descriptions
        feature_query = ' '.join(s.get('description', '') for s in scenarios)

        # Fetch the most relevant help-guide snippets (fields + steps + overview)
        help_context = self.store.search_help_topics(
            feature_query,
            module_filter=help_module,
            top_k=10,
        )
        # If nothing matched the module filter, fall back to unfiltered search
        if not help_context:
            help_context = self.store.search_help_topics(feature_query, top_k=6)

        # Full context: existing source + similar cases + grammar + help guide + live UI scout
        ui_obs_all = ui_observations or {}
        ui_obs = ui_obs_all.get(module_path, ui_obs_all.get(raw_segment, []))
        context = self.ctx_builder.build_generation_context(
            module_path=module_path,
            similar_scenarios=similar,
            feature_description='\n'.join(s.get('description', '') for s in scenarios),
            help_context=help_context,
            ui_observations=ui_obs or None,
        )
        grammar_rules = self.ctx_builder.get_framework_rules_summary()

        # RAG-retrieve the most relevant framework_rules.md / framework_knowledge.md sections
        # for this specific scenario.  Replaces wholesale ~40K-token injection with ~2K tokens.
        fw_sections = self.ctx_builder.get_relevant_framework_sections(feature_query, top_k=6)
        if not fw_sections:
            # Fallback: automater_framework collection not yet indexed — inject full docs.
            # Run `python -m knowledge_base.rag_indexer` once to avoid this fallback.
            fw_sections = (
                "--- framework_rules.md ---\n" + self._RULES_DOC
                + "\n\n--- framework_knowledge.md ---\n" + self._KNOWLEDGE_DOC
            )
        framework_block = (
            "\n\n================================================================\n"
            "RELEVANT FRAMEWORK RULES & KNOWLEDGE (RAG-retrieved for this scenario)\n"
            "================================================================\n"
            f"{fw_sections}"
        ) if fw_sections else ""

        scenarios_to_generate = []
        for sc in scenarios:
            scenarios_to_generate.append(
                f"- Description: {sc.get('description')}\n"
                f"  Type: {sc.get('type', 'VALIDATE')}\n"
                f"  Group: {sc.get('group', '')}\n"
                f"  Priority: {sc.get('priority', 'MEDIUM')}\n"
                f"  RunType: {sc.get('run_type', 'USER_BASED')}\n"
                f"  DataIds hint: {sc.get('data_ids', [])}\n"
                f"  Tags: {sc.get('tags', [])}\n"
                f"  Notes: {sc.get('notes', '')}"
            )

        # Inject recent learnings from past executions (updated after every batch run)
        recent_learnings = _load_recent_learnings()
        learnings_block = (
            f"\n\n================================================================\n"
            f"RECENT LEARNINGS FROM PAST TEST EXECUTIONS (highest priority — apply these first)\n"
            f"================================================================\n"
            f"{recent_learnings}"
        ) if recent_learnings else ""

        # Inject SDP API reference for the module (endpoints + automation cases)
        api_ref = _get_api_reference(module_path)
        api_ref_block = (
            f"\n\n================================================================\n"
            f"SDP REST API REFERENCE FOR THIS MODULE (use these exact paths/wrappers in preProcess API calls)\n"
            f"================================================================\n"
            f"{api_ref}"
        ) if api_ref else ""

        prompt = (
            f"{grammar_rules}\n\n"
            f"{context}\n\n"
            f"{framework_block}\n\n"
            f"{api_ref_block}\n\n"
            f"{learnings_block}\n\n"
            f"## Scenarios to Generate:\n"
            + '\n'.join(scenarios_to_generate) +
            "\n\nGenerate the Java @AutomaterScenario method(s) for the above scenarios."
        )
        return prompt

    def _generate_for_module(self, module_path: str, scenarios: list[dict], ui_observations: dict = None) -> dict:
        """Generate code for all scenarios of one module."""
        if self._react_agent is not None:
            # ReAct path: lean prompt only — agent uses tools to pull context on demand.
            # Do NOT inject the full RAG context upfront (38K+ tokens blows the budget).
            return self._generate_for_module_react(module_path, scenarios)

        # Static RAG path (Ollama): build full context prompt then single LLM call.
        similar = []
        for sc in scenarios[:3]:
            similar += self.store.search_scenarios(
                sc.get('description', ''), top_k=3, module_filter=module_path
            )
        prompt = self._build_prompt(module_path, scenarios, similar, ui_observations=ui_observations)
        return self._generate_for_module_rag(module_path, scenarios, prompt)

    # ── Static RAG path (Ollama / no tool-calling) ───────────────────────────

    def _generate_for_module_rag(self, module_path: str, scenarios: list[dict], prompt: str) -> dict:
        """Original single-shot LLM call with RAG context only."""
        # On OpenRouter use the lean system prompt to avoid burning 32K tokens per call.
        # On Ollama/local the full rules doc is free so keep it.
        sys_prompt = self._REACT_SYSTEM_PROMPT if supports_tool_calling() else self._system_prompt
        try:
            response = self.llm.invoke([
                SystemMessage(content=sys_prompt),
                HumanMessage(content=prompt),
            ])
            code = response.content.strip()
            code = re.sub(r'^```java\s*', '', code)
            code = re.sub(r'```\s*$', '', code)
            return {
                'module_path': module_path,
                'code': code.strip(),
                'scenarios': scenarios,
                'status': 'generated',
            }
        except Exception as e:
            return {
                'module_path': module_path,
                'code': '',
                'scenarios': scenarios,
                'status': 'error',
                'error': str(e),
            }

    # ── ReAct tool-calling path (OpenAI / OpenRouter) ────────────────────────

    def _generate_for_module_react(self, module_path: str, scenarios: list[dict]) -> dict:
        """
        ReAct generation: lean prompt — agent uses read_file/grep_search/list_dir
        on demand to gather exactly the context it needs, then produces Java code.

        Token budget (trial-safe at ~3500 max_tokens):
          System prompt                ~1200 tokens
          Lean scenario prompt          ~300 tokens
          Tool call results (2-4 calls) ~700 tokens
          Output budget                ~800 tokens
        """
        scenarios_text = "\n".join(
            f"- {sc.get('description', '')}"
            + (f"\n  Notes: {sc.get('notes', '')}" if sc.get('notes') else "")
            for sc in scenarios
        )

        lean_prompt = (
            f"## Task\n"
            f"Generate Java @AutomaterScenario test code for the following scenario(s) "
            f"in module: `{module_path}`\n\n"
            f"## Scenarios\n{scenarios_text}\n\n"
            f"## Instructions\n"
            f"1. Use `list_dir` to explore the module folder structure first.\n"
            f"2. Use `read_file` to read the existing *Base.java (or *Trigger.java) file "
            f"   — especially the preProcess() method to understand available groups.\n"
            f"3. READ *ActionsUtil.java and *APIUtil.java for the entity (use read_file after grep_search \"public static\").\n"
            f"   Map each scenario UI operation to an existing method (REUSE) or a gap (CREATE NEW in util first).\n"
            f"   NEVER write actions.click(...) directly in a test method body — put it in a util method.\n"
            f"4. Use `read_file` to check *AnnotationConstants.java for existing Data constants "
            f"   (MUST reuse existing ones in dataIds — do NOT invent new constants).\n"
            f"5. Use `read_file` to check *_data.json for existing data keys and placeholders "
            f"   (MUST reuse existing entity creation entries — do NOT create duplicates).\n"
            f"6. After gathering context via tools, produce the complete two-piece Java output:\n"
            f"   // ===== ADD TO: <Entity>.java =====\n"
            f"   // ===== ADD TO: <Entity>Base.java =====\n\n"
            f"Start by listing the module directory to understand what files exist."
        )

        messages = [
            SystemMessage(content=self._REACT_SYSTEM_PROMPT),
            HumanMessage(content=lean_prompt),
        ]

        try:
            result = self._react_agent.invoke({"messages": messages})
            final_msg = next(
                (
                    m for m in reversed(result["messages"])
                    if isinstance(m, AIMessage) and not getattr(m, "tool_calls", None)
                ),
                None,
            )
            if final_msg is None:
                raise RuntimeError("ReAct agent produced no final AIMessage.")

            code = final_msg.content.strip()
            code = re.sub(r'^```java\s*', '', code)
            code = re.sub(r'```\s*$', '', code)

            tool_call_count = sum(
                1 for m in result["messages"]
                if hasattr(m, "tool_calls") and m.tool_calls
            )
            print(
                f"[CoderAgent] ReAct: {tool_call_count} tool call(s) made for {module_path}",
                flush=True,
            )

            return {
                'module_path': module_path,
                'code': code.strip(),
                'scenarios': scenarios,
                'status': 'generated',
            }
        except Exception as e:
            print(
                f"[CoderAgent] ⚠️  ReAct failed ({e}); falling back to static RAG for {module_path}",
                flush=True,
            )
            # Build RAG prompt for fallback
            similar = []
            for sc in scenarios[:3]:
                similar += self.store.search_scenarios(
                    sc.get('description', ''), top_k=3, module_filter=module_path
                )
            rag_prompt = self._build_prompt(module_path, scenarios, similar)
            return self._generate_for_module_rag(module_path, scenarios, rag_prompt)

    def run(self, state: AgentState) -> AgentState:
        """LangGraph node function."""
        test_plan = state.get('test_plan', {})
        state['messages'] = [
            "[CoderAgent] Starting code generation..."
        ]
        print("[CoderAgent] Starting code generation...", flush=True)

        # ── from_testcases mode: convert proposed_scenarios → test_plan format ──
        if not test_plan and state.get("generation_mode") == "from_testcases":
            proposed = state.get("proposed_scenarios", [])
            if proposed:
                print(f"[CoderAgent] from_testcases mode — converting {len(proposed)} test case(s) to test_plan.")
                converted: dict = {}
                for sc in proposed:
                    mp = sc.get("module_path", "unknown/module")
                    # Enrich description with steps + expected result so LLM has full spec
                    desc = sc.get("description", sc.get("title", ""))
                    steps = sc.get("test_steps", [])
                    expected = sc.get("expected_result", "")
                    if steps:
                        desc += "\n\nTest Steps:\n" + "\n".join(f"  {i+1}. {s}" for i, s in enumerate(steps))
                    if expected:
                        desc += f"\n\nExpected Result: {expected}"
                    enriched = dict(sc)  # shallow copy so we don't mutate state
                    enriched["description"] = desc
                    enriched["_from_testcase"] = True  # hint for LLM: exact spec provided
                    converted.setdefault(mp, []).append(enriched)
                test_plan = converted
                state["test_plan"] = test_plan

        ui_observations = state.get('ui_observations', {})
        generated = []
        for module_path, scenarios in test_plan.items():
            if not scenarios:
                continue

            state['messages'] = [
                f"[CoderAgent] Generating {len(scenarios)} scenario(s) for {module_path}"
            ]
            print(f"[CoderAgent] Generating {len(scenarios)} scenario(s) for {module_path}...", flush=True)
            result = self._generate_for_module(module_path, scenarios, ui_observations=ui_observations)
            generated.append(result)

        state['generated_code'] = generated
        state['messages'] = [
            f"[CoderAgent] Generated code for {len(generated)} modules."
        ]
        print(f"[CoderAgent] ✅ Done — code generated for {len(generated)} module(s).", flush=True)
        return state
