#!/usr/bin/env bash
# docker-entrypoint.sh
# Runs inside the container before starting the FastAPI server.

set -euo pipefail

echo "── AI Automation QA — container startup ─────────────────────────────────"

# ── 1. Start virtual display (Xvfb) for any headful Firefox JVM tests ────────
# Selenium in JVM uses DISPLAY even with --headless flag as a safety net.
echo "[docker] Starting Xvfb on :99 ..."
Xvfb :99 -screen 0 1920x1080x24 -ac &
export DISPLAY=:99

# ── 2. Compile AutomaterSeleniumFramework into bin/ (if mounted & not done) ──
# setup_framework_bin.sh is idempotent — skips recompile if bin/ is current.
if [ -f "/app/setup_framework_bin.sh" ] && \
   [ -d "/app/AutomaterSeleniumFramework/src" ]; then
    echo "[docker] Compiling AutomaterSeleniumFramework into bin/ ..."
    bash /app/setup_framework_bin.sh
else
    echo "[docker] AutomaterSeleniumFramework not mounted — skipping framework compile."
fi

# ── 3. Start FastAPI server ───────────────────────────────────────────────────
echo "[docker] Starting FastAPI on ${HOST:-0.0.0.0}:${PORT:-9500} ..."
exec python3 -m uvicorn web.server:app \
    --host "${HOST:-0.0.0.0}" \
    --port "${PORT:-9500}"
