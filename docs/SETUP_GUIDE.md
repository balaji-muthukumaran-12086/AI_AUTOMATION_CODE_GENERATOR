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

Run each command below in your terminal, one at a time:

```bash
git clone https://github.com/balaji-muthukumaran-12086/AI_AUTOMATION_CODE_GENERATOR.git
```
```bash
cd AI_AUTOMATION_CODE_GENERATOR
```
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
```bash
pip install -r requirements.txt
```

Then open the `AI_AUTOMATION_CODE_GENERATOR` folder in VS Code (`File → Open Folder`).

---

## Step 2 — Run the Setup Agent

1. Open **Copilot Chat** (sidebar or `Ctrl+Shift+I`)
2. Switch to **Agent mode** (dropdown at top of chat)
3. Type: `@setup-project setup`

The agent asks you **two things**:

### Choose your mode

| Mode | What it does | What you need |
|------|-------------|--------------|
| **1. Generate only** | Generates Java test code — does NOT run tests | hg username + dependencies path |
| **2. Generate and Run** | Generates code AND runs tests against a live SDP instance | All of the above + SDP URL, credentials, Firefox/Geckodriver |
| **3. Reconfigure existing project** | Skips cloning — just updates run environment config | Dependencies path + SDP URL, credentials, Firefox/Geckodriver |

> **When to use Reconfigure**: You already have the project cloned (from a previous setup or manual clone) and just need to point it at a different SDP instance, update credentials, or switch to execution mode. No hg username or branch needed — the agent auto-detects your existing project folder.

### Fill in the form

The agent shows a numbered owner list and a clean form you can copy-paste. Example for **Generate only** mode:

```
owner       = 3
hg_username = your-zrepo-username
branch      = SDPLIVE_UI_AUTOMATION_BRANCH
deps_path   = /home/you/Automater/dependencies
```

> `branch` has no default — enter your team's branch name (e.g. `SDPLIVE_UI_AUTOMATION_BRANCH`).

For **Generate and Run** mode, the form also includes:

```
sdp_url          = https://sdpodqa-auto1.csez.zohocorpin.com:9090/
portal           = portal1
admin_email      = admin@zohotest.com
tech_email       = tech@zohotest.com
test_user_emails = 
password         = yourpassword
drivers_path     = /home/you/Automater/Drivers
```

A legend explaining each key is shown below the form. Just fill in the values, copy the block, and paste it back.

For **Reconfigure** mode, the form is shorter — no hg credentials needed:

```
owner            = 3
deps_path        = /home/you/Automater/dependencies
sdp_url          = https://sdpodqa-auto1.csez.zohocorpin.com:9090/
portal           = portal1
admin_email      = admin@zohotest.com
tech_email       = tech@zohotest.com
test_user_emails = 
password         = yourpassword
drivers_path     = /home/you/Automater/Drivers
```

The agent auto-detects which project folder to use. If multiple project folders exist, it asks you to pick one.

> **Existing folder handling**: If you choose mode 1 or 2 and a project folder already exists, the agent asks what to do: *Pull & Update*, *Delete & Re-clone*, or *Use as-is*. It never silently reuses an old folder.

> **Fresh session**: Every time you run `@setup-project setup`, it starts completely fresh — it never picks up leftover values from a previous run.

> **Security note**: Your hg password is **never typed in the chat**. When the agent clones the repository, Mercurial prompts you for your password directly in the VS Code terminal.

The agent handles everything else: cloning the Mercurial branch (prompts for hg password in the terminal), compiling framework classes, writing `.env`, creating the `Testcase/` folder.

> **New team member?** Select `new` as your owner. The agent asks for your full name and Zoho Corp ID, then registers you automatically.

---

## Step 3 — Prepare Your Use-Case Document

Test generation starts with a **use-case document in CSV format**. This is the primary and recommended input method.

### CSV format

Use the template at `docs/templates/usecase_template.csv`:

