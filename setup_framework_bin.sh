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
# Resolve PROJECT_NAME: honour env var if already set (e.g. from breakage_api clone),
# otherwise fall back to .env → project_config.py
if [ -z "$PROJECT_NAME" ]; then
  if [ -f "$WORKSPACE/.env" ]; then
    _PN=$(grep -E '^PROJECT_NAME\s*=' "$WORKSPACE/.env" | sed 's/^PROJECT_NAME\s*=\s*//' | tr -d '"'"'"' ')
  fi
  if [ -z "$_PN" ]; then
    _PN=$(cd "$WORKSPACE" && python3 -c "from config.project_config import PROJECT_NAME; print(PROJECT_NAME)" 2>/dev/null)
  fi
  PROJECT_NAME="$_PN"
fi
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

# Create bin/ if it doesn't exist (e.g., bin/ was in .hgignore and not cloned)
if [ ! -d "$BIN" ]; then
  echo "ℹ️  bin/ not found — creating: $BIN"
  mkdir -p "$BIN"
fi

if [ ! -d "$DEPS" ]; then
  echo "❌ Dependencies directory not found: $DEPS"
  exit 1
fi
echo "✅ Paths OK"

# ── 1b. Determine framework source ──────────────────────────────────────────
# Priority:
#   1. AutomaterSeleniumFramework/ hg repo (maintainers only)
#   2. Framework source ZIP in dependencies (automater-selenium-framework-*.zip)
#   3. Pre-compiled classes already in bin/ (from hg clone of base branch)
FW_SOURCE="none"
FW_COMPILE_DIR=""

if [ -d "$WORKSPACE/AutomaterSeleniumFramework" ] && [ -d "$FW_SRC" ]; then
  FW_SOURCE="hg_repo"
  FW_COMPILE_DIR="$FW_SRC"
  echo "✅ Framework source found (hg repo: AutomaterSeleniumFramework/)"
else
  # Try to extract framework source from ZIP in dependencies
  FW_ZIP=$(find "$DEPS" -name 'automater-selenium-framework-*.zip' -type f 2>/dev/null | head -1)
  if [ -n "$FW_ZIP" ]; then
    FW_SOURCE="zip"
    FW_EXTRACT_DIR=$(mktemp -d /tmp/fw_extract_XXXXXX)
    echo "ℹ️  AutomaterSeleniumFramework/ not present — extracting from ZIP:"
    echo "   $FW_ZIP"
    unzip -q "$FW_ZIP" -d "$FW_EXTRACT_DIR"
    FW_COMPILE_DIR="$FW_EXTRACT_DIR"

    # ── Patch ZIP source for compatibility with old AutomationFrameWork.jar ──
    # The ZIP may reference CommonVariables fields/methods that only exist in
    # newer builds (setisSkipScreenShot, launchPrimaryInRemote, gridURL).
    # The hg repo has these patched out; we apply the same patches here.
    echo "🔧 Patching ZIP source for JAR compatibility..."
    _EC="$FW_EXTRACT_DIR/com/zoho/automater/selenium/base/EntityCase.java"
    _DU="$FW_EXTRACT_DIR/com/zoho/automater/selenium/base/utils/DriverUtil.java"
    _FF="$FW_EXTRACT_DIR/com/zoho/automater/selenium/base/drivers/FirefoxWebDriver.java"
    _CH="$FW_EXTRACT_DIR/com/zoho/automater/selenium/base/drivers/ChromeWebDriver.java"
    # EntityCase: comment out setisSkipScreenShot calls
    if [ -f "$_EC" ]; then
      sed -i 's|CommonVariables\.setisSkipScreenShot(false);|// CommonVariables.setisSkipScreenShot(false); // patched: method not in JAR|g' "$_EC"
      sed -i 's|CommonVariables\.setisSkipScreenShot(true);|// CommonVariables.setisSkipScreenShot(true); // patched: method not in JAR|g' "$_EC"
    fi
    # DriverUtil: replace launchPrimaryInRemote access with default false
    if [ -f "$_DU" ]; then
      sed -i 's|LOGGER\.info("\[Aalam\] CommonVariables\.launchPrimaryInRemote = " + CommonVariables\.launchPrimaryInRemote);|LOGGER.info("[Aalam] launchPrimaryInRemote defaulting to false (local build)");|g' "$_DU"
      sed -i 's|return CommonVariables\.launchPrimaryInRemote;|return false;|g' "$_DU"
      # Remove the import if it was added (not in original hg source)
      sed -i '/^import com\.zoho\.automation\.CommonVariables;$/d' "$_DU"
    fi
    # FirefoxWebDriver: comment out gridURL assignment
    if [ -f "$_FF" ]; then
      sed -i 's|CommonVariables\.gridURL = gridURL;|// CommonVariables.gridURL = gridURL; // patched: field not in JAR|g' "$_FF"
    fi
    # ChromeWebDriver: comment out gridURL assignment
    if [ -f "$_CH" ]; then
      sed -i 's|CommonVariables\.gridURL = gridURL;|// CommonVariables.gridURL = gridURL; // patched: field not in JAR|g' "$_CH"
    fi
    # SDPCloudActions: fix "New Role" button xpath for modern SDP UI
    _SCA="$FW_EXTRACT_DIR/com/zoho/automater/selenium/base/client/SDPCloudActions.java"
    if [ -f "$_SCA" ]; then
      sed -i "s|//button\[text()='New Role'\]|//*[normalize-space(text())='New Role']|g" "$_SCA"
    fi

    echo "✅ Framework source extracted and patched from ZIP"
  else
    echo "ℹ️  No framework source available (no hg repo, no ZIP in deps)"
  fi
