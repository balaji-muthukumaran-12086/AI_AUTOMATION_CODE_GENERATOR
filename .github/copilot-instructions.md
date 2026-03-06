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

> All paths below are set via **`config/project_config.py`** (reads from env vars / `.env` file).
> Override in `.env` — never hardcode machine-specific paths in test code.

| Resource | Config var | Default fallback |
|----------|-----------|-----------------|
| Firefox binary | `FIREFOX_BINARY` | `$DRIVERS_DIR/firefox/firefox` |
| Geckodriver | `GECKODRIVER_PATH` | `$DRIVERS_DIR/geckodriver` |
| Dependencies (JARs) | `DEPS_DIR` | machine-specific — must set in `.env` |
| SDP URL | `SDP_URL` | see `project_config.py` |
| Python venv | — | `.venv/` (activate with `.venv/bin/activate`) |

```python
# run_test.py — edit RUN_CONFIG to target a different test
RUN_CONFIG = {
    "entity_class":  "ChangeDetailsView",       # ENTITY_IMPORT_MAP in runner_agent.py must have entry
    "method_name":   "attachDetachChildChangesAndVerifyListView",
    "url":           SDP_URL,                   # from config/project_config.py
    "admin_mail_id": SDP_ADMIN_EMAIL,
    "email_id":      SDP_EMAIL_ID,
    "portal_name":   SDP_PORTAL,
    "password":      SDP_ADMIN_PASS,
    "skip_compile":  True,                      # keep True — full compile is broken
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

> 📖 **API Reference Doc**: `docs/api-doc/SDP_API_Endpoints_Documentation.md` — contains exact V3 API paths, HTTP methods, input wrappers, and worked automation cases for all 16 SDP modules.
> **When writing any `preProcess()` API call or `RestAPI.*` invocation**, consult this doc for the correct:
> - API path (e.g. `api/v3/changes`, `api/v3/requests/{id}/notes`)
> - Input wrapper key (e.g. `{"change": {...}}`, `{"request": {...}}`)
> - Available sub-resource paths (notes, tasks, worklogs, approvals, etc.)

> ⚠️ **API calls go through the browser via JavaScript** — NOT a direct HTTP client.

- `RestAPI.triggerRestAPI()` calls `executeScript("sdpAPICall(apiPath, method, ...).responseJSON")` → browser executes JS → returns JSON string
- Requires an **active logged-in browser session** — the browser must be on a valid SDP page
- If JS returns `undefined`/`null`, `responseString` is null → `response` is null → NPE in callers
- Base URL is implicit (same as browser session origin)

### Core RestAPI Methods
| Method | Returns | Use When |
|--------|---------|----------|
| `restAPI.create(entityName, apiPath, inputData)` | String ID | Only need entity ID |
| `restAPI.createAndGetResponse(entityName, apiPath, inputData)` | JSONObject entity | Need ID + title + fields (**most common**) |
| `restAPI.createAndGetFullResponse(apiPath, inputData)` | JSONObject raw response | Need full response envelope |
| `restAPI.get(apiPath, inputData)` | JSONObject | Reading entity data |
| `restAPI.update(apiPath, inputData)` | JSONObject | Updating entity |
| `restAPI.delete(apiPath)` | boolean | Deleting entity (true if statusCode 2000) |
| `restAPI.getEntityIdUsingSearchCriteria(plural, path, data)` | String ID | Find by criteria |
| `restAPI.getEntityIDUsingFieldValue(path, field, value)` | String ID | Find by field value (2-step) |

### Input Data Wrapping
```java
JSONObject inputData = getTestCaseDataUsingCaseId(dataId);     // Load JSON + resolve placeholders
JSONObject response = restAPI.createAndGetResponse(getName(), getModuleName(), getInputData(inputData));
// getInputData() wraps as {"change": {...}} or {"request": {...}} per module convention
```

### Auto-Cleanup
Every `POST` (create) call auto-registers in `DataUtil.cleanUpIds` for automatic cleanup.

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
| `sdp_api_helper.py` | `agents/sdp_api_helper.py` |
| `run_test.py` | `run_test.py` |
| `setup_framework_bin.sh` | `setup_framework_bin.sh` |
| **`SDP_API_Endpoints_Documentation.md`** | `docs/api-doc/SDP_API_Endpoints_Documentation.md` — V3 API paths, input wrappers and automation cases for all 16 modules. **Read this before writing any preProcess API call.** |

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

## Code Generation Rules (REQUIRED — apply on every new test)

### @AutomaterScenario — All 9 Fields (always include all)

```java
@AutomaterScenario(
    id          = "SDPOD_AUTO_SOL_DV_243",        // next sequential — run grep to verify
    group       = "create",                        // MUST exist in preProcess()
    priority    = Priority.MEDIUM,                 // HIGH / MEDIUM / LOW
    dataIds     = {SolutionAnnotationConstants.Data.CREATE_PUB_APP_SOL_API},
    tags        = {},
    description = "Plain English description",
    owner       = OwnerConstants.RAJESHWARAN_A,
    runType     = ScenarioRunType.USER_BASED,      // ⚠️ ALWAYS explicit — default is PORTAL_BASED
    switchOn    = SwitchToUserSession.AFTER_PRE_PROCESS  // or BEFORE_PRE_PROCESS / NEVER
)
```

> ⚠️ **`runType` trap**: Annotation default is `PORTAL_BASED`. **Always write `runType = ScenarioRunType.USER_BASED` explicitly. Never omit it.**

### Test ID Format (per module — do NOT mix prefixes)

| Module | Pattern | Example |
|---|---|---|
| Requests ListView | `SDP_REQ_LS_AAA###` | `SDP_REQ_LS_AAA101` |
| Requests DetailView | `SDP_REQ_DV_AAA###` | `SDP_REQ_DV_AAA115` |
| Solutions (generic) | `SDPOD_AUTO_SOL_###` | `SDPOD_AUTO_SOL_136` |
| Solutions ListView | `SDPOD_AUTO_SOL_LV_###` | `SDPOD_AUTO_SOL_LV_180` |
| Solutions DetailView | `SDPOD_AUTO_SOL_DV_###` | `SDPOD_AUTO_SOL_DV_243` |
| Changes | `SDPOD_AUTO_CH_LV_###` | `SDPOD_AUTO_CH_LV_492` |
| Problems | `SDPOD_AUTO_PB_###` | — |

