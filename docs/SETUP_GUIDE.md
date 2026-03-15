# AI Automation Code Generator — User Setup Guide

> Give use-case documents to Copilot agents → get fully generated Selenium test code.

---

## 3 Steps — That's It

```
  1. Setup       →   Web UI (localhost:9500/setup)   →   Project ready
  2. Generate    →   @test-generator                →   Java tests generated
  3. Run         →   @test-runner batch              →   Tests executed & auto-fixed
```

---

## Before You Start

1. Install [VS Code](https://code.visualstudio.com/) with **GitHub Copilot** + **Copilot Chat** extensions (v1.99+)
2. Download **Dependencies** and **Drivers** (Firefox + Geckodriver) zip files from [WorkDrive](https://workdrive.zoho.in/folder/l5o5d7049285d45dd49ae80d7be1a209a6841)

Open VS Code, then open the **Terminal** (`Ctrl+\``) and run:

```bash
sudo apt install openjdk-17-jdk git mercurial python3 python3-venv nodejs npm
```

---

## Step 1 — Clone & Open

In the same VS Code terminal, run these one by one:

```bash
git clone https://github.com/balaji-muthukumaran-12086/AI_AUTOMATION_CODE_GENERATOR.git
```
```bash
cd AI_AUTOMATION_CODE_GENERATOR
```
```bash
# Pick ONE — lightweight (VS Code/Copilot only) or full (LangGraph pipeline + orchestrator):
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements_vs.txt   # lightweight — 2 packages
# python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt    # full — all 22 packages
```
```bash
npm install                      # installs @playwright/mcp + auto-downloads Chromium browser
```

Now open this folder in VS Code: **File → Open Folder** → select `AI_AUTOMATION_CODE_GENERATOR`

---

## Step 2 — Project Setup

Start the server and open the setup page in your browser:

```bash
./server.sh start
```

Open **http://localhost:9500/setup** in your browser.

#### Setup Modes

| Mode | When to Use |
|------|-------------|
| **📝 Generate Only** | Generate Java test code from feature docs. You run tests manually. |
| **🚀 Generate & Run** | Generate code AND execute against a live SDP instance automatically. |
| **⚙️ Reconfigure** | Project already set up. Add or update SDP credentials, drivers & environment to enable test execution. |

#### Generate Only / Generate & Run

1. Select your mode
2. Fill in:
   - **Hg Username** — your zrepository username (e.g. `balaji-12086`)
   - **Branch Name** — hg branch to clone (e.g. `feature/SDPLIVE_LINKING_CHANGE_AI`)
   - **Dependencies Path** — absolute path to the JARs folder
3. For **Generate & Run**, also fill in:
   - **SDP URL**, **Portal**, **Admin Email**, **Tech Email**, **Password**, **Drivers Path**
4. Click **🚀 Run Setup**
5. A **password modal** appears in the browser — enter your hg password (used once for cloning, never saved)
6. An **owner selection modal** appears — pick your name from the list
   - **New to the team?** Click *"➕ Not in the list? Register as new member"* — enter your full name and Zoho email to register
7. Watch the progress log — setup clones the branch, compiles the framework, and configures `.env`

#### Reconfigure

Use this when your project is already cloned and you need to add or update SDP connection details — for example, after starting in **Generate Only** mode and later wanting to run tests.

1. Select **Reconfigure** mode
2. Pick your project from the **Project Folder** dropdown (shows all project folders including `MSP_*`, `SDP_*`, `SDPLIVE_*`)
3. Fill in / update SDP credentials and driver paths
4. Click **🚀 Run Setup** — `.env` is updated, no re-clone or re-generation needed

> **Upgrade workflow**: Generate Only → (days later) → Reconfigure → `@test-runner batch`  
> Your generated tests are preserved. Reconfigure only adds the missing SDP environment to `.env`.

#### Server Commands

```bash
./server.sh start     # Start on port 9500
./server.sh stop      # Stop the server
./server.sh restart   # Restart
./server.sh status    # Check if running
./server.sh logs      # Tail live logs
PORT=8090 ./server.sh start   # Custom port
```

> **Password security**: The hg password is entered via a browser modal during setup and is never saved to `.env`, logs, or chat history.

---

## Step 3 — Generate & Run Tests

### Upload your use-case document

Place your file (`.csv`, `.xlsx`, or `.xls`) in `<PROJECT_NAME>/Testcase/` (template: `docs/templates/usecase_template.csv`).

> Only rows with `UI To-be-automated = Yes` are processed.

### Generate from a use-case document (recommended for batches)

In Copilot Chat: **`@test-generator`** — it picks up the document automatically. Review the plan, reply `all` to generate.

### Generate from a description (quick one-offs)

```
@test-generator Create an incident request, add a note, and verify it appears in the Notes tab
```

### Run tests

```
@test-runner batch                          # run all generated tests
@test-runner Solution.createSolution        # run a single test
```

The runner auto-diagnoses failures, fixes locators/code, and reruns (up to 3 attempts).

### Debug a specific failure

```
@test-debugger SDPOD_AUTO_SOL_DV_243 fails with NoSuchElementException on the approval button
```

### View reports

```
<PROJECT_NAME>/reports/LOCAL_<methodName>_<timestamp>/ScenarioReport.html
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Start web server | `./server.sh start` → open `http://localhost:9500` |
| Setup project | `http://localhost:9500/setup` |
| Reconfigure project | Setup page → Reconfigure mode |
| Generate from use-case doc | Place file in `Testcase/`, then `@test-generator` |
| Generate from text | `@test-generator <description>` |
| Run all tests | `@test-runner batch` |
| Run one test | `@test-runner Entity.methodName` |
| Debug a failure | `@test-debugger <test ID> <error>` |
| Recompile framework | `./setup_framework_bin.sh` |
| Setup Playwright MCP | `npm install && npx playwright install chromium` |
| Verify Playwright | `./start_playwright_mcp.sh` |
| Start dashboard | `./orchestrator.sh start` → `http://localhost:9600` |
| Stop web server | `./server.sh stop` |

---

## Common Fixes

| Problem | Fix |
|---------|-----|
| VPN / connection errors | Connect to Zoho VPN first |
| `NullPointerException` in test | `./setup_framework_bin.sh` |
| `Testcase/` folder missing | `mkdir -p <PROJECT_NAME>/Testcase` |
| Project not in Reconfigure dropdown | Project folder must be in the workspace root; names with `MSP_`/`SDP_`/`SDPLIVE_`/`AALAM_` prefixes or containing `src/` are auto-detected |
| Owner not in dropdown | Click *"➕ Not in the list? Register as new member"* to add yourself |
| Hg password prompt not appearing | Ensure the server is running (`./server.sh status`); reload setup page |
| Test fails on first run | Normal — `@test-runner` auto-fixes and reruns |
| Wrong project targeted | `@test-generator project=BRANCH_NAME` |
| Upgrade Generate Only → Run | Setup page → Reconfigure → add SDP URL/credentials/drivers |
| Playwright MCP not available | `npm install && npx playwright install chromium` then `./start_playwright_mcp.sh` |
| `@test-runner` skips locator fixes | Playwright MCP not loaded — restart VS Code or run `./start_playwright_mcp.sh --start` |

---

> **Why VS Code?** The `@agent` workflow requires VS Code Agent mode (1.99+) — Eclipse and IntelliJ don't support it. You can still use Eclipse for regular Java work alongside VS Code for test generation.
