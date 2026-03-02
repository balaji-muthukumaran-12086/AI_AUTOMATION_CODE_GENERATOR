"""
coder_tools.py
--------------
LangChain tool wrappers that give the CoderAgent the same file-system access
I (GitHub Copilot) have: read_file, grep_search, list_dir.

These are used by the ReAct CoderAgent when the LLM supports tool-calling
(OpenAI / Anthropic via OpenRouter). Ollama 7B falls back to static RAG.

All paths are validated against PROJECT_ROOT to prevent traversal outside
the active project.
"""

from __future__ import annotations

import fnmatch
import os
import re
from pathlib import Path
from typing import Optional

from langchain_core.tools import tool

from config.project_config import PROJECT_ROOT, BASE_DIR

# ── Safety boundary ─────────────────────────────────────────────────────────
# Tools are allowed to read anywhere inside the active project OR the
# AutomaterSeleniumFramework (shared framework code).
_ALLOWED_ROOTS = [
    Path(PROJECT_ROOT).resolve(),
    Path(BASE_DIR, "AutomaterSeleniumFramework").resolve(),
    Path(BASE_DIR, "config").resolve(),
]

_MAX_READ_LINES = 300   # cap single read to avoid blowing context window
_MAX_GREP_HITS  = 30    # cap grep results


def _resolve_safe(raw_path: str) -> Path | None:
    """
    Resolve a (possibly relative) path to an absolute Path.
    Returns None if the resolved path falls outside all allowed roots.
    Relative paths are resolved relative to PROJECT_ROOT/src so the agent
    can write short paths like:
      com/zoho/.../triggers/ProblemTrigger.java
    or absolute paths as-is.
    """
    p = Path(raw_path)
    if not p.is_absolute():
        # Try project src first
        candidate = Path(PROJECT_ROOT, "src", raw_path).resolve()
        if not candidate.exists():
            # Try resource dir
            candidate = Path(PROJECT_ROOT, "resources", raw_path).resolve()
        if not candidate.exists():
            # Bare relative from PROJECT_ROOT
            candidate = Path(PROJECT_ROOT, raw_path).resolve()
        if not candidate.exists():
            # framework src
            candidate = Path(BASE_DIR, "AutomaterSeleniumFramework", "src", raw_path).resolve()
        p = candidate
    else:
        p = p.resolve()

    for root in _ALLOWED_ROOTS:
        try:
            p.relative_to(root)
            return p
        except ValueError:
            continue
    return None  # outside all allowed roots


# ── Tool 1: read_file ────────────────────────────────────────────────────────

@tool
def read_file(file_path: str, start_line: int = 1, end_line: int = 100) -> str:
    """
    Read lines from a file in the project.

    Args:
        file_path: Relative path from project/src (e.g.
                   "com/zoho/automater/selenium/modules/admin/automation/triggers/ProblemTrigger.java")
                   or an absolute path within the project.
        start_line: First line to read (1-based, inclusive). Defaults to 1.
        end_line:   Last line to read (1-based, inclusive). Defaults to 100.
                    Capped at start_line + 300 to protect context window.

    Returns:
        The requested lines as a string, prefixed with line numbers.
        Returns an error message if the file is not found or path is unsafe.
    """
    resolved = _resolve_safe(file_path)
    if resolved is None:
        return f"[read_file] ERROR: path '{file_path}' is outside allowed project boundaries."
    if not resolved.exists():
        return f"[read_file] ERROR: file not found: {resolved}"
    if not resolved.is_file():
        return f"[read_file] ERROR: not a file: {resolved}"

    # Cap range
    start_line = max(1, start_line)
    end_line   = min(end_line, start_line + _MAX_READ_LINES - 1)

    try:
        lines = resolved.read_text(encoding="utf-8", errors="replace").splitlines()
    except Exception as exc:
        return f"[read_file] ERROR reading file: {exc}"

    total = len(lines)
    end_line = min(end_line, total)
    if start_line > total:
        return f"[read_file] File has only {total} lines; start_line={start_line} is out of range."

    result_lines = lines[start_line - 1 : end_line]
    numbered = "\n".join(f"{start_line + i:>5}: {ln}" for i, ln in enumerate(result_lines))
    return f"// {resolved}  (lines {start_line}–{end_line} of {total})\n{numbered}"


# ── Tool 2: grep_search ──────────────────────────────────────────────────────

@tool
def grep_search(
    query: str,
    file_pattern: str = "**/*.java",
    case_sensitive: bool = False,
    max_results: int = 20,
) -> str:
    """
    Search for a pattern across project source files.

    Args:
        query:          Plain-text or regex pattern to search for.
        file_pattern:   Glob pattern relative to project root, e.g. "**/*.java",
                        "**/*.json", "src/**/*.java". Defaults to "**/*.java".
        case_sensitive: Whether the match is case-sensitive. Defaults to False.
        max_results:    Maximum number of matching lines to return. Defaults to 20.

    Returns:
        Matching lines in "filepath:lineno: content" format, or a message if
        nothing was found.
    """
    max_results = min(max_results, _MAX_GREP_HITS)
    flags = 0 if case_sensitive else re.IGNORECASE

    try:
        pattern = re.compile(query, flags)
    except re.error as exc:
        # Treat as literal string if invalid regex
        pattern = re.compile(re.escape(query), flags)

    hits: list[str] = []
    search_root = Path(PROJECT_ROOT)

    for file_path in sorted(search_root.rglob(file_pattern)):
        if not file_path.is_file():
            continue
        # skip bin / build dirs
        parts = file_path.parts
        if any(p in parts for p in ("bin", "build", "__pycache__")):
            continue
        try:
            for lineno, line in enumerate(
                file_path.read_text(encoding="utf-8", errors="replace").splitlines(),
                start=1,
            ):
                if pattern.search(line):
                    rel = file_path.relative_to(search_root)
                    hits.append(f"{rel}:{lineno}: {line.rstrip()}")
                    if len(hits) >= max_results:
                        break
        except Exception:
            continue
        if len(hits) >= max_results:
            break

    if not hits:
        return f"[grep_search] No matches for '{query}' in {file_pattern}"
    header = f"[grep_search] {len(hits)} match(es) for '{query}' in {file_pattern}:\n"
    return header + "\n".join(hits)


# ── Tool 3: list_dir ─────────────────────────────────────────────────────────

@tool
def list_dir(dir_path: str = "") -> str:
    """
    List the contents of a directory inside the project.

    Args:
        dir_path: Relative path from project root (e.g. "src/com/zoho/automater/selenium/modules")
                  or absolute path. Leave empty to list project root.

    Returns:
        Directory listing with entries marked as [DIR] or [FILE], or an error
        message if the path is not found or unsafe.
    """
    if not dir_path:
        target = Path(PROJECT_ROOT).resolve()
    else:
        resolved = _resolve_safe(dir_path)
        if resolved is None:
            return f"[list_dir] ERROR: path '{dir_path}' is outside allowed project boundaries."
        target = resolved

    if not target.exists():
        return f"[list_dir] ERROR: path not found: {target}"
    if not target.is_dir():
        return f"[list_dir] ERROR: not a directory: {target}"

    entries = sorted(target.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    lines = [f"// {target}"]
    for entry in entries:
        tag = "[DIR] " if entry.is_dir() else "[FILE]"
        lines.append(f"  {tag} {entry.name}")
    return "\n".join(lines)


# ── Public tool list (imported by CoderAgent) ────────────────────────────────
CODER_TOOLS = [read_file, grep_search, list_dir]