```bash
# Find next available ID before assigning (example for Solutions DV):
grep -rn 'id = "SDPOD_AUTO_SOL_DV' SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/ | \
  sed 's/.*id = "\([^"]*\)".*/\1/' | sort | tail -1
```

### Valid preProcess Groups — Requests module

```
"create"                  → creates a single request
"detailView"              → creates request for detail-view tests
"addTask"                 → creates request + task template
"addTaskTemplate"         → creates task template only
"BulkCreate"              → creates requests for bulk operations
"multipleCreate"          → creates multiple requests
"rowColor"                → creates request for row-color test
"customView"              → creates list-view filter via API
"PinFavorite"             → creates pinned favorite filter
"assetRequest"            → creates request with asset linkage
"mixedCreate"             → creates mixed IR+SR requests
"differentRequest"        → creates requests of different types
"SubEntity_Resolution"    → creates resolution sub-entity
"SubEntity_Reminder"      → creates reminder sub-entity
"SubEntity_createTask"    → creates task sub-entity
"Associations"            → creates linked associations
"copyResolution"          → creates request to copy resolution from
"create_sla"              → creates request with SLA
"requester_create"        → creates request as requester
"NoPreprocess"            → ⚡ ZERO API calls, ZERO cleanup — pair with dataIds={}
```

### Valid preProcess Groups — Solutions module

```
"create"                     → creates a solution
"create_cust_sol_temp"       → creates solution with custom template
"create_cust_temp_topic"     → creates solution with custom template + topic
"createMultipleSolution"     → creates multiple solutions
"create_topic"               → creates a topic
"NoPreprocess"               → ⚡ ZERO API calls — pair with dataIds={}
```

> ⚠️ **FORBIDDEN**: Inventing group name strings not listed above.

### Where `preProcess()` lives — check subclass first, then parent

`preProcess()` is often defined in the module parent class, but **subclasses can and do
override it**. Always check the **subclass first** for a `preProcess()` override before
looking in the parent.

```
Change.java            (parent — owns preProcess with all group branches by default)
DetailsView extends Change   (subclass — if no override, inherits parent's preProcess)
ChangeWorkflow extends Workflow  (may have its own preProcess override for workflow-specific groups)

Solution.java          (parent — owns preProcess, ends with super.preProcess(...))
SolutionBase.java      (base helper class, not where groups are defined)
```

**Discovery order (mandatory):**
1. Open the leaf/subclass file → look for its own `preProcess()` method
2. If found: that is authoritative. Check if it ends with `return super.preProcess(group, dataIds)` — if yes, also read the parent
3. If not found: open the parent class (from `extends` clause) and read its `preProcess()`

**To add a new group:**
- Applies to whole module → add `else-if` to the parent class (`Change.java`, `Solution.java`, etc.)
- Specific to one subclass only → override in that subclass + `return super.preProcess(group, dataIds)` at end

### ⭐ Reuse existing groups — do NOT add new `else-if` blocks needlessly

Before writing any new `preProcess()` code, **read the parent class's `preProcess()` body**. If an existing group already:
1. Creates the entity type you need via API
2. Stores the IDs/names you need in `LocalStorage`

→ **Use that same group value** in your `@AutomaterScenario`. No new code in `preProcess()`.

```java
// Example: "create" already calls ChangeAPIUtil.createChange() and stores:
//   LocalStorage(getName(), changeId)  →  getEntityId()
//   LocalStorage("changeName", name)   →  LocalStorage.fetch("changeName")

// ✅ CORRECT — new scenario reuses "create", reads LocalStorage:
@AutomaterScenario(group = "create", dataIds = {ChangeAnnotationConstants.Data.CREATE_CHANGE_API}, ...)
public void verifyChangeDetailView() throws Exception {
    String changeId   = getEntityId();
    String changeName = LocalStorage.fetch("changeName");
    ...
}

// ❌ WRONG — new else-if block in preProcess() when "create" already does the same thing
} else if ("createForDetailView".equalsIgnoreCase(group)) { // ← DUPLICATION
    ChangeAPIUtil.createChange(dataIds[0]);
}
```

**Decision flow:**
```
Does an existing group create the entity I need + store the LocalStorage keys I need?
  → YES: reuse that group, zero new preProcess code
  → NO:  add new else-if block with a new group string
```

### Role Constants (module-specific — import matters)

```java
// Requests module only:
RequestsRole.SDADMIN  |  RequestsRole.FULL_CONTROL  |  RequestsRole.VIEW_ONLY  |  RequestsRole.REQUESTER1

// All other modules:
Role.SDADMIN  |  ModulesRoleSkeleton.SDADMIN
```

### Owner Constants — use ONLY these 12

