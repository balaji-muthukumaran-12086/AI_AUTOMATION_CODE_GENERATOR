"""
ui_scout_agent.py
-----------------
UI Scout Agent — Proactive Playwright-based UI behaviour observer.

Runs BEFORE the Coder Agent to surf the actual SDP application and capture
real UI state observations that static help docs cannot provide.

What it does:
  1. Logs into the SDP instance as admin
  2. For each planned scenario module, navigates to the relevant UI flows
  3. At each significant interaction point, captures:
       - Visible form fields
       - Visible submit/action buttons
       - State changes after clicking checkboxes/toggles
       - Required field markers
  4. Feeds structured "UI observations" into the Coder Agent's context so
     the LLM knows the REAL behaviour (e.g. which buttons appear before/after
     clicking "Publish in Self-Service Portal")

Pipeline position:
  planner → coverage → [UIScoutAgent] → coder → reviewer → output

Key insight: The healer fixes AFTER failure; the scout PREVENTS failure by
observing before code is written.
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ── Path bootstrap — ensure repo root is on sys.path before local imports ──
_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))
# ──────────────────────────────────────────────────────────────────────────

from langchain_core.messages import SystemMessage, HumanMessage

from agents.llm_factory import get_llm
from agents.state import AgentState

# ── Defaults ───────────────────────────────────────────────────────────────────
DEFAULT_URL         = "https://sdpodqa-auto1.csez.zohocorpin.com:9090/"
DEFAULT_PORTAL      = "portal1"
DEFAULT_ADMIN_EMAIL = "jaya.kumar+org1admin1t0@zohotest.com"
DEFAULT_ADMIN_PASS  = "Zoho@135"

SCOUT_SCREENSHOTS_DIR = "knowledge_base/scout_snapshots"

# Maps module_path segment → SDP URL path + key interactions to scout
MODULE_SCOUT_PLANS: dict[str, dict] = {
    "solutions/solution": {
        "module_url": "solutions",
        "flows": [
            {
                "name": "new_solution_form_initial",
                "description": "Observe the New Solution form BEFORE clicking Publish checkbox",
                "steps": [
                    {"action": "navigate_module"},
                    {"action": "click_new"},
                ],
            },
            {
                "name": "new_solution_form_after_publish",
                "description": "Observe the New Solution form AFTER clicking Publish in Self-Service Portal",
                "steps": [
                    {"action": "navigate_module"},
                    {"action": "click_new"},
                    {"action": "click", "selector": "//input[@id='is_public']//following::span", "label": "click_publish_checkbox"},
                ],
            },
        ],
    },
    "requests/request": {
        "module_url": "requests",
        "flows": [
            {
                "name": "new_request_form",
                "description": "Observe New Request form fields and buttons",
                "steps": [
                    {"action": "navigate_module"},
                    {"action": "click_new"},
                ],
            },
        ],
    },
    "problems/problem": {
        "module_url": "problems",
        "flows": [
            {
                "name": "new_problem_form",
                "description": "Observe New Problem form",
                "steps": [
                    {"action": "navigate_module"},
                    {"action": "click_new"},
                ],
            },
        ],
    },
    "changes/change": {
        "module_url": "changes",
        "flows": [
            {
                "name": "new_change_form",
                "description": "Observe New Change form",
                "steps": [
                    {"action": "navigate_module"},
                    {"action": "click_new"},
                ],
            },
        ],
    },
}

# ── UI Observation container ───────────────────────────────────────────────────

class UIObservation:
    """Holds a single UI state observation from a scout flow."""

    def __init__(
        self,
        flow_name: str,
        description: str,
        visible_buttons: list[str],
        visible_fields: list[str],
        required_fields: list[str],
        checkboxes: list[dict],
        raw_snapshot: str,
        screenshot_path: str = "",
        notes: list[str] = None,
    ):
        self.flow_name       = flow_name
        self.description     = description
        self.visible_buttons = visible_buttons
        self.visible_fields  = visible_fields
        self.required_fields = required_fields
        self.checkboxes      = checkboxes        # [{label, checked, effect}]
        self.raw_snapshot    = raw_snapshot
        self.screenshot_path = screenshot_path
        self.notes           = notes or []

    def to_dict(self) -> dict:
        return {
            "flow_name":       self.flow_name,
            "description":     self.description,
            "visible_buttons": self.visible_buttons,
            "visible_fields":  self.visible_fields,
            "required_fields": self.required_fields,
            "checkboxes":      self.checkboxes,
            "notes":           self.notes,
            "screenshot_path": self.screenshot_path,
        }

    def to_context_text(self) -> str:
        """Format for injection into the Coder Agent's LLM prompt."""
        lines = [
            f"  ── Flow: {self.flow_name} ──",
            f"  {self.description}",
        ]
        if self.visible_buttons:
            lines.append(f"  Visible buttons : {', '.join(self.visible_buttons)}")
        if self.visible_fields:
            lines.append(f"  Visible fields  : {', '.join(self.visible_fields[:15])}")
        if self.required_fields:
            lines.append(f"  Required fields : {', '.join(self.required_fields)}")
        if self.checkboxes:
            for cb in self.checkboxes:
                lines.append(f"  Checkbox '{cb.get('label')}' (checked={cb.get('checked')}) → {cb.get('effect', '')}")
        for note in self.notes:
            lines.append(f"  ⚠ NOTE: {note}")
        return "\n".join(lines)


