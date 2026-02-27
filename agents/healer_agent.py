"""
healer_agent.py
---------------
Healer Agent: A Playwright-powered self-healing agent that activates when a
test case fails. It opens a real browser session, surfs through the application
to reach the failing UI state, captures an accessibility snapshot, uses the LLM
to identify the correct locator or code fix, patches the Java source, recompiles,
and re-runs the test — all autonomously.

Pipeline position:
  ... → runner → [FAILED?] → healer → END
                    │
                 [PASSED] → END

Architecture:
  ┌──────────────────────────────────────────────────────────────────────┐
  │  HealerAgent.heal(state)                                             │
  │                                                                      │
  │  1. Read run_result from state                                       │
  │  2. If success → skip                                                │
  │  3. _classify_failure() → LLM decides: LOCATOR | API | LOGIC | OTHER│
  │  4a. LOCATOR → _run_playwright_session()                             │
  │       ├─ launch Chromium (headless or headed)                        │
  │       ├─ login() → navigate to module                                │
  │       ├─ replay_ui_steps() → drive to failing UI state               │
  │       ├─ snapshot() → accessibility tree as text                     │
  │       └─ _extract_locator_fix() → LLM maps snapshot to Java locator  │
  │       └─ _apply_patch() → write fixed locator to .java file          │
  │  4b. API/LOGIC → _run_code_fix() → LLM generates code patch          │
  │  5. _recompile() → javac only the changed .java files                │
  │  6. _rerun() → RunnerAgent.run_test() with same config               │
  │  7. Return heal_result dict to state                                 │
  └──────────────────────────────────────────────────────────────────────┘

Usage (standalone):
    from agents.healer_agent import HealerAgent
    healer = HealerAgent(base_dir=BASE_DIR, ...)
    healer.heal_from_run_result(
        run_result=result.to_dict(),
        run_config=RUN_CONFIG,
        entity_source_files=["/path/to/SolutionBase.java", "/path/to/SolutionLocators.java"],
    )

Usage (LangGraph):
    Wired automatically by pipeline.py after runner node.
"""

import os
import re
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Optional

from langchain_core.messages import SystemMessage, HumanMessage

from agents.state import AgentState
from agents.llm_factory import get_llm
from config.project_config import PROJECT_NAME


# ── Constants ─────────────────────────────────────────────────────────────────

HEALER_SCREENSHOTS_DIR = ".playwright-mcp"

# Failure categories
FAILURE_LOCATOR = "LOCATOR_FAILURE"
FAILURE_API     = "API_FAILURE"
FAILURE_LOGIC   = "LOGIC_FAILURE"
FAILURE_COMPILE = "COMPILE_FAILURE"
FAILURE_OTHER   = "OTHER"

# Default app credentials — overridden from .env or run_config
DEFAULT_URL          = "https://sdpodqa-auto1.csez.zohocorpin.com:9090/"
DEFAULT_PORTAL       = "portal1"
DEFAULT_ADMIN_EMAIL  = "jaya.kumar+org1admin1t0@zohotest.com"
DEFAULT_ADMIN_PASS   = "Admin@123"

# Entity → module navigation path (used by Playwright to reach the right page)
MODULE_NAV_MAP = {
    "Solution":  "Solutions",
    "Request":   "Requests",
    "Problem":   "Problems",
    "Change":    "Changes",
    "Release":   "Releases",
    "Asset":     "Assets",
    "Project":   "Projects",
    "Task":      "Tasks",
}


# ── Result container ──────────────────────────────────────────────────────────

class HealResult:
    """Holds the outcome of a single healing attempt."""

    def __init__(
        self,
        healed: bool,
        failure_type: str = FAILURE_OTHER,
        fix_description: str = "",
        patched_files: list = None,
        rerun_success: bool = False,
        snapshots: list = None,
        error: str = "",
    ):
        self.healed         = healed
        self.failure_type   = failure_type
        self.fix_description = fix_description
        self.patched_files  = patched_files or []
        self.rerun_success  = rerun_success
        self.snapshots      = snapshots or []
        self.error          = error
        self.timestamp      = datetime.now().isoformat()

    def summary(self) -> str:
        icon = "🩹 HEALED" if self.healed else "💔 NOT HEALED"
        rerun = "✅ RERUN PASSED" if self.rerun_success else "❌ RERUN FAILED" if self.healed else ""
        lines = [
            f"{icon} — {self.failure_type}",
            f"  Fix        : {self.fix_description}",
            f"  Patched    : {', '.join(self.patched_files) or 'none'}",
        ]
        if rerun:
            lines.append(f"  Rerun      : {rerun}")
        if self.error:
            lines.append(f"  Error      : {self.error}")
        lines.append(f"  Timestamp  : {self.timestamp}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "healed":          self.healed,
            "failure_type":    self.failure_type,
            "fix_description": self.fix_description,
            "patched_files":   self.patched_files,
            "rerun_success":   self.rerun_success,
            "snapshots":       self.snapshots,
            "error":           self.error,
            "timestamp":       self.timestamp,
        }


