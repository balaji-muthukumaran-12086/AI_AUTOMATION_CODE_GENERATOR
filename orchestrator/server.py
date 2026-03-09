"""
orchestrator/server.py
----------------------
Centralized logging server for the AutomaterSelenium framework.

Receives events from multiple team members' machines via HTTP,
stores them in SQLite, and provides a real-time dashboard.

Run:
  cd ai-automation-qa
  .venv/bin/python -m orchestrator.server
  # or:
  .venv/bin/uvicorn orchestrator.server:app --host 0.0.0.0 --port 9600
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import threading
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import uvicorn
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

# ── Bootstrap paths ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

from orchestrator.models import (
    AgentName,
    DashboardStats,
    EventType,
    LogEvent,
    StoredEvent,
)

# ── Configuration ─────────────────────────────────────────────────────────────
DB_PATH = os.environ.get("ORCHESTRATOR_DB", str(BASE_DIR / "orchestrator" / "orchestrator.db"))
SERVER_PORT = int(os.environ.get("ORCHESTRATOR_PORT", "9600"))

# ── SQLite setup ──────────────────────────────────────────────────────────────
_db_lock = threading.Lock()


def _init_db():
    """Create the events table if it doesn't exist."""
    with _get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp    TEXT NOT NULL,
                received_at  TEXT NOT NULL,
                event_type   TEXT NOT NULL,
                agent        TEXT NOT NULL,
                owner        TEXT NOT NULL,
                machine_id   TEXT NOT NULL,
                module       TEXT,
                entity       TEXT,
                feature_name TEXT,
                scenario_id  TEXT,
                method_name  TEXT,
                status       TEXT,
                duration_ms  INTEGER,
                error_message TEXT,
                scenarios_count INTEGER,
                metadata     TEXT
            )
        """)
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_owner ON events(owner)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_type ON events(event_type)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_agent ON events(agent)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_module ON events(module)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_feature ON events(feature_name)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_ts ON events(timestamp)")
        conn.commit()


@contextmanager
def _get_db():
    """Thread-safe SQLite connection context manager."""
    conn = sqlite3.connect(DB_PATH, timeout=10)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def _insert_event(event: LogEvent) -> int:
    """Insert an event and return its ID."""
    now = datetime.now(timezone.utc).isoformat()
    with _db_lock, _get_db() as conn:
        cursor = conn.execute(
            """
            INSERT INTO events (
                timestamp, received_at, event_type, agent, owner, machine_id,
                module, entity, feature_name, scenario_id, method_name,
                status, duration_ms, error_message, scenarios_count, metadata
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                now, now, event.event_type.value, event.agent.value,
                event.owner, event.machine_id,
                event.module, event.entity, event.feature_name,
                event.scenario_id, event.method_name,
                event.status, event.duration_ms, event.error_message,
                event.scenarios_count,
                json.dumps(event.metadata) if event.metadata else None,
            ),
        )
        conn.commit()
        return cursor.lastrowid


def _query_events(
    owner: Optional[str] = None,
    agent: Optional[str] = None,
    module: Optional[str] = None,
    event_type: Optional[str] = None,
    feature_name: Optional[str] = None,
    since: Optional[str] = None,
    until: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
) -> list[dict]:
    """Query events with optional filters."""
    conditions = []
    params = []

    if owner:
        conditions.append("owner = ?")
        params.append(owner)
    if agent:
        conditions.append("agent = ?")
        params.append(agent)
    if module:
        conditions.append("module = ?")
        params.append(module)
    if event_type:
        conditions.append("event_type = ?")
        params.append(event_type)
    if feature_name:
        conditions.append("feature_name = ?")
        params.append(feature_name)
    if since:
        conditions.append("timestamp >= ?")
        params.append(since)
    if until:
        conditions.append("timestamp <= ?")
        params.append(until)

    where = " AND ".join(conditions) if conditions else "1=1"
    params.extend([limit, offset])

    with _get_db() as conn:
        rows = conn.execute(
            f"SELECT * FROM events WHERE {where} ORDER BY timestamp DESC LIMIT ? OFFSET ?",
            params,
        ).fetchall()
        return [dict(r) for r in rows]


def _get_stats() -> dict:
    """Compute aggregated dashboard statistics."""
    with _get_db() as conn:
        total = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]

        generated = conn.execute(
            "SELECT COALESCE(SUM(scenarios_count), 0) FROM events WHERE event_type = 'scenario_generated'"
        ).fetchone()[0]
        # Also count individual scenario_generated events without scenarios_count
        generated_events = conn.execute(
            "SELECT COUNT(*) FROM events WHERE event_type = 'scenario_generated' AND (scenarios_count IS NULL OR scenarios_count = 0)"
        ).fetchone()[0]
        total_generated = generated + generated_events

        passed = conn.execute(
            "SELECT COUNT(*) FROM events WHERE event_type = 'scenario_passed'"
        ).fetchone()[0]
        failed = conn.execute(
            "SELECT COUNT(*) FROM events WHERE event_type = 'scenario_failed'"
        ).fetchone()[0]

        active_users = conn.execute(
            "SELECT COUNT(DISTINCT owner) FROM events"
        ).fetchone()[0]

        features = conn.execute(
            "SELECT COUNT(DISTINCT feature_name) FROM events WHERE feature_name IS NOT NULL"
        ).fetchone()[0]

        # Events by owner
        by_owner = {}
        for row in conn.execute("SELECT owner, COUNT(*) as cnt FROM events GROUP BY owner ORDER BY cnt DESC"):
            by_owner[row["owner"]] = row["cnt"]

        # Events by module
        by_module = {}
        for row in conn.execute(
            "SELECT module, COUNT(*) as cnt FROM events WHERE module IS NOT NULL GROUP BY module ORDER BY cnt DESC"
        ):
            by_module[row["module"]] = row["cnt"]

        # Events by agent
        by_agent = {}
        for row in conn.execute("SELECT agent, COUNT(*) as cnt FROM events GROUP BY agent ORDER BY cnt DESC"):
            by_agent[row["agent"]] = row["cnt"]

        # Recent activity (last 20 events)
        recent = conn.execute(
            "SELECT * FROM events ORDER BY timestamp DESC LIMIT 20"
        ).fetchall()
        recent_list = [dict(r) for r in recent]

        executed = passed + failed
        pass_rate = round((passed / executed * 100), 1) if executed > 0 else 0.0

    return {
        "total_events": total,
        "total_scenarios_generated": total_generated,
        "total_scenarios_passed": passed,
        "total_scenarios_failed": failed,
        "active_users": active_users,
        "features_processed": features,
        "events_by_owner": by_owner,
        "events_by_module": by_module,
        "events_by_agent": by_agent,
        "recent_activity": recent_list,
        "pass_rate": pass_rate,
    }


