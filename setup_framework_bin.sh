#!/usr/bin/env bash
# =============================================================================
# setup_framework_bin.sh
#
# Compiles AutomaterSeleniumFramework source (branch: AI_Automation_Code_Generator)
# into SDPLIVE_LATEST_AUTOMATER_SELENIUM/bin/ so the AI-fixed local-run classes
# override the old AutomationFrameWork.jar at runtime.
#
# Run this once after:
#   - A fresh clone / machine setup
#   - Pulling updates to AutomaterSeleniumFramework
#   - Switching the framework hg branch
#
# Usage:
#   ./setup_framework_bin.sh
# =============================================================================

set -e

WORKSPACE="$(cd "$(dirname "$0")" && pwd)"
FW_SRC="$WORKSPACE/AutomaterSeleniumFramework/src"
# Resolve PROJECT_NAME via Python (reads .env → os.environ fallback)
if [ -f "$WORKSPACE/.env" ]; then
  _PN=$(grep -E '^PROJECT_NAME\s*=' "$WORKSPACE/.env" | sed 's/^PROJECT_NAME\s*=\s*//' | tr -d '"'"'"' ')
fi
if [ -z "$_PN" ]; then
  _PN=$(cd "$WORKSPACE" && python3 -c "from config.project_config import PROJECT_NAME; print(PROJECT_NAME)" 2>/dev/null)
fi
PROJECT_NAME="$_PN"
if [ -z "$PROJECT_NAME" ]; then
  echo "❌ Could not read PROJECT_NAME from .env or config/project_config.py"
  exit 1
fi

# Read DEPS_DIR from .env (set by @setup-project agent)
if [ -f "$WORKSPACE/.env" ]; then
  DEPS=$(grep -E '^DEPS_DIR\s*=' "$WORKSPACE/.env" | sed 's/^DEPS_DIR\s*=\s*//' | tr -d '"'"'"' ')
fi
if [ -z "$DEPS" ] || [ ! -d "$DEPS" ]; then
  echo "❌ DEPS_DIR not set or directory not found."
  echo "   Set it in .env (e.g., DEPS_DIR=/home/you/dependencies)"
  echo "   or run '@setup-project setup' to configure it."
  exit 1
fi

BIN="$WORKSPACE/$PROJECT_NAME/bin"
FW_DIR="$WORKSPACE/AutomaterSeleniumFramework"
TARGET_BRANCH="AI_Automation_Code_Generator"

echo "======================================================"
echo "  AutomaterSeleniumFramework  →  SDPLIVE bin/ compiler"
echo "======================================================"

# ── 0. Check hg-managed folders exist (gitignored — must be cloned via hg) ───
if [ ! -d "$WORKSPACE/$PROJECT_NAME" ]; then
  echo "❌ $PROJECT_NAME/ not found."
  echo "   This folder is managed via Mercurial (hg) and is NOT included in the git clone."
  echo "   Clone it with:"
  echo "     cd $WORKSPACE"
  echo "     hg clone <repo-url> $PROJECT_NAME"
  echo ""
  echo "⚠️  Please clone the test-case repo above, then re-run this script."
  exit 1
fi

if [ ! -d "$BIN" ]; then
  echo "❌ bin/ directory not found at: $BIN"
  exit 1
fi

# Check if framework source is available (optional — only maintainers have this)
HAS_FRAMEWORK=false
if [ -d "$WORKSPACE/AutomaterSeleniumFramework" ]; then
  if [ -d "$FW_SRC" ]; then
    HAS_FRAMEWORK=true
    echo "✅ Framework source found"
  fi
else
  echo "ℹ️  AutomaterSeleniumFramework/ not present — will use pre-compiled classes from bin/"
fi

if [ ! -d "$DEPS" ]; then
  echo "❌ Dependencies directory not found: $DEPS"
  exit 1
fi
echo "✅ Paths OK"

