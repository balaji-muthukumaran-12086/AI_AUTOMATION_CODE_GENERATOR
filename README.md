<p align="center">
  <h1 align="center">AI Automation Code Generator</h1>
  <p align="center">
    <strong>Generate production-ready Selenium test cases from natural language using an AI-powered agentic pipeline</strong>
  </p>
  <p align="center">
    <a href="#features">Features</a> •
    <a href="#architecture">Architecture</a> •
    <a href="#quick-start">Quick Start</a> •
    <a href="#usage">Usage</a> •
    <a href="#agents">Agents</a> •
    <a href="#knowledge-base">Knowledge Base</a> •
    <a href="#documentation">Documentation</a>
  </p>
</p>

---

## Overview

AI Automation Code Generator is an end-to-end system that transforms **feature descriptions or documents** into **working, framework-compliant Java Selenium test cases** — without manual intervention.

Upload a feature document → the system reads it, plans test scenarios, checks for duplicates against 14,637 existing tests, observes the live UI via Playwright, generates Java code, reviews it, compiles it, runs it against a real SDP instance, and if it fails — **self-heals and retries automatically**.

Built for the [ServiceDesk Plus](https://www.manageengine.com/products/service-desk/) QA automation framework (`AutomaterSelenium`), but the agentic architecture is adaptable to any Selenium-based test framework.

## Features

- **Document Ingestion** — Parse PDF, DOCX, XLSX, PPTX, Markdown, and plain text feature documents
- **Intelligent Planning** — LLM breaks features into concrete test scenarios mapped to correct modules
- **Duplicate Detection** — ChromaDB vector search against 14,637 indexed scenarios prevents redundant generation
- **Live UI Observation** — Playwright captures real DOM snapshots before code generation for accurate locators
- **Convention-Compliant Code** — RAG-powered generation follows the exact `AutomaterSelenium` patterns
- **Automated Review** — Static + semantic code review with revision loop (max 2 iterations)
- **Compile & Execute** — Generated tests are compiled with `javac` and run against a live SDP instance
- **Self-Healing** — Failed tests are auto-debugged via Playwright DOM inspection and LLM-driven patching
- **Learning Loop** — Extracts DO/DON'T rules from failures; future runs get smarter
- **Web UI** — Real-time progress via SSE streaming, document upload, run history
- **Parallel Execution** — Batch runner launches multiple JVMs concurrently
- **Version Control** — Optional Mercurial auto-branch and commit on test pass

## Architecture

```
                         Feature Document / Description
                                      │
                                      ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Ingestion│→ │ Planner  │→ │ Coverage │→ │ UI Scout │→ │  Coder   │
│  Agent   │  │  Agent   │  │  Agent   │  │  Agent   │  │  Agent   │
│  📄→📝   │  │  🤖 LLM   │  │  🔍 RAG  │  │  🌐+🤖   │  │  🤖 LLM   │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘
                                                               │
                                                               ▼
┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│ Hg Agent │← │  Healer  │← │  Runner  │← │  Output  │← │ Reviewer │
│   (VCS)  │  │  Agent   │  │  Agent   │  │  Agent   │  │  Agent   │
│   📦     │  │  🤖+🌐   │  │  ☕ Java  │  │  📁     │  │  🤖 LLM   │
└──────────┘  └──────────┘  └──────────┘  └──────────┘  └──────────┘

🤖 LLM call    🌐 Playwright browser    ☕ Java subprocess    🔍 Vector search
```

### Tech Stack

| Component | Technology |
|-----------|-----------|
| Orchestration | [LangGraph](https://github.com/langchain-ai/langgraph) |
| LLM (local) | [Ollama](https://ollama.ai/) — `qwen2.5-coder:7b` |
| LLM (cloud) | [OpenRouter](https://openrouter.ai/) — `gpt-4o-mini` |
| Vector DB | [ChromaDB](https://www.trychroma.com/) — `all-MiniLM-L6-v2` embeddings |
| Browser Automation | [Playwright](https://playwright.dev/) (Chromium) |
| Test Framework | Java Selenium (AutomaterSelenium) |
| Web Server | [FastAPI](https://fastapi.tiangolo.com/) + SSE |
| Containerization | Docker + docker-compose |

## Quick Start

### Prerequisites

- Python 3.10+
- Java 8+ (for `javac` compilation)
- [Ollama](https://ollama.ai/) (optional — for local LLM inference)

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

# Pull the local LLM model (optional)
ollama pull qwen2.5-coder:7b
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
python3 main.py setup
```

## Usage

### Web UI (Recommended)

```bash
# Start the server
./server.sh start

# Open in browser
# http://localhost:9500
```

Upload a feature document or paste a description → click **Generate** → watch real-time progress as each agent executes.

### CLI

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

### Docker

```bash
docker-compose up --build
# Web UI available at http://localhost:9500
```

## Agents

The pipeline consists of **10 specialized agents**, each handling a distinct concern:

| # | Agent | Lines | Purpose | Uses |
|---|-------|-------|---------|------|
| 1 | **Ingestion** | 502 | Parse uploaded documents (PDF/DOCX/XLSX/TXT) | PyMuPDF, python-docx |
| 2 | **Planner** | 139 | Break features into test scenarios | LLM |
| 3 | **Coverage** | 159 | Deduplicate against existing tests | ChromaDB |
| 4 | **UI Scout** | 788 | Capture live DOM snapshots | Playwright + LLM |
| 5 | **Coder** | 892 | Generate Java test code | LLM + RAG context |
| 6 | **Reviewer** | 271 | Static + semantic code review | LLM |
| 7 | **Output** | 273 | Write files to disk, index in ChromaDB | File I/O |
| 8 | **Runner** | 850 | Compile and execute tests | javac + JVM |
| 9 | **Healer** | 1,079 | Self-heal failing tests via DOM inspection | Playwright + LLM |
| 10 | **Hg** | 319 | Auto-commit to Mercurial (gated) | hg CLI |

**Supporting modules:**

| Module | Lines | Purpose |
|--------|-------|---------|
| SDP API Helper | 1,065 | Create prerequisite test data via browser JS API |
| Learning Agent | 658 | Extract DO/DON'T rules from batch results |
| Parallel Runner | 303 | Concurrent multi-JVM test execution |
| LLM Factory | 102 | Unified Ollama/OpenRouter abstraction |
| Pipeline | 320 | LangGraph routing and state management |

**Total: 8,007 lines of agent code across 17 files**

## Knowledge Base

The system's quality depends on **context** — it must understand 17,101 existing test patterns before generating new ones.

| Collection | Vectors | Source |
|------------|---------|--------|
| Scenarios | 14,637 | Parsed `@AutomaterScenario` annotations from 1,426 Java files |
| Source Chunks | 8,722 | Method bodies and class structures |
| Help Topics | 920 | Crawled SDP help documentation |

**Embeddings:** `all-MiniLM-L6-v2` (384 dimensions, cosine similarity)

### Duplicate Detection Thresholds

| Similarity | Classification | Action |
|-----------|---------------|--------|
| ≥ 0.90 | Duplicate | Skip |
| 0.75–0.89 | Similar | Generate with note |
| < 0.75 | New | Generate |

## Project Structure

```
ai-automation-qa/
├── agents/                    # All 14 AI agents
│   ├── pipeline.py            # LangGraph orchestration
│   ├── coder_agent.py         # Code generation (RAG + LLM)
│   ├── healer_agent.py        # Self-healing (Playwright + LLM)
│   ├── runner_agent.py        # Compile & execute
│   ├── sdp_api_helper.py      # Prerequisite data creation
│   └── ...
├── config/
│   ├── project_config.py      # All project settings
│   ├── framework_rules.md     # Generation rules & learnings
│   └── module_taxonomy.yaml   # 210 SDP module paths
├── knowledge_base/
│   ├── vector_store.py        # ChromaDB wrapper
│   ├── context_builder.py     # RAG context assembly
│   └── chroma_db/             # Persistent vector database
├── web/
│   ├── server.py              # FastAPI + SSE endpoints
│   └── static/                # Web UI assets
├── ingestion/                 # Document parsing & indexing
├── templates/java/            # Code generation templates
├── main.py                    # CLI entry point
├── run_test.py                # Quick single-test runner
├── server.sh                  # Web server start/stop
├── Dockerfile                 # Container support
├── docker-compose.yml
└── DEMO_DOCUMENTATION.md      # Detailed technical documentation
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/generate` | Start a pipeline run |
| `GET` | `/api/stream/{run_id}` | SSE event stream (live logs) |
| `GET` | `/api/runs` | List all past runs |
| `GET` | `/api/runs/{run_id}` | Get run details |
| `POST` | `/api/runs/{run_id}/stop` | Stop a running pipeline |
| `GET` | `/api/modules` | List SDP modules |
| `GET` | `/api/stats` | System resource stats |
| `GET` | `/api/health` | Health check |

## Results

Tests generated and validated against live SDP instances:

| Module | Tests Passing | Feature |
|--------|:---:|---------|
| Solutions | 2 | Detail view operations (share, custom topic, review/expiry dates) |
| Changes | 6 | CH-286 Linking Changes (parent/child associations, attach/detach) |
| Requests | 1 | Incident request creation with notes |
| Problems | 1 | Problem trigger creation and verification |

## Configuration

Key settings in `config/project_config.py`:

```python
PROJECT_NAME = "SDPLIVE_LATEST_AUTOMATER_SELENIUM"

LLM_PROVIDER = "ollama"          # "ollama" or "openrouter"
OLLAMA_MODEL = "qwen2.5-coder:7b"
OPENROUTER_MODEL = "gpt-4o-mini"

PARALLEL_WORKERS = 2
TEST_EXECUTION_TIMEOUT = 1800    # seconds
HEADLESS_MODE = True
```

## Documentation

- [**DEMO_DOCUMENTATION.md**](DEMO_DOCUMENTATION.md) — Comprehensive technical walkthrough (1,172 lines) covering architecture, all agents, day-by-day timeline, and results
- [**docs/pipeline-flow.md**](docs/pipeline-flow.md) — Pipeline routing logic and state flow
- [**config/framework_knowledge.md**](config/framework_knowledge.md) — AutomaterSelenium framework conventions
- [**.github/copilot-instructions.md**](.github/copilot-instructions.md) — Complete project knowledge base for AI-assisted development

## Roadmap

- [x] Core agentic pipeline (Planner → Coder → Reviewer → Runner)
- [x] Self-healing with Playwright
- [x] ChromaDB knowledge base (14,637 vectors)
- [x] Document ingestion (PDF/DOCX/XLSX/PPTX)
- [x] Web UI with SSE streaming
- [x] Mercurial integration (gated)
- [x] Parallel execution + learning loop
- [x] Docker support
- [ ] One-click test validation from Web UI
- [ ] Multi-entity scale (all 210 modules)
- [ ] Feedback loop with human approval queue
- [ ] Pipeline monitoring dashboard with per-agent metrics

---

<p align="center">
  Built with LangGraph, ChromaDB, Playwright, and a lot of ☕
</p>
