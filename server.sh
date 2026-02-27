#!/usr/bin/env bash
# server.sh — Start / Stop / Restart the AI Test Generator web server
#
# Usage:
#   ./server.sh start      → start on port 9500 (default)
#   ./server.sh stop       → kill the running server
#   ./server.sh restart    → stop then start
#   ./server.sh status     → show whether the server is running
#   ./server.sh logs       → tail the live log file
#
# Port can be overridden:
#   PORT=8090 ./server.sh start

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────────────────
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$REPO_DIR/.venv/bin/activate"
PORT="${PORT:-9500}"
HOST="${HOST:-0.0.0.0}"
LOG_FILE="$REPO_DIR/logs/server.log"
PID_FILE="$REPO_DIR/logs/server.pid"

# ── Helpers ───────────────────────────────────────────────────────────────────
_ensure_venv() {
    if [[ ! -f "$VENV" ]]; then
        echo "❌  Virtual environment not found at .venv/"
        echo "    Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
        exit 1
    fi
}

_is_running() {
    [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

_start() {
    _ensure_venv
    if _is_running; then
        echo "⚠️   Server is already running (PID $(cat "$PID_FILE")) on port $PORT"
        echo "     Use './server.sh restart' to reload."
        exit 0
    fi

    mkdir -p "$REPO_DIR/logs"
    echo "🚀  Starting server on http://localhost:$PORT ..."

    # shellcheck disable=SC1090
    source "$VENV"
    nohup uvicorn web.server:app \
        --host "$HOST" \
        --port "$PORT" \
        --log-level warning \
        >> "$LOG_FILE" 2>&1 &

    echo $! > "$PID_FILE"
    sleep 1

    if _is_running; then
        echo "✅  Server started — PID $(cat "$PID_FILE")"
        echo "    UI  : http://localhost:$PORT"
        echo "    Log : $LOG_FILE"
        echo "    PID : $PID_FILE"
    else
        echo "❌  Server failed to start. Check logs:"
        tail -20 "$LOG_FILE"
        exit 1
    fi
}

_stop() {
    if ! _is_running; then
        echo "ℹ️   Server is not running."
        rm -f "$PID_FILE"
        return
    fi
    PID=$(cat "$PID_FILE")
    echo "🛑  Stopping server (PID $PID) ..."
    kill "$PID" 2>/dev/null || true
    # Wait up to 5 s for it to die
    for i in {1..10}; do
        kill -0 "$PID" 2>/dev/null || break
        sleep 0.5
    done
    rm -f "$PID_FILE"
    echo "✅  Server stopped."
}

_status() {
    if _is_running; then
        PID=$(cat "$PID_FILE")
        echo "✅  Server is running — PID $PID on port $PORT"
        echo "    UI  : http://localhost:$PORT"
        echo "    Log : $LOG_FILE"
    else
        echo "🔴  Server is not running."
    fi
}

_logs() {
    if [[ ! -f "$LOG_FILE" ]]; then
        echo "ℹ️   No log file yet. Start the server first."
        exit 0
    fi
    echo "📜  Tailing $LOG_FILE  (Ctrl+C to stop)"
    tail -f "$LOG_FILE"
}

# ── Dispatch ──────────────────────────────────────────────────────────────────
CMD="${1:-help}"
case "$CMD" in
    start)   _start ;;
    stop)    _stop  ;;
    restart) _stop; sleep 1; _start ;;
    status)  _status ;;
    logs)    _logs ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        echo ""
        echo "  start    — start the web server (default port 9500)"
        echo "  stop     — stop the running server"
        echo "  restart  — stop then start (picks up config changes)"
        echo "  status   — check if the server is running"
        echo "  logs     — tail the server log file"
        echo ""
        echo "  PORT=8090 ./server.sh start   — start on a custom port"
        ;;
esac
