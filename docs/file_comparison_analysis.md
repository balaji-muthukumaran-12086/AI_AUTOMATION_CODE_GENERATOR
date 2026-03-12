# Comprehensive Comparison Analysis: Three Framework Documentation Files

**Files analyzed:**
- **File A**: `.github/copilot-instructions.md` (1323 lines) — Copilot system prompt
- **File B**: `config/framework_rules.md` (2613 lines) — AI code-generation rules
- **File C**: `config/framework_knowledge.md` (2165 lines) — Complete knowledge base

Also cross-referenced:
- `.github/instructions/java-test-conventions.instructions.md` (100 lines) — subset of A
- `.github/instructions/test-data-format.instructions.md` (71 lines) — subset of A

---

## 1. TOPIC MATRIX

Legend: ✅ = covered in depth | 🔸 = mentioned briefly | ❌ = absent

| # | Topic | File A | File B | File C | Agreement? |
|---|-------|--------|--------|--------|------------|
| 1 | Project structure / folder layout | ✅ | ❌ | ❌ | n/a — only in A |
| 2 | Module placement (derive from use-case noun) | ✅ | ✅ §0 | ❌ | ✅ Agree |
| 3 | Two-layer class architecture (Entity + Base) | 🔸 | ✅ §1 | ✅ §2–4 | ✅ Agree |
| 4 | Multi-level inheritance (3+ deep) | ❌ | ❌ | ✅ | n/a — only in C |
| 5 | @AutomaterScenario (all 9 fields) | ✅ | ✅ §2 | ✅ §4 | ✅ Agree |
| 6 | runType trap (default PORTAL_BASED) | ✅ | ✅ §2.1 | 🔸 | ✅ Agree |
| 7 | @AutomaterSuite | ❌ | ✅ §3 | 🔸 | n/a |
| 8 | @AutomaterCase (parameterized helpers) | ❌ | ✅ §29 | ✅ | ✅ Agree |
| 9 | Test lifecycle (preProcess → process → postProcess) | ✅ | ✅ §5,28 | ✅ §1,6 | ✅ Agree |
| 10 | preProcess groups — Requests (hardcoded list) | ✅ | ✅ §5 | ❌ | ✅ Agree (same list) |
| 11 | preProcess groups — Solutions (hardcoded list) | ✅ | ✅ §5 | ✅ §6 | ✅ Agree (same list) |
| 12 | preProcess — NoPreprocess pattern | ✅ | ✅ §5.3 | ✅ §6 | ✅ Agree |
| 13 | preProcess — Minimal group selection | ✅ | ✅ §5.4 | ✅ §6 | ✅ Agree |
| 14 | preProcess — Reuse existing groups | ✅ | ✅ §5.5 | ✅ §6 | ✅ Agree |
| 15 | preProcess — Where it lives (subclass first check) | ✅ | 🔸 | ✅ | ✅ Agree |
| 16 | preProcess — switch vs if/else-if style | ❌ | ✅ §28.1 | ❌ | n/a — only in B |
| 17 | preProcess — Silent catch pitfall | ✅ | ✅ §28.2 | ❌ | ✅ Agree |
| 18 | preProcess — addFailureReport in catch | ❌ | ✅ §28.2 | ❌ | n/a — only in B |
| 19 | postProcess conditional cleanup | ❌ | ✅ §28.3 | ✅ | ✅ Agree |
| 20 | **Test ID rules** | ✅ ⚠️ | ✅ §7 ⚠️ | ✅ §9 ⚠️ | **⚠️ CONTRADICTION — see §2** |
| 21 | Multi-ID grouping (comma-separated) | ✅ | ✅ §7.3 | ❌ | ✅ Agree |
| 22 | Data JSON format (wrapper, types, lookup fields) | ✅ | ✅ §8 | 🔸 §7 | ✅ Agree |
| 23 | Data reuse (check existing before creating new) | ✅ | ✅ §8b | 🔸 | ✅ Agree |
| 24 | LocalStorage pre-seed pattern | ✅ | ✅ §8b | ❌ | ✅ Agree |
| 25 | DataConstants pattern (TestCaseData declaration) | ✅ | ✅ §9 | ✅ §7 | ✅ Agree |
| 26 | DataConstants inner class naming | ✅ | ✅ §32.2 | ✅ | ✅ Agree |
| 27 | AnnotationConstants vs DataConstants (not interchangeable) | ✅ | ✅ §9 | ✅ §7 | ✅ Agree |
| 28 | Data loading methods (3-method table) | ✅ | ✅ §9.5 | ❌ explicit | ✅ Agree (A & B identical) |
| 29 | Forbidden inline JSONObject construction | ✅ | ✅ §9,§13.2 | ❌ | ✅ Agree |
| 30 | Placeholder reference (complete list) | ✅ | 🔸 §8 | ✅ | ✅ Agree — see §2 for gaps |
| 31 | `$(rest_api, ...)` sub-methods | 🔸 | ❌ | ✅ (detailed) | n/a |
| 32 | `$[custom_KEY]` (square bracket URL embed) | ❌ | ❌ | ✅ | n/a — only in C |
| 33 | DataUtil caching behaviour warning | ❌ | ❌ | ✅ | n/a — only in C |
| 34 | Field config (entity conf JSON) | ✅ | 🔸 | ✅ §3 | ✅ Agree |
| 35 | FieldType complete list + skipped types | ✅ | ✅ §32.7 | ✅ §8 | ✅ Agree |
| 36 | FieldDetails constructor (6 params) | ✅ | ✅ §32.5 | ✅ §13 | ✅ Agree |
| 37 | FormBuilder complete API | ✅ | ✅ §19 | ✅ §8 | ✅ Agree |
| 38 | fillInputForAnEntity internals / isClientFramework trap | 🔸 | ✅ §20.1,§20.2 | ✅ §8 | ✅ Agree |
| 39 | Checkbox/boolean trap | ✅ | ✅ §20.2 | ✅ §8 | ✅ Agree |
| 40 | **waitForAjaxComplete rules** | ✅ (table) | ✅ §20.4 | ✅ (table) | ✅ Agree (all consistent) |
| 41 | actions.navigate complete API | ✅ | 🔸 | ✅ §14 | ✅ Agree |
| 42 | actions.listView complete API | ✅ | 🔸 §15 | ✅ §15 | ✅ Agree |
| 43 | actions.detailsView complete API | ✅ | ❌ | ✅ §16 | ✅ Agree |
| 44 | actions.validate complete API | ✅ | ✅ §16 | ❌ explicit | ✅ Agree |
| 45 | actions.windowManager API | ✅ | ✅ §17 | ❌ | ✅ Agree |
| 46 | actions.popUp.listView (use inside popups) | ✅ | ✅ §22 | ✅ §25 | ✅ Agree |
| 47 | Select2 dropdown handling | 🔸 | ✅ §22 | ✅ §26 | ✅ Agree |
| 48 | REST API architecture (browser JS execution) | ✅ | ✅ §21 | ✅ §23 | ✅ Agree |
| 49 | Core RestAPI methods table | ✅ | 🔸 | ✅ §10 | ✅ Agree |
| 50 | getInputData wrapping | 🔸 | 🔸 | ✅ §27 | ✅ Agree |
| 51 | Auto-cleanup (DataUtil.cleanUpIds) | ✅ | ❌ | 🔸 | ✅ Agree |
| 52 | Session context (admin→preProcess, user→test) | ✅ | ✅ §20.5 | ✅ | ✅ Agree |
| 53 | Role system (createUserByRole flow) | ✅ | ✅ §33 | ✅ | ✅ Agree |
| 54 | Role JSON structure | ✅ | ✅ §33.3 | ✅ | ✅ Agree |
| 55 | SDADMIN = no session split | ✅ | ✅ §33.4 | ✅ | ✅ Agree |
| 56 | Owner constants (auto-detected from hg username) | ✅ | ✅ §6 | ❌ | ✅ Agree |
| 57 | ActionsUtil/APIUtil pattern | ✅ | ✅ §23 | ✅ §19 | ✅ Agree |
| 58 | APIUtil data flow (MUST use *_data.json) | ✅ | ✅ §23 | ✅ §19 | ✅ Agree |
| 59 | Existing method protection (shared util files) | ✅ | ✅ §23 | ❌ | ✅ Agree |
| 60 | 4-step pre-generation workflow (mandatory) | ✅ | ✅ §23 | ✅ §19 | ✅ Agree |
| 61 | Method granularity rules | ✅ | ✅ §23 | ❌ | ✅ Agree |
| 62 | Known entity utility files table | ✅ | 🔸 | ✅ §19 | ✅ Agree |
| 63 | Two-Piece Output Format (markers) | ✅ | ✅ §12 | ❌ | ✅ Agree |
| 64 | LLM implementation skeleton template | ❌ | ✅ §10 | ✅ §5 | ✅ Agree |
| 65 | Forbidden patterns list (13 items) | ❌ | ✅ §13 | ❌ | n/a — only in B |
| 66 | Quick checklists | ❌ | ✅ §15 | ❌ | n/a — only in B |
| 67 | RandomUtil API | ❌ | ✅ §18 | ❌ | n/a — only in B |
| 68 | Compilation (full broken, targeted only) | ✅ | ❌ | ❌ | n/a — only in A |
| 69 | Running a test (run_test.py / RUN_CONFIG) | ✅ | ❌ | ❌ | n/a — only in A |
| 70 | Runner agent `_parse_success()` logic | ✅ | ❌ | ❌ | n/a — only in A |
| 71 | Report generation (ScenarioReport.html) | 🔸 | ✅ §27,§30 | ❌ | n/a |
| 72 | EntityCase lifecycle & reporting | ❌ | ✅ §27 | ❌ | n/a — only in B |
| 73 | addReport smart variant + clearFailureMessage | ❌ | ✅ §27.1–2 | ❌ | n/a — only in B |
| 74 | cleanUp() singletons destroyed | ❌ | ✅ §27.3 | ✅ | ✅ Agree |
| 75 | Report wrapping pattern (start/endMethodFlow) | ❌ | ✅ §30 | ❌ | n/a — only in B |
| 76 | getMethodName() stack frame rule | ❌ | ✅ §30.2 | ❌ | n/a — only in B |
| 77 | Skeleton scaffolding (GenerateSkeletonForAnEntity) | 🔸 | ✅ §31 | ✅ | ✅ Agree |
| 78 | AutoGenerateConstantFiles (dispatch map) | 🔸 | ✅ §32 | ✅ | ✅ Agree |
| 79 | Linking Changes CH-286 | ❌ | ✅ §24 | ✅ | ✅ Agree |
| 80 | Workflow boundary tests (stage vs flat) | ❌ | ✅ §24.7 | ✅ | ✅ Agree |
| 81 | Asset workflow sub_module special case | ❌ | 🔸 | ✅ | ✅ Agree |
| 82 | Task node connector ports | ❌ | ✅ §26 | ❌ | n/a — only in B |
| 83 | Checkstyle NeedBraces | ✅ | ✅ §25 | ❌ | ✅ Agree |
| 84 | Non-existent methods (never use these) | ✅ | ✅ §13.11–12 | ❌ | ✅ Agree |
| 85 | SDPCloudActions methods | ❌ | ❌ | ✅ §21e | n/a — only in C |
| 86 | SolutionConstants.java complete reference | ❌ | ❌ | ✅ §22 | n/a — only in C |
| 87 | ClientFrameworkActions hierarchy | ❌ | ❌ | ✅ §24 | n/a — only in C |
| 88 | Problem module Actions dropdown gotcha | ❌ | ✅ §20.8 | ❌ | n/a — only in B |
| 89 | Copy Problem flow trap | ❌ | ✅ §20.10 | ❌ | n/a — only in B |
| 90 | SOLUTION_ADD vs SOLUTION_ADD_APPROVE | ✅ | ✅ §20.9 | ❌ | ✅ Agree |
| 91 | AI Orchestrator Pipeline docs | ✅ | ❌ | ❌ | n/a — only in A |
| 92 | Playwright MCP Data Creation SOP | ✅ | ❌ | ❌ | n/a — only in A |
| 93 | sdpAPICall() JS reference | ✅ | ❌ | ❌ | n/a — only in A |
| 94 | LocalSetupManager internals | ❌ | ❌ | ✅ | n/a — only in C |
| 95 | BeforeAndAfterCaseActions lifecycle phases | ❌ | ❌ | ✅ | n/a — only in C |
| 96 | SolutionBase.createSolution() pattern | ❌ | ❌ | ✅ | n/a — only in C |
| 97 | Learned patterns (auto-generated: IR Workflow, AssetTrigger, etc.) | ❌ | 🔸 | ✅ | n/a |
| 98 | Git+Hg coexistence / GitHub push guide | ❌ | ❌ | ✅ | n/a — only in C |
| 99 | Entity creation patterns (DataUtil.getInputDataForRestAPI) | ❌ | ❌ | ✅ §27 | n/a — only in C |
| 100 | `$(rest_api)` method variants table | 🔸 | ❌ | ✅ | n/a — only in C |

