---
# VS Code 1.111: Agent-scoped hook (Preview)
# Runs BEFORE the test-runner agent starts processing.
# Ensures the environment is ready to execute tests.
event: preSend
agents: [test-runner]
---

## Pre-Run Environment Validation

Before running any test, verify:

1. **Framework compiled** — `bin/` must contain `EntityCase.class`, `ScenarioReport.class`, `LocalSetupManager.class`. If missing, run `./setup_framework_bin.sh`
2. **SDP connectivity** — The SDP instance at `SDP_URL` must be reachable (a quick curl check)
3. **ENTITY_IMPORT_MAP** — The target `entity_class` must exist in `agents/runner_agent.py`'s `ENTITY_IMPORT_MAP`. If missing, add the FQCN entry before running
4. **Orchestrator** — Start the orchestrator server (`./orchestrator.sh start`) for logging test results

If framework bin is stale or missing, compile it first — do not proceed with a broken classpath.
