# AI Automation Code Generator — User Setup Guide

> Give use-case documents to Copilot agents → get fully generated Selenium test code.

---

## 3 Steps — That's It

```
  1. Setup       →   @setup-project setup         →   Project ready
  2. Generate    →   @test-generator               →   Java tests generated
  3. Run         →   @test-runner batch             →   Tests executed & auto-fixed
```

---

## Before You Start

1. Install [VS Code](https://code.visualstudio.com/) with **GitHub Copilot** + **Copilot Chat** extensions (v1.99+)
2. Download **Dependencies** and **Drivers** (Firefox + Geckodriver) zip files from [WorkDrive](https://workdrive.zoho.in/folder/l5o5d7049285d45dd49ae80d7be1a209a6841)

Open VS Code, then open the **Terminal** (`Ctrl+\``) and run:

```bash
sudo apt install openjdk-17-jdk git mercurial python3 python3-venv
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

Now open this folder in VS Code: **File → Open Folder** → select `AI_AUTOMATION_CODE_GENERATOR`

---

## Step 2 — Run Setup Agent

1. Open **Copilot Chat** (`Ctrl+Shift+I`)
2. Switch to **Agent mode** (dropdown at top)
3. Type: **`@setup-project setup`**

The agent walks you through everything:
- Picks your **mode**: Generate only (1), Generate and Run (2), or Reconfigure (3)
- Shows a **form** — fill in your values and paste it back
- Clones the hg branch, compiles framework, writes config

> **New team member?** Pick `new` as owner — the agent registers you automatically.
>
> **Already cloned?** Choose mode 3 (Reconfigure) to just update credentials/URL.
>
> **Password security**: hg password is entered in the terminal, never in chat.

---

## Step 3 — Generate & Run Tests

### From a use-case document (recommended for batches)

1. Place your file (`.csv`, `.xlsx`, or `.xls`) in `<PROJECT_NAME>/Testcase/` (template: `docs/templates/usecase_template.csv`)
2. In Copilot Chat: **`@test-generator`** — it detects the document automatically (`.xlsx`/`.xls` files are auto-converted to CSV)
3. Review the plan, reply `all` to generate

> Only rows with `UI To-be-automated = Yes` are processed.

### From a description (quick one-offs)

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
| Setup | `@setup-project setup` |
| Reconfigure | `@setup-project setup` → mode 3 |
| Generate from use-case doc | Place file in `Testcase/`, then `@test-generator` |
| Generate from text | `@test-generator <description>` |
| Run all tests | `@test-runner batch` |
| Run one test | `@test-runner Entity.methodName` |
| Debug a failure | `@test-debugger <test ID> <error>` |
| Recompile framework | `./setup_framework_bin.sh` |
| Start dashboard | `./orchestrator.sh start` → `http://localhost:9600` |

---

## Common Fixes

| Problem | Fix |
|---------|-----|
| VPN / connection errors | Connect to Zoho VPN first |
| `NullPointerException` in test | `./setup_framework_bin.sh` |
| `Testcase/` folder missing | `mkdir -p <PROJECT_NAME>/Testcase` |
| Test fails on first run | Normal — `@test-runner` auto-fixes and reruns |
| Wrong project targeted | `@test-generator project=BRANCH_NAME` |
| Need to switch SDP instance | `@setup-project setup` → mode 3 |

---

> **Why VS Code?** The `@agent` workflow requires VS Code Agent mode (1.99+) — Eclipse and IntelliJ don't support it. You can still use Eclipse for regular Java work alongside VS Code for test generation.