---

## 2. CONTRADICTIONS

### CONTRADICTION 1 — Test ID Rules (CRITICAL)

**File A** (line ~337) and **File B** (§7):
> "When a Use-Case Document (CSV) Is Provided: **Use the use-case ID as-is** in `@AutomaterScenario(id = "...")`"  
> "When No Use-Case Document Is Provided: Fall back to the **auto-generated sequential ID pattern** per module"

CSV is PRIMARY. Sequential is FALLBACK only.

**File C** (§9, ~line 297):
> "Test IDs follow the pattern `SDPOD_AUTO_<MODULE>_<AREA>_NNN`"  
> "NEVER use `SDP_` prefix (triggers Aalam harness conflicts)"

File C presents the sequential `SDPOD_AUTO_` pattern as **the only rule**. It makes NO mention of CSV use-case IDs as a primary source. It also introduces an **additional prohibition** ("NEVER use `SDP_` prefix") that Files A and B do not mention.

**Impact**: An agent using only File C will always generate sequential IDs, even when a CSV file with manual test case IDs exists in `$PROJECT_NAME/Testcase/`.

**Recommendation**: File C must be updated to include the CSV-primary/sequential-fallback decision flow from Files A and B.

---

### CONTRADICTION 2 — Test ID Prefix Restriction

