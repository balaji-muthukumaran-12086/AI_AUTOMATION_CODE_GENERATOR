# AutomaterSelenium Framework — Copilot Instructions

This workspace is a **Selenium-based Java automation QA framework** for the ServiceDesk Plus (SDP) product.
Always read this file before inferring anything about the project structure.

> **Active project**: determined by `PROJECT_NAME` in `.env` (default: `SDPLIVE_LATEST_AUTOMATER_SELENIUM`)
> Single source of truth: `config/project_config.py` → `PROJECT_NAME`
> All agents, runner, healer, and ingestion now derive paths from this config.

### Companion Reference Files

This file provides the primary overview. For deeper coverage, **read these files before generating or modifying test code**:

| File | When to read | What it contains |
|------|-------------|-----------------|
| `config/framework_rules.md` | Writing `@AutomaterScenario`, preProcess groups, annotations, reporting patterns | Strict rules with numbered sections — annotation fields, valid values, forbidden patterns, checklists |
| `config/framework_knowledge.md` | Debugging failures, understanding framework internals, lifecycle questions | Deep-dive knowledge — Entity/EntityCase lifecycle, REST API internals, compilation, worked examples |
| `.github/instructions/java-test-conventions.instructions.md` | Editing any `*.java` file under `src/` (auto-loaded by `applyTo` pattern) | Concise Java-specific conventions — ActionsUtil/APIUtil patterns, data loading, locator rules |
| `.github/instructions/test-data-format.instructions.md` | Editing `*_data.json` files (auto-loaded by `applyTo` pattern) | JSON data format rules — `{"data": {...}}` wrapper, placeholders, lookup field format |
| `.github/instructions/token-budget-rules.instructions.md` | **ALWAYS** (auto-loaded for all files) | Token budget limits, session management, file reading rules, edit batching |

> The `.github/instructions/` files are auto-loaded when editing matching files. The `config/` files are NOT auto-loaded — read them explicitly when the task involves annotations, preProcess groups, or framework internals.

### Token-Efficient Context Loading (MANDATORY)

> **Problem**: Framework files are 1500–2500 lines each. Reading them in full burns 12K–20K tokens
> per read. Agents that read 3-4 files in full consume 50K+ tokens before writing a single line of code.

**Loading order (from cheapest to most expensive):**

| Step | File | Lines | ~Tokens | When to stop |
|------|------|-------|---------|-------------|
| 1 | `config/critical_rules_digest.md` | ~150 | ~1,200 | Covers 80% of rules — stop here if sufficient |
| 2 | `config/framework_file_index.yaml` | ~140 | ~1,100 | Identifies exact chunks for targeted reads |
| 3 | Targeted chunk from full file | 50-200 | ~400-1,600 | Read ONLY the chunk relevant to your task |
| 4 | `CHANGELOG.md` (top 30 lines) | ~30 | ~250 | Understand recent changes |

**NEVER read framework_rules.md, framework_knowledge.md, or copilot-instructions.md in full.**
Use `config/framework_file_index.yaml` to find the relevant chunk, then `read_file(startLine, endLine)`.

### Session Management Hard Rules

1. **One phase per chat session** — planning, generation, execution, debugging are separate sessions
2. **CHANGELOG.md checkpoint** — update at end of every session before closing
3. **Batch edits** — use `multi_replace_string_in_file` for 3+ edits, never sequential single-edits
4. **Compile once** — fix ALL errors in a batch, then recompile once (not per-error)
5. **Never re-read** — after reading a file once, reference from memory; do not read again

### Requirement-First Workflow (for tasks involving 3+ files)

1. Create a requirement doc (template: `docs/templates/requirement_template.md`)
2. Create an implementation plan (template: `docs/templates/implementation_plan_template.md`)
3. Execute phase-by-phase, one session per phase
4. Checkpoint to CHANGELOG.md between phases

### Skills & Tools Inventory

Before starting complex work, check `config/skills_manifest.yaml` for the full registry of
available agents, LLM providers, knowledge base tools, scripts, and templates.

---

## Agent Routing — NEVER delegate MCP-dependent agents to subagents

> **Critical platform limitation**: `runSubagent()` creates a sandboxed child context that
> **cannot use MCP tools** (Playwright, etc.). MCP permissions are per-session and not inherited.
>
> When the user asks to run tests (`@test-runner`, "run batch", "run all tests"), **execute
> the test-runner workflow DIRECTLY in the current chat session** — never via `runSubagent()`.
> The current session has working MCP access; subagents do not.
>
> **Affected agents** (require MCP tools — must run inline):
> - `test-runner` — needs Playwright MCP for UI diagnosis
> - `test-debugger` — needs Playwright MCP for locator inspection
> - `product-discovery` — needs Playwright MCP to explore live SDP product
>
> **Safe to delegate via `runSubagent()`** (no MCP dependency):
> - `test-generator` — only generates code, no browser needed
> - `setup-project` — hg clone and config, no browser needed
> - `Explore` — read-only codebase search, no browser needed

When executing the test-runner workflow inline, follow the full workflow documented in
`.github/agents/test-runner.agent.md` — resolve paths, bootstrap Playwright, compile,
run each test, diagnose failures with `browser_snapshot`, fix, recompile, re-run.

---

## Project Structure

```
ai-automation-qa/
├── $PROJECT_NAME/                      # ACTIVE — Module-specific tests (gitignored, managed via Mercurial)
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
│   │       ├── <Entity>DataConstants.java # Enum-style data key constants (auto-generated from *_data.json)
│   │       ├── <Entity>AnnotationConstants.java # Group/Data string constants for @AutomaterScenario (hand-written)
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
    └── automater-selenium-framework-*.zip  # Framework source ZIP — readable via unzip -p
```

> **Framework source ZIP**: When you need to verify which framework methods call `waitForAjaxComplete()` internally,
> check method signatures, or read any base class implementation, extract from the framework ZIP:
> ```bash
> FW_ZIP=$(find "$DEPS_DIR" -name 'automater-selenium-framework-*.zip' | head -1)
> unzip -p "$FW_ZIP" "com/zoho/automater/selenium/base/Actions.java" | grep -n "pattern"
> ```
> Key source files inside: `Actions.java` (click, type, sendKeys, getText), `Navigate.java`, `FormBuilder.java`, `Validator.java`, `SDPCloudActions.java`, `RestAPI.java`.

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

### MSP (Managed Service Provider) Cases — SKIP for Now

> **MSP case generation is NOT available yet.** MSP uses a different instance/portal with
> customer-based UI and has framework-specific tweaks that are not yet supported in this
> automation setup. When analyzing use-case CSVs:
> - If a row's `IS MSP/ SDP` column = `MSP`, or the Module/Description indicates MSP → **skip it**
> - Report skipped MSP rows in the plan summary: `MSP (skipped — not available yet): {count}`
> - Do NOT generate any test code, data entries, or annotations for MSP scenarios
> - MSP-specific automation will be added later once the framework supports it

---

## Test Lifecycle

