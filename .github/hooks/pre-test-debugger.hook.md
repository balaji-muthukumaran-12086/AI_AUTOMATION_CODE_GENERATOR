---
# VS Code 1.111: Agent-scoped hook (Preview)
# Runs BEFORE the test-debugger agent starts processing.
# Ensures failure context is available before debugging begins.
event: preSend
agents: [test-debugger]
---

## Pre-Debug Context Collection

Before starting any debug investigation:

1. **Locate the latest report** — Find `ScenarioReport.html` from the most recent test run:
   ```bash
   PROJECT=$(.venv/bin/python -c "from config.project_config import PROJECT_ROOT; print(PROJECT_ROOT)")
   ls -dt "$PROJECT"/reports/LOCAL_* | head -1
   ```
2. **Verify SDP session** — The browser must be on a logged-in SDP page for Playwright MCP tools and `sdpAPICall()` to work
3. **Read the failure** — Parse ScenarioReport.html for the exact failure step and exception type BEFORE opening Playwright

Do NOT read Java source files as the first step. The ScenarioReport is the starting point for every debug investigation.
