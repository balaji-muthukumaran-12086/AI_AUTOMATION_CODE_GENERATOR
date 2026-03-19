# CHANGELOG

All notable changes to the AI Automation Code Generator are documented here.
Most recent changes appear first. Agents should read the top ~30 lines to understand current state.

> **Format**: `[YYYY-MM-DD] CATEGORY: Brief description (files affected)`
> **Categories**: ADDED | CHANGED | FIXED | REMOVED | OPTIMIZATION | AGENT | CONFIG

---

## [2026-03-19] — Framework-FineTuning Branch Created

### ADDED
- `config/framework_file_index.yaml` — Chunked file index for token-efficient context loading. Maps every large file (framework_rules.md, framework_knowledge.md, API docs, copilot-instructions.md) to line-range chunks with topic descriptions and keywords. Agents read this ~120-line index instead of the full 2000+ line files.
- `.github/instructions/token-budget-rules.instructions.md` — Hard rules for session management, file reading budgets, edit batching, and compilation cycles. Auto-loaded for all files via `applyTo: "**"`.
- `CHANGELOG.md` (this file) — Change tracking for AI context continuity across sessions.
- `docs/templates/requirement_template.md` — Standardized template for documenting requirements before coding starts.
- `docs/templates/implementation_plan_template.md` — Phase-by-phase execution plan template with session break points.
- `config/skills_manifest.yaml` — Registry of all available tools, agents, skills, and their capabilities for quick lookup.
- `.github/agents/context-optimizer.agent.md` — Dedicated agent for optimizing token usage, chunking large files, and managing session context.

### OPTIMIZATION
- Established chunking system: all framework files > 300 lines now have indexed chunks in `framework_file_index.yaml`
- Session-per-phase rule: new chat sessions required for each distinct work phase
- Edit batching rule: multi_replace_string_in_file preferred over sequential edits
- Compile-once rule: fix all errors in batch before recompiling

### CONFIG
- Updated `.github/copilot-instructions.md` with token budget awareness section pointing to new instruction files
