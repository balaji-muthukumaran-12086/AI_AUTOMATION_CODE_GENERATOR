# AutomaterSelenium Framework — Copilot Instructions

This workspace is a **Selenium-based Java automation QA framework** for the ServiceDesk Plus (SDP) product.
Always read this file before inferring anything about the project structure.

> **Active project (as of Feb 27, 2026):** `SDPLIVE_LATEST_AUTOMATER_SELENIUM`
> Single source of truth: `config/project_config.py` → `PROJECT_NAME`
> All agents, runner, healer, and ingestion now derive paths from this config.

---

## Project Structure

```
ai-automation-qa/
├── SDPLIVE_LATEST_AUTOMATER_SELENIUM/  # ACTIVE — Module-specific tests (gitignored, managed via Mercurial)
│   ├── src/com/zoho/automater/selenium/modules/<module>/<entity>/
│   └── bin/                            # Pre-compiled .class files
│
├── AutomaterSelenium/          # LEGACY (gitignored) — do NOT write new tests here
│   ├── src/com/zoho/automater/selenium/modules/<module>/<entity>/
│   │   ├── <Entity>.java               # Annotated test methods (thin wrappers)
│   │   └── <Entity>Base.java           # Actual test logic
│   │   └── common/
│   │       ├── <Entity>Locators.java   # XPath/By locators as interface constants
│   │       ├── <Entity>Constants.java  # String constants (module name, alert messages, etc.)
│   │       ├── <Entity>DataConstants.java # Enum-style data key constants
│   │       └── <Entity>Fields.java     # Field name/dataPath definitions
│   ├── resources/
│   │   ├── entity/conf/<module>/<entity>.json   # Field config (field_type, data_path per field)
│   │   ├── entity/data/<module>/<entity>/<entity>_data.json  # Test input data (keyed by snake_case)
│   │   └── entity/roles/<module>.json           # Role/permission definitions
│   └── bin/                            # Pre-compiled .class files (used by runner)
│
├── AutomaterSeleniumFramework/         # Core engine (base classes, actions, utilities)
│   │                                   # hg branch: AI_Automation_Code_Generator (rev 304)
│   └── src/com/zoho/automater/selenium/base/
│       ├── Entity.java                 # preProcess/postProcess lifecycle
│       ├── EntityCase.java             # addSuccessReport / addFailureReport (isLocalSetup() guarded)
│       ├── standalone/LocalSetupManager.java  # local run config, report path, cleanup
│       ├── report/ScenarioReport.java  # HTML report writer for local runs
│       ├── client/components/
│       │   ├── FormBuilder.java        # fillInputForAnEntity, fillDateField, fillSelectField, etc.
│       │   └── Validator.java          # textContent, isElementPresent, etc.
│       ├── client/SDPCloudActions.java # click, getText, waitForAjaxComplete, etc.
│       ├── utils/PlaceholderUtil.java  # $(placeholder) resolution at runtime
│       └── common/LocalStorage.java   # In-memory key-value store across test lifecycle
│
├── agents/runner_agent.py              # Python runner — patches 2 files, compiles, executes
├── run_test.py                         # Entry point — configure RUN_CONFIG here
└── dependencies/                       # All JARs (including framework/ subdirectory)
```

---

## ⚠️ MODULE PLACEMENT — DERIVE FROM USE CASE, NOT FROM OPEN FILE

> **Root cause of past misplacement**: Copilot defaulted to the currently open file's module
> (`SolutionBase.java` was open) instead of reading the use-case description.
> `"create an incident request and add notes"` → **Requests module**, not Solutions.

### Rule: before writing or moving ANY scenario, answer these three questions in order

1. **What entity does the use case name?**  
   Match the noun in the description to the correct module:

   | Use-case noun | Module path | Correct entity class(es) |
   |---|---|---|
   | incident request / IR | `modules/requests/request/` | `IncidentRequest`, `IncidentRequestNotes`, `RequestNotes` |
   | service request / SR | `modules/requests/request/` | `ServiceRequest`, `ServiceRequestNotes` |
   | solution | `modules/solutions/solution/` | `Solution`, `SolutionBase` |
   | problem | `modules/problems/problem/` | `Problem`, `ProblemBase` |
   | change | `modules/changes/change/` | `Change`, `ChangeBase` |
   | task | `modules/tasks/task/` | `Task`, `TaskBase` |

