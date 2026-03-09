# AI Automation Code Generator — Setup Guide

> **For new team members.** Follow these steps after cloning the GitHub repository to get the full system running on your machine.

---

## Prerequisites

Install the following before you begin:

| Requirement | Minimum Version | Verify With |
|-------------|----------------|-------------|
| **Python** | 3.10+ | `python3 --version` |
| **Java JDK** | 11+ (JDK 17 recommended) | `java -version` |
| **Git** | Any recent version | `git --version` |
| **Mercurial (hg)** | Any recent version | `hg --version` |
| **Firefox** | ESR or latest | `firefox --version` |
| **Geckodriver** | Compatible with your Firefox | `geckodriver --version` |
| **VS Code** | Latest stable | — |
| **GitHub Copilot extension** | Latest (Chat + Agent mode) | VS Code Extensions panel |

### Network Access

- **VPN**: Connect to the Zoho VPN via FortiClient (`vpn.zohocorporation.com:10443`) before running any tests — the SDP instance and Mercurial repository are internal.
- **Internet**: Required for `pip install`, Playwright browser download, and (optionally) cloud LLM API calls.

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/balaji-muthukumaran-12086/AI_AUTOMATION_CODE_GENERATOR.git
cd AI_AUTOMATION_CODE_GENERATOR
```

---

## Step 2 — Python Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate       # Linux / macOS
# .venv\Scripts\activate        # Windows (if applicable)

pip install -r requirements.txt
```

This installs all 21 Python dependencies (LangChain, ChromaDB, Playwright, FastAPI, etc.).

### Install Playwright Browser

```bash
playwright install chromium
```

Playwright (Chromium) is used by the UI Scout and Healer agents to capture live DOM snapshots. This is separate from the Firefox + Geckodriver used for Selenium test execution.

---

## Step 3 — Run the Setup Agent (VS Code)

This is the **recommended** way to configure everything. It handles Mercurial clone, owner detection, SDP credentials, and path configuration in one interactive flow.

1. Open the project folder in VS Code
2. Open **GitHub Copilot Chat** (Ctrl+Shift+I or the Copilot icon)
3. Switch to **Agent mode** (click the mode selector at the top of the chat panel)
4. Type:
   ```
   @setup-project setup
   ```
5. The agent will ask you for:

| Prompt | What to Provide | Example |
|--------|----------------|---------|
| Mercurial username | Your `zrepository` username | `balaji-12086` |
| Mercurial password | Your `zrepository` password | *(entered securely)* |
| Hg branch name | The test-case branch to clone | `SDPLIVE_LATEST_AUTOMATER_SELENIUM` |
| SDP build URL | Your SDP Cloud instance URL | `https://sdpondemand.manageengine.com` |
| Portal name | SDP portal identifier | `portal1` |
| Admin email | SDP admin login email | `admin@example.com` |
| Technician email | Technician user email (for USER_BASED tests) | `tech@example.com` |
| Password | SDP login password | `Admin@123` |
| Dependencies path | Absolute path to the Java JARs folder | `/home/you/dependencies` |
| Drivers path | Folder containing Firefox binary + geckodriver | `/home/you/Drivers` |

### What the Agent Does Automatically

- **Clones** the Mercurial test-case branch into `SDPLIVE_LATEST_AUTOMATER_SELENIUM/`
- **Detects your owner identity** from your hg username (maps to `OwnerConstants.*`)
  - If you're a **new team member** not yet in the mapping, it will ask your full name and email, then register you in `OwnerConstants.java` automatically
- **Writes** all values to `.env` and updates `config/project_config.py`
- **Compiles** the framework (runs `setup_framework_bin.sh` if needed)

After the agent finishes, your `.env` file will be fully configured. You should **never need to edit `.env` manually** unless changing machines.

---

## Step 4 — Manual `.env` Setup (Alternative)

If you prefer not to use the setup agent, copy the template and fill in values by hand:

```bash
cp .env.example .env
```

Edit `.env` and fill in these **required** fields:

```env
# ── LLM Provider ──────────────────────────────
# Option A: Local Ollama (free, lower quality)
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5-coder:7b
OLLAMA_BASE_URL=http://localhost:11434

# Option B: OpenRouter (RECOMMENDED — best code quality)
# LLM_PROVIDER=openrouter
# OPENROUTER_API_KEY=sk-or-...your-key...
# OPENROUTER_MODEL=openai/gpt-4o

# ── Java Dependencies & Drivers ───────────────
DEPS_DIR=/absolute/path/to/dependencies
FIREFOX_BINARY=/absolute/path/to/firefox/firefox
GECKODRIVER_PATH=/absolute/path/to/geckodriver

# ── Mercurial Identity ────────────────────────
HG_USERNAME=your-zrepo-username
# OWNER_CONSTANT is auto-resolved — leave blank
OWNER_CONSTANT=
```

Then clone the test-case branch manually:

```bash
hg clone -b SDPLIVE_LATEST_AUTOMATER_SELENIUM \
  https://YOUR_USERNAME:YOUR_PASSWORD@zrepository.zohocorpcloud.in/zohocorp/Automater/AutomaterSelenium \
  SDPLIVE_LATEST_AUTOMATER_SELENIUM
```

And compile the framework:

```bash
./setup_framework_bin.sh
```

---

## Step 5 — LLM Configuration

Choose **one** of these LLM providers:

### Option A: Ollama (Local, Free)

```bash
# Install Ollama (if not already installed)
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the recommended model
ollama pull qwen2.5-coder:7b

# Start ollama server (usually starts automatically)
ollama serve
```

> **Note**: The 7B local model does not support tool-calling. The Coder Agent will use static RAG mode (still functional, but lower quality than cloud models).

### Option B: OpenRouter (Recommended)