| UseCase ID | Severity | Module | Sub-Module | Impact Area | Pre-Requisite | Description | UI To-be-automated |
|---|---|---|---|---|---|---|---|
| SDPOD_CH_001 | Critical | Changes | Change Detail View | Navigate to change detail page | SDAdmin, change exists | Verify change title and status display correctly in detail view | Yes |
| SDPOD_CH_002 | Major | Changes | Change Notes | Add note to change | SDAdmin, change exists | Add a note to a change and verify it appears in the Notes tab | Yes |
| SDPOD_CH_003 | Minor | Changes | Change Detail View | Spot edit priority field | SDAdmin, change exists | Verify the priority field is editable via spot edit | Yes |
| SDPOD_CH_API_004 | Major | API | Change Validation | Create change via API | Two changes exist | POST /api/v3/changes and verify response | No |

**Columns explained:**

| Column | Required? | What it controls |
|--------|-----------|------------------|
| **UseCase ID** | Yes | Links back to your use case — mapped as test scenario ID reference |
| **Severity** | Yes | Maps to test priority: `Critical` → HIGH, `Major` → MEDIUM, `Minor` → LOW |
| **Module** | Yes | Parent module (e.g., `Admin`, `CMDB`, `Changes`, `Requests`). For cross-cutting concerns (`RBAC`, `Security`, `API`), routes to the actual entity identified by Sub-Module |
| **Sub-Module** | Yes | Entity subclass routing (e.g., `Sub Form Configuration`, `CI Details - Sub Form`). If no matching subclass exists, the agent creates one or uses nearest match |
| **Impact Area** | Yes | What area/feature is being tested — cumulated with Pre-Requisite + Description |
| **Pre-Requisite** | Yes | What must exist before the test (drives `preProcess` group and role selection) |
| **Description** | Yes | Scenario steps and expected results — cumulated with Impact Area + Pre-Requisite for full context |
| **UI To-be-automated** | Yes | Filter gate — only rows with `Yes` are processed; `No`/empty rows are skipped |

> **Tip**: The use case can be in **any sheet** in the workbook — all sheets are processed. Only rows with `UI To-be-automated = Yes` are picked for automation. Extra columns beyond the 8 above are ignored.

### Where to place the CSV

Put your CSV file in the project's `Testcase/` folder:

```
<PROJECT_NAME>/
└── Testcase/
    └── my_use_cases.csv       ← place your file here
```

> `<PROJECT_NAME>` is the branch folder created by `@setup-project` (e.g. `SDPLIVE_LATEST_AUTOMATER_SELENIUM`). Check your `.env` for the exact name.

This folder was created by `@setup-project`. If it doesn't exist, create it:
```bash
mkdir -p <PROJECT_NAME>/Testcase
```

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
<PROJECT_NAME>/reports/LOCAL_<methodName>_<timestamp>/ScenarioReport.html
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
| Reconfigure existing project | `@setup-project setup` → choose mode 3 |
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
| Already cloned, just need to configure | Use `@setup-project setup` → choose mode 3 (Reconfigure) |
| Switched SDP instance | Use `@setup-project setup` → mode 3 to update URL + credentials |
| `Testcase/` folder missing | `mkdir -p <PROJECT_NAME>/Testcase` (replace with your branch name from `.env`) |
| Generated test fails on first run | Normal — `@test-runner` auto-diagnoses and fixes. Run `@test-runner batch` |

---
### Alternative: plain-text description

For quick one-off scenarios, you can skip the CSV and just describe what you want:

```
@test-generator Create an incident request, add a note, and verify it appears in the Notes tab
```

This works well for 1-3 scenarios. For larger batches, CSV is strongly recommended.

---

## Multi-Project Targeting

If you have multiple test-case branches cloned, you can specify which project a command targets:

```
@test-generator project=SDPLIVE_UI_AUTOMATION_BRANCH create a change and verify the detail view
```

If not specified, the agent uses the default `PROJECT_NAME` from your `.env` configuration.