```
OwnerConstants.UMESH_SUDAN     OwnerConstants.ANTONYRAJAN_D    OwnerConstants.RAJESHWARAN_A
OwnerConstants.MUTHUSIVABALAN_S  OwnerConstants.VINUTHNA_K     OwnerConstants.NANTHAKUMAR_G
OwnerConstants.VIGNESH_E       OwnerConstants.RUJENDRAN        OwnerConstants.THILAK_RAJ
OwnerConstants.PURVA_RAJESH    OwnerConstants.VEERAVEL         OwnerConstants.JAYA_KUMAR
```

### DataConstants Pattern (REQUIRED — never use raw string literals)

```java
// 1. Declare in ModuleDataConstants.java:
public final static TestCaseData MY_KEY = new TestCaseData("my_key", PATH);
// PATH → "data/<module>/<entity>/<entity>_data.json"

// 2. Use in test method (UI data):
JSONObject inputData = getTestCaseData(ModuleDataConstants.ModuleData.MY_KEY);

// 3. Use in preProcess (API setup data):
JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[0]);  // key from AnnotationConstants.Data
```

> **FORBIDDEN**: `getTestCaseData("my_key")` — never pass raw string to `getTestCaseData()`.

### Data JSON Format Rules

```json
"my_data_key": {
  "data": {
    "subject":   "Test Subject $(unique_string)",
    "priority":  {"name": "High"},
    "requester": {"name": "$(user_name)"},
    "is_public": false
  }
}
```

1. Always wrap with `{"data": {...}}` — no exceptions
2. Lookup/dropdown fields = `{"name": "Value"}` object, NEVER a flat string
3. Boolean = `true`/`false`, NOT the string `"true"`

### Data Reuse (CRITICAL — prevents duplicate data entries)

Before creating any new `*_data.json` entry or `DataConstants` constant:
1. Read the existing `*_data.json` — list all top-level keys
2. Read `*AnnotationConstants.java → Data` interface for all preProcess data IDs
3. Read `*DataConstants.java` for all declared `TestCaseData` constants

**Reuse** an existing entry if it covers the same entity creation payload. Only create new entries when the field combination is genuinely different.

### ⭐ LocalStorage pre-seed — customize existing JSON entries without duplicating them

If a `*_data.json` entry has `$(custom_KEY)` placeholders, you can provide specific values
by storing them in LocalStorage **BEFORE** calling `getTestCaseData()`. This is the preferred
technique to avoid creating new JSON entries just to vary one field value.

```java
// JSON entry "create_change_with_template" has:
//   "template": {"name": "$(custom_template_name)"}

// ❌ WRONG — new JSON entry just to use a different template:
// "create_change_special": { "data": { "template": {"name": "My Template"} } }

// ✅ CORRECT — pre-seed LocalStorage, then reuse existing JSON entry:
LocalStorage.store("template_name", LocalStorage.getAsString("createdTemplateName")); // set in preProcess
JSONObject inputData = getTestCaseData(ChangeDataConstants.ChangeData.CREATE_CHANGE_WITH_TEMPLATE);
// $(custom_template_name) resolves from LocalStorage automatically
```

**Decision flow before every `getTestCaseData()` call:**
```
Need a specific field value (template, topic, linked entity, etc.)?
  ↓
  Does existing JSON have $(custom_KEY) placeholder for it?
  → YES: LocalStorage.store("KEY", value)  then  getTestCaseData(EXISTING_KEY)  [REUSE]
  → NO:  Does any existing entry provide the same payload with fixed values?
         → YES: getTestCaseData(EXISTING_KEY)  [REUSE AS-IS]
         → NO:  Create a new *_data.json entry  [only justified case]
```

### Complete Runtime Placeholder Reference

```
$(unique_string)             → millisecond timestamp (unique per run)
$(custom_KEY)                → LocalStorage.fetch("KEY") set by preProcess
$(custom_solution_template)  → LocalStorage "solution_template"
$(custom_topic)              → LocalStorage "topic"
$(user_name)                 → scenario user's display name
$(user_email_id)             → scenario user's email address
$(user_id)                   → scenario user's entity ID
$(admin_email_id)            → admin email
$(admin_name)                → admin display name
$(date, N, ahead)            → date N days ahead in milliseconds
$(datetime, N, ahead)        → datetime N days ahead in milliseconds
$(mspcustomer_id)            → MSP customer ID (MSP tests only)
$(mspcustomer_name)          → MSP customer name (MSP tests only)
```

### Non-Existent Methods — NEVER use these

```java
actions.listView.doAction()        // ❌ — use rowAction(entityID, actionName)
actions.listView.selectRecord()    // ❌ — use navigate.toDetailsPageUsingRecordId(id)
actions.navigate.clickModule()     // ❌ — use navigate.toModule(name)
LocalAutomationData.Builder.isLocal(Boolean)  // ❌ — deprecated, does not exist
```

---

### ActionUtils / APIUtil Pattern (MANDATORY — apply to every entity)

> **Rule — Enforced by code review**: Any block of UI actions or API calls that appears in more than one test method **MUST** be extracted into the entity's `*ActionsUtil.java` or `*APIUtil.java`. Test method bodies must never contain duplicate interaction sequences.

#### Where to place reusable code

| What | Where | Example file |
|------|-------|--------------|
| Multi-step UI flows (navigate, click, form fill, verify) | `modules/<module>/<entity>/utils/<Entity>ActionsUtil.java` | `ChangeActionsUtil.java` |
| REST API wrapper logic (create / update / delete / link) | `modules/<module>/<entity>/utils/<Entity>APIUtil.java` | `ChangeAPIUtil.java` |

#### Class declaration (REQUIRED — exactly this pattern)