# ── Scout Agent ────────────────────────────────────────────────────────────────

class UIScoutAgent:
    """
    Proactive Playwright-based UI behaviour observer.
    Runs before code generation to capture real application behaviour.
    """

    def __init__(
        self,
        base_dir: str = None,
        url: str = DEFAULT_URL,
        portal: str = DEFAULT_PORTAL,
        admin_email: str = DEFAULT_ADMIN_EMAIL,
        admin_password: str = DEFAULT_ADMIN_PASS,
        headless: bool = True,
    ):
        self.base           = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self.url            = url.rstrip("/") + "/"
        self.portal         = portal
        self.admin_email    = admin_email
        self.admin_password = admin_password
        self.headless       = headless
        self.llm            = get_llm(temperature=0.0)
        self.screenshots_dir = self.base / SCOUT_SCREENSHOTS_DIR
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)

    # ── LangGraph node entry point ─────────────────────────────────────────

    def run(self, state: AgentState) -> AgentState:
        """
        LangGraph node: called between coverage and coder.
        Reads  : state['test_plan']    → { module_path: [scenarios] }
        Writes : state['ui_observations'] → { module_path: [UIObservation.to_dict()] }
                 state['messages']     += [summary]
        """
        test_plan = state.get("test_plan", {})
        if not test_plan:
            state["ui_observations"] = {}
            return state

        run_config = state.get("run_config", {})
        url          = run_config.get("url", self.url)
        portal       = run_config.get("portal_name", self.portal)
        admin_email  = run_config.get("admin_mail_id", self.admin_email)

        print("[UIScoutAgent] 🔍 Scouting application UI before code generation...")
        all_observations: dict[str, list] = {}

        for module_path in test_plan.keys():
            print(f"[UIScoutAgent] Scouting module: {module_path}")
            plan = self._resolve_scout_plan(module_path)
            if not plan:
                print(f"[UIScoutAgent] No scout plan for {module_path} — generating via LLM...")
                plan = self._infer_scout_plan(module_path, test_plan[module_path])

            observations = self._scout_module(
                module_path=module_path,
                scout_plan=plan,
                url=url,
                portal=portal,
                admin_email=admin_email,
            )
            all_observations[module_path] = [o.to_dict() for o in observations]
            print(f"[UIScoutAgent] ✅ {module_path}: {len(observations)} observations captured")

        state["ui_observations"] = all_observations
        summary = f"[UIScoutAgent] Scouted {len(all_observations)} module(s), " \
                  f"captured {sum(len(v) for v in all_observations.values())} UI observations."
        state["messages"] = [summary]
        print(summary)
        return state

    # ── Module scouting ────────────────────────────────────────────────────

    def _scout_module(
        self,
        module_path: str,
        scout_plan: dict,
        url: str,
        portal: str,
        admin_email: str,
    ) -> list[UIObservation]:
        """Run all scout flows for a module and return observations."""
        return asyncio.run(self._async_scout_module(module_path, scout_plan, url, portal, admin_email))

    async def _async_scout_module(
        self,
        module_path: str,
        scout_plan: dict,
        url: str,
        portal: str,
        admin_email: str,
    ) -> list[UIObservation]:
        from playwright.async_api import async_playwright

        observations: list[UIObservation] = []
        module_url_segment = scout_plan.get("module_url", module_path.split("/")[0])

        async with async_playwright() as pw:
            browser = await pw.chromium.launch(
                headless=self.headless,
                args=["--ignore-certificate-errors", "--no-sandbox"],
            )
            context = await browser.new_context(ignore_https_errors=True)
            page    = await context.new_page()

            # ── Login ───────────────────────────────────────────────────
            await self._login(page, url, portal, admin_email)

            # ── Run each flow ──────────────────────────────────────────
            for flow in scout_plan.get("flows", []):
                try:
                    print(f"[UIScoutAgent]   Flow: {flow['name']}")
                    obs = await self._run_flow(
                        page, flow, url, portal, module_url_segment, module_path
                    )
                    if obs:
                        observations.append(obs)
                except Exception as ex:
                    print(f"[UIScoutAgent]   ⚠ Flow {flow['name']} failed: {ex}")

            await browser.close()

        return observations

    async def _login(self, page, url: str, portal: str, admin_email: str):
        """Log into the SDP instance."""
        target = f"{url}app/{portal}/"
        print(f"[UIScoutAgent] Navigating to {target}")
        await page.goto(target, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(2000)

        login_selectors = "input[name='loginName'], input[type='email'], #username, #j_username"
        if await page.locator(login_selectors).count() > 0:
            print(f"[UIScoutAgent] Logging in as {admin_email}...")
            await page.fill(login_selectors, admin_email)
            pwd_sel = "input[type='password'], input[name='password'], #password, #j_password"
            if await page.locator(pwd_sel).count() > 0:
                await page.fill(pwd_sel, self.admin_password)
            await page.keyboard.press("Enter")
            await page.wait_for_load_state("networkidle", timeout=25000)
            print("[UIScoutAgent] ✅ Logged in")

    async def _run_flow(
        self, page, flow: dict, url: str, portal: str,
        module_url_segment: str, module_path: str,
    ) -> Optional[UIObservation]:
        """Execute a single scout flow and capture observation."""
        screenshots: list[str] = []

        for step in flow.get("steps", []):
            action = step.get("action")

            if action == "navigate_module":
                nav_url = f"{url}app/{portal}/{module_url_segment}/"
                await page.goto(nav_url, wait_until="networkidle", timeout=25000)
                await page.wait_for_timeout(1500)

            elif action == "click_new":
                # SDP uses a global actions bar — try specific known selectors first
                new_selectors = [
                    "text=New Solution",
                    "text=New Request",
                    "text=New Problem",
                    "text=New Change",
                    "[title='New Solution']",
                    "[title='New Request']",
                    "a.globalaction-btn",
                    "button.globalaction-btn",
                    ".sdp-global-action-item",
                    "a[href*='NewSolution']",
                    "a[href*='NewRequest']",
                    # Generic fallbacks
                    "button:has-text('New')",
                    "a:has-text('New')",
                    "[title*='New']",
                ]
                clicked = False
                for sel in new_selectors:
                    try:
                        loc = page.locator(sel).first
                        if await loc.count() > 0:
                            await loc.click()
                            await page.wait_for_timeout(3000)
                            clicked = True
                            print(f"[UIScoutAgent]   Clicked New via: {sel}")
                            break
                    except Exception:
                        continue
                if not clicked:
                    # Last resort: look for any visible link/button in the global action bar
                    try:
                        bar_btn = await page.evaluate("""
                            () => {
                                const candidates = [...document.querySelectorAll('a, button')];
                                const found = candidates.find(el =>
                                    el.offsetParent !== null &&
                                    /new/i.test(el.textContent.trim()) &&
                                    el.textContent.trim().length < 30
                                );
                                if (found) { found.click(); return found.textContent.trim(); }
                                return null;
                            }
                        """)
                        if bar_btn:
                            await page.wait_for_timeout(3000)
                            clicked = True
                            print(f"[UIScoutAgent]   Clicked New via JS eval: '{bar_btn}'")
                    except Exception:
                        pass
                if not clicked:
                    print(f"[UIScoutAgent]   ⚠ Could not click New button")

            elif action == "click":
                selector = step.get("selector", "")
                label    = step.get("label", "")
                try:
                    # Try CSS first, then XPath
                    if selector.startswith("//") or selector.startswith("(//"):
                        loc = page.locator(f"xpath={selector}").first
                    else:
                        loc = page.locator(selector).first
                    if await loc.count() > 0:
                        await loc.click()
                        await page.wait_for_timeout(1500)
                        print(f"[UIScoutAgent]   Clicked: {label}")
                    else:
                        print(f"[UIScoutAgent]   ⚠ Not found: {selector} ({label})")
                except Exception as ex:
                    print(f"[UIScoutAgent]   ⚠ Click failed ({label}): {ex}")

            # Screenshot after each step
            ss_path = await self._screenshot(page, f"{flow['name']}_{step.get('action','step')}")
            screenshots.append(ss_path)

        # ── Capture final page state ──────────────────────────────────
        # Playwright 1.58 does not have page.accessibility — use evaluate() instead
        snapshot_str   = await self._get_aria_snapshot(page)
        html_fragment  = await self._get_html_fragment(page)

        # ── Parse the page state ──────────────────────────────────────
        buttons        = await self._extract_buttons(page)
        fields         = await self._extract_form_fields(page)
        required       = await self._extract_required_fields(page)
        checkboxes     = await self._extract_checkboxes(page)

        # ── Ask LLM to annotate the observation ──────────────────────
        notes = self._llm_annotate_observation(
            flow_name=flow["name"],
            description=flow.get("description", ""),
            buttons=buttons,
            fields=fields,
            required=required,
            checkboxes=checkboxes,
            snapshot=snapshot_str[:3000],
        )

        return UIObservation(
            flow_name=flow["name"],
            description=flow.get("description", ""),
            visible_buttons=buttons,
            visible_fields=fields,
            required_fields=required,
            checkboxes=checkboxes,
            raw_snapshot=snapshot_str[:4000],
            screenshot_path=screenshots[-1] if screenshots else "",
            notes=notes,
        )

    # ── Page state extractors ──────────────────────────────────────────────

    async def _extract_buttons(self, page) -> list[str]:
        """Extract visible submit/action button labels from the page."""
        buttons = []
        try:
            els = page.locator("button:visible, input[type='submit']:visible, input[type='button']:visible")
            count = await els.count()
            for i in range(min(count, 20)):
                try:
                    text = (await els.nth(i).inner_text()).strip()
                    if text and len(text) < 60:
                        buttons.append(text)
                except Exception:
                    pass
        except Exception:
            pass
        return buttons

    async def _extract_form_fields(self, page) -> list[str]:
        """Extract visible input field labels from the form."""
        fields = []
        try:
            # Collect label texts that accompany inputs
            labels = page.locator("label:visible, .field-label:visible, .form-label:visible")
            count = await labels.count()
            for i in range(min(count, 30)):
                try:
                    text = (await labels.nth(i).inner_text()).strip()
                    if text and len(text) < 80 and len(text) > 1:
                        fields.append(text)
                except Exception:
                    pass
        except Exception:
            pass
        return fields

    async def _extract_required_fields(self, page) -> list[str]:
        """Extract field names marked as required (*)."""
        required = []
        try:
            # Common patterns: label with *, aria-required, .required class
            req_els = page.locator(
                "label:has-text('*'):visible, "
                "[aria-required='true']:visible, "
                ".required:visible, "
                ".mandatory:visible"
            )
            count = await req_els.count()
            for i in range(min(count, 20)):
                try:
                    text = (await req_els.nth(i).inner_text()).strip().replace("*", "").strip()
                    if text and len(text) < 80:
                        required.append(text)
                except Exception:
                    pass
        except Exception:
            pass
        return required

    async def _extract_checkboxes(self, page) -> list[dict]:
        """Extract checkboxes and their labels + checked state."""
        checkboxes = []
        try:
            cbs = page.locator("input[type='checkbox']:visible")
            count = await cbs.count()
            for i in range(min(count, 10)):
                try:
                    cb = cbs.nth(i)
                    checked = await cb.is_checked()
                    # Try to get the associated label
                    cb_id = await cb.get_attribute("id")
                    label_text = ""
                    if cb_id:
                        lbl = page.locator(f"label[for='{cb_id}']")
                        if await lbl.count() > 0:
                            label_text = (await lbl.inner_text()).strip()
                    if not label_text:
                        # Try sibling or parent text
                        try:
                            parent_text = await cb.evaluate(
                                "el => el.closest('label, .checkbox-wrapper, .field-row')?.innerText || ''"
                            )
                            label_text = parent_text.strip()[:60]
                        except Exception:
                            pass
                    checkboxes.append({
                        "label":   label_text or f"checkbox_{i}",
                        "checked": checked,
                        "id":      cb_id or "",
                        "effect":  "",  # filled in by LLM annotation
                    })
                except Exception:
                    pass
        except Exception:
            pass
        return checkboxes

    async def _get_aria_snapshot(self, page) -> str:
        """
        Extract a structured text snapshot of the page's interactive elements.
        Works with Playwright 1.58 (no page.accessibility API).
        Uses evaluate() to walk the DOM and collect roles, labels, and text.
        """
        try:
            data = await page.evaluate("""
                () => {
                    const collect = (el, depth) => {
                        if (depth > 6) return [];
                        const role  = el.getAttribute('role') || el.tagName.toLowerCase();
                        const label = el.getAttribute('aria-label') || el.getAttribute('placeholder') || '';
                        const text  = (el.innerText || '').trim().slice(0, 80);
                        const items = [];
                        if (text || label) {
                            items.push({ role, label, text, tag: el.tagName.toLowerCase() });
                        }
                        for (const child of el.children) {
                            items.push(...collect(child, depth + 1));
                        }
                        return items;
                    };
                    return collect(document.body, 0).slice(0, 200);
                }
            """)
            return json.dumps(data, indent=2) if data else ""
        except Exception as ex:
            print(f"[UIScoutAgent] aria_snapshot failed: {ex}")
            return ""

    async def _get_html_fragment(self, page) -> str:
        """Get a trimmed HTML fragment of the main form area."""
        try:
            # Try to find the main form/modal first
            for selector in ["form:visible", ".create-form", "#new-entity-form", ".modal-body", "main"]:
                try:
                    if await page.locator(selector).count() > 0:
                        html = await page.locator(selector).first.inner_html()
                        return html[:4000]
                except Exception:
                    pass
            return (await page.inner_html("body"))[:4000]
        except Exception:
            return ""

    async def _screenshot(self, page, label: str) -> str:
        """Take a screenshot and return path."""
        ts = datetime.now().strftime("%Y%m%dT%H%M%S")
        path = str(self.screenshots_dir / f"scout_{ts}_{label[:40]}.png")
        try:
            await page.screenshot(path=path, full_page=False)
        except Exception as ex:
            print(f"[UIScoutAgent] Screenshot failed: {ex}")
        return path

    # ── LLM annotation ────────────────────────────────────────────────────

    def _llm_annotate_observation(
        self,
        flow_name: str,
        description: str,
        buttons: list[str],
        fields: list[str],
        required: list[str],
        checkboxes: list[dict],
        snapshot: str,
    ) -> list[str]:
        """
        Ask the LLM to derive actionable notes from the observed UI state.
        Returns a list of short, precise notes for the Coder Agent.
        """
        if not buttons and not fields and not checkboxes:
            return []

        prompt = f"""You are analysing a live UI observation from Zoho ServiceDesk Plus.

Flow: {flow_name}
Description: {description}

Observed UI state:
  Visible buttons  : {buttons}
  Visible fields   : {fields[:15]}
  Required fields  : {required}
  Checkboxes       : {json.dumps(checkboxes, indent=2)}

Accessibility snapshot (partial):
{snapshot[:2000]}

Write 2-5 SHORT, PRECISE notes that a Java Selenium test automation engineer 
MUST know before coding this scenario. Focus on:
  - Which button to click to submit (and when NOT to click a particular button)
  - Which fields are mandatory vs optional
  - What the checkbox does when checked (what new UI elements appear)
  - Any traps (e.g. checking a checkbox reveals a second submit button)

Return ONLY a JSON array of strings. No explanation outside JSON.
Example: ["Clicking 'Add' creates unapproved; clicking 'Add And Approve' creates approved", "Title and Description are mandatory"]"""

        try:
            resp = self.llm.invoke([
                SystemMessage(content="You are a UI behaviour analyser. Return only valid JSON arrays."),
                HumanMessage(content=prompt),
            ])
            text = resp.content.strip()
            text = re.sub(r"```json\s*|\s*```", "", text).strip()
            notes = json.loads(text)
            if isinstance(notes, list):
                return [str(n) for n in notes[:5]]
        except Exception as ex:
            print(f"[UIScoutAgent] LLM annotation failed: {ex}")
        return []

    # ── Scout plan helpers ─────────────────────────────────────────────────

    def _resolve_scout_plan(self, module_path: str) -> Optional[dict]:
        """Return a predefined scout plan for a known module, or None."""
        # Exact match
        if module_path in MODULE_SCOUT_PLANS:
            return MODULE_SCOUT_PLANS[module_path]
        # Partial match — e.g. "modules/solutions/solution" → "solutions/solution"
        for key, plan in MODULE_SCOUT_PLANS.items():
            if key in module_path or module_path.endswith(key):
                return plan
        return None

    def _infer_scout_plan(self, module_path: str, scenarios: list[dict]) -> dict:
        """
        For unknown modules, ask the LLM to infer a minimal scout plan
        based on the planned scenarios.
        """
        scenario_descs = [s.get("description", "") for s in scenarios[:5]]
        segment = module_path.split("/")[-1] if "/" in module_path else module_path

        prompt = f"""You are building a UI scouting plan for a Zoho ServiceDesk Plus module.

Module path: {module_path}
Planned test scenarios:
{json.dumps(scenario_descs, indent=2)}

Generate a JSON scout plan with:
  - "module_url": the SDP URL segment for this module (e.g. "solutions", "requests", "changes")
  - "flows": list of flows to scout, each with:
      - "name": short snake_case name
      - "description": what this flow observes
      - "steps": list of steps, each: {{"action": "navigate_module"|"click_new"|"click", "selector": "...", "label": "..."}}

Keep it to 2 flows max. Return ONLY valid JSON."""

        try:
            resp = self.llm.invoke([
                SystemMessage(content="You are a UI test planning expert. Return only valid JSON."),
                HumanMessage(content=prompt),
            ])
            text = re.sub(r"```json\s*|\s*```", "", resp.content.strip()).strip()
            plan = json.loads(text)
            if "flows" in plan:
                return plan
        except Exception as ex:
            print(f"[UIScoutAgent] LLM plan inference failed: {ex}")

        # Fallback: minimal plan
        return {
            "module_url": segment,
            "flows": [
                {
                    "name": f"{segment}_new_form",
                    "description": f"Observe the New {segment.title()} form",
                    "steps": [
                        {"action": "navigate_module"},
                        {"action": "click_new"},
                    ],
                }
            ],
        }

    # ── Public: scout a single module directly ─────────────────────────────

    def scout(
        self,
        module_path: str,
        url: str = None,
        portal: str = None,
        admin_email: str = None,
    ) -> list[dict]:
        """
        Public entry point for standalone use (without LangGraph).
        Returns list of UIObservation.to_dict().
        """
        plan = self._resolve_scout_plan(module_path) or self._infer_scout_plan(module_path, [])
        observations = self._scout_module(
            module_path=module_path,
            scout_plan=plan,
            url=url or self.url,
            portal=portal or self.portal,
            admin_email=admin_email or self.admin_email,
        )
        return [o.to_dict() for o in observations]


# ── CLI ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import sys
    module = sys.argv[1] if len(sys.argv) > 1 else "solutions/solution"
    print(f"\n[UIScoutAgent] Scouting: {module}\n")

    scout = UIScoutAgent(headless=False)  # headless=False so you can watch it
    results = scout.scout(module)

    for obs in results:
        print(f"\n── {obs['flow_name']} ──")
        print(f"  Buttons  : {obs['visible_buttons']}")
        print(f"  Fields   : {obs['visible_fields'][:8]}")
        print(f"  Required : {obs['required_fields']}")
        print(f"  Notes    :")
        for note in obs["notes"]:
            print(f"    ⚠ {note}")

    # Save to file for inspection
    out = Path(__file__).resolve().parents[1] / "knowledge_base/scout_snapshots/latest_observations.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\n✅ Saved to {out}")