**File C** (§9):
> "NEVER use `SDP_` prefix"

**File A** (preProcess groups table):
> Shows `SDP_REQ_LS_AAA###` and `SDP_REQ_DV_AAA###` as valid Requests module sequential ID patterns.

**File B** (§7):
> Also shows `SDP_REQ_LS_AAA###` and `SDP_REQ_DV_AAA###` as valid patterns.

**Impact**: File C's blanket "NEVER use SDP_ prefix" directly contradicts the Requests module ID patterns documented in Files A and B.

**Recommendation**: File C should restrict the prohibition to `SDP_` only in specific contexts (e.g., "NEVER use bare `SDP_` without module suffix") or update the Requests patterns to use `SDPOD_` prefix.

---

### CONTRADICTION 3 — `addReport()` Smart Variant Coverage

**File A**: No mention of `addReport(String message)` at all. Only documents `addSuccessReport()` and `addFailureReport()`.

**File B** (§27.1): Documents a **three-method** reporting API:
> `addReport(message)` inspects `failureMessage.length()`: `== 0` → success; `> 0` → failure.

**File C**: No mention.

**Impact**: Minor — agents using only File A will never use the smart `addReport()` variant, always writing explicit `if/else` with `addSuccessReport`/`addFailureReport`. Not wrong, but less elegant.