2. **Does a matching leaf class already exist?**  
   Search `modules/<module>/` for an existing `*Notes.java`, `*DetailView.java`, etc.  
   Place the scenario there — never create a new file if a suitable one exists.

3. **Does `entity_class` in `run_test.py` match the leaf class?**  
   Update it to the correct value (e.g. `"IncidentRequestNotes"`) before running.

> **FORBIDDEN**: Using the currently open / most recently edited file as the default target
> for a new scenario. Always validate module semantics from the use-case description first.

---

## Test Lifecycle

1. **preProcess** (driven by `@AutomaterScenario(group=..., dataIds={...})`)
   - Creates prerequisite data via REST API (templates, topics, solutions, etc.)
   - Stores IDs/names in `LocalStorage` (e.g., `"solution_template"`, `"topic"`)

2. **Test method** (in `<Entity>Base.java`)
   - Loads data: `getTestCaseData(DataConstants.SomeKey)` → resolves `$(placeholders)` from LocalStorage
   - Navigates UI, fills form via `fillInputForAnEntity` + manual field calls
   - Validates result

3. **postProcess** — deletes created entities via REST API

---

## Data & Field Config

### `entity/conf/<entity>.json` — field config loaded into `fields` Map
```json
{ "name": "template", "field_type": "select", "data_path": "template.name" }
```
Supported `field_type` values: `input`, `select`, `multiselect`, `html`, `date`, `datetime`, `textarea`, `criteria`, `picklist`, `attachment`

> ⚠️ **No `boolean`/`checkbox` field_type exists.** `fillInputForAnEntity` calls
> `getValueAsStringFromInputUsingAPIPath()` which returns `null` for JSON booleans →
> boolean fields (like `is_public`) are **silently skipped**.
> Checkboxes must be handled manually via explicit `actions.click(locator)`.

### `entity/data/<entity>_data.json` — keyed test data
```json
"sol_unapproved_pub_cust_temp_exp_rev_date_cust_topic": {
  "data": { "title": "..._$(unique_string)", "template": {"name": "$(custom_solution_template)"}, ... }
}
```
- `$(unique_string)` → millisecond timestamp
- `$(custom_X)` → looks up key `X` in `LocalStorage` (set by preProcess)
- `$(date, 2D 1M, ahead)` → relative date string

---

## Compilation

> ⚠️ **Full project compile is BROKEN** — 67 pre-existing errors in unrelated modules (requests,
> problems, contracts, admin, etc.). Never run full project compile.

### Step 1 — Framework compile (run once after clone or branch switch):
```bash
./setup_framework_bin.sh
```
This compiles all 90+ `AutomaterSeleniumFramework` source files (branch `AI_Automation_Code_Generator`)
into `SDPLIVE_LATEST_AUTOMATER_SELENIUM/bin/`, overriding old classes from `AutomationFrameWork.jar`.
**Required** because `EntityCase`, `ScenarioReport`, `LocalSetupManager` etc. need UmeshBranch versions
for local runs to work correctly (report/screenshot generation depends on `isLocalSetup()` guards).

### Step 2 — Module targeted compile (after editing module source):
```bash
DEPS=/home/balaji-12086/Desktop/Workspace/Zide/dependencies
BIN=/home/balaji-12086/Desktop/Workspace/Zide/ai-automation-qa/SDPLIVE_LATEST_AUTOMATER_SELENIUM/bin
SRC=/home/balaji-12086/Desktop/Workspace/Zide/ai-automation-qa/SDPLIVE_LATEST_AUTOMATER_SELENIUM/src
CP="$BIN:$(find "$DEPS" -name "*.jar" | tr '\n' ':')"
javac -encoding UTF-8 -cp "$CP" -d "$BIN" \
  "$SRC/com/zoho/automater/selenium/modules/solutions/solution/common/SolutionLocators.java" \
  "$SRC/com/zoho/automater/selenium/modules/solutions/solution/SolutionBase.java"
```
- Must include `find "$DEPS" -name "*.jar"` **recursively** — `dependencies/framework/` subdirectory has critical JARs (selenium, AutomationFrameWork.jar, json.jar)
- Runner (`run_test.py`) with `skip_compile=True` only recompiles 2 patched files — always run targeted compile after editing module source files

### Classpath precedence (critical):
```
bin/  (our compiled classes — WINS over JARs)
AutomationFrameWork.jar  (old versions, overridden for Entity/Report classes)
selenium*.jar, json.jar, etc.
```

---

## Running a Test

