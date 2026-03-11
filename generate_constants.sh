#!/usr/bin/env bash
# generate_constants.sh — Run AutoGenerateConstantFiles.main() to regenerate
# *DataConstants.java, *Fields.java, and *Role.java from resource JSON files.
#
# Equivalent to the Eclipse Ant builder that triggers on save of data/conf/role JSON.
# Usage:
#   ./generate_constants.sh            # auto-detect from project_config.py
#   ./generate_constants.sh <file>     # touch file first so it's the "most recently modified"
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# Derive paths from project_config.py (single source of truth)
PROJECT_NAME=$(.venv/bin/python -c "from config.project_config import PROJECT_NAME; print(PROJECT_NAME)")
DEPS_DIR=$(.venv/bin/python -c "from config.project_config import DEPS_DIR; print(DEPS_DIR)")
BIN_DIR="$SCRIPT_DIR/$PROJECT_NAME/bin"

# If a specific file was passed, touch it so it becomes the "most recently modified"
if [[ $# -ge 1 && -f "$1" ]]; then
    touch "$1"
    echo "[generate_constants] Touched: $1"
fi

# Build classpath: bin/ + all JARs in deps
CP="$BIN_DIR"
while IFS= read -r jar; do
    CP="$CP:$jar"
done < <(find "$DEPS_DIR" -name "*.jar" 2>/dev/null)

echo "[generate_constants] Running AutoGenerateConstantFiles.main()..."
java -cp "$CP" com.zoho.automater.selenium.standalone.AutoGenerateConstantFiles

echo "[generate_constants] Done."