---

### CONTRADICTION 4 — preProcess Silent Catch Recommendation

**File A** (Common Pitfalls):
> `Solution.java` has `catch(Exception) { return false; }` — listed as a **pitfall** to be aware of.

**File B** (§28.2):
> Explicitly says `return false` silently is **acceptable but** recommends `addFailureReport(...)` instead.

**File B** (§28.4):
> Shows `return true` unconditionally as valid for NoPreprocess.

These aren't contradictory per se, but File A implies silent catch is always bad, while File B provides nuance (acceptable for stubs, but prefer logging for real groups).

---

## 3. MODULE-SPECIFIC HARDCODED CONTENT

Every section below contains content tied to a specific SDP module (not generic framework rules).

### File A — Module-Specific Sections

| Section | Module(s) | Content |
|---------|-----------|---------|
| Module Placement table | Requests, Solutions, Problems, Changes, Tasks | Use-case noun → module path mapping |
| preProcess Groups — Requests | Requests | 20 hardcoded group strings |
| preProcess Groups — Solutions | Solutions | 6 hardcoded group strings |
| Common Pitfalls: `SOLUTION_ADD` | Solutions | XPath normalize-space bug |
| Common Pitfalls: Select2 | All modules | `select2-result-label` pattern |
| Common Pitfalls: SDP Associations tab | Changes | `change_associations_parent_change` ID |
| Playwright MCP sdpAPICall table | All 11 modules | Module → API path → wrapper key mapping |
| Known entity utility files table | 15+ modules | Module → ActionsUtil/APIUtil file paths |

### File B — Module-Specific Sections

