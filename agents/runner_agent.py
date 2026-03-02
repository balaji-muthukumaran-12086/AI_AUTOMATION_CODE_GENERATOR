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
from pathlib import Path
from datetime import datetime
from typing import Optional

from agents.state import AgentState
from config.project_config import (
    PROJECT_NAME,
    DEPS_DIR as _DEFAULT_DEPS_DIR,
    FIREFOX_BINARY as _DEFAULT_FIREFOX,
    GECKODRIVER_PATH as _DEFAULT_GECKODRIVER,
    TEST_EXECUTION_TIMEOUT as _TEST_EXECUTION_TIMEOUT,
    HEADLESS as _HEADLESS,
)


# ── Constants ──────────────────────────────────────────────────────────────

STANDALONE_DEFAULT_PATH = (
    f"{PROJECT_NAME}/src/com/zoho/automater/selenium/standalone/StandaloneDefault.java"
)
MAIN_CLASS_PATH = (
    f"{PROJECT_NAME}/src/com/zoho/automater/selenium/standalone/AutomaterSeleniumMain.java"
)

# Known entity class → fully-qualified import mapping
# IMPORTANT: Every entity class passed via tests_to_run.json MUST have an entry
# here. Missing entries cause Class.forName() to receive a simple name instead
# of a FQCN, throwing ClassNotFoundException that is silently caught by
# AutomaterSeleniumMain → browser opens then closes → reported as false-PASS.
ENTITY_IMPORT_MAP = {
    # ── Solutions ──────────────────────────────────────────────────────────
    "Solution":              "com.zoho.automater.selenium.modules.solutions.solution.Solution",
    # ── Requests ───────────────────────────────────────────────────────────
    "Request":               "com.zoho.automater.selenium.modules.requests.request.Request",
    "IncidentRequest":       "com.zoho.automater.selenium.modules.requests.request.IncidentRequest",
    "IncidentRequestNotes":  "com.zoho.automater.selenium.modules.requests.request.IncidentRequestNotes",
    "ServiceRequest":        "com.zoho.automater.selenium.modules.requests.request.ServiceRequest",
    "RequestNotes":          "com.zoho.automater.selenium.modules.requests.request.RequestNotes",
    # ── Problems ───────────────────────────────────────────────────────────
    "Problem":               "com.zoho.automater.selenium.modules.problems.problem.Problem",
    # ── Changes ────────────────────────────────────────────────────────────
    "Change":                "com.zoho.automater.selenium.modules.changes.change.Change",
    "CabEvaluationTask":     "com.zoho.automater.selenium.modules.changes.cabevaluationtask.CabEvaluationTask",
    # ── Releases ───────────────────────────────────────────────────────────
    "Release":               "com.zoho.automater.selenium.modules.releases.release.Release",
    "UATTask":               "com.zoho.automater.selenium.modules.releases.uattask.UATTask",
    # ── Projects & Tasks ───────────────────────────────────────────────────
    "Project":               "com.zoho.automater.selenium.modules.projects.project.Project",
    "Task":                  "com.zoho.automater.selenium.modules.tasks.task.Task",
    # ── Assets ─────────────────────────────────────────────────────────────
    "Asset":                 "com.zoho.automater.selenium.modules.assets.asset.Asset",
    "AssetTrigger":          "com.zoho.automater.selenium.modules.admin.automation.triggers.AssetTrigger",
    # ── Admin — Automation / Triggers ─────────────────────────────────────
    "ProblemTrigger":        "com.zoho.automater.selenium.modules.admin.automation.triggers.ProblemTrigger",
    "IncidentRequestTrigger": "com.zoho.automater.selenium.modules.admin.automation.triggers.IncidentRequestTrigger",
    "ChangeTrigger":         "com.zoho.automater.selenium.modules.admin.automation.triggers.ChangeTrigger",
    "ServiceRequestTrigger": "com.zoho.automater.selenium.modules.admin.automation.triggers.ServiceRequestTrigger",
    # ── Admin — Automation / Workflows ────────────────────────────────────
    "IncidentRequestWorkflow": "com.zoho.automater.selenium.modules.admin.automation.workflows.IncidentRequestWorkflow",
    # ── Admin — Customization / Additional Fields ──────────────────────────
    "ProjectUDF":            "com.zoho.automater.selenium.modules.admin.customization.additionalfields.ProjectUDF",}


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
        url: str,
        email_id: Optional[str] = None,
        portal_name: Optional[str] = None,
        admin_mail_id: Optional[str] = None,
        skip_compile: bool = False,
    ) -> RunResult:
        """
        Patch, compile (optional), and execute a single test method.

        Args:
            entity_class  : Simple class name, e.g. "Solution"
            method_name   : Method to run, e.g. "createAndShareApprovedPublicSolutionFromDV"
            url           : Target server URL, e.g. "http://sdpod-auto1:8080/"
            email_id      : Technician user email (overrides StandaloneDefault.EMAIL_ID)
            portal_name   : Portal name (overrides StandaloneDefault.PORTAL_NAME)
            admin_mail_id : Admin email (overrides StandaloneDefault.ADMIN_MAIL_ID)
            skip_compile  : If True, skip compilation (use existing bin/)
        """
        print(f"[RunnerAgent] Preparing to run: {entity_class}.{method_name}")
        print(f"[RunnerAgent] Target URL: {url}")

        # Stamp browser paths from env into app.properties before the JVM starts
        self._patch_app_properties()

        try:
            # 1. Backup StandaloneDefault.java only (AutomaterSeleniumMain is no longer patched —
            #    entity class and method name are passed as command-line args instead)
            default_backup = self._backup(self._standalone_default)

            try:
                # 2. Patch StandaloneDefault.java with the provided URL / credentials
                self._patch_standalone_default(url, email_id, portal_name, admin_mail_id)

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
                run_result = self._execute(entity_class, method_name)
                success = self._parse_success(run_result.stdout, run_result.stderr)
                report_path = self._find_latest_report(method_name)

                # ── HTML report override ─────────────────────────────────────
                # 1. If _parse_success returned False but the HTML report says
                #    PASS (cleanup NPE on no-display env), promote to True.
                # 2. If _parse_success returned True but the report directory is
                #    empty (no HTML written — test never ran), demote to False.
                if report_path:
                    html_file = Path(report_path) / "ScenarioReport.html"
                    if not success and html_file.exists():
                        content = html_file.read_text(encoding="utf-8", errors="ignore")
                        if 'data-result="FAIL"' not in content and 'data-result="PASS"' in content:
                            success = True
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
                # Restore StandaloneDefault.java to its original state
                self._restore(self._standalone_default, default_backup)

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
            url=config.get("url", ""),
            email_id=config.get("email_id"),
            portal_name=config.get("portal_name"),
            admin_mail_id=config.get("admin_mail_id"),
            skip_compile=config.get("skip_compile", False),
        )

        state["run_result"] = result.to_dict()
        state["messages"] = [result.summary()]
        print(result.summary())
        return state

    # ── Patching helpers ───────────────────────────────────────────────────

    def _patch_standalone_default(
        self,
        url: str,
        email_id: Optional[str],
        portal_name: Optional[str],
        admin_mail_id: Optional[str],
    ) -> None:
        """Replace SERVER_URL (and optionally EMAIL_ID / PORTAL_NAME) in StandaloneDefault.java."""
        content = self._standalone_default.read_text(encoding="utf-8")

        # Replace the active (uncommented) SERVER_URL line
        content = re.sub(
            r'^(\s*public static final String SERVER_URL\s*=\s*)"[^"]*"(;)',
            rf'\1"{url}"\2',
            content,
            flags=re.MULTILINE,
        )

        if email_id:
            content = re.sub(
                r'^(\s*protected static final String EMAIL_ID\s*=\s*)"[^"]*"(;)',
                rf'\1"{email_id}"\2',
                content,
                flags=re.MULTILINE,
            )

        if portal_name:
            content = re.sub(
                r'^(\s*(?:private|protected) static final String PORTAL_NAME\s*=\s*)"[^"]*"(;)',
                rf'\1"{portal_name}"\2',
                content,
                flags=re.MULTILINE,
            )

        if admin_mail_id:
            content = re.sub(
                r'^(\s*private static final String ADMIN_MAIL_ID\s*=\s*)"[^"]*"(;)',
                rf'\1"{admin_mail_id}"\2',
                content,
                flags=re.MULTILINE,
            )

        self._standalone_default.write_text(content, encoding="utf-8")
        print(f"[RunnerAgent] Patched StandaloneDefault.java → URL={url}")

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
        Always-on fast compile: recompile ONLY the two patched standalone
        files so the new URL / entity / method are baked into the bytecode.
        Takes ~1 second vs full project compile (~5 min).
        """
        classpath_parts = [str(self.bin_dir)]
        for jar in self.deps_dir.rglob("*.jar"):
            classpath_parts.append(str(jar))
        classpath = ":".join(classpath_parts)

        files = [
            str(self._standalone_default),
            # AutomaterSeleniumMain.java is no longer patched — entity/method passed as CLI args
        ]

        cmd = [
            "javac",
            "-encoding", "UTF-8",
            "-cp", classpath,
            "-d", str(self.bin_dir),
        ] + files

        print(f"[RunnerAgent] Compiling patched StandaloneDefault.java (fast)...")
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

    def _execute(self, entity_class: str, method_name: str) -> subprocess.CompletedProcess:
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
                # addFailureReport → <div class=" error message-detail ...">
                # This CSS class only appears on actual failure step elements,
                # not in the stylesheet selectors (those use .error without quotes).
                if 'class=" error message-detail' in html_content:
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
