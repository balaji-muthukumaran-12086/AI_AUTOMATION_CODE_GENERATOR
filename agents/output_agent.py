"""
output_agent.py
---------------
Output Agent: Final step in the pipeline.

Responsibilities:
  1. Takes approved generated_code from ReviewerAgent
  2. Parses the LLM's TWO-PIECE output format:
       // ===== ADD TO: IncidentRequest.java =====
       <wrapper methods>
       // ===== ADD TO: RequestCommonBase.java =====
       <implementation methods>
  3. Writes one snippet file per target class into generated/<timestamp>_<module>/
  4. Resolves the full target file path from AutomaterSelenium/src/
  5. Writes a plain-English WHAT_TO_DO.txt so the user knows exactly where to paste
  6. Reports paths + instructions back into state for terminal display

Copy-paste workflow:
  → generated/20260225_142301_requests_request/
       1_ADD_TO_IncidentRequest.java       ← paste these methods into IncidentRequest.java
       2_ADD_TO_RequestCommonBase.java     ← paste these methods into RequestCommonBase.java
       3_ADD_TO_RequestDataConstants.java  ← paste these constants into RequestDataConstants.java
       WHAT_TO_DO.txt                      ← exact file paths + paste instructions
"""

import re
import json
from pathlib import Path
from datetime import datetime

from agents.state import AgentState