| Section | Module(s) | Content |
|---------|-----------|---------|
| §0 Module Placement table | Requests, Solutions, Problems, Changes, Tasks | Same as File A |
| §5 preProcess Groups — Requests | Requests | Same 20 hardcoded group strings |
| §5 preProcess Groups — Solutions | Solutions | Same 6 hardcoded group strings |
| §20.8 Problem Actions dropdown | Problems | `toGlobalActionInDetailsPage` fails for Problems |
| §20.9 SOLUTION_ADD bug | Solutions | Same XPath issue as File A |
| §20.10 Copy Problem flow | Problems | waitForAjaxComplete timing for Problem copy |
| §20.11 SolutionAPIUtil vs ProblemAPIUtil | Solutions, Problems | Diff between createSolution/createProblem helpers |
| §24 Linking Changes CH-286 | Changes | Full CH-286 feature: locators, API, 19 scenarios |
| §24.7 Workflow boundary tests | Changes, Releases, Problems, Assets | Stage-based vs flat-status per module |
| §25 Checkstyle | All | Generic but showed module examples |
| §26 Task Node Connector Ports | Changes (Workflows) | Task node input/output `Completed`/`Overdue` ports |
| §28.1 switch pattern | Requests (Approvals) | RequestApprovalsBase example |
| §33 Role system examples | Solutions | Solution_FullControl, Solution_Requester examples |

### File C — Module-Specific Sections

| Section | Module(s) | Content |
|---------|-----------|---------|
| §5 Implementation Pattern | Solutions | Full SolutionBase.java example |
| §6 preProcess Solutions code | Solutions | Actual Solution.java preProcess code |
| §9 Test ID prefixes | Solutions, Changes, Problems | Module-specific ID pattern table |
| §20b ChangeActionsUtil reference | Changes | Complete method listing |
| §21e SDPCloudActions | All | Module-agnostic but SDP-specific |
| §22 SolutionConstants.java | Solutions | Complete constants reference |
| §27 Entity Creation Patterns | Changes | `Change.java createChangeGetResponse` deep dive |
| Linking Changes CH-286 | Changes | Full pattern with locator/API details |
| Asset Workflow | Assets | sub_module field, API patterns, test IDs |
| Learned patterns (auto-generated) | Requests (IR Workflow), Assets (Triggers), Projects (UDF) | IncidentRequestWorkflow, AssetTrigger, ProjectUDF |
| SolutionBase.createSolution() | Solutions | LocalStorage store pattern |
| Git/Hg push | — | Not module-specific (DevOps) |

---

## 4. UNIQUE LEARNINGS (Rules in Only One File)

### Only in File A

| Topic | Why It's Unique |
|-------|----------------|
| Project folder structure diagram | Physical layout of workspace folders |
| Compilation instructions (`setup_framework_bin.sh`, targeted compile) | Operational knowledge for running tests |
| `run_test.py` / `RUN_CONFIG` | How to execute tests from CLI |
| Runner agent `_parse_success()` logic | Python runner internals |
| AI Orchestrator Pipeline (LangGraph) | Pipeline architecture |
| Playwright MCP Data Creation SOP | Browser-based debugging workflow |
| `sdpAPICall()` JS quick reference | JavaScript API for browser debugging |
| Driver & environment paths table | Machine config (Firefox, geckodriver) |
| Report file locations | `reports/LOCAL_<method>_<ts>/ScenarioReport.html` |
| Entity class mapping (ENTITY_IMPORT_MAP) | Python runner entity resolution |

### Only in File B

| Topic | Why It's Unique |
|-------|----------------|
| §3 @AutomaterSuite full spec | Suite-level annotation with `role`, `owner`, `tags`, `description` |
| §4 @AutomaterCase forbidden for new tests | Deprecation rule |
| §10 Implementation method skeleton template | Full boilerplate with report wrapping |
| §11 postProcess full pattern | `try/catch` + suppressed cleanup |
| §13 Forbidden patterns (13 subsections) | Explicit anti-patterns list |
| §15 Quick checklists (6 items) | Pre-commit validation list |
| §18 RandomUtil API | `getAlphabets(n)`, `getNumbers(n)`, `getAlphaNumeric(n)`, `getAlphaNumericSpecialChar(n)` |
| §20.8 Problem Actions dropdown gotcha | `toGlobalActionInDetailsPage` tries 3 different paths |
| §20.10 Copy Problem flow timing | `waitForAjaxComplete()` between radio-click and copy-click |
| §26 Task Node Connector Ports | `input_Completed`/`output_Overdue` for Tasks |
| §27 EntityCase lifecycle & reporting | `addReport` smart variant, `clearFailureMessage`, screenshot internals |
| §28.1 switch vs if/else-if preference | 4+ groups → use switch |
| §28.2 addFailureReport in preProcess catch | Best practice vs silent return |
| §29 @AutomaterScenario vs @AutomaterCase full comparison | Side-by-side annotation comparison |
| §30 Report wrapping pattern | `startMethodFlowInStepsToReproduce` / `endMethodFlowInStepsToReproduce` |
| §30.2 getMethodName() stack frame rule | Must call at outermost frame |

