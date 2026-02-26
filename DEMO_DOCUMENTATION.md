# AI Automation QA — Demo Documentation

> **What this system does:** Accepts a plain English feature description and autonomously
> generates, validates, compiles, and runs a Java Selenium test case for Zoho ServiceDesk Plus —
> with zero manual coding.

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Agent Pipeline — Step by Step](#2-agent-pipeline--step-by-step)
3. [Every File Read Before a Test Case is Generated](#3-every-file-read-before-a-test-case-is-generated)
4. [Generated Output — What Gets Written](#4-generated-output--what-gets-written)
5. [Existing Module vs New Feature — Can it handle both?](#5-existing-module-vs-new-feature--can-it-handle-both)
6. [Self-Healing — What Happens When a Test Fails](#6-self-healing--what-happens-when-a-test-fails)
7. [Knowledge Base Architecture](#7-knowledge-base-architecture)
8. [End-to-End Demo Flow](#8-end-to-end-demo-flow)

---

## 1. System Overview

```
You type:
  "Create a test case that creates an incident request and adds a note
   with text 'Case generated from Claude AI' in its detail page."

The system:
  ├── Understands the requirement (Planner)
  ├── Checks if it already exists (Coverage)
  ├── Surfs the live SDP UI to observe real behaviour (UIScout)
  ├── Reads all relevant Java source files (ContextBuilder)
  ├── Writes the Java test code via LLM (Coder)
  ├── Validates the code against framework rules (Reviewer)
  ├── Writes it into the correct .java files (Output)
  ├── Compiles + runs it (Runner)
  └── Heals itself if it fails (Healer)
```

**Technology Stack:**
| Layer | Technology |
|---|---|
| Orchestration | LangGraph (stateful agent graph) |
| LLM | Local Ollama (`qwen2.5-coder:7b`) / GPT-4o |
| Vector DB | ChromaDB (local, persistent) |
| UI Automation | Playwright (Python) for scouting + healing |
| Test Framework | Selenium + AutomaterSelenium (Java) |
| Build | `javac` targeted compile |

---

## 2. Agent Pipeline — Step by Step

```
 User Input
     │
     ▼
┌─────────────┐
│  1. PLANNER │  Understands intent, maps to SDP module(s)
└──────┬──────┘
       │  test_plan: { "requests/request": [{description, type, group, priority}] }
       ▼
┌──────────────┐
│  2. COVERAGE │  Checks ChromaDB — is this scenario already tested?
└──────┬───────┘
       │  coverage_gaps: [new scenarios only] | duplicate_warnings: [existing ones]
       ▼
┌────────────────┐
│  3. UI SCOUT   │  Opens live SDP browser → captures real form fields & buttons
└──────┬─────────┘
       │  ui_observations: [{visible_fields, visible_buttons, required_fields, notes}]
       ▼
┌───────────────┐
│  4. CODER     │  Reads 8 source types + observations → LLM generates Java code
└──────┬────────┘
       │  generated_code: "// ===== ADD TO: Solution.java ===== ..."
       ▼
┌────────────────┐
│  5. REVIEWER   │  Validates: annotations, ID format, try/catch, no hardcoded selectors
└──────┬─────────┘
       │  approved OR revision_requests → loops back to Coder (max 2 retries)
       ▼
┌───────────────┐
│  6. OUTPUT    │  Writes code into correct .java files in the project
└──────┬────────┘
       ▼
┌───────────────┐
│  7. RUNNER    │  javac compile → execute test → capture HTML report
└──────┬────────┘
       │  PASS → Done ✅
       │  FAIL ↓
       ▼
┌───────────────┐
│  8. HEALER    │  Playwright browser → snapshots failing UI → LLM patches Java → re-runs
└───────────────┘
```

---

## 3. Every File Read Before a Test Case is Generated

When you say _"Create a test case for requests/request"_, here is the **exact read sequence**:

### Stage A — Planner Agent

| File | Path | What it reads |
|---|---|---|
| `module_taxonomy.yaml` | `config/module_taxonomy.yaml` | All SDP modules, their aliases, and descriptions — so the LLM knows `"incident"` maps to `requests/request` |

---

### Stage B — Coverage Agent

| Source | What it queries |
|---|---|
| ChromaDB `automater_scenarios` collection | Semantic vector search — finds existing test cases similar to your description to avoid duplicates |

---

### Stage C — UI Scout Agent _(live Playwright browser)_

| What it does | Data captured |
|---|---|
| Opens real SDP browser, logs in as admin | — |
| Navigates to the target module's create form | Visible form fields, required field markers |
| Clicks key toggles/checkboxes | State change observations (which buttons appear/disappear) |
| Captures accessibility snapshot | All visible buttons at that moment |

> ⚡ This is the **only agent that hits the live application** before code is written.
> It prevents wrong assumptions (e.g. a button that only appears after a toggle is clicked).

---

### Stage D — Coder Agent _(the main context assembly)_

This is where the most files are read. The `ContextBuilder` reads **directly from disk**:

#### From `knowledge_base/raw/module_index.json`
The index tells it which Java files belong to the target module.

#### Then reads these Java source files:

| File Type | Example for `requests/request` | What the LLM uses it for |
|---|---|---|
| **Fields.java** | `RequestFields.java` | Know all field names, data paths, field types |
| **DataConstants.java** | `RequestDataConstants.java` | Know valid test data key constants |
| **Locators.java** | `RequestLocators.java` | Know all XPath/By locators — never hardcodes them |
| **Constants.java** | `RequestConstants.java` | Know string constants (module name, alert messages) |
| **Sample scenario files** | `RequestBase.java`, `Request.java` (up to 2, 4000 chars each) | Learn the exact coding pattern used in this module |

#### From ChromaDB (in-process, no HTTP):
| Collection | Query | Purpose |
|---|---|---|
| `automater_scenarios` | Semantic search on your description | Find 3–5 similar existing test cases as pattern reference |
| `automater_help_topics` | Semantic search on feature description | SDP help guide: field definitions, workflow steps, feature overview |

#### From config files:
| File | Path | What it provides |
|---|---|---|
| `framework_grammar.yaml` | `config/framework_grammar.yaml` | Annotation rules, required fields, code template skeleton |
| `framework_rules.md` | `config/framework_rules.md` | 26 strict coding rules injected into LLM system prompt |

#### Full context assembled into LLM prompt:
```
════════════════════════════════════
FRAMEWORK CONTEXT FOR CODE GENERATION
════════════════════════════════════
## Target Module: requests/request
## Existing Scenario IDs (do NOT reuse): SDPOD_AUTO_IR_CREATE_001, ...

## Field Definitions (RequestFields.java):     ← disk read
## Available Test Data Constants:              ← disk read
## UI Locators (RequestLocators.java):         ← disk read
## Existing Scenario Class Sample 1:           ← disk read
## Similar Existing Test Cases:                ← ChromaDB query
## Framework Annotation Rules:                 ← framework_grammar.yaml
## LIVE UI Behaviour Observations:             ← UIScout (Playwright)
## SDP Application Context (help guide):       ← ChromaDB help_topics query
## Your Task: Generate test case for ...
```

---

### Stage E — Reviewer Agent

| What it checks | How |
|---|---|
| `@AutomaterScenario` annotation present | Regex |
| ID format `SDPOD_AUTO_<MODULE>_<AREA>_NNN` | Regex |
| `try/catch/finally` structure | Regex |
| `addSuccessReport` + `addFailureReport` both present | Regex |
| No hardcoded `By.xpath(` strings | Regex |
| `startMethodFlowInStepsToReproduce` / `endMethodFlowInStepsToReproduce` | Regex |
| LLM review for semantic correctness | LLM call |

If any check fails → sends **revision instructions** back to Coder (up to 2 retries).

---

## 4. Generated Output — What Gets Written

The LLM generates a **two-piece output** format. One scenario produces edits to **two files**:

### File 1 — `<Entity>.java` (thin wrapper)
```java
// ===== ADD TO: Solution.java =====
@Override
@AutomaterScenario(
    id          = "SDPOD_AUTO_SOL_CREATE_128",
    group       = "createIncidentForNotes",
    priority    = Priority.HIGH,
    dataIds     = {},
    tags        = {},
    owner       = OwnerConstants.RAJESHWARAN_A,
    runType     = ScenarioRunType.USER_BASED,
    description = "Create incident request via API, add notes in detail page"
)
public void createIncidentRequestAndAddNotes() {
    super.createIncidentRequestAndAddNotes();  // delegates to Base
}
```

### File 2 — `<Entity>Base.java` (actual test logic)
```java
// ===== ADD TO: SolutionBase.java =====
public void createIncidentRequestAndAddNotes() {
    report.startMethodFlowInStepsToReproduce(...);
    try {
        AdminActionsUtil.openRequestUsingShortCut(LocalStorage.getAsString("displayId"));
        actions.click(RequestLocators.DetailView.ICN_ADD_NOTE);
        actions.formBuilder.fillHTMLField("descname", "Case generated from Claude AI");
        actions.click(RequestLocators.DetailView.RequestNotes.NOTES_SAVE_BUTTON);
        actions.waitForAjaxComplete();
        if (actions.isElementPresent(RequestLocators.DetailView.VERIFY_NOTES)) {
            addSuccessReport("Notes added successfully...");
        } else {
            addFailureReport("Verification failed", "Note not found");
        }
    } catch (Exception e) {
        addFailureReport("Error in " + getMethodName(), e.getMessage());
    } finally {
        report.endMethodFlowInStepsToReproduce();
    }
}
```

### Generated snippet files saved to:
```
generated/
└── 20260226_120000_requests_request/
    ├── 1_ADD_TO_Request.java        ← paste into Request.java
    ├── 2_ADD_TO_RequestBase.java    ← paste into RequestBase.java
    └── WHAT_TO_DO.txt               ← exact file paths + instructions
```

---

## 5. Existing Module vs New Feature — Can it handle both?

### ✅ Existing Module (e.g., Requests, Solutions, Problems)

The system has **maximum context** because:
- Java source files are already indexed in `module_index.json`
- Existing scenarios are in ChromaDB for pattern reference and dedup
- UIScout has pre-defined `MODULE_SCOUT_PLANS` for these modules
- Help guide topics are indexed for these modules

**Result:** High quality, framework-compliant code generated on first attempt.

---

### ✅ New Feature on an Existing Module

Example: _"Add a test for the new AI-Suggested Solutions feature in the Request module"_

- Planner maps it to `requests/request` (existing module)
- Coverage Agent sees no existing test → marks it as `new` (coverage gap)
- UIScout navigates to the actual feature in the live app and captures its UI behaviour
- Coder uses existing locators/constants from `RequestLocators.java` + live UI observations
- If new locators are needed → the **Healer Agent** discovers the correct XPaths via Playwright

**Result:** New feature tests generated using existing module infrastructure.

---

### ⚠️ Completely New Module (never indexed)

Example: _"Add tests for a brand new CMDB module"_

- Planner may not find it in `module_taxonomy.yaml` → marks as unknown module
- `module_index.json` has no entry → `ContextBuilder` returns empty source files
- ChromaDB has no similar scenarios to reference
- UIScout has no `MODULE_SCOUT_PLANS` entry → skips live scouting

**Result:** The LLM generates code using only the framework skeleton and rules — it will compile but may miss module-specific locators. This requires:
1. Running `rag_indexer.py` to index the new module's Java source files
2. Adding the module to `module_taxonomy.yaml` and `MODULE_SCOUT_PLANS`

---

## 6. Self-Healing — What Happens When a Test Fails

```
Test FAILS
    │
    ▼
HealerAgent classifies failure type (via LLM):
  LOCATOR_FAILURE  → XPath/element not found
  API_FAILURE      → REST API call returned null
  LOGIC_FAILURE    → Wrong test flow / assertion
  COMPILE_FAILURE  → Java compile error

    │
    ▼ (for LOCATOR_FAILURE)
Playwright opens real browser
    ├── Logs in, navigates to failing UI state
    ├── Captures accessibility snapshot (full element tree)
    └── LLM maps snapshot → correct XPath

    ▼
Patches the Java source file with fixed locator
    ▼
Re-compiles (targeted javac — only changed files)
    ▼
Re-runs the test
    ▼
PASS ✅ or reports remaining issue
```

**Key advantage:** The healer has access to the **same live application** the test targets —
so it derives locators from actual rendered HTML, not static guesses.

---

## 7. Knowledge Base Architecture

```
knowledge_base/
├── chroma_db/                    ← ChromaDB persistent vector store
│   ├── automater_scenarios       ← All existing @AutomaterScenario metadata
│   ├── automater_source_files    ← Java source file chunks (indexed by entity)
│   ├── automater_modules         ← Per-module summary docs
│   └── automater_help_topics     ← SDP help guide articles
│
└── raw/
    ├── scenarios_flat.json       ← All scenarios extracted from Java source
    ├── module_index.json         ← Maps module_path → file paths on disk
    ├── testcases_parsed.json     ← Parsed test case metadata
    ├── help_topics_flat.json     ← SDP help guide (crawled)
    └── help_topics.json          ← Structured help content
```

### How the KB is populated:
```bash
# Index all scenarios + source files into ChromaDB
python knowledge_base/rag_indexer.py

# Crawl SDP help guide
python ingestion/help_doc_crawler.py
```

> **Note:** Agents access ChromaDB **directly in-process** via `VectorStore`.
> The `rag_server.py` FastAPI server is a separate REST interface for external tools
> (Web UI, curl) — it is **not** called during the generation pipeline.

---

## 8. End-to-End Demo Flow

### Input
```python
# main.py or direct agent call
feature_description = """
Create a test case that navigates to an incident request's detail page
and adds a note with the text 'Case generated from Claude AI'.
The incident request should be created via API in the preProcess step.
"""
target_modules = ["requests/request"]  # optional hint
```

### What happens (with approximate timing)

| Step | Agent | Time | Output |
|---|---|---|---|
| 1 | Planner | ~3s | `test_plan` with 1 scenario for `requests/request` |
| 2 | Coverage | ~1s | Confirms no duplicate in ChromaDB |
| 3 | UIScout | ~30s | Captures New Request form fields + buttons from live app |
| 4 | Coder | ~15s | Reads 5 Java files + queries ChromaDB + calls LLM → Java code |
| 5 | Reviewer | ~5s | Validates 8 static checks + LLM review → approved |
| 6 | Output | ~1s | Writes to `generated/` folder + WHAT_TO_DO.txt |
| 7 | Runner | ~90s | `javac` compile → Firefox browser → test executes → HTML report |
| 8 | Healer | (if needed) | Playwright snapshot → fix → recompile → rerun |

### Output
```
✅ PASSED — IncidentRequestNotes.createIncidentRequestAndAddNotes
  Report: SDPLIVE_LATEST_AUTOMATER_SELENIUM/reports/LOCAL_createIncidentRequestAndAddNotes_*/ScenarioReport.html
```

**HTML Report contains:**
- Step-by-step screenshots of every action
- Pass/Fail status per step
- Exact user and role used
- Time taken per step

---

## Summary

| Capability | Status |
|---|---|
| Generate tests from plain English | ✅ |
| Gap-aware (no duplicate generation) | ✅ |
| Reads actual project Java files as context | ✅ |
| Observes live UI before generating code | ✅ |
| Validates generated code against 26 rules | ✅ |
| Compiles and runs the test automatically | ✅ |
| Self-heals failing tests via Playwright | ✅ |
| Supports new features on existing modules | ✅ |
| Supports completely new modules | ⚠️ Requires KB indexing first |
| Works without internet (local LLM) | ✅ (Ollama) |
