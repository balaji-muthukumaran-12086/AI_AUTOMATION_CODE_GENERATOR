# 🚀 AI Test Automation Orchestrator — Overall Vision

**Author**: Balaji  
**Captured**: February 25, 2026  
**Status**: Phase-wise execution in progress

---

## 🎯 The Ultimate Goal

> **Generate automation test cases for software features without any manual intervention.**

The system takes a feature document / help document / use-case sheet as input and autonomously produces production-ready Java Selenium test cases that can be appended to the codebase, compiled, and pushed to production — all bug-free.

---

## 🗺️ Architecture Vision (High Level)

```
┌──────────────────────────────────────────────────────────────────────────┐
│                        AI Orchestrator Platform (Web UI)                 │
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
└──────────────────────────────────────────────────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────────────────────────────────────────┐
│                         Agent Pipeline (LangGraph)                       │
│                                                                          │
│   Document         Planner        Coverage       Coder                  │
│   Ingestion   →    Agent     →    Agent     →    Agent                  │
│   Agent            (parse          (gap           (generate              │
│   (PDF/DOCX/       use-cases       analysis)      Java code)             │
│    XLSX/TXT        → scenarios)                                          │
│    → structured)        │                              │                 │
│                         │                         Reviewer               │
│                         │                         Agent                  │
│                         │                         (validate)             │
│                         │                              │                 │
│                         │                         Output                 │
│                         │                         Agent                  │
│                         │                         (write files)          │
│                         │                              │                 │
│                         │                         Runner                 │
│                         │                         Agent                  │
│                         │                         (compile + run)        │
│                         │                              │                 │
│                         │                    FAILED    │    PASSED        │
│                         │                       ↓      │      ↓          │
│                         │                    Healer    │    → UI shows   │
│                         │                    Agent     │      ✅ result   │
│                         │                    (Playwright                 │
│                         │                     self-heal)                 │
│                         │                         │                      │
│                         └─────────────────────────┘                      │
│                                     ↓                                    │
│                         UI responds with:                                │
│                         - File names changed                             │
│                         - Code snippets generated                        │
│                         - Test pass/fail result                          │
│                         - Diff ready to push                             │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 Phase-wise Execution Plan

### ✅ Phase 0 — Foundation (COMPLETED)
- LangGraph pipeline: Planner → Coverage → Coder → Reviewer → Output → Runner
- RunnerAgent: compile + execute AutomaterSelenium test cases
- Knowledge base (ChromaDB vector store) seeded with existing test cases
- LLM factory (Ollama local / OpenAI)
- First AI-generated test case: `SDPOD_AUTO_SOL_DV_241` — PASSING

### ✅ Phase 0.5 — Self-Healing (COMPLETED — Feb 25, 2026)
- HealerAgent (`agents/healer_agent.py`) — Playwright-powered
  - Classifies failure: LOCATOR | API | LOGIC | COMPILE
  - Opens browser, navigates to failing UI state
  - Captures accessibility snapshot
  - LLM derives correct locator / code fix
  - Patches Java source, recompiles, reruns
  - Wired into pipeline: runner FAILED → healer → END
- Chromium installed at `~/.cache/ms-playwright/`

### 🔲 Phase 1 — Document Ingestion Agent (NEXT)
**Goal**: Accept raw documents (PDF, DOCX, XLSX, TXT, Markdown) and convert them into structured use-case objects that the Planner Agent can consume.

Key tasks:
- `agents/ingestion_agent.py` — reads uploaded file, extracts use-cases
- Support formats: `.pdf`, `.docx`, `.xlsx`, `.md`, `.txt`
- Output: structured JSON `[{ "entity": "Solution", "feature": "...", "scenarios": [...] }]`
- Integrate with existing `ingestion/` folder (already exists in workspace)
- Feed output directly into `AgentState.feature_description` + `target_modules`

### 🔲 Phase 2 — Web UI (React / Next.js or simple FastAPI + HTML)
**Goal**: A browser-based interface where users upload documents and see results.

Key tasks:
- File upload area (drag & drop)
- Entity selector (Solutions, Requests, Problems, etc.)
- Live streaming pipeline progress (SSE or WebSocket)
- Output panel showing:
  - File name + code snippet of each generated case
  - Pass/Fail badge from RunnerAgent
  - Healer activity log if triggered
  - Git diff preview
  - "Copy to clipboard" + "Download patch" buttons
- Backend: FastAPI wrapping the LangGraph pipeline

### 🔲 Phase 3 — Git Integration
**Goal**: One-click push to production branch.

Key tasks:
- Auto-create a feature branch: `auto/SDPOD_AUTO_SOL_DV_XXX`
- Commit generated files with descriptive message
- Open PR / push to review queue
- Integrate with GitLab / GitHub CI to auto-run test on push

### 🔲 Phase 4 — Multi-Entity & Regression Suite
**Goal**: Handle all 10+ entities (Request, Problem, Change, Release, Asset, Project...) and generate a full regression suite from a single feature spec.

Key tasks:
- Cross-entity scenario detection
- Coverage matrix: which entities are affected by a feature change
- Batch generation: one document → 10+ test cases across entities
- Regression gap analysis: compare existing suite vs new feature spec

### 🔲 Phase 5 — Feedback Loop & Auto-Improvement
**Goal**: Learn from test failures and human reviews to improve generation quality.

Key tasks:
- Store reviewer feedback in vector store
- Failed healer attempts → log as "known hard cases" for future training
- Human approval queue: reviewer can approve/reject generated cases from UI
- Approved cases automatically update the knowledge base

---

## 🏗️ Current Project Structure

```
ai-automation-qa/
├── agents/
│   ├── pipeline.py          ← LangGraph graph (all agents wired)
│   ├── planner_agent.py     ← Breaks feature description → test scenarios
│   ├── coverage_agent.py    ← Gap analysis against existing tests
│   ├── coder_agent.py       ← Generates Java test code (LLM)
│   ├── reviewer_agent.py    ← Reviews generated code quality
│   ├── output_agent.py      ← Writes code to .java files
│   ├── runner_agent.py      ← Compiles + runs tests
│   ├── healer_agent.py      ← ✅ NEW: Playwright self-healing
│   ├── state.py             ← Shared LangGraph state
│   └── llm_factory.py       ← Ollama / OpenAI factory
├── knowledge_base/          ← ChromaDB vector store
├── ingestion/               ← (to be expanded in Phase 1)
├── AutomaterSelenium/       ← Java Selenium test framework
│   └── src/...modules/      ← Entity-specific test classes
├── config/
├── My Memory/               ← Session memory files
│   ├── 2026-02-24.md        ← Yesterday's session notes
│   └── vision.md            ← THIS FILE
├── run_test.py              ← Quick CLI test runner
└── main.py                  ← Pipeline entry point
```

---

## 🧠 Key Design Principles

1. **Zero manual intervention** — from document upload to test running, no human in the loop
2. **Self-healing** — when tests break, the healer fixes them automatically
3. **Modular agents** — each agent does ONE thing well, wired together with LangGraph
4. **Knowledge-driven** — ChromaDB stores all existing tests; new generation is always gap-aware
5. **Framework-native** — generated code follows AutomaterSelenium conventions exactly
6. **UI-first delivery** — developers see exactly what was generated and can inspect before pushing

---

## 💡 Notes for Continuation

- The LLM currently runs on **local Ollama** (`qwen2.5-coder:7b`) — upgrade to `gpt-4o` for better generation quality when ready
- `ingestion/` folder already exists — likely has some initial scaffolding to build on
- Phase 1 (Ingestion Agent) is the **next immediate priority**
- The HealerAgent's `headless=True` can be flipped to `False` to watch it surf the app live during debugging

---

*"Generate the Automation cases for the features without manual intervention"*  
— Balaji's Vision, February 25, 2026
