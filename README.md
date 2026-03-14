<div align="center">

# AI Automation Code Generator

**Generate production-ready Selenium test cases from natural language — fully autonomous, two approaches, one goal.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Java 8+](https://img.shields.io/badge/java-8+-orange.svg)](https://www.oracle.com/java/)
[![LangGraph](https://img.shields.io/badge/orchestration-LangGraph-purple.svg)](https://github.com/langchain-ai/langgraph)
[![Claude Opus](https://img.shields.io/badge/LLM-Claude%20Opus%204.6-blueviolet.svg)](https://www.anthropic.com/)
[![Docker](https://img.shields.io/badge/docker-supported-2496ED.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

[Features](#-features) · [Two Approaches](#-two-approaches) · [Architecture](#-architecture) · [Quick Start](#-quick-start) · [Usage](#-usage) · [Documentation](#-documentation)

</div>

---

## Overview

AI Automation Code Generator transforms **feature descriptions or documents** into **working, framework-compliant Java Selenium test cases** — without manual intervention.

It provides **two distinct approaches** to AI-powered test generation:

| | **Approach 1: Agentic Pipeline** | **Approach 2: VS Code Agents** |
|---|---|---|
| **How** | Fully automated end-to-end LangGraph pipeline | Interactive agents inside VS Code with Claude Opus |
| **Input** | Feature documents (PDF/DOCX/XLSX) or CLI text | Natural language chat or use-case CSVs |
| **Autonomy** | Hands-free — upload and walk away | Conversational — guide or let agents autopilot |
| **LLM** | Ollama (local) or OpenRouter (cloud) | Claude Opus 4.6 / Claude Sonnet 4 via GitHub Copilot |
| **Best for** | Batch generation, CI/CD integration | Iterative development, debugging, learning |

Both approaches generate code that compiles, runs against a live SDP instance, and self-heals on failure.

Built for the [ServiceDesk Plus](https://www.manageengine.com/products/service-desk/) QA automation framework (`AutomaterSelenium`), but the architecture is adaptable to any Selenium-based test framework.

---

## 🎯 Features

- **Document Ingestion** — Parse PDF, DOCX, XLSX, PPTX, Markdown, and plain text feature documents
- **Intelligent Planning** — LLM breaks features into concrete test scenarios mapped to correct modules
- **Duplicate Detection** — ChromaDB vector search against 14,637 indexed scenarios prevents redundant generation
- **Live UI Observation** — Playwright captures real DOM snapshots before code generation for accurate locators
- **Convention-Compliant Code** — RAG-powered generation follows exact `AutomaterSelenium` framework patterns
- **Automated Review** — Static + semantic code review with revision loop
- **Compile & Execute** — Generated tests are compiled with `javac` and run against a live SDP instance
- **Self-Healing** — Failed tests are auto-debugged via Playwright DOM inspection and LLM-driven patching
- **Learning Loop** — Extracts DO/DON'T rules from failures; future runs get smarter
- **Web UI** — Real-time progress via SSE streaming, document upload, and run history
- **Parallel Execution** — Batch runner launches multiple JVMs concurrently
- **Version Control** — Optional Mercurial auto-branch and commit on test pass

---

## 🔀 Two Approaches

### Approach 1: Agentic Pipeline (End-to-End Automation)

A fully autonomous **LangGraph-orchestrated pipeline** that takes a feature document as input and produces passing test code as output — no human in the loop.

```
📄 Feature Document
        │
        ▼
  ┌─────────────────────────────────────────────────────────────────┐
  │  Ingestion → Planner → Coverage → UI Scout → Coder → Reviewer  │
  │                                                       │         │
  │               Output ← Runner ← Healer ←─────────────┘         │
  │                 │                  ↑                             │
  │                 │           (self-heal loop)                     │
  │                 ▼                                                │
  │            Hg Agent (auto-commit)                                │
  └─────────────────────────────────────────────────────────────────┘
        │
        ▼
  ✅ Passing Java Test Code
```

**10 specialized agents** form a DAG, each handling a single concern:

| # | Agent | Purpose | Key Technology |
|---|-------|---------|----------------|
| 1 | **Ingestion** | Parse uploaded documents (PDF/DOCX/XLSX/TXT) | PyMuPDF, python-docx |
| 2 | **Planner** | Break features into test scenarios | LLM |
| 3 | **Coverage** | Deduplicate against 14,637 existing tests | ChromaDB |
| 4 | **UI Scout** | Capture live DOM snapshots for accurate locators | Playwright + LLM |
| 5 | **Coder** | Generate Java test code with RAG context | LLM + ChromaDB |
| 6 | **Reviewer** | Static + semantic code review | LLM |
| 7 | **Output** | Write files to disk, update knowledge base | File I/O |
| 8 | **Runner** | Compile (`javac`) and execute tests | Java subprocess |
| 9 | **Healer** | Self-heal failing tests via DOM inspection | Playwright + LLM |
| 10 | **Hg** | Auto-commit passing tests to Mercurial | hg CLI |

**Supporting modules:**

| Module | Purpose |
|--------|---------|
| SDP API Helper | Create prerequisite test data via browser JS API |
| Learning Agent | Extract DO/DON'T rules from batch execution results |
| Parallel Runner | Concurrent multi-JVM test execution |
| LLM Factory | Unified Ollama / OpenRouter / OpenAI abstraction |

**Run it via:**
```bash
# Web UI
./server.sh start              # → http://localhost:9500

# CLI
python3 main.py generate --feature "Create a change and verify the detail view"
python3 main.py generate --doc path/to/feature.pdf

# Docker
docker-compose up --build      # → http://localhost:9500
```

---

### Approach 2: VS Code Agents (Interactive + Claude Opus)

Four purpose-built **VS Code agent modes** powered by **Claude Opus 4.6** via GitHub Copilot, designed for interactive test development directly inside the editor.

```
Developer in VS Code
        │
        ├── @setup-project    → Clone repo, configure environment, pick owner
        ├── @test-generator   → Generate tests from CSV or description (autopilot)
        ├── @test-runner      → Compile → Run → Diagnose → Fix → Re-run (autonomous loop)
        └── @test-debugger    → Playwright-driven DOM inspection & locator fixes
```

| Agent | Mode | Description |
|-------|------|-------------|
| **`@setup-project`** | Interactive | Clone Mercurial branch, configure `.env`, compile framework, select owner |
| **`@test-generator`** | Autopilot (30 turns) | Reads use-case CSVs or plain-text descriptions; generates all Java files, data JSONs, and constants |
| **`@test-runner`** | Autopilot (40 turns) | Compiles and runs tests; on failure, opens Playwright browser, inspects live DOM, patches code, recompiles, re-runs |
| **`@test-debugger`** | Autopilot (20 turns) | Deep failure analysis — reads `ScenarioReport.html`, uses Playwright to inspect UI state, fixes broken locators |

**Key capabilities of the VS Code approach:**

- **Conversational** — Ask the agent to generate a specific scenario, explain a failure, or refactor existing code
- **Playwright MCP integration** — Agents can launch a real browser, navigate SDP pages, take DOM snapshots, and create prerequisite data via `sdpAPICall()` — all from within VS Code
- **Deep framework knowledge** — 2,000+ lines of codified framework rules in `.github/copilot-instructions.md`, with auto-loaded instruction files for Java and JSON conventions
- **Autopilot mode** — Agents iterate autonomously (up to 40 turns) through generate → compile → run → diagnose → fix → re-run cycles
- **Use-case CSV intake** — Upload a spreadsheet of manual test cases; the generator maps each row to the correct module, entity, and annotation pattern

**Run it via:**
```
1. Open the project in VS Code with GitHub Copilot enabled
2. In Copilot Chat, type:  @test-generator create a change and verify the detail view
3. Or:                      @test-runner ChangeDetailsView.verifyDetailViewTitle
4. Or:                      @test-debugger SDPOD_AUTO_CH_LV_001 fails with NoSuchElementException
```

---

### When to Use Which

| Scenario | Recommended Approach |
|----------|---------------------|
| Generating tests from a large feature document | **Agentic Pipeline** — batch processing, no manual steps |
| Generating a handful of scenarios from a CSV | **VS Code `@test-generator`** — interactive, iterative |
| Running and debugging a specific failing test | **VS Code `@test-runner`** — Playwright-driven self-healing |
| Exploring the codebase or understanding framework conventions | **VS Code `@test-debugger`** or plain Copilot Chat |
| CI/CD integration or headless environments | **Agentic Pipeline** — CLI/Docker, no IDE required |
| New team member onboarding | **VS Code `@setup-project`** — guided interactive setup |

---

## 🏗 Architecture

### High-Level System Design

```
┌───────────────────────────────────────────────────────────────────────────┐
│                        AI Automation Code Generator                       │
│                                                                           │
│  ┌─────────────────────────────┐   ┌─────────────────────────────────┐   │
│  │   APPROACH 1: Pipeline      │   │   APPROACH 2: VS Code Agents    │   │
│  │                             │   │                                 │   │
│  │  LangGraph DAG              │   │  GitHub Copilot + Claude Opus   │   │
│  │  ┌────┐ ┌────┐ ┌────┐     │   │  ┌──────────┐ ┌──────────┐     │   │
│  │  │Ing.│→│Plan│→│Cov.│→... │   │  │@generator│ │@runner   │     │   │
│  │  └────┘ └────┘ └────┘     │   │  └──────────┘ └──────────┘     │   │
│  │  Ollama / OpenRouter       │   │  ┌──────────┐ ┌──────────┐     │   │
│  │  FastAPI Web UI             │   │  │@debugger │ │@setup    │     │   │
│  │  Docker-ready               │   │  └──────────┘ └──────────┘     │   │
│  └──────────────┬──────────────┘   └──────────────┬──────────────────┘   │
│                 │                                  │                      │
│                 └──────────┬───────────────────────┘                      │
│                            ▼                                              │
│               ┌────────────────────────┐                                  │
│               │    Shared Foundation    │                                  │
│               │                        │                                  │
│               │  • ChromaDB (14,637    │                                  │
│               │    indexed scenarios)  │                                  │
│               │  • Playwright MCP      │                                  │
│               │  • Java Compiler       │                                  │
│               │  • Framework Rules     │                                  │
│               │  • SDP API Helper      │                                  │
│               └────────────────────────┘                                  │
│                            ▼                                              │
│               ┌────────────────────────┐                                  │
│               │  AutomaterSelenium     │                                  │
│               │  Framework (Java)      │                                  │
│               │  17,101 scenarios      │                                  │
│               │  210 modules           │                                  │
│               └────────────────────────┘                                  │
└───────────────────────────────────────────────────────────────────────────┘
```

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Pipeline Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) (DAG-based agent routing) |
| VS Code Integration | [GitHub Copilot](https://github.com/features/copilot) Agent Mode + Custom Agents |
| LLM (Pipeline — local) | [Ollama](https://ollama.ai/) — `qwen2.5-coder:7b` |
| LLM (Pipeline — cloud) | [OpenRouter](https://openrouter.ai/) — `gpt-4o-mini` / `gpt-4o` |
| LLM (VS Code Agents) | Claude Opus 4.6 / Claude Sonnet 4 via GitHub Copilot |
| Vector DB | [ChromaDB](https://www.trychroma.com/) — `all-MiniLM-L6-v2` embeddings |
| Browser Automation | [Playwright](https://playwright.dev/) (Chromium) via MCP |
| Test Framework | Java Selenium (`AutomaterSelenium`) |
| Web Server | [FastAPI](https://fastapi.tiangolo.com/) + SSE |
| Containerization | Docker + docker-compose |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Java 8+ (for `javac` compilation)
- [Ollama](https://ollama.ai/) (optional — for local LLM in pipeline mode)
- [VS Code](https://code.visualstudio.com/) + [GitHub Copilot](https://github.com/features/copilot) (for agent mode)

### Installation

```bash
# Clone the repository
git clone https://github.com/balaji-muthukumaran-12086/AI_AUTOMATION_CODE_GENERATOR.git
cd AI_AUTOMATION_CODE_GENERATOR

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers
playwright install chromium
```

### Environment Setup

```bash
# Copy and configure environment variables
cp .env.example .env
# Edit .env with your SDP instance URL, credentials, and API keys
```

### Build Knowledge Base (one-time)

```bash
# Index all existing test scenarios into ChromaDB
python3 main.py ingest
python3 main.py index
```

### Compile Framework (one-time)

```bash
# Build framework classes into bin/
./setup_framework_bin.sh
```

---

## 📖 Usage

### Approach 1: Agentic Pipeline

#### Web UI (Recommended)

```bash
./server.sh start
# Open http://localhost:9500
```

Upload a feature document or type a description → click **Generate** → watch real-time progress as each agent executes.

#### CLI

```bash
# Generate from a text description
python3 main.py generate --feature "Create an incident request and add notes to it"

# Generate from a document
python3 main.py generate --doc path/to/feature.pdf

# Search the knowledge base
python3 main.py search "create solution with custom template" --top-k 5

# Run a specific test
python3 main.py run --entity Solution --method createAndShareApprovedPublicSolutionFromDV
```

#### Docker

```bash
docker-compose up --build
# Web UI at http://localhost:9500
```

### Approach 2: VS Code Agents

> Requires VS Code with GitHub Copilot (Claude Opus 4.6 model).

```
# Set up a new project (interactive wizard)
@setup-project

# Generate tests from a use-case description
@test-generator create a change and verify the detail view title

# Generate tests from a CSV file (place CSV in $PROJECT_NAME/Testcase/)
@test-generator generate tests from the uploaded CSV

# Run and auto-heal a specific test
@test-runner ChangeDetailsView.verifyDetailViewTitle

# Run all pending tests in batch
@test-runner batch

# Debug a specific failure
@test-debugger SDPOD_AUTO_CH_LV_001 fails with NoSuchElementException on association tab
```

---

## 🧠 Knowledge Base

The system's quality depends on **context** — understanding 17,101 existing test patterns before generating new ones.

| Collection | Vectors | Source |
|------------|---------|--------|
| Scenarios | 14,637 | Parsed `@AutomaterScenario` annotations from 1,426 Java files |
| Source Chunks | 8,722 | Method bodies and class structures |
| Help Topics | 920 | Crawled SDP help documentation |

**Embeddings:** `all-MiniLM-L6-v2` (384 dimensions, cosine similarity)

**Duplicate Detection:**

| Similarity | Classification | Action |
|-----------|---------------|--------|
| ≥ 0.90 | Duplicate | Skip |
| 0.75–0.89 | Similar | Generate with note |
| < 0.75 | New | Generate |

---

## 📁 Project Structure

```
AI_AUTOMATION_CODE_GENERATOR/
│
├── agents/                         # Core AI agents (pipeline + shared logic)
│   ├── pipeline.py                 #   LangGraph DAG orchestration
│   ├── ingestion_agent.py          #   Document parsing (PDF/DOCX/XLSX)
│   ├── planner_agent.py            #   Feature → test scenario planning
│   ├── coverage_agent.py           #   Duplicate detection via ChromaDB
│   ├── ui_scout_agent.py           #   Playwright DOM observation
│   ├── coder_agent.py              #   RAG-powered code generation
│   ├── reviewer_agent.py           #   Static + semantic review
│   ├── output_agent.py             #   File writer + KB index update
│   ├── runner_agent.py             #   javac compile + JVM execute
│   ├── healer_agent.py             #   Self-healing via Playwright + LLM
│   ├── hg_agent.py                 #   Mercurial auto-commit (gated)
│   ├── learning_agent.py           #   DO/DON'T rule extraction
│   ├── parallel_runner_agent.py    #   Multi-JVM concurrent runner
│   ├── sdp_api_helper.py           #   SDP data creation via JS API
│   └── llm_factory.py              #   Ollama / OpenRouter / OpenAI factory
│
├── .github/
│   ├── copilot-instructions.md     # 2,000+ lines of framework knowledge for AI agents
│   ├── agents/                     # VS Code agent mode definitions
│   │   ├── test-generator.agent.md #   @test-generator — scenario creation
│   │   ├── test-runner.agent.md    #   @test-runner — compile/run/heal loop
│   │   ├── test-debugger.agent.md  #   @test-debugger — Playwright diagnosis
│   │   └── setup-project.agent.md  #   @setup-project — onboarding wizard
│   └── instructions/               # Auto-loaded coding conventions
│       ├── java-test-conventions.instructions.md
│       └── test-data-format.instructions.md
│
├── config/
│   ├── project_config.py           # All project settings (reads .env)
│   ├── framework_rules.md          # Strict annotation & coding rules
│   ├── framework_knowledge.md      # Framework internals deep-dive
│   └── module_taxonomy.yaml        # 210 SDP module paths
│
├── knowledge_base/
│   ├── vector_store.py             # ChromaDB wrapper
│   ├── context_builder.py          # RAG context assembly
│   └── chroma_db/                  # Persistent vector database
│
├── web/
│   ├── server.py                   # FastAPI + SSE endpoints
│   └── static/                     # Web UI assets
│
├── ingestion/                      # Document parsing & Java source indexing
├── evaluation/                     # Coverage reports & scenario auditing
├── orchestrator/                   # Dashboard server for parallel runs
├── docs/                           # API docs, feature docs, templates
│   └── api-doc/                    #   SDP V3 API endpoint reference
│
├── main.py                         # CLI entry point (pipeline mode)
├── run_test.py                     # Quick single-test runner
├── setup_framework_bin.sh          # Framework compilation script
├── generate_constants.sh           # Auto-generate DataConstants from JSON
├── server.sh                       # Web server start/stop
├── Dockerfile                      # Container support
├── docker-compose.yml
└── $PROJECT_NAME/                  # Active test project (hg-managed)
    ├── src/                        #   Java test source files
    ├── bin/                        #   Compiled .class files
    ├── resources/                  #   Field configs, test data JSONs, roles
    ├── reports/                    #   ScenarioReport.html + screenshots
    └── Testcase/                   #   Use-case CSV/XLSX input files
```

---

## 🔌 API Endpoints

The pipeline mode exposes a REST API via FastAPI:

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/generate` | Start a pipeline run |
| `GET` | `/api/stream/{run_id}` | SSE event stream (live logs) |
| `GET` | `/api/runs` | List all past runs |
| `GET` | `/api/runs/{run_id}` | Get run details + results |
| `POST` | `/api/runs/{run_id}/stop` | Stop a running pipeline |
| `GET` | `/api/modules` | List all 210 SDP modules |
| `GET` | `/api/stats` | System resource stats |
| `GET` | `/api/health` | Health check |

---

## 📊 Results

Tests generated and validated against live SDP instances:

| Module | Tests Passing | Feature |
|--------|:---:|---------|
| Solutions | 2 | Detail view operations (share, custom topic, review/expiry dates) |
| Changes | 6 | CH-286 Linking Changes (parent/child associations, attach/detach) |
| Requests | 1 | Incident request creation with notes |
| Problems | 1 | Problem trigger creation and verification |

---

## ⚙️ Configuration

Key settings in `config/project_config.py` (all overridable via `.env`):

```python
PROJECT_NAME = "SDPLIVE_LATEST_AUTOMATER_SELENIUM"

# Pipeline LLM settings
LLM_PROVIDER = "ollama"              # "ollama", "openrouter", or "openai"
OLLAMA_MODEL = "qwen2.5-coder:7b"
OPENROUTER_MODEL = "gpt-4o-mini"

# Execution settings
PARALLEL_WORKERS = 2
TEST_EXECUTION_TIMEOUT = 1800        # seconds
HEADLESS_MODE = True
```

VS Code agent settings are configured in `.github/agents/*.agent.md` files (model selection, tool permissions, autopilot turn limits).

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [DEMO_DOCUMENTATION.md](DEMO_DOCUMENTATION.md) | Comprehensive technical walkthrough — architecture, all agents, build timeline, results |
| [docs/pipeline-flow.md](docs/pipeline-flow.md) | Pipeline routing logic and state flow diagrams |
| [config/framework_knowledge.md](config/framework_knowledge.md) | AutomaterSelenium framework internals deep-dive |
| [config/framework_rules.md](config/framework_rules.md) | Strict annotation rules, coding conventions, checklists |
| [.github/copilot-instructions.md](.github/copilot-instructions.md) | Complete project knowledge base for AI agents (2,000+ lines) |
| [docs/api-doc/SDP_API_Endpoints_Documentation.md](docs/api-doc/SDP_API_Endpoints_Documentation.md) | SDP V3 REST API reference for all 16 modules |

---

## 🗺 Roadmap

- [x] Core agentic pipeline (Planner → Coder → Reviewer → Runner)
- [x] Self-healing with Playwright
- [x] ChromaDB knowledge base (14,637 vectors)
- [x] Document ingestion (PDF/DOCX/XLSX/PPTX)
- [x] Web UI with SSE streaming
- [x] Mercurial integration (gated auto-commit)
- [x] Parallel execution + learning loop
- [x] Docker support
- [x] VS Code agent modes (`@test-generator`, `@test-runner`, `@test-debugger`, `@setup-project`)
- [x] Claude Opus 4.6 integration via GitHub Copilot
- [x] Playwright MCP for live browser-driven debugging
- [x] Autopilot mode for autonomous generate → run → fix cycles
- [ ] One-click test validation from Web UI
- [ ] Multi-entity scale (all 210 modules)
- [ ] Feedback loop with human approval queue
- [ ] Pipeline monitoring dashboard with per-agent metrics

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Built with LangGraph · Claude Opus · Playwright · ChromaDB · and a lot of ☕
  <br><br>
  <i>From feature document to passing test — in minutes, not days.</i>
</p>
