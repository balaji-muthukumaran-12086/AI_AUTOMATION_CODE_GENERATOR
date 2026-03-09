"""
orchestrator/models.py
----------------------
Pydantic models for the orchestrator event logging system.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class EventType(str, Enum):
    """All trackable event types in the pipeline."""
    # Feature / document events
    FEATURE_INGESTED = "feature_ingested"

    # Scenario lifecycle
    SCENARIO_PLANNED = "scenario_planned"
    SCENARIO_GENERATED = "scenario_generated"
    SCENARIO_COMPILED = "scenario_compiled"
    SCENARIO_EXECUTED = "scenario_executed"
    SCENARIO_PASSED = "scenario_passed"
    SCENARIO_FAILED = "scenario_failed"
    SCENARIO_HEALED = "scenario_healed"

    # Agent-level events
    AGENT_STARTED = "agent_started"
    AGENT_COMPLETED = "agent_completed"
    AGENT_ERROR = "agent_error"

    # Setup events
    PROJECT_SETUP = "project_setup"

    # Custom / free-form
    CUSTOM = "custom"


class AgentName(str, Enum):
    """Agent identifiers."""
    SETUP_PROJECT = "setup-project"
    TEST_GENERATOR = "test-generator"
    TEST_DEBUGGER = "test-debugger"
    INGESTION = "ingestion"
    PLANNER = "planner"
    COVERAGE = "coverage"
    CODER = "coder"
    REVIEWER = "reviewer"
    OUTPUT = "output"
    RUNNER = "runner"
    HEALER = "healer"
    PIPELINE = "pipeline"


class LogEvent(BaseModel):
    """A single event logged by any agent on any machine."""
    event_type: EventType
    agent: AgentName
    owner: str = Field(..., description="OwnerConstants value (e.g. BALAJI_M)")
    machine_id: str = Field(..., description="Hostname or unique machine identifier")
    module: Optional[str] = Field(None, description="SDP module (changes, requests, etc.)")
    entity: Optional[str] = Field(None, description="Entity name (Change, Solution, etc.)")
    feature_name: Optional[str] = Field(None, description="Feature document or use-case name")
    scenario_id: Optional[str] = Field(None, description="@AutomaterScenario id value")
    method_name: Optional[str] = Field(None, description="Test method name")
    status: Optional[str] = Field(None, description="pass / fail / error / skipped")
    duration_ms: Optional[int] = Field(None, description="Duration in milliseconds")
    error_message: Optional[str] = Field(None, description="Error details if failed")
    scenarios_count: Optional[int] = Field(None, description="Number of scenarios generated")
    metadata: Optional[dict] = Field(None, description="Any extra key-value data")


class StoredEvent(LogEvent):
    """Event as stored in DB with server-assigned fields."""
    id: int
    timestamp: datetime
    received_at: datetime


class DashboardQuery(BaseModel):
    """Query parameters for dashboard filtering."""
    owner: Optional[str] = None
    agent: Optional[AgentName] = None
    module: Optional[str] = None
    event_type: Optional[EventType] = None
    feature_name: Optional[str] = None
    since: Optional[datetime] = None
    until: Optional[datetime] = None
    limit: int = Field(100, ge=1, le=1000)
    offset: int = Field(0, ge=0)


class DashboardStats(BaseModel):
    """Aggregated statistics for the dashboard."""
    total_events: int
    total_scenarios_generated: int
    total_scenarios_passed: int
    total_scenarios_failed: int
    active_users: int
    features_processed: int
    events_by_owner: dict[str, int]
    events_by_module: dict[str, int]
    events_by_agent: dict[str, int]
    recent_activity: list[dict]
    pass_rate: float
