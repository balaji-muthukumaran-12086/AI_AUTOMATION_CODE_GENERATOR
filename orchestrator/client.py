"""
orchestrator/client.py
----------------------
Lightweight HTTP client for logging events to the centralized orchestrator server.

Usage in any agent or script:
    from orchestrator.client import OrchestratorClient

    oc = OrchestratorClient()
    oc.scenario_generated(
        module="changes", entity="Change",
        feature_name="linking_changes",
        scenario_id="SDPOD_AUTO_CH_LV_500",
        method_name="verifyLinkParentChange",
        scenarios_count=3,
    )
    oc.scenario_passed(scenario_id="SDPOD_AUTO_CH_LV_500", method_name="verifyLinkParentChange")

The client is fire-and-forget: if the server is unreachable, events are
silently dropped (or queued to a local fallback file for later replay).
"""
from __future__ import annotations

import json
import logging
import os
import platform
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.error import URLError
from urllib.request import Request, urlopen

# ── Bootstrap ─────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

logger = logging.getLogger("orchestrator.client")

# ── Configuration ─────────────────────────────────────────────────────────────
_DEFAULT_SERVER = os.environ.get("ORCHESTRATOR_URL", "http://localhost:9600")
_FALLBACK_LOG = BASE_DIR / "orchestrator" / "offline_events.jsonl"
_TIMEOUT = 5  # seconds


def _resolve_owner() -> str:
    """Resolve the owner constant from project_config."""
    try:
        from config.project_config import OWNER_CONSTANT
        return OWNER_CONSTANT
    except Exception:
        return os.environ.get("OWNER_CONSTANT", "UNKNOWN")


def _resolve_machine_id() -> str:
    """Generate a machine identifier."""
    return platform.node() or os.environ.get("HOSTNAME", "unknown")