fi

# ── 2. Compile framework source (from hg repo or ZIP) ────────────────────────
if [ "$FW_SOURCE" != "none" ]; then

  # Switch hg branch (only for hg repo source)
  if [ "$FW_SOURCE" = "hg_repo" ]; then
    CURRENT_BRANCH=$(cd "$FW_DIR" && hg branch 2>/dev/null)
    if [ "$CURRENT_BRANCH" != "$TARGET_BRANCH" ]; then
      echo "⚠️  Framework is on branch '$CURRENT_BRANCH', switching to '$TARGET_BRANCH'..."
      cd "$FW_DIR" && hg update "$TARGET_BRANCH"
      echo "✅ Switched to $TARGET_BRANCH"
    else
      echo "✅ Framework branch: $TARGET_BRANCH"
    fi
  fi

  # ── 3. Build classpath (all JARs under deps recursively) ───────────────────
  CP="$BIN:$(find "$DEPS" -name "*.jar" | tr '\n' ':')"

  # ── 4. Collect source files — exclude Aalam-only BeforeAndAfterCaseActions ──
  SOURCES_FILE=$(mktemp /tmp/fw_sources_XXXXXX.txt)
  find "$FW_COMPILE_DIR" -name "*.java" | grep -v "BeforeAndAfterCaseActions" > "$SOURCES_FILE"
  FILE_COUNT=$(wc -l < "$SOURCES_FILE")
  echo "📂 Source files to compile: $FILE_COUNT"

  # ── 5. Compile ──────────────────────────────────────────────────────────────
  echo "⚙️  Compiling..."
  COMPILE_OUTPUT=$(javac -encoding UTF-8 -cp "$CP" -d "$BIN" @"$SOURCES_FILE" 2>&1)
  COMPILE_EXIT=$?
  if echo "$COMPILE_OUTPUT" | grep -q "error:"; then
    echo "$COMPILE_OUTPUT" | grep "error:" | head -20
    echo "❌ Compile FAILED — see errors above"
    rm -f "$SOURCES_FILE"
    [ -n "${FW_EXTRACT_DIR:-}" ] && rm -rf "$FW_EXTRACT_DIR"
    exit 1
  fi
  rm -f "$SOURCES_FILE"
  [ -n "${FW_EXTRACT_DIR:-}" ] && rm -rf "$FW_EXTRACT_DIR"

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
    SRC_LABEL="hg repo"
    [ "$FW_SOURCE" = "zip" ] && SRC_LABEL="ZIP in dependencies"
    echo "✅ Framework compiled successfully into $PROJECT_NAME/bin/ (from $SRC_LABEL)"
    echo "   $(find "$BIN/com/zoho/automater/selenium/base" -name "*.class" | wc -l) framework classes total"
  else
    echo "❌ $MISSING expected class(es) missing — compile may have partially failed"
    exit 1
  fi