```java
// ✅ CORRECT
public final class ChangeActionsUtil extends Utilities {
    // All methods must be public static
    // Utilities base class provides: actions, report, restAPI as static fields
    
    public static void openAssociationTab() throws Exception {
        actions.click(ChangeLocators.LinkingChange.LHS_ASSOCIATION_TAB);
        actions.waitForAjaxComplete();
    }
}

// ❌ WRONG — do NOT instantiate, do NOT make non-static
public class ChangeActionsUtil {
    public void openAssociationTab() { ... }  // non-static fails — no access to actions
}
```

#### Method granularity rules

| Bad — too granular | Good — focused unit of work |
|---|---|
| `clickAttachDropdown()` | `openAttachParentChangePopup()` (click dropdown + click option + waitForAjax) |
| `clickYesOnConfirm()` | `detachParentChange()` (click detach + validate confirm dialog + click YES + waitForAjax) |
| Inline 6-line open+search+select+associate | `linkParentChangeViaUI(name, id)` (all 6 lines encapsulated) |

Each method should represent **one complete, named UI operation** that a person doing manual testing would describe as a single step.

#### Calling convention in test methods

```java
// ✅ CORRECT — test method delegates to utility
public void verifySingleParentConstraint() throws Exception {
    ChangeActionsUtil.openAssociationTab();
    ChangeActionsUtil.linkParentChangeViaUI(
        LocalStorage.getAsString("targetChangeName1"),
        LocalStorage.getAsString("targetChangeId1")
    );
    // Only assertion code stays in the test method
    if(actions.isElementPresent(ChangeLocators.LinkingChange.DETACH_PARENT_CHANGE)) {
        addSuccessReport("SDPOD_LINKING_CH_022: Detach button shown after parent linked");
    }
}

// ❌ WRONG — inline repeated navigation/click/wait in test body
public void verifySingleParentConstraint() throws Exception {
    actions.click(ChangeLocators.LinkingChange.LHS_ASSOCIATION_TAB);   // do not inline
    actions.waitForAjaxComplete();
    actions.click(ChangeLocators.LinkingChange.ATTACH_BUTTON_DROPDOWN);
    actions.click(ChangeLocators.LinkingChange.ATTACH_PARENT_CHANGE_OPTION);
    actions.waitForAjaxComplete();
    ...
}
```

#### Pre-generation analysis — MANDATORY WORKFLOW (run BEFORE writing any test code)

> **This is the most important rule.** Every new scenario MUST complete all 4 steps before a single line of test code is written.

**Step 1 — READ the entity's util files in full**

For the target `<Entity>` in `modules/<module>/<entity>/utils/`:
- READ `<Entity>ActionsUtil.java` (or `<Entity>ActionUtils.java`) — list every `public static` method: name, parameters, what UI operation it performs.
- READ `<Entity>APIUtil.java` — same listing.
- If either file does not exist yet, note that it must be created before any scenario code is generated.

```bash
# Discover util files:
find src/com/zoho/automater/selenium/modules/<module>/<entity>/utils/ -name "*.java" | sort
# List all existing public methods (then READ the file for parameter shapes + purpose):
grep -n "public static" <Entity>ActionsUtil.java
grep -n "public static" <Entity>APIUtil.java
```

**Step 2 — MAP each operation in the scenario to a method**

Produce a decision table before writing any code:

| Operation in scenario | Existing method? | Decision |
|---|---|---|
| Open association tab | `openAssociationTab()` | REUSE |
| Link parent change | `linkParentChangeViaUI(name, id)` | REUSE |
| Some new UI flow | *(not found in util file)* | CREATE NEW |
| API create in preProcess | `ChangeAPIUtil.createChange(data)` | REUSE |

**Step 3 — Create missing methods FIRST (before writing the scenario)**

For each `CREATE NEW` in the decision table:
1. Add `public static void <methodName>(...) throws Exception { ... }` to `<Entity>ActionsUtil.java`
2. One method = one complete named UI operation (not a single click; not an entire test)
3. Compile the util file to verify before proceeding to Step 4

**Step 4 — Generate the scenario using only util calls + assertions**

- Test method body = utility calls + assertions + `addSuccessReport`/`addFailureReport` ONLY
- Zero inline `actions.click(...)` / `actions.waitForAjaxComplete()` sequences in test body
- If you catch yourself typing `actions.click(` directly in a test method → STOP → move to util first

#### Known entity utility files (read these in Step 1 before generating)

> **The list below is NOT exhaustive.** Every module in this codebase has a `utils/`
> sub-folder. Always run the discovery command first for whatever entity you are working on:

```bash
find src/com/zoho/automater/selenium/modules/<module>/<entity>/utils/ -name "*.java" | sort
```

**Comprehensive module registry** (sample — filesystem is the source of truth):

| Module | Entity | ActionsUtil | APIUtil |
|--------|--------|-------------|---------|
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

> If the entity is not in this table, run the discovery command — it will have a `utils/` folder.

---

### Complete `actions.navigate` API

```java
actions.navigate.to(Locator)
actions.navigate.toAdmin()
actions.navigate.toModule(String moduleName)
actions.navigate.toGlobalActionInListview(String name)
actions.navigate.toLocalActionInListview(String name)
actions.navigate.toDetailsPageUsingRecordId(String id)
actions.navigate.toDetailsPageUsingRecordIndex(String index)  // "1"-based String
actions.navigate.toGlobalActionInDetailsPage(String name)
actions.navigate.toLeftTabWithNoChildren(String tab)
actions.navigate.toLeftSubTabWithChildren(String tab)
actions.navigate.toSubTabInDetailsPage(String tab)
// All return `this` → chainable:
actions.navigate.toModule(getModuleName()).toGlobalActionInListview(ConstantName);
```

### Complete `actions.listView` API

