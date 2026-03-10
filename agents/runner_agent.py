"""
runner_agent.py
---------------
Runner Agent: Executes a generated test case against a target URL by
dynamically patching AutomaterSeleniumMain.java with the correct entity
class and method name, compiling the project, and invoking the test.

Responsibilities:
  1. Accept target URL, entity class, and method name
  2. Patch StandaloneDefault.java SERVER_URL with the provided URL
  3. Patch AutomaterSeleniumMain.java entity class + method name
  4. Compile the AutomaterSelenium project via Eclipse/javac
  5. Execute the test via the compiled main class
  6. Capture stdout/stderr and parse pass/fail from report output
  7. Return a RunResult with status, log, and report path

Can be used standalone (runner_agent.run_test(...)) or wired into the
LangGraph pipeline after the output agent.

Pipeline position (optional extension):
  ... → output → runner → END
"""

import os
import re
import subprocess
import shutil
import warnings
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict

from agents.state import AgentState
from config.project_config import (
    PROJECT_NAME,
    DEPS_DIR as _DEFAULT_DEPS_DIR,
    FIREFOX_BINARY as _DEFAULT_FIREFOX,
    GECKODRIVER_PATH as _DEFAULT_GECKODRIVER,
    TEST_EXECUTION_TIMEOUT as _TEST_EXECUTION_TIMEOUT,
    HEADLESS as _HEADLESS,
    SDP_URL as _DEFAULT_SDP_URL,
    SDP_PORTAL as _DEFAULT_SDP_PORTAL,
    SDP_ADMIN_EMAIL as _DEFAULT_SDP_ADMIN_EMAIL,
    SDP_EMAIL_ID as _DEFAULT_SDP_EMAIL_ID,
    SDP_ADMIN_PASS as _DEFAULT_SDP_ADMIN_PASS,
    SDP_TEST_USER_EMAILS as _DEFAULT_SDP_TEST_USER_EMAILS,
)


# ── Constants ──────────────────────────────────────────────────────────────

STANDALONE_DEFAULT_PATH = (
    f"{PROJECT_NAME}/src/com/zoho/automater/selenium/standalone/StandaloneDefault.java"
)
MAIN_CLASS_PATH = (
    f"{PROJECT_NAME}/src/com/zoho/automater/selenium/standalone/AutomaterSeleniumMain.java"
)

# ── Dynamic entity-class → FQCN map ───────────────────────────────────────────
#
# Support-class suffixes that are never passed as an entity_class — excluding
# them from the map avoids noisy duplicate warnings for Locators/Constants/etc.
# that exist in both requests.task and problems.task, for example.
_SUPPORT_SUFFIXES = (
    "Locators", "Constants", "DataConstants", "AnnotationConstants",
    "Fields", "Base", "APIUtil", "Actions", "Utils", "Helper",
)

# Aliases: lookup key that DIFFERS from the actual Java filename.
# Add one entry per alias — never add keys whose name already matches the file.
#
# Format: "CallerUsedName": "ActualJavaFileName"
#   where ActualJavaFileName uniquely identifies one .java file in the modules tree.
#   If the same filename exists in multiple modules, use the full simple name
#   to disambiguate via the module prefix pattern below.
_ENTITY_ALIASES: Dict[str, str] = {
    # Changes
    "ChangeDetailsView":     "DetailsView",       # DetailsView.java lives in changes.change
    "ChangeListView":        "ListView",           # ListView.java → changes (last-found wins; use alias for releases)
    "ChangeUATTask":         "UATTask",            # UATTask → changes.changetask (scan last-wins)
    "ChangeReleaseTask":     "ReleaseTask",
    "ChangeSubmissionTask":  "SubmissionTask",
    "ChangeReviewTask":      "ReviewTask",
    "ChangeCloseTask":       "CloseTask",
    "ChangePlanningTask":    "PlanningTask",
    # Note: Request/Problem sub-entities (Task, Worklog, Reminder) are in _FQCN_OVERRIDES
    # with explicit module paths — do not add them here as simple-name aliases.
}