### Only in File C

| Topic | Why It's Unique |
|-------|----------------|
| Multi-level inheritance >2 deep | TaskBase → ProjectMilestoneTaskBase → ProjectMilestoneTask |
| `$(rest_api, ...)` method variants table | `get`, `post`, `getResponse`, `search`, `getFieldValue` |
| `$[custom_KEY]` (square brackets in URL) | LocalStorage embed in API paths |
| DataUtil caching behaviour warning | Same TestCaseData key cached after first `getTestCaseData()` call |
| §24 ClientFrameworkActions hierarchy | Full inheritance: Actions → ClientActions → ClientFrameworkActions |
| §25 PopUp & ListViewForPopUp complete methods | `selectFilterUsingSearch`, `selectFilterWithoutSearch` internals |
| §26 Select2 dropdown internals | Option `<li>` rendered at `<body>` level, not inside parent |
| §27 DataUtil.getInputDataForRestAPI() | Fresh placeholder resolution per API call |
| Asset workflow sub_module pattern | `workflowPayload.put("sub_module", "Computers")` |
| LocalSetupManager internals | `System.getProperty("automation.local.setup")`, NO CommonVariables |
| BeforeAndAfterCaseActions lifecycle (9 phases) | Full pre-test lifecycle from framework |
| SolutionBase.createSolution() pattern | `restAPI.createAndGetResponse` + LocalStorage store |
| SDPCloudActions method reference | `isMSP()`, `getDisplayId()`, module utility methods |
| SolutionConstants.java complete reference | All inner-class constants |
| Git+Hg coexistence guide | `git init` inside hg repo, GitHub SSH/PAT push |
| Learned patterns (auto-generated by LearningAgent) | IncidentRequestWorkflow, AssetTrigger, ProjectUDF examples |

---

## 5. MISSING FROM EACH FILE

### File A Is Missing

1. **@AutomaterSuite annotation spec** (§3 in B) — no mention of suite-level annotation
2. **@AutomaterCase annotation** (§29 in B, also in C) — no mention of parameterized helpers
3. **Forbidden patterns list** (§13 in B) — no consolidated anti-patterns section
4. **Quick checklists** (§15 in B) — no pre-commit validation checklist
5. **RandomUtil API** (§18 in B) — random data generation methods
6. **EntityCase lifecycle/reporting internals** (§27 in B) — `addReport` smart variant, screenshot flow
7. **Report wrapping pattern** (§30 in B) — `startMethodFlowInStepsToReproduce`
8. **Implementation method skeleton** (§10 in B) — boilerplate template for new methods
9. **postProcess full pattern** (§11 in B) — cleanup pattern with method-name matching
10. **Multi-level inheritance** (C only) — 3+ deep hierarchy patterns
11. **DataUtil caching warning** (C only) — cached data won't pick up later LocalStorage changes
12. **`$(rest_api, ...)` method variants** (C only) — 5 sub-methods for REST placeholders
13. **`$[custom_KEY]` square bracket syntax** (C only) — URL embedding
14. **LocalSetupManager internals** (C only) — system property detection
15. **BeforeAndAfterCaseActions lifecycle** (C only) — 9-phase pre-test setup
16. **preProcess switch vs if/else style guide** (§28.1 in B)

### File B Is Missing

1. **Project structure / folder layout** (A only) — physical workspace layout
2. **Compilation instructions** (A only) — `setup_framework_bin.sh`, targeted compile commands
3. **Running a test / run_test.py** (A only) — how to execute from CLI
4. **Runner agent `_parse_success()` logic** (A only) — Python success detection
5. **AI Orchestrator Pipeline** (A only) — LangGraph pipeline architecture
6. **Playwright MCP SOP** (A only) — browser debugging workflow
7. **sdpAPICall() JS reference** (A only) — JavaScript API for debugging
8. **Driver/environment paths** (A only) — Firefox, geckodriver, `.env` config
9. **actions.detailsView complete API** (A and C, missing in B)
10. **Multi-level inheritance** (C only)
11. **DataUtil caching warning** (C only)
12. **`$(rest_api, ...)` detailed methods** (C only)
13. **`$[custom_KEY]` square bracket syntax** (C only)
14. **ClientFrameworkActions hierarchy** (C only)
15. **LocalSetupManager internals** (C only)
16. **BeforeAndAfterCaseActions lifecycle** (C only)
17. **Entity creation patterns (DataUtil.getInputDataForRestAPI)** (C only)
18. **SDPCloudActions method reference** (C only)

