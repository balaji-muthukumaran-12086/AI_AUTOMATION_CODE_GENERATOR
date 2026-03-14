#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────
# start_playwright_mcp.sh — Ensures Playwright MCP server is ready
#
# Called by @test-runner agent before batch/single test execution.
# Verifies all prerequisites (node, @playwright/mcp, browser binary)
# and starts the MCP server if not already running.
#
# Usage:
#   ./start_playwright_mcp.sh          # verify + print status
#   ./start_playwright_mcp.sh --start  # start server in background (SSE mode)
#   ./start_playwright_mcp.sh --stop   # stop running server
#   ./start_playwright_mcp.sh --status # check if server is running
# ─────────────────────────────────────────────────────────────────────

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PID_FILE="$SCRIPT_DIR/.playwright_mcp.pid"
LOG_FILE="$SCRIPT_DIR/logs/playwright_mcp.log"
MCP_PORT="${PLAYWRIGHT_MCP_PORT:-3100}"

# ── Colors ───────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

ok()   { echo -e "${GREEN}✓${NC} $1"; }
warn() { echo -e "${YELLOW}⚠${NC} $1"; }
fail() { echo -e "${RED}✗${NC} $1"; }

# ── Prerequisite checks ─────────────────────────────────────────────
check_prereqs() {
    local all_ok=true

    # Node.js
    if command -v node &>/dev/null; then
        ok "Node.js $(node --version)"
    else
        fail "Node.js not found — install from https://nodejs.org"
        all_ok=false
    fi

    # @playwright/mcp package
    if [[ -d "$SCRIPT_DIR/node_modules/@playwright/mcp" ]]; then
        local ver
        ver=$(node -e "console.log(require('@playwright/mcp/package.json').version)" 2>/dev/null || echo "unknown")
        ok "@playwright/mcp v${ver} (local)"
    else
        fail "@playwright/mcp not installed — run: npm install @playwright/mcp"
        all_ok=false
    fi

    # Chromium browser binary
    if npx playwright install --dry-run chromium 2>&1 | grep -qi "already installed\|up to date\|browsers"; then
        ok "Chromium browser available"
    elif [[ -d "$HOME/.cache/ms-playwright" ]] && ls "$HOME/.cache/ms-playwright"/chromium* &>/dev/null; then
        ok "Chromium browser found in cache"
    else
        warn "Chromium may not be installed — run: npx playwright install chromium"
    fi

    $all_ok
}

# ── Server management ────────────────────────────────────────────────
is_running() {
    if [[ -f "$PID_FILE" ]]; then
        local pid
        pid=$(cat "$PID_FILE")
        if kill -0 "$pid" 2>/dev/null; then
            return 0
        else
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

start_server() {
    if is_running; then
        local pid
        pid=$(cat "$PID_FILE")
        ok "Playwright MCP server already running (PID $pid)"
        return 0
    fi

    mkdir -p "$(dirname "$LOG_FILE")"

    echo -e "Starting Playwright MCP server on port ${MCP_PORT}..."

    # Start in background with nohup — uses local node_modules binary
    # --port enables SSE transport (persistent server mode)
    # --vision enables screenshot capability for debugging
    nohup node "$SCRIPT_DIR/node_modules/@playwright/mcp/cli.js" \
        --port "$MCP_PORT" \
        --vision \
        > "$LOG_FILE" 2>&1 &
    local pid=$!
    echo "$pid" > "$PID_FILE"

    # Wait for server to be ready (max 10 seconds)
    local attempts=0
    while [[ $attempts -lt 20 ]]; do
        if curl -sf "http://localhost:${MCP_PORT}/sse" -o /dev/null --max-time 1 2>/dev/null; then
            ok "Playwright MCP server started (PID $pid, port $MCP_PORT)"
            return 0
        fi
        sleep 0.5
        ((attempts++))
    done

    # Check if process is still alive
    if kill -0 "$pid" 2>/dev/null; then
        ok "Playwright MCP server started (PID $pid, port $MCP_PORT) — may still be initializing"
    else
        fail "Playwright MCP server failed to start. Check $LOG_FILE"
        cat "$LOG_FILE" | tail -20
        rm -f "$PID_FILE"
        return 1
    fi
}

stop_server() {
    if ! is_running; then
        warn "Playwright MCP server is not running"
        return 0
    fi

    local pid
    pid=$(cat "$PID_FILE")
    kill "$pid" 2>/dev/null || true
    rm -f "$PID_FILE"
    ok "Playwright MCP server stopped (was PID $pid)"
}

status_server() {
    if is_running; then
        local pid
        pid=$(cat "$PID_FILE")
        ok "Playwright MCP server is running (PID $pid, port $MCP_PORT)"
    else
        warn "Playwright MCP server is not running"
        return 1
    fi
}

# ── Main ─────────────────────────────────────────────────────────────
case "${1:-}" in
    --start)
        check_prereqs || exit 1
        start_server
        ;;
    --stop)
        stop_server
        ;;
    --status)
        status_server
        ;;
    *)
        echo "═══ Playwright MCP Preflight Check ═══"
        check_prereqs
        echo ""
        status_server 2>/dev/null || warn "Server not running — use: $0 --start"
        echo ""
        echo "Commands:"
        echo "  $0 --start   Start the MCP server"
        echo "  $0 --stop    Stop the MCP server"
        echo "  $0 --status  Check server status"
        ;;
esac