> ⚠️ **UNIVERSAL RULE — UI Testing, NOT API Testing**: This is a UI automation framework. Every
> `@AutomaterScenario` test method MUST exercise the actual UI flow (Selenium clicks, navigation,
> form fills, validations). API calls in test method bodies are **FORBIDDEN** — they turn the test into
> API testing. Only `preProcess` should use API calls for data setup. If no API exists for prerequisite
> data, `preProcess` may use UI-based setup as a fallback. This applies to ALL features universally.

1. **preProcess** (driven by `@AutomaterScenario(group=..., dataIds={...})`)
   - Creates prerequisite **entities** via REST API (changes, requests, templates, users, etc.)
   - Sets prerequisite **state** via API (trash a change, close a change for testing something else)
   - If API is unavailable for the prerequisite, UI-based setup is acceptable as fallback
   - Stores IDs/names in `LocalStorage` (e.g., `"solution_template"`, `"topic"`)
   - **NEVER performs the feature/action under test** — preProcess is for data/state setup ONLY

2. **Test method** (in `<Entity>Base.java`) — **UI-ONLY**
   - Loads data: `getTestCaseData(DataConstants.SomeKey)` → resolves `$(placeholders)` from LocalStorage
   - **Performs the feature under test via UI** — linking, associations, form fills, status changes
   - Validates result via UI (getText, isElementPresent, etc.)
   - **NEVER** calls `restAPI.*` or `*APIUtil.*` methods — that would be API testing

> ⚠️ **"Data creation" vs "Feature under test"**: preProcess API creates entities that need to
> EXIST. The **action being tested** (linking, approving, associating, etc.) MUST be done via UI
> in the test method. If a test verifies "link child change", preProcess creates the two changes,
> the test method performs the linking via UI clicks. If a test verifies "trashed change not in
> popup", preProcess creates + trashes one change, the test method opens the popup via UI and
> verifies absence.

3. **postProcess** — deletes created entities via REST API

---

## Data & Field Config

### `entity/conf/<entity>.json` — field config loaded into `fields` Map
```json
{ "name": "template", "field_type": "select", "data_path": "template.name" }
```
All `FieldType` constants (full list from source):
```
Handled by fillInputForAnEntity:
  "input", "select", "multiselect", "html", "date", "datetime",
  "textarea", "criteria", "pickList", "attachment"

NOT handled by fillInputForAnEntity (silent skip — manual click required):
  "checkbox", "radio", "selectonly", "selectaction",
  "mappedfield", "systemSelect", "selectRelationship", "ipaddress"
```

> ⚠️ **No `boolean` field_type exists.** `fillInputForAnEntity` calls
> `getValueAsStringFromInputUsingAPIPath()` which returns `null` for JSON booleans →
> boolean fields (like `is_public`) are **silently skipped**.
> Checkboxes/radio buttons must be handled manually via explicit `actions.click(locator)`.
> Note: `FieldType.PICKLIST = "pickList"`, `FieldType.SYSTEMSELECT = "systemSelect"`, `FieldType.SELECTRELATIONSHIP = "selectRelationship"` use camelCase values (not all-lowercase) — match exactly in conf JSON.

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
This compiles 90+ framework source files into `$PROJECT_NAME/bin/`, overriding old classes
from `AutomationFrameWork.jar`. The script auto-detects the framework source using this
priority chain:
1. `AutomaterSeleniumFramework/` hg repo (maintainers only — has the full source tree)
2. `automater-selenium-framework-*.zip` in `$DEPS_DIR` (all users — extracted & compiled automatically)
3. Pre-compiled framework classes already in `bin/` from the hg clone (fallback — no compilation)

**Required** because `EntityCase`, `ScenarioReport`, `LocalSetupManager` etc. need the
local-run versions for reports/screenshots to work correctly (`isLocalSetup()` guards).

> ⚠️ **NEVER copy `bin/` from another project folder** (e.g., `.SDPLIVE_LATEST_AUTOMATER_SELENIUM/`)
> as a workaround for compilation failures. Each project's `bin/` must be self-contained.

### Step 2 — Module targeted compile (after editing module source):
```bash
# Derive paths from project_config.py (single source of truth — reads .env)
DEPS=$(.venv/bin/python -c "from config.project_config import DEPS_DIR; print(DEPS_DIR)")
BIN=$(.venv/bin/python -c "from config.project_config import PROJECT_ROOT, PROJECT_NAME; print(PROJECT_ROOT + '/' + PROJECT_NAME + '/bin')")
SRC=$(.venv/bin/python -c "from config.project_config import PROJECT_ROOT, PROJECT_NAME; print(PROJECT_ROOT + '/' + PROJECT_NAME + '/src')")
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
| Test user emails | `SDP_TEST_USER_EMAILS` | comma-separated emails for TEST_USER_1..4 (empty = keep hardcoded defaults) |
| Orchestrator dashboard | `ORCHESTRATOR_URL` | `http://localhost:9600` |
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
`$PROJECT_NAME/reports/LOCAL_<methodName>_<timestamp>/ScenarioReport.html`

Screenshots at: `reports/LOCAL_<methodName>_<timestamp>/screenshots/Success_<ts>.png`

> ⚠️ Report filename changed from `ScenarioLogDetails__.html` (Aalam mode) to `ScenarioReport.html` (local mode)

---

## Key Framework Behaviours

| Behaviour | Detail |
|-----------|--------|
| `actions.click(locator)` | Calls `waitForAjaxComplete()` **before** clicking — NEVER add `waitForAjaxComplete()` between consecutive clicks (redundant). Only add it after a click if the next action is a non-click read (`getText`, `isElementPresent`) that depends on AJAX completion |
| `actions.type(locator, value)` | Calls `waitForAjaxComplete()` internally — no need to add before `type()` |
| `actions.sendKeys(locator, value)` | Calls `waitForAjaxComplete()` internally |
| `actions.getText(locator)` | Calls `waitForAjaxComplete()` internally + has **3-second** `waitForAnElementToAppear` timeout — can miss slow-loading pages |
| `actions.navigate.to(locator)` | Calls `click()` + `waitForAjaxCompleteLoad()` — double-wait internally |
| `actions.navigate.toModule(name)` | Calls `to()` + additional `waitForAjaxComplete()` — fully waited |
| `actions.navigate.toDetailsPageUsingRecordId(id)` | Calls `waitForAnElementToAppear` + `to()` + `waitForAjaxComplete()` — fully waited |
| `fillInputForAnEntity` | Skips fields where value is `null` (including all JSON booleans); also silently skips `checkbox`, `radio`, `selectonly`, `selectaction`, `mappedfield`, `systemSelect`, `selectRelationship`, `ipaddress` types |
| `PORTAL_BASED` scenario + `UserBased` flow | Scenario is **SKIPPED** (not FAILED) — `scenarioDetails.setRestrictRerun(true)` called; incompatible run type, not an error |
| `fillDateField(name, millis)` | Opens datepicker → navigates by year/month arrows → clicks day cell |
| `LocalStorage` | Scoped to single test run; key `"solution_template"` → template name, `"topic"` → topic name |
| `MODULE_TITLE` locator | `//div[@id='details-middle-container']/descendant::h1` — may include display ID prefix (e.g. `SOL-8Title...`) |
| Local run report flow | `EntityCase.addSuccessReport()` → `LocalFailureTemplates` + `ScenarioReport` rows + `screenshots/Success_<ts>.png` → `Entity.run()` finally → `ScenarioReport.createReport()` → `ScenarioReport.html` |
| `AutomationReport` (Aalam/CI) | NOT used in local runs — guarded by `!LocalSetupManager.isLocalSetup()` in `EntityCase`. Old JAR version has no guard → `IOException` when `REPORT_FILE_PATH` is null. Always compile framework via `setup_framework_bin.sh` to get the guarded version. |
| `addReport(message)` | Smart variant — inspects `failureMessage.length()`: `== 0` → `addSuccessReport(message)`; `> 0` → `addFailureReport(message, failureMessage)`. Use after validation blocks where `failureMessage` accumulates errors. **`clearFailureMessage()` is called automatically** inside every `addReport()` / `addSuccessReport()` / `addFailureReport()` call (verified in EntityCase.java source). Only call `clearFailureMessage()` manually if you need to **discard** accumulated failures mid-step before reporting. |

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
| `restAPI.createAndGetAPIResponse(apiPath, inputData)` | JSONObject raw response | Alias for `createAndGetFullResponse()` — same result |
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