### File C Is Missing

1. **Module placement rule** (A and B) — derive from use-case noun, not open file
2. **CSV use-case ID as primary test ID source** (A and B) — CRITICAL gap (see Contradiction #1)
3. **Multi-ID grouping** (A and B) — comma-separated IDs in annotation
4. **preProcess groups for Requests module** (A and B) — 20 hardcoded group strings
5. **Data loading methods table** (A and B) — 3-method context table
6. **Forbidden inline JSONObject construction** (A and B) — explicit prohibition
7. **Data reuse decision flow** (A and B) — check existing before creating new
8. **LocalStorage pre-seed pattern** (A and B) — reuse JSON entries with dynamic values
9. **Existing method protection** (A and B) — shared util methods across projects
10. **Method granularity rules** (A and B) — one complete UI operation per method
11. **Non-existent methods list** (A and B) — methods that don't exist
12. **Two-Piece Output Format** (A and B) — LLM output markers
13. **Compilation instructions** (A only)
14. **Running a test** (A only)
15. **Runner agent parse logic** (A only)
16. **AI Orchestrator Pipeline** (A only)
17. **Playwright MCP SOP** (A only)
18. **@AutomaterSuite full spec** (B only)
19. **Forbidden patterns list** (B only)
20. **Quick checklists** (B only)
21. **RandomUtil API** (B only)
22. **EntityCase lifecycle** (B only)
23. **Report wrapping pattern** (B only)
24. **addReport smart variant** (B only)
25. **switch vs if/else-if** (B only)
26. **Task node connector ports** (B only)
27. **actions.validate API** (A and B) — complete validator methods
28. **actions.windowManager API** (A and B)

---

## 6. DEEP-DIVE: REQUESTED FOCUS AREAS

### 6.1 preProcess Group Lists

| File | Requests Groups | Solutions Groups | Other Modules |
|------|----------------|-----------------|---------------|
| A | ✅ 20 groups (hardcoded list) | ✅ 6 groups (hardcoded list) | ❌ None |
| B | ✅ 20 groups (identical to A) | ✅ 6 groups (identical to A) | RequestApprovals groups (§28.1 example) |
| C | ❌ Not listed | ✅ 6 groups (identical) via code example | ❌ None |

**Finding**: A and B are perfectly synchronized. C only has Solutions. No file documents groups for Changes, Problems, or other modules — those must be discovered from source code.

### 6.2 Test ID Rules

| Aspect | File A | File B | File C |
|--------|--------|--------|--------|
| CSV primary source | ✅ | ✅ | ❌ "NEVER" mentioned |
| Sequential fallback | ✅ | ✅ | ✅ (presented as ONLY option) |
| SDP_ prefix prohibition | ❌ | ❌ | ✅ "NEVER use SDP_ prefix" |
| SDP_REQ_ pattern valid | ✅ | ✅ | ❌ (contradicts SDP_ prohibition) |
| Multi-ID comma grouping | ✅ | ✅ | ❌ |
| Module prefix table | ✅ (7 modules) | ✅ (7 modules, identical) | 🔸 (3 modules) |

**Finding**: **CRITICAL CONTRADICTION.** File C is out of date and must be updated.

### 6.3 Placeholder Reference Completeness

| Placeholder | File A | File B | File C |
|-------------|--------|--------|--------|
| `$(unique_string)` | ✅ | ✅ | ✅ |
| `$(common_string)` | ✅ | ❌ | ✅ |
| `$(custom_KEY)` | ✅ | ✅ | ✅ |
| `$(user_name)` | ✅ | ✅ | ✅ |
| `$(user_email_id)` | ✅ | ✅ | ✅ |
| `$(user_id)` | ✅ | ✅ | ✅ |
| `$(admin_email_id)` | ✅ | ✅ | ✅ |
| `$(admin_name)` | ✅ | ✅ | ✅ |
| `$(mspcustomer_*)` (3) | ✅ | ❌ | ✅ |
| `$(date, N, ahead)` | ✅ | ✅ | ✅ |
| `$(datetime, N, ahead)` | ✅ | ✅ | ✅ |
| `$(rest_api, ...)` | 🔸 | ❌ | ✅ (5 sub-methods) |
| `$(local_storage, store, ...)` | ✅ | ❌ | ✅ |
| `$(local_storage, get, ...)` | ✅ | ❌ | ✅ |
| `$[custom_KEY]` (URL embed) | ❌ | ❌ | ✅ |

**Finding**: File C has the most complete placeholder reference. File B is missing `$(common_string)`, `$(mspcustomer_*)`, `$(rest_api,...)`, `$(local_storage,...)`, and `$[custom_KEY]`.

### 6.4 Data Loading Methods

| File | 3-Method Table | Context Rules | Forbidden Combos |
|------|---------------|---------------|------------------|
| A | ✅ (identical table) | ✅ | ✅ (explicit) |
| B | ✅ (identical table) | ✅ | ✅ (explicit) |
| C | ❌ (no explicit table) | 🔸 (implied) | ❌ |

**Finding**: A and B have identical 3-method tables with forbidden combinations. C documents the methods individually but does not present the unified table with context restrictions.

### 6.5 waitForAjaxComplete Rules

| File | Method-level table | When to add manually | Framework internals |
|------|-------------------|---------------------|---------------------|
| A | ✅ (11-row table) | ✅ | ❌ |
| B | ✅ (§20.4 rules) | ✅ (more detailed) | ❌ |
| C | ✅ (12-row table) | ✅ | ✅ (verified from source ZIP) |

**Finding**: All three agree on the core rule. File C adds `toGlobalActionInDetailsPage` and `toGlobalActionInListview` to the table. File B provides the most practical nuance (when to add Thread.sleep).

### 6.6 ActionsUtil/APIUtil Patterns

| Aspect | File A | File B | File C |
|--------|--------|--------|--------|
| Class declaration (`extends Utilities`) | ✅ | ✅ | ✅ |
| 4-step pre-generation workflow | ✅ | ✅ | ✅ |
| APIUtil data flow (MUST use *_data.json) | ✅ | ✅ | ✅ |
| Existing method protection | ✅ | ✅ | ❌ |
| Method granularity rules | ✅ | ✅ | ❌ |
| Known util files table | ✅ (15+ modules) | 🔸 | ✅ (15+ modules) |
| ChangeActionsUtil complete reference | ❌ | ❌ | ✅ §20b |
| Post-load JSON modification OK | ✅ | ✅ | ❌ explicit |

**Finding**: All three cover the core pattern identically. File A and B add protection and granularity rules. File C adds the only complete method-by-method reference for ChangeActionsUtil.

---

## 7. SUMMARY & RECOMMENDATIONS

### File Roles (intended purpose)

| File | Role | Audience |
|------|------|----------|
| **A** (copilot-instructions.md) | System prompt for Copilot | All Copilot interactions (highest authority) |
| **B** (framework_rules.md) | Comprehensive code-gen rules | Coder Agent (AI pipeline) |
| **C** (framework_knowledge.md) | Deep framework reference + learned patterns | All agents (RAG-indexed knowledge) |

### Key Findings

1. **Files A and B are highly synchronized** — nearly all shared topics agree. B is a superset of A for code-generation rules (adds forbidden patterns, skeletons, report wrapping, EntityCase lifecycle).

2. **File C has a critical Test ID contradiction** — must update §9 to include CSV-primary/sequential-fallback rule and remove the blanket "NEVER use SDP_ prefix" prohibition (or restrict it to non-Requests modules).

3. **File C is the deepest on framework internals** — ClientFrameworkActions hierarchy, DataUtil caching, LocalSetupManager, BeforeAndAfterCaseActions, Select2 internals, `$(rest_api)` sub-methods. These are nowhere else and valuable.

4. **File B is the only source for key operational rules** — EntityCase reporting lifecycle, report wrapping, forbidden patterns list, quick checklists, RandomUtil, @AutomaterCase deprecation, switch vs if/else-if preference.

5. **File A is the only source for execution/operational info** — compilation, running tests, runner agent logic, Playwright MCP, AI pipeline docs.

6. **No single file is sufficient alone.** Each has unique critical content the others lack.

### Recommended Actions

| Priority | Action |
|----------|--------|
| **P0** | Fix File C §9 Test ID rules — add CSV-primary/sequential-fallback, fix SDP_ prohibition |
| **P1** | Add `$(common_string)`, `$(mspcustomer_*)`, `$(rest_api,...)`, `$(local_storage,...)` to File B placeholder list |
| **P1** | Add `actions.detailsView` API to File B |
| **P2** | Add Data loading methods table to File C |
| **P2** | Add Module placement rule to File C |
| **P2** | Add Forbidden inline JSONObject rule to File C |
| **P3** | Add Multi-ID grouping to File C |
| **P3** | Backport addReport smart variant to File A |
| **P3** | Backport @AutomaterCase docs to File A |
