---
# VS Code 1.111: Agent-scoped hook (replaces post-java-edit.json)
# Triggers after any tool use that edits a .java file.
# Scoped to test-generator and test-debugger only — setup-project doesn't edit Java.
event: postToolUse
agents: [test-generator, test-runner, test-debugger]
---

## Post Java Edit — Compilation Reminder

When a `.java` file is edited (via `replace_string_in_file`, `create_file`, or `multi_replace_string_in_file`):

1. **Queue targeted compilation** — Add the modified file to the compile list
2. **NEVER full project compile** — Full compile has 67+ pre-existing errors. Only compile the changed files and their direct dependencies (Locators, Constants, Base classes)
3. **Include dependencies recursively** — `find "$DEPS" -name "*.jar"` must scan subdirectories (e.g., `dependencies/framework/` has critical JARs)

Compilation command template:
```bash
DEPS=$(.venv/bin/python -c "from config.project_config import DEPS_DIR; print(DEPS_DIR)")
BIN=$(.venv/bin/python -c "from config.project_config import PROJECT_ROOT, PROJECT_NAME; print(PROJECT_ROOT + '/' + PROJECT_NAME + '/bin')")
SRC=$(.venv/bin/python -c "from config.project_config import PROJECT_ROOT, PROJECT_NAME; print(PROJECT_ROOT + '/' + PROJECT_NAME + '/src')")
CP="$BIN:$(find "$DEPS" -name "*.jar" | tr '\n' ':')"
javac -encoding UTF-8 -cp "$CP" -d "$BIN" <changed .java files>
```