class OrchestratorClient:
    """Fire-and-forget client for sending events to the orchestrator server."""

    def __init__(self, server_url: Optional[str] = None, owner: Optional[str] = None):
        self.server_url = (server_url or _DEFAULT_SERVER).rstrip("/")
        self.owner = owner or _resolve_owner()
        self.machine_id = _resolve_machine_id()
        self._enabled = os.environ.get("ORCHESTRATOR_ENABLED", "true").lower() != "false"

    def _send(self, event: dict) -> bool:
        """Send event to the server. Returns True on success."""
        if not self._enabled:
            return False

        payload = json.dumps(event).encode("utf-8")
        req = Request(
            f"{self.server_url}/api/events",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(req, timeout=_TIMEOUT) as resp:
                return resp.status == 200
        except (URLError, OSError, TimeoutError):
            self._save_offline(event)
            return False

    def _send_async(self, event: dict):
        """Send event in a background thread (non-blocking)."""
        t = threading.Thread(target=self._send, args=(event,), daemon=True)
        t.start()

    def _save_offline(self, event: dict):
        """Append event to offline fallback file for later replay."""
        try:
            _FALLBACK_LOG.parent.mkdir(parents=True, exist_ok=True)
            with open(_FALLBACK_LOG, "a", encoding="utf-8") as f:
                f.write(json.dumps(event) + "\n")
        except OSError:
            pass  # Truly silent fallback

    def _build_event(
        self,
        event_type: str,
        agent: str,
        module: Optional[str] = None,
        entity: Optional[str] = None,
        feature_name: Optional[str] = None,
        scenario_id: Optional[str] = None,
        method_name: Optional[str] = None,
        status: Optional[str] = None,
        duration_ms: Optional[int] = None,
        error_message: Optional[str] = None,
        scenarios_count: Optional[int] = None,
        metadata: Optional[dict] = None,
    ) -> dict:
        return {
            "event_type": event_type,
            "agent": agent,
            "owner": self.owner,
            "machine_id": self.machine_id,
            "module": module,
            "entity": entity,
            "feature_name": feature_name,
            "scenario_id": scenario_id,
            "method_name": method_name,
            "status": status,
            "duration_ms": duration_ms,
            "error_message": error_message,
            "scenarios_count": scenarios_count,
            "metadata": metadata,
        }

    # ── Convenience methods ───────────────────────────────────────────────────

    def feature_ingested(self, feature_name: str, module: Optional[str] = None,
                         scenarios_count: Optional[int] = None, **kw):
        event = self._build_event(
            "feature_ingested", "ingestion",
            feature_name=feature_name, module=module,
            scenarios_count=scenarios_count, **kw,
        )
        self._send_async(event)

    def scenario_planned(self, feature_name: str, scenario_id: Optional[str] = None,
                         method_name: Optional[str] = None, module: Optional[str] = None, **kw):
        event = self._build_event(
            "scenario_planned", "planner",
            feature_name=feature_name, scenario_id=scenario_id,
            method_name=method_name, module=module, **kw,
        )
        self._send_async(event)

    def scenario_generated(self, module: Optional[str] = None, entity: Optional[str] = None,
                           feature_name: Optional[str] = None, scenario_id: Optional[str] = None,
                           method_name: Optional[str] = None, scenarios_count: Optional[int] = None,
                           agent: str = "test-generator", **kw):
        event = self._build_event(
            "scenario_generated", agent,
            module=module, entity=entity, feature_name=feature_name,
            scenario_id=scenario_id, method_name=method_name,
            scenarios_count=scenarios_count, **kw,
        )
        self._send_async(event)

    def scenario_compiled(self, module: Optional[str] = None, entity: Optional[str] = None,
                          scenario_id: Optional[str] = None, method_name: Optional[str] = None,
                          status: str = "pass", error_message: Optional[str] = None, **kw):
        event = self._build_event(
            "scenario_compiled", "runner",
            module=module, entity=entity, scenario_id=scenario_id,
            method_name=method_name, status=status,
            error_message=error_message, **kw,
        )
        self._send_async(event)

    def scenario_executed(self, scenario_id: Optional[str] = None,
                          method_name: Optional[str] = None, module: Optional[str] = None,
                          duration_ms: Optional[int] = None, **kw):
        event = self._build_event(
            "scenario_executed", "runner",
            scenario_id=scenario_id, method_name=method_name,
            module=module, duration_ms=duration_ms, **kw,
        )
        self._send_async(event)

    def scenario_passed(self, scenario_id: Optional[str] = None,
                        method_name: Optional[str] = None, module: Optional[str] = None,
                        duration_ms: Optional[int] = None, **kw):
        event = self._build_event(
            "scenario_passed", "runner",
            scenario_id=scenario_id, method_name=method_name,
            module=module, duration_ms=duration_ms, status="pass", **kw,
        )
        self._send_async(event)

    def scenario_failed(self, scenario_id: Optional[str] = None,
                        method_name: Optional[str] = None, module: Optional[str] = None,
                        error_message: Optional[str] = None,
                        duration_ms: Optional[int] = None, **kw):
        event = self._build_event(
            "scenario_failed", "runner",
            scenario_id=scenario_id, method_name=method_name,
            module=module, error_message=error_message,
            duration_ms=duration_ms, status="fail", **kw,
        )
        self._send_async(event)

    def scenario_healed(self, scenario_id: Optional[str] = None,
                        method_name: Optional[str] = None, module: Optional[str] = None,
                        metadata: Optional[dict] = None, **kw):
        event = self._build_event(
            "scenario_healed", "healer",
            scenario_id=scenario_id, method_name=method_name,
            module=module, metadata=metadata, status="healed", **kw,
        )
        self._send_async(event)

    def agent_started(self, agent: str, feature_name: Optional[str] = None,
                      metadata: Optional[dict] = None, **kw):
        event = self._build_event(
            "agent_started", agent,
            feature_name=feature_name, metadata=metadata, **kw,
        )
        self._send_async(event)

    def agent_completed(self, agent: str, feature_name: Optional[str] = None,
                        duration_ms: Optional[int] = None,
                        metadata: Optional[dict] = None, **kw):
        event = self._build_event(
            "agent_completed", agent,
            feature_name=feature_name, duration_ms=duration_ms,
            metadata=metadata, **kw,
        )
        self._send_async(event)

    def agent_error(self, agent: str, error_message: str,
                    feature_name: Optional[str] = None, **kw):
        event = self._build_event(
            "agent_error", agent,
            feature_name=feature_name, error_message=error_message,
            status="error", **kw,
        )
        self._send_async(event)

    def project_setup(self, metadata: Optional[dict] = None, **kw):
        event = self._build_event(
            "project_setup", "setup-project",
            metadata=metadata, **kw,
        )
        self._send_async(event)

    def custom(self, agent: str, message: str, metadata: Optional[dict] = None, **kw):
        event = self._build_event(
            "custom", agent,
            error_message=message, metadata=metadata, **kw,
        )
        self._send_async(event)

    # ── Replay offline events ─────────────────────────────────────────────────

    def replay_offline(self) -> int:
        """Replay events saved in the offline fallback file. Returns count sent."""
        if not _FALLBACK_LOG.exists():
            return 0

        sent = 0
        remaining = []

        with open(_FALLBACK_LOG, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    event = json.loads(line)
                    if self._send(event):
                        sent += 1
                    else:
                        remaining.append(line)
                except json.JSONDecodeError:
                    continue

        # Rewrite file with unsent events (or remove if all sent)
        if remaining:
            with open(_FALLBACK_LOG, "w", encoding="utf-8") as f:
                f.write("\n".join(remaining) + "\n")
        elif _FALLBACK_LOG.exists():
            _FALLBACK_LOG.unlink()

        return sent


# ── Module-level singleton for easy imports ───────────────────────────────────
_client: Optional[OrchestratorClient] = None


def get_client() -> OrchestratorClient:
    """Get or create the global OrchestratorClient singleton."""
    global _client
    if _client is None:
        _client = OrchestratorClient()
    return _client