1. Create an account at [openrouter.ai](https://openrouter.ai/)
2. Generate an API key
3. Set in `.env`:
   ```env
   LLM_PROVIDER=openrouter
   OPENROUTER_API_KEY=sk-or-...your-key...
   OPENROUTER_MODEL=openai/gpt-4o
   ```

This gives access to GPT-4o, Claude, and other models through a single API key with full tool-calling support.

---

## Step 6 — Build the Knowledge Base (One-Time)

Index all existing test scenarios into ChromaDB for duplicate detection and RAG context:

```bash
source .venv/bin/activate
python3 main.py setup
```

This scans all Java test files and creates vector embeddings. Takes a few minutes on first run.

---

## Step 7 — Verify the Setup

### Quick Smoke Test

```bash
source .venv/bin/activate

# Search the knowledge base (should return results)
python3 main.py search "create solution with custom template" --top-k 3
```

If this returns matching test scenarios, the knowledge base is working.

### Run an Existing Test

Edit `run_test.py` to target a known-good test, then:

```bash
python3 run_test.py 2>&1
```

Check the report at:
```
SDPLIVE_LATEST_AUTOMATER_SELENIUM/reports/LOCAL_<methodName>_<timestamp>/ScenarioReport.html
```

---

## Usage

Once setup is complete, you have **three ways** to generate and run tests:

### 1. VS Code Agent Mode (Recommended for Daily Use)

In Copilot Chat (Agent mode):

```
@test-generator Create a test that verifies adding notes to an incident request
```

The agent will:
- Determine the correct module and entity
- Check for duplicates
- Generate the Java test code
- Write all necessary files (test class, data JSON, constants)

### 2. Web UI

```bash
./server.sh start
# Open http://localhost:9500
```

Upload a feature document (PDF, DOCX, XLSX, Markdown) or paste a description. Watch real-time progress as each pipeline agent executes.

To stop:
```bash
./server.sh stop
```

### 3. CLI

```bash
# Generate from a text description
python3 main.py generate --feature "Create a change and verify the detail view"

# Generate from a document
python3 main.py generate --doc path/to/feature.pdf

# Run a specific test
python3 main.py run --entity Solution --method createAndShareApprovedPublicSolutionFromDV
```

---

## Java Dependencies

The framework requires a `dependencies/` folder containing all Selenium and framework JARs. This folder is **not included** in the Git repository (it's too large).

### Where to Get It

Ask a team member for the `dependencies/` (or `dependencies17/`) folder, or copy it from an existing automation workstation. It contains:

```
dependencies/
├── selenium-*.jar          # Selenium WebDriver
├── json.jar                # JSON parsing
├── testng.jar              # TestNG annotations
├── framework/
│   ├── AutomationFrameWork.jar   # Core automation framework
│   └── ...
└── ... (other support JARs)
```

Set its absolute path in `.env`:
```env
DEPS_DIR=/home/you/dependencies
```

---

## Firefox & Geckodriver

The Selenium tests run on **Firefox** (not Chrome). You need:

1. **Firefox binary** — download from [mozilla.org](https://www.mozilla.org/firefox/) or use your system package manager
2. **Geckodriver** — download from [github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases) (match your Firefox version)

Set paths in `.env`:
```env
FIREFOX_BINARY=/path/to/firefox/firefox
GECKODRIVER_PATH=/path/to/geckodriver
```

Or set `DRIVERS_DIR` to a parent folder containing both:
```env
DRIVERS_DIR=/home/you/Drivers
# Expected structure:
# Drivers/firefox/firefox
# Drivers/geckodriver
```

---

## Folder Structure After Setup

```
AI_AUTOMATION_CODE_GENERATOR/
├── .env                                    # Your local config (gitignored)
├── .venv/                                  # Python virtual environment (gitignored)
├── SDPLIVE_LATEST_AUTOMATER_SELENIUM/      # Hg-cloned test cases (gitignored)
│   ├── src/                                # Test source files
│   ├── bin/                                # Compiled .class files
│   ├── resources/                          # JSON data & config
│   └── reports/                            # Test execution reports
├── AutomaterSeleniumFramework/             # Framework source (git-tracked)
├── agents/                                 # Pipeline agents (Python)
├── config/                                 # Project configuration
├── docs/                                   # Documentation
├── knowledge_base/                         # ChromaDB vector store (gitignored)
└── web/                                    # Web UI static files
```

> Files marked **(gitignored)** are generated locally and not committed to Git.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` on `import` | Activate venv: `source .venv/bin/activate` |
| `javac: command not found` | Install JDK: `sudo apt install openjdk-17-jdk` |
| `hg: command not found` | Install Mercurial: `sudo apt install mercurial` |
| `ConnectionRefusedError` on test run | Connect to VPN first, verify SDP URL is reachable |
| `NullPointerException` in test | Run `./setup_framework_bin.sh` to recompile the framework |
| Knowledge base empty / no results | Run `python3 main.py setup` to re-index |
| `OWNER_CONSTANT` is empty | Re-run `@setup-project setup` or set `HG_USERNAME` in `.env` |
| Firefox crashes / geckodriver error | Verify Firefox + geckodriver version compatibility |
| `BUILD FAILED` on compile | Use targeted compile (see `copilot-instructions.md`) — full compile is broken |
| Port 9500 already in use | `./server.sh stop` then `./server.sh start` |

---

## Getting Help

- **Pipeline documentation**: See [docs/pipeline-flow.md](pipeline-flow.md)
- **API reference**: See [docs/api-doc/SDP_API_Endpoints_Documentation.md](api-doc/SDP_API_Endpoints_Documentation.md)
- **Framework conventions**: See [.github/copilot-instructions.md](../.github/copilot-instructions.md)
- **Ask Copilot**: In VS Code Agent mode, ask `@workspace` about the codebase structure
