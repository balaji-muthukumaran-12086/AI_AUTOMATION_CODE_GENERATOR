---
# VS Code 1.111: Agent-scoped hook (Preview)
# Runs AFTER the test-generator agent completes a response.
# Ensures generated code is compilable and constants are synced.
event: postSend
agents: [test-generator]
---

## Post-Generation Checks

After generating test code, always perform these steps:

1. **Regenerate DataConstants** — Run `./generate_constants.sh` if any `*_data.json` entry was added or modified
2. **Targeted compilation** — Compile only the changed module files (NEVER full project):
   ```bash
   DEPS=$(.venv/bin/python -c "from config.project_config import DEPS_DIR; print(DEPS_DIR)")
   BIN=$(.venv/bin/python -c "from config.project_config import PROJECT_ROOT, PROJECT_NAME; print(PROJECT_ROOT + '/' + PROJECT_NAME + '/bin')")
   SRC=$(.venv/bin/python -c "from config.project_config import PROJECT_ROOT, PROJECT_NAME; print(PROJECT_ROOT + '/' + PROJECT_NAME + '/src')")
   CP="$BIN:$(find "$DEPS" -name "*.jar" | tr '\n' ':')"
   javac -encoding UTF-8 -cp "$CP" -d "$BIN" <changed .java files>
   ```
3. **Update `$PROJECT_NAME/tests_to_run.json`** — If batch mode, append the newly generated test entry
4. **Report compilation result** — If compile fails, show the error and fix it before yielding

Do NOT skip compilation. A generated test that doesn't compile is not a valid deliverable.