else
  # ── No framework source at all — check if pre-compiled classes exist ────────
  echo ""
  echo "🔍 Checking for pre-compiled framework classes in $PROJECT_NAME/bin/..."
  KEY_CLASS="$BIN/com/zoho/automater/selenium/base/EntityCase.class"
  if [ -f "$KEY_CLASS" ]; then
    FW_CLASS_COUNT=$(find "$BIN/com/zoho/automater/selenium/base" -name "*.class" 2>/dev/null | wc -l)
    echo "✅ Found $FW_CLASS_COUNT pre-compiled framework classes in bin/"
    echo "   Tests will use these classes + the framework JAR from dependencies."
  else
    echo "⚠️  No pre-compiled framework classes found in bin/"
    echo "   Tests will rely on AutomationFrameWork.jar from dependencies."
    echo "   Local-run HTML reports may not generate correctly (missing isLocalSetup guard)."
    echo ""
    echo "   To fix: place the framework ZIP (automater-selenium-framework-*.zip)"
    echo "   in your dependencies folder and re-run this script."
  fi
fi

# ── 7. Generate .vscode/settings.json (Java classpath for VS Code) ───────────
# Eliminates red-line import errors in VS Code by configuring Java Language Server.
# Safe to run multiple times — preserves existing settings, only updates Java keys.
echo ""
echo "🔧 Configuring VS Code Java classpath..."
VSCODE_DIR="$WORKSPACE/.vscode"
SETTINGS_FILE="$VSCODE_DIR/settings.json"
mkdir -p "$VSCODE_DIR"

python3 - "$PROJECT_NAME" "$DEPS" "$SETTINGS_FILE" <<'PYEOF'
import json, sys, os

project_name = sys.argv[1]
deps_dir = sys.argv[2]
settings_path = sys.argv[3]

# Load existing settings (strip // comments for JSON parsing)
existing = {}
if os.path.isfile(settings_path):
    with open(settings_path, "r") as f:
        lines = f.readlines()
    cleaned = []
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("//"):
            continue
        # Remove inline // comments (naive but sufficient for settings.json)
        idx = line.find("//")
        if idx > 0 and '"' not in line[idx:]:
            line = line[:idx] + "\n"
        cleaned.append(line)
    try:
        existing = json.loads("".join(cleaned))
    except json.JSONDecodeError:
        existing = {}

# Update Java classpath settings
existing["java.project.sourcePaths"] = [project_name + "/src"]
existing["java.project.outputPath"] = project_name + "/bin"
existing["java.project.referencedLibraries"] = [deps_dir + "/**/*.jar"]
existing.setdefault("java.errors.incompleteClasspath.severity", "ignore")

with open(settings_path, "w") as f:
    json.dump(existing, f, indent=2)

print("  ✅ " + settings_path)
print("     sourcePaths:          " + project_name + "/src")
print("     outputPath:           " + project_name + "/bin")
print("     referencedLibraries:  " + deps_dir + "/**/*.jar")
PYEOF

echo ""
echo "======================================================"
echo "  Setup complete."
echo "======================================================"