### Driver & Environment Paths
| Resource | Path |
|----------|------|
| Firefox binary | `/home/balaji-12086/Desktop/Workspace/Zide/Drivers/firefox/firefox` |
| Geckodriver | `/home/balaji-12086/Desktop/Workspace/Zide/Drivers/geckodriver` |
| Dependencies | `/home/balaji-12086/Desktop/Workspace/Zide/dependencies` |
| Python venv | `.venv/` (activate with `.venv/bin/activate`) |

```python
# run_test.py  (current state — Feb 27, 2026)
RUN_CONFIG = {
    "entity_class":  "IncidentRequestNotes",   # last run class — change as needed
    "method_name":   "createIncidentRequestAndAddNotes",
    "url":           "https://sdpodqa-auto1.csez.zohocorpin.com:9090/",
    "admin_mail_id": "jaya.kumar+org1admin1t0@zohotest.com",
    "email_id":      "jaya.kumar+org1admin1t0@zohotest.com",
    "portal_name":   "portal1",
    "skip_compile":  True,   # keep True — full compile is broken
}
```
```bash
cd /home/balaji-12086/Desktop/Workspace/Zide/ai-automation-qa
.venv/bin/python run_test.py 2>&1
```

Reports generated at:
`SDPLIVE_LATEST_AUTOMATER_SELENIUM/reports/LOCAL_<methodName>_<timestamp>/ScenarioReport.html`

Screenshots at: `reports/LOCAL_<methodName>_<timestamp>/screenshots/Success_<ts>.png`

> ⚠️ Report filename changed from `ScenarioLogDetails__.html` (Aalam mode) to `ScenarioReport.html` (local mode)

---

## Key Framework Behaviours

| Behaviour | Detail |
|-----------|--------|
| `actions.click(locator)` | Calls `waitForAjaxComplete()` **before** clicking — no need to add it after |
| `actions.getText(locator)` | Has **3-second** `waitForAnElementToAppear` timeout — can miss slow-loading pages |
| `fillInputForAnEntity` | Skips fields where value is `null` (including all JSON booleans) |
| `fillDateField(name, millis)` | Opens datepicker → navigates by year/month arrows → clicks day cell |
| `LocalStorage` | Scoped to single test run; key `"solution_template"` → template name, `"topic"` → topic name |
| `MODULE_TITLE` locator | `//div[@id='details-middle-container']/descendant::h1` — may include display ID prefix (e.g. `SOL-8Title...`) |
| Local run report flow | `EntityCase.addSuccessReport()` → `LocalFailureTemplates` + `ScenarioReport` rows + `screenshots/Success_<ts>.png` → `Entity.run()` finally → `ScenarioReport.createReport()` → `ScenarioReport.html` |
| `AutomationReport` (Aalam/CI) | NOT used in local runs — guarded by `!LocalSetupManager.isLocalSetup()` in `EntityCase`. Old JAR version has no guard → `IOException` when `REPORT_FILE_PATH` is null. Always compile framework via `setup_framework_bin.sh` to get the guarded version. |

---

## REST API Architecture

> ⚠️ **API calls go through the browser via JavaScript** — NOT a direct HTTP client.

- `RestAPI.triggerRestAPI()` calls `executeScript("sdpAPICall(apiPath, method, ...).responseJSON")` → browser executes JS → returns JSON string
- Requires an **active logged-in browser session** — the browser must be on a valid SDP page
- If JS returns `undefined`/`null`, `responseString` is null → `response` is null → NPE in callers
- Base URL is implicit (same as browser session origin)

### Session Context During Test Lifecycle
1. `initializeAdminSession()` → browser logs in as **admin**
2. `preProcess(group, dataIds)` → runs API calls **in admin session** (correct permissions)
3. `switchToUserSession()` → browser switches to scenario user
4. `process(method)` → test method runs **in user session**

> ⚠️ **Critical**: If API calls (e.g., `createSolutionTemplateAndGetName`) are placed inside the **test method body** instead of `preProcess`, they run in the **user session** — users cannot create solution templates → `sdpAPICall` returns null → NPE.
> Always put prerequisite API calls in `preProcess` group, not in the method body.

### `preProcess` Silent Catch
`Solution.java::preProcess()` has `catch(Exception) { return false; }` — silently swallows all exceptions.
If `preProcess` returns `false`, the test is skipped without any visible error. Debug by temporarily adding logging or moving the call into the method body.

