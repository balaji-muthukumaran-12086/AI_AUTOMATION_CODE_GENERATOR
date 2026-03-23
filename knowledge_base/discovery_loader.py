"""
discovery_loader.py
-------------------
Loads Feature Knowledge Documents produced by the @product-discovery agent
and makes them available to the Coder Agent / test-generator pipeline.

Discovery documents live in:  knowledge_base/discoveries/{module}_{feature}.json

Usage:
    from knowledge_base.discovery_loader import DiscoveryLoader

    loader = DiscoveryLoader()

    # Load a specific feature discovery
    doc = loader.load("changes", "trash")

    # Get context text for LLM prompt injection
    context = loader.get_context_text("changes", "trash")

    # Check if discovery exists before generating tests
    if not loader.exists("changes", "link_child"):
        print("Run @product-discovery changes/link_child first!")

    # List all available discoveries
    all_discoveries = loader.list_all()
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional


class DiscoveryLoader:
    """Loads and queries Feature Knowledge Documents from the discoveries directory."""

    def __init__(self, base_dir: str = None):
        base = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self.discoveries_dir = base / "knowledge_base" / "discoveries"
        self.discoveries_dir.mkdir(parents=True, exist_ok=True)

    def _doc_path(self, module: str, feature: str) -> Path:
        return self.discoveries_dir / f"{module}_{feature}.json"

    def exists(self, module: str, feature: str) -> bool:
        """Check if a discovery document exists for this module/feature."""
        return self._doc_path(module, feature).exists()

    def load(self, module: str, feature: str) -> Optional[dict]:
        """Load a feature knowledge document. Returns None if not found."""
        path = self._doc_path(module, feature)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))

    def list_all(self) -> list[dict]:
        """List all available discovery documents with basic metadata."""
        results = []
        for path in sorted(self.discoveries_dir.glob("*.json")):
            if path.name.endswith("_summary.json"):
                continue
            parts = path.stem.split("_", 1)
            if len(parts) == 2:
                module, feature = parts
            else:
                module, feature = parts[0], "general"
            doc = json.loads(path.read_text(encoding="utf-8"))
            results.append({
                "module": module,
                "feature": feature,
                "discovered_at": doc.get("discovered_at", "unknown"),
                "api_count": len(doc.get("api_endpoints", {}).get("verified_working", [])),
                "edge_case_count": len(doc.get("edge_cases", [])),
                "file": str(path),
            })
        return results

    def get_context_text(self, module: str, feature: str) -> str:
        """
        Format a discovery document as context text for injection into LLM prompts.
        Returns empty string if no discovery exists.
        """
        doc = self.load(module, feature)
        if not doc:
            return ""

        lines = []
        lines.append("=" * 60)
        lines.append(f"PRODUCT DISCOVERY: {module}/{feature}")
        lines.append(f"(Discovered via live Playwright exploration — AUTHORITATIVE)")
        lines.append("=" * 60)

        # Verified APIs
        endpoints = doc.get("api_endpoints", {})
        working = endpoints.get("verified_working", [])
        broken = endpoints.get("verified_broken", [])
        from_ui = endpoints.get("observed_from_ui", [])

        if working:
            lines.append("\n## Verified Working API Endpoints:")
            for ep in working:
                lines.append(f"  ✅ {ep['method']} {ep['path']}")
                if ep.get("input_format"):
                    lines.append(f"     Input: {json.dumps(ep['input_format'])[:200]}")
                if ep.get("notes"):
                    lines.append(f"     Note: {ep['notes']}")

        if broken:
            lines.append("\n## BROKEN API Endpoints (DO NOT USE):")
            for ep in broken:
                lines.append(f"  ❌ {ep['method']} {ep['path']} → {ep.get('error', 'failed')}")
                if ep.get("notes"):
                    lines.append(f"     Note: {ep['notes']}")

        if from_ui:
            lines.append("\n## API Endpoints Observed from UI (GOLD STANDARD):")
            for ep in from_ui:
                lines.append(f"  🔍 {ep.get('method', '?')} {ep['path']}")
                if ep.get("input_format"):
                    lines.append(f"     Input: {json.dumps(ep['input_format'])[:200]}")
                if ep.get("notes"):
                    lines.append(f"     Note: {ep['notes']}")

        # UI Flow
        ui_flow = doc.get("ui_flow", {})
        steps = ui_flow.get("steps", [])
        if steps:
            lines.append("\n## UI Flow Steps:")
            for step in steps:
                lines.append(f"  {step.get('step', '?')}. {step.get('action', '')}")
                if step.get("locator_hint"):
                    lines.append(f"     Locator hint: {step['locator_hint']}")

        success_msgs = ui_flow.get("success_messages", [])
        if success_msgs:
            lines.append(f"\n  Success messages: {success_msgs}")

        error_msgs = ui_flow.get("error_messages", [])
        if error_msgs:
            lines.append(f"  Error messages: {error_msgs}")

        # DOM observations
        dom_obs = doc.get("dom_observations", {})
        if dom_obs:
            lines.append("\n## DOM Observations:")
            for section_name, section in dom_obs.items():
                lines.append(f"\n  ### {section_name}:")
                if isinstance(section, dict):
                    for key, val in section.items():
                        if key != "notes":
                            lines.append(f"    {key}: {val}")
                    if section.get("notes"):
                        lines.append(f"    ⚠ {section['notes']}")

        # Edge cases
        edge_cases = doc.get("edge_cases", [])
        if edge_cases:
            lines.append("\n## Discovered Edge Cases:")
            for ec in edge_cases:
                lines.append(f"  • {ec.get('scenario', 'unknown')}")
                lines.append(f"    Observed: {ec.get('observed_behavior', '')}")
                if ec.get("api_behavior"):
                    lines.append(f"    API: {ec['api_behavior']}")

        # Locator hints
        locators = doc.get("locator_hints", {})
        if locators:
            lines.append("\n## Locator Hints:")
            for name, xpath in locators.items():
                lines.append(f"  {name}: {xpath}")

        # Existing codebase methods
        existing = doc.get("existing_codebase_methods", {})
        if existing:
            lines.append("\n## Existing Codebase Context:")
            for category, methods in existing.items():
                if category != "notes" and methods:
                    lines.append(f"  {category}: {methods}")
            if existing.get("notes"):
                lines.append(f"  ⚠ {existing['notes']}")

        return "\n".join(lines)

    def get_all_context_for_module(self, module: str) -> str:
        """Get combined context text for all discoveries in a module."""
        parts = []
        for path in sorted(self.discoveries_dir.glob(f"{module}_*.json")):
            if path.name.endswith("_summary.json"):
                continue
            feature = path.stem.split("_", 1)[1] if "_" in path.stem else "general"
            text = self.get_context_text(module, feature)
            if text:
                parts.append(text)
        return "\n\n".join(parts)
