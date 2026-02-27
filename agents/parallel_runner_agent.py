"""
parallel_runner_agent.py
------------------------
Parallel Runner Agent: Executes multiple Selenium test cases concurrently
against the configured SDP instance, then hands results to LearningAgent.

Architecture
────────────
  1. Loads tests from tests_to_run.json (or state['batch_run_configs'])
  2. Resolves $(SDP_URL), $(SDP_PORTAL), $(SDP_ADMIN_EMAIL) placeholders
  3. Patches StandaloneDefault.java ONCE with shared URL / credentials
  4. Compiles only the patched file (fast — ~1 s)
  5. Launches N JVMs concurrently (N = PARALLEL_WORKERS; each JVM gets its
     own entity_class + method_name as CLI args — no per-test source patch)
  6. Collects RunResult objects, restores StandaloneDefault.java
  7. Stores results in state['batch_run_results']

Why parallel JVMs are safe here
────────────────────────────────
  • entity_class and method_name are CLI args to AutomaterSeleniumMain —
    they are NOT baked into compiled bytecode.
  • Each JVM opens its own Firefox window and operates its own SDP session.
  • The only shared on-disk resource is bin/ (read-only during JVM execution).
  • Test data uses $(unique_string) (millisecond timestamp) for names, so
    concurrent creates do not collide.

Pipeline position:
  (standalone)  tests_to_run.json → ParallelRunnerAgent → LearningAgent
  (in pipeline) ... → output → ParallelRunnerAgent → LearningAgent → ...
"""

import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path
from typing import Optional

from agents.state import AgentState
from agents.runner_agent import RunnerAgent, RunResult, ENTITY_IMPORT_MAP
from config.project_config import (
    BASE_DIR,
    DEPS_DIR,
    PROJECT_NAME,
    PARALLEL_WORKERS,
    TESTS_TO_RUN_PATH,
    SDP_URL,
    SDP_PORTAL,
    SDP_ADMIN_EMAIL,
    SDP_ADMIN_PASS,
)


# ── Placeholder resolution ─────────────────────────────────────────────────

_PLACEHOLDER_MAP = {
    "$(SDP_URL)":          SDP_URL,
    "$(SDP_PORTAL)":       SDP_PORTAL,
    "$(SDP_ADMIN_EMAIL)":  SDP_ADMIN_EMAIL,
    "$(SDP_ADMIN_PASS)":   SDP_ADMIN_PASS,
}


def _resolve(value: str) -> str:
    """Replace $(KEY) tokens with live config values."""
    if not isinstance(value, str):
        return value
    for token, real in _PLACEHOLDER_MAP.items():
        value = value.replace(token, real)
    return value


def _resolve_config(cfg: dict) -> dict:
    """Return a copy of a run-config dict with all placeholders resolved."""
    return {k: _resolve(v) for k, v in cfg.items()}


# ── Batch result container ─────────────────────────────────────────────────

class BatchRunResult:
    """Summary of a full parallel batch execution."""

    def __init__(self, results: list[RunResult], duration_s: float = 0.0):
        self.results    = results
        self.duration_s = duration_s
        self.passed     = [r for r in results if r.success]
        self.failed     = [r for r in results if not r.success]
        self.timestamp  = datetime.now().isoformat()

    @property
    def pass_rate(self) -> float:
        return len(self.passed) / len(self.results) if self.results else 0.0

    def summary(self) -> str:
        lines = [
            f"[ParallelRunner] Batch complete — {len(self.passed)}/{len(self.results)} passed "
            f"({self.pass_rate:.0%}) in {self.duration_s:.1f}s",
        ]
        for r in self.results:
            icon = "✅" if r.success else "❌"
            lines.append(f"  {icon} {r.entity_class}.{r.method_name}")
        return "\n".join(lines)

    def to_list(self) -> list[dict]:
        return [r.to_dict() for r in self.results]


# ── Parallel Runner Agent ──────────────────────────────────────────────────

