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
from config.project_config import PROJECT_NAME, DEPS_DIR as _DEFAULT_DEPS_DIR


# ── Constants ──────────────────────────────────────────────────────────────

STANDALONE_DEFAULT_PATH = (
    f"{PROJECT_NAME}/src/com/zoho/automater/selenium/standalone/StandaloneDefault.java"
)
MAIN_CLASS_PATH = (
    f"{PROJECT_NAME}/src/com/zoho/automater/selenium/standalone/AutomaterSeleniumMain.java"
)

# Known entity class → fully-qualified import mapping
ENTITY_IMPORT_MAP = {
    "Solution":       "com.zoho.automater.selenium.modules.solutions.solution.Solution",
    "Asset":          "com.zoho.automater.selenium.modules.assets.asset.Asset",
    "Request":        "com.zoho.automater.selenium.modules.requests.request.Request",
    "Problem":        "com.zoho.automater.selenium.modules.problems.problem.Problem",
    "Change":         "com.zoho.automater.selenium.modules.changes.change.Change",
    "Release":        "com.zoho.automater.selenium.modules.releases.release.Release",
    "Project":        "com.zoho.automater.selenium.modules.projects.project.Project",
    "Task":           "com.zoho.automater.selenium.modules.tasks.task.Task",
    "CabEvaluationTask": "com.zoho.automater.selenium.modules.changes.cabevaluationtask.CabEvaluationTask",
    "UATTask":        "com.zoho.automater.selenium.modules.releases.uattask.UATTask",
}


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
                # The framework's LocalSetupManager.cleanup() can throw a
                # NullPointerException when trying to open the report in a
                # browser (no desktop env). This causes _parse_success() to
                # return False even when the test actually passed.  Correct it
                # by checking the generated HTML report directly.
                if not success and report_path:
                    html_file = Path(report_path) / "ScenarioReport.html"
                    if html_file.exists():
                        content = html_file.read_text(encoding="utf-8", errors="ignore")
                        if 'data-result="FAIL"' not in content and 'data-result="PASS"' in content:
                            success = True

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

        stdout_lines = []
        stderr_lines = []

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=str(self.automater_root),
            start_new_session=True,   # detach from terminal process group so Ctrl+C doesn't kill the Java subprocess
        )

        # Stream stdout and stderr simultaneously
        import threading

        def stream(pipe, lines, label):
            for line in iter(pipe.readline, ""):
                line = line.rstrip()
                lines.append(line)
                print(f"  [{label}] {line}")
            pipe.close()

        t_out = threading.Thread(target=stream, args=(process.stdout, stdout_lines, "OUT"))
        t_err = threading.Thread(target=stream, args=(process.stderr, stderr_lines, "ERR"))
        t_out.start()
        t_err.start()

        try:
            process.wait(timeout=300)
        except subprocess.TimeoutExpired:
            process.kill()
            print("[RunnerAgent] ⚠️  Test timed out after 300 seconds")

        t_out.join()
        t_err.join()

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

        # Default: no explicit failure detected → pass
        return True

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
