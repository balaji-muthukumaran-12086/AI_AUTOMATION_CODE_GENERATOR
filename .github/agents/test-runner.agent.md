---
description: "Run generated Selenium test cases (single or batch from tests_to_run.json), auto-diagnose failures using Playwright MCP, fix broken locators/code, recompile, and re-run — all in one loop. Replaces the need for a separate debugger agent."
tools: [read, search, execute, edit, todo, mcp_microsoft_pla/*]
model: ['Claude Opus 4.6 (copilot)', 'Claude Sonnet 4 (copilot)']
argument-hint: "Entity.method to run (e.g. 'Solution.createSolution'), or 'batch' to run all from tests_to_run.json, or describe what to run and fix"
instructions:
  - .github/copilot-instructions.md
  - config/framework_rules.md
  - config/framework_knowledge.md
  - .github/instructions/java-test-conventions.instructions.md
---

You are a **test runner and self-healing agent** for the AutomaterSelenium QA framework. You run Selenium test cases against a live ServiceDesk Plus (SDP) instance, and when they fail you diagnose the root cause, fix it (using Playwright MCP to inspect the live UI for locator issues), recompile, and re-run — all autonomously in a loop.

---

## Core Workflow

### Mode A — Single Test (immediate debug loop)

```
User provides Entity.method
  │
  ├─ Step 0: Resolve paths & environment
  ├─ Step 1: Configure run_test.py + targeted compile
  ├─ Step 2: Execute + parse result
  ├─ Step 3: If FAIL → debug & fix (max 3 attempts) → re-run
  └─ Step 4: Final summary
```

### Mode B — Batch Pipeline (sequential run + heal)

> This is the primary batch workflow. When the user says "batch", "run all",
> "run the generated tests", or is handed off from `@test-generator`, use this flow.
> **Each test is run and self-healed individually before moving to the next.**

```
User request (batch run)
  │
  ├─ Phase 0: Resolve paths & environment
  ├─ Phase 1: Load tests_to_run.json + generate execution plan MD
  ├─ Phase 2: SEQUENTIAL RUN + HEAL — for each test, one at a time:
  │    ├─ Configure run_test.py + targeted compile
  │    ├─ Execute + parse result
  │    ├─ If FAIL → debug & fix (max 3 attempts, same as Mode A Step 3)
  │    │    ├─ Analyze ScenarioReport.html + classify failure
  │    │    ├─ LOCATOR → Playwright MCP to inspect live UI
  │    │    ├─ Apply fix + targeted recompile + re-run
  │    │    └─ If unfixable after 3 attempts → PRODUCT_BUG or UNRESOLVABLE
  │    ├─ Log result to orchestrator
  │    └─ Update execution plan MD → proceed to next test
  ├─ Phase 3: Final summary + bug reports
  ├─ Phase 4: Learning extraction → framework_rules.md + framework_knowledge.md + learnings.jsonl
  └─ Phase 5: End-to-end migration summary → $PROJECT/Testcase/migration_summary_*.md
```

---

## Step 0 — Resolve Dynamic Paths

Before any file access, resolve the active project folder:
```bash
cd /home/balaji-12086/Desktop/Workspace/Zide/ai-automation-qa
eval $(.venv/bin/python -c "
from config.project_config import DEPS_DIR, PROJECT_ROOT, PROJECT_NAME, BASE_DIR
print(f'export DEPS={DEPS_DIR}')
print(f'export BIN={PROJECT_ROOT}/bin')
print(f'export SRC={PROJECT_ROOT}/src')
print(f'export PROJECT={PROJECT_NAME}')
print(f'export BASE={BASE_DIR}')
")
```
Use `$PROJECT`, `$BIN`, `$SRC`, `$DEPS`, `$BASE` for all paths.

---

## Step 1 — Determine Run Mode

### Mode A: Single Test
User provides `EntityClass.methodName` (e.g., `Solution.createSolution`).
- Parse into `entity_class` and `method_name`
- Proceed to Step 2 (single run + debug loop)

### Mode B: Batch Pipeline (sequential run + heal)
User says "batch", "run all", "run the generated tests", or is handed off from `@test-generator`.
- **Skip directly to Phase 1** (the batch pipeline below)

### Mode C: Re-run generated tests
User says "run the generated tests" or wants to re-run after manual edits.
- Verify `tests_to_run.json` exists and has entries
- **Skip directly to Phase 1** (same batch pipeline)

> **Note**: `@test-generator` only generates test code — it does NOT run tests.
> After generation, invoke `@test-runner` to execute and self-heal.
> This agent handles: running tests from `tests_to_run.json`, single-test execution,
> re-running after manual code changes, and Playwright-based self-healing.

---

## ════════════════════════════════════════════════════════
## MODE A — Single Test Flow (Steps 2-4)
## ════════════════════════════════════════════════════════

---

## Step 2 — Run a Single Test

### 2a. Configure run_test.py

Update `run_test.py` with the target test:
```python
RUN_CONFIG = {
    "entity_class":  "<EntityClass>",
    "method_name":   "<methodName>",
    "url":           SDP_URL,
    "admin_mail_id": SDP_ADMIN_EMAIL,
    "email_id":      SDP_EMAIL_ID,
    "portal_name":   SDP_PORTAL,
    "password":      SDP_ADMIN_PASS,
    "skip_compile":  True,
    "skip_cleanup":  False,
}
```

### 2b. Targeted Compile (if Java files were modified)

NEVER run full project compile (67 pre-existing errors). Only compile the specific module files:
```bash
CP="$BIN:$(find "$DEPS" -name "*.jar" | tr '\n' ':')"
javac -encoding UTF-8 -cp "$CP" -d "$BIN" \
  "$SRC/com/zoho/automater/selenium/modules/<module>/<entity>/common/<Entity>Locators.java" \
  "$SRC/com/zoho/automater/selenium/modules/<module>/<entity>/<EntityBase>.java"
```

### 2c. Execute

```bash
cd /home/balaji-12086/Desktop/Workspace/Zide/ai-automation-qa
.venv/bin/python run_test.py 2>&1
```

### 2d. Parse Result

Check output using priority order:
1. `$$Failure` in output → **FAILED**
2. `"Additional Specific Info":["` + `"successfully"` → **PASSED**
3. `BUILD FAILED` → **FAILED**
4. `BUILD SUCCESSFUL` → **PASSED**
5. Java exceptions (`NullPointerException`, `NoSuchElementException`, `TimeoutException`, etc.) → **FAILED**
6. No positive signal → **FAILED**

Also check ScenarioReport.html:
```bash
ls -t $PROJECT/reports/LOCAL_<methodName>_* | head -1
```
Read the HTML for `data-result="PASS"` / `data-result="FAIL"` / `scenario-result FAIL`.

### 2e. On PASS → done. On FAIL → Step 3 (debug loop).

---

## Step 3 — Debug & Fix (Single Test — max 3 attempts)

**Maximum 3 debug-fix-rerun attempts per test.** After 3 failures, report as unresolvable.

### 3a. Analyze the Failure

1. Read the ScenarioReport.html:
```bash
REPORT_DIR=$(ls -dt $PROJECT/reports/LOCAL_<methodName>_* 2>/dev/null | head -1)
cat "$REPORT_DIR/ScenarioReport.html"
```

2. Search stdout/stderr for the root cause:
   - `NoSuchElementException` → locator XPath is wrong
   - `NullPointerException` in restAPI → preProcess API call failing
   - `TimeoutException` → element slow to appear or selector wrong
   - `ClassNotFoundException` → missing ENTITY_IMPORT_MAP entry
   - `AssertionException` → logic/validation mismatch

### 3b. Classify Failure

| Symptom | Type | Fix Target |
|---------|------|------------|
| `NoSuchElementException` / `TimeoutException` on UI element | LOCATOR | `*Locators.java` — inspect with Playwright |
| `NullPointerException` in restAPI / preProcess | API | preProcess data setup — wrong API path or session |
| `AssertionException` / wrong validation | LOGIC | Test method logic in `*Base.java` |
| javac errors | COMPILE | Syntax/import fix in source |
| Test code is correct but SDP behaviour is wrong | **PRODUCT_BUG** | **No code fix — report to user** |

> **PRODUCT_BUG detection**: After fixing LOCATOR/API/LOGIC issues and confirming the test code
> is correct (element exists, API returns expected data, locator matches), if the test STILL fails
> because the SDP application itself behaves differently from the expected specification — that's
> a product bug. Do NOT keep retrying. Mark as `PRODUCT_BUG` and include it in the bug report.

### 3c. LOCATOR Failures — Use Playwright MCP

This is the most common failure type. Use Playwright browser tools to inspect the live SDP UI and find the correct selector.

#### Login to SDP
```
browser_navigate → SDP_URL (from config)
browser_snapshot → verify login page
browser_fill_form → username/password
browser_click → Login button
browser_snapshot → verify dashboard loaded
```

#### Consult API Reference
Before writing any API path or input wrapper, **read the relevant module section** in `docs/api-doc/SDP_API_Endpoints_Documentation.md` — contains exact V3 paths, HTTP methods, input wrappers, and sub-resource paths for all 16 SDP modules. Do NOT guess.

#### Create prerequisite data (if needed for navigation)
Use `browser_evaluate` with `sdpAPICall()` — browser must be on a logged-in SDP page:
```javascript
// Create entity via API (preferred over UI clicks)
() => sdpAPICall('changes', 'post',
  'input_data=' + JSON.stringify({
    change: { title: "Debug Change " + Date.now(), change_type: { name: "Standard" } }
  })
).responseJSON
```

**CRITICAL**: Use raw `JSON.stringify()` — do NOT use `encodeURIComponent`.

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

#### Navigate to failing state and snapshot
```
browser_navigate → module page
(create data, click through UI to reach the failing state)
browser_snapshot → get accessibility tree
```

#### Identify the correct selector
Compare the snapshot accessibility tree with the broken XPath in `*Locators.java`. Find the element and construct the correct XPath.

**Key SDP UI patterns:**
- Select2 dropdowns: `<li>` in `<div class="select2-drop">` at `<body>` level, NOT inside parent dialog
- Association tab: container ID `change_associations_parent_change`
- Module title: `//div[@id='details-middle-container']/descendant::h1`

#### Cleanup created data
Track all entity IDs created during debugging and DELETE before finishing:
```javascript
() => sdpAPICall('<module>/<id>', 'del').responseJSON
```

### 3d. Apply Fix

Update the locator/code in the Java source file:
- **LOCATOR fix**: Edit `*Locators.java` with the corrected XPath
- **API fix**: Edit preProcess logic or API paths
- **LOGIC fix**: Edit test assertions or flow in `*Base.java`
- **COMPILE fix**: Fix syntax, imports, missing methods

### 3e. Targeted Recompile

Compile ONLY the changed files:
```bash
CP="$BIN:$(find "$DEPS" -name "*.jar" | tr '\n' ':')"
javac -encoding UTF-8 -cp "$CP" -d "$BIN" <list of changed .java files>
```

### 3f. Re-run

Go back to Step 2c. If this is attempt 3 and still failing, report as unresolvable.

---

## Step 4 — Single Test Final Summary

Report the result:
```
| Entity.Method | Result | Attempts | Fix Applied |
|--------------|--------|----------|-------------|
| Solution.createSolution | PASSED | 2 | Fixed XPath for title locator |
```

If unresolvable or PRODUCT_BUG, generate a bug report (see Bug Reports section below).

---

## ════════════════════════════════════════════════════════
## MODE B — Batch Pipeline (Sequential Run + Heal)
## ════════════════════════════════════════════════════════

> This is the structured end-to-end workflow for batch execution.
> Use this when the user says "batch", "run all", or when handed off from `@test-generator`.

---

### Phase 0 — Environment Setup

Same as Step 0 — resolve paths. Additionally:

1. Verify `tests_to_run.json` exists and has entries:
```bash
cat tests_to_run.json | .venv/bin/python -c "import json,sys; d=json.load(sys.stdin); print(f'Tests to run: {len(d.get(\"tests\",[]))}')"
```

2. Ensure targeted compile is done for all modules involved:
```bash
# List unique entity classes to determine which modules need compilation
cat tests_to_run.json | .venv/bin/python -c "
import json,sys
d=json.load(sys.stdin)
entities = set(t['entity_class'] for t in d.get('tests',[]))
print('Entity classes:', ', '.join(sorted(entities)))
"
```

3. Compile all relevant module source files BEFORE the batch run (compile once, run many):
```bash
CP="$BIN:$(find "$DEPS" -name "*.jar" | tr '\n' ':')"
javac -encoding UTF-8 -cp "$CP" -d "$BIN" \
  $SRC/com/zoho/automater/selenium/modules/<module>/<entity>/common/<Entity>Locators.java \
  $SRC/com/zoho/automater/selenium/modules/<module>/<entity>/<EntityBase>.java \
  $SRC/com/zoho/automater/selenium/modules/<module>/<entity>/<Entity>.java \
  $SRC/com/zoho/automater/selenium/modules/<module>/<entity>/utils/<Entity>ActionsUtil.java
# Include ALL files for ALL entity classes found in tests_to_run.json
```

---

### Phase 1 — Load Tests + Generate Execution Plan

Create a categorized execution plan that tracks progress as each test is run and healed sequentially.

**Generate the execution plan:**
```bash
.venv/bin/python -c "
import json, os
from datetime import datetime
from config.project_config import PROJECT_NAME

with open('tests_to_run.json') as f:
    data = json.load(f)
tests = data.get('tests', [])

groups = {}
for t in tests:
    entity = t.get('entity_class', 'Unknown')
    groups.setdefault(entity, []).append(t)

lines = [
    f'# Execution Plan — {PROJECT_NAME}',
    f'',
    f'**Generated**: {datetime.now().strftime(\"%Y-%m-%d %H:%M:%S\")}  ',
    f'**Total tests**: {len(tests)}  ',
    f'**Entity classes**: {len(groups)}  ',
    f'',
    f'---',
    f'',
    f'## Test Progress',
    f'',
    f'| # | Entity.Method | Scenario ID | Status | Attempts | Fix Applied | Notes |',
    f'|---|--------------|-------------|--------|----------|-------------|-------|',
]

idx = 0
for entity in sorted(groups.keys()):
    for t in groups[entity]:
        idx += 1
        method = t.get('method_name', '?')
        sid = t.get('_id', '—')
        lines.append(f'| {idx} | {entity}.{method} | {sid} | ⏳ | 0 | — | — |')

lines.extend([
    f'',
    f'---',
    f'',
    f'## Grouped by Entity',
    f'',
])

for entity in sorted(groups.keys()):
    methods = groups[entity]
    lines.append(f'### {entity} ({len(methods)} tests)')
    for t in methods:
        lines.append(f'- [ ] {t.get(\"method_name\", \"?\")} ({t.get(\"_id\", \"—\")})')
    lines.append('')

plan_path = f'{PROJECT_NAME}/execution_plan.md'
os.makedirs(os.path.dirname(plan_path), exist_ok=True)
with open(plan_path, 'w') as f:
    f.write('\\n'.join(lines) + '\\n')
print(f'Execution plan written to {plan_path}')
"
```

Read the generated execution plan to confirm:
```bash
cat $PROJECT/execution_plan.md
```

---

### Phase 2 — Sequential Run + Heal (one test at a time)

> **Core principle**: Process each test fully (run → diagnose → fix → re-run) before moving to the next.
> This is identical to Mode A Steps 2-4 applied in a loop over `tests_to_run.json`.

**For each test in `tests_to_run.json`:**

#### 2a. Configure + Compile

Update `run_test.py` with the current test's entity_class and method_name (same as Mode A Step 2a).
If any Java files were modified since the last compile, run targeted compile.

#### 2b. Execute + Parse

```bash
.venv/bin/python run_test.py 2>&1
```

Parse using the same priority-order checks from Mode A Step 2d:
1. `$$Failure` → FAILED
2. `"Additional Specific Info":["` + `"successfully"` → PASSED
3. `BUILD FAILED` → FAILED / `BUILD SUCCESSFUL` → PASSED
4. Java exceptions → FAILED
5. No positive signal → FAILED

Also check `ScenarioReport.html` for `data-result` attributes.

#### 2c. On PASS → Log + Next Test

Log the pass to the orchestrator and update the execution plan:
```bash
.venv/bin/python -c "
from orchestrator.client import get_client
get_client().scenario_passed(scenario_id='<ID>', method_name='<method>', module='<module>')
"
```
Update the test's row in `$PROJECT/execution_plan.md`: Status → `✅ PASS`, Attempts → `1`.

Proceed to the next test.

#### 2d. On FAIL → Debug & Fix (max 3 attempts)

Apply the **same debug-fix loop as Mode A Step 3** — analyze ScenarioReport.html, classify failure, use Playwright MCP for LOCATOR issues, apply fix, targeted recompile, re-run.

| Symptom | Type | Fix Target |
|---------|------|------------|
| `NoSuchElementException` / `TimeoutException` | LOCATOR | `*Locators.java` — inspect with Playwright |
| `NullPointerException` in restAPI / preProcess | API | preProcess data / API paths |
| `AssertionException` / wrong validation | LOGIC | Test method in `*Base.java` |
| javac errors | COMPILE | Syntax/import fix |
| SDP behaviour differs from spec | **PRODUCT_BUG** | No code fix — report |

**After each attempt**, re-run and parse. If it passes, log success + move to next test.

**After 3 failed attempts**, mark as PRODUCT_BUG or UNRESOLVABLE:
```bash
.venv/bin/python -c "
from orchestrator.client import get_client
get_client().scenario_failed(scenario_id='<ID>', method_name='<method>', module='<module>', error_message='<error>')
"
```
Update the execution plan row: Status → `🐛 PRODUCT_BUG` or `⛔ UNRESOLVABLE`, Attempts → `3`, Notes → failure summary.

Proceed to the next test.

#### 2e. Progress Reporting

After every test (pass or fail), report progress to the user:
```
[3/15] ✅ DetailsView.verifyAssociationTab — PASSED (attempt 1)
[4/15] 🔧 DetailsView.verifyParentChange — PASSED (attempt 2, fixed XPath)
[5/15] 🐛 ListView.verifyColumnSearch — PRODUCT_BUG after 3 attempts
```

---

### Phase 3 — Final Summary + Bug Reports

#### Summary Table

Present the final results:

```
| # | Entity.Method | Result | Attempts | Fix Applied |
|---|--------------|--------|----------|-------------|
| 1 | DV.verifyAssociationTab | ✅ PASS | 1 | — |
| 2 | DV.verifyParentChange | ✅ PASS | 2 | 🔧 XPath fix |
| 3 | LV.verifyColumnSearch | 🐛 BUG | 3 | — (SDP issue) |
| 4 | DV.verifyDetach | ⛔ UNRESOLVED | 3 | Attempted API fix |
```

#### Aggregate Stats

```
📊 Final Batch Results:
- Total: {N}
- ✅ Passed (first attempt): {N}
- 🔧 Passed (after self-heal): {N}
- 🐛 Product Bugs: {N}
- ⛔ Unresolvable Failures: {N}
- Final Success Rate: {N}%
```

#### Update Execution Plan MD

Write the final status to `$PROJECT/execution_plan.md`:
- Convert `[ ]` checkboxes to `[x]` for passed tests
- Add a "Final Results" section at the bottom with aggregate stats

### Bug Reports (for PRODUCT_BUG and unresolvable FAILED tests)

For every test that ends as **PRODUCT_BUG** or **FAILED after max attempts**, generate a bug report block.
This gives the user everything needed to log the bug:

```
---
🐛 BUG REPORT: <Entity.Method> — <one-line summary>

**Scenario ID**: <@AutomaterScenario id>
**Failure Type**: PRODUCT_BUG | UNRESOLVABLE_FAILURE
**Module**: <module name (e.g., Changes, Requests, Solutions)>
**Severity**: <Critical / Major / Minor — based on impact>

**Summary**:
<2-3 sentence description of what failed and why it appears to be a product issue
vs a test code issue>

**Steps to Reproduce**:
1. Login as <role> (e.g., SDAdmin)
2. Navigate to <module> → <specific page>
3. <exact UI steps that lead to the failure>
4. <what was expected vs what actually happened>

**Expected Result**: <what the test expected to see>
**Actual Result**: <what SDP actually showed/returned>

**Report Path**: `<absolute path to ScenarioReport.html>`
**Screenshot Path**: `<absolute path to screenshots/ folder>`

**Evidence**:
- ScenarioReport.html failure row: <copy the $$Failure line or error message>
- Console error (if any): <Java exception or JS error>
- Playwright snapshot (if captured): <key observation from accessibility tree>

**Debug Notes**: <any additional context from the debug attempts>
---
```

**Rules for bug reports:**
1. **Always include the report path** — find it with: `ls -dt $PROJECT/reports/LOCAL_<methodName>_* | head -1`
2. **Steps to Reproduce must be manual-testable** — write them as if a human QA engineer will follow them
3. **Include the $$Failure message** from ScenarioReport.html
4. **Differentiate PRODUCT_BUG from test issues**: Test code, locators, and data verified correct but SDP behaves unexpectedly → PRODUCT_BUG. Test code issue we couldn't fix after 3 attempts → UNRESOLVABLE_FAILURE
5. **One report per failed test**

---

### Phase 4 — Learning Extraction (Closed Feedback Loop)

> **Purpose**: After all tests are run (Phase 3 complete), analyze the results to extract
> actionable learnings — failure rules and success patterns — and persist them so that
> future `@test-generator` runs (Step 0.7) benefit from this execution's outcomes.
> This is the WRITE side of the learning feedback loop within the Copilot agent ecosystem.

#### 6a. Persist batch results to learnings.jsonl

For EACH test result (passed AND failed), create a JSONL entry:

```bash
.venv/bin/python << 'LEARNING_EXTRACT'
import json, os
from datetime import datetime
from pathlib import Path

LEARNINGS_LOG = Path("logs/learnings.jsonl")
LEARNINGS_LOG.parent.mkdir(parents=True, exist_ok=True)

# Load results from Phase 2 (sequential run + heal)
results_file = "batch_run_results.json"
if not os.path.exists(results_file):
    print("No batch_run_results.json found — skipping learning extraction.")
    exit(0)

with open(results_file) as f:
    data = json.load(f)

results = data if isinstance(data, list) else data.get("results", [])
entries = []

for r in results:
    status = r.get("status", "UNKNOWN")
    method = r.get("method_name", "?")
    entity = r.get("entity_class", "?")
    error  = r.get("error", r.get("failure_info", ""))

    if status in ("PASS", "PASSED"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "learning_type": "PATTERN",
            "title": f"{entity}.{method} passed",
            "body": f"Test {entity}.{method} executed successfully. The locators, data setup, and validation logic are verified working.",
            "source": f"test-runner batch @ {datetime.now().strftime('%Y-%m-%d')}",
            "entity_class": entity,
            "method_name": method,
        }
    else:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "learning_type": "RULE",
            "title": f"{entity}.{method} failed: {error[:80]}",
            "body": f"DO NOT repeat this pattern. Test {entity}.{method} failed with: {error[:200]}",
            "source": f"test-runner batch @ {datetime.now().strftime('%Y-%m-%d')}",
            "entity_class": entity,
            "method_name": method,
        }
    entries.append(entry)

# Append to JSONL
with open(LEARNINGS_LOG, "a", encoding="utf-8") as f:
    for e in entries:
        f.write(json.dumps(e) + "\n")

print(f"Persisted {len(entries)} learnings to {LEARNINGS_LOG}")
print(f"  - PATTERN (success): {sum(1 for e in entries if e['learning_type'] == 'PATTERN')}")
print(f"  - RULE (failure):    {sum(1 for e in entries if e['learning_type'] == 'RULE')}")
LEARNING_EXTRACT
```

#### 6b. Update framework knowledge files (for failures with diagnosed root causes)

For tests that FAILED and were FIXED during Phase 2 (self-heal), extract a DO/DON'T rule
and append it to `config/framework_rules.md`:

```bash
.venv/bin/python << 'RULES_UPDATE'
from pathlib import Path

RULES_FILE = Path("config/framework_rules.md")
LEARNED_HEADER = "\n\n---\n\n## LEARNED RULES (auto-generated by test-runner)\n"

# Collect rules from Phase 2 fix records (self-heal fixes applied during sequential run)
# Format: list of {"test": "Entity.method", "fix_type": "LOCATOR|API|LOGIC", "description": "what was wrong and how it was fixed"}
fix_records = []  # ← populated from Phase 3 fix tracking

# Example: After Phase 2, you tracked fixes like:
# fix_records = [
#   {"test": "DV.verifyAssociationTab", "fix_type": "LOCATOR", "description": "Changed //div[@id='old-id'] to //section[@data-tab='associations']"},
#   {"test": "DV.verifyParentChange", "fix_type": "API", "description": "API path changed from changes/link to changes/{id}/link_parent_change"},
# ]

if not fix_records:
    print("No fix records from Phase 2 — skipping framework_rules.md update.")
    exit(0)

content = RULES_FILE.read_text(encoding="utf-8") if RULES_FILE.exists() else ""

if LEARNED_HEADER.strip() not in content:
    content += LEARNED_HEADER

rules_to_add = []
for fix in fix_records:
    rule = f"\n- **{fix['fix_type']}** (`{fix['test']}`): {fix['description']}"
    if rule.strip() not in content:
        rules_to_add.append(rule)

if rules_to_add:
    content += "\n".join(rules_to_add) + "\n"
    RULES_FILE.write_text(content, encoding="utf-8")
    print(f"Appended {len(rules_to_add)} learned rules to {RULES_FILE}")
else:
    print("All fix rules already in framework_rules.md — no update needed.")
RULES_UPDATE
```

For tests that PASSED, extract success patterns to `config/framework_knowledge.md`:

```bash
.venv/bin/python << 'PATTERNS_UPDATE'
from pathlib import Path

KNOWLEDGE_FILE = Path("config/framework_knowledge.md")
LEARNED_HEADER = "\n\n---\n\n## LEARNED PATTERNS (auto-generated by test-runner)\n"

# Count passes by module to identify which modules are well-covered
import json, os
results_file = "batch_run_results.json"
if not os.path.exists(results_file):
    exit(0)

with open(results_file) as f:
    data = json.load(f)

results = data if isinstance(data, list) else data.get("results", [])
passed_by_entity = {}
for r in results:
    if r.get("status") in ("PASS", "PASSED"):
        entity = r.get("entity_class", "Unknown")
        passed_by_entity.setdefault(entity, []).append(r.get("method_name", "?"))

if not passed_by_entity:
    print("No passed tests — skipping framework_knowledge.md update.")
    exit(0)

content = KNOWLEDGE_FILE.read_text(encoding="utf-8") if KNOWLEDGE_FILE.exists() else ""

if LEARNED_HEADER.strip() not in content:
    content += LEARNED_HEADER

from datetime import datetime
date_str = datetime.now().strftime("%Y-%m-%d")
patterns = []
for entity, methods in passed_by_entity.items():
    line = f"\n- **{entity}** ({date_str}): {len(methods)} tests passed — `{'`, `'.join(methods[:5])}`{'...' if len(methods) > 5 else ''}"
    if entity not in content.split(LEARNED_HEADER.strip())[-1] if LEARNED_HEADER.strip() in content else True:
        patterns.append(line)

if patterns:
    content += "\n".join(patterns) + "\n"
    KNOWLEDGE_FILE.write_text(content, encoding="utf-8")
    print(f"Appended {len(patterns)} success patterns to {KNOWLEDGE_FILE}")
else:
    print("Patterns already recorded — no update needed.")
PATTERNS_UPDATE
```

#### 6c. Log learning event to orchestrator

```bash
.venv/bin/python -c "
from orchestrator.client import get_client
oc = get_client()
oc.log_event(
    event_type='CUSTOM',
    agent='test-runner',
    module='batch',
    feature_name='learning_extraction',
    status='completed',
    metadata={'phase': 'learning_extraction', 'source': 'copilot_test_runner'},
)
print('Learning extraction event logged to orchestrator.')
"
```

> **This step closes the feedback loop.** The `@test-generator` agent reads these learnings
> in Step 0.7 before generating new code. The cycle is:
> `@test-generator` Step 0.7 (read) → Steps 1-6 (generate) → `@test-runner` Phase 2
> (run + heal) → Phase 4 (extract & persist) → next `@test-generator` Step 0.7 (read improved).

---

### Phase 5 — End-to-End Migration Summary

> **Purpose**: Generate a single consolidated document that traces the FULL lifecycle:
> CSV use-case rows → generated test methods → execution results → self-heal fixes →
> bug reports → learned rules. This is the audit trail and deliverable.

```bash
PROJECT=$(.venv/bin/python -c "from config.project_config import PROJECT_NAME; print(PROJECT_NAME)")
```

Generate the migration summary:

```bash
.venv/bin/python << 'MIGRATION_SUMMARY'
import json, os
from datetime import datetime
from pathlib import Path

PROJECT = os.popen(".venv/bin/python -c \"from config.project_config import PROJECT_NAME; print(PROJECT_NAME)\"").read().strip()
TESTCASE_DIR = Path(PROJECT) / "Testcase"
TESTCASE_DIR.mkdir(parents=True, exist_ok=True)

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
summary_path = TESTCASE_DIR / f"migration_summary_{timestamp}.md"

# ── Gather data sources ──
batch_results = []
results_file = "batch_run_results.json"
if os.path.exists(results_file):
    with open(results_file) as f:
        data = json.load(f)
    batch_results = data if isinstance(data, list) else data.get("results", [])

tests_to_run = []
if os.path.exists("tests_to_run.json"):
    with open("tests_to_run.json") as f:
        tests_to_run = json.load(f).get("tests", [])

execution_plan = ""
plan_path = Path(PROJECT) / "execution_plan.md"
if plan_path.exists():
    execution_plan = plan_path.read_text(encoding="utf-8")

learnings = []
learnings_path = Path("logs/learnings.jsonl")
if learnings_path.exists():
    for line in learnings_path.read_text(encoding="utf-8").strip().splitlines()[-20:]:
        line = line.strip()
        if line:
            try:
                learnings.append(json.loads(line))
            except Exception:
                pass

# ── Stats ──
total = len(batch_results)
passed = sum(1 for r in batch_results if r.get("status") in ("PASS", "PASSED"))
failed = sum(1 for r in batch_results if r.get("status") in ("FAIL", "FAILED", "ERROR"))
healed = sum(1 for r in batch_results if r.get("status") in ("PASS", "PASSED") and r.get("was_healed"))
bugs   = sum(1 for r in batch_results if "PRODUCT_BUG" in str(r.get("failure_info", "")))

# ── Build document ──
lines = [
    f"# End-to-End Migration Summary",
    f"",
    f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    f"**Project**: {PROJECT}",
    f"",
    f"---",
    f"",
    f"## Pipeline Overview",
    f"",
    f"```",
    f"CSV Use-Case Document",
    f"  └─ @test-generator (code generation)",
    f"       └─ @test-runner (batch execution)",
    f"            ├─ Phase 2: Sequential Run + Heal (per test)",
    f"            ├─ Phase 3: Final Summary + Bug Reports",
    f"            ├─ Phase 4: Learning Extraction ← framework self-correction",
    f"            └─ Phase 5: This Summary ← you are here",
    f"```",
    f"",
    f"---",
    f"",
    f"## Execution Statistics",
    f"",
    f"| Metric | Count |",
    f"|--------|-------|",
    f"| Tests Generated | {len(tests_to_run)} |",
    f"| Tests Executed | {total} |",
    f"| Passed (first run) | {passed - healed} |",
    f"| Passed (after self-heal) | {healed} |",
    f"| Failed (product bugs) | {bugs} |",
    f"| Failed (unresolvable) | {failed - bugs} |",
    f"| **Final Success Rate** | **{((passed/total)*100) if total else 0:.1f}%** |",
    f"",
    f"---",
    f"",
    f"## Test Results Detail",
    f"",
    f"| # | Entity.Method | Status | Error (if any) |",
    f"|---|--------------|--------|----------------|",
]

for i, r in enumerate(batch_results, 1):
    entity = r.get("entity_class", "?")
    method = r.get("method_name", "?")
    status = r.get("status", "?")
    error  = r.get("error", r.get("failure_info", ""))[:60]
    icon   = "✅" if status in ("PASS", "PASSED") else "❌"
    lines.append(f"| {i} | {entity}.{method} | {icon} {status} | {error} |")

lines += [
    f"",
    f"---",
    f"",
    f"## Learnings Extracted This Run",
    f"",
]

if learnings:
    rules   = [l for l in learnings if l.get("learning_type") == "RULE"]
    patterns = [l for l in learnings if l.get("learning_type") == "PATTERN"]
    lines.append(f"### Failure Rules ({len(rules)} extracted)")
    lines.append(f"")
    for r in rules[-10:]:
        lines.append(f"- **{r.get('title', '?')}**: {r.get('body', '')[:120]}")
    lines.append(f"")
    lines.append(f"### Success Patterns ({len(patterns)} recorded)")
    lines.append(f"")
    for p in patterns[-10:]:
        lines.append(f"- {p.get('title', '?')}")
else:
    lines.append("_No learnings extracted (first run or learnings.jsonl empty)._")

lines += [
    f"",
    f"---",
    f"",
    f"## Framework Files Updated",
    f"",
    f"| File | Section | Impact |",
    f"|------|---------|--------|",
    f"| `config/framework_rules.md` | LEARNED RULES | Failure rules appended — prevents repeat mistakes |",
    f"| `config/framework_knowledge.md` | LEARNED PATTERNS | Success patterns appended — guides future generation |",
    f"| `logs/learnings.jsonl` | (append-only log) | Full history — read by @test-generator Step 0.7 on next generation run |",
    f"",
    f"---",
    f"",
    f"## Artifacts",
    f"",
    f"| Artifact | Location |",
    f"|----------|----------|",
    f"| Use-case CSV | `{PROJECT}/Testcase/` (original upload) |",
    f"| Execution Plan | `{PROJECT}/execution_plan.md` |",
    f"| Run Results | `batch_run_results.json` (if generated) |",
    f"| Bug Reports | See Phase 3 output above |",
    f"| This Summary | `{summary_path}` |",
    f"| ScenarioReport HTMLs | `{PROJECT}/reports/LOCAL_*/ScenarioReport.html` |",
    f"",
]

summary_path.write_text("\n".join(lines), encoding="utf-8")
print(f"Migration summary written to: {summary_path}")
print(f"Stats: {total} tests | {passed} passed | {failed} failed | {((passed/total)*100) if total else 0:.1f}% success rate")
MIGRATION_SUMMARY
```

Read and present the summary to the user:

```bash
cat "$PROJECT/Testcase/migration_summary_"*.md | tail -1 | xargs -I{} dirname {} | head -1
# Or simply:
ls -t "$PROJECT/Testcase/migration_summary_"*.md 2>/dev/null | head -1 | xargs cat
```

Present the key stats:

```
📋 End-to-End Migration Summary Generated
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Pipeline: CSV → @test-generator → @test-runner → Learning Extraction
Tests: {N} generated → {N} executed → {pass_rate}% success rate

✅ Passed (first run): {N}
🔧 Passed (self-healed): {N}
🐛 Product Bugs: {N}
⛔ Unresolvable: {N}

📝 Learnings: {N} rules + {N} patterns → framework files updated
📁 Summary: {PROJECT}/Testcase/migration_summary_{timestamp}.md

The learning loop is now closed:
  @test-generator reads learnings → generates code → @test-runner executes →
  extracts learnings → updates framework files → @test-generator reads improved context
```

---

## Batch Mode — tests_to_run.json Format

When writing tests to `tests_to_run.json` for batch execution:

```json
{
  "parallelism": 1,
  "learning_retries": 1,
  "tests": [
    {
      "_id": "SCENARIO_ID",
      "entity_class": "EntityClass",
      "method_name": "methodName",
      "url": "$(SDP_URL)",
      "admin_mail_id": "$(SDP_ADMIN_EMAIL)",
      "email_id": "$(SDP_ADMIN_EMAIL)",
      "portal_name": "$(SDP_PORTAL)",
      "skip_compile": true
    }
  ]
}
```

Placeholders `$(SDP_URL)`, `$(SDP_ADMIN_EMAIL)`, `$(SDP_PORTAL)` are resolved at runtime from `config/project_config.py`.

### batch_run_helper.py API

The batch runner is invoked from the terminal. It supports two modes:

```bash
# Single test (returns RESULT:PASS|... or RESULT:FAIL|...)
.venv/bin/python batch_run_helper.py <EntityClass> <methodName>

# Full batch from tests_to_run.json (runs all sequentially)
.venv/bin/python batch_run_helper.py --batch

# Batch from a specific JSON file
.venv/bin/python batch_run_helper.py --batch --json path/to/tests.json
```

**Batch output files:**
- `batch_run_results.json` — structured results with status, report_path, failure_info per test
- `batch_run_results.md` — human-readable Markdown summary table

**Structured result format** (in `batch_run_results.json`):
```json
{
  "started_at": "2026-03-11 14:30:00",
  "finished_at": "2026-03-11 15:45:00",
  "total": 34,
  "passed": 28,
  "failed": 6,
  "skipped": 0,
  "results": [
    {
      "entity_class": "DetailsView",
      "method_name": "verifyAssociationTab",
      "scenario_id": "LNKCHG_DV_001",
      "status": "PASS",
      "report_path": "/path/to/ScenarioReport.html",
      "failure_info": "",
      "duration_seconds": 45.2,
      "test_key": "DetailsView.verifyAssociationTab"
    }
  ]
}
```

---

## Report Locations

- Reports: `$PROJECT/reports/LOCAL_<methodName>_<timestamp>/ScenarioReport.html`
- Screenshots: `$PROJECT/reports/LOCAL_<methodName>_<timestamp>/screenshots/`

## Orchestrator Logging (fire-and-forget)

Before logging, ensure the orchestrator server is running (idempotent — safe to call every time):
```bash
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
./orchestrator.sh start
```

After each test result, log to the orchestrator:
```bash
.venv/bin/python -c "
from orchestrator.client import get_client
oc = get_client()
oc.scenario_passed(scenario_id='<ID>', method_name='<method>', module='<module>')
"
```
Or on failure:
```bash
.venv/bin/python -c "
from orchestrator.client import get_client
get_client().scenario_failed(scenario_id='<ID>', method_name='<method>', module='<module>', error_message='<error>')
"
```
If the orchestrator isn't running, events are silently saved to `orchestrator/offline_events.jsonl`.

---

## Constraints

- NEVER run full project compile — only targeted module compile
- NEVER modify `AutomaterSeleniumFramework/` source without explicit approval
- NEVER guess locators — always verify with `browser_snapshot` first
- ALWAYS clean up test data created during Playwright debugging sessions
- Maximum 3 debug-fix-rerun attempts per failed test before moving on