class OutputAgent:

    def __init__(self, base_dir: str = None):
        self.base = Path(base_dir) if base_dir else Path(__file__).resolve().parents[1]
        self.output_root = (
            self.base / 'AutomaterSelenium' / 'src' /
            'com' / 'zoho' / 'automater' / 'selenium' / 'modules'
        )
        self.generated_dir = self.base / 'generated'
        self.generated_dir.mkdir(parents=True, exist_ok=True)

    # ── TWO-PIECE PARSER ────────────────────────────────────────────────────

    def _parse_two_piece(self, raw_code: str) -> list[dict]:
        """
        Parse LLM output with // ===== ADD TO: FileName.java ===== markers
        into a list of {target_file, code} dicts.

        Handles variations:
          // ===== ADD TO: Solution.java =====
          // ----- ADD TO: SolutionBase.java -----
          // === ADD TO: RequestDataConstants.java
          // ADD TO: RequestFields.java
        """
        pattern = r'//\s*[=\-]{0,10}\s*ADD TO:\s*([^\n]+?\.java)\s*[=\-]*'
        parts = re.split(pattern, raw_code, flags=re.IGNORECASE)

        pieces = []
        if len(parts) >= 3:
            # parts = [pre_text, File1.java, code1, File2.java, code2, ...]
            for i in range(1, len(parts) - 1, 2):
                target = parts[i].strip()
                code = parts[i + 1].strip() if i + 1 < len(parts) else ''
                if code:
                    pieces.append({'target_file': target, 'code': code})

        if not pieces:
            # LLM didn't use markers — treat whole output as single snippet
            stripped = raw_code.strip()
            if stripped:
                pieces.append({'target_file': 'GeneratedCode.java', 'code': stripped})

        return pieces

    # ── TARGET FILE RESOLVER ────────────────────────────────────────────────

    def _resolve_target_path(self, filename: str) -> Path | None:
        """
        Find the full path of filename inside AutomaterSelenium/src/.
        Returns None if not found (new file to be created).
        """
        if not self.output_root.exists():
            return None
        matches = list(self.output_root.glob(f'**/{filename}'))
        return matches[0] if matches else None

    # ── INSTRUCTIONS FILE ───────────────────────────────────────────────────

    def _build_instructions(
        self,
        run_dir: Path,
        resolved: list[tuple],
        feature_description: str,
        module_path: str,
        scenario_count: int,
    ) -> list[str]:
        """
        Build WHAT_TO_DO.txt content and return terminal-printable lines.
        resolved = list of (snippet_path, target_path_or_None)
        """
        ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sep = '═' * 66

        lines = [
            sep,
            '  GENERATED TEST CODE — COPY-PASTE INSTRUCTIONS',
            sep,
            f'  Feature  : {feature_description[:80]}',
            f'  Entity   : {module_path}',
            f'  Generated: {ts}',
            f'  Scenarios: {scenario_count} new test case(s)',
            '',
            '  HOW TO USE:',
            '  ──────────────────────────────────────────────────────────────',
        ]

        for idx, (snippet_path, target_path) in enumerate(resolved, 1):
            snippet_name = snippet_path.name
            if target_path and target_path.exists():
                rel = target_path.relative_to(self.base)
                lines.append(f'  [{idx}] Paste code from:')
                lines.append(f'        {snippet_name}')
                lines.append(f'      Into (before the final `}}` of the class):')
                lines.append(f'        {rel}')
            else:
                target_name = snippet_name.replace(f'{idx}_ADD_TO_', '')
                lines.append(f'  [{idx}] Paste code from:')
                lines.append(f'        {snippet_name}')
                lines.append(f'      Target file not found in repo — place in the matching .java file:')
                lines.append(f'        AutomaterSelenium/src/.../{target_name}')
            lines.append('')

        lines += [
            '  NEXT STEPS AFTER PASTING:',
            '  ──────────────────────────────────────────────────────────────',
            '  1. Review each pasted method (verify IDs are unique)',
            '  2. Build the project:  ant clean build  (or IDE rebuild)',
            '  3. Run using the @AutomaterScenario id from the generated code',
            sep,
        ]

        what_to_do = run_dir / 'WHAT_TO_DO.txt'
        what_to_do.write_text('\n'.join(lines), encoding='utf-8')

        return lines

    # ── MAIN RUN ────────────────────────────────────────────────────────────

    def run(self, state: AgentState) -> AgentState:
        """LangGraph node function."""
        generated = state.get('generated_code', [])
        review_results = {r['module_path']: r for r in state.get('review_results', [])}
        feature_description = state.get('feature_description', 'Unnamed feature')

        state['messages'] = state.get('messages', []) + [
            "[OutputAgent] Parsing LLM output and writing snippet files..."
        ]

        all_output_paths: list[str] = []
        all_instructions: list[str] = []
        last_run_dir: str = ''
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')

        for gen in generated:
            module_path = gen.get('module_path', '')
            raw_code = gen.get('code', '')

            if gen.get('status') == 'error' or not raw_code.strip():
                state['messages'] = state.get('messages', []) + [
                    f"[OutputAgent] Skipped {module_path} — no code (status={gen.get('status')})"
                ]
                continue

            review = review_results.get(module_path, {})
            if not review.get('approved', True):
                state['messages'] = state.get('messages', []) + [
                    f"[OutputAgent] Skipped {module_path} — reviewer rejected"
                ]
                continue

            # ── Create run directory ────────────────────────────────────────
            safe_module = module_path.replace('/', '_').strip('_')
            run_dir = self.generated_dir / f"{ts}_{safe_module}"
            run_dir.mkdir(parents=True, exist_ok=True)
            last_run_dir = str(run_dir)

            # ── Parse the two-piece output ──────────────────────────────────
            pieces = self._parse_two_piece(raw_code)

            # ── Write each snippet and resolve target paths ─────────────────
            resolved: list[tuple] = []
            for idx, piece in enumerate(pieces, 1):
                target_file = piece['target_file']
                snippet_name = f"{idx}_ADD_TO_{target_file}"
                snippet_path = run_dir / snippet_name
                snippet_path.write_text(piece['code'], encoding='utf-8')

                target_path = self._resolve_target_path(target_file)
                resolved.append((snippet_path, target_path))
                all_output_paths.append(str(snippet_path))

            # ── Write WHAT_TO_DO.txt ────────────────────────────────────────
            scenario_count = len(gen.get('scenarios', []))
            instructions = self._build_instructions(
                run_dir=run_dir,
                resolved=resolved,
                feature_description=feature_description,
                module_path=module_path,
                scenario_count=scenario_count,
            )
            instructions_path = str(run_dir / 'WHAT_TO_DO.txt')
            all_output_paths.append(instructions_path)
            all_instructions = instructions   # shown in terminal for last module

            state['messages'] = state.get('messages', []) + [
                f"[OutputAgent] ✅ {len(pieces)} snippet(s) for [{module_path}] → {run_dir.name}/"
            ]

        # ── Summary JSON ────────────────────────────────────────────────────
        if all_output_paths:
            summary_path = self.generated_dir / f"summary_{ts}.json"
            with open(summary_path, 'w') as f:
                json.dump({
                    'timestamp': ts,
                    'feature': feature_description,
                    'generated_files': all_output_paths,
                    'coverage_gaps': state.get('coverage_gaps', []),
                    'duplicate_warnings': state.get('duplicate_warnings', []),
                }, f, indent=2)

        state['final_output_paths'] = all_output_paths
        state['generation_instructions'] = all_instructions
        state['generated_dir'] = last_run_dir
        state['messages'] = state.get('messages', []) + [
            f"[OutputAgent] ✅ Done — {len(all_output_paths)} file(s) in {self.generated_dir}",
        ]
        return state
