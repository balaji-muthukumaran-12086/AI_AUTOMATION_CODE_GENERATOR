# AI Test Automation Orchestrator — Technical Demo Document

**Author:** Balaji M  
**Date:** March 3, 2026  
**Duration of Build:** February 24 – March 3, 2026 (8 working days)  
**Repository:** [AI_AUTOMATION_CODE_GENERATOR](https://github.com/balaji-muthukumaran-12086/AI_AUTOMATION_CODE_GENERATOR)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [The Problem We're Solving](#2-the-problem-were-solving)
3. [Solution Overview](#3-solution-overview)
4. [Understanding the Existing Automation Framework](#4-understanding-the-existing-automation-framework)
5. [What We Built — The AI Layer](#5-what-we-built--the-ai-layer)
6. [Knowledge Base & RAG — Why It's Critical](#6-knowledge-base--rag--why-its-critical)
7. [The Agentic Pipeline — Step by Step](#7-the-agentic-pipeline--step-by-step)
8. [Web UI — The Interface](#8-web-ui--the-interface)
9. [Self-Healing with Playwright](#9-self-healing-with-playwright)
10. [Parallel Execution & Learning Loop](#10-parallel-execution--learning-loop)
11. [Real Results — Tests That Passed](#11-real-results--tests-that-passed)
12. [Day-by-Day Build Timeline](#12-day-by-day-build-timeline)
13. [Project Statistics](#13-project-statistics)
14. [How to Run — Quick Start](#14-how-to-run--quick-start)
15. [What's Next — Roadmap](#15-whats-next--roadmap)
16. [Appendix A: Agentic Pipeline Architecture (Detailed)](#appendix-a-agentic-pipeline-architecture-detailed)

---

## 1. Executive Summary

We built an **AI-powered system that automatically generates production-ready Selenium test cases** for ServiceDesk Plus (SDP) from plain-English feature descriptions or uploaded documents.

**In one sentence:** Upload a feature document → the system reads it, plans test scenarios, checks for duplicates, observes the live UI, generates Java test code, reviews it, compiles it, runs it, and if it fails — self-heals and retries. All without human intervention.

### Key Numbers

| Metric | Value |
|--------|-------|
| Total development time | 8 days |
| Lines of Python code written | **12,194** |
| AI agents built | **14** (across 17 files) |
| Knowledge base vectors | **14,637** scenarios indexed |
| Modules covered | **210** SDP modules |
| Tests successfully generated & passing | **8+** (Solutions, Requests, Changes, Problems) |
| LLM calls per generation run | 3–7 (local Ollama or OpenRouter) |
| Git commits | **36** |

---

## 2. The Problem We're Solving

### The Current Pain Point

Writing automation test cases for SDP is a **manual, time-intensive process**:

1. A developer reads the feature requirements document
2. They study the existing framework conventions (annotations, data files, locators, constants)
3. They write the Java test code — often 100+ lines per scenario
4. They create test data JSON entries
5. They compile, run, debug, fix locators, re-run
6. Repeat for every new feature

**For a typical feature with 6 test scenarios, this takes 2-3 days of a developer's time.**

### The Scale Problem

Our automation framework (`SDPLIVE_LATEST_AUTOMATER_SELENIUM`) already has:
- **17,101 test scenarios** across 210 modules
- **1,426 Java source files**
- A complex two-layer architecture (`Entity.java` → `EntityBase.java` → `Entity extends EntityBase`)

Every new feature adds more. The framework follows strict conventions — any deviation breaks the build or produces false positives.

### What If...

> What if we could hand a feature document to an AI system, and it produces working, convention-compliant test code that compiles and passes — **in minutes instead of days**?

That's what we built.

---

## 3. Solution Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   📄 Input                        📦 Output                     │
│                                                                 │
│   Feature document          →     Working Java test code        │
│   (PDF / DOCX / XLSX /            that is:                      │
│    Markdown / plain text)         ✅ Framework-compliant          │
│                                   ✅ Compiled                     │
│   OR                              ✅ Executed against live SDP    │
│                                   ✅ Self-healed if broken        │
│   Plain-English description       ✅ Ready to commit               │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

The system has three major layers:

| Layer | Purpose | Technology |
|-------|---------|------------|
| **Knowledge Base** | Understand all 17,101 existing tests + framework rules | ChromaDB vector store + sentence-transformers |
| **Agent Pipeline** | 10-agent LangGraph pipeline that plans, codes, reviews, runs, heals | Python + LangGraph + Ollama/OpenRouter |
| **Web UI** | Upload documents, track progress, view results | FastAPI + SSE + HTML/JS |

---

## 4. Understanding the Existing Automation Framework

Before explaining the AI layer, let's understand what we're generating code for.

### AutomaterSelenium — The Java Framework

The SDP QA team uses a homegrown Java Selenium framework called **AutomaterSelenium**. It follows a strict architecture:

#### Two-Layer Class Architecture

```
Entity (framework base class)
  └── <Entity>Base extends Entity          ← ALL test logic goes here
        └── <Entity> extends <Entity>Base  ← ONLY annotations go here
```

**Example:**
```
Solution.java        → @AutomaterScenario annotations only (thin wrapper)
SolutionBase.java    → Actual test implementation (navigate, fill form, validate)
```

#### File Structure Per Entity (7 files per module)

```
modules/<module>/<entity>/
├── <Entity>.java                          ← Annotation wrapper
├── <Entity>Base.java                      ← Test implementation
├── common/
│   ├── <Entity>Locators.java             ← XPath/CSS selectors
│   ├── <Entity>Constants.java            ← UI string constants
│   ├── <Entity>DataConstants.java        ← Data key enums
│   ├── <Entity>AnnotationConstants.java  ← Group/data string constants
│   └── <Entity>Fields.java              ← Field name/type definitions
│
resources/entity/
├── conf/<module>/<entity>.json           ← Field configuration
└── data/<module>/<entity>/<entity>_data.json  ← Test input data
```

#### Test Lifecycle

```
1. Runner invokes @AutomaterScenario method
2. Entity.run() →
   ├── initializeAdminSession()      → Browser logs in as admin
   ├── preProcess(group, dataIds[])  → REST API creates test data (templates, topics)
   ├── switchToUserSession()         → Browser switches to test user
   ├── <test method body>            → UI navigation, form filling, validation
   └── postProcess()                 → Cleanup via REST API
3. Report is generated (HTML + screenshots)
```

#### Key Behaviors the AI Must Follow

| Convention | Rule |
|-----------|------|
| Boolean fields | Framework's `fillInputForAnEntity` silently skips JSON booleans. Checkboxes MUST be clicked via explicit locators |
| Button matching | Must use `normalize-space(text())='Add'` not `contains(text(),'Add')` to avoid matching "Add And Approve" |
| API calls | Go through the browser via JavaScript (`sdpAPICall(...)`) — not direct HTTP |
| preProcess session | API calls must run in admin session (preProcess), not user session (method body) |
| Data placeholders | `$(custom_X)` resolves to `LocalStorage.getAsString("X")` at runtime |

**This is why we need a knowledge base** — the AI must learn all of these conventions from the existing 17,101 test scenarios, not guess them.

---

## 5. What We Built — The AI Layer

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        AI Orchestrator Platform (Web UI)                 │
│                        http://localhost:9500                             │
│                                                                          │
│  ┌────────────────────┐    ┌──────────────────────────────────────────┐  │
│  │  📄 Document Upload │    │           Generated Output Panel         │  │
│  │                    │    │                                          │  │
│  │  - Feature doc     │    │  ✅ Solution.java (lines 3890–3920)       │  │
│  │  - Help article    │ →  │  ✅ SolutionBase.java (lines 7361–7420)   │  │
│  │  - Use-case sheet  │    │  ✅ solution_data.json (new data key)     │  │
│  │  - User story      │    │                                          │  │
│  └────────────────────┘    │  [View Diff]  [Copy]  [Run Test]         │  │
│                            └──────────────────────────────────────────┘  │
└───────────────────────────────────────────┬──────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         Agent Pipeline (LangGraph)                       │
│                                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Ingestion│→ │ Planner  │→ │ Coverage │→ │ UI Scout │→ │  Coder   │  │
│  │ Agent    │  │ Agent    │  │ Agent    │  │ Agent    │  │  Agent   │  │
│  │          │  │ 🤖 LLM   │  │ ChromaDB │  │ 🤖+🌐    │  │ 🤖 LLM   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│                                                                │         │
│                                                                ▼         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Hg Agent │← │ Healer   │← │  Runner  │← │  Output  │← │ Reviewer │  │
│  │ (VCS)    │  │ Agent    │  │  Agent   │  │  Agent   │  │ Agent    │  │
│  │          │  │ 🤖+🌐    │  │ ☕ Java  │  │ 📁 File  │  │ 🤖 LLM   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
│                                                                          │
│  🤖 = LLM call    🌐 = Playwright browser    ☕ = Java subprocess        │
└──────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                        Knowledge Base (ChromaDB)                         │
│                                                                          │
│  14,637 vectors from 17,101 scenarios across 210 modules                │
│  + Framework rules, help topics, field configs                           │
│  + AI-generated scenarios (auto-indexed after each run)                  │
└──────────────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Agent orchestration | **LangGraph** (LangChain) | State machine with conditional routing, revision loops, shared state |
| LLM (local) | **Ollama** + `qwen2.5-coder:7b` | Free, runs locally, no API costs, 4.3 GiB RAM |
| LLM (cloud) | **OpenRouter** → `gpt-4o-mini` | Better quality when needed, tool-calling support |
| Vector database | **ChromaDB** + `all-MiniLM-L6-v2` | Lightweight, embeddable, fast cosine similarity search |
| Browser automation | **Playwright** (Chromium) | UI observation + self-healing — async, headless capable |
| Test execution | **Java (javac)** + Selenium + Firefox | Framework-native compilation and execution |
| Web server | **FastAPI** + SSE streaming | Real-time progress updates, async pipeline execution |
| Version control | **Mercurial** (hg) | SDP codebase uses Mercurial; auto-branch commit on test pass |
| Containerization | **Docker** + docker-compose | Portable deployment (Dockerfile included) |

---

## 6. Knowledge Base & RAG — Why It's Critical

### The Problem with "Just Ask an LLM"

If you ask ChatGPT or any LLM to "write a Selenium test for creating a solution in SDP", it will produce generic Selenium code that:
- Doesn't follow `AutomaterSelenium` conventions
- Uses wrong class hierarchy
- Misses `@AutomaterScenario` annotations
- Creates incorrect data JSON structure
- Uses locators that don't exist in SDP's DOM

**The LLM has never seen our framework. It needs context.**

### RAG — Retrieval-Augmented Generation

RAG solves this by giving the LLM **real examples from our codebase** before asking it to generate code.

```
                         User's feature description
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │     ChromaDB Search        │
                    │  "Find 3 most similar      │
                    │   existing test scenarios"  │
                    └───────────┬───────────────┘
                                │
                    ┌───────────▼───────────────┐
                    │     Retrieved Context       │
                    │                             │
                    │  1. SolutionBase.java       │
                    │     createSolution() — 50   │
                    │     lines of real code      │
                    │                             │
                    │  2. solution_data.json       │
                    │     Template + field config  │
                    │                             │
                    │  3. SolutionLocators.java    │
                    │     Real XPath selectors     │
                    └───────────┬───────────────┘
                                │
                    ┌───────────▼───────────────┐
                    │     LLM Prompt              │
                    │                             │
                    │  "Here are 3 similar tests.  │
                    │   Here are framework rules.  │
                    │   Here are live UI snapshots. │
                    │   Now generate THIS test."   │
                    └───────────┬───────────────┘
                                │
                                ▼
                    Framework-compliant Java code
```

### Knowledge Base Contents

| Collection | Count | Source | Purpose |
|-----------|-------|--------|---------|
| **Scenarios** | 14,637 vectors | Parsed from 1,426 Java files | Find similar existing tests to use as examples |
| **Source Chunks** | 8,722 vectors | Actual Java source code chunks | Provide real code patterns to the LLM |
| **Help Topics** | 920 vectors | Crawled SDP help documentation | Understand module features and field descriptions |

### How Indexing Works

```bash
# Step 1: Parse all Java files → structured JSON
python main.py ingest

# Step 2: Build ChromaDB vectors
python main.py index

# Output: knowledge_base/chroma_db/ (persistent on disk)
```

The indexer:
1. Reads every `.java` file under `SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/`
2. Extracts `@AutomaterScenario` annotations → scenario metadata
3. Extracts method bodies → source code chunks
4. Builds embedding text: `"Module: {path} | Entity: {entity} | Test ID: {id} | Method: {method} | Description: {desc}"`
5. Upserts into ChromaDB with cosine similarity

### Duplicate Detection

When a feature is submitted for generation, the **CoverageAgent** checks every planned scenario against the knowledge base:

| Similarity Score | Classification | Action |
|-----------------|---------------|--------|
| ≥ 0.90 | **Duplicate** | Skip — already exists |
| 0.75 – 0.89 | **Similar** | Generate with a note |
| < 0.75 | **New** | Generate — this is a coverage gap |

After generation, new scenarios are **automatically indexed** back into ChromaDB so they're detected as duplicates on subsequent runs.

---

## 7. The Agentic Pipeline — Step by Step

### Why Agents? Why Not Just One LLM Call?

A single LLM call cannot:
- Parse uploaded documents (PDF/DOCX)
- Check 14,637 existing tests for duplicates
- Open a real browser and observe the SDP UI
- Run `javac` to compile Java code
- Execute a Selenium test and parse the report
- Fix broken locators by inspecting the live DOM

Each of these requires **different capabilities** — file I/O, vector search, browser automation, subprocess execution, LLM reasoning. An agentic pipeline chains specialized agents, each doing one thing well.

### The 10 Agents

#### Agent 1: Ingestion Agent
**Purpose:** Parse uploaded documents into structured text  
**LLM:** None (rule-based parsing)

```
Input:  Feature document (PDF / DOCX / XLSX / Markdown / TXT)
Output: Enriched feature description + suggested target modules
```

- Uses `PyPDF2` for PDFs, `python-docx` for DOCX, `openpyxl` for XLSX
- Extracts use-case tables, feature descriptions, test scenario lists
- If no document is uploaded (text-only), this is a no-op pass-through

---

#### Agent 2: Planner Agent
**Purpose:** Break a feature description into concrete test scenarios  
**LLM:** Ollama Call #1

```
Input:  "Create a new change request and link parent/child changes in the Associations tab"
Output: {
  "modules/changes/change": [
    { "description": "Verify association tab and attach options", "priority": "high" },
    { "description": "Attach parent change and verify association", "priority": "high" },
    { "description": "Detach parent change and verify reset", "priority": "medium" },
    ...
  ]
}
```

The Planner uses `config/module_taxonomy.yaml` (210 module paths) to map feature nouns to correct module locations.

---

#### Agent 3: Coverage Agent
**Purpose:** Prevent duplicate test generation  
**LLM:** None (ChromaDB vector search)

```
Input:  6 planned scenarios
Output: 4 new scenarios (2 duplicates skipped, already exist in codebase)
```

For each planned scenario, it:
1. Builds an enriched query: `"Module: modules/changes/change | Entity: change | Description: ..."`
2. Searches ChromaDB for top-5 similar existing tests
3. Classifies by similarity threshold (≥ 0.90 = duplicate)

---

#### Agent 4: UI Scout Agent
**Purpose:** Observe the real SDP UI before code generation  
**LLM:** Ollama Call #2 + #3 (or OpenRouter)

```
Input:  List of target modules to scout
Output: Live UI observations (DOM snapshot, field names, button labels, element states)
```

This agent uses **Playwright** to:
1. Open Chromium, navigate to the SDP instance
2. Login as admin
3. Navigate to each target module (e.g., Changes → Detail View → Associations tab)
4. Capture an **accessibility snapshot** of the page
5. Ask the LLM to annotate the snapshot with actionable observations

**Why this matters:** The real DOM might have changed since the last test was written. The Scout gives the Coder *fresh ground truth*.

---

#### Agent 5: Coder Agent
**Purpose:** Generate the actual Java test code  
**LLM:** Ollama Call #4 (or OpenRouter with ReAct tool-calling)

```
Input:  Scenario descriptions + RAG context + UI observations + framework rules
Output: Java code in two-piece format:
        // ===== ADD TO: ChangeBase.java =====
        public void verifyAssociationTab() { ... }

        // ===== ADD TO: Change.java =====
        @AutomaterScenario(id="CH_001", ...)
        public void verifyAssociationTab() { super.verifyAssociationTab(); }
```

The Coder's prompt includes:
- **3 similar existing tests** from ChromaDB (RAG context)
- **Framework rules** from `config/framework_rules.md`
- **Live UI observations** from the Scout
- **Learnings from previous failures** (if any exist in `logs/learnings.jsonl`)
- **Field configs and locator patterns** for the target module

On OpenRouter, the Coder uses **ReAct tool-calling** — it can read files (`read_file`), search code (`grep_search`), and list directories (`list_dir`) to gather additional context before generating.

---

#### Agent 6: Reviewer Agent
**Purpose:** Quality gate — catch errors before compilation  
**LLM:** Ollama Call #5

**Phase A — Static Checks (no LLM):**
- `@AutomaterScenario` annotation present with all required fields?
- Two-piece format followed (wrapper + base)?
- Import statements correct?
- Data key references valid?

**Phase B — Semantic Review (LLM):**
- Does the code correctly implement the described scenario?
- Are there logic errors or missing steps?
- Does it follow the framework conventions?

**Revision loop:** If issues found → routes back to Coder with fix instructions. Max 2 revisions.

---

#### Agent 7: Output Agent
**Purpose:** Write generated code to disk  
**LLM:** None (file I/O)

```
Output directory:
  generated/
    <timestamp>_<module>/
      ChangeBase_snippet.java
      Change_snippet.java
      summary.json
```

Also:
- Generates copy-paste instructions (which file to patch, which line to insert at)
- Indexes generated scenarios into ChromaDB for future duplicate detection

---

#### Agent 8: Runner Agent
**Purpose:** Compile and execute the generated test  
**LLM:** None (Java subprocess)

1. Patches `StandaloneDefault.java` with the test class and method name
2. Runs `javac` targeted compilation
3. Executes the test via `run_test.py`
4. Opens Firefox, navigates SDP, runs the full test lifecycle
5. Parses stdout for `$$Failure` / `"successfully"` / Java exceptions
6. Returns pass/fail with detailed log

---

#### Agent 9: Healer Agent
**Purpose:** Automatically fix failing tests  
**LLM:** Ollama Call #6 + #7

Only activates when RunnerAgent reports failure. Classification:

| Failure Type | How It Heals |
|-------------|-------------|
| **LOCATOR** | Opens Playwright, navigates to failing page, captures fresh DOM snapshot, asks LLM for correct XPath |
| **API** | Injects SDP API cheatsheet into prompt, asks LLM to fix the API call |
| **LOGIC** | Asks LLM to analyze the error and generate a code patch |
| **COMPILE** | Fixes syntax errors from the error output |

The Healer also **creates prerequisite test data** (via `SDPAPIHelper`) before debugging — it replays the `preProcess` API calls from the previous run's report.

---

#### Agent 10: Hg Agent
**Purpose:** Auto-commit generated code to Mercurial  
**LLM:** None (VCS operations)

When enabled (`HG_AGENT_ENABLED = True`):
- Creates a feature branch: `feature/AI_GEN_<scenario_id>`
- Commits all generated files with descriptive message
- Gated by configuration — currently disabled pending approval

---

### Agent Sizes

| Agent | Lines of Code | Has LLM? | Has Browser? |
|-------|--------------|-----------|-------------|
| Healer Agent | 1,079 | Yes | Yes (Playwright) |
| SDP API Helper | 1,065 | No | Yes (JS execution) |
| Coder Agent | 892 | Yes | No |
| Runner Agent | 850 | No | No (subprocess) |
| UI Scout Agent | 788 | Yes | Yes (Playwright) |
| Learning Agent | 658 | Yes | No |
| Ingestion Agent | 502 | No | No |
| Pipeline (orchestrator) | 320 | No | No |
| Hg Agent | 319 | No | No |
| Parallel Runner | 303 | No | No (subprocesses) |
| Output Agent | 273 | No | No |
| Reviewer Agent | 271 | Yes | No |
| Coder Tools | 220 | No | No |
| Coverage Agent | 159 | No | No |
| Planner Agent | 139 | Yes | No |
| LLM Factory | 102 | — | — |
| State | 67 | — | — |
| **Total** | **8,007** | | |

---

## 8. Web UI — The Interface

### Accessing the UI

```bash
# Start the server
./server.sh start

# Or manually
.venv/bin/python -m uvicorn web.server:app --port 9500
```

Open `http://localhost:9500` in any browser.

**Orchestrator Dashboard** (tracks Copilot-generated scenarios, test runs, healing events):
- Local: `http://localhost:9600`
- Hosted: `https://balajimuthukumaran-jlbdxduj-9600.zcodecorp.in`

### Features

| Feature | Description |
|---------|-------------|
| **Document upload** | Drag-and-drop PDF, DOCX, XLSX, TXT, Markdown files |
| **Text input** | Type or paste feature descriptions directly |
| **Module selector** | Pick target SDP modules from the taxonomy |
| **Live progress** | Real-time SSE streaming — see which agent is running |
| **Stage indicator** | Visual progress bar: Ingestion → Planner → Coverage → ... |
| **Generated files panel** | View generated Java code with syntax highlighting |
| **Run history** | Table of all past pipeline runs with status, duration, errors |
| **Stop button** | Cancel a running pipeline mid-execution |
| **System stats** | Live RAM/CPU usage in the header bar |
| **Browser notifications** | Get notified when generation completes (background tab) |
| **Clear history** | Wipe all past run records |

### API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/` | Serve the Web UI |
| `POST` | `/api/generate` | Start a pipeline run |
| `GET` | `/api/stream/{run_id}` | SSE event stream for live logs |
| `GET` | `/api/runs` | List all past runs |
| `GET` | `/api/runs/{run_id}` | Get detailed run info |
| `POST` | `/api/runs/{run_id}/stop` | Stop a running pipeline |
| `GET` | `/api/runs/{run_id}/file` | Download a generated file |
| `GET` | `/api/modules` | List available SDP modules |
| `GET` | `/api/stats` | System memory/CPU stats |
| `GET` | `/api/health` | Health check |
| `DELETE` | `/api/runs` | Clear run history |

---

## 9. Self-Healing with Playwright

### The Problem

Generated tests can fail due to:
- **Stale locators** — the UI changed since the last test was written (button moved, ID renamed)
- **API changes** — REST API endpoint or payload structure changed
- **Logic errors** — the LLM generated incorrect navigation steps

Traditionally, a developer would manually debug, inspect the DOM, and fix the code. This takes 30–60 minutes per failure.

### The Healer Agent Solution

```
Test fails
    │
    ▼
┌────────────────────────────┐
│ Classify failure type       │
│ (LOCATOR / API / LOGIC)     │
│ 🤖 LLM Call #6              │
└────────────┬───────────────┘
             │
     ┌───────┴────────┐
     ▼                ▼
 LOCATOR           API / LOGIC
     │                │
     ▼                ▼
┌──────────────┐  ┌──────────────┐
│ Open Playwright│ │ Inject API   │
│ browser       │  │ cheatsheet  │
│ Navigate to   │  │ 🤖 LLM Call │
│ failing page  │  │ Generate fix│
│ Capture DOM   │  └──────┬──────┘
│ 🤖 LLM: derive│         │
│ correct XPath │         │
└──────┬───────┘         │
       │                  │
       ▼                  ▼
┌────────────────────────────┐
│ Patch Java source           │
│ Recompile (javac)           │
│ Re-run test                 │
└────────────────────────────┘
```

### SDP API Helper

A 1,065-line support module that enables the Healer to **create prerequisite test data** (templates, topics, changes) via the browser's JavaScript API before debugging:

```javascript
// The Healer executes this in Playwright's browser context:
sdpAPICall('/api/v3/changes', 'post',
  'input_data=' + encodeURIComponent(JSON.stringify({change: {...}}))
).responseJSON
```

This ensures the UI state is correct when the Healer starts inspecting the DOM.

---

## 10. Parallel Execution & Learning Loop

### Parallel Runner Agent

For batch execution of multiple tests simultaneously:

```
tests_to_run.json          →     ParallelRunnerAgent
[                                 │
  { class: "Solution",            ├── JVM 1: Solution test (Firefox 1)
    method: "createSol..." },     ├── JVM 2: Request test (Firefox 2)
  { class: "Request",             │   (PARALLEL_WORKERS = 2)
    method: "createReq..." },     │
  ...                             ▼
]                                batch_run_results[]
```

### Learning Agent

After batch execution, the Learning Agent:
1. Analyzes failures → extracts DO/DON'T rules
2. Analyzes successes → extracts working patterns
3. Appends learnings to `config/framework_rules.md`
4. Persists to `logs/learnings.jsonl`
5. Future CoderAgent runs see these learnings in their prompt

```
Run batch → Analyze results → Extract learnings → Heal failures → Re-run → Repeat
                                                                     ↑        │
                                                                     └────────┘
                                                                  (up to 2 retries)
```

This creates a **continuous improvement loop** — the system gets smarter with every test it runs.

---

## 11. Real Results — Tests That Passed

### Solutions Module

| Test ID | Method | Status | What It Tests |
|---------|--------|--------|--------------|
| SDPOD_AUTO_SOL_DV_241 | `createAndShareApprovedPublicSolutionFromDV` | ✅ PASSED | Create approved public solution, share from detail view |
| SDPOD_AUTO_SOL_DV_242 | `createUnapprovedSolutionWithCustomTopicRevDateExpDate` | ✅ PASSED | Create unapproved solution with custom topic, review/expiry dates |

### Changes Module — CH-286 Linking Changes (6 tests)

| Test ID | Method | Status | What It Tests |
|---------|--------|--------|--------------|
| CH_001, CH_005 | `verifyAssociationTabAndAttachOptionsInLHS` | ✅ PASSED | Associations tab visibility, attach button dropdown |
| CH_006–CH_011 | `verifyAttachParentChangePopup` | ✅ PASSED | Parent change popup, filter dropdown, pagination, table settings |
| CH_012–CH_016 | `attachParentChangeAndVerifyAssociation` | ✅ PASSED | Attach parent change, verify association displays correctly |
| CH_017 | `detachParentChangeAndVerifyReset` | ✅ PASSED | Detach parent change, verify section resets |
| CH_018–CH_019 | `verifyAttachChildChangePopup` | ✅ PASSED | Child changes popup, checkbox selection, Associate/Cancel buttons |
| CH_002–CH_004 | `attachDetachChildChangesAndVerifyListView` | ✅ PASSED | Attach/detach child changes, verify in list view |

### Problem/Triggers Module

| Test ID | Method | Status |
|---------|--------|--------|
| SDPOD_AUTO_PROB_TRIG_NEW_001 | `createProblemTriggerAndVerify` | ✅ PASSED |

---

## 12. Day-by-Day Build Timeline

### Day 1 — February 24 (Monday)
**Foundation Day**

- Started with the raw AutomaterSelenium framework — no AI layer existed
- Built the core agent architecture: `state.py`, `pipeline.py`, `llm_factory.py`
- Created `PlannerAgent`, `CoderAgent`, `ReviewerAgent`, `OutputAgent`, `RunnerAgent`
- Wired the LangGraph pipeline: Planner → Coverage → Coder → Reviewer → Output → Runner
- First test: `SDPOD_AUTO_SOL_DV_241` — `createAndShareApprovedPublicSolutionFromDV`
- Debugged `runner_agent.py` `_parse_success()` logic for correct pass/fail detection
- Fixed `SHARE_SOL_POPUP_SUBMIT` locator and `SOLUTIONS_SHARED_MSG` constant
- **Result: First AI-generated test PASSING** ✅

### Day 2 — February 25 (Tuesday)
**Self-Healing Day**

- Fixed `SDPOD_AUTO_SOL_DV_242` (unapproved solution) — discovered boolean field skip bug
- Built the **HealerAgent** (1,079 lines) with Playwright integration
- Healer classifies failures → opens browser → captures DOM → derives fix
- Created GitHub repository, pushed initial 41 files
- Created `.github/copilot-instructions.md` — comprehensive framework knowledge base
- Added `USE_PIPELINE` toggle to `run_test.py`
- **Result: Self-healing pipeline operational** ✅

### Day 3 — February 26 (Wednesday)
**Knowledge Base Day**

- Switched active project from `AutomaterSelenium` to `SDPLIVE_LATEST_AUTOMATER_SELENIUM`
- Reindexed ChromaDB: **210 modules, 17,101 scenarios, 14,637 vectors**
- Built `CoverageAgent` with ChromaDB vector search for duplicate detection
- Audited scenario IDs: found 1,461 duplicates + 1,372 empty IDs
- Fixed module placement rules in copilot-instructions.md
- **Result: Knowledge base fully populated** ✅

### Day 4 — February 27 (Thursday)
**Mega Build Day — 16 commits**

- **Phase 1:** Built `IngestionAgent` (PDF/DOCX/XLSX/PPTX/TXT parsing) — 502 lines
- **Phase 2:** Built Web UI (FastAPI + SSE + drag-drop) — 589 lines server + HTML
- **Phase 3:** Built `HgAgent` for Mercurial auto-commit — 319 lines
- **Phase 5:** Built Pipeline Monitoring (run history, stage progress, browser notifications)
- **Phase 8:** Built `ParallelRunnerAgent` + `LearningAgent` (961 lines combined)
- Fixed framework compilation: `setup_framework_bin.sh` for local report generation
- Fixed `Annotated[list, operator.add]` exponential duplication bug
- Built `pipeline-flow.md` documentation (394 lines)
- Added `server.sh` start/stop script
- **Result: Full Web UI + monitoring + parallel execution operational** ✅

### Day 5 — March 2 (Sunday)
**Hardening Day**

- Added Docker support (Dockerfile + docker-compose + entrypoint)
- Replaced all hardcoded paths with environment variables for portability
- Registered 3 new entity types
- Fixed test timeout: 300s → configurable `TEST_EXECUTION_TIMEOUT` (default 1800s)
- Built Phase 0.8: runner watchdog + preProcess refactor
- Added **ReAct tool-calling** to CoderAgent (read_file, grep_search, list_dir on OpenRouter)
- Switched to `gpt-4o-mini` on OpenRouter (4× cheaper)
- Fixed infinite revision loop (increment revision_count properly)
- **Result: Production-hardened, portable, Docker-ready** ✅

### Day 6–7 — March 2–3 (Sunday–Monday)
**CH-286 Feature Testing**

- Generated 6 test methods for CH-286 Linking Changes feature
- Built new locator interfaces: `LinkingChange`, `LinkingChangePopup`
- Created `ChangeAPIUtil` enhancements for linking operations
- Fixed Select2 dropdown filter handling
- Fixed dialog text assertion, child-section locators
- All 6 tests passing → committed as `5ec05c7`
- **Result: Complete feature test suite generated and validated** ✅

### Day 8 — March 3 (Monday)
**Polish & Documentation Day**

- Built `SDPAPIHelper` (1,065 lines) — enables Playwright agents to create prerequisite data
- Fixed POST response parsing (div-depth-counting for nested HTML)
- Integrated SDPAPIHelper into HealerAgent and UIScoutAgent
- Fixed ChromaDB re-indexing gap — generated scenarios now auto-indexed (prevents duplicate generation)
- Enhanced CoverageAgent query format + threshold tuning (0.92 → 0.90)
- Created this demo documentation
- **Result: All features complete, documented, ready for demo** ✅

---

## 13. Project Statistics

### Codebase

| Metric | Value |
|--------|-------|
| Python source files | 52 |
| Agent files | 17 |
| Total Python LoC | 12,194 |
| Agent LoC (core) | 8,007 |
| Config/docs/templates | 4,187 |
| Git commits | 36 |
| Development days | 8 |

### Knowledge Base

| Metric | Value |
|--------|-------|
| Java files parsed | 1,426 |
| Scenarios indexed | 14,637 vectors |
| Total scenarios in source | 17,101 |
| Modules covered | 210 |
| Source code chunks | 8,722 |
| Help topic vectors | 920 |
| Embedding model | `all-MiniLM-L6-v2` |
| Vector dimensions | 384 |
| Similarity metric | Cosine |

### LLM Usage

| Metric | Value |
|--------|-------|
| Local model | `qwen2.5-coder:7b` (Ollama) |
| Cloud model | `gpt-4o-mini` (OpenRouter) |
| RAM for local model | 4.3 GiB |
| Max LLM calls per run | 7 |
| Min LLM calls (happy path) | 3 |
| Average pipeline runtime | 15–25 minutes (local CPU) |

### Tests

| Metric | Value |
|--------|-------|
| Tests generated & passing | 8+ |
| Modules tested | Solutions, Changes, Requests, Problems |
| Feature suites generated | 2 (Sol detail view, CH-286 linking) |

---

## 14. How to Run — Quick Start

### Prerequisites

```bash
# Python 3.10+
python --version

# Java 8+ (for compiling AutomaterSelenium)
javac -version

# Ollama (optional — for local LLM)
ollama --version
ollama pull qwen2.5-coder:7b
```

### Setup

```bash
cd /home/balaji-12086/Desktop/Workspace/Zide/ai-automation-qa

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (for UI Scout + Healer)
playwright install chromium

# Build the knowledge base (one-time)
python main.py setup
```

### Run via Web UI

```bash
# Start the server
./server.sh start

# Open browser
http://localhost:9500

# Paste a feature description → click Generate
```

### Run via CLI

```bash
# Generate tests from a feature description
python main.py generate --feature "Create an incident request and add notes to it"

# Generate from a document
python main.py generate --doc docs/Feature_Document/my_feature.pdf

# Search the knowledge base
python main.py search "create solution with custom template" --top-k 5
```

### Run a Single Test Directly

```python
# Edit run_test.py
RUN_CONFIG = {
    "entity_class":  "Solution",
    "method_name":   "createAndShareApprovedPublicSolutionFromDV",
    "skip_compile":  True,
}

# Execute
.venv/bin/python run_test.py
```

---

## 15. What's Next — Roadmap

| Phase | Description | Status |
|-------|-------------|--------|
| 0 — Foundation | Core pipeline: Planner → Coder → Reviewer → Runner | ✅ Done |
| 0.5 — Self-Healing | Playwright-powered HealerAgent | ✅ Done |
| 0.6 — SDPLIVE Sync | Switch to production project, reindex 210 modules | ✅ Done |
| 0.8 — Local Run Infra | Framework compilation, report generation | ✅ Done |
| 1 — Document Ingestion | PDF/DOCX/XLSX/PPTX/TXT parsing | ✅ Done |
| 2 — Web UI | FastAPI + SSE streaming + live progress | ✅ Done |
| 3 — Hg Integration | Auto-branch + commit (gated) | ✅ Done |
| 4 — Live Test Run | End-to-end generation via Web UI | ✅ Done |
| 5 — Pipeline Monitoring | Run history, stage progress, stats | ✅ Done |
| 8 — Parallel Execution | Batch runner + learning loop | ✅ Done |
| **4.5 — Run-Once Validation** | One-click test validation + copy-paste panel in UI | 🔲 Next |
| **6 — Multi-Entity Scale** | All 10+ entities, regression suite generation | 🔲 Planned |
| **7 — Feedback Loop** | Learn from failures, human approval queue | 🔲 Planned |

### Team-Level Adoption Plan

1. **Share this document + live demo** with the team
2. **Each developer gets access** to the Web UI (port 9500)
3. **Start with new features** — when a new feature is assigned, feed the doc to the AI
4. **Review generated code** — developer inspects, approves, merges
5. **Self-healing handles regressions** — existing tests break? Healer patches them
6. **Learning loop improves quality** — every run makes future generation better
7. **Scale to all modules** — currently Solutions/Changes/Requests/Problems → expand to all 210

---

## Appendix A: Agentic Pipeline Architecture (Detailed)

### Why an Agentic Pipeline?

Traditional automation test generation approaches:
- **Template-based:** Rigid, can't handle novel scenarios
- **Record-and-playback:** Fragile, breaks on UI changes
- **Single LLM call:** No context, no validation, no execution

An agentic pipeline overcomes all three:

| Challenge | How Agents Solve It |
|-----------|-------------------|
| LLM doesn't know our framework | **RAG** — ChromaDB provides real examples from 14,637 existing tests |
| LLM might generate wrong code | **Reviewer Agent** — catches errors before compilation |
| Generated code might not compile | **Runner Agent** — actually compiles and runs it |
| Test might fail due to stale locators | **Healer Agent** — opens browser, finds correct locator, patches |
| Same test might be generated twice | **Coverage Agent** — deduplicates against knowledge base |
| UI might have changed since last test | **UI Scout Agent** — captures live DOM snapshot |
| Need to handle documents, not just text | **Ingestion Agent** — parses PDF/DOCX/XLSX |
| Need version control | **Hg Agent** — auto-commits on success |

### Pipeline Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                                                                         │
│  USER INPUT: Feature description + optional document upload             │
│                                                                         │
└────────────────────────────────┬────────────────────────────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   1. INGESTION AGENT    │  Parse uploaded doc
                    │   (No LLM)             │  PDF → structured text
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   2. PLANNER AGENT      │  Feature → test scenarios
                    │   🤖 LLM Call #1        │  Map to module paths
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   3. COVERAGE AGENT     │  Deduplicate against
                    │   (ChromaDB search)     │  14,637 existing tests
                    └────────────┬───────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   4. UI SCOUT AGENT     │  Open real SDP browser
                    │   🤖 LLM #2 + #3       │  Capture live DOM state
                    │   🌐 Playwright          │
                    └────────────┬───────────┘
                                 │
                                 ▼
               ┌─────────────────────────────────────┐
               │                                     │
               │   5. CODER AGENT                    │
               │   🤖 LLM Call #4                     │
               │                                     │
               │   Prompt includes:                  │
               │   ├── 3 similar tests (RAG)         │
               │   ├── Framework rules               │
               │   ├── Live UI observations          │
               │   ├── Learnings from past runs      │
               │   └── Field configs + locators      │
               │                                     │
               │   Output: Java @AutomaterScenario   │
               │   code in two-piece format          │
               │                                     │
               └─────────────────┬───────────────────┘
                                 │
                                 ▼
                    ┌────────────────────────┐
                    │   6. REVIEWER AGENT     │  Static + semantic review
                    │   🤖 LLM Call #5        │
                    │                        │
                    │   Issues found?         │
                    │   ├── YES → back to     │──────┐
                    │   │   Coder (max 2×)    │      │
                    │   └── NO → continue     │      │
                    └────────────┬───────────┘      │
                                 │                   │
                          (revision loop)            │
                                 │◄──────────────────┘
                                 ▼
                    ┌────────────────────────┐
                    │   7. OUTPUT AGENT       │  Write .java snippets
                    │   (File I/O)            │  Index into ChromaDB
                    └────────────┬───────────┘
                                 │
                    ┌────────────┴───────────┐
                    │  Run config provided?   │
                    │  YES              NO    │
                    └───┬────────────────┬───┘
                        │                │
                        ▼                │
           ┌────────────────────────┐    │
           │   8. RUNNER AGENT       │   │
           │   ☕ javac + Java exec  │    │
           │                        │    │
           │   PASSED?              │    │
           │   ├── YES ──────────── │ ───┤
           │   └── NO               │    │
           └────────────┬───────────┘    │
                        │                │
                        ▼                │
           ┌────────────────────────┐    │
           │   9. HEALER AGENT       │   │
           │   🤖 LLM #6 + #7       │    │
           │   🌐 Playwright          │   │
           │                        │    │
           │   Classify → Fix →     │    │
           │   Patch → Recompile →  │    │
           │   Re-run               │    │
           └────────────┬───────────┘    │
                        │                │
                        ▼                ▼
                    ┌────────────────────────┐
                    │   10. HG AGENT          │  Auto-commit to
                    │   (Mercurial, gated)    │  feature branch
                    └────────────┬───────────┘
                                 │
                                 ▼
                          ✅ DONE
                    Files shown in Web UI
                    with copy-paste panel
```

### Shared State Between Agents

All agents read from and write to a single `AgentState` dictionary — LangGraph manages the state transitions:

```python
AgentState = {
    # Input
    "feature_description": str,
    "target_modules": list[str],
    "source_document": str,

    # Pipeline data flow
    "test_plan":          dict,    # Planner → Coverage/Coder
    "coverage_gaps":      list,    # Coverage → Coder
    "ui_observations":    dict,    # Scout → Coder
    "generated_code":     list,    # Coder → Reviewer → Output
    "review_results":     list,    # Reviewer output
    "revision_requests":  list,    # Reviewer → Coder (loop)
    "final_output_paths": list,    # Output → Web UI
    "run_result":         dict,    # Runner → Healer
    "heal_result":        dict,    # Healer output
    "hg_result":          dict,    # Hg output

    # Control flow
    "messages":           list,    # Accumulated log (streamed to UI via SSE)
    "errors":             list,    # Accumulated errors
    "revision_count":     int,     # Tracks Coder ↔ Reviewer loops
    "learnings":          list,    # Past failure learnings injected into prompts
}
```

### LLM Call Summary

| # | Agent | Purpose | When Skipped |
|---|-------|---------|-------------|
| 1 | Planner | Feature → JSON test plan | Never |
| 2 | UI Scout | Infer navigation plan | Module has pre-built plan |
| 3 | UI Scout | DOM snapshot → observations | Playwright fails |
| 4 | Coder | Generate Java code | test_plan is empty |
| 5 | Reviewer | Semantic code review | generated_code is empty |
| 6 | Healer | Classify failure type | Test passed |
| 7 | Healer | Derive fix from DOM/error | Test passed |

**Maximum LLM calls per run: 7 | Minimum (happy path): 3**

### Why Each Agent Exists

```
Without Ingestion Agent  → Can only handle plain text, not documents
Without Planner Agent    → No structured test plan, LLM guesses wildly
Without Coverage Agent   → Generates duplicate tests that already exist
Without UI Scout Agent   → Code uses outdated locators that fail immediately
Without Coder Agent      → No code generation (obviously)
Without Reviewer Agent   → Bad code reaches compilation, wastes time
Without Output Agent     → Code lives only in memory, not on disk
Without Runner Agent     → Never know if code actually works
Without Healer Agent     → Every failure requires manual developer intervention
Without Hg Agent         → No version control for generated tests
```

**Remove any single agent, and the pipeline degrades significantly.** That's why it's agentic — each agent is a specialist that handles one concern, composed together for an end-to-end autonomous workflow.

---

*"Generate the Automation cases for the features without manual intervention"*  
— Balaji M, February 2026

---

**End of Document**