class ParallelRunnerAgent:
    """
    Runs a batch of Selenium tests concurrently and collects results.

    Core innovation: patch + compile happen ONCE for the whole batch (all
    tests share the same URL/credentials); then N JVM processes launch
    simultaneously.  The compile lock ensures no two threads race on the
    shared StandaloneDefault.java file.
    """

    def __init__(
        self,
        base_dir: str = None,
        deps_dir: str = None,
        workers: int = None,
    ):
        self.base     = Path(base_dir) if base_dir else Path(BASE_DIR)
        self.deps_dir = Path(deps_dir) if deps_dir else Path(DEPS_DIR)
        self.workers  = workers if workers is not None else PARALLEL_WORKERS

        self._runner = RunnerAgent(
            base_dir=str(self.base),
            deps_dir=str(self.deps_dir),
            pre_compiled_bin_dir=str(self.base / PROJECT_NAME / "bin"),
        )

        # Lock protects StandaloneDefault.java patch + compile from concurrent access.
        # During the execution phase the lock is released so JVMs run in parallel.
        self._patch_lock = threading.Lock()

    # ── LangGraph node entry point ────────────────────────────────────────

    def run(self, state: AgentState) -> AgentState:
        """
        LangGraph node.  Reads batch_run_configs (or loads tests_to_run.json).
        Writes batch_run_results.
        """
        configs = state.get("batch_run_configs") or self._load_tests_from_file()
        if not configs:
            state["messages"] = ["[ParallelRunner] No tests to run — batch_run_configs is empty."]
            state["batch_run_results"] = []
            return state

        print(f"[ParallelRunner] Starting batch of {len(configs)} test(s) "
              f"with parallelism={self.workers}...")

        batch = self.run_batch(configs)
        print(batch.summary())

        state["batch_run_results"] = batch.to_list()
        state["messages"] = [batch.summary()]
        return state

    # ── Main public API ───────────────────────────────────────────────────

    def run_batch(self, configs: list[dict]) -> BatchRunResult:
        """
        Execute all configs in parallel.

        Flow per test config:
          resolved_cfg → _execute_one(entity_class, method_name) → RunResult

        The shared patch+compile step is done once before launching JVMs.
        """
        import time
        start = time.time()

        # Resolve placeholders in all configs
        resolved = [_resolve_config(c) for c in configs]

        # Use the first config's credentials to patch StandaloneDefault.java
        ref = resolved[0]
        url          = ref.get("url",          SDP_URL)
        email_id     = ref.get("email_id",     SDP_ADMIN_EMAIL)
        portal_name  = ref.get("portal_name",  SDP_PORTAL)
        admin_mail_id= ref.get("admin_mail_id",SDP_ADMIN_EMAIL)

        # ── Phase 1: patch + compile (serialised — touches shared file) ──
        with self._patch_lock:
            backup = self._runner._backup(self._runner._standalone_default)
            try:
                self._runner._patch_standalone_default(url, email_id, portal_name, admin_mail_id)
                result = self._runner._compile_patched_files()
                if result.returncode != 0:
                    self._runner._restore(self._runner._standalone_default, backup)
                    return BatchRunResult(
                        [RunResult(
                            success=False,
                            method_name=c.get("method_name", "?"),
                            entity_class=c.get("entity_class", "?"),
                            url=url,
                            error=f"Batch compile failed:\n{result.stderr[:1000]}",
                        ) for c in configs],
                        duration_s=time.time() - start,
                    )
            except Exception as exc:
                self._runner._restore(self._runner._standalone_default, backup)
                return BatchRunResult(
                    [RunResult(
                        success=False,
                        method_name=c.get("method_name", "?"),
                        entity_class=c.get("entity_class", "?"),
                        url=url,
                        error=f"Batch patch error: {exc}",
                    ) for c in configs],
                    duration_s=time.time() - start,
                )

        # ── Phase 2: parallel JVM execution (lock released — bin/ is read-only) ──
        results: list[RunResult] = []
        try:
            with ThreadPoolExecutor(max_workers=self.workers) as pool:
                future_to_cfg = {
                    pool.submit(self._execute_one, cfg): cfg
                    for cfg in resolved
                }
                for future in as_completed(future_to_cfg):
                    cfg = future_to_cfg[future]
                    try:
                        result = future.result()
                    except Exception as exc:
                        result = RunResult(
                            success=False,
                            method_name=cfg.get("method_name", "?"),
                            entity_class=cfg.get("entity_class", "?"),
                            url=cfg.get("url", url),
                            error=f"Thread error: {exc}",
                        )
                    results.append(result)
        finally:
            # ── Phase 3: always restore StandaloneDefault.java ───────────
            with self._patch_lock:
                self._runner._restore(self._runner._standalone_default, backup)

        return BatchRunResult(results, duration_s=time.time() - start)

    # ── Per-test JVM execution ────────────────────────────────────────────

    def _execute_one(self, cfg: dict) -> RunResult:
        """
        Execute a single test by calling RunnerAgent._execute() directly.
        Does NOT touch StandaloneDefault.java (already compiled by batch setup).
        """
        entity_class = cfg.get("entity_class", "")
        method_name  = cfg.get("method_name", "")
        url          = cfg.get("url", SDP_URL)

        print(f"[ParallelRunner] ▶ {entity_class}.{method_name}")
        try:
            raw = self._runner._execute(entity_class, method_name)
            success = self._runner._parse_success(raw.stdout, raw.stderr)
            report_path = self._runner._find_latest_report(method_name)

            # HTML report override (same logic as RunnerAgent.run_test)
            if not success and report_path:
                from pathlib import Path as _Path
                html_file = _Path(report_path) / "ScenarioReport.html"
                if html_file.exists():
                    content = html_file.read_text(encoding="utf-8", errors="ignore")
                    if 'data-result="FAIL"' not in content and 'data-result="PASS"' in content:
                        success = True

            return RunResult(
                success=success,
                method_name=method_name,
                entity_class=entity_class,
                url=url,
                stdout=raw.stdout,
                stderr=raw.stderr,
                report_path=report_path,
                error="" if success else self._runner._extract_error(raw.stdout, raw.stderr),
            )
        except Exception as exc:
            return RunResult(
                success=False,
                method_name=method_name,
                entity_class=entity_class,
                url=url,
                error=str(exc),
            )

    # ── File helpers ──────────────────────────────────────────────────────

    def _load_tests_from_file(self, path: str = None) -> list[dict]:
        """Load and return the 'tests' array from tests_to_run.json."""
        fpath = Path(path or TESTS_TO_RUN_PATH)
        if not fpath.exists():
            print(f"[ParallelRunner] ⚠️  tests_to_run.json not found at {fpath}")
            return []
        data = json.loads(fpath.read_text(encoding="utf-8"))
        tests = data.get("tests", [])
        # Strip comment keys (keys starting with _)
        return [{k: v for k, v in t.items() if not k.startswith("_")} for t in tests]