### `preProcess` Exception Handling
`preProcess` exception handling varies by module — some modules (e.g. `Solution.java`) use `catch(Exception) { return false; }` which **silently swallows** exceptions — test is skipped with zero visibility. Other modules (e.g. `ProblemsCommonBase.java`) call `addFailureReport(...)` before `return false` — visible in report.

**Rule for NEW code**: Always use `addFailureReport()` in preProcess catch blocks — never silent swallow. Failure visibility is critical for the self-healing process.
```java
// ✅ CORRECT — failure visible in ScenarioReport:
} catch(Exception exception) {
    report.addCaseFlow("Exception occurred while pre processing: " + exception);
    addFailureReport("Pre-process failed", exception.getMessage());
    return false;
}

// ❌ FORBIDDEN in new code — silent skip, impossible to debug:
} catch(Exception exception) {
    return false;
}
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

> Java modules follow the pattern: `$PROJECT_NAME/src/com/zoho/automater/selenium/modules/<module>/<entity>/`  
> Framework source: `AutomaterSeleniumFramework/src/com/zoho/automater/selenium/base/`  
> **API reference**: `docs/api-doc/SDP_API_Endpoints_Documentation.md` — V3 API paths, input wrappers and automation cases for all 16 modules. Read before writing any `preProcess` API call.

```bash
# Discover files for any entity:
find $PROJECT_NAME/src -path "*modules/<module>/<entity>*" -name "*.java"
```

---

## Common Pitfalls

- **`SOLUTION_ADD` vs `SOLUTION_ADD_APPROVE`**: Always use `normalize-space(text())='Add'` for exact match
- **Checkbox fields**: Must click via explicit locator — never rely on `fillInputForAnEntity` for booleans
- **Data key naming**: `SOL_UNAPPROVED_PUB_*` maps to snake_case `sol_unapproved_pub_*` in JSON
- **Template/topic setup**: Must be in `preProcess` group `CREATE_CUST_TEMP_TOPIC` — stores under `"solution_template"` and `"topic"` in LocalStorage
- **`$(custom_solution_template)`**: Strips `custom_` prefix → looks up `"solution_template"` in LocalStorage
- **Select2 dropdowns**: Render option `<li>` elements in `<div class="select2-drop">` appended to `<body>` — NOT inside the parent dialog/popup. Use `//div[contains(@class,'select2-result-label')]` to match options.
- **SDP Associations tab container ID**: `change_associations_parent_change` (not `change_associations_linked_changes`). Attach button has `name="associating-change-button"`.
- **Local run reports/screenshots**: Always compile with `setup_framework_bin.sh` first — old JAR lacks `isLocalSetup()` guards → `IOException` on null `REPORT_FILE_PATH`.
- **Checkstyle NeedBraces**: ALL block statements require braces — `if`, `else`, `for`, `while`, `catch`, `finally`. Inline `} catch (Exception ignore) {}` is FORBIDDEN; always expand to multi-line.
- **`preProcess` exception handling varies by module**: Some modules (e.g. `Solution.java`) silently swallow exceptions in catch blocks — test is skipped with zero visible error. Always use `addFailureReport()` in preProcess catch blocks in new code.
- **Module misplacement**: Always derive module from the use-case noun, NOT from the currently open file. `"create incident request"` → `modules/requests/request/`, never solutions.
- **`FieldDetails` constructor takes 6 parameters**: `new FieldDetails(name, apiPath, apiKey, FieldType, isCustom, isUDF)`. Writing 4 args compiles broken. The `apiKey` (3rd) and `apiPath` (2nd) are separate fields from the conf JSON.
- **DataConstants constant name = raw `.toUpperCase()`**: JSON key `"create_change_api"` → constant `CREATE_CHANGE_API`. Always use `snake_case` keys in `*_data.json` — `camelCase` keys like `"createChange"` become the unreadable `CREATECHANGE`.
- **New entity scaffolding**: Run `GenerateSkeletonForAnEntity.java` (set `MODULE_NAME` + `ENTITY_NAME` in PascalCase, run `main()`) to generate the 7 Java stubs + 3 resource files. **Do NOT create entity files by hand.** After skeleton runs, fill `plural_name` + `api_path` in the conf JSON.

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
    runType     = ScenarioRunType.USER_BASED       // ⚠️ ALWAYS explicit — default is PORTAL_BASED
    // switchOn omitted → defaults to SwitchToUserSession.AFTER_PRE_PROCESS
    // Use switchOn = SwitchToUserSession.BEFORE_PRE_PROCESS when preProcess must run in user session
    // Use switchOn = SwitchToUserSession.NEVER when entire test must run in admin session
)
```

> ⚠️ **`runType` trap**: Annotation default is `PORTAL_BASED`. **Always write `runType = ScenarioRunType.USER_BASED` explicitly. Never omit it.**
>
> **When to use `PORTAL_BASED`**: For scenarios that have side effects on other tests in the suite — e.g. business rules, SLA triggers, automation rules. These run in an **isolated session**: effects are scoped and cleaned up within that session so they don't contaminate other test cases in the same suite run. `USER_BASED` is for all standard scenarios whose execution does not affect global state seen by other tests.

### Test ID Source — Use-Case Document vs Fallback

> **Use-case documents** (CSV, XLSX, or XLS) are located in `$PROJECT_NAME/Testcase/` after cloning.
> XLSX/XLS files are auto-converted to CSV by the test-generator agent before processing.
> These contain manual test case IDs used directly as `@AutomaterScenario(id)`.
> Template: `docs/templates/usecase_template.csv`
>
> **Feature documents** (optional) can be placed in `$PROJECT_NAME/Testcase/Feature_Document/`
> alongside the use-case CSV. These provide **product knowledge only** (UI flows, API endpoints,
> business rules, edge cases) that the test-generator loads as context before generating code.
> They do NOT control what to generate — the CSV does. Feature docs improve generation accuracy.
> Supported formats: `.md`, `.pdf`, `.docx`, `.doc`, `.txt` (PDF/DOCX are auto-converted to text).
> Template: `docs/templates/feature_document_template.md`

#### Use-Case Document Column Definitions

| Column | Maps to | Rules |
|--------|---------|-------|
| **UseCase ID** | `@AutomaterScenario(id = "...")` | Use as-is in annotation. NEVER embed in method names, data keys, or locator names. |
| **Severity** | `@AutomaterScenario(priority = ...)` | `Critical` → `Priority.HIGH`, `Major` → `Priority.MEDIUM`, `Minor` → `Priority.LOW` |
| **Module** | Parent entity/module path | Maps to `modules/<module>/` — determines which parent class to extend. See module placement table below. |
| **Sub-Module** | Leaf entity class | Maps to an existing subclass under the module. If no matching subclass exists, find the nearest match. If no relevant subclass at all, generate entity skeleton (`GenerateSkeletonForAnEntity`) and create a new subclass extending the parent. |
| **Impact Area + Pre-Requisite + Description** | Combined scenario logic | Cumulate all three columns to understand the full test scope. Generate a scenario covering all validation points. If coverage is too large for one method, split into multiple scenarios with the same UseCase ID appended with `_1`, `_2`, etc. (e.g., `SDPOD_MODULE_001`, `SDPOD_MODULE_001_1`). |
| **UI To-be-automated** | Filter gate | **Only generate automation for rows where this column = `Yes`**. Skip all rows with `No` or blank — these are API-only or manual-only cases. |

#### Sub-Module → Entity Class Resolution

```
Sub-Module value in CSV
  ↓
  Step 1: Does an existing leaf class match the Sub-Module name exactly?
  → YES: Place scenario in that class
  ↓ NO
  Step 2: Is the Sub-Module a FEATURE or TAB within an existing view?
  → YES: Place in the existing view class that owns that feature.
         DO NOT create a new entity class for a feature/tab.
  ↓ NO
  Step 3: Is there a close match in the module?
  → YES: Use that class (prefer existing over creating new)
  ↓ NO
  Step 4: Generate entity skeleton (LAST RESORT — only for genuinely new entities
          like ChangeWorklog, ChangeTask, ChangeConversations that have their own
          API path, own data JSON, own field config):
          run GenerateSkeletonForAnEntity.java with MODULE_NAME + ENTITY_NAME