```java
actions.listView.selectFilter(String filterName, String tableViewName)  // tableViewName can be null
actions.listView.columnSearch(String column, String value)              // column = display name
actions.listView.getRecordsInPage()                                     // int
actions.listView.getFieldValueFromFirstRow(String field)                // field = internal name
actions.listView.getFieldValueFromRow(String field, String row)         // row = "1"-based String
actions.listView.rowAction(String entityID, String actionName)
actions.listView.clickSpotEditField(String recordID, String field)
actions.listView.selectCheckBoxInListViewPage(String row)               // "1"-based
actions.listView.selectAllCheckBoxesInListviewPage()
actions.listView.clearAllCheckBoxInListviewPage()
actions.listView.clickBulkActionButton(String buttonName)
actions.listView.checkBulkActionsActionName(String actionName)          // returns boolean
actions.listView.setTableSettings(JSONObject data, String path)
actions.listView.sortByColumn(String colName, boolean ascending)
actions.listView.columnChooser(String column, boolean enable)
actions.listView.isColumnSelected(String column)
```

### Complete `actions.detailsView` API

```java
actions.detailsView.clickSubTab(String subTabName)
actions.detailsView.clickFromActions(String actionName)
actions.detailsView.verifyFieldInDetailsPage(String field, String value)   // returns boolean
actions.detailsView.getFieldValueFromDetailsPage(String field)
actions.detailsView.getValueFromRhsDetails(String fieldName)
actions.detailsView.clickRhsDetails(String fieldName)
actions.detailsView.verifyRecentHistoryDescription(String desc)
actions.detailsView.verifyTitleInDetailsPage(String expected)              // returns boolean
actions.detailsView.getTitle()
// Spot edit:
actions.detailsView.spotEditFieldUsingSearch(String field, String value)
actions.detailsView.spotEditTypeField(String field, String value)
actions.detailsView.spotEditPickList(String field, String value)
actions.detailsView.spotEditFieldWithoutSearch(String field, String value)
actions.detailsView.spotEditMultiSelectField(String field, String value)
```

### Complete `actions.validate` API

```java
Boolean actions.validate.textContent(Locator locator, String content)
void    actions.validate.successMessageInAlert(String message)
void    actions.validate.successMessageInAlertAndClose(String message)
void    actions.validate.errorMessageInAlert(String message)
void    actions.validate.errorMessageInAlertAndClose(String message)
void    actions.validate.verifyMessageInAlert(Boolean isSuccess, String message)
void    actions.validate.verifyMessageInAlertAndClose(Boolean isSuccess, String message)
void    actions.validate.customAssert(String expected, String got)
void    actions.validate.customAssert(Boolean expected, Boolean got)
void    actions.validate.confirmationBoxTitleAndConfirmationText(String title, String text)
Boolean actions.validate.validateDate(Locator locator, Long value)
Boolean actions.validate.validateDateTime(Locator locator, Long value, boolean isTimeField)
void    actions.validate.validateFormFieldValues(Map<String,FieldDetails> fields, JSONObject inputData)
```

### Complete `actions.formBuilder` API

```java
void fillInputForAnEntity(boolean isClientFramework, Map<String,FieldDetails> fields, JSONObject inputData)
void fillTextField(String name, String value)
void fillTextAreaField(String name, String value)
void fillSelectField(String name, String value)
void fillMultiSelectField(FieldDetails fd, JSONObject inputData, String path)
void fillHTMLField(String name, String value)
void fillDateField(String name, Long value)                               // date-only
void fillDateTimeField(String name, Long value)                           // date + time
void fillDateTimeFieldInForm(String name, Long value, boolean isTimeField)
void fillDateTimeFieldInSpotEdit(String name, Long value, boolean isTimeField)
void fillCriteria(JSONArray criteria)
void submit()                                                              // FORM_SAVE then FORM_SUBMIT
void submit(String name)                                                   // click by button name

// Date helpers (PlaceholderUtil):
Long PlaceholderUtil.getDateInMilliSeconds(int days, int months, int years, boolean isAhead)
Long PlaceholderUtil.getDateTimeInMilliSeconds(int mins, int hrs, int days, int months, int years, boolean isAhead)
```

### `actions.windowManager` API

```java
String actions.windowManager.switchToNewTab(int timeoutSeconds)  // wait + switch, returns handle
void   actions.windowManager.returnToOriginalTab()
void   actions.windowManager.switchToTabByIndex(int index)        // 0-based
void   actions.windowManager.switchToTabByTitle(String title)     // partial match
void   actions.windowManager.switchToTabByUrl(String url)         // partial match
void   actions.windowManager.closeTabByIndex(int index)
void   actions.windowManager.closeAllTabsExceptOriginal()
```

### `actions.popUp.listView` — Use Inside Popups

When interacting with a table inside **any popup**, always use `actions.popUp.listView` methods, not `actions.listView`:

```java
// ✅ CORRECT — searching inside popup
actions.popUp.listView.columnSearch("Title", changeName);

// ❌ WRONG — searches behind the popup in the main list view
actions.listView.columnSearch("Title", changeName);
```

> ⚠️ Framework popup filter methods (`selectFilterUsingSearch`, `selectFilterWithoutSearch`) only work for popups with CSS class `slide-down-popup`. For non-standard popups (e.g., `association-dialog-popup`), use custom module locators for the filter trigger + Select2 option pattern for the selection.

### Two-Piece Output Format (REQUIRED — OutputAgent parses these markers)

```java
// ===== ADD TO: Solution.java =====
// (only the @AutomaterScenario wrapper method)

// ===== ADD TO: SolutionBase.java =====
// (only the new implementation method)

// ===== ADD TO: SolutionDataConstants.java =====
// (only the new TestCaseData constant line)

// ===== ADD TO: solution_data.json =====
// (only the new JSON data entry)
```

