"""
sdp_api_helper.py
-----------------
SDP API data creation helper for Playwright browser sessions.

Enables HealerAgent and UIScoutAgent to create prerequisite test data
via SDP's built-in client-side ``sdpAPICall()`` JavaScript function.

The SDP web application exposes a global ``sdpAPICall(apiPath, method, formData)``
JS function that makes synchronous XHR calls.  This module builds the correct JS
invocations and executes them through Playwright's ``page.evaluate()``.

Two strategies for knowing WHAT data to create:

  1. **Report-based** (preferred):
     Parse a previous ``ScenarioReport.html`` → extract all preProcess POST calls
     with their exact JSON payloads → replay them in the current browser session.

  2. **Data-JSON-based** (fallback):
     Load test input data directly from ``entity/data/<module>/<entity>/<entity>_data.json``,
     resolve placeholders, and create entities using the standard API paths.

Usage (HealerAgent — sync Playwright):
    from agents.sdp_api_helper import SDPAPIHelper
    helper = SDPAPIHelper()
    created = helper.create_prerequisites_sync(page, method_name="verifyAttachParentChangePopup")

Usage (UIScoutAgent — async Playwright):
    from agents.sdp_api_helper import SDPAPIHelper
    helper = SDPAPIHelper()
    created = await helper.create_entity_async(page, module_path="changes/change")
"""

from __future__ import annotations

import glob
import html as html_mod
import json
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from config.project_config import (
    PROJECT_ROOT,
    PROJECT_RES,
    SDP_ADMIN_EMAIL,
    SDP_EMAIL_ID,
)


