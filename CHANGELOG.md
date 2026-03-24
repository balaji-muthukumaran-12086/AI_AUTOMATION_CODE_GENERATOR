# CHANGELOG

All notable changes to the AI Automation Code Generator are documented here.
Most recent changes appear first. Agents should read the top ~30 lines to understand current state.

> **Format**: `[YYYY-MM-DD] CATEGORY: Brief description (files affected)`
> **Categories**: ADDED | CHANGED | FIXED | REMOVED | OPTIMIZATION | AGENT | CONFIG

---

## [2025-06-27] ADDED: Batch 1 — 30 Linking Change test scenarios generated + compiled (SDPLIVE_LINK_CHANGE_TEST)

**Infrastructure (from previous session):**
- ChangeLocators.java: LinkingChange interface (~30 locators for associations page, popup, pagination, etc.)
- ChangeConstants.java: LinkingChange inner class (constants for labels, columns, badge text)
- ChangeAnnotationConstants.java: 5 new Group constants + 5 new Data constants for linking
- ChangeAPIUtil.java: 6 new methods (createChangeForLinking, linkParentChange, linkChildChange, unlinkParentChange, unlinkChildChange, createAndStoreChangeForLinking)
- ChangeActionsUtil.java: 7 new methods (navigateToChangeAssociationsTab, openAttachDropdown, openAttachPopup, associateParentChangeViaUI, associateChildChangeViaUI, detachAndConfirm, searchInAssociationPopup)
- Change.java: 5 new preProcess groups (createChangeForLinking, createMultipleChangeForLinking, createAndLinkParentChange, createAndLinkChildChanges, createClosedChangeForLinking)
- change_data.json: 5 new data entries (link_parent/child, api_create_change x3)

**Test Scenarios (this session):**
- DetailsView.java: 30 new @AutomaterScenario methods added
  - Associations Page (15): SDPOD_LNKCHG_UI_001-010e (page load, attach dropdown, empty state, columns, pagination, detach, refresh, back, multi-tab, external link, section label, dropdown hide, tab reset, breadcrumbs, tooltip)
  - Parent Popup (15): SDPOD_LNKCHG_UI_011-023d (popup open, filter, radio select, associate success, comments, popup pagination, search, cancel, close, ESC, modal, exclusion, closed change, validation, self-link, view toggle)
- Change.java: Fixed group references (string literals instead of ChangeAnnotationConstants package references)
- Compilation: **0 errors** ✓

**Remaining:** Batches 2-7 (172 scenarios) — Child Popup, Detach, RHS, List View, Constraints, Closure, History, RBAC, Lookup, Migration, Regression, etc.

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