Each block = **only the additions**. Never output the entire file. Marker must match exact filename.

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
| 1 | `verifyAssociationTabAndAttachOptionsInLHS` | CH_001, CH_005 | ✅ PASSED (Mar 2) |
| 2 | `verifyAttachParentChangePopup` | CH_006-011 | ✅ PASSED (Mar 3 11:19) |
| 3 | `attachParentChangeAndVerifyAssociation` | CH_012-016 | ✅ PASSED (Mar 3 12:10) |
| 4 | `detachParentChangeAndVerifyReset` | CH_017 | ✅ PASSED (Mar 3 12:26) |
| 5 | `verifyAttachChildChangePopup` | CH_018-019 | ✅ PASSED (Mar 3 12:29) |
| 6 | `attachDetachChildChangesAndVerifyListView` | CH_002-004 | ✅ PASSED (Mar 3 12:39) |
| 7 | `verifyHistoryEntryOnLinkingAndUnlinkingChange` | CH_020 | ✅ PASSED (Mar 4) |
| 8 | `verifyCancelInAssociationPopupDoesNotLink` | CH_031 | ✅ PASSED (Mar 4, re-run after fix) |

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
    "method_name":   "attachDetachChildChangesAndVerifyListView",  # last run (all 6 PASSED Mar 3)
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

## CH-2320 Workflow Statement Tuple Limit — Boundary Test Suite (as of Mar 2026)

> **Feature**: Statement tuple limit raised from 100 → 150 (connector limit 250 → 300)
> **Feature doc**: `docs/Feature_Document/CH-2320...md`
> **Pattern**: Each module gets 4 tests: API-reject(101), API-accept(100), UI-reject(101), UI-accept(100)

### Boundary Test Methods (all 5 modules implemented)

| Module | Class | IDs |
|--------|-------|-----|
| Incident Request | `IncidentRequestWorkflow.java` | `SDPOD_WF_TUPLE_LIMIT_IR_001–004` ✅ PASSING |
| Change | `ChangeWorkflow.java` | `SDPOD_WF_TUPLE_LIMIT_CH_001–004` ✅ PASSING |
| Problem | `ProblemWorkflow.java` | `SDPOD_WF_TUPLE_LIMIT_PB_001–004` |
| Service Request | `ServiceRequestWorkflow.java` | `SDPOD_WF_TUPLE_LIMIT_SR_001–004` |
| Release | `ReleaseWorkflow.java` | `SDPOD_WF_TUPLE_LIMIT_RL_001–004` |

### Stage-Based vs Flat-Status Module Classification

> **CRITICAL**: This distinction determines which `_UI()` implementation pattern to use.

| Module | Type | Blank canvas starts with | Override required? |
|--------|------|--------------------------|-------------------|
| Incident Request | Flat-status | Start + End (not counted) | ❌ Use base `_UI()` |
| Problem | Flat-status | Start + End (not counted) | ❌ Use base `_UI()` |
| Service Request | Flat-status | Start + End (not counted) | ❌ Use base `_UI()` |
| Change | **Stage-based** | Start + Submission + Close + End (counted!) | ✅ Must `@Override` |
| Release | **Stage-based** | Start + Submission + Closure + End (counted!) | ✅ Must `@Override` |

**Rule**: If a module uses Stages (not Statuses), the blank canvas starts with stage FlowNodes that the server counts in the statement tuple. Dragging 100 FieldUpdate nodes = 100 + baseCount > limit → always over limit. You must `@Override` `_UI()` methods in that module's workflow class.

### Recommended Pattern for UI Boundary Tests

**Stage-based modules (Change, Release)** — `@Override` required:
```java
@Override
protected void verifyStatementTupleLimitRejectionOnOverflow_UI() throws Exception {
    LocalStorage.store("workFlowModuleName", "change"); // lowercase module key!
    WorkflowsAPIUtil.createWorkflowViaAPI(
        getTestCaseData(WorkflowsDataConstants.WorkflowsData.CREATE_WORKFLOW_CHANGE_TRANSITION_VIA_API));
    String workflowId = LocalStorage.getAsString("workflowId");
    String wfName     = LocalStorage.getAsString("workFlowName");

    // Self-calibrate: actual baseCount may differ from assumption.
    int baseCount = 4; // Start + Submission + Close + End (conservative default)
    try {
        JSONObject wfResp = restAPI.get("workflows/" + workflowId, null);
        if (wfResp != null && wfResp.optJSONObject("workflow") != null) {
            org.json.JSONArray stmts = wfResp.getJSONObject("workflow").optJSONArray("statements");
            if (stmts != null) baseCount = stmts.length();
        }
    } catch (Exception ignore) {}

    int dragsNeeded = WorkflowsConstants.TupleLimit.DEFAULT_STATEMENT_LIMIT - baseCount + 1; // 101 total
    try {
        WorkflowsActionsUtil.openExistingWorkflowInCanvas("Change", wfName);
        actions.click(WorkflowsLocators.Listview.WORKFLOW_RHS_TOGGLE_BUTTON);
        for (int i = 1; i <= dragsNeeded; i++) {
            JSONObject fu = new JSONObject()
                .put("name", "FU_Overflow_" + i + "_" + System.currentTimeMillis())
                .put("field", "Impact").put("field_value", "Affects Business")
                .put("Setup_alternate_path_on_error", false);
            actions.dragAndDrop(WorkflowsLocators.Listview.DRAG_NODE_LOCATOR.apply("Field"),
                                WorkflowsLocators.Listview.DROP_CANVAS_LOCATOR);
            createFieldUpdate(fu);
        }
        actions.click(WorkflowsLocators.Listview.SAVE_MORE);
        actions.click(WorkflowsLocators.Listview.SAVE_CLOSE);
        actions.waitForAjaxComplete();
        if (actions.isElementPresent(WorkflowsLocators.Listview.WORKFLOW_CANCEL_LOCATOR)) {
            addSuccessReport("[CH-2320 UI] canvas correctly rejected " + (baseCount + dragsNeeded) + " statements");
            actions.click(WorkflowsLocators.Listview.WORKFLOW_CANCEL_LOCATOR);
        } else {
            addFailureReport("limit NOT enforced", "Expected rejection");
        }
    } finally {
        restAPI.delete("workflows/" + workflowId);
    }
}
```

