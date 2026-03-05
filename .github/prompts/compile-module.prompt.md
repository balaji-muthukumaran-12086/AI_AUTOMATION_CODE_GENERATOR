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
DEPS=/home/balaji-12086/Desktop/Workspace/Zide/dependencies
BIN=/home/balaji-12086/Desktop/Workspace/Zide/ai-automation-qa/SDPLIVE_LATEST_AUTOMATER_SELENIUM/bin
SRC=/home/balaji-12086/Desktop/Workspace/Zide/ai-automation-qa/SDPLIVE_LATEST_AUTOMATER_SELENIUM/src
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