# For cross-module aliases that resolve to the same simple name, we need the
# full module path override.  Store those here as {alias_key: full_fqcn}.
_FQCN_OVERRIDES: Dict[str, str] = {
    # Releases versions (scan last-wins gives changes; these keep releases)
    "ReleasesUATTask":       "com.zoho.automater.selenium.modules.releases.releasetask.UATTask",
    "ReleasesReleaseTask":   "com.zoho.automater.selenium.modules.releases.releasetask.ReleaseTask",
    "ReleasesSubmissionTask":"com.zoho.automater.selenium.modules.releases.releasetask.SubmissionTask",
    "ReleasesReviewTask":    "com.zoho.automater.selenium.modules.releases.releasetask.ReviewTask",
    "ReleasesCloseTask":     "com.zoho.automater.selenium.modules.releases.releasetask.CloseTask",
    "ReleasesPlanningTask":  "com.zoho.automater.selenium.modules.releases.releasetask.PlanningTask",
    "ReleasesListView":      "com.zoho.automater.selenium.modules.releases.release.ListView",
    "ReleasesReleaseWorkflow":"com.zoho.automater.selenium.modules.releases.release.ReleaseWorkflow",
    "AdminChangeWorkflow":         "com.zoho.automater.selenium.modules.admin.automation.workflows.ChangeWorkflow",
    "AdminIncidentRequestWorkflow":"com.zoho.automater.selenium.modules.admin.automation.workflows.IncidentRequestWorkflow",
    "AdminServiceRequestWorkflow": "com.zoho.automater.selenium.modules.admin.automation.workflows.ServiceRequestWorkflow",
    "AdminProblemWorkflow":        "com.zoho.automater.selenium.modules.admin.automation.workflows.ProblemWorkflow",
    "AdminReleaseWorkflow":        "com.zoho.automater.selenium.modules.admin.automation.workflows.ReleaseWorkflow",
    "AdminAssetWorkflow":          "com.zoho.automater.selenium.modules.admin.automation.workflows.AssetWorkflow",
    # Requests sub-entity versions
    "RequestTask":           "com.zoho.automater.selenium.modules.requests.task.Task",
    "RequestWorklog":        "com.zoho.automater.selenium.modules.requests.worklog.Worklog",
    "RequestReminder":       "com.zoho.automater.selenium.modules.requests.reminder.Reminder",
    # Problems sub-entity versions
    "ProblemTask":           "com.zoho.automater.selenium.modules.problems.task.Task",
    "ProblemWorklog":        "com.zoho.automater.selenium.modules.problems.worklog.Worklog",
    "ProblemReminder":       "com.zoho.automater.selenium.modules.problems.reminder.Reminder",
}


def _build_entity_import_map() -> Dict[str, str]:
    """
    Scan SDPLIVE_LATEST_AUTOMATER_SELENIUM/src/com/zoho/automater/selenium/modules/
    and build a {SimpleClassName: fully.qualified.ClassName} dict automatically.

    Strategy
    --------
    Every .java file under the modules/ tree has a path of the form:
        .../src/<pkg/path>/<ClassName>.java
    The FQCN is simply the part after `src/` with `/` → `.` and `.java` stripped.

    Support classes (Locators, Constants, Base, etc.) are excluded — they are
    never used as entity_class values so we skip them to suppress noisy warnings.

    Duplicate runnable class names across modules are warned about once.
    _FQCN_OVERRIDES is merged in last to provide stable aliases for
    callers that need the non-default module's version.
    """
    _base_src = (
        Path(__file__).resolve().parents[1]
        / PROJECT_NAME
        / "src"
        / "com" / "zoho" / "automater" / "selenium" / "modules"
    )

    if not _base_src.exists():
        warnings.warn(
            f"[RunnerAgent] modules src dir not found at {_base_src}; "
            "ENTITY_IMPORT_MAP will be empty — tests may fail with ClassNotFoundException.",
            RuntimeWarning,
            stacklevel=2,
        )
        return {}

    src_root = _base_src.parents[4]   # .../SDPLIVE_.../src

    result: Dict[str, str] = {}
    for java_file in _base_src.rglob("*.java"):
        simple = java_file.stem

        # Skip support / base classes — never used as entity_class
        if simple.endswith(_SUPPORT_SUFFIXES):
            continue

        fqcn = str(java_file.relative_to(src_root)).replace("/", ".").replace(".java", "")

        if simple in result and result[simple] != fqcn:
            warnings.warn(
                f"[RunnerAgent] Duplicate entity class name '{simple}': "
                f"'{result[simple]}' overridden by '{fqcn}'. "
                f"Use a prefixed alias in _FQCN_OVERRIDES if both are needed.",
                RuntimeWarning,
                stacklevel=2,
            )
        result[simple] = fqcn

    # Resolve simple-name aliases
    for alias_key, target_simple in _ENTITY_ALIASES.items():
        if alias_key in _FQCN_OVERRIDES:
            continue   # full-path override wins — applied below
        if target_simple in result:
            result[alias_key] = result[target_simple]
        else:
            warnings.warn(
                f"[RunnerAgent] Alias '{alias_key}' → '{target_simple}' could not be "
                f"resolved ('{target_simple}' not in scan). Check _ENTITY_ALIASES.",
                RuntimeWarning,
                stacklevel=2,
            )

    # Apply full-path overrides (highest priority)
    result.update(_FQCN_OVERRIDES)

    print(f"[RunnerAgent] ENTITY_IMPORT_MAP: {len(result)} classes discovered from src/.")
    return result


# Built once at import time — zero per-test overhead.
ENTITY_IMPORT_MAP: Dict[str, str] = _build_entity_import_map()


