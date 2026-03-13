---
# VS Code 1.111: Agent-scoped hook (Preview)
# Runs AFTER the test-runner agent completes a response.
# Handles result logging and cleanup.
event: postSend
agents: [test-runner]
---

## Post-Run Cleanup & Reporting

After every test execution (pass or fail):

1. **Log to orchestrator** — Report the scenario result via `orchestrator.client`:
   ```python
   from orchestrator.client import get_client
   oc = get_client()
   oc.scenario_passed(scenario_id='ID', method_name='method', module='module')  # or scenario_failed(...)
   ```
2. **Cleanup Playwright data** — If Playwright MCP was used for debugging, delete all entities created via `sdpAPICall()` during the session
3. **Update batch results** — If in batch mode, write results to `batch_run_results.json`
4. **ScenarioReport check** — Verify `ScenarioReport.html` exists in the report directory. If missing after a reported PASS, flag it as suspicious

Never leave test data behind in the SDP instance after a debugging session.