### `SolutionAPIUtil` Patterns
```java
// Creates a solution template, stores name in LocalStorage("solution_template_name"), returns name
String templateName = SolutionAPIUtil.createSolutionTemplateAndGetName("solution_templates", templateData);
LocalStorage.store("solution_template", templateName);  // key used by $(custom_solution_template)

// Creates a topic, returns name
String topicName = SolutionAPIUtil.createSolutionTopicAndGetName("topics", topicData);
LocalStorage.store("topic", topicName);  // key used by $(custom_topic)
```

---

## Runner Agent `_parse_success()` Logic

Priority order (first match wins):
1. `"$$Failure"` in output → **FAILED** (highest priority)
2. `'"Additional Specific Info":["'` + `"successfully"` → **PASSED**
3. `"BUILD FAILED"` → **FAILED**
4. `"BUILD SUCCESSFUL"` → **PASSED**
5. Java exceptions (`addFailureReport`, `NullPointerException`, `NoSuchElementException`, `TimeoutException`, `WebDriverException`, `AssertionException`) → **FAILED**
6. **Default: `False`** — no positive signal = FAILED (prevents false PASS on clean JVM exit)

### Additional checks (applied after parse):
- `ENTITY_IMPORT_MAP` must contain FQCN for entity class — missing entry → `ClassNotFoundException` silently caught → false PASS
- Empty report directory after `success=True` → overridden to FAIL (report dir created early by `LocalSetupManager.configure()` before test runs)
- `ScenarioReport.html` must exist in report dir for result to be trusted as PASS

---

## Key File Locations

> All Java paths below are under `SDPLIVE_LATEST_AUTOMATER_SELENIUM/` (active project).