> **Tip**: Use `@setup-project setup` → mode 3 (Reconfigure) to switch your default project without re-cloning.

---

## Why VS Code + GitHub Copilot (Claude) Is Required

This framework's agent workflow (`@setup-project`, `@test-generator`, `@test-runner`) relies on **VS Code Agent mode** — a feature exclusive to VS Code's GitHub Copilot extension. No other IDE supports it today.

### What Agent mode provides (and why alternatives won't work)

| Capability | Used by our agents | Available in VS Code | Eclipse / IntelliJ Copilot |
|---|---|---|---|
| **`@agent-name` invocation** | `@setup-project`, `@test-generator`, `@test-runner` | Yes | No |
| **`.agent.md` files** | Agent definitions with YAML frontmatter (tools, model, instructions) | Yes | No |
| **Tool use** (file read/edit, terminal, search) | Agents read Java files, edit code, run `javac`, execute tests | Yes | No |
| **MCP tools** (Playwright browser) | `@test-runner` opens SDP pages to inspect/fix XPath locators | Yes | No |
| **`.github/instructions/` auto-loading** | Framework rules and conventions injected per file context | Yes | No |
| **Model selection** (Claude Opus 4.6 / Sonnet 4) | Agents specify which LLM to use in YAML frontmatter | Yes | No |
| **Code completions** | General autocomplete (not used by our agents) | Yes | Yes |

### What about other IDEs?

- **Eclipse + Copilot**: Only supports code completions. No chat agent mode, no tool use, no `.agent.md` support.
- **IntelliJ + Copilot**: Supports Copilot Chat but **not** Agent mode with custom `.agent.md` files or MCP tools.
- **Cursor / Windsurf**: Have their own agent systems but use different file formats — our `.agent.md` files are VS Code-specific.

### Can I use Eclipse for other work?

Yes. You can use **Eclipse for regular Java development** and **VS Code only for the agent-driven test generation workflow**. Both can point to the same project folder — they don't conflict. The typical dual-IDE workflow:

1. Open the project in **VS Code** → run `@setup-project`, `@test-generator`, `@test-runner`
2. Open the same project in **Eclipse** → review generated code, make manual edits, commit to hg

### Minimum VS Code requirements

| Requirement | Minimum version |
|---|---|
| VS Code | 1.99+ (Agent mode was introduced in 1.99) |
| GitHub Copilot extension | Latest (includes Agent mode + MCP support) |
| GitHub Copilot Chat extension | Latest |
| Copilot plan | GitHub Copilot Individual, Business, or Enterprise (Agent mode requires an active subscription) |

### Minimum model requirements

The agents in this framework specify their model requirements in `.agent.md` YAML frontmatter. The following models are supported and tested:

| Model | Required for | Why |
|---|---|---|
| **Claude Opus 4.6** | `@test-generator`, `@test-debugger`, `@setup-project` | Complex multi-step code generation, debugging, and tool orchestration — needs the strongest reasoning |
| **Claude Sonnet 4.6** | `@test-generator`, `@test-debugger`, `@setup-project` | Acceptable alternative — faster but slightly less accurate on complex entity scaffolding |
| **Claude Sonnet 4** | `@test-runner` | Sufficient for compile → run → fix loops that don't require deep code generation |

> **How models are selected**: Each `.agent.md` file has a `model:` field listing acceptable models in priority order. VS Code uses the first available model from the list. You can override the model per-conversation via the model picker dropdown in Copilot Chat.
>
> **Minimum recommended**: Claude Sonnet 4.6 or higher. Older models (GPT-4o, Claude 3.5 Sonnet) are **not tested** and may produce incorrect Java code, miss framework conventions, or fail to use tools correctly.
>
> **Model availability**: Depends on your GitHub Copilot plan and region. If a specific model is unavailable, the agent falls back to the next model in its list.

> **To verify**: Open VS Code → Copilot Chat → click the model picker dropdown. You should see Claude Opus 4.6 and/or Claude Sonnet 4.6 in the list.