**Flat-status modules (IR, Problem, SR)** — delegate to base:
```java
public void verifyIRWorkflowStatementTupleLimitRejectionOnOverflow() {
    try { verifyStatementTupleLimitRejectionOnOverflow(); }
    catch (Exception e) { addFailureReport("Error in " + getMethodName(), e.toString()); }
}
```

### Verifying UI Workflow Creation (CORRECT PATTERN)

After creating a workflow via `createWorkflow()` or `WorkflowsAPIUtil.createWorkflowViaAPI()`, **do NOT re-open the workflow in canvas by clicking its name in the list view** — this is fragile (timing, filter state). Instead, use API search:

```java
// ✅ CORRECT — API confirmation of save
String workflowId = restAPI.getEntityIdUsingSearchCriteria("workflows", "workflows", searchData);
if (workflowId != null && !workflowId.isEmpty()) {
    addSuccessReport("Workflow saved and confirmed via API — id=" + workflowId);
} else {
    addFailureReport("Workflow not found via API search after UI creation", workflowName);
}

// ❌ WRONG — fragile UI re-open
WorkflowsActionsUtil.openExistingWorkflowInCanvas("Change", workflowName);  // may fail on timing
if (actions.isElementPresent(WorkflowsLocators.Listview.WORKFLOW_RHS_TOGGLE_BUTTON)) { ... }
```

### Data Constants for Workflow API Creation

| Module | DataConstants key | JSON data key |
|--------|------------------|---------------|
| Change | `WorkflowsDataConstants.WorkflowsData.CREATE_WORKFLOW_CHANGE_TRANSITION_VIA_API` | `create_workflow_change_transition_via_api` |
| Release | `WorkflowsDataConstants.WorkflowsData.CREATE_WORKFLOW_RELEASE_TRANSITION_VIA_API` | `create_workflow_release_transition_via_api` |
| Incident | `WorkflowsDataConstants.WorkflowsData.CREATE_WORKFLOW_TRANSITION_VIA_API` | `create_workflow_transition_via_api` |

### runner_agent.py `_parse_success()` Fix (Mar 2026)

Two bugs were fixed in the HTML report override block:
1. **Wrong class string**: Was `'class=" error message-detail'` (leading space) — never matched actual `class="error message-detail default"`. Fixed: `'class="error message-detail'`
2. **Missing True→False demotion**: Old code only promoted `False→True`; never caught HTML FAILs when stdout falsely showed PASS signals. Fixed: added `else:` branch to demote when `'scenario-result FAIL' in content`

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
- **Creates prerequisite test data** via `SDPAPIHelper` before debugging (from report replay)
- LLM prompts include prerequisite context + SDP API cheatsheet for API failure fixes

### SDPAPIHelper (`agents/sdp_api_helper.py`)

Enables Playwright agents (HealerAgent + UIScoutAgent) to **create prerequisite test data
via SDP's browser JavaScript API** during debugging/scouting sessions.

#### How It Works
1. **Report parsing**: Reads `ScenarioReport.html` → extracts all `sdpAPICall()` invocations
   (method, path, formdata, response) with phase classification (preprocess / test / postprocess)
2. **Prerequisite replay**: Filters to preprocess POST calls → generates fresh `sdpAPICall()` JS
   with updated timestamps → executes via `page.evaluate()` in Playwright
3. **Cleanup**: Tracks all created entities → DELETEs them via API after session ends
4. **LLM context**: Generates human-readable prerequisite descriptions for LLM prompts

#### Key Classes
| Class | Purpose |
|-------|---------|
| `APICallRecord` | Dataclass: method, path, input_data, response, phase, data_key, created_id |
| `CreatedEntity` | Dataclass: api_path, entity_id, entity_name (for cleanup tracking) |
| `SDPAPIHelper` | Main helper — report parsing, JS building, Playwright execution |

#### Key Methods
| Method | Use |
|--------|-----|
| `build_create_js(api_path, data)` | Builds JS: `sdpAPICall(path, 'post', formData).responseJSON` |
| `build_delete_js(api_path)` | Builds JS: `sdpAPICall(path, 'del', ...).responseJSON` |
| `parse_report_api_calls(report)` | Parses HTML → list of `APICallRecord` (div-depth-counting for nested HTML) |
| `get_preprocess_creates(report)` | Returns only preprocess POST calls |
| `create_prerequisites_sync(page, method)` | **HealerAgent entry point** — replays preprocess POSTs |
| `create_prerequisites_async(page, ...)` | **UIScoutAgent entry point** — async version |
| `cleanup_entities_sync/async(page, entities)` | DELETEs all created entities |
| `get_entity_context_for_llm(method)` | Generates text for LLM prompts |
| `get_sdp_api_cheatsheet()` | Returns SDP API reference for LLM prompts |