class RunResult:
    """Holds the outcome of a single test execution."""

    def __init__(
        self,
        success: bool,
        method_name: str,
        entity_class: str,
        url: str,
        stdout: str = "",
        stderr: str = "",
        report_path: str = "",
        error: str = "",
    ):
        self.success = success
        self.method_name = method_name
        self.entity_class = entity_class
        self.url = url
        self.stdout = stdout
        self.stderr = stderr
        self.report_path = report_path
        self.error = error
        self.timestamp = datetime.now().isoformat()

    def summary(self) -> str:
        status = "✅ PASSED" if self.success else "❌ FAILED"
        lines = [
            f"{status} — {self.entity_class}.{self.method_name}",
            f"  URL        : {self.url}",
            f"  Timestamp  : {self.timestamp}",
        ]
        if self.report_path:
            lines.append(f"  Report     : {self.report_path}")
        if self.error:
            lines.append(f"  Error      : {self.error}")
        return "\n".join(lines)

    def to_dict(self) -> dict:
        return {
            "success":      self.success,
            "method_name":  self.method_name,
            "entity_class": self.entity_class,
            "url":          self.url,
            "stdout":       self.stdout[-3000:],   # truncate for state
            "stderr":       self.stderr[-1000:],
            "report_path":  self.report_path,
            "error":        self.error,
            "timestamp":    self.timestamp,
        }