| File | Path |
|------|------|
| `Solution.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/solutions/solution/Solution.java` |
| `SolutionBase.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/solutions/solution/SolutionBase.java` |
| `SolutionLocators.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/solutions/solution/common/SolutionLocators.java` |
| `SolutionConstants.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/solutions/solution/common/SolutionConstants.java` |
| `SolutionAPIUtil.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/solutions/solution/utils/SolutionAPIUtil.java` |
| `SolutionAnnotationConstants.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/solutions/solution/common/SolutionAnnotationConstants.java` |
| `SolutionDataConstants.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/solutions/solution/common/SolutionDataConstants.java` |
| `solution_data.json` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/resources/entity/data/solutions/solution/solution_data.json` |
| `IncidentRequestNotes.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/requests/request/IncidentRequestNotes.java` |
| `RequestNotes.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/requests/request/RequestNotes.java` |
| `Entity.java` | `AutomaterSeleniumFramework/src/com/zoho/automater/selenium/base/Entity.java` |
| `RestAPI.java` | `AutomaterSeleniumFramework/src/com/zoho/automater/selenium/base/client/api/RestAPI.java` |
| `PlaceholderUtil.java` | `AutomaterSeleniumFramework/src/com/zoho/automater/selenium/base/utils/PlaceholderUtil.java` |
| `LocalStorage.java` | `AutomaterSeleniumFramework/src/com/zoho/automater/selenium/base/common/LocalStorage.java` |
| `LocalSetupManager.java` | `AutomaterSeleniumFramework/src/com/zoho/automater/selenium/base/standalone/LocalSetupManager.java` |
| `ScenarioReport.java` | `AutomaterSeleniumFramework/src/com/zoho/automater/selenium/base/report/ScenarioReport.java` |
| `project_config.py` | `config/project_config.py` |
| `module_taxonomy.yaml` | `config/module_taxonomy.yaml` |
| `runner_agent.py` | `agents/runner_agent.py` |
| `run_test.py` | `run_test.py` |
| `setup_framework_bin.sh` | `setup_framework_bin.sh` |

---

## ChromaDB Knowledge Base State (as of Feb 26, 2026)

| Metric | Value |
|--------|-------|
| Active project | `SDPLIVE_LATEST_AUTOMATER_SELENIUM` |
| Java files parsed | 1,426 |
| Modules indexed | 210 |
| Scenarios in `scenarios_flat.json` | 17,101 |
| ChromaDB actual vectors | **14,637** (not 17,101 — see below) |
| ChromaDB source chunks | 8,722 |
| ChromaDB help topics | 920 |

### ⚠️ Why ChromaDB is short 2,464 vectors
ChromaDB upsert collapses records with the same `id` — the delta is caused by **1,350 duplicate `id` strings** in Java `@AutomaterScenario` annotations:

| Duplicate ID | Count | Location |
|---|---|---|
| `SDPOD_AUTO_NOTIFICATION_014` | ×185 | `admin/automation/notificationrules` |
| `NoPreprocess` | ×42 | Various — `group` name used as `id=` by mistake |
| `SDPOD_ZIA_028` | ×36 | `admin/zia` |
| `SDPOD_AUTO_REQ_TRIGGER_324` | ×36 | `admin/automation/triggers` |
| `SDPOD_ORG_ROLE_*` | ×22–26 each | Instance configuration |

Additionally **3,209 scenarios have empty `id`** (`@AutomaterCase` old style or `id=""`).

### ⏳ Pending — Fix Duplicate / Empty IDs
1. Fix `SDPOD_AUTO_NOTIFICATION_014` ×185 — mass copy-paste, assign sequential IDs
2. Fix `NoPreprocess` ×42 — assign proper `SDPOD_AUTO_<MODULE>_NNN` IDs
3. Fix remaining 1,300+ duplicates
4. After fixing: `python knowledge_base/rag_indexer.py --reset` → should reach clean 17,101 vectors
5. Decide fate of 3,209 empty-ID legacy scenarios

---

## Known Fixed Bugs (as of Feb 27, 2026)

### Local Run — Reports & Screenshots Not Generated (Feb 27, 2026)
**Status**: ✅ Fixed
**Root cause**: `AutomaterSeleniumFramework` source was not compiled into `bin/` — old JAR's `EntityCase.class` (without `isLocalSetup()` guards) was being loaded. It called `AutomationReport.addRowToReport()` which reads `CommonVariables.REPORT_FILE_PATH` (null in local runs) → `IOException`.
**Fix**: `setup_framework_bin.sh` — compiles all 90 framework sources into `bin/`. New `EntityCase` uses `ScenarioReport` + `LocalFailureTemplates` for local runs (completely bypasses `AutomationReport`).
**Additional fixes in framework source:**
- `EntityCase.java` — commented out `CommonVariables.setisSkipScreenShot()` (missing in local JAR)
- `ScenarioReport.java` — `element.childNodeSize()` → `element.children().size()` (jsoup API)
- `FirefoxWebDriver.java` + `ChromeWebDriver.java` — commented out `CommonVariables.gridURL` (missing field)
- `LocalSetupManager.openReport()` — fixed NPE: `System.getProperty("headless")` null-guarded with `Boolean.parseBoolean(..., "false")`
**hg commit**: `AI_Automation_Code_Generator` rev `304:bb0d9ca1eaa6` by `Balaji_M`

---

### SDPOD_AUTO_IR_NOTES_001 — `createIncidentRequestAndAddNotes` (Feb 26, 2026)
**Status**: ✅ Compiled & placed correctly
**Issue**: Scenario was in wrong module (`Solution.java`/`SolutionBase.java`) — should be in Requests.
**Files changed:**
- `IncidentRequestNotes.java` (requests/request) — Added `@AutomaterScenario` wrapper
- `RequestNotes.java` (requests/request) — Added preProcess branch + full method implementation
- `SolutionBase.java` — Removed `createIncidentForNotes` preProcess branch + method body
- `Solution.java` — Removed `@AutomaterScenario` wrapper
- `run_test.py` — `entity_class` updated to `"IncidentRequestNotes"`

---

### SDPOD_AUTO_SOL_DV_241 — `createAndShareApprovedPublicSolutionFromDV`
**Status**: ✅ PASSING
**Files changed:**
- `SolutionLocators.java` — Added `SHARE_SOL_POPUP_SUBMIT` locator in `SolutionDetailView`
- `SolutionConstants.java` — Added `SOLUTIONS_SHARED_MSG = "Solutions shared"` in `AlertMessages`
- `runner_agent.py` — Fixed `_parse_success()` to use `$$Failure` marker, not broad `"Error:"` string

### SDPOD_AUTO_SOL_DV_242 — `createUnapprovedSolutionWithCustomTopicRevDateExpDate`
**Files changed:**
- `SolutionLocators.java` — `SOLUTION_ADD`: `contains(text(),' Add ')` → `normalize-space(text())='Add'`
  (prevents matching "Add And Approve" button)
- `solution_data.json` — `sol_unapproved_pub_cust_temp_exp_rev_date_cust_topic`: `is_public: true` → `false`
  (method has no `SOLUTION_IS_PUBLIC_1` click → form defaults to unchecked/private)
- `SolutionBase.java` — removed `actions.click(SolutionLocators.SolutionCreateForm.SOLUTION_IS_PUBLIC_1)`
  (was toggling checkbox incorrectly; boolean not handled by fillInputForAnEntity)

---

## Common Pitfalls

- **`SOLUTION_ADD` vs `SOLUTION_ADD_APPROVE`**: Always use `normalize-space(text())='Add'` for exact match
- **Checkbox fields**: Must click via explicit locator — never rely on `fillInputForAnEntity` for booleans
- **Data key naming**: `SOL_UNAPPROVED_PUB_*` maps to snake_case `sol_unapproved_pub_*` in JSON
- **Template/topic setup**: Must be in `preProcess` group `CREATE_CUST_TEMP_TOPIC` — stores under `"solution_template"` and `"topic"` in LocalStorage
- **`$(custom_solution_template)`**: Strips `custom_` prefix → looks up `"solution_template"` in LocalStorage
- **Select2 dropdowns**: Render option `<li>` elements in `<div class="select2-drop">` appended to `<body>` — NOT inside the parent dialog/popup. Use `//div[contains(@class,'select2-result-label')]` to match options.
- **SDP Associations tab container ID**: `change_associations_parent_change` (not `change_associations_linked_changes`). Attach button has `name="associating-change-button"`.