#### Report Parsing Detail
- Uses **div-depth-counting** (not regex `(.*?)`) to handle nested `</div>` tags
  from notification template HTML embedded in POST response JSON
- Escapes control characters (newlines in notification templates) before `json.loads()`
- Phase detection: pre-first-UI-action = preprocess, DELETE calls = postprocess

#### MODULE_ENTITY_MAP
Covers: `changes`, `requests`, `solutions`, `problems`, `tasks`, `releases`
Each entry: `entity_name`, `api_path`, `data_json` path, `default_data_key`

#### Integration Points
- **HealerAgent** (`healer_agent.py`): After login, before module navigation →
  `create_prerequisites_sync()` → feeds `prereq_context` into `_extract_locator_fix()` prompt;
  `api_cheatsheet` injected into `_llm_generate_code_fix()` for API failures
- **UIScoutAgent** (`ui_scout_agent.py`): After login →
  `create_prerequisites_async()` → cleanup after scouting flows complete

---

### Playwright MCP — Data Creation SOP (Standard Operating Procedure)

> **Context**: When Copilot uses Playwright MCP tools (`browser_navigate`, `browser_click`,
> `browser_evaluate`, etc.) to debug locators or inspect UI, it may need to **create prerequisite
> test data** (changes, requests, solutions, etc.) to reach the correct UI state.

#### Fallback Chain (MANDATORY — follow in order)

```
Need to create prerequisite data during Playwright MCP session?
│
├── Step 1: browser_evaluate → sdpAPICall() JS  (PREFERRED — fastest, no UI fragility)
│   │
│   │  () => sdpAPICall('changes', 'post',
│   │    'input_data=' + JSON.stringify({
│   │      change: { title: "Test Change " + Date.now(), change_type: { name: "Standard" } }
│   │    })
│   │  ).responseJSON
│   │
│   │  ⚠️  Do NOT use encodeURIComponent — pass raw JSON.stringify() directly.
│   │
│   ├── Success? → Parse response, extract entity ID, continue debugging
│   └── Failed (null response / JS error)?
│       │
│       ▼
├── Step 2: Run sdp_api_helper.py via terminal
│   │
│   │  .venv/bin/python -c "
│   │  from agents.sdp_api_helper import SDPAPIHelper
│   │  helper = SDPAPIHelper()
│   │  # Use helper methods for complex multi-entity setup
│   │  "
│   │
│   ├── Success? → Entities created, continue in Playwright MCP
│   └── Failed?
│       │
│       ▼
└── Step 3: Create via UI clicks in Playwright MCP  (LAST RESORT — slowest, most fragile)
    │
    │  browser_navigate → module page
    │  browser_click → "New" button
    │  browser_fill_form → fill fields
    │  browser_click → "Save"
    │
    └── If this also fails → report to user, do not retry indefinitely
```

#### sdpAPICall() Quick Reference (for browser_evaluate)

| Module | API Path | Input Wrapper |
|--------|----------|---------------|
| Changes | `changes` | `{ "change": {...} }` |
| Requests | `requests` | `{ "request": {...} }` |
| Solutions | `solutions` | `{ "solution": {...} }` |
| Problems | `problems` | `{ "problem": {...} }` |
| Tasks | `tasks` | `{ "task": {...} }` |
| Releases | `releases` | `{ "release": {...} }` |
| Assets | `assets` | `{ "asset": {...} }` |
| Projects | `projects` | `{ "project": {...} }` |
| Purchase Orders | `purchase_orders` | `{ "purchase_order": {...} }` |
| Contracts | `contracts` | `{ "contract": {...} }` |
| CMDB (Business Views) | `business_views` | `{ "business_view": {...} }` |

> Full API paths, required fields, and sub-resource patterns for every module are in [`docs/api-doc/SDP_API_Endpoints_Documentation.md`](docs/api-doc/SDP_API_Endpoints_Documentation.md). Read the relevant module section before creating prerequisite data in a new module.

```javascript
// CREATE — returns response JSON with entity ID
// Use short path ('changes') OR full path ('/api/v3/changes') — both work
// CRITICAL: raw JSON.stringify only — do NOT use encodeURIComponent
() => sdpAPICall('changes', 'post',
  'input_data=' + JSON.stringify({ change: { title: "Test " + Date.now() } })
).responseJSON

// READ — get entity by ID
() => sdpAPICall('changes/12345', 'get').responseJSON

// DELETE — cleanup after debugging
() => sdpAPICall('changes/12345', 'del').responseJSON

// SUB-RESOURCE create (e.g. note on a request) — use full path with parent ID
() => sdpAPICall('requests/8000000012345/notes', 'post',
  'input_data=' + JSON.stringify({ note: { description: "Test note " + Date.now() } })
).responseJSON
```

#### Prerequisites
- Browser must be on a **logged-in SDP page** (any page — JS API is global)
- Admin session preferred (user sessions may lack permissions for certain entities)
- Always **clean up created entities** after debugging session via DELETE calls

#### Cleanup Pattern
After every Playwright MCP debugging session that created test data:
1. Track all created entity IDs during the session
2. Before closing, run DELETE for each: `sdpAPICall('<module>/<id>', 'del').responseJSON`
3. If session was interrupted, note leftover entity IDs for manual cleanup

---

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
| **8 — Shared Central ChromaDB** | 🔲 | — | Single shared ChromaDB server for the whole team — prevents cross-person duplicate generation; nightly reindex from Mercurial; `VectorStore` configurable via `CHROMA_SERVER_URL` in `.env` (local `persist_dir` remains the fallback); write-lock for concurrent OutputAgent upserts (see `docs/pipeline-flow.md` Phase 8 spec) |

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
