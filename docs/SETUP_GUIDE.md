# AutomaterSelenium — User Guide

> **Goal**: Go from a use-case document to fully generated (and optionally executed) Selenium test automation code — driven entirely by Copilot agents inside VS Code.

---

## How It Works — Overview

```
  You                     Copilot Agents                        Output
  ───                     ──────────────                        ──────
  1. Run setup        →   @setup-project                   →   Project configured
  2. Upload CSV       →   @test-generator                  →   Java test code generated
  3. (Optional) Run   →   @test-runner                     →   Tests executed & auto-fixed
```

| Step | What you do | What the agent does |
|------|------------|---------------------|
| **Setup** | Answer a few questions (owner, credentials) | Clones the repo, installs dependencies, writes config |
| **Generate** | Place a CSV use-case file in `Testcase/` | Reads CSV, generates Java test code, data files, constants |
| **Run** | Say `@test-runner batch` | Runs each test, auto-diagnoses failures, fixes locators, reruns |

---

## Prerequisites

| Tool | How to check | Install |
|------|-------------|---------|
| Python 3.10+ | `python3 --version` | Pre-installed on most Linux distros |
| Java JDK 17 | `java -version` | `sudo apt install openjdk-17-jdk` |
| Git | `git --version` | `sudo apt install git` |
| Mercurial | `hg --version` | `sudo apt install mercurial` |
| VS Code | — | [Download](https://code.visualstudio.com/) |
| GitHub Copilot | — | Install the VS Code extension + Copilot Chat |
| Firefox + Geckodriver | — | Only needed for **Generate and Run** mode |
| Zoho VPN | — | Connect to `vpn.zohocorporation.com:10443` before any step |

**Also needed** (get from a team member or existing workstation):
- **Dependencies folder** — a directory containing all Selenium and framework JARs. The setup agent will ask for its path.

---

## Step 1 — Clone This Project

```bash
git clone https://github.com/balaji-muthukumaran-12086/AI_AUTOMATION_CODE_GENERATOR.git
cd AI_AUTOMATION_CODE_GENERATOR
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Open the project folder in VS Code.

---

## Step 2 — Run the Setup Agent

1. Open **Copilot Chat** (sidebar or `Ctrl+Shift+I`)
2. Switch to **Agent mode** (dropdown at top of chat)
3. Type: `@setup-project setup`

The agent asks you **two things**:

### Choose your mode

| Mode | What it does | What you need |
|------|-------------|--------------|
| **Generate only** | Generates Java test code — does NOT run tests | hg username + dependencies path |
| **Generate and Run** | Generates code AND runs tests against a live SDP instance | All of the above + SDP URL, credentials, Firefox/Geckodriver |

### Fill in the form

The agent shows a numbered owner list and a form. Example for **Generate only** mode:

```
owner        = 3            ← pick your number from the list, or "new"
hg_username  = your-zrepo-username
branch       = SDPLIVE_LATEST_AUTOMATER_SELENIUM
deps_path    = /home/you/Automater/dependencies
```

> **Security note**: Your hg password is **never typed in the chat**. When the agent clones the repository, Mercurial prompts you for your password directly in the VS Code terminal. This keeps your credentials out of chat history and log files.

For **Generate and Run** mode, you also provide:

```
sdp_url      = https://sdpodqa-auto1.csez.zohocorpin.com:9090/
portal       = portal1
admin_email  = admin@zohotest.com
tech_email   = tech@zohotest.com
password     = yourpassword
drivers_path = /home/you/Automater/Drivers
```

The agent handles everything else: cloning the Mercurial branch (prompts for hg password in the terminal), compiling framework classes, writing `.env`, creating the `Testcase/` folder.

> **New team member?** Select `new` as your owner. The agent asks for your full name and Zoho Corp ID, then registers you automatically.

---

## Step 3 — Prepare Your Use-Case Document

Test generation starts with a **use-case document in CSV format**. This is the primary and recommended input method.

### CSV format

Use the template at `docs/templates/usecase_template.csv`:

| UseCase ID | Severity | Description |
|---|---|---|
| SDPOD_CH_001 | Critical | Create a standard change and verify the title in detail view |
| SDPOD_CH_002 | Major | Add a note to a change and verify it appears in the Notes tab |
| SDPOD_CH_003 | Minor | Verify the priority field is editable via spot edit |

**Columns explained:**

| Column | Required? | What it controls |
|--------|-----------|------------------|
| **UseCase ID** | Yes | Links back to your use case — used in test scenario description |
| **Severity** | Yes | Maps to test priority: `Critical` → HIGH, `Major` → MEDIUM, `Minor` → LOW |
| **Description** | Yes | What the test should do — plain English |
| Module | Optional | Framework module placement (e.g., `Changes`, `Requests`, `Solutions`) |
| Sub-Module | Optional | Entity subclass routing (e.g., `Detail View`, `List View`) |
| Impact Area | Optional | Additional context for the scenario |
| Pre-Requisite | Optional | What needs to exist before the test (drives `preProcess` group selection) |
| UI To-be-automated | Optional | Filter gate — only rows with `Yes` are processed (if column exists) |

> **Tip**: Start with just the 3 required columns. The agent infers Module and Sub-Module from the Description when they're not provided.

### Where to place the CSV

Put your CSV file in the project's `Testcase/` folder:

```
SDPLIVE_LATEST_AUTOMATER_SELENIUM/
└── Testcase/
    └── my_use_cases.csv       ← place your file here
```

This folder was created by `@setup-project`. If it doesn't exist, create it:
```bash
mkdir -p SDPLIVE_LATEST_AUTOMATER_SELENIUM/Testcase
```

### Alternative: plain-text description

For quick one-off scenarios, you can skip the CSV and just describe what you want:

```
@test-generator Create an incident request, add a note, and verify it appears in the Notes tab
```

This works well for 1-3 scenarios. For larger batches, CSV is strongly recommended.

---

## Step 4 — Generate Tests

1. Open **Copilot Chat** → **Agent mode**
2. Type: `@test-generator`
3. If you placed a CSV in `Testcase/`, the agent detects it automatically. Otherwise, drag the file into the chat or type your description.

### What happens

The agent:

1. **Reads** your CSV and filters rows (only `UI To-be-automated = Yes` if the column exists)
2. **Presents a plan** — lists each scenario to generate, grouped by module
3. **Waits for your confirmation** — reply `all` or specific numbers
4. **Generates Java code** for each scenario:
   - `@AutomaterScenario` annotation wrapper in the entity class
   - Test method implementation in the base class
   - Test data entries in `*_data.json`
   - Constants in `*DataConstants.java` and `*AnnotationConstants.java`
   - Locators in `*Locators.java` (if new XPaths are needed)
   - Utility methods in `*ActionsUtil.java` (if new UI operations are needed)
5. **Compiles** the generated code (targeted compile — only edited files)
6. **Writes** test entries to `tests_to_run.json` for the runner

### Multi-project targeting

If you have multiple test-case branches cloned, specify which one:

```
@test-generator project=SDPLIVE_UI_AUTOMATION_BRANCH create a change and verify the detail view
```

If not specified, the agent uses the default from your `.env` configuration.

---

## Step 5 — Run and Debug Tests (Generate and Run mode)

If you chose **Generate and Run** mode during setup, the test-generator hands off to the runner automatically.

To run manually at any time:

```
@test-runner batch
```

This runs every test in `tests_to_run.json` sequentially. For each test:

1. **Runs** the test via the Java runner
2. **If it passes** — moves to the next test
3. **If it fails** — classifies the failure:
   - **Locator issue** → opens the SDP page in a browser, inspects the UI, fixes the XPath
   - **API error** → checks the REST call, fixes the payload
   - **Compile error** → reads the error, fixes the code
   - **Logic error** → analyzes the flow, adjusts the test
4. **Recompiles and reruns** (up to 3 attempts per test)
5. **Reports results** in a summary table

### Run a single test

```
@test-runner Solution.createSolution
```

### View results

Test reports are generated at:
```
SDPLIVE_LATEST_AUTOMATER_SELENIUM/reports/LOCAL_<methodName>_<timestamp>/ScenarioReport.html
```

Open `ScenarioReport.html` in a browser to see pass/fail details with screenshots.

---

## Step 6 — Debug a Specific Test (Optional)

If you need to investigate a particular failure in detail:

```
@test-debugger SDPOD_AUTO_SOL_DV_243 fails with NoSuchElementException on the approval button
```

The debugger agent can:
- Analyze `ScenarioReport.html` failures and screenshots
- Open an SDP page in a browser to inspect UI elements live
- Create prerequisite test data to reach the correct UI state
- Fix broken XPath locators and API calls

> **Tip**: Include the test ID, error type, and any relevant log output for faster diagnosis.

---

## Orchestrator Dashboard

The orchestrator tracks all generated scenarios, test runs, and healing events in a web dashboard.

```bash
# Start locally
./orchestrator.sh start
# Open http://localhost:9600
```

**Hosted URL** (if configured): check your `.env` for `ORCHESTRATOR_URL`.

---

## Quick Reference

| Task | Command |
|------|---------|
| Initial setup | `@setup-project setup` |
| Generate tests from CSV | Place CSV in `Testcase/`, then `@test-generator` |
| Generate from description | `@test-generator <your description>` |
| Run all generated tests | `@test-runner batch` |
| Run one test | `@test-runner Solution.createSolution` |
| Debug a failure | `@test-debugger <test ID> <error description>` |
| Start dashboard | `./orchestrator.sh start` |
| Recompile framework | `./setup_framework_bin.sh` |

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `javac: command not found` | `sudo apt install openjdk-17-jdk` |
| `hg: command not found` | `sudo apt install mercurial` |
| `NullPointerException` in test | Run `./setup_framework_bin.sh` to recompile framework |
| VPN / connection errors | Connect to Zoho VPN first |
| `BUILD FAILED` on compile | Use targeted compile — full project compile is intentionally unsupported |
| `OWNER_CONSTANT` empty | Re-run `@setup-project setup` |
| Project folder not found | Run `@setup-project setup`, or check the folder name |
| Multiple projects, wrong target | Use `@test-generator project=BRANCH_NAME` |
| `Testcase/` folder missing | `mkdir -p SDPLIVE_LATEST_AUTOMATER_SELENIUM/Testcase` |
| Generated test fails on first run | Normal — `@test-runner` auto-diagnoses and fixes. Run `@test-runner batch` |
