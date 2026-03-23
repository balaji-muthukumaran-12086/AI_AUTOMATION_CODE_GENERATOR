# Implementation Plan — [Feature/Task Title]

> **Linked Requirement**: `docs/requirements/[requirement_doc].md`  
> **Created**: [YYYY-MM-DD]  
> **Author**: [Name]  
> **Status**: Planning | In Progress | Completed

---

## Principles

1. **One phase per chat session** — Never carry a huge context across phases
2. **Read once, reference from memory** — Use CHANGELOG.md + session notes
3. **Batch edits** — Use multi_replace_string_in_file for multiple changes
4. **Compile once per phase** — Fix all errors in batch before recompiling
5. **Checkpoint after each phase** — Update CHANGELOG.md before ending session

---

## Phase 0 — Pre-Analysis (Session 1)

**Goal**: Read existing code, understand current state, finalize plan.

| Step | Action | Files to read | Token budget |
|------|--------|--------------|-------------|
| 0.1 | Read CHANGELOG.md (top 30 lines) | CHANGELOG.md | ~200 |
| 0.2 | Read critical_rules_digest.md | config/critical_rules_digest.md | ~1,200 |
| 0.3 | Read relevant entity files | [list specific files + line ranges] | ~2,000 |
| 0.4 | Read existing utils | [ActionsUtil, APIUtil — grep methods first] | ~1,500 |
| 0.5 | Finalize this plan with updates | This file | ~500 |

**Session output**: Updated plan + session memory notes  
**Checkpoint**: Update CHANGELOG.md with "Phase 0 complete — plan finalized"

---

## Phase 1 — Data & Config (Session 2)

**Goal**: Create all test data entries and config changes.

| Step | Action | Files to modify | Edits |
|------|--------|----------------|-------|
| 1.1 | Add data entries to `*_data.json` | [file path] | [N entries] |
| 1.2 | Add AnnotationConstants entries | [file path] | [N constants] |
| 1.3 | Run `./generate_constants.sh` | — | Auto-generates DataConstants |
| 1.4 | Add new locators (if any) | [Locators.java] | [N locators] |
| 1.5 | Compile to verify | Terminal | 1 compile |

**Session output**: All data + config ready  
**Checkpoint**: Update CHANGELOG.md with data entries added

---

## Phase 2 — Utility Methods (Session 3)

**Goal**: Create any new ActionsUtil/APIUtil methods needed by test scenarios.

| Step | Action | Files to modify | Edits |
|------|--------|----------------|-------|
| 2.1 | Add new methods to ActionsUtil | [file path] | [N methods] |
| 2.2 | Add new methods to APIUtil | [file path] | [N methods] |
| 2.3 | Compile utils | Terminal | 1 compile |

**Session output**: All utility methods ready  
**Checkpoint**: Update CHANGELOG.md with util methods added

---

## Phase 3 — Test Scenarios (Session 4)

**Goal**: Generate test scenario code (annotations + implementations).

| Step | Action | Files to modify | Edits |
|------|--------|----------------|-------|
| 3.1 | Add @AutomaterScenario methods to Entity.java | [file path] | [N methods] |
| 3.2 | Add implementations to EntityBase.java | [file path] | [N methods] |
| 3.3 | Add preProcess groups (if new ones needed) | [file path] | [N groups] |
| 3.4 | Compile all modified files | Terminal | 1 compile |

**Session output**: All scenarios compiled  
**Checkpoint**: Update CHANGELOG.md with scenarios generated

---

## Phase 4 — Test Execution (Session 5)

**Goal**: Run tests, diagnose failures, fix.

| Step | Action | Notes |
|------|--------|-------|
| 4.1 | Run first scenario | Terminal + Playwright MCP |
| 4.2 | Fix any failures | Batch fixes → recompile once |
| 4.3 | Run remaining scenarios | One at a time or batch |
| 4.4 | Update tests_to_run.json | Record results |

**Session output**: All tests passing or documented failures  
**Checkpoint**: Update CHANGELOG.md with run results

---

## Rollback Plan

If a phase fails and cannot be recovered:
1. Check `git diff` for all changes made in this phase
2. `git stash` to save work
3. Document what went wrong in CHANGELOG.md
4. Start a new session with the diagnosis

---

## Completion Criteria

- [ ] All scenarios compile without errors
- [ ] All tests pass (or failures documented with root cause)
- [ ] CHANGELOG.md updated with final status
- [ ] Session memory cleaned up (remove temp notes)