class RunnerAgent:
    """
    Patches AutomaterSeleniumMain.java and StandaloneDefault.java,
    compiles the project, and runs the specified test method.
    """

    def __init__(self, base_dir: str = None, deps_dir: str = None, pre_compiled_bin_dir: str = None):
        self.base = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self.automater_root = self.base / PROJECT_NAME
        self.bin_dir = Path(pre_compiled_bin_dir) if pre_compiled_bin_dir else self.automater_root / "bin"
        self.src_dir = self.automater_root / "src"
        self.resources_dir = self.automater_root / "resources"
        # deps_dir: folder containing all runtime *.jar files
        self.deps_dir = Path(deps_dir) if deps_dir else Path(_DEFAULT_DEPS_DIR)

        self._standalone_default = self.base / STANDALONE_DEFAULT_PATH
        self._main_class = self.base / MAIN_CLASS_PATH
        self._app_properties = self.automater_root / "product_package" / "conf" / "app.properties"

    # ── Public API ─────────────────────────────────────────────────────────

    def run_test(
        self,
        entity_class: str,
        method_name: str,
        url: Optional[str] = None,
        email_id: Optional[str] = None,
        portal_name: Optional[str] = None,
        admin_mail_id: Optional[str] = None,
        skip_compile: bool = False,
        password: Optional[str] = None,
        skip_cleanup: bool = False,
    ) -> RunResult:
        """
        Patch, compile (optional), and execute a single test method.

        All credential/URL parameters default to values from config/project_config.py
        (the single source of truth).  Pass explicit values only to override.

        Args:
            entity_class  : Simple class name, e.g. "Solution"
            method_name   : Method to run, e.g. "createAndShareApprovedPublicSolutionFromDV"
            url           : Target server URL (default: SDP_URL from project_config)
            email_id      : Technician user email (default: SDP_EMAIL_ID from project_config)
            portal_name   : Portal name (default: SDP_PORTAL from project_config)
            admin_mail_id : Admin email (default: SDP_ADMIN_EMAIL from project_config)
            skip_compile  : If True, skip compilation (use existing bin/)
            password      : User password (default: SDP_ADMIN_PASS from project_config)
            skip_cleanup  : If True, pass -DskipCleanup=true to the JVM so postProcess()
                            and finally-block deletes are skipped — useful for debugging.
        """
        # Resolve defaults from project_config.py (single source of truth)
        url           = url           or _DEFAULT_SDP_URL
        email_id      = email_id      or _DEFAULT_SDP_EMAIL_ID
        portal_name   = portal_name   or _DEFAULT_SDP_PORTAL
        admin_mail_id = admin_mail_id or _DEFAULT_SDP_ADMIN_EMAIL
        password      = password      or _DEFAULT_SDP_ADMIN_PASS

        print(f"[RunnerAgent] Preparing to run: {entity_class}.{method_name}")
        print(f"[RunnerAgent] Target URL: {url}")
        print(f"[RunnerAgent] Admin: {admin_mail_id}  |  Email: {email_id}  |  Portal: {portal_name}")

        # Stamp browser paths from env into app.properties before the JVM starts
        self._patch_app_properties()

        try:
            # 1. Backup StandaloneDefault.java and AutomaterSeleniumMain.java
            default_backup = self._backup(self._standalone_default)
            main_backup = self._backup(self._main_class)

            try:
                # 2. Patch StandaloneDefault.java with the provided URL / credentials
                self._patch_standalone_default(url, email_id, portal_name, admin_mail_id, password)

                # 2b. Patch test user emails in AutomaterSeleniumMain.java (if configured)
                self._patch_test_user_emails(_DEFAULT_SDP_TEST_USER_EMAILS)

                # 3. Full project compile (optional)
                if not skip_compile:
                    compile_result = self._compile()
                    if compile_result.returncode != 0:
                        return RunResult(
                            success=False,
                            method_name=method_name,
                            entity_class=entity_class,
                            url=url,
                            stderr=compile_result.stderr,
                            error=f"Compilation failed:\n{compile_result.stderr[:2000]}",
                        )
                    print("[RunnerAgent] Full compilation succeeded.")

                # 3b. Always recompile StandaloneDefault.java to bake in new URL/credentials
                patch_compile = self._compile_patched_files()
                if patch_compile.returncode != 0:
                    return RunResult(
                        success=False,
                        method_name=method_name,
                        entity_class=entity_class,
                        url=url,
                        stderr=patch_compile.stderr,
                        error=f"Patch compilation failed:\n{patch_compile.stderr[:2000]}",
                    )

                # 4. Execute — entity class FQCN and method name passed as CLI args
                run_result = self._execute(entity_class, method_name, skip_cleanup=skip_cleanup)
                success = self._parse_success(run_result.stdout, run_result.stderr)
                report_path = self._find_latest_report(method_name)

                # ── HTML report override ─────────────────────────────────────
                # 1. If _parse_success returned False but the HTML report says
                #    PASS (cleanup NPE on no-display env), promote to True.
                # 2. If _parse_success returned True but the HTML report says
                #    FAIL (e.g. _parse_success missed the error — see leading-space
                #    class-check bug), demote to False.  This is the authoritative
                #    override: the HTML report is the ground truth.
                # 3. If _parse_success returned True but the report directory is
                #    empty (no HTML written — test never ran), demote to False.
                if report_path:
                    html_file = Path(report_path) / "ScenarioReport.html"
                    if html_file.exists():
                        content = html_file.read_text(encoding="utf-8", errors="ignore")
                        if not success:
                            # Promote False→True only when HTML has NO failure markers
                            if 'data-result="FAIL"' not in content and 'data-result="PASS"' in content:
                                success = True
                        else:
                            # Demote True→False when HTML's overall result is FAIL
                            # ScenarioReport writes: class="scenario-result FAIL"
                            if 'scenario-result FAIL' in content:
                                print("[RunnerAgent] ⚠️  HTML report shows scenario-result FAIL — overriding _parse_success True→False")
                                success = False
                    elif success and not html_file.exists():
                        # Report dir was created by LocalSetupManager but test
                        # exited before writing the HTML → treat as failure.
                        print(f"[RunnerAgent] ⚠️  Report directory is empty (no HTML written) — marking FAIL")
                        success = False
                elif success:
                    # No report directory at all and no explicit success signal → FAIL
                    print(f"[RunnerAgent] ⚠️  No report directory found — marking FAIL")
                    success = False

                if not success:
                    print("[RunnerAgent] ── Captured Error ─────────────────────────")
                    for line in (run_result.stdout + "\n" + run_result.stderr).splitlines():
                        if any(kw in line for kw in ["Exception", "Error", "FAILED", "addFailureReport", "Caused by"]):
                            print(f"  ⚠️  {line}")

                return RunResult(
                    success=success,
                    method_name=method_name,
                    entity_class=entity_class,
                    url=url,
                    stdout=run_result.stdout,
                    stderr=run_result.stderr,
                    report_path=report_path,
                    error="" if success else self._extract_error(run_result.stdout, run_result.stderr),
                )

            finally:
                # Restore StandaloneDefault.java and AutomaterSeleniumMain.java to original state
                self._restore(self._standalone_default, default_backup)
                self._restore(self._main_class, main_backup)

        except Exception as exc:
            return RunResult(
                success=False,
                method_name=method_name,
                entity_class=entity_class,
                url=url,
                error=str(exc),
            )

    # ── LangGraph node entry point ─────────────────────────────────────────

    def run(self, state: AgentState) -> AgentState:
        """
        LangGraph node: reads run_config from state and executes the test.

        State keys consumed:
          state['run_config'] = {
              "entity_class": "Solution",
              "method_name":  "createAndShareApprovedPublicSolutionFromDV",
              "url":          "http://sdpod-auto1:8080/",
              "email_id":     "...",           # optional
              "portal_name":  "...",           # optional
              "admin_mail_id": "...",          # optional
              "skip_compile": False,           # optional
          }

        State keys produced:
          state['run_result']  = RunResult.to_dict()
          state['messages']    += [summary string]
        """
        config = state.get("run_config", {})
        if not config:
            state["messages"] = [
                "[RunnerAgent] No run_config found in state — skipping execution."
            ]
            return state

        result = self.run_test(
            entity_class=config.get("entity_class", ""),
            method_name=config.get("method_name", ""),
            url=config.get("url"),
            email_id=config.get("email_id"),
            portal_name=config.get("portal_name"),
            admin_mail_id=config.get("admin_mail_id"),
            skip_compile=config.get("skip_compile", False),
            password=config.get("password"),
        )

        state["run_result"] = result.to_dict()
        state["messages"] = [result.summary()]
        print(result.summary())
        return state

    # ── Patching helpers ───────────────────────────────────────────────────

    def _patch_standalone_default(
        self,
        url: str,
        email_id: str,
        portal_name: str,
        admin_mail_id: str,
        password: str,
    ) -> None:
        """Replace SERVER_URL, EMAIL_ID, PORTAL_NAME, ADMIN_MAIL_ID, and DEFAULT_PASSWORD
        in StandaloneDefault.java.  All values are always provided (resolved from
        project_config.py defaults in run_test())."""
        content = self._standalone_default.read_text(encoding="utf-8")

        # Ensure URL ends with '/' so Java concatenation produces valid URLs
        # e.g. "https://host:8080" + "app/portal/..." → needs slash separator
        url = url.rstrip("/") + "/"

        # Replace the active (uncommented) SERVER_URL line
        content = re.sub(
            r'^(\s*public static final String SERVER_URL\s*=\s*)"[^"]*"(;)',
            rf'\1"{url}"\2',
            content,
            flags=re.MULTILINE,
        )

        content = re.sub(
            r'^(\s*protected static final String EMAIL_ID\s*=\s*)"[^"]*"(;)',
            rf'\1"{email_id}"\2',
            content,
            flags=re.MULTILINE,
        )

        content = re.sub(
            r'^(\s*(?:private|protected) static final String PORTAL_NAME\s*=\s*)"[^"]*"(;)',
            rf'\1"{portal_name}"\2',
            content,
            flags=re.MULTILINE,
        )

        content = re.sub(
            r'^(\s*private static final String ADMIN_MAIL_ID\s*=\s*)"[^"]*"(;)',
            rf'\1"{admin_mail_id}"\2',
            content,
            flags=re.MULTILINE,
        )

        content = re.sub(
            r'^(\s*protected static final String DEFAULT_PASSWORD\s*=\s*)"[^"]*"(;)',
            rf'\1"{password}"\2',
            content,
            flags=re.MULTILINE,
        )

        self._standalone_default.write_text(content, encoding="utf-8")
        print(f"[RunnerAgent] Patched StandaloneDefault.java → URL={url}, admin={admin_mail_id}, "
              f"email={email_id}, portal={portal_name}, password=***")

    def _patch_test_user_emails(self, test_user_emails: str) -> None:
        """Patch the hardcoded test user emails in AutomaterSeleniumMain.setupUsers().

        Args:
            test_user_emails: Comma-separated emails for TEST_USER_1..4.
                              If fewer than 4, the last email is reused for remaining slots.
                              If empty/blank, no patching is done (keeps existing hardcoded values).
        """
        if not test_user_emails or not test_user_emails.strip():
            return

        emails = [e.strip() for e in test_user_emails.split(",") if e.strip()]
        if not emails:
            return

        # Pad to 4 entries by reusing the last email
        while len(emails) < 4:
            emails.append(emails[-1])

        content = self._main_class.read_text(encoding="utf-8")

        # Pattern matches: getUser("any@email.com") on lines containing TEST_USER_N
        user_patterns = [
            (r'(ScenarioUsers\.TEST_USER_1.*?getUser\()"[^"]*"', emails[0]),
            (r'(ScenarioUsers\.TEST_USER_2.*?getUser\()"[^"]*"', emails[1]),
            (r'(ScenarioUsers\.TEST_USER_3.*?getUser\()"[^"]*"', emails[2]),
            (r'(ScenarioUsers\.TEST_USER_4.*?getUser\()"[^"]*"', emails[3]),
        ]

        # Reverse approach: find the getUser("...") call on lines that put TEST_USER_N
        for i, (_, email) in enumerate(user_patterns, start=1):
            # Match: getUser("old@email") on a line that contains TEST_USER_{i}
            pattern = rf'(puts?\(ScenarioUsers\.TEST_USER_{i}.*?)getUser\("[^"]*"\)'
            replacement = rf'\1getUser("{email}")'
            new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            if new_content == content:
                # Fallback: match the two-line pattern (getUser on previous line)
                pattern2 = rf'(User user{i}\s*=\s*getUser\()"[^"]*"'
                replacement2 = rf'\1"{email}"'
                new_content = re.sub(pattern2, replacement2, content)
            content = new_content

        self._main_class.write_text(content, encoding="utf-8")
        print(f"[RunnerAgent] Patched AutomaterSeleniumMain.java test users → "
              f"TU1={emails[0]}, TU2={emails[1]}, TU3={emails[2]}, TU4={emails[3]}")

    def _patch_main_class(self, entity_class: str, method_name: str) -> None:
        """
        Replace the entity class and methodName in AutomaterSeleniumMain.java.
        Also ensures the correct import is present.
        """
        content = self._main_class.read_text(encoding="utf-8")

        # ── Update import ──
        fqcn = ENTITY_IMPORT_MAP.get(entity_class)
        if fqcn:
            # Remove any existing entity import lines and add the correct one
            content = re.sub(
                r'^\s*import com\.zoho\.automater\.selenium\.modules\.[^;]+;\s*\n',
                "",
                content,
                flags=re.MULTILINE,
            )
            # Insert after the last framework import
            content = re.sub(
                r'(import com\.zoho\.setup\.SetupVariables;)',
                rf'import {fqcn};\nimport com.zoho.setup.SetupVariables;',
                content,
            )

        # ── Update entity class ──
        # Replace: Class<?> entity = <Anything>.class;
        content = re.sub(
            r'(\s*)Class<\?> entity\s*=\s*\w+\.class;',
            rf'\t\t\tClass<?> entity = {entity_class}.class;',
            content,
        )

        # ── Update method name ──
        # Replace: String methodName = "<anything>";
        content = re.sub(
            r'(\s*)String methodName\s*=\s*"[^"]*";',
            rf'\t\t\tString methodName = "{method_name}";',
            content,
        )

        self._main_class.write_text(content, encoding="utf-8")
        print(f"[RunnerAgent] Patched AutomaterSeleniumMain.java → {entity_class}.{method_name}")

    # ── Compile & run ──────────────────────────────────────────────────────

    def _patch_app_properties(self) -> None:
        """Overwrite firefox_local and geckodriver_local in app.properties with
        values from FIREFOX_BINARY / GECKODRIVER_PATH env vars (set in .env).

        This is the single point that makes browser-driver paths portable:
        deploying to a new machine only requires updating .env — no Java
        source files need touching.
        """
        props_path = self._app_properties
        if not props_path.exists():
            print(f"[RunnerAgent] Warning: app.properties not found at {props_path} — skipping browser path patch")
            return

        firefox     = _DEFAULT_FIREFOX
        geckodriver = _DEFAULT_GECKODRIVER

        headless_str = "true" if _HEADLESS else "false"

        lines = props_path.read_text(encoding="utf-8").splitlines()
        updated = []
        for line in lines:
            if line.startswith("firefox_local="):
                updated.append(f"firefox_local={firefox}")
            elif line.startswith("geckodriver_local="):
                updated.append(f"geckodriver_local={geckodriver}")
            elif line.startswith("headless="):
                updated.append(f"headless={headless_str}")
            else:
                updated.append(line)
        props_path.write_text("\n".join(updated) + "\n", encoding="utf-8")
        print(f"[RunnerAgent] app.properties → firefox_local={firefox}")
        print(f"[RunnerAgent] app.properties → geckodriver_local={geckodriver}")
        print(f"[RunnerAgent] app.properties → headless={headless_str}")

    def _compile_patched_files(self) -> subprocess.CompletedProcess:
        """
        Always-on fast compile: recompile the patched standalone files so the
        new URL / credentials are baked into the bytecode.

        CRITICAL: Must compile BOTH StandaloneDefault.java AND
        AutomaterSeleniumMain.java.  Java inlines `static final String`
        constants at compile time — if only StandaloneDefault is recompiled,
        AutomaterSeleniumMain.class keeps the OLD inlined values for
        EMAIL_ID, DEFAULT_PASSWORD, PORTAL_NAME, SERVER_URL.
        """
        classpath_parts = [str(self.bin_dir)]
        for jar in self.deps_dir.rglob("*.jar"):
            classpath_parts.append(str(jar))
        classpath = ":".join(classpath_parts)

        files = [
            str(self._standalone_default),
            str(self._main_class),  # Must recompile — inherits inlined constants from parent
        ]

        cmd = [
            "javac",
            "-encoding", "UTF-8",
            "-cp", classpath,
            "-d", str(self.bin_dir),
        ] + files

        print(f"[RunnerAgent] Compiling patched StandaloneDefault.java + AutomaterSeleniumMain.java (fast)...")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.automater_root))
        if result.returncode != 0:
            print(f"[RunnerAgent] ⚠️  Patch-compile error:\n{result.stderr[:1000]}")
        else:
            print("[RunnerAgent] Patch-compile OK.")
        return result

    def _compile(self) -> subprocess.CompletedProcess:
        """
        Compile the AutomaterSelenium project using javac with the
        dependencies jar on the classpath.
        """
        classpath_parts = [str(self.bin_dir)]

        # Add all jars from deps_dir (top-level + framework/ subdir)
        for jar in self.deps_dir.rglob("*.jar"):
            classpath_parts.append(str(jar))

        classpath = ":".join(classpath_parts)

        # Collect all .java source files
        java_files = list(self.src_dir.rglob("*.java"))
        src_list_file = self.automater_root / "_src_files.txt"
        src_list_file.write_text("\n".join(str(f) for f in java_files), encoding="utf-8")

        self.bin_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            "javac",
            "-encoding", "UTF-8",
            "-cp", classpath,
            "-d", str(self.bin_dir),
            f"@{src_list_file}",
        ]

        print(f"[RunnerAgent] Compiling {len(java_files)} source files...")
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.automater_root))

        src_list_file.unlink(missing_ok=True)
        return result

    def _execute(self, entity_class: str, method_name: str, skip_cleanup: bool = False) -> subprocess.CompletedProcess:
        """Run the compiled AutomaterSeleniumMain class, streaming output live.
        
        New execution model: entity class (FQCN) and method name are passed as
        command-line args[0] and args[1] — no source patching of Main.java required.
        """
        classpath_parts = [str(self.bin_dir), str(self.resources_dir)]

        for jar in self.deps_dir.rglob("*.jar"):
            classpath_parts.append(str(jar))

        classpath = ":".join(classpath_parts)

        # Resolve fully-qualified class name for args[0]
        fqcn = ENTITY_IMPORT_MAP.get(entity_class, entity_class)

        cmd = [
            "java",
        ]
        if skip_cleanup:
            cmd.append("-DskipCleanup=true")
            print("[RunnerAgent] skip_cleanup=True → passing -DskipCleanup=true to JVM (postProcess/finally deletes disabled)")
        cmd += [
            "-cp", classpath,
            "com.zoho.automater.selenium.standalone.AutomaterSeleniumMain",
            fqcn,          # args[0]: fully-qualified entity class name
            method_name,   # args[1]: method name to execute
        ]

        print(f"[RunnerAgent] Executing: {method_name} ...")
        print("[RunnerAgent] ─── Live Output ──────────────────────────────")

        import time as _time
        run_start_ms = int(_time.time() * 1000)  # used to ignore stale report dirs

        stdout_lines = []
        stderr_lines = []

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.automater_root),
            # NOTE: do NOT use start_new_session=True — keeping the Java process
            # in the same process group ensures it is killed when the terminal/
            # parent process exits (e.g. Ctrl+C, session close).
        )

        # Stream stdout and stderr simultaneously
        import threading
        import psutil

        def stream(pipe, lines, label):
            for line in iter(pipe.readline, ""):
                line = line.rstrip()
                lines.append(line)
                print(f"  [{label}] {line}")
            pipe.close()

        t_out = threading.Thread(target=stream, args=(process.stdout, stdout_lines, "OUT"), daemon=True)
        t_err = threading.Thread(target=stream, args=(process.stderr, stderr_lines, "ERR"), daemon=True)
        t_out.start()
        t_err.start()

        def _kill_tree(pid: int) -> None:
            """Kill a process and all its children — mirrors Eclipse's JVM termination.

            Eclipse terminates the JVM process entirely (no background survivors).
            We must do the same: kill Java + geckodriver + Firefox in one shot.
            """
            try:
                parent = psutil.Process(pid)
                children = parent.children(recursive=True)
                for child in children:
                    try:
                        child.kill()
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
                parent.kill()
                print(f"[RunnerAgent] 🔪 Killed process tree rooted at PID {pid} "
                      f"({len(children)} child(ren)).")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass  # already gone

        def _browser_watchdog(java_proc: subprocess.Popen, start_ms: int) -> None:
            """Mirror Eclipse behavior: once ScenarioReport.html is written the test
            is done — kill the entire process tree immediately (Java + geckodriver +
            Firefox).  In Eclipse, main() returns after LocalSetupManager.cleanup()
            writes the report and the JVM exits naturally; here Selenium's non-daemon
            threads keep the JVM alive, so we force-kill on the same signal.

            Fallback: if Firefox closes but the report never appears within 45 s,
            kill anyway to avoid a hung runner (handles cleanup() failures).

            start_ms: epoch-milliseconds recorded just before process launch.
            Only report directories with a timestamp suffix >= (start_ms - 10_000)
            are considered — this prevents a ScenarioReport.html from a *previous*
            run of the same method from triggering an early kill.
            """
            import time

            java_pid = java_proc.pid
            reports_dir = self.automater_root / "reports"

            def _report_exists() -> bool:
                all_matched = (
                    list(reports_dir.glob(f"LOCAL_{method_name}_*")) +
                    list(reports_dir.glob(f"{method_name}_*"))
                )
                # Only consider directories created by THIS run — filter by the
                # millisecond timestamp embedded in the directory name suffix.
                # Tolerance of 10 s (10_000 ms) covers JVM startup time.
                current_run_dirs = []
                for d in all_matched:
                    try:
                        suffix = int(d.name.rsplit("_", 1)[-1])
                        if suffix >= start_ms - 10_000:
                            current_run_dirs.append(d)
                    except ValueError:
                        pass
                if not current_run_dirs:
                    return False
                # Sort so newest is last, check for report
                current_run_dirs.sort(key=lambda p: p.name)
                return (current_run_dirs[-1] / "ScenarioReport.html").exists()

            def _child_browser_pids() -> set:
                try:
                    return {
                        p.pid for p in psutil.Process(java_pid).children(recursive=True)
                        if p.name().lower() in ("firefox", "firefox-bin", "geckodriver")
                    }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    return set()

            # Wait for Firefox to launch before we start watching
            print("[RunnerAgent] 👁  Watchdog started — waiting for Firefox launch...")
            for _ in range(30):           # up to 30 s
                if java_proc.poll() is not None:
                    return               # Java already exited on its own
                if _child_browser_pids():
                    break
                time.sleep(1)

            browser_died_at: float | None = None

            while java_proc.poll() is None:
                # ── Primary signal: report written → test complete ──────────
                if _report_exists():
                    print("[RunnerAgent] ✅ ScenarioReport.html detected — "
                          "killing process tree now (Eclipse-style clean exit).")
                    _kill_tree(java_pid)
                    break

                # ── Fallback: browser closed but report not yet written ─────
                browser_alive = bool(_child_browser_pids())
                if not browser_alive:
                    if browser_died_at is None:
                        browser_died_at = time.time()
                        print("[RunnerAgent] 🌐 Firefox closed — waiting up to 45 s "
                              "for ScenarioReport.html before force-kill...")
                    elif time.time() - browser_died_at > 45:
                        print("[RunnerAgent] ⚠️  Report not written 45 s after Firefox "
                              "closed — force-killing Java process tree.")
                        _kill_tree(java_pid)
                        break
                else:
                    browser_died_at = None   # Firefox relaunched / still alive

                time.sleep(2)

        watchdog = threading.Thread(target=_browser_watchdog, args=(process, run_start_ms), daemon=True)
        watchdog.start()

        timeout_s = _TEST_EXECUTION_TIMEOUT
        try:
            process.wait(timeout=timeout_s)
        except subprocess.TimeoutExpired:
            _kill_tree(process.pid)
            print(f"[RunnerAgent] ⚠️  Test timed out after {timeout_s}s "
                  f"({timeout_s // 60}m). Increase TEST_EXECUTION_TIMEOUT in .env if needed.")

        # Give reader threads a grace window to drain any remaining output
        # before we proceed, so no output lines are lost after process exit.
        t_out.join(timeout=30)
        t_err.join(timeout=30)

        print("[RunnerAgent] ─── End Output ───────────────────────────────")

        # Return a CompletedProcess-like object for compatibility
        class _Result:
            returncode = process.returncode
            stdout = "\n".join(stdout_lines)
            stderr = "\n".join(stderr_lines)

        return _Result()

    # ── Helpers ────────────────────────────────────────────────────────────

    def _parse_success(self, stdout: str, stderr: str) -> bool:
        """
        Determine pass/fail from output.
        Priority: framework's own markers take precedence over heuristics.
        """
        combined = stdout + stderr

        # ── Framework-level success/failure markers (highest priority) ──────
        # The SDP framework prints "$$Failure=Failure" for any test failure.
        # This MUST be checked before any "successfully" heuristic — a single run
        # can contain BOTH an addSuccessReport (from a passing step) AND an
        # addFailureReport (from a later failing step).  $$Failure always wins.
        if "$$Failure" in combined:
            return False
        if "addFailureReport" in combined:
            return False
        # The framework's addSuccessReport prints the success message in
        # "Additional Specific Info" — safe to treat as pass ONLY when no failure
        # markers are present (both guards above have already been checked).
        if '"Additional Specific Info":["' in combined and "successfully" in combined:
            return True

        # ── Build-level markers ───────────────────────────────────────────────
        if "BUILD FAILED" in combined:
            return False
        if "BUILD SUCCESSFUL" in combined:
            return True

        # ── Java runtime failure markers (avoid false positives from browser JS) ─
        java_fail_markers = [
            "addFailureReport",
            "Exception in thread",
            "NullPointerException",
            "NoSuchElementException",
            "TimeoutException",
            "WebDriverException",
            "AssertionException",
            "AssertionError",                     # Java stdlib assertion (≠ framework AssertionException)
            "StaleElementReferenceException",     # element gone between find and interact
            "ElementNotInteractableException",    # element present but not clickable/typeable
            "IllegalStateException",              # driver/session invalidated mid-test
            "IndexOutOfBoundsException",          # list/array mishandling in test logic
            "ClassNotFoundException",             # entity class missing from ENTITY_IMPORT_MAP
        ]
        for marker in java_fail_markers:
            if marker in combined:
                return False

        # ── LOCAL mode: parse ScenarioReport.html ────────────────────────────
        # In local mode addSuccessReport / addFailureReport write ONLY to the
        # HTML report — nothing appears in stdout/stderr.  We locate the report
        # from the INFO log line printed by LocalSetupManager and parse it.
        import re as _re
        html_match = _re.search(
            r"INFO: \[LOCAL\] Report successfully created: (.+?ScenarioReport\.html)",
            combined,
        )
        if html_match:
            report_path = html_match.group(1).strip()
            try:
                with open(report_path) as _f:
                    html_content = _f.read()
                # addFailureReport → <div class="error message-detail default">
                # ScenarioReport.java: .addClass(messageType + " message-detail " + messageClass).addClass("default")
                # jsoup normalises trailing spaces, so the class has NO leading space.
                if 'class="error message-detail' in html_content:
                    return False
                # Report exists, written cleanly, and no error entries → PASS
                return True
            except OSError:
                pass  # report unreadable — fall through to default

        # Default: no explicit positive signal → FAIL.
        # A test is only PASS when the framework emits a success marker,
        # BUILD SUCCESSFUL, or a clean local ScenarioReport with no errors.
        # Silently exiting (ClassNotFoundException caught, cleanup without
        # report, etc.) must NOT be treated as a pass.
        return False

    def _extract_error(self, stdout: str, stderr: str) -> str:
        """Pull the most relevant error line from combined output."""
        combined = stdout + stderr
        for line in combined.splitlines():
            if any(kw in line for kw in ["Exception", "Error", "FAILED", "addFailureReport"]):
                return line.strip()
        return "Unknown error — see stdout/stderr in run_result"

    def _find_latest_report(self, method_name: str) -> str:
        """Locate the most recently created report directory for this method.
        Handles both '<method>_<ts>' and 'LOCAL_<method>_<ts>' naming."""
        reports_dir = self.automater_root / "reports"
        if not reports_dir.exists():
            return ""
        matches = sorted(
            list(reports_dir.glob(f"{method_name}_*")) +
            list(reports_dir.glob(f"LOCAL_{method_name}_*")),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        return str(matches[0]) if matches else ""

    def _backup(self, path: Path) -> str:
        """Copy file to a temp backup and return backup path."""
        backup = str(path) + ".runner_bak"
        shutil.copy2(str(path), backup)
        return backup

    def _restore(self, path: Path, backup_path: str) -> None:
        """Restore file from backup and remove backup."""
        bak = Path(backup_path)
        if bak.exists():
            shutil.copy2(backup_path, str(path))
            bak.unlink()