# ── 2. Check / switch hg branch (only if framework source is present) ─────────
if [ "$HAS_FRAMEWORK" = true ]; then
  CURRENT_BRANCH=$(cd "$FW_DIR" && hg branch 2>/dev/null)
  if [ "$CURRENT_BRANCH" != "$TARGET_BRANCH" ]; then
    echo "⚠️  Framework is on branch '$CURRENT_BRANCH', switching to '$TARGET_BRANCH'..."
    cd "$FW_DIR" && hg update "$TARGET_BRANCH"
    echo "✅ Switched to $TARGET_BRANCH"
  else
    echo "✅ Framework branch: $TARGET_BRANCH"
  fi

  # ── 3. Build classpath (all JARs under dependencies/ recursively) ───────────
  CP="$BIN:$(find "$DEPS" -name "*.jar" | tr '\n' ':')"

  # ── 4. Collect source files — exclude Aalam-only BeforeAndAfterCaseActions ──
  SOURCES_FILE=$(mktemp /tmp/fw_sources_XXXXXX.txt)
  find "$FW_SRC" -name "*.java" | grep -v "BeforeAndAfterCaseActions" > "$SOURCES_FILE"
  FILE_COUNT=$(wc -l < "$SOURCES_FILE")
  echo "📂 Source files to compile: $FILE_COUNT"

  # ── 5. Compile ──────────────────────────────────────────────────────────────
  echo "⚙️  Compiling..."
  if javac -encoding UTF-8 -cp "$CP" -d "$BIN" @"$SOURCES_FILE" 2>&1 | grep "error:"; then
    echo "❌ Compile FAILED — see errors above"
    rm -f "$SOURCES_FILE"
    exit 1
  fi
  rm -f "$SOURCES_FILE"

  # ── 6. Spot-check key classes ───────────────────────────────────────────────
  echo ""
  echo "🔍 Verifying key classes in bin/..."
  MISSING=0
  for cls in \
    "com/zoho/automater/selenium/base/EntityCase.class" \
    "com/zoho/automater/selenium/base/Entity.class" \
    "com/zoho/automater/selenium/base/report/ScenarioReport.class" \
    "com/zoho/automater/selenium/base/standalone/LocalSetupManager.class" \
    "com/zoho/automater/selenium/base/standalone/LocalFailureTemplates.class" \
    "com/zoho/automater/selenium/base/utils/DriverUtil.class"
  do
    if [ -f "$BIN/$cls" ]; then
      echo "  ✅ $cls"
    else
      echo "  ❌ MISSING: $cls"
      MISSING=$((MISSING + 1))
    fi
  done

  echo ""
  if [ "$MISSING" -eq 0 ]; then
    echo "✅ Framework compiled successfully into $PROJECT_NAME/bin/"
    echo "   $(find "$BIN/com/zoho/automater/selenium/base" -name "*.class" | wc -l) framework classes total"
  else
    echo "❌ $MISSING expected class(es) missing — compile may have partially failed"
    exit 1
  fi

else
  # ── No framework source — check if pre-compiled classes already exist ───────
  echo ""
  echo "🔍 Checking for pre-compiled framework classes in $PROJECT_NAME/bin/..."
  KEY_CLASS="$BIN/com/zoho/automater/selenium/base/EntityCase.class"
  if [ -f "$KEY_CLASS" ]; then
    FW_CLASS_COUNT=$(find "$BIN/com/zoho/automater/selenium/base" -name "*.class" 2>/dev/null | wc -l)
    echo "✅ Found $FW_CLASS_COUNT pre-compiled framework classes in bin/"
    echo "   Tests will use these classes + the framework JAR from dependencies."
    echo ""
    echo "ℹ️  If you need the latest framework source overrides (local-run report fixes),"
    echo "   ask the framework maintainer to push the compiled classes to the hg branch,"
    echo "   or clone AutomaterSeleniumFramework/ and re-run this script."
  else
    echo "⚠️  No pre-compiled framework classes found in bin/"
    echo "   Tests will rely on AutomationFrameWork.jar from dependencies."
    echo "   Local-run HTML reports may not generate correctly (missing isLocalSetup guard)."
    echo ""
    echo "   To fix: clone AutomaterSeleniumFramework/ and re-run this script."
  fi
fi