```

**Step 2 applies to ALL modules — not just Changes.** Examples across modules:

| Sub-Module in CSV | Module | Is it a feature/tab? | Correct placement |
|---|---|---|---|
| Linking Change / Associations | Changes | YES — Associations tab | `DetailsView.java` (changes/change/) |
| Approval | Changes / Requests | YES — Approval section in DV | `DetailsView.java` or stage class |
| Notes | Requests / Problems | YES — Notes tab in DV | `DetailsView.java` or existing `*Notes.java` if present |
| Resolution | Requests | YES — Resolution tab in DV | `DetailsView.java` (requests/request/) |
| Bulk Actions | Any module | YES — List view feature | `ListView.java` |
| Column Search / Filters | Any module | YES — List view feature | `ListView.java` |
| Custom Fields / UDF | Any module | YES — Form/DV feature | `DetailsView.java` or parent entity |
| Solution Comments | Solutions | YES — Comments tab in DV | `DetailsView.java` (solutions/solution/) |
| Stage Transition | Changes / Releases | YES — Stage flow | `<Stage>Stage.java` |
| Change Worklog | Changes | **NO — own API** (`changes/{id}/worklogs`) | `ChangeWorklog.java` (separate entity) |
| Change Task | Changes | **NO — own API** (`changes/{id}/tasks`) | `ChangeTask.java` (separate entity) |

> **Decision rule**: Does the sub-module have its **own REST API endpoint** (own CRUD path like
> `<module>/{id}/<sub-resource>`)? NO → it's a feature/tab → existing view class.
> YES → genuine sub-entity → skeleton generation is justified.

#### When a Use-Case Document (CSV/XLSX/XLS) Is Provided

1. **Read the CSV** in `$PROJECT_NAME/Testcase/` — each row has a use-case ID (e.g. `SDPOD_SFCMDB_ADMIN_001`)
2. **Use the use-case ID as-is** in `@AutomaterScenario(id = "...")` — this is the ONLY place the use-case ID appears
3. **Do NOT embed the use-case ID** in method names, DataConstants names, data JSON keys, locator names, or any other identifier
4. Method names must be descriptive of the action (e.g. `verifyDetailViewTitle`), not derived from the ID

```java
// ✅ CORRECT — use-case ID directly as annotation id, descriptive method name
@AutomaterScenario(
    id = "SDPOD_SFCMDB_ADMIN_001",  // from CSV UseCase ID column
    description = "Verify sub-form page loads under Setup > Customization",
    ...
)
public void verifySubFormPageLoads() throws Exception { ... }  // descriptive name

// ❌ FORBIDDEN — use-case ID leaked into method name
public void SDPOD_SFCMDB_ADMIN_001() throws Exception { ... }

// ❌ FORBIDDEN — use-case ID in data key
"SDPOD_SFCMDB_ADMIN_001_data": { ... }
```

#### When No Use-Case Document Is Provided (Feature Description / Single-Line Case)

Fall back to the **auto-generated sequential ID pattern** per module (same as above):

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
grep -rn 'id = "SDPOD_AUTO_SOL_DV' $PROJECT_NAME/src/ | \
  sed 's/.*id = "\([^"]*\)".*/\1/' | sort | tail -1
```

#### Decision Flow for Scenario ID

```
Use-case CSV exists in $PROJECT_NAME/Testcase/ ?
  → YES: Use CSV use-case ID directly as @AutomaterScenario(id = "...")
         Keep method names descriptive (verifyXxx, createXxx) — NEVER from the ID
  → NO:  Generate next sequential ID using the module prefix pattern above
```

### Multi-ID Grouping — Map Multiple Manual Cases to One Automation Scenario

When **multiple manual test cases** from the use-case document can be covered by a **single automation test method**, comma-separate the CSV use-case IDs in the `id` field:

```java
@AutomaterScenario(
    id = "SDPOD_SFCMDB_ADMIN_001,SDPOD_SFCMDB_ADMIN_002",
    description = "Verify Updated By column in list view",
    ...
)
public void verifyUpdatedByColumnInListView() throws Exception { ... }
```

**Rules:**
- Each comma-separated ID in `id` is a CSV use-case ID (one per CSV row covered)
- Only group cases that are genuinely validated within the same method — do not pad IDs for coverage
- The method's `description` should summarize the combined coverage
- Use-case CSV rows that map to the same grouped method should each list the automation method name

### Valid preProcess Groups — Generic Rules

