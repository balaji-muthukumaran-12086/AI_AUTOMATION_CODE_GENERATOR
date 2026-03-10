# AI Test Generator — Team Quick Start Guide

> **URL**: `http://<server-ip>:9500`
> **Max concurrent runs**: 2 (queued runs wait automatically)

---

## How to Submit Test Cases

You have **3 ways** to submit work to the AI test generator:

### 1. Type a single use case (fastest)
1. Open the Web UI
2. Enter your name in **"Your Name"**
3. Type a one-liner in **"Feature Description / Use Cases"**, e.g.:
   ```
   Create an incident request with high priority and verify detail view
   ```
4. Optionally set **Module Hints** (e.g. `requests/request`)
5. Click **⚡ Generate Test Cases**

### 2. Type multiple use cases (batch mode)
Same as above, but enter **one use case per line**:
```
Create a change and verify status in detail view
Add a note to an existing change
Verify history entry when change is updated
Attach a parent change and verify association tab
```

### 3. Upload a document (richest input)
Upload one of these formats: **PDF, DOCX, XLSX, CSV, PPTX, TXT, MD**

For CSV files, use the template format (see `docs/templates/usecase_template.csv`):
```csv
UseCase ID,Severity,Module,Sub-Module,Impact Area,Pre-Requisite,Description,UI To-be-automated
SDPOD_MODULE_001,Critical,Admin,Sub Form Configuration,"Navigate to Sub-form page","Logged in as SDAdmin","Verify Sub-form page loads under Setup > Customization.",Yes
```

> Only rows with `UI To-be-automated = Yes` are picked. The use case can span **any sheet** in the workbook.

---

## Generation Modes

| Mode | When to Use |
|------|-------------|
| **🆕 New Feature** | You're testing a brand new feature (default) |
| **🔍 Gap Fill** | Fill coverage gaps in an existing module's test suite |
| **🔄 Regression** | Regenerate or extend a regression suite |
| **⚡ From Test Cases** | Your CSV/Excel already has structured test cases (skips planning) |

---

## Module Hints

To help the AI target the right module, add a hint. Common module paths:

| Module | Path |
|--------|------|
| Incident Requests | `requests/request` |
| Changes | `changes/change` |
| Problems | `problems/problem` |
| Solutions | `solutions/solution` |
| Releases | `releases/release` |
| Assets | `assets/asset` |
| Projects | `projects/project` |
| Contracts | `contracts/contract` |
| Admin - Workflows | `admin/automation/workflows` |
| Admin - SLA | `admin/sla` |
| Admin - Notifications | `admin/automation/notificationrules` |

---

## Watching Your Run

- The **stage progress bar** shows which pipeline agent is currently working
- The **live log panel** streams real-time output from each agent
- The **header stats** show: active runs / max concurrent, RAM usage, CPU usage
- When your run finishes, you'll get a **browser notification** (allow when prompted)

---

## Run History

- Every run is tracked with your name, status, and duration
- Click any row in the history table to replay its log
- Runs persist across server restarts

---

## What Gets Generated

The pipeline produces:
1. **Java test files** — `@AutomaterScenario` annotated methods in the correct module
2. **Test data JSON** — Input data entries with placeholders
3. **Locator updates** — New XPath locators if needed
4. **DataConstants** — New `TestCaseData` constant declarations

Generated files appear in the **📁 Generated Files** panel with download links.

---

## Tips

- **Be specific** in descriptions — "Create a change with template X and verify status" is better than "test changes"
- **Include expected results** when possible — the AI generates better assertions
- **Use module hints** if auto-detection picks the wrong module
- **Check the queue indicator** (top-right, 🔄 icon) — if both slots are occupied, your run will wait
- **Don't close the tab** during generation — the SSE stream needs an open connection

---

## Supported SDP Build

The test generator targets the SDP build configured in `config/project_config.py`.
If you need tests for a specific feature branch build, coordinate with the admin.

## Need Help?

Contact: Balaji M (AI Automation pipeline owner)