---

## CH-286 Linking Changes — Active Test Suite (as of Mar 2, 2026)

> **Feature**: Link parent/child changes in Change module Associations tab
> **Build URL**: `https://sdpod-am1.csez.zohocorpin.com:55091/` (feature branch)
> **Feature doc**: `docs/Feature_Document/Linking Change and Lookup field Enhancement.md`
> **Use case CSV**: `docs/UseCase/Balaji_CH 286 Linking Changes and Multi select Lookup Fields for Change _Sheet1.csv`
> **19 CSV use cases → 6 test methods** in `DetailsView.java` (lines 1727-2243)

### Test Methods & Execution Status

| # | Method | IDs | Status |
|---|--------|-----|--------|
| 1 | `verifyAssociationTabAndAttachOptionsInLHS` | CH_001, CH_005 | ✅ PASSED |
| 2 | `verifyAttachParentChangePopup` | CH_006-011 | ❌ Fix applied, needs re-run |
| 3 | `attachParentChangeAndVerifyAssociation` | CH_012-016 | ⏳ Not run |
| 4 | `detachParentChangeAndVerifyReset` | CH_017 | ⏳ Not run |
| 5 | `verifyAttachChildChangePopup` | CH_018-019 | ⏳ Not run |
| 6 | `attachDetachChildChangesAndVerifyListView` | CH_002-004 | ⏳ Not run |

### Key Files

| File | Path |
|------|------|
| `DetailsView.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/changes/change/DetailsView.java` |
| `ChangeLocators.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/changes/change/common/ChangeLocators.java` |
| `ChangeConstants.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/changes/change/common/ChangeConstants.java` |
| `ChangeAnnotationConstants.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/changes/change/common/ChangeAnnotationConstants.java` |
| `ChangeDataConstants.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/changes/change/common/ChangeDataConstants.java` |
| `ChangeAPIUtil.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/changes/change/utils/ChangeAPIUtil.java` |
| `Change.java` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/changes/change/Change.java` |
| `change_data.json` | `SDPLIVE_LATEST_AUTOMATER_SELENIUM/resources/entity/data/changes/change/change_data.json` |

### Locator Interfaces Added to ChangeLocators.java

- **`LinkingChange`** — Main page locators: Association tab, Attach button, dropdown options (Parent/Child), Detach button, records count, pagination, table settings, linked change rows
- **`LinkingChangePopup`** — Popup dialog locators: title, filter dropdown (Select2), filter options, radio/checkbox selection, Associate/Cancel buttons, search, records count, pagination, table settings

### preProcess Group: `CREATE_CHANGES_FOR_LINKING`
- Creates 3 changes via API (1 source + 2 targets)
- Stores in LocalStorage: `changeName`, `changeId`, `targetChangeName1`, `targetChangeId1`, `targetChangeName2`, `targetChangeId2`

### DOM Mapping (verified via Playwright)

| UI Element | Selector |
|---|---|
| Associations tab | `//a[@data-tabname='associations']` |
| Parent change container | `//div[@id='change_associations_parent_change']` |
| Attach button | `//button[@name='associating-change-button']` |
| Parent Change option | `//a[@name='associate_parent_change']` |
| Child Changes option | `//a[@name='associate_child_changes']` |
| Popup dialog | `.association-dialog-popup.changes-association` |
| Select2 trigger | `//div[contains(@class,'association-dialog-popup')]//span[contains(@class,'select2-chosen')]` |
| Select2 options | `//div[contains(@class,'select2-result-label') and contains(text(),'...')]` (at body level) |
| Records count | `//span[contains(@class,'navigatorDetailsColumn')]` |
| Table settings | `//div[@data-sdp-table-id='sdp-table-list-settings']` |