> `preProcess()` is an **abstract method** defined in `Entity.java` (the base class):
> ```java
> protected abstract boolean preProcess(String group, String[] dataIds);
> ```
> Every entity MUST implement it. The `group` parameter selects which if/else or switch-case block
> to execute. The `dataIds` array is optional — some groups need them, some don't.

**Group + dataIds combinations:**

| Scenario | group | dataIds | Meaning |
|---|---|---|---|
| No data creation needed | `""` or `"NoPreprocess"` | `{}` | preProcess skips or returns `true` immediately — no API calls, no cleanup |
| Group handles creation internally | e.g. `"create"` | `{}` | preProcess runs the matching block; data creation is hardcoded inside (no dataIds needed) |
| Group uses passed dataIds | e.g. `"create"` | `{AnnotationConstants.Data.KEY1, ...}` | preProcess uses `getTestCaseDataUsingCaseId(dataIds[0])`, `dataIds[1]`, etc. by index |

**The purpose of `group`** is solely to match which preProcess block should execute.
preProcess can use `if/else-if` chains or `switch` statements — both are valid.

> ⚠️ **FORBIDDEN**: Inventing new group strings when an existing group already creates the same entity type and stores the same LocalStorage keys you need. Always **read the entity's existing preProcess()** before adding a new group. Only create a new group when genuinely different setup is required.

### Where `preProcess()` lives — check subclass first, then parent

`preProcess()` is an **abstract method** in `Entity.java`:
```java
protected abstract boolean preProcess(String group, String[] dataIds);
```
It is often implemented in the **module parent class**, but **subclasses can and do
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

### ⭐ Minimal Group Selection (MANDATORY — apply to every scenario)

> **Root cause of past bugs**: Assigning the heaviest preProcess group to ALL scenarios
> "just in case" — wastes API calls, slows test suite, creates unnecessary cleanup.

Always select the **lightest** group that satisfies the test method's actual data needs:

```
1. Does the test method use any entity created by preProcess (getEntityId(), LocalStorage)?
   → NO:  group = "NoPreprocess", dataIds = {}
2. Does it ONLY use getEntityId() (the base entity)?
   → YES: use simplest group (e.g., "create") + single data template
3. Does it reference extra entities (linkChange_*_id, multiple IDs from LocalStorage)?
   → YES: use the heavy multi-entity group
```

> **FORBIDDEN**: Defaulting all scenarios to the heaviest group.

### Role Constants (module-specific — import matters)

```java
// Requests module only:
RequestsRole.SDADMIN  |  RequestsRole.FULL_CONTROL  |  RequestsRole.VIEW_ONLY  |  RequestsRole.REQUESTER1

// All other modules:
Role.SDADMIN  |  ModulesRoleSkeleton.SDADMIN
```

**SDADMIN = no session split.** When `role = Role.SDADMIN` and the scenario user email is the admin email, `switchToUserSession()` logs back in as admin — so both `preProcess` **and** the test method run in the admin session. API calls inside the test method body are safe with `Role.SDADMIN`. For any non-admin role, API calls in the test method body run in the restricted user session and will fail.

**`getRoleDetails()` lookup order** — looks up `general.json` first (contains `sdadmin`, `sdsite_admin`, `sdguest`), then falls back to `<module>.json`. Module entry wins if the same key exists in both.

**Role JSON structure** (for writing new entries in `resources/entity/roles/<module>.json`):
```json
"My_Role": {
  "user": {
    "roles": [{"name": "My_Role"}],
    "default_project_role": {"name": "Project Admin"}
  },
  "custom_roles": {
    "My_Role": {
      "permissions": [
        {"name": "ViewSolutions"},
        {"name": "CreateSolutions"}
      ],
      "description": "..."
    }
  },
  "is_technician": true
}
```
- `is_technician: true` → `createTechnician()` path; `false` → `createRequester()` path
- `custom_roles` block → framework ensures the custom role exists in SDP before assigning (creates it via UI if missing)
- Requester entries omit `custom_roles` and `roles[]`; include `login_user`, `requester_allowed_to_view`, etc.

### ⚠️ RBAC Scenario Pattern — MANDATORY for Role-Based Tests

> **Any scenario testing role-based access/permissions MUST follow the `createUserByRole` → `switchUser` flow.**
> Running RBAC tests as admin verifies nothing — admin always has all permissions.
> This applies to ALL modules: Changes, Requests, Problems, Solutions, Assets, Releases, Projects, CMDB, Admin, etc.

**Required flow:**

1. **preProcess**: Clean slate + create user with the target role
```java
// Step 0: Always clean up stale user from prior runs
deleteScenarioUser(ScenarioUsers.TEST_USER_3);

// Step 1: Create user with role
User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
// moduleName = "changes", "requests", "problems", "solutions", etc.
// roleConfigKey = key in resources/entity/roles/<module>.json or general.json
actions.createUserByRole(AutomaterConstants.TECHNICIAN, getModuleName(), "roleKey", user);
LocalStorage.store("techName", user.getDisplayId());
```

2. **Test method**: Switch to that user, test under their permissions
```java
User user = scenarioDetails.getUser(ScenarioUsers.TEST_USER_3);
actions.switchUser(user);
// All subsequent UI actions run under the role user's permissions
actions.navigate.toModule(getModuleName());
// ... verify what this user CAN or CANNOT do ...
switchToAdminSession();  // switch back if needed
```

**`createUserByRole` signature:**
```java
actions.createUserByRole(
    String userType,      // AutomaterConstants.TECHNICIAN or AutomaterConstants.REQUESTER
    String moduleName,    // "changes", "requests", "problems", "solutions", etc. — selects which role JSON file to read
    String roleConfigKey, // key in resources/entity/roles/<module>.json or general.json
    User userObject       // from scenarioDetails.getUser(ScenarioUsers.TEST_USER_N)
)
```

> **CRITICAL**: Always call `deleteScenarioUser(ScenarioUsers.TEST_USER_N)` BEFORE
> `createUserByRole()` to avoid stale user state from prior test runs.

**Role JSON files per module** (in `resources/entity/roles/`):

| Module | File | Example keys |
|--------|------|-------------|
| Changes | `changes.json` | `SDChangeManager`, `Change_FullControl_With_CMDB` |
| Requests | `requests.json` | `Requester`, `Full_Control`, `View_Only` |
| System | `general.json` | `sdadmin`, `sdsite_admin`, `sdguest`, `helpdeskconfig` |
| Other modules | `<module>.json` | Module-specific custom roles |

**Decision flow for RBAC scenarios (all modules):**
```
CSV description says "verify user with/without X permission can/cannot Y"?
  → 1. Identify role → check <module>.json / general.json for matching key
  → 2. If no match → add new role entry to the correct module's JSON file
  → 3. Add preProcess group: deleteScenarioUser() + createUserByRole() + create test data
  → 4. In test method: switchUser(user) → test under role → switchToAdminSession()
```

> **FORBIDDEN**: Testing role restrictions as admin with placeholder comments like
> "admin baseline — role restriction test requires non-edit user". The test MUST
> actually switch to the restricted user and validate the behavior.

