---
# VS Code 1.111: Agent-scoped hook (Preview)
# Runs BEFORE the test-generator agent starts processing.
# Validates project structure and ensures prerequisites are met.
event: preSend
agents: [test-generator]
---

## Pre-Generation Validation

Before generating any test code, verify:

1. **Project folder exists** — The active `PROJECT_NAME` from `.env` must have a valid `src/` directory
2. **Constants are up-to-date** — If any `*_data.json` was recently modified, run `./generate_constants.sh` to regenerate DataConstants
3. **Framework is compiled** — Check that `bin/` contains framework classes (run `./setup_framework_bin.sh` if missing)
4. **Use-case document exists in `{PROJECT}/Testcase/`** — This is a MANDATORY hard gate:
   - The document must physically exist in `{PROJECT}/Testcase/` (`.csv`, `.xlsx`, `.xls`, `.md`, or `.txt`)
   - The USER must have placed the document there themselves
   - Do NOT copy documents from `docs/UseCase/`, `docs/Feature_Document/`, `web/uploads/`, or any other location into `Testcase/`
   - Do NOT generate, synthesize, or fabricate use-case documents
   - If `Testcase/` is empty and the user did not provide a concrete scenario description, STOP and prompt the user to upload their document

If any check fails, inform the user and stop — do not generate partial code.