def _get_owner_summary() -> list[dict]:
    """Per-owner summary: features worked on, scenarios generated/passed/failed."""
    with _get_db() as conn:
        rows = conn.execute("""
            SELECT
                owner,
                COUNT(DISTINCT feature_name) as features_count,
                COUNT(DISTINCT CASE WHEN event_type = 'scenario_generated' THEN scenario_id END) as generated,
                COUNT(CASE WHEN event_type = 'scenario_passed' THEN 1 END) as passed,
                COUNT(CASE WHEN event_type = 'scenario_failed' THEN 1 END) as failed,
                COUNT(CASE WHEN event_type = 'scenario_healed' THEN 1 END) as healed,
                MIN(timestamp) as first_seen,
                MAX(timestamp) as last_seen
            FROM events
            GROUP BY owner
            ORDER BY last_seen DESC
        """).fetchall()
        return [dict(r) for r in rows]


def _get_feature_summary() -> list[dict]:
    """Per-feature summary: who worked on it, scenario counts, pass rate."""
    with _get_db() as conn:
        rows = conn.execute("""
            SELECT
                feature_name,
                GROUP_CONCAT(DISTINCT owner) as owners,
                GROUP_CONCAT(DISTINCT module) as modules,
                COUNT(CASE WHEN event_type = 'scenario_planned' THEN 1 END) as planned,
                COUNT(CASE WHEN event_type = 'scenario_generated' THEN 1 END) as generated,
                COUNT(CASE WHEN event_type = 'scenario_passed' THEN 1 END) as passed,
                COUNT(CASE WHEN event_type = 'scenario_failed' THEN 1 END) as failed,
                MIN(timestamp) as started_at,
                MAX(timestamp) as last_activity
            FROM events
            WHERE feature_name IS NOT NULL
            GROUP BY feature_name
            ORDER BY last_activity DESC
        """).fetchall()
        return [dict(r) for r in rows]


# ── FastAPI app ───────────────────────────────────────────────────────────────
app = FastAPI(title="AutomaterSelenium Orchestrator", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup():
    _init_db()


# ── API Endpoints ─────────────────────────────────────────────────────────────

@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "orchestrator"}


@app.post("/api/events")
async def log_event(event: LogEvent):
    """Receive and store a single event from any agent/machine."""
    event_id = _insert_event(event)
    return {"id": event_id, "status": "logged"}


@app.post("/api/events/batch")
async def log_events_batch(events: list[LogEvent]):
    """Receive and store multiple events at once."""
    ids = []
    for event in events:
        ids.append(_insert_event(event))
    return {"ids": ids, "count": len(ids), "status": "logged"}


@app.get("/api/events")
async def query_events(
    owner: Optional[str] = Query(None),
    agent: Optional[str] = Query(None),
    module: Optional[str] = Query(None),
    event_type: Optional[str] = Query(None),
    feature_name: Optional[str] = Query(None),
    since: Optional[str] = Query(None),
    until: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """Query events with optional filters."""
    return _query_events(
        owner=owner, agent=agent, module=module,
        event_type=event_type, feature_name=feature_name,
        since=since, until=until, limit=limit, offset=offset,
    )


@app.get("/api/stats")
async def get_stats():
    """Aggregated dashboard statistics."""
    return _get_stats()


@app.get("/api/owners")
async def get_owner_summary():
    """Per-owner activity summary."""
    return _get_owner_summary()


@app.get("/api/features")
async def get_feature_summary():
    """Per-feature activity summary."""
    return _get_feature_summary()


# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """Serve the orchestrator dashboard."""
    dashboard_path = Path(__file__).parent / "dashboard.html"
    if not dashboard_path.exists():
        raise HTTPException(404, "Dashboard not found")
    return dashboard_path.read_text(encoding="utf-8")


# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    _init_db()
    print(f"🚀 Orchestrator server starting on http://0.0.0.0:{SERVER_PORT}")
    print(f"   Dashboard: http://localhost:{SERVER_PORT}/")
    print(f"   API docs:  http://localhost:{SERVER_PORT}/docs")
    print(f"   Database:  {DB_PATH}")
    uvicorn.run(app, host="0.0.0.0", port=SERVER_PORT)