### Change Stage Transitions — Close Change Pattern

> SDP changes have 8 lifecycle stages. Closing a change requires SDChangeManager privilege
> and advancing through all stages via API. See `framework_rules.md` § "SECTION 34" and
> `framework_knowledge.md` § "Close Change via Stage Transitions" for complete patterns.
>
> **Key rules:**
> - NEVER send `closure_code` field (returns `EXTRA_KEY_FOUND_IN_JSON`)
> - SDChangeManager role required — admin without this role CANNOT close changes
> - Stage order: Submission → Planning → CAB Evaluation → Implementation → UAT → Release → Review → Close
> - preProcess pattern: create tech with role → create change with tech as change_manager → switchUser(tech) → advance all stages → switchToAdminSession()

### Owner Constants — auto-detected from hg username

The `owner` field in `@AutomaterScenario` is automatically resolved from the user's hg
username via `config/project_config.py → OWNER_CONSTANT`. The setup-project agent sets
`HG_USERNAME` and `OWNER_CONSTANT` in `.env` at clone time.

**To get the current owner at generation time:**
```bash
.venv/bin/python -c "from config.project_config import OWNER_CONSTANT; print(OWNER_CONSTANT)"
```

**Full constant list** (all defined in `OwnerConstants.java`):
```
OwnerConstants.ABHISHEK_RAV    OwnerConstants.ABINAYA_AK       OwnerConstants.AISHWARYA_JAYASANKAR
OwnerConstants.ANITHA_A        OwnerConstants.ANTONYRAJAN_D    OwnerConstants.BALAJI_M
OwnerConstants.BALAJI_MR       OwnerConstants.BINESH_N         OwnerConstants.DEVIRANI_R
OwnerConstants.ELANGO_S        OwnerConstants.GOWTHAM_A        OwnerConstants.GURDEEP_SINGH
OwnerConstants.HEMAPRIYA_S     OwnerConstants.JANAKI_R         OwnerConstants.JAYA_KUMAR
OwnerConstants.KARTHIKA_R      OwnerConstants.KARUPPASAMY      OwnerConstants.KASIM
OwnerConstants.KAVIN_KUMAR_R   OwnerConstants.MUTHUSIVABALAN_S OwnerConstants.NANTHAKUMAR_G
OwnerConstants.NITHIN_K        OwnerConstants.OMPIRAKASH       OwnerConstants.PAVITHRA_R
OwnerConstants.PURVA_RAJESH    OwnerConstants.RAJESHWARAN_A    OwnerConstants.RANJITH_N
OwnerConstants.RUJENDRAN       OwnerConstants.SANTHIYA_PR      OwnerConstants.SANTHOSH_BD
OwnerConstants.SIVANESH_MUTHUKUMAR OwnerConstants.SUBHA        OwnerConstants.SURENDHAR_GS
OwnerConstants.SURYA           OwnerConstants.TEJASWINI_G      OwnerConstants.THILAK_RAJ
OwnerConstants.UGESH           OwnerConstants.UMESH_SUDAN      OwnerConstants.VEERAVEL
OwnerConstants.VIGNESH_E       OwnerConstants.VIGNESHRAJ       OwnerConstants.VINUTHNA_K
OwnerConstants.YUVAN_R
```

> **No silent fallback**: If `HG_USERNAME` is not set or not found in the mapping, the user
> is asked for their name. `fuzzy_match_owner(name)` then finds the closest constant.
> If no match, the user is registered as a new owner via `register_new_owner(hg_username, name, email)`,
> which appends the constant to `OwnerConstants.java`, adds the mapping to `_OWNER_MAP`,
> and updates `.env`.

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

### ⚠️ Test Data Loading Methods — Correct Context (REQUIRED)

Three methods exist for loading test data. **Each has a specific context where it MUST be used — mixing them is FORBIDDEN.**

| Method | Where to use | Parameter | Auto-path? |
|--------|-------------|-----------|------------|
| `getTestCaseData(TestCaseData)` | **Test method body** | `DataConstants` constant | ✅ from TestCaseData object |
| `getTestCaseDataUsingCaseId(dataIds[N])` | **preProcess() only** | Raw string from `dataIds` array | ✅ `data/<module>/<entity>/<entity>_data.json` |
| `DataUtil.getTestCaseDataUsingFilePath(path, caseId)` | **APIUtil files** (static methods) | Explicit file path + case ID string | ❌ manual path |

#### Rules

1. **`getTestCaseDataUsingCaseId(String)`** — Instance method on Entity. Uses `getModuleName()` + `getName()` to build the path automatically. **ONLY use inside `preProcess()` where `dataIds` array is available as a parameter.** The `dataIds` come from `@AutomaterScenario(dataIds = {...})`.

2. **`DataUtil.getTestCaseDataUsingFilePath(path, caseId)`** — Static method on DataUtil. Takes an explicit file path. **Use in `*APIUtil.java` files** where there is no Entity instance context. Define a `PATH` constant in the APIUtil class.

3. **`getTestCaseData(TestCaseData)`** — Instance method on Entity. Takes a `TestCaseData` constant from `*DataConstants.java`. **Use in test method bodies** for loading UI form data.

```java
// ✅ CORRECT — preProcess uses getTestCaseDataUsingCaseId with dataIds
protected boolean preProcess(String group, String[] dataIds) {
    if ("create".equalsIgnoreCase(group)) {
        JSONObject inputData = getTestCaseDataUsingCaseId(dataIds[0]);
        // ...
    }
}

// ✅ CORRECT — APIUtil uses DataUtil.getTestCaseDataUsingFilePath with explicit path
public final class SolutionAPIUtil extends Utilities {
    private static final String PATH = "data" + File.separator + "solutions"
        + File.separator + "solution" + File.separator + "solution_data.json";

    public static String createTopic(String caseId) throws Exception {
        JSONObject data = DataUtil.getTestCaseDataUsingFilePath(
            AutomaterUtil.getResourceFolderPath() + PATH, caseId);
        // ...
    }
}

// ✅ CORRECT — test method uses getTestCaseData with DataConstants
public void myTestMethod() throws Exception {
    JSONObject inputData = getTestCaseData(SolutionDataConstants.SolutionData.MY_KEY);
    // ...
}

// ❌ FORBIDDEN — getTestCaseDataUsingCaseId inside APIUtil (no Entity context)
public static void createEntity(String caseId) {
    JSONObject data = getTestCaseDataUsingCaseId(caseId);  // WRONG — static context, no dataIds
}

// ❌ FORBIDDEN — getTestCaseDataUsingFilePath inside preProcess (use getTestCaseDataUsingCaseId)
protected boolean preProcess(String group, String[] dataIds) {
    JSONObject data = DataUtil.getTestCaseDataUsingFilePath(PATH, dataIds[0]);  // WRONG
}
```

### DataConstants inner class naming (REQUIRED — read before writing any constant reference)

