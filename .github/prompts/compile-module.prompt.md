---
description: "Compile Java test module source files after editing. Targeted compilation only — never full project."
agent: "agent"
argument-hint: "Module path, e.g. solutions/solution or changes/change"
tools: [execute, read, search]
---

Compile the specified module's Java source files using targeted compilation.

**CRITICAL**: Full project compile is BROKEN (67+ pre-existing errors). Only compile the specific files that were changed.

## Compilation Command

```bash
# Derive paths from project_config.py (single source of truth — reads .env)
DEPS=$(.venv/bin/python -c "from config.project_config import DEPS_DIR; print(DEPS_DIR)")
BIN=$(.venv/bin/python -c "from config.project_config import PROJECT_ROOT, PROJECT_NAME; print(PROJECT_ROOT + '/' + PROJECT_NAME + '/bin')")
SRC=$(.venv/bin/python -c "from config.project_config import PROJECT_ROOT, PROJECT_NAME; print(PROJECT_ROOT + '/' + PROJECT_NAME + '/src')")
CP="$BIN:$(find "$DEPS" -name "*.jar" | tr '\n' ':')"

javac -encoding UTF-8 -cp "$CP" -d "$BIN" \
  "$SRC/com/zoho/automater/selenium/modules/{MODULE_PATH}/common/{Entity}Locators.java" \
  "$SRC/com/zoho/automater/selenium/modules/{MODULE_PATH}/{Entity}Base.java"
```

Replace `{MODULE_PATH}` and `{Entity}` with the user's target module.

## Steps
1. Identify which `.java` files were recently modified (check git status or ask user)
2. Build the `javac` command with all modified files + their dependencies (Locators, Constants, etc.)
3. Run the command and report success/failure
4. If compilation fails, read the error and fix the Java source
