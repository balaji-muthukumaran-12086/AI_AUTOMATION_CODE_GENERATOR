# Setup Guide

## Prerequisites

| Tool | Install |
|------|---------|
| Python 3.10+ | `python3 --version` |
| Java JDK 17 | `java -version` / `sudo apt install openjdk-17-jdk` |
| Git | `git --version` |
| Mercurial | `hg --version` / `sudo apt install mercurial` |
| Firefox + Geckodriver | Needed only for test execution (Generate and Run mode) |
| VS Code + GitHub Copilot | With Agent mode enabled |

> **VPN**: Connect to Zoho VPN (`vpn.zohocorporation.com:10443`) before any step that touches the hg repo or SDP instance.

---

## Step 1 — Clone & Create Virtual Environment

```bash
git clone https://github.com/balaji-muthukumaran-12086/AI_AUTOMATION_CODE_GENERATOR.git
cd AI_AUTOMATION_CODE_GENERATOR
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Step 2 — Run the Setup Agent

1. Open the project in VS Code
2. Open **Copilot Chat** → switch to **Agent mode**
3. Type: `@setup-project setup`

The agent asks your usage mode:

- **Generate only** — generate Java test code, no SDP credentials needed
- **Generate and Run** — generate AND execute against a live SDP instance

Then it shows a **numbered owner list** (read from `OwnerConstants.java`) and presents a form. Pick your number from the list, or enter `new` if you're not listed.

**Generate only** (5 fields):
```
owner        = <number or "new">
hg_username  = 
hg_password  = 
branch       = SDPLIVE_LATEST_AUTOMATER_SELENIUM
deps_path    = 
```

**Generate and Run** (11 fields):
```
owner        = <number or "new">
hg_username  = 
hg_password  = 
branch       = SDPLIVE_LATEST_AUTOMATER_SELENIUM
deps_path    = 

sdp_url      = 
portal       = 
admin_email  = 
tech_email   = 
password     = 
drivers_path = 
```

| Field | Example |
|-------|---------|
| `owner` | Number from the list, or `new` for new team members |
| `hg_username` | Your zrepository username |
| `hg_password` | Your zrepository password (not stored in any file) |
| `branch` | Hg branch to clone (default pre-filled) |
| `deps_path` | Absolute path to the Java JARs folder |
| `sdp_url` | `https://sdpodqa-auto1.csez.zohocorpin.com:9090/` |
| `portal` | `portal1` |
| `admin_email` | Org admin email |
| `tech_email` | Technician / scenario user email |
| `password` | Common password for SDP accounts |
| `drivers_path` | Absolute path to folder with `firefox/firefox` and `geckodriver` |

If you select `new`, the agent asks for your **full name** and **Zoho Corp ID**, then registers you in `OwnerConstants.java` automatically.

The agent will: clone the hg branch, set your owner, write `.env`, update `config/project_config.py`, and compile the framework.

---

## Step 3 — Manual Setup (Alternative)

Skip this if you used the setup agent in Step 2.

```bash
cp .env.example .env
```

Fill in `.env`:
```env
DEPS_DIR=/absolute/path/to/dependencies
HG_USERNAME=your-zrepo-username
OWNER_CONSTANT=BALAJI_M
# For Generate and Run mode only:
SDP_URL=https://...
SDP_PORTAL=portal1
SDP_ADMIN_EMAIL=admin@zohotest.com
SDP_EMAIL_ID=tech@zohotest.com
SDP_ADMIN_PASS=yourpassword
DRIVERS_DIR=/absolute/path/to/Drivers
```

Clone the test-case branch:
```bash
hg clone -b SDPLIVE_LATEST_AUTOMATER_SELENIUM \
  https://USERNAME:PASSWORD@zrepository.zohocorpcloud.in/zohocorp/Automater/AutomaterSelenium \
  SDPLIVE_LATEST_AUTOMATER_SELENIUM
```

Compile the framework:
```bash
./setup_framework_bin.sh
```

---

## Dependencies Folder

Get the `dependencies/` folder from a team member or existing workstation. It contains all Selenium and framework JARs:

```
dependencies/
├── framework/              # AutomationFrameWork.jar + sub-JARs
├── selenium-server-*.jar
├── commons-lang3-*.jar
├── gson-*.jar
└── ... (other JARs)
```

The build script and runner recursively scan this entire folder (including `framework/`), so all JARs are automatically included in the classpath.

---

## Verify

```bash
# Check framework compiled correctly (should see .class files)
ls SDPLIVE_LATEST_AUTOMATER_SELENIUM/bin/com/zoho/automater/selenium/base/Entity.class

# Run an existing test (Generate and Run mode only)
source .venv/bin/activate
python3 run_test.py 2>&1
```

Reports appear at: `SDPLIVE_LATEST_AUTOMATER_SELENIUM/reports/LOCAL_<method>_<timestamp>/ScenarioReport.html`

---

## Generating Tests — `@test-generator`

1. Open **Copilot Chat** → **Agent mode**
2. Provide the use case in one of these ways:
   - **Type a description**: `@test-generator Create an incident request, add a note, and verify it appears in the notes tab`
   - **Attach a document**: Drag a `.md`, `.txt`, `.xls`, `.xlsx`, or `.csv` file into the chat and type `@test-generator`
   - **Use-case docs folder**: Place documents in `docs/UseCase/` or `docs/Feature_Document/` for reference

The agent will:
- Read framework rules and knowledge files
- Analyze the use case and identify the correct module/entity
- Check existing data entries and reuse where possible
- Generate Java test code (annotation wrapper + base implementation + data JSON + constants)
- Output code blocks with `// ===== ADD TO: <filename> =====` markers

> **Tip**: For best results, be specific about what module (requests, solutions, changes, etc.) and what actions (create, edit, verify, add notes, etc.) the test should cover.

---

## Debugging Tests — `@test-debugger`

1. Open **Copilot Chat** → **Agent mode**
2. Describe the failure: `@test-debugger SDPOD_AUTO_SOL_DV_243 fails with NoSuchElementException on the approval button`

The agent can:
- Analyze `ScenarioReport.html` failures and screenshots
- Inspect SDP UI elements using the browser (Playwright MCP)
- Create prerequisite test data via `sdpAPICall()` to reach the correct UI state
- Fix broken XPath locators
- Investigate `NullPointerException` and API response issues

> **Tip**: Include the test ID, error type, and any relevant log output for faster diagnosis.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `javac: command not found` | `sudo apt install openjdk-17-jdk` |
| `hg: command not found` | `sudo apt install mercurial` |
| `NullPointerException` in test | Run `./setup_framework_bin.sh` |
| VPN / connection errors | Connect to Zoho VPN first |
| `BUILD FAILED` | Use targeted compile — full project compile is broken (see `copilot-instructions.md`) |
| `OWNER_CONSTANT` empty | Re-run `@setup-project setup` |