# ─────────────────────────────────────────────────────────────────────────────
# Module → entity API configuration
# ─────────────────────────────────────────────────────────────────────────────
MODULE_ENTITY_MAP: dict[str, dict[str, str]] = {
    "changes/change": {
        "entity_name": "change",
        "api_path": "changes",
        "data_json": "resources/entity/data/changes/change/change_data.json",
        "default_data_key": "api_valid_input_general_template",
    },
    "requests/request": {
        "entity_name": "request",
        "api_path": "requests",
        "data_json": "resources/entity/data/requests/request/request_data.json",
        "default_data_key": "api_valid_input",
    },
    "solutions/solution": {
        "entity_name": "solution",
        "api_path": "solutions",
        "data_json": "resources/entity/data/solutions/solution/solution_data.json",
        "default_data_key": "sol_unapproved_default_temp",
    },
    "problems/problem": {
        "entity_name": "problem",
        "api_path": "problems",
        "data_json": "resources/entity/data/problems/problem/problem_data.json",
        "default_data_key": "api_valid_input",
    },
    "tasks/task": {
        "entity_name": "task",
        "api_path": "tasks",
        "data_json": "resources/entity/data/tasks/task/task_data.json",
        "default_data_key": "api_valid_input",
    },
    "releases/release": {
        "entity_name": "release",
        "api_path": "releases",
        "data_json": "resources/entity/data/releases/release/release_data.json",
        "default_data_key": "api_valid_input",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Data classes
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class APICallRecord:
    """A single API call extracted from an HTML report."""
    method: str          # POST, GET, PUT, DELETE
    path: str            # e.g. "changes", "changes/8000000065956"
    input_data: dict     # parsed JSON payload (may be empty for DELETE/GET)
    response: dict       # parsed response JSON (may be empty)
    phase: str = "unknown"   # preprocess | test | postprocess
    data_key: str = ""       # the data JSON key used (if available from report)

    def is_create(self) -> bool:
        return self.method == "POST" and "/" not in self.path

    def is_delete(self) -> bool:
        return self.method == "DELETE"

    @property
    def entity_name(self) -> str:
        """Derive singular entity name from API path. 'changes' → 'change'."""
        base = self.path.split("/")[0]
        return base.rstrip("s") if base.endswith("s") else base

    @property
    def created_id(self) -> str:
        """Extract entity ID from the response."""
        ename = self.entity_name
        if ename in self.response:
            entity_obj = self.response[ename]
            if isinstance(entity_obj, dict):
                return str(entity_obj.get("id", ""))
            elif isinstance(entity_obj, list) and entity_obj:
                return str(entity_obj[0].get("id", ""))
        return ""


@dataclass
class CreatedEntity:
    """An entity that was created via the API helper."""
    entity_name: str     # e.g. "change"
    entity_id: str       # e.g. "8000000065944"
    title: str = ""
    display_id: str = ""
    api_path: str = ""   # e.g. "changes"
    extra: dict = field(default_factory=dict)

    def delete_path(self) -> str:
        return f"{self.api_path}/{self.entity_id}"


# ─────────────────────────────────────────────────────────────────────────────
# SDPAPIHelper — main class
# ─────────────────────────────────────────────────────────────────────────────

class SDPAPIHelper:
    """
    Helps Playwright agents create / delete SDP test data through the browser.

    All API calls are made by executing ``sdpAPICall()`` JS in the browser
    context, which requires the browser to be on a valid SDP page with an
    active logged-in session.
    """

    def __init__(self, project_root: str = PROJECT_ROOT):
        self.project_root = Path(project_root)
        self.reports_dir = self.project_root / "reports"
        self.resources_dir = self.project_root / "resources"

    # =====================================================================
    # 1. JavaScript builders
    # =====================================================================

    @staticmethod
    def build_create_js(api_path: str, entity_data: dict) -> str:
        """
        Build JS code that calls ``sdpAPICall()`` to POST (create) an entity.

        Parameters
        ----------
        api_path : str
            The API path, e.g. ``"changes"``, ``"requests"``.
        entity_data : dict
            The full input payload, already wrapped.
            E.g. ``{"change": {"title": "Test", ...}}``.

        Returns
        -------
        str
            JavaScript source to be executed via ``page.evaluate()``.
        """
        json_str = json.dumps(entity_data, ensure_ascii=False)
        # sdpAPICall signature: sdpAPICall(apiPath, method, formDataString)
        # formDataString: 'input_data='+encodeURIComponent(JSON.stringify({...}))
        return f"""
            () => {{
                try {{
                    const payload = {json_str};
                    const formData = 'input_data=' + encodeURIComponent(JSON.stringify(payload));
                    const result = sdpAPICall('{api_path}', 'post', formData);
                    return result ? result.responseJSON : null;
                }} catch (e) {{
                    return {{ error: e.message || String(e) }};
                }}
            }}
        """

    @staticmethod
    def build_get_js(api_path: str, search_criteria: dict | None = None) -> str:
        """Build JS for a GET API call."""
        if search_criteria:
            json_str = json.dumps(search_criteria, ensure_ascii=False)
            return f"""
                () => {{
                    try {{
                        const payload = {json_str};
                        const formData = 'input_data=' + encodeURIComponent(JSON.stringify(payload));
                        const result = sdpAPICall('{api_path}', 'get', formData);
                        return result ? result.responseJSON : null;
                    }} catch (e) {{
                        return {{ error: e.message || String(e) }};
                    }}
                }}
            """
        return f"""
            () => {{
                try {{
                    const result = sdpAPICall('{api_path}', 'get');
                    return result ? result.responseJSON : null;
                }} catch (e) {{
                    return {{ error: e.message || String(e) }};
                }}
            }}
        """

    @staticmethod
    def build_update_js(api_path: str, entity_data: dict) -> str:
        """Build JS for a PUT (update) API call."""
        json_str = json.dumps(entity_data, ensure_ascii=False)
        return f"""
            () => {{
                try {{
                    const payload = {json_str};
                    const formData = 'input_data=' + encodeURIComponent(JSON.stringify(payload));
                    const result = sdpAPICall('{api_path}', 'put', formData);
                    return result ? result.responseJSON : null;
                }} catch (e) {{
                    return {{ error: e.message || String(e) }};
                }}
            }}
        """

    @staticmethod
    def build_delete_js(api_path: str) -> str:
        """
        Build JS for a DELETE API call.

        Note: SDP uses 'del' (not 'delete') as the HTTP method name.
        """
        return f"""
            () => {{
                try {{
                    const result = sdpAPICall('{api_path}', 'del');
                    return result ? result.responseJSON : null;
                }} catch (e) {{
                    return {{ error: e.message || String(e) }};
                }}
            }}
        """

    # =====================================================================
    # 2. Report parsing — extract API calls from ScenarioReport.html
    # =====================================================================

    def find_latest_report(self, method_name: str) -> str | None:
        """
        Find the most recent ScenarioReport.html for a given test method.

        Scans ``{PROJECT_ROOT}/reports/LOCAL_{methodName}_*/ScenarioReport.html``
        and returns the one with the highest timestamp.
        """
        pattern = str(self.reports_dir / f"LOCAL_{method_name}_*" / "ScenarioReport.html")
        reports = glob.glob(pattern)
        if not reports:
            # Also check non-LOCAL pattern
            pattern = str(self.reports_dir / f"{method_name}_*" / "ScenarioReport.html")
            reports = glob.glob(pattern)
        if not reports:
            return None
        # Sort by modification time (most recent last)
        reports.sort(key=os.path.getmtime)
        return reports[-1]

    def parse_report_api_calls(self, report_path: str) -> list[APICallRecord]:
        """
        Parse a ScenarioReport.html and extract all API call records.

        The report HTML contains a flat sequence of div blocks:
          - ``rest_api`` class: "Trigger POST call for the path changes"
          - ``debug`` class: "Formdata for debugging{input_data=...}"
          - ``debug`` class: "Response String for debugging{...}"

        We also look for ``"Fetching data from the file ... with the testcase id ..."``
        lines to annotate which data JSON key was used.

        Returns a list of APICallRecord objects with ``phase`` set to
        ``"preprocess"``, ``"test"``, or ``"postprocess"``.
        """
        try:
            raw_html = Path(report_path).read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"[SDPAPIHelper] ⚠ Cannot read report: {e}")
            return []

        # IMPORTANT: parse from RAW HTML.  Response strings from POST calls
        # contain notification-template HTML (literal <div>…</div> tags) that
        # break a simple (.*?)</div> regex.  We therefore:
        #   1. Match *only* up to the opening of the automater-step-message div,
        #   2. Use div-depth counting to find the **real** closing </div>,
        #   3. Strip HTML tags and unescape entities on the extracted content.

        calls: list[APICallRecord] = []
        current_data_key = ""

        # ── Split into message divs ──────────────────────────────────
        # Step 1: locate each <div …automater-step-message…> opening.
        msg_start_pattern = re.compile(
            r'<div\s+class="([^"]*?)"[^>]*id="([^"]*?)"[^>]*>'
            r'.*?<div\s+class="[^"]*automater-step-message[^"]*">',
            re.DOTALL,
        )

        messages: list[tuple[str, str, str]] = []  # (classes, id, message_text)
        for m in msg_start_pattern.finditer(raw_html):
            classes = m.group(1)
            div_id = m.group(2)

            # Step 2: depth-counting from the end of the match (right after '>').
            content_start = m.end()
            depth = 1
            pos = content_start
            content_end = len(raw_html)  # fallback
            while pos < len(raw_html) and depth > 0:
                next_open = raw_html.find('<div', pos)
                next_close = raw_html.find('</div>', pos)
                if next_close == -1:
                    break  # malformed HTML — take everything
                if next_open != -1 and next_open < next_close:
                    depth += 1
                    pos = next_open + 4
                else:
                    depth -= 1
                    if depth == 0:
                        content_end = next_close
                        break
                    pos = next_close + 6

            msg_raw = raw_html[content_start:content_end].strip()

            # Step 3: strip inner HTML tags then unescape entities (&quot; → ")
            msg_clean = re.sub(r'<[^>]+>', '', msg_raw).strip()
            msg_clean = html_mod.unescape(msg_clean)
            messages.append((classes, div_id, msg_clean))

        # ── Parse messages into API call records ─────────────────────
        i = 0
        first_ui_action_seen = False
        delete_phase_started = False

        while i < len(messages):
            classes, div_id, msg = messages[i]

            # Track data key from "Fetching data from the file..."
            fetch_match = re.search(
                r'Fetching data from the file\s+\S+\s+with the testcase id\s+(\S+)',
                msg,
            )
            if fetch_match:
                current_data_key = fetch_match.group(1)

            # Detect phase boundaries
            if not first_ui_action_seen and "rest_api" not in classes and "debug" not in classes and "storage" not in classes:
                # Check if this is a UI action (navigating, clicking, filling, etc.)
                ui_keywords = [
                    "navigat", "click", "fill", "enter", "select", "open",
                    "wait", "check", "verify", "assert", "validate",
                ]
                if any(kw in msg.lower() for kw in ui_keywords):
                    first_ui_action_seen = True

            # Parse rest_api divs
            if "rest_api" in classes:
                api_match = re.search(
                    r'Trigger\s+(\w+)\s+call for the path\s+(.+?)$',
                    msg,
                )
                if api_match:
                    method = api_match.group(1).upper()
                    path = api_match.group(2).strip()

                    # Determine phase
                    if method == "DELETE":
                        delete_phase_started = True
                    if delete_phase_started:
                        phase = "postprocess"
                    elif first_ui_action_seen:
                        phase = "test"
                    else:
                        phase = "preprocess"

                    # Look ahead for formdata and response in next debug divs
                    input_data: dict = {}
                    response: dict = {}

                    for j in range(i + 1, min(i + 6, len(messages))):
                        _, _, next_msg = messages[j]

                        # Formdata
                        if next_msg.startswith("Formdata for debugging"):
                            fd_match = re.search(
                                r'Formdata for debugging\{input_data=(.*)\}$',
                                next_msg,
                            )
                            if fd_match:
                                try:
                                    input_data = json.loads(fd_match.group(1))
                                except json.JSONDecodeError:
                                    # Try to fix common JSON issues
                                    raw = fd_match.group(1)
                                    try:
                                        input_data = json.loads(raw.rstrip("}"))
                                    except Exception:
                                        input_data = {"_raw": raw[:500]}

                        # Response
                        if next_msg.startswith("Response String for debugging"):
                            resp_str = next_msg[len("Response String for debugging"):]
                            # Escape control chars (newlines/tabs from notification
                            # template HTML that survive into the JSON string values).
                            resp_str_safe = re.sub(
                                r'[\x00-\x1f\x7f]',
                                lambda c: '\\u{:04x}'.format(ord(c.group())),
                                resp_str,
                            )
                            try:
                                response = json.loads(resp_str_safe)
                            except json.JSONDecodeError:
                                # Truncated responses — try partial parse via brace counting
                                try:
                                    brace_count = 0
                                    end_idx = 0
                                    for ci, ch in enumerate(resp_str_safe):
                                        if ch == '{':
                                            brace_count += 1
                                        elif ch == '}':
                                            brace_count -= 1
                                            if brace_count == 0:
                                                end_idx = ci + 1
                                                break
                                    if end_idx > 0:
                                        response = json.loads(resp_str_safe[:end_idx])
                                except Exception:
                                    response = {"_raw": resp_str[:500]}

                        # Stop lookahead when we hit another rest_api div
                        if "rest_api" in messages[j][0]:
                            break

                    calls.append(APICallRecord(
                        method=method,
                        path=path,
                        input_data=input_data,
                        response=response,
                        phase=phase,
                        data_key=current_data_key,
                    ))
                    current_data_key = ""

            i += 1

        print(f"[SDPAPIHelper] Parsed {len(calls)} API calls from report "
              f"(preprocess={sum(1 for c in calls if c.phase == 'preprocess')}, "
              f"test={sum(1 for c in calls if c.phase == 'test')}, "
              f"postprocess={sum(1 for c in calls if c.phase == 'postprocess')})")
        return calls

    def get_preprocess_creates(self, report_path: str) -> list[APICallRecord]:
        """Get only the POST calls from the preprocess phase."""
        all_calls = self.parse_report_api_calls(report_path)
        return [c for c in all_calls if c.phase == "preprocess" and c.method == "POST"]

    # =====================================================================
    # 3. Data JSON loading & placeholder resolution
    # =====================================================================

    def load_data_json(
        self,
        module_path: str,
        data_key: str | None = None,
    ) -> dict:
        """
        Load test data from the entity's data JSON file.

        Parameters
        ----------
        module_path : str
            Module path like ``"changes/change"`` or ``"solutions/solution"``.
        data_key : str, optional
            The specific data entry key. If None, uses the default from
            MODULE_ENTITY_MAP.

        Returns
        -------
        dict
            The ``"data"`` sub-object of the test case entry.
        """
        config = MODULE_ENTITY_MAP.get(module_path)
        if not config:
            print(f"[SDPAPIHelper] ⚠ Unknown module_path: {module_path}")
            return {}

        key = data_key or config["default_data_key"]
        json_path = self.project_root / config["data_json"]

        if not json_path.exists():
            print(f"[SDPAPIHelper] ⚠ Data JSON not found: {json_path}")
            return {}

        try:
            with open(json_path, encoding="utf-8") as f:
                all_data = json.load(f)
            entry = all_data.get(key, {})
            return entry.get("data", entry)
        except Exception as e:
            print(f"[SDPAPIHelper] ⚠ Error loading data JSON: {e}")
            return {}

    @staticmethod
    def resolve_placeholders(
        data: dict,
        context: dict | None = None,
        admin_email: str = SDP_ADMIN_EMAIL,
        user_email: str = SDP_EMAIL_ID,
    ) -> dict:
        """
        Resolve common placeholders in test data.

        Handled placeholders:
          - ``$(unique_string)`` → current millisecond timestamp
          - ``$(custom_X)`` → lookup key ``X`` in ``context`` dict
          - ``$(user_email_id)`` → ``user_email``
          - ``$(admin_email_id)`` → ``admin_email``
          - ``$(date, ...)`` and ``$(datetime, ...)`` → future timestamp

        Parameters
        ----------
        data : dict
            The test data dictionary (modified in-place and returned).
        context : dict, optional
            Key-value pairs for ``$(custom_*)`` resolution (like LocalStorage).
        admin_email : str
            Email for ``$(admin_email_id)`` placeholder.
        user_email : str
            Email for ``$(user_email_id)`` placeholder.
        """
        context = context or {}
        unique = str(int(time.time() * 1000))

        def _resolve_value(val: Any) -> Any:
            if isinstance(val, str):
                # $(unique_string)
                val = val.replace("$(unique_string)", unique)
                # $(user_email_id)
                val = val.replace("$(user_email_id)", user_email)
                # $(admin_email_id)
                val = val.replace("$(admin_email_id)", admin_email)
                # $(custom_X) → looks up 'X' in context
                custom_match = re.findall(r'\$\(custom_(\w+)\)', val)
                for key in custom_match:
                    replacement = context.get(key, f"MISSING_{key}")
                    val = val.replace(f"$(custom_{key})", str(replacement))
                # $(datetime, ...) → far-future timestamp (safe default)
                if re.search(r'\$\(datetime?,', val):
                    # Generate a timestamp ~3 years in the future
                    future_ms = str(int(time.time() * 1000) + 100_000_000_000)
                    val = re.sub(r'\$\(datetime?,\s*[^)]+\)', future_ms, val)
                # $(date, ...) → date string
                if re.search(r'\$\(date,', val):
                    from datetime import datetime, timedelta
                    future = datetime.now() + timedelta(days=365)
                    val = re.sub(r'\$\(date,\s*[^)]+\)', future.strftime("%b %d, %Y"), val)
                return val
            elif isinstance(val, dict):
                return {k: _resolve_value(v) for k, v in val.items()}
            elif isinstance(val, list):
                return [_resolve_value(item) for item in val]
            return val

        return _resolve_value(data)

    # =====================================================================
    # 4. Sync execution (HealerAgent — playwright.sync_api)
    # =====================================================================

    def create_entity_sync(
        self,
        page,
        api_path: str,
        entity_data: dict,
        entity_name: str = "",
    ) -> CreatedEntity | None:
        """
        Create a single entity via the browser's ``sdpAPICall()``.

        Parameters
        ----------
        page : playwright.sync_api.Page
            An active Playwright page with a logged-in SDP session.
        api_path : str
            API path, e.g. ``"changes"``.
        entity_data : dict
            The full wrapped payload, e.g. ``{"change": {"title": "..."}}``.
        entity_name : str, optional
            Entity name for parsing the response (e.g. "change").
            If empty, inferred from api_path.

        Returns
        -------
        CreatedEntity or None
        """
        if not entity_name:
            entity_name = api_path.rstrip("s") if api_path.endswith("s") else api_path

        js = self.build_create_js(api_path, entity_data)
        print(f"[SDPAPIHelper] 📡 POST {api_path} (sync)...")

        try:
            result = page.evaluate(js)
        except Exception as e:
            print(f"[SDPAPIHelper] ⚠ JS execution failed: {e}")
            return None

        if not result or isinstance(result, dict) and "error" in result:
            print(f"[SDPAPIHelper] ⚠ API call failed: {result}")
            return None

        # Check response status
        status = result.get("response_status", {})
        if isinstance(status, list):
            status = status[0] if status else {}
        if status.get("status_code") != 2000 and status.get("status") != "success":
            print(f"[SDPAPIHelper] ⚠ API returned non-success: {status}")
            return None

        entity_obj = result.get(entity_name, {})
        entity_id = str(entity_obj.get("id", ""))
        title = entity_obj.get("title", entity_obj.get("name", ""))
        display_id = ""
        if "display_id" in entity_obj:
            di = entity_obj["display_id"]
            display_id = di.get("display_value", str(di)) if isinstance(di, dict) else str(di)

        created = CreatedEntity(
            entity_name=entity_name,
            entity_id=entity_id,
            title=title,
            display_id=display_id,
            api_path=api_path,
            extra=entity_obj,
        )
        print(f"[SDPAPIHelper] ✅ Created {entity_name} id={entity_id} title='{title}' display_id='{display_id}'")
        return created

    def delete_entity_sync(self, page, api_path: str, entity_id: str) -> bool:
        """Delete a single entity via the browser API (sync)."""
        delete_path = f"{api_path}/{entity_id}"
        js = self.build_delete_js(delete_path)
        print(f"[SDPAPIHelper] 🗑 DELETE {delete_path} (sync)...")
        try:
            result = page.evaluate(js)
            if result:
                status = result.get("response_status", {})
                if isinstance(status, list):
                    status = status[0] if status else {}
                if status.get("status_code") == 2000 or status.get("status") == "success":
                    print(f"[SDPAPIHelper] ✅ Deleted {delete_path}")
                    return True
            print(f"[SDPAPIHelper] ⚠ Delete may have failed: {result}")
            return False
        except Exception as e:
            print(f"[SDPAPIHelper] ⚠ Delete error: {e}")
            return False

    def create_prerequisites_sync(
        self,
        page,
        method_name: str,
        context: dict | None = None,
    ) -> list[CreatedEntity]:
        """
        Recreate all preProcess entities from the latest report for this method.

        This is the primary integration point for HealerAgent:
        after login and before replaying navigation steps, call this to
        ensure all prerequisite data exists.

        Parameters
        ----------
        page : playwright.sync_api.Page
        method_name : str
            The test method name, e.g. ``"verifyAttachParentChangePopup"``.
        context : dict, optional
            Pre-populated context for placeholder resolution.

        Returns
        -------
        list[CreatedEntity]
            All entities that were successfully created.
        """
        report = self.find_latest_report(method_name)
        if not report:
            print(f"[SDPAPIHelper] ⚠ No report found for method '{method_name}' — cannot replay prerequisites")
            return []

        print(f"[SDPAPIHelper] 📋 Replaying preProcess from report: {report}")
        creates = self.get_preprocess_creates(report)
        if not creates:
            print("[SDPAPIHelper] No preProcess POST calls found in report")
            return []

        created_entities: list[CreatedEntity] = []
        local_storage: dict[str, str] = dict(context or {})

        for call in creates:
            payload = call.input_data
            if not payload:
                print(f"[SDPAPIHelper] ⚠ Skipping call with empty payload: {call.method} {call.path}")
                continue

            # For replaying, use the ORIGINAL payload but regenerate unique strings
            # so we don't collide with existing entities
            payload = self._refresh_unique_strings(payload)

            entity_name = call.entity_name
            created = self.create_entity_sync(page, call.path, payload, entity_name)
            if created:
                created_entities.append(created)
                # Build context keys matching the Java LocalStorage conventions
                local_storage[entity_name] = created.entity_id
                local_storage[f"{entity_name}Id"] = created.entity_id
                local_storage[f"{entity_name}Name"] = created.title
                if created.display_id:
                    local_storage[f"{entity_name}DisplayValue"] = created.display_id

                # For numbered target entities (target 1, 2, ...)
                idx = len([e for e in created_entities if e.entity_name == entity_name])
                if idx > 1:
                    suffix = str(idx - 1)
                    local_storage[f"target{entity_name.capitalize()}Id{suffix}"] = created.entity_id
                    local_storage[f"target{entity_name.capitalize()}Name{suffix}"] = created.title
                    if created.display_id:
                        local_storage[f"target{entity_name.capitalize()}DisplayValue{suffix}"] = created.display_id

        print(f"[SDPAPIHelper] ✅ Created {len(created_entities)} prerequisite entities")
        if local_storage:
            print(f"[SDPAPIHelper] LocalStorage context: {json.dumps(local_storage, indent=2)}")
        return created_entities

    def create_from_data_json_sync(
        self,
        page,
        module_path: str,
        data_key: str | None = None,
        context: dict | None = None,
    ) -> CreatedEntity | None:
        """
        Create an entity using data loaded from the entity's data JSON file.

        Useful as a fallback when no report is available.

        Parameters
        ----------
        page : playwright.sync_api.Page
        module_path : str
            Module path like ``"changes/change"``.
        data_key : str, optional
            Data entry key. Uses default if not provided.
        context : dict, optional
            For placeholder resolution.
        """
        config = MODULE_ENTITY_MAP.get(module_path)
        if not config:
            print(f"[SDPAPIHelper] ⚠ Unknown module: {module_path}")
            return None

        entity_name = config["entity_name"]
        api_path = config["api_path"]

        data = self.load_data_json(module_path, data_key)
        if not data:
            print(f"[SDPAPIHelper] ⚠ No data loaded for {module_path}/{data_key}")
            return None

        resolved = self.resolve_placeholders(data, context)
        wrapped = {entity_name: resolved}
        return self.create_entity_sync(page, api_path, wrapped, entity_name)

    # =====================================================================
    # 5. Async execution (UIScoutAgent — playwright.async_api)
    # =====================================================================

    async def create_entity_async(
        self,
        page,
        api_path: str,
        entity_data: dict,
        entity_name: str = "",
    ) -> CreatedEntity | None:
        """Create a single entity via the browser API (async)."""
        if not entity_name:
            entity_name = api_path.rstrip("s") if api_path.endswith("s") else api_path

        js = self.build_create_js(api_path, entity_data)
        print(f"[SDPAPIHelper] 📡 POST {api_path} (async)...")

        try:
            result = await page.evaluate(js)
        except Exception as e:
            print(f"[SDPAPIHelper] ⚠ JS execution failed: {e}")
            return None

        if not result or isinstance(result, dict) and "error" in result:
            print(f"[SDPAPIHelper] ⚠ API call failed: {result}")
            return None

        status = result.get("response_status", {})
        if isinstance(status, list):
            status = status[0] if status else {}
        if status.get("status_code") != 2000 and status.get("status") != "success":
            print(f"[SDPAPIHelper] ⚠ API returned non-success: {status}")
            return None

        entity_obj = result.get(entity_name, {})
        entity_id = str(entity_obj.get("id", ""))
        title = entity_obj.get("title", entity_obj.get("name", ""))
        display_id = ""
        if "display_id" in entity_obj:
            di = entity_obj["display_id"]
            display_id = di.get("display_value", str(di)) if isinstance(di, dict) else str(di)

        created = CreatedEntity(
            entity_name=entity_name,
            entity_id=entity_id,
            title=title,
            display_id=display_id,
            api_path=api_path,
            extra=entity_obj,
        )
        print(f"[SDPAPIHelper] ✅ Created {entity_name} id={entity_id} title='{title}'")
        return created

    async def delete_entity_async(self, page, api_path: str, entity_id: str) -> bool:
        """Delete a single entity via the browser API (async)."""
        delete_path = f"{api_path}/{entity_id}"
        js = self.build_delete_js(delete_path)
        print(f"[SDPAPIHelper] 🗑 DELETE {delete_path} (async)...")
        try:
            result = await page.evaluate(js)
            if result:
                status = result.get("response_status", {})
                if isinstance(status, list):
                    status = status[0] if status else {}
                if status.get("status_code") == 2000 or status.get("status") == "success":
                    print(f"[SDPAPIHelper] ✅ Deleted {delete_path}")
                    return True
            return False
        except Exception as e:
            print(f"[SDPAPIHelper] ⚠ Delete error: {e}")
            return False

    async def create_prerequisites_async(
        self,
        page,
        method_name: str | None = None,
        module_path: str | None = None,
        data_key: str | None = None,
        context: dict | None = None,
    ) -> list[CreatedEntity]:
        """
        Create prerequisite entities for UIScoutAgent.

        Tries two strategies:
          1. If ``method_name`` is given, replay from the latest report.
          2. Otherwise, create a simple entity from data JSON.
        """
        created: list[CreatedEntity] = []

        # Strategy 1: replay from report
        if method_name:
            report = self.find_latest_report(method_name)
            if report:
                print(f"[SDPAPIHelper] 📋 Replaying preProcess from report (async): {report}")
                creates = self.get_preprocess_creates(report)
                for call in creates:
                    payload = call.input_data
                    if not payload:
                        continue
                    payload = self._refresh_unique_strings(payload)
                    entity = await self.create_entity_async(page, call.path, payload, call.entity_name)
                    if entity:
                        created.append(entity)
                if created:
                    return created

        # Strategy 2: create from data JSON
        if module_path:
            config = MODULE_ENTITY_MAP.get(module_path)
            if config:
                entity_name = config["entity_name"]
                api_path = config["api_path"]
                data = self.load_data_json(module_path, data_key)
                if data:
                    resolved = self.resolve_placeholders(data, context)
                    wrapped = {entity_name: resolved}
                    entity = await self.create_entity_async(page, api_path, wrapped, entity_name)
                    if entity:
                        created.append(entity)

        return created

    async def cleanup_entities_async(self, page, entities: list[CreatedEntity]) -> None:
        """Delete all created entities (cleanup after scouting)."""
        for entity in reversed(entities):
            await self.delete_entity_async(page, entity.api_path, entity.entity_id)

    def cleanup_entities_sync(self, page, entities: list[CreatedEntity]) -> None:
        """Delete all created entities (cleanup after healing)."""
        for entity in reversed(entities):
            self.delete_entity_sync(page, entity.api_path, entity.entity_id)

    # =====================================================================
    # 6. Utility methods
    # =====================================================================

    @staticmethod
    def _refresh_unique_strings(payload: dict) -> dict:
        """
        Replace timestamp-like unique strings in a payload with fresh ones.

        When replaying API calls from a past report, the titles contain old
        timestamps (e.g. "Linking Change 1772516756509"). We replace those
        with a current timestamp so the new entities have unique names.
        """
        unique = str(int(time.time() * 1000))

        def _replace(val: Any) -> Any:
            if isinstance(val, str):
                # Replace 13-digit timestamps in strings
                return re.sub(r'\b1[6-9]\d{11}\b', unique, val)
            elif isinstance(val, dict):
                return {k: _replace(v) for k, v in val.items()}
            elif isinstance(val, list):
                return [_replace(item) for item in val]
            return val

        return _replace(payload)

    def get_entity_context_for_llm(self, method_name: str) -> str:
        """
        Build a concise text description of prerequisite API calls for LLM consumption.

        Used by HealerAgent and UIScoutAgent to inform the LLM about what data
        needs to exist and how it was created.
        """
        report = self.find_latest_report(method_name)
        if not report:
            return "No previous report found — cannot determine prerequisite data."

        creates = self.get_preprocess_creates(report)
        if not creates:
            return "No preProcess API calls found in the report."

        lines = [
            f"## Prerequisite Data (from report)",
            f"The test method '{method_name}' requires the following entities to be created via API:",
            "",
        ]
        for i, call in enumerate(creates, 1):
            lines.append(f"### Entity {i}: {call.method} /{call.path}")
            if call.data_key:
                lines.append(f"Data key: `{call.data_key}`")
            lines.append(f"Payload: ```json\n{json.dumps(call.input_data, indent=2)[:500]}\n```")
            if call.response and call.entity_name in call.response:
                entity = call.response[call.entity_name]
                lines.append(f"Created ID: {entity.get('id', 'unknown')}")
                lines.append(f"Created title: {entity.get('title', entity.get('name', 'unknown'))}")
            lines.append("")

        lines.append(
            "These entities can be recreated via JavaScript in the browser:\n"
            "```javascript\n"
            "sdpAPICall('apiPath', 'post', 'input_data=' + encodeURIComponent(JSON.stringify(payload))).responseJSON\n"
            "```\n"
            "Note: 'del' (not 'delete') is used for DELETE calls.\n"
        )
        return "\n".join(lines)

    def get_sdp_api_cheatsheet(self) -> str:
        """
        Return a concise cheatsheet of SDP API patterns for LLM prompts.

        Informs the LLM how ``sdpAPICall()`` works so it can construct
        correct API calls during healing or scouting.
        """
        return """## SDP Browser API — sdpAPICall() Reference

SDP exposes a global JS function `sdpAPICall(apiPath, method, formData)` in the browser.
It makes synchronous XHR calls and returns `{responseJSON: <parsed JSON>}`.

### Method mapping (CRITICAL — use lowercase):
- POST   → 'post'
- GET    → 'get'
- PUT    → 'put'
- DELETE → 'del'   (NOT 'delete'!)

### Create entity (POST):
```javascript
const result = sdpAPICall('changes', 'post',
    'input_data=' + encodeURIComponent(JSON.stringify({
        "change": { "title": "My Change", "template": {"name": "General Template"} }
    }))
);
const entity = result.responseJSON.change;  // {id: "800...", title: "My Change", ...}
```

### Get entity (GET with criteria):
```javascript
const result = sdpAPICall('changes', 'get',
    'input_data=' + encodeURIComponent(JSON.stringify({
        "list_info": {"search_criteria": {"field": "title", "condition": "is", "value": "My Change"}}
    }))
);
```

### Delete entity (DELETE):
```javascript
sdpAPICall('changes/8000000065944', 'del');
```

### Common API paths:
| Entity   | POST path  | Wrapper key    |
|----------|-----------|----------------|
| Change   | changes   | {"change":{}}  |
| Request  | requests  | {"request":{}} |
| Solution | solutions | {"solution":{}}|
| Problem  | problems  | {"problem":{}} |
| Task     | tasks     | {"task":{}}    |

### Response format:
```json
{
    "response_status": {"status_code": 2000, "status": "success"},
    "change": {"id": "8000000065944", "title": "...", "display_id": {"display_value": "CH-14"}}
}
```
status_code 2000 = success. Any other code = failure.
"""