# ── Healer Agent ──────────────────────────────────────────────────────────────

class HealerAgent:
    """
    Playwright-powered self-healing agent.

    When a test fails this agent:
      1. Classifies the failure type using the LLM
      2. For LOCATOR failures: opens a real browser, replays the UI flow,
         captures accessibility snapshots, and uses the LLM to extract the
         correct locator — then patches the Java source file.
      3. For API/LOGIC failures: uses the LLM to generate a code patch
         directly from the error + source context.
      4. Recompiles only the changed files, then re-runs the test.
    """

    def __init__(
        self,
        base_dir: str = None,
        deps_dir: str = None,
        pre_compiled_bin_dir: str = None,
        headless: bool = True,
    ):
        self.base             = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self.automater_root   = self.base / PROJECT_NAME
        self.bin_dir          = Path(pre_compiled_bin_dir) if pre_compiled_bin_dir else self.automater_root / "bin"
        self.src_dir          = self.automater_root / "src"
        self.deps_dir         = Path(deps_dir) if deps_dir else Path("/home/balaji-12086/Desktop/Workspace/Zide/dependencies")
        self.screenshots_dir  = self.base / HEALER_SCREENSHOTS_DIR
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.headless         = headless
        self.llm              = get_llm(temperature=0.1)

    # ── LangGraph node entry point ────────────────────────────────────────

    def run(self, state: AgentState) -> AgentState:
        """
        LangGraph node: activates only when run_result.success is False.

        Reads:
          state['run_result']  — from RunnerAgent
          state['run_config']  — original test config

        Writes:
          state['heal_result'] — HealResult.to_dict()
          state['messages']    += [summary]
        """
        run_result = state.get("run_result", {})
        run_config = state.get("run_config", {})

        if run_result.get("success", True):
            msg = "[HealerAgent] Test passed — no healing needed."
            print(msg)
            state["heal_result"] = HealResult(healed=False, fix_description="Test already passed").to_dict()
            state["messages"] = [msg]
            return state

        print("[HealerAgent] 🩺 Test failed — activating healer...")

        # Resolve entity source files from run_config
        entity_class = run_config.get("entity_class", "Solution")
        source_files = self._find_source_files(entity_class)

        result = self.heal_from_run_result(
            run_result=run_result,
            run_config=run_config,
            entity_source_files=source_files,
        )

        state["heal_result"] = result.to_dict()
        state["messages"] = [result.summary()]
        print(result.summary())
        return state

    # ── Main heal entry point ─────────────────────────────────────────────

    def heal_from_run_result(
        self,
        run_result: dict,
        run_config: dict,
        entity_source_files: list = None,
    ) -> HealResult:
        """
        Full healing workflow: classify → browser-heal or code-heal → rerun.

        Args:
            run_result          : RunResult.to_dict() from RunnerAgent
            run_config          : { entity_class, method_name, url, ... }
            entity_source_files : Paths to relevant .java source files
        """
        stdout       = run_result.get("stdout", "")
        stderr       = run_result.get("stderr", "")
        entity_class = run_config.get("entity_class", "Solution")
        method_name  = run_config.get("method_name", "")
        url          = run_config.get("url", DEFAULT_URL)
        portal       = run_config.get("portal_name", DEFAULT_PORTAL)
        admin_email  = run_config.get("admin_mail_id", DEFAULT_ADMIN_EMAIL)

        source_files = entity_source_files or self._find_source_files(entity_class)

        # ── Step 1: Classify the failure ──────────────────────────────────
        print("[HealerAgent] Step 1: Classifying failure...")
        failure_type = self._classify_failure(stdout, stderr, source_files)
        print(f"[HealerAgent] Failure type: {failure_type}")

        # ── Step 2: Heal based on type ────────────────────────────────────
        if failure_type == FAILURE_LOCATOR:
            return self._heal_locator_failure(
                stdout, stderr, entity_class, method_name,
                url, portal, admin_email, source_files, run_config,
            )
        elif failure_type in (FAILURE_API, FAILURE_LOGIC):
            return self._heal_code_failure(
                stdout, stderr, entity_class, method_name,
                source_files, run_config, failure_type,
            )
        elif failure_type == FAILURE_COMPILE:
            return self._heal_compile_failure(
                stdout, stderr, source_files, run_config,
            )
        else:
            return HealResult(
                healed=False,
                failure_type=failure_type,
                fix_description="Failure type not auto-healable — requires manual intervention",
                error=self._extract_error_snippet(stdout, stderr),
            )

    # ── Failure classification ────────────────────────────────────────────

    def _classify_failure(self, stdout: str, stderr: str, source_files: list) -> str:
        """Use LLM to classify the failure type from the test output."""

        # Fast heuristics first (no LLM cost)
        combined = stdout + stderr
        if "NoSuchElementException" in combined or "TimeoutException" in combined \
                or "ElementNotInteractableException" in combined \
                or "StaleElementReferenceException" in combined \
                or "Unable to locate element" in combined:
            return FAILURE_LOCATOR
        if "BUILD FAILED" in combined or "javac" in combined.lower() \
                or "cannot find symbol" in combined or "error:" in combined[:500]:
            return FAILURE_COMPILE
        if "NullPointerException" in combined and "sdpAPICall" in combined:
            return FAILURE_API
        if "NullPointerException" in combined or "responseJSON" in combined:
            return FAILURE_API

        # LLM-based classification for ambiguous cases
        error_snippet = self._extract_error_snippet(stdout, stderr)
        source_context = self._read_source_snippet(source_files, max_lines=60)

        prompt = f"""You are analyzing a Java Selenium test failure.

ERROR OUTPUT (relevant lines):
{error_snippet}

SOURCE CONTEXT (failing method area):
{source_context}

Classify the failure into EXACTLY ONE of these categories:
- LOCATOR_FAILURE  : Selenium cannot find an element (wrong XPath/CSS/ID/name)
- API_FAILURE      : A REST API call returned null or an unexpected response
- LOGIC_FAILURE    : Business logic error, wrong condition, missing step
- COMPILE_FAILURE  : Java compilation error
- OTHER            : None of the above

Reply with ONLY the category name (e.g. LOCATOR_FAILURE). No explanation."""

        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a test failure classification expert."),
                HumanMessage(content=prompt),
            ])
            category = response.content.strip().upper()
            for known in (FAILURE_LOCATOR, FAILURE_API, FAILURE_LOGIC, FAILURE_COMPILE, FAILURE_OTHER):
                if known in category:
                    return known
        except Exception as ex:
            print(f"[HealerAgent] LLM classification failed: {ex}")

        return FAILURE_OTHER

    # ── Locator healing (Playwright path) ────────────────────────────────

    def _heal_locator_failure(
        self, stdout, stderr, entity_class, method_name,
        url, portal, admin_email, source_files, run_config,
    ) -> HealResult:
        """
        Open a real browser, navigate to the failing UI state,
        capture accessibility snapshot, fix the locator with LLM.
        """
        print("[HealerAgent] 🌐 Launching Playwright browser session...")
        snapshots = []
        patched_files = []

        try:
            from playwright.sync_api import sync_playwright

            error_snippet = self._extract_error_snippet(stdout, stderr)
            broken_locator_hint = self._extract_broken_locator_hint(stdout, stderr, source_files)
            nav_steps = self._infer_navigation_steps(method_name, entity_class, source_files)

            print(f"[HealerAgent] Broken locator hint: {broken_locator_hint}")
            print(f"[HealerAgent] Navigation steps: {nav_steps}")

            with sync_playwright() as pw:
                browser = pw.chromium.launch(
                    headless=self.headless,
                    args=["--ignore-certificate-errors", "--no-sandbox"],
                )
                context = browser.new_context(ignore_https_errors=True)
                page = context.new_page()

                # ── Login ─────────────────────────────────────────────
                print(f"[HealerAgent] Navigating to {url}app/{portal}/")
                page.goto(f"{url}app/{portal}/", wait_until="networkidle", timeout=30000)
                snap = self._take_snapshot(page, "01_initial_page")
                snapshots.append(snap)

                # Check if login form exists
                if page.locator("input[name='loginName'], input[type='email'], #username").count() > 0:
                    print(f"[HealerAgent] Logging in as {admin_email}...")
                    page.fill("input[name='loginName'], input[type='email'], #username", admin_email)
                    # Password field
                    pwd_sel = "input[type='password'], input[name='password'], #password"
                    if page.locator(pwd_sel).count() > 0:
                        page.fill(pwd_sel, DEFAULT_ADMIN_PASS)
                    # Submit
                    page.keyboard.press("Enter")
                    page.wait_for_load_state("networkidle", timeout=20000)
                    snap = self._take_snapshot(page, "02_after_login")
                    snapshots.append(snap)
                    print("[HealerAgent] ✅ Logged in")
                else:
                    print("[HealerAgent] Already logged in or login form not found")

                # ── Navigate to module ────────────────────────────────
                module_name = MODULE_NAV_MAP.get(entity_class, entity_class + "s")
                nav_url = f"{url}app/{portal}/{module_name.lower()}/"
                print(f"[HealerAgent] Navigating to module: {nav_url}")
                page.goto(nav_url, wait_until="networkidle", timeout=30000)
                snap = self._take_snapshot(page, f"03_{module_name.lower()}_listview")
                snapshots.append(snap)

                # ── Replay navigation steps ───────────────────────────
                step_snapshots = self._replay_navigation_steps(page, nav_steps, url, portal, module_name)
                snapshots.extend(step_snapshots)

                # ── Capture final snapshot ────────────────────────────
                final_snapshot_text = page.accessibility.snapshot()
                final_snapshot_str  = json.dumps(final_snapshot_text, indent=2) if final_snapshot_text else ""
                final_html_snippet  = self._get_relevant_html(page)

                # Save full snapshot
                snap_path = str(self.screenshots_dir / f"healer_{method_name}_final.json")
                Path(snap_path).write_text(final_snapshot_str, encoding="utf-8")
                snapshots.append(snap_path)
                print(f"[HealerAgent] 📸 Accessibility snapshot captured → {snap_path}")

                context.close()
                browser.close()

            # ── Use LLM to derive correct locator ────────────────────
            print("[HealerAgent] 🤖 Asking LLM to identify correct locator...")
            locator_file = self._find_locator_file(entity_class)
            locator_file_content = Path(locator_file).read_text(encoding="utf-8") if locator_file else ""

            fix = self._extract_locator_fix(
                snapshot_text=final_snapshot_str,
                html_snippet=final_html_snippet,
                error_snippet=error_snippet,
                broken_locator_hint=broken_locator_hint,
                locator_file_content=locator_file_content,
                method_name=method_name,
                entity_class=entity_class,
            )

            if not fix or not fix.get("old_line") or not fix.get("new_line"):
                return HealResult(
                    healed=False,
                    failure_type=FAILURE_LOCATOR,
                    fix_description="LLM could not determine a confident locator fix",
                    snapshots=snapshots,
                    error="No fix generated by LLM",
                )

            # ── Patch the locator file ────────────────────────────────
            print(f"[HealerAgent] Patching locator: {fix.get('old_line')} → {fix.get('new_line')}")
            target_file = fix.get("file_path") or locator_file

            if target_file and Path(target_file).exists():
                content = Path(target_file).read_text(encoding="utf-8")
                if fix["old_line"] in content:
                    new_content = content.replace(fix["old_line"], fix["new_line"], 1)
                    Path(target_file).write_text(new_content, encoding="utf-8")
                    patched_files.append(target_file)
                    print(f"[HealerAgent] ✅ Patched: {target_file}")
                else:
                    print(f"[HealerAgent] ⚠️  Could not find old_line in {target_file}")
                    # Try applying via LLM-guided full-file rewrite
                    rewritten = self._llm_rewrite_file(target_file, fix)
                    if rewritten:
                        patched_files.append(target_file)

            # ── Recompile ─────────────────────────────────────────────
            if patched_files:
                print("[HealerAgent] ⚙️  Recompiling patched files...")
                compile_ok = self._recompile_files(patched_files)
                if not compile_ok:
                    return HealResult(
                        healed=True,
                        failure_type=FAILURE_LOCATOR,
                        fix_description=fix.get("description", "Locator patched but recompile failed"),
                        patched_files=patched_files,
                        rerun_success=False,
                        snapshots=snapshots,
                        error="Recompile failed after patch",
                    )

                # ── Rerun test ─────────────────────────────────────────
                print("[HealerAgent] 🔄 Re-running test to verify fix...")
                rerun_ok = self._rerun_test(run_config)
                return HealResult(
                    healed=True,
                    failure_type=FAILURE_LOCATOR,
                    fix_description=fix.get("description", "Locator fix applied"),
                    patched_files=patched_files,
                    rerun_success=rerun_ok,
                    snapshots=snapshots,
                )

            return HealResult(
                healed=False,
                failure_type=FAILURE_LOCATOR,
                fix_description="No suitable locator file found to patch",
                snapshots=snapshots,
            )

        except Exception as exc:
            print(f"[HealerAgent] ❌ Playwright session error: {exc}")
            import traceback
            traceback.print_exc()
            return HealResult(
                healed=False,
                failure_type=FAILURE_LOCATOR,
                fix_description="Playwright session crashed",
                snapshots=snapshots,
                error=str(exc),
            )

    # ── API / Logic healing (code patch path) ────────────────────────────

    def _heal_code_failure(
        self, stdout, stderr, entity_class, method_name,
        source_files, run_config, failure_type,
    ) -> HealResult:
        """
        Use the LLM to generate a code fix for API or logic failures,
        then patch the Java source, recompile, and re-run.
        """
        print(f"[HealerAgent] 🔧 Generating code fix for {failure_type}...")
        patched_files = []

        error_snippet    = self._extract_error_snippet(stdout, stderr)
        source_context   = self._read_full_source(source_files, max_chars=8000)

        fix = self._llm_generate_code_fix(
            error_snippet=error_snippet,
            source_context=source_context,
            method_name=method_name,
            entity_class=entity_class,
            failure_type=failure_type,
        )

        if not fix or not fix.get("file_path"):
            return HealResult(
                healed=False,
                failure_type=failure_type,
                fix_description="LLM could not generate a code fix",
                error="No fix generated",
            )

        target_file = fix["file_path"]
        if not Path(target_file).exists():
            return HealResult(
                healed=False,
                failure_type=failure_type,
                fix_description=f"Target file not found: {target_file}",
                error="File not found",
            )

        # Apply old → new replacement
        content = Path(target_file).read_text(encoding="utf-8")
        old_code = fix.get("old_code", "")
        new_code = fix.get("new_code", "")

        if old_code and old_code in content:
            new_content = content.replace(old_code, new_code, 1)
            Path(target_file).write_text(new_content, encoding="utf-8")
            patched_files.append(target_file)
            print(f"[HealerAgent] ✅ Code patch applied to {target_file}")
        else:
            print(f"[HealerAgent] ⚠️  Could not find exact code block — trying LLM rewrite...")
            rewritten = self._llm_rewrite_file(target_file, fix)
            if rewritten:
                patched_files.append(target_file)

        if not patched_files:
            return HealResult(
                healed=False,
                failure_type=failure_type,
                fix_description="Code patch could not be applied",
                error="Patch application failed",
            )

        # Recompile
        compile_ok = self._recompile_files(patched_files)
        if not compile_ok:
            return HealResult(
                healed=True,
                failure_type=failure_type,
                fix_description=fix.get("description", "Code patched but recompile failed"),
                patched_files=patched_files,
                rerun_success=False,
                error="Recompile failed after patch",
            )

        # Rerun
        rerun_ok = self._rerun_test(run_config)
        return HealResult(
            healed=True,
            failure_type=failure_type,
            fix_description=fix.get("description", "Code fix applied"),
            patched_files=patched_files,
            rerun_success=rerun_ok,
        )

    # ── Compile failure healing ───────────────────────────────────────────

    def _heal_compile_failure(self, stdout, stderr, source_files, run_config) -> HealResult:
        """Fix Java compile errors using the LLM."""
        print("[HealerAgent] 🔧 Fixing compile error...")
        error_snippet  = self._extract_error_snippet(stdout, stderr)
        source_context = self._read_full_source(source_files, max_chars=6000)

        fix = self._llm_generate_code_fix(
            error_snippet=error_snippet,
            source_context=source_context,
            method_name="",
            entity_class="",
            failure_type=FAILURE_COMPILE,
        )

        if not fix or not fix.get("file_path"):
            return HealResult(
                healed=False,
                failure_type=FAILURE_COMPILE,
                fix_description="LLM could not generate compile fix",
                error="No fix generated",
            )

        target_file = fix["file_path"]
        patched_files = []
        if Path(target_file).exists():
            content = Path(target_file).read_text(encoding="utf-8")
            old_code = fix.get("old_code", "")
            new_code = fix.get("new_code", "")
            if old_code and old_code in content:
                Path(target_file).write_text(content.replace(old_code, new_code, 1), encoding="utf-8")
                patched_files.append(target_file)

        if not patched_files:
            return HealResult(healed=False, failure_type=FAILURE_COMPILE, fix_description="Patch not applied")

        compile_ok = self._recompile_files(patched_files)
        rerun_ok = self._rerun_test(run_config) if compile_ok else False
        return HealResult(
            healed=True,
            failure_type=FAILURE_COMPILE,
            fix_description=fix.get("description", "Compile fix applied"),
            patched_files=patched_files,
            rerun_success=rerun_ok,
        )

    # ── Playwright helpers ────────────────────────────────────────────────

    def _take_snapshot(self, page, label: str) -> str:
        """Save a screenshot + return path."""
        ts = datetime.now().strftime("%Y%m%dT%H%M%S")
        path = str(self.screenshots_dir / f"healer_{ts}_{label}.png")
        try:
            page.screenshot(path=path, full_page=False)
            print(f"[HealerAgent] 📸 Screenshot: {path}")
        except Exception as ex:
            print(f"[HealerAgent] Screenshot failed: {ex}")
        return path

    def _replay_navigation_steps(self, page, nav_steps: list, url, portal, module_name) -> list:
        """
        Execute inferred navigation steps to reach the failing UI state.
        Each step is a dict: { "action": "click|fill|navigate", "selector": "...", "value": "..." }
        Returns list of snapshot paths taken.
        """
        snapshots = []
        for i, step in enumerate(nav_steps):
            action   = step.get("action", "")
            selector = step.get("selector", "")
            value    = step.get("value", "")
            label    = step.get("label", f"step_{i+1}")

            try:
                print(f"[HealerAgent] Nav step {i+1}: {action} → {selector} [{label}]")
                if action == "navigate":
                    page.goto(value, wait_until="networkidle", timeout=20000)
                elif action == "click" and selector:
                    loc = page.locator(selector)
                    if loc.count() > 0:
                        loc.first.click()
                        page.wait_for_load_state("networkidle", timeout=10000)
                    else:
                        print(f"[HealerAgent]   ⚠️  selector not found: {selector}")
                elif action == "fill" and selector:
                    page.fill(selector, value)

                snap = self._take_snapshot(page, label)
                snapshots.append(snap)

            except Exception as ex:
                print(f"[HealerAgent]   Step {i+1} error: {ex}")

        return snapshots

    def _get_relevant_html(self, page, selector: str = "body") -> str:
        """Extract a trimmed HTML fragment around the main content area."""
        try:
            html = page.inner_html("body")
            # Trim to first 8000 chars to avoid huge context
            return html[:8000]
        except Exception:
            return ""

    # ── LLM helpers ───────────────────────────────────────────────────────

    def _extract_locator_fix(
        self,
        snapshot_text: str,
        html_snippet: str,
        error_snippet: str,
        broken_locator_hint: str,
        locator_file_content: str,
        method_name: str,
        entity_class: str,
    ) -> Optional[dict]:
        """
        Ask the LLM to identify the correct locator from the live accessibility
        snapshot, and return a dict with old_line, new_line, file_path, description.
        """
        prompt = f"""You are a Selenium locator repair expert for a Java test automation framework.

A test case FAILED because a locator could not find the element in the browser.

BROKEN LOCATOR HINT (from error/source):
{broken_locator_hint}

ERROR:
{error_snippet}

LIVE ACCESSIBILITY SNAPSHOT (from the page where the error occurred):
{snapshot_text[:5000]}

HTML FRAGMENT (trimmed):
{html_snippet[:3000]}

CURRENT LOCATOR FILE CONTENT:
{locator_file_content}

FAILING TEST METHOD: {method_name} (class: {entity_class})

Your job:
1. Identify which locator constant in the locator file is broken
2. Look at the accessibility snapshot and HTML to find the correct selector
3. Return a JSON object with these exact keys:
   - "old_line": the exact current Java line in the locator file that needs fixing
   - "new_line": the corrected Java line (same format, just different By selector)
   - "description": one-line description of what changed
   - "confidence": "high" | "medium" | "low"

RULES:
- Prefer By.id() over By.xpath() when an id is available
- Prefer By.name() when a name attribute is present
- Only fix ONE locator (the one that caused the failure)
- Return ONLY valid JSON, no markdown, no explanation outside the JSON

Example:
{{"old_line": "Locator FOO = new Locator(By.id(\\"old_id\\"), \\"description\\");",
  "new_line": "Locator FOO = new Locator(By.id(\\"new_id\\"), \\"description\\");",
  "description": "Updated FOO locator id from old_id to new_id",
  "confidence": "high"}}"""

        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a Selenium locator expert. Return only valid JSON."),
                HumanMessage(content=prompt),
            ])
            text = response.content.strip()
            # Strip markdown fences if present
            text = re.sub(r"```json\s*|\s*```", "", text).strip()
            return json.loads(text)
        except Exception as ex:
            print(f"[HealerAgent] LLM locator fix failed: {ex}")
            return None

    def _llm_generate_code_fix(
        self,
        error_snippet: str,
        source_context: str,
        method_name: str,
        entity_class: str,
        failure_type: str,
    ) -> Optional[dict]:
        """
        Ask the LLM to generate a code patch (old_code → new_code) for
        API/logic/compile failures.
        """
        prompt = f"""You are a Java test automation expert for Zoho ServiceDesk Plus.

A test has FAILED with a {failure_type}.

ERROR (relevant lines):
{error_snippet}

SOURCE CODE CONTEXT:
{source_context}

FAILING METHOD: {method_name} (class: {entity_class})

Your job: generate a minimal code fix.

Return a JSON object with these exact keys:
- "file_path": absolute path of the Java file that needs to be changed
- "old_code": the exact block of Java code to be replaced (must match source exactly)
- "new_code": the corrected replacement code
- "description": one-line description of the fix

RULES:
- The fix must be minimal — change only what is necessary
- Do not rename methods or change method signatures
- old_code must be an exact substring of the source (copy from SOURCE CODE CONTEXT)
- Return ONLY valid JSON, no markdown

Example:
{{"file_path": "/path/to/SolutionBase.java",
  "old_code": "String x = foo.bar();",
  "new_code": "String x = (foo != null) ? foo.bar() : null;",
  "description": "Added null guard before calling foo.bar()"}}"""

        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a Java code fix expert. Return only valid JSON."),
                HumanMessage(content=prompt),
            ])
            text = response.content.strip()
            text = re.sub(r"```json\s*|\s*```", "", text).strip()
            return json.loads(text)
        except Exception as ex:
            print(f"[HealerAgent] LLM code fix failed: {ex}")
            return None

    def _llm_rewrite_file(self, file_path: str, fix: dict) -> bool:
        """Fallback: ask LLM to rewrite the full file applying the fix."""
        try:
            content = Path(file_path).read_text(encoding="utf-8")
            prompt = f"""Apply the following fix to this Java file.

FIX DESCRIPTION: {fix.get('description', '')}
OLD CODE: {fix.get('old_code') or fix.get('old_line', '')}
NEW CODE: {fix.get('new_code') or fix.get('new_line', '')}

FULL FILE CONTENT:
{content}

Return ONLY the complete corrected file content. No explanation, no markdown fences."""

            response = self.llm.invoke([
                SystemMessage(content="You are a Java file editor. Return only the corrected file content."),
                HumanMessage(content=prompt),
            ])
            new_content = response.content.strip()
            if len(new_content) > 100:
                Path(file_path).write_text(new_content, encoding="utf-8")
                print(f"[HealerAgent] LLM full-file rewrite applied to {file_path}")
                return True
        except Exception as ex:
            print(f"[HealerAgent] LLM full-file rewrite failed: {ex}")
        return False

    def _infer_navigation_steps(self, method_name: str, entity_class: str, source_files: list) -> list:
        """
        Use the LLM to infer which UI navigation steps need to be replayed
        to reach the state where the failing element appears.
        """
        source_context = self._read_source_snippet(source_files, max_lines=80)

        prompt = f"""A Selenium test for '{entity_class}.{method_name}' is failing on a locator.

Here is the test method source code:
{source_context}

Generate a JSON list of navigation steps needed to reach the UI state where the
failing element would appear in a browser. The application is Zoho ServiceDesk Plus.

Each step must be a JSON object with:
  - "action": "navigate" | "click" | "fill"
  - "selector": CSS selector or XPath (for click/fill actions)
  - "value": URL (for navigate) or text value (for fill)
  - "label": short label describing the step (e.g. "open_new_solution_form")

RULES:
- Include ONLY essential steps (navigate to module, click New, fill required fields to open a popup etc.)
- Max 8 steps
- Prefer generic stable selectors (button[contains text], [id=...])
- Return ONLY a JSON array

Example:
[
  {{"action": "click", "selector": "a[href*='new_solution']", "value": "", "label": "click_new_solution"}},
  {{"action": "click", "selector": "button:has-text('Add And Approve')", "value": "", "label": "click_add_and_approve"}}
]"""

        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a Selenium navigation expert. Return only valid JSON."),
                HumanMessage(content=prompt),
            ])
            text = response.content.strip()
            text = re.sub(r"```json\s*|\s*```", "", text).strip()
            steps = json.loads(text)
            if isinstance(steps, list):
                return steps
        except Exception as ex:
            print(f"[HealerAgent] LLM navigation inference failed: {ex}")

        # Fallback: minimal default steps
        return [
            {"action": "click", "selector": "a[href*='new'], button:has-text('New')", "value": "", "label": "click_new"},
        ]

    def _extract_broken_locator_hint(self, stdout: str, stderr: str, source_files: list) -> str:
        """
        Try to identify which locator constant name caused the failure
        from the error output and stack trace.
        """
        combined = stdout + stderr
        hints = []

        # Look for LOCATOR constant names (UPPER_SNAKE_CASE) in the error context
        locator_pattern = re.compile(r'\b([A-Z][A-Z0-9_]{3,})\b')
        for line in combined.splitlines():
            if any(kw in line for kw in ["NoSuchElement", "TimeoutException", "unable to locate",
                                          "ElementNotInteractable", "StaleElement"]):
                matches = locator_pattern.findall(line)
                hints.extend(matches)

        # Also check java stack trace for line numbers, then read source
        line_match = re.search(r'SolutionBase\.java:(\d+)', combined)
        if line_match and source_files:
            lineno = int(line_match.group(1))
            for sf in source_files:
                if "Base" in sf and Path(sf).exists():
                    lines = Path(sf).read_text(encoding="utf-8").splitlines()
                    start = max(0, lineno - 5)
                    end   = min(len(lines), lineno + 5)
                    excerpt = "\n".join(lines[start:end])
                    # Find locator references like SolutionLocators.X.CONSTANT
                    matches = re.findall(r'[A-Za-z]+Locators\.[A-Za-z]+\.([A-Z_]+)', excerpt)
                    hints.extend(matches)

        return ", ".join(set(hints)) if hints else "unknown (see error above)"

    # ── Compilation helpers ───────────────────────────────────────────────

    def _recompile_files(self, file_paths: list) -> bool:
        """Recompile a list of .java files using existing bin/ as classpath."""
        classpath_parts = [str(self.bin_dir)]
        for jar in self.deps_dir.rglob("*.jar"):
            classpath_parts.append(str(jar))
        classpath = ":".join(classpath_parts)

        cmd = [
            "javac",
            "-encoding", "UTF-8",
            "-cp", classpath,
            "-d", str(self.bin_dir),
        ] + file_paths

        print(f"[HealerAgent] Compiling {len(file_paths)} file(s)...")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.automater_root))
        if result.returncode != 0:
            print(f"[HealerAgent] ⚠️  Compile error:\n{result.stderr[:1000]}")
            return False
        print("[HealerAgent] ✅ Recompile successful")
        return True

    def _rerun_test(self, run_config: dict) -> bool:
        """Re-run the test using RunnerAgent to verify the fix."""
        from agents.runner_agent import RunnerAgent
        runner = RunnerAgent(
            base_dir=str(self.base),
            deps_dir=str(self.deps_dir),
            pre_compiled_bin_dir=str(self.bin_dir),
        )
        result = runner.run_test(
            entity_class=run_config.get("entity_class", ""),
            method_name=run_config.get("method_name", ""),
            url=run_config.get("url", DEFAULT_URL),
            email_id=run_config.get("email_id"),
            portal_name=run_config.get("portal_name"),
            admin_mail_id=run_config.get("admin_mail_id"),
            skip_compile=True,  # We already compiled above
        )
        print(f"[HealerAgent] Rerun result: {'✅ PASSED' if result.success else '❌ FAILED'}")
        return result.success

    # ── Source file helpers ───────────────────────────────────────────────

    def _find_source_files(self, entity_class: str) -> list:
        """Find the Base + Locators Java source files for an entity class."""
        files = []
        module_dir = None

        # Map entity class to module directory
        class_lower = entity_class.lower()
        for candidate in self.src_dir.rglob(f"{entity_class}Base.java"):
            module_dir = candidate.parent
            files.append(str(candidate))
            break

        if not files:
            for candidate in self.src_dir.rglob(f"{entity_class}CommonBase.java"):
                module_dir = candidate.parent
                files.append(str(candidate))
                break

        # Find locators file
        locator_file = self._find_locator_file(entity_class)
        if locator_file:
            files.append(locator_file)

        # Find the entity class itself
        for candidate in self.src_dir.rglob(f"{entity_class}.java"):
            files.append(str(candidate))
            break

        return files

    def _find_locator_file(self, entity_class: str) -> Optional[str]:
        """Find the *Locators.java file for an entity class."""
        for candidate in self.src_dir.rglob(f"{entity_class}Locators.java"):
            return str(candidate)
        return None

    def _read_source_snippet(self, source_files: list, max_lines: int = 80) -> str:
        """Read a snippet from source files (first max_lines relevant lines)."""
        snippets = []
        for path in source_files:
            if Path(path).exists():
                lines = Path(path).read_text(encoding="utf-8").splitlines()
                snippets.append(f"// {path}\n" + "\n".join(lines[:max_lines]))
        return "\n\n".join(snippets)

    def _read_full_source(self, source_files: list, max_chars: int = 8000) -> str:
        """Read full source of multiple files, up to max_chars total."""
        combined = []
        remaining = max_chars
        for path in source_files:
            if Path(path).exists() and remaining > 0:
                content = Path(path).read_text(encoding="utf-8")
                chunk = content[:remaining]
                combined.append(f"// === {path} ===\n{chunk}")
                remaining -= len(chunk)
        return "\n\n".join(combined)

    def _extract_error_snippet(self, stdout: str, stderr: str, max_lines: int = 30) -> str:
        """Extract the most relevant error lines from combined output."""
        combined = stdout + "\n" + stderr
        relevant = []
        for line in combined.splitlines():
            if any(kw in line for kw in [
                "Exception", "Error", "FAILED", "addFailureReport",
                "Caused by", "NoSuchElement", "TimeoutException",
                "NullPointer", "Unable to locate", "$$Failure",
                "cannot find symbol",
            ]):
                relevant.append(line)
        return "\n".join(relevant[:max_lines]) if relevant else combined.splitlines()[-20:] and "\n".join(combined.splitlines()[-20:])
