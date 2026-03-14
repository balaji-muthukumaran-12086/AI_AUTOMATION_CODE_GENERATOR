# AI Automation Code Generator — User Setup Guide

> Give use-case documents to Copilot agents → get fully generated Selenium test code.

---

## 3 Steps — That's It

```
  1. Setup       →   Web UI or @setup-project      →   Project ready
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
python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
```
```bash
npm install                      # installs @playwright/mcp + auto-downloads Chromium browser
```

Now open this folder in VS Code: **File → Open Folder** → select `AI_AUTOMATION_CODE_GENERATOR`

---

## Step 2 — Project Setup

You have **two options** — the Web UI or the Copilot Chat agent. Both perform the full setup including use-case document upload and analysis.

| Capability | Web UI | @setup-project agent |
|-----------|--------|---------------------|
| Mode selection (generate only / generate & run / reconfigure) | ✅ | ✅ |
| Hg clone with branch creation fallback | ✅ | ✅ |
| Password entry | Browser modal (secure) | Terminal prompt (secure) |
| Owner selection + new member registration | ✅ | ✅ |
| `.env` + `.gitignore` + VS Code settings | ✅ | ✅ |
| Framework compilation | ✅ | ✅ |
| Testcase/ folder creation + spreadsheet conversion | ✅ | ✅ |
| **Use-case document upload** | ✅ (drag & drop modal) | ✅ (blocks until uploaded) |
| **Use-case analysis report** | ✅ (runs `generate_batch_summary.py`) | ✅ (runs `generate_batch_summary.py`) |
| **Folder-exists handling** (Pull/Delete/Use-as-is) | Auto-pulls | ✅ (asks user) |
| **Reveal project in VS Code Explorer** | ❌ | ✅ |

> **TL;DR**: Use the **Web UI** for quick, full-featured setup. Use `@setup-project` only if you need interactive folder-exists choices or VS Code Explorer reveal.

### Option A — Web UI Setup (recommended)

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
| **⚙️ Reconfigure** | Project already cloned. Update environment, credentials, drivers. |

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

1. Select **Reconfigure** mode
2. Pick your project from the **Project Folder** dropdown (shows all project folders including `MSP_*`, `SDP_*`, `SDPLIVE_*`)
3. Update credentials/paths as needed
4. Click **🚀 Run Setup**

#### Server Commands

```bash
./server.sh start     # Start on port 9500
./server.sh stop      # Stop the server
./server.sh restart   # Restart
./server.sh status    # Check if running
./server.sh logs      # Tail live logs
PORT=8090 ./server.sh start   # Custom port
```

### Option B — Copilot Chat Agent

1. Open **Copilot Chat** (`Ctrl+Shift+I`)
2. Switch to **Agent mode** (dropdown at top)
3. Type: **`@setup-project setup`**

The agent walks you through everything interactively in chat.

> **Password security**: In both options, the hg password is entered interactively (browser modal or terminal prompt) and never saved to `.env`, logs, or chat history.

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
| Setup via Web UI | `http://localhost:9500/setup` |
| Setup via agent | `@setup-project setup` |
| Reconfigure (Web) | Setup page → Reconfigure mode |
| Reconfigure (agent) | `@setup-project setup` → mode 3 |
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
| Need to switch SDP instance | Setup page → Reconfigure → update URL/credentials |
| Playwright MCP not available | `npm install && npx playwright install chromium` then `./start_playwright_mcp.sh` |
| `@test-runner` skips locator fixes | Playwright MCP not loaded — restart VS Code or run `./start_playwright_mcp.sh --start` |

---

> **Why VS Code?** The `@agent` workflow requires VS Code Agent mode (1.99+) — Eclipse and IntelliJ don't support it. You can still use Eclipse for regular Java work alongside VS Code for test generation.
