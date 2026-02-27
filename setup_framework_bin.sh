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
DEPS="$WORKSPACE/../dependencies"
FW_SRC="$WORKSPACE/AutomaterSeleniumFramework/src"
BIN="$WORKSPACE/SDPLIVE_LATEST_AUTOMATER_SELENIUM/bin"
FW_DIR="$WORKSPACE/AutomaterSeleniumFramework"
TARGET_BRANCH="AI_Automation_Code_Generator"

echo "======================================================"
echo "  AutomaterSeleniumFramework  →  SDPLIVE bin/ compiler"
echo "======================================================"

# ── 1. Verify paths exist ─────────────────────────────────────────────────────
for path in "$DEPS" "$FW_SRC" "$BIN"; do
  if [ ! -d "$path" ]; then
    echo "❌ Directory not found: $path"
    exit 1
  fi
done
echo "✅ Paths OK"

# ── 2. Check / switch hg branch ───────────────────────────────────────────────
CURRENT_BRANCH=$(cd "$FW_DIR" && hg branch 2>/dev/null)
if [ "$CURRENT_BRANCH" != "$TARGET_BRANCH" ]; then
  echo "⚠️  Framework is on branch '$CURRENT_BRANCH', switching to '$TARGET_BRANCH'..."
  cd "$FW_DIR" && hg update "$TARGET_BRANCH"
  echo "✅ Switched to $TARGET_BRANCH"
else
  echo "✅ Framework branch: $TARGET_BRANCH"
fi

# ── 3. Build classpath (all JARs under dependencies/ recursively) ─────────────
CP="$BIN:$(find "$DEPS" -name "*.jar" | tr '\n' ':')"

# ── 4. Collect source files — exclude Aalam-only BeforeAndAfterCaseActions ────
SOURCES_FILE=$(mktemp /tmp/fw_sources_XXXXXX.txt)
find "$FW_SRC" -name "*.java" | grep -v "BeforeAndAfterCaseActions" > "$SOURCES_FILE"
FILE_COUNT=$(wc -l < "$SOURCES_FILE")
echo "📂 Source files to compile: $FILE_COUNT"

# ── 5. Compile ────────────────────────────────────────────────────────────────
echo "⚙️  Compiling..."
if javac -encoding UTF-8 -cp "$CP" -d "$BIN" @"$SOURCES_FILE" 2>&1 | grep "error:"; then
  echo "❌ Compile FAILED — see errors above"
  rm -f "$SOURCES_FILE"
  exit 1
fi
rm -f "$SOURCES_FILE"

# ── 6. Spot-check key classes ─────────────────────────────────────────────────
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
  echo "✅ Framework compiled successfully into bin/"
  echo "   $(find "$BIN/com/zoho/automater/selenium/base" -name "*.class" | wc -l) framework classes total"
else
  echo "❌ $MISSING expected class(es) missing — compile may have partially failed"
  exit 1
fi