The inner class name inside `*DataConstants.java` is derived from the **data filename** via `LOWER_UNDERSCORE → UPPER_CAMEL`:
```
change_workflow_data.json  →  inner class  ChangeWorkflowData  (NOT ChangeData)
solution_data.json         →  inner class  SolutionData
request_data.json          →  inner class  RequestData
```
Always check the actual inner class name in the file before referencing it. Never guess `EntityData` — it may be `EntityWorkflowData`, `EntityChecklistData`, etc.

### `AnnotationConstants` vs `DataConstants` — NOT interchangeable (REQUIRED)

| Class | Purpose | Used by |
|-------|---------|--------|
| `<Entity>DataConstants.<InnerClass>.KEY` | Test-method UI input data | `getTestCaseData(DataConstants.Data.KEY)` |
| `<Entity>AnnotationConstants.Data.KEY` | preProcess data IDs only | `@AutomaterScenario(dataIds = {...})` |

These are **separate files**. `DataConstants` is auto-generated from `*_data.json`. `AnnotationConstants` is hand-written and holds only the subset needed by `preProcess()`.

### Auto-Generating Constants (DataConstants, Fields, Roles)

In Eclipse, the Ant builder runs `AutoGenerateConstantFiles.main()` on save of any `*_data.json`, conf, or role JSON file. In VS Code / CLI, three equivalent mechanisms exist:

**Option A — VS Code task** (manual trigger):
Run the task **"Auto-Generate Constants"** from the Command Palette (`Tasks: Run Task`). Or run the script directly:
```bash
./generate_constants.sh                          # regenerate from most recently modified JSON
./generate_constants.sh path/to/entity_data.json # touch + regenerate a specific file
```

**Option B — Automatic via runner_agent** (before every test execution):
`runner_agent.py` calls `AutoGenerateConstantFiles.main()` automatically before compilation, so any new `*_data.json` entries are reflected in `*DataConstants.java` before the test runs.

**Option C — Automatic via test-generator agent** (generate-only mode):
The `@test-generator` agent runs `./generate_constants.sh` in **Step P0** after writing any `*_data.json` entry and before compiling (Step P1). This works because `AutoGenerateConstantFiles.class` is always pre-compiled in `$PROJECT_NAME/bin/` after cloning — no compilation required to invoke it. This ensures DataConstants are up-to-date even when tests are NOT executed (generate-only mode).

> `AnnotationConstants.java` is NOT auto-generated — it must still be edited by hand.

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
4. **FORBIDDEN: Inline JSONObject construction for data creation** — NEVER build test data from scratch with `new JSONObject().put(...)` chains in Java code. ALL entity data (UI inputs AND API payloads) MUST originate from `*_data.json` and be loaded via `getTestCaseData()` / `getTestCaseDataUsingCaseId()` / `DataUtil.getTestCaseDataUsingFilePath()`. This applies to **test methods, preProcess, AND APIUtil files**. For dynamic values, use `$(custom_KEY)` placeholders + `LocalStorage.store("KEY", value)` before loading. See the "APIUtil Data Flow" section for the required pattern.
5. **Post-load modification IS allowed** — After loading data from `*_data.json`, you MAY use JSONObject methods (`.put()`, `.remove()`, `.getJSONObject()`) to modify or augment the loaded data before passing it to the API. The rule is: **core data creation must always be in `*_data.json`**; post-load transformation in Java is fine when the modification is dynamic and cannot be expressed via `$(custom_KEY)` placeholders.

### Data Reuse (CRITICAL — prevents duplicate data entries)

Before creating any new `*_data.json` entry or `DataConstants` constant:
1. Read the existing `*_data.json` — list all top-level keys
2. Read `*AnnotationConstants.java → Data` interface for all preProcess data IDs
3. Read `*DataConstants.java` for all declared `TestCaseData` constants

**Reuse** an existing entry if it covers the same entity creation payload. Only create new entries when the field combination is genuinely different.

> **⚠️ `$(unique_string)` makes each load unique — NEVER create N near-identical entries for N entities.**
> When preProcess needs to create multiple entities of the same type (e.g. 3 changes for linking),
> call `getTestCaseDataUsingCaseId(dataIds[0])` or the APIUtil method N times with different
> LocalStorage key names — NOT N separate data entries with trivially different titles.
> `$(unique_string)` resolves to a new millisecond timestamp on every load call, guaranteeing
> unique titles automatically. Only the storage keys need to differ between calls.
> Similarly, `dataIds = {...}` in `@AutomaterScenario` only needs ONE entry — not N copies of the same key.

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

> **Caching warning**: `DataUtil` caches loaded JSON entries by `filePath_id` key. If you call
> `LocalStorage.store(key, newValue)` AFTER the first `getTestCaseData()` with the same `TestCaseData`
> key, the second call returns the CACHED result with the OLD placeholder value. Always pre-seed
> LocalStorage BEFORE the first load.

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
$(mspcustomer_email)         → MSP customer email (MSP tests only)
$(rest_api, method, apiPath, inputDataKey, storageKey[, iterate]) → calls REST API, stores result value in LocalStorage under storageKey
$(local_storage, store, key, value) → stores value in LocalStorage at runtime
$(local_storage, get, key)          → reads value from LocalStorage at runtime
$(common_string)             → timestamp + partName (unique per run, includes build info)
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
    }
}

// ❌ WRONG — do NOT instantiate, do NOT make non-static
public class ChangeActionsUtil {
    public void openAssociationTab() { ... }  // non-static fails — no access to actions
}
```

#### ⚠️ APIUtil Data Flow (MANDATORY — NEVER construct JSON inline)

> **Root cause of past violations**: APIUtil methods used `new JSONObject().put(...)` chains to build
> API payloads instead of loading from `*_data.json`. This is **FORBIDDEN** for ALL entity data —
> including API payloads for create, update, link, and association calls.

**The correct flow for EVERY new APIUtil method that sends data to an API:**

```
Step 1: Create a data entry in *_data.json (e.g. change_data.json)
        ↓
Step 2: Define PATH constant in the APIUtil class
        ↓
Step 3: APIUtil method loads data via DataUtil.getTestCaseDataUsingFilePath(PATH, caseId)
        ↓
Step 4: DataConstants are auto-generated on compile — reference them from callers
```

**Example — CORRECT pattern (link parent change via API):**

```json
// ===== In change_data.json =====
"link_parent_change_api": {
  "data": {
    "parent_change": [
      { "parent_change": { "id": "$(custom_target_change_id)" } }
    ]
  }
}
```

```java
// ===== In ChangeAPIUtil.java =====
public final class ChangeAPIUtil extends Utilities {
    private static final String PATH = "data" + File.separator + "changes"
        + File.separator + "change" + File.separator + "change_data.json";

