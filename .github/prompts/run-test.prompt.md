---
description: "Run a specific test method via run_test.py. Updates RUN_CONFIG and executes."
agent: "agent"
argument-hint: "Entity class and method name, e.g. 'ChangeDetailsView.attachParentChangeAndVerifyAssociation'"
tools: [execute, read, edit]
---

Run a specific Selenium test method using the framework's runner.

## Steps

1. Parse the user input to extract `entity_class` and `method_name` (format: `EntityClass.methodName`)
2. Update `run_test.py` with the correct `RUN_CONFIG`:
   ```python
   RUN_CONFIG = {
       "entity_class":  "{EntityClass}",
       "method_name":   "{methodName}",
       "url":           SDP_URL,
       "admin_mail_id": SDP_ADMIN_EMAIL,
       "email_id":      SDP_EMAIL_ID,
       "portal_name":   SDP_PORTAL,
       "password":      SDP_ADMIN_PASS,
       "skip_compile":  True,
   }
   ```
3. Verify `entity_class` exists in `ENTITY_IMPORT_MAP` in `agents/runner_agent.py` — add if missing
4. Run:
   ```bash
   cd /home/balaji-12086/Desktop/Workspace/Zide/ai-automation-qa
   .venv/bin/python run_test.py 2>&1
   ```
5. Check the output for PASS/FAIL:
   - `$$Failure` → FAILED
   - `"successfully"` in Additional Specific Info → PASSED
   - `BUILD SUCCESSFUL` → PASSED
   - Java exceptions → FAILED
6. Report location: `SDPLIVE_LATEST_AUTOMATER_SELENIUM/reports/LOCAL_{method}_{timestamp}/ScenarioReport.html`