### Run Configuration
```python
# run_test.py
RUN_CONFIG = {
    "entity_class":  "ChangeDetailsView",
    "method_name":   "verifyAttachParentChangePopup",  # change per test
    "skip_compile":  True,
}
# runner_agent.py ENTITY_IMPORT_MAP:
# "ChangeDetailsView": "com.zoho.automater.selenium.modules.changes.change.DetailsView"
```

### Remaining Feature Gaps (10 areas, deferred)
1. List View — linked changes column
2. RHS summary count
3. History entries for link/unlink
4. Closure Rules (block close if linked changes open)
5. Trash/Restore behaviour
6. Export linked changes
7. Permissions (technician vs requester)
8. MSP considerations
9. Linking Constraints (self-link, circular)
10. Multi-select Lookup Field Enhancement

---

## AI Orchestrator Pipeline

> **Vision**: Generate automation test cases from feature documents with zero manual intervention.

### Agent Pipeline (LangGraph)
```
Document Ingestion → Planner → Coverage → Coder → Reviewer → Output → Runner
                                                                           │
                                                              FAILED → HealerAgent
                                                              PASSED → Done ✅
```

| Agent | File | Role |
|-------|------|------|
| Planner | `agents/planner_agent.py` | Breaks feature description → test scenarios |
| Coverage | `agents/coverage_agent.py` | Gap analysis against existing ChromaDB tests |
| Coder | `agents/coder_agent.py` | Generates Java test code via LLM |
| Reviewer | `agents/reviewer_agent.py` | Validates generated code quality |
| Output | `agents/output_agent.py` | Writes code to `.java` files |
| Runner | `agents/runner_agent.py` | Compiles + runs tests |
| **Healer** | `agents/healer_agent.py` | ✅ Playwright self-healing (COMPLETED Feb 25, 2026) |

### HealerAgent
- Classifies failure type: `LOCATOR | API | LOGIC | COMPILE`
- Opens Playwright browser, navigates to failing UI state
- Captures accessibility snapshot → LLM derives correct fix
- Patches Java source, recompiles, reruns
- `headless=True` by default — set to `False` to watch it debug live
- Chromium installed at `~/.cache/ms-playwright/`

### Knowledge Base
- **ChromaDB** vector store at `knowledge_base/chroma_db/` — 14,637 scenario vectors (210 modules, 17,101 source scenarios — 2,464 collapsed due to duplicate IDs in Java source)
- `config/project_config.py` → `PROJECT_NAME` drives all ingestion + agent paths
- `coverage_agent.py` uses `top_k=5` for duplicate search (raised from 3 after corpus grew 3×)
- New generation is always gap-aware (Coverage Agent queries KB before generating)
- LLM: **local Ollama** (`qwen2.5-coder:7b`) — upgrade to `gpt-4o` for better quality
- Entry point: `main.py` (full pipeline), `run_test.py` (quick CLI runner)