    public static void linkParentChange(String changeId, String targetChangeId) throws Exception {
        LocalStorage.store("target_change_id", targetChangeId);
        JSONObject inputData = DataUtil.getTestCaseDataUsingFilePath(
            AutomaterUtil.getResourceFolderPath() + PATH, "link_parent_change_api");
        restAPI.update("changes/" + changeId + "/link_parent_change", inputData);
    }
}
```

```java
// ❌ FORBIDDEN — inline JSON construction in APIUtil
public static void linkParentChange(String changeId, String targetChangeId) throws Exception {
    JSONObject parentChangeObj = new JSONObject().put("id", targetChangeId);
    JSONObject wrapper = new JSONObject().put("parent_change", parentChangeObj);
    // ... more inline construction — NEVER do this
}
```

**Decision flow for EVERY APIUtil method:**
```
Does the method send data to an API (POST/PUT/PATCH)?
  → YES: Data MUST be in *_data.json, loaded via DataUtil.getTestCaseDataUsingFilePath()
         Use $(custom_KEY) placeholders for dynamic values (IDs, names)
         Store dynamic values via LocalStorage.store("KEY", value) before loading
  → NO (e.g., DELETE with only a path, or GET): No data entry needed, direct API call is fine
```

> **Existing codebase note**: Many pre-existing APIUtil files use inline JSON construction.
> This is legacy code — do NOT follow that pattern. All **newly generated** APIUtil methods
> MUST use `*_data.json` entries. When modifying existing methods, refactor to use data.json
> if the scope of change allows.

> **Post-load modification is OK**: After loading from `*_data.json`, you MAY use `.put()` / `.remove()` to tweak the loaded JSONObject (e.g., conditionally adding a field based on runtime state). The rule is: core data **creation** lives in JSON; post-load **transformation** in Java is acceptable.

#### Existing Method Protection (REQUIRED — shared across projects)

> **ActionsUtil and APIUtil methods are shared across multiple projects.** Modifying an existing
> method's signature, behaviour, or return type can break callers in other projects that were
> not compiled in this workspace.

**Default rule: Do NOT modify existing `public static` methods in `*ActionsUtil.java` or `*APIUtil.java`.**

**Exception — minimal usage**: If a method is used in **only 1–2 callers within the current project**
and **zero other projects**, it MAY be modified. In that case:
1. Search all callers first: `grep -rn "methodName" $PROJECT_NAME/src/`
2. Update ALL callers to match the new signature/behaviour
3. Compile ALL affected files (callers + utility) — zero errors required
4. If compilation fails, revert the change and create a new method instead

**Preferred alternative**: When the existing method doesn't quite fit, **create a new method**
with a different name (e.g., `linkParentChangeWithValidation(...)` alongside existing
`linkParentChange(...)`) rather than altering the original.

```bash
# Before modifying ANY existing util method — verify caller count:
grep -rn "methodName" $PROJECT_NAME/src/ | grep -v "utils/.*ActionsUtil\|utils/.*APIUtil" | wc -l
# If count > 2 → FORBIDDEN to modify. Create a new method instead.
```

#### Method granularity rules

| Bad — too granular | Bad — near-duplicate | Good — focused + parameterized |
|---|---|---|
| `clickAttachDropdown()` | `openAttachParentChangePopup()` + `openAttachChildChangesPopup()` | `openAttachPopup(String associationType)` (click dropdown + click option) |
| `clickYesOnConfirm()` | `detachParentChange()` + `detachChildChange()` doing same steps | `detachChange(String detachButtonLocator)` or parameterize the variant |
| Single-click wrappers | Two methods differing only by one string literal | One parameterized method covering all variants |

> **ANTI-PATTERN**: Creating multiple methods that share the same action sequence but differ
> only by a string value (entity name, tab name, dropdown option, button label). This inflates
> the util file and creates maintenance burden. Always parameterize.

Each method should represent **one complete, named UI operation** that a person doing manual testing would describe as a single step.

#### Generic Method Design Rules (MANDATORY for all new ActionsUtil methods)

**Rule 1 — Parameterize, don’t duplicate**

Before creating any new method, search the existing util for methods with the same click/type/navigate sequence. If one exists with a hardcoded string where yours would use a different string → **merge into one parameterized method**.

```java
// ❌ FORBIDDEN — two methods that differ only by one argument
public static void openAttachParentChangePopup() throws Exception {
    actions.click(ChangeLocators.LinkingChange.ATTACH_BUTTON_DROPDOWN);
    actions.click(ChangeLocators.LinkingChange.ATTACH_DROPDOWN_OPTION.apply("Parent Change"));
    actions.waitForAjaxComplete(); // Also redundant — see Rule 2
}
public static void openAttachChildChangesPopup() throws Exception {
    actions.click(ChangeLocators.LinkingChange.ATTACH_BUTTON_DROPDOWN);
    actions.click(ChangeLocators.LinkingChange.ATTACH_DROPDOWN_OPTION.apply("Child Changes"));
    actions.waitForAjaxComplete(); // Also redundant
}

// ✅ CORRECT — single parameterized method
public static void openAttachPopup(String associationType) throws Exception {
    actions.click(ChangeLocators.LinkingChange.ATTACH_BUTTON_DROPDOWN);
    actions.click(ChangeLocators.LinkingChange.ATTACH_DROPDOWN_OPTION.apply(associationType));
}
```

**Rule 2 — No redundant `waitForAjaxComplete()`**

`actions.click()` already calls `waitForAjaxComplete()` before clicking. NEVER add it:
- Between consecutive `click()` calls
- After the last `click()` in a method (the next framework call at the caller will wait internally)
- After `type()`, `sendKeys()`, `getText()`, `navigate.*()`, or `submit()` — all wait internally

The **only** valid uses: after `executeScript()` that triggers AJAX, or after `Thread.sleep()` where the next read depends on AJAX.

**Rule 3 — No thin wrappers around single framework calls**

Do NOT create a util method that just wraps a single `actions.*` call with no additional logic:
```java
// ❌ FORBIDDEN — just call actions.navigate.toModule() directly
public static void navigateToChanges() { actions.navigate.toModule("Changes"); }

// ❌ FORBIDDEN — single click, no encapsulated flow
public static void clickSaveButton() { actions.click(SAVE_BUTTON); }
```

**Rule 4 — Prefer explicit parameters over LocalStorage for method-local values**

Use explicit parameters when the caller has the value. Use `LocalStorage.getAsString()` inside the method only when the value was set by a different lifecycle phase (e.g., preProcess sets it, test method’s util reads it).

```java
// ✅ Explicit param — caller knows the value
ChangeActionsUtil.openAttachPopup("Parent Change");

// ✅ LocalStorage — value set by preProcess, read across methods
String changeName = LocalStorage.getAsString("changeName");
actions.listView.columnSearch("Title", changeName);
```

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
void   actions.windowManager.switchToTabByTitle(String title)     // exact case-insensitive match
void   actions.windowManager.switchToTabByUrl(String url)         // exact case-insensitive match
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


## AI Orchestrator Pipeline

LangGraph pipeline: `Ingestion → Planner → Coverage → Coder → Reviewer → Output → Runner → (fail) → HealerAgent`  
Entry points: `main.py` (full pipeline), `run_test.py` (quick CLI runner)  
HealerAgent uses Playwright + `SDPAPIHelper` (`agents/sdp_api_helper.py`) to replay preprocess API calls, inspect UI state, and generate locator/API fixes automatically.

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

