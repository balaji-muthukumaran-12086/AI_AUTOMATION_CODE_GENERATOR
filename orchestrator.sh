#!/usr/bin/env bash
# orchestrator.sh — Start / Stop / Restart the Orchestrator monitoring server
#
# Usage:
#   ./orchestrator.sh start      → start on port 9600 (default)
#   ./orchestrator.sh stop       → kill the running server
#   ./orchestrator.sh restart    → stop then start
#   ./orchestrator.sh status     → show whether the server is running
#   ./orchestrator.sh logs       → tail the live log file
#
# Port can be overridden:
#   PORT=9601 ./orchestrator.sh start

set -euo pipefail

# ── Config ────────────────────────────────────────────────────────────────────
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV="$REPO_DIR/.venv/bin/activate"
PORT="${PORT:-9600}"
HOST="${HOST:-0.0.0.0}"
LOG_DIR="$REPO_DIR/logs"
LOG_FILE="$LOG_DIR/orchestrator.log"
PID_FILE="$LOG_DIR/orchestrator.pid"

# ── Helpers ───────────────────────────────────────────────────────────────────
_ensure_venv() {
    if [[ ! -f "$VENV" ]]; then
        echo "Virtual environment not found at .venv/"
        echo "Run: python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
        exit 1
    fi
}

_is_running() {
    [[ -f "$PID_FILE" ]] && kill -0 "$(cat "$PID_FILE")" 2>/dev/null
}

_start() {
    _ensure_venv
    if _is_running; then
        echo "Orchestrator is already running (PID $(cat "$PID_FILE")) on port $PORT"
        echo "Use './orchestrator.sh restart' to reload."
        exit 0
    fi

    mkdir -p "$LOG_DIR"
    echo "Starting orchestrator on http://localhost:$PORT ..."

    # shellcheck disable=SC1090
    source "$VENV"
    nohup python -m uvicorn orchestrator.server:app \
        --host "$HOST" \
        --port "$PORT" \
        --log-level warning \
        >> "$LOG_FILE" 2>&1 &

    echo $! > "$PID_FILE"
    sleep 1

    if _is_running; then
        echo "Orchestrator started — PID $(cat "$PID_FILE")  http://localhost:$PORT"
    else
        echo "Failed to start. Check $LOG_FILE"
        exit 1
    fi
}

_stop() {
    if ! _is_running; then
        echo "Orchestrator is not running."
        rm -f "$PID_FILE"
        return
    fi

    local pid
    pid="$(cat "$PID_FILE")"
    echo "Stopping orchestrator (PID $pid) ..."
    kill "$pid" 2>/dev/null || true
    sleep 1
    if kill -0 "$pid" 2>/dev/null; then
        kill -9 "$pid" 2>/dev/null || true
    fi
    rm -f "$PID_FILE"
    echo "Orchestrator stopped."
}

_status() {
    if _is_running; then
        echo "Orchestrator is running — PID $(cat "$PID_FILE"), port $PORT"
    else
        echo "Orchestrator is not running."
        rm -f "$PID_FILE"
    fi
}

_logs() {
    if [[ -f "$LOG_FILE" ]]; then
        tail -f "$LOG_FILE"
    else
        echo "No log file found at $LOG_FILE"
    fi
}

# ── Main ──────────────────────────────────────────────────────────────────────
case "${1:-help}" in
    start)   _start   ;;
    stop)    _stop    ;;
    restart) _stop; _start ;;
    status)  _status  ;;
    logs)    _logs    ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs}"
        exit 1
        ;;
esac