### Phase Status
| Phase | Status | Commit | Description |
|-------|--------|--------|-------------|
| 0 — Foundation | ✅ DONE | — | LangGraph pipeline, RunnerAgent, ChromaDB, first AI-generated test |
| 0.5 — Self-Healing | ✅ DONE | — | HealerAgent with Playwright (Feb 25, 2026) |
| 0.6 — SDPLIVE Sync | ✅ DONE | — | Switched active project to SDPLIVE_LATEST_AUTOMATER_SELENIUM; reindexed 210 modules / 17,101 scenarios; fixed all hardcoded paths (Feb 26, 2026) |
| 0.7 — Duplicate ID Cleanup | ⏳ IN PROGRESS | `bd959b3` | Fix 1,350 duplicate IDs + 3,209 empty IDs in Java source → clean --reset reindex to 17,101 vectors (2-week Java task) |
| 0.8 — Local Run Infrastructure | ✅ DONE | `56a0f3c` | Compiled AutomaterSeleniumFramework (AI_Automation_Code_Generator hg branch) into SDPLIVE bin/; fixed report + screenshot generation; setup_framework_bin.sh for repeatable setup (Feb 27, 2026) |
| 1 — Document Ingestion | ✅ DONE | `bc42247` | PDF/DOCX/XLSX/TXT → structured use-cases via IngestionAgent |
| 2 — Web UI | ✅ DONE | `6438cba` | FastAPI + React upload interface with live SSE streaming on port 9500 |
| 3 — Hg Integration | ✅ DONE | `aad0e69` | Auto-branch + commit in Mercurial on test pass; gated by `HG_AGENT_ENABLED` flag |
| 4 — Live Test Run | ✅ DONE | `358fb4f`, `e416284` | End-to-end generation via Web UI; fixed NameError in CoderAgent + Annotated[list] reducer doubling bug |
| **4.5 — Run-Once + UI Copy-Paste** | 🔲 NEXT | — | After generation, one-click test validation via RunnerAgent; generated .java files shown in Web UI with syntax-highlighted copy-paste panel and target-path hint; `GET /api/runs/{run_id}/file-content` endpoint; "Run once" toggle on generate form (see `docs/pipeline-flow.md` Phase 4.5 spec) |
| **5 — Pipeline Monitoring & Orchestrator** | 🔲 | — | Real-time per-agent monitoring, orchestrator agent, progress UI, OOM/timeout recovery (see spec below) |
| 6 — Multi-Entity | 🔲 | — | All 10+ entities, regression suite generation |
| 7 — Feedback Loop | 🔲 | — | Learn from failures, human approval queue |

---

### Phase 5 — Pipeline Monitoring & Orchestrator Agent (Detailed Spec)

> **Goal**: Replace the current "black-box RUNNING" state with full per-stage visibility and an intelligent orchestrator that can detect, diagnose, and recover from mid-pipeline failures without human intervention.

#### 5.1 — Per-Agent Progress Streaming
| Item | Detail |
|------|--------|
| Stage indicator | UI shows which node is currently executing: `Ingestion → Planner → Coverage → Scout → Coder → Reviewer → Output → Runner → Healer` |
| Per-agent log panel | Each agent streams its own timestamped sub-logs via SSE (not batched at end) |
| Token / time metrics | Track tokens used + wall-clock time per agent; display in run summary |
| Progress bar | Estimated % complete based on stage weights (Coder = heaviest) |

#### 5.2 — Orchestrator Agent (`agents/orchestrator_agent.py`)
Wraps the LangGraph invocation and provides:
| Responsibility | Detail |
|----------------|--------|
| Stage lifecycle events | Emits `STAGE_START` / `STAGE_END` / `STAGE_ERROR` events for each node |
| OOM detection & retry | Detects `"requires more system memory"` from Ollama → waits 30s, kills idle processes inside runner thread, retries up to 2× |
| Timeout watchdog | Per-agent timeout (configurable in `project_config.py`); kills stuck agent, marks it as `TIMED_OUT`, continues pipeline |
| Partial-result recovery | If Planner partially succeeds (some modules planned), Coverage + Coder still run on those modules |
| Health pulse | Emits a heartbeat every 10s so the UI knows the pipeline is alive (prevents false "stuck" display) |

#### 5.3 — Run History & Monitoring Dashboard
| Item | Detail |
|------|--------|
| Persistent run log | Store all runs in `logs/runs.jsonl` (append-only) for post-mortem |
| `/api/runs` history endpoint | Return last N runs with status, duration, error summary |
| Dashboard view | New tab in Web UI: table of all past runs, click to expand full log |
| Memory / CPU gauge | Live system stats (RAM available, Ollama resident size) shown in UI header |
| Alert badge | Red badge on UI if last 3 runs all failed (signals systemic issue) |

#### 5.4 — Notification on Completion
| Item | Detail |
|------|--------|
| Browser notification | `Notification API` push when tab is backgrounded |
| Webhook (optional) | POST to configurable URL on `success` / `failure` |
| Sound indicator (opt-in) | Audible ding on completion |

#### 5.5 — Config additions (`config/project_config.py`)
```python
AGENT_TIMEOUTS = {
    "planner":  120,   # seconds
    "coverage":  60,
    "scout":    180,
    "coder":    300,
    "reviewer":  90,
    "output":    60,
    "runner":   600,
    "healer":   300,
}
OOM_RETRY_MAX    = 2
OOM_RETRY_WAIT_S = 30
MONITORING_HEARTBEAT_S = 10
RUNS_LOG_PATH    = "logs/runs.jsonl"
```
