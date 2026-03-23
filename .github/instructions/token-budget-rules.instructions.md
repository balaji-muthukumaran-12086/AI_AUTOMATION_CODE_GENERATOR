---
applyTo: "**"
---

# Token Budget & Session Management — HARD RULES

> These rules prevent Copilot agent session rate limits and ensure efficient token usage.
> Every agent (human or AI) in this workspace MUST follow these rules.

---

## 1. Session Scoping — One Phase Per Chat

**RULE**: Start a **new chat session** for each distinct phase of work.

| Phase | Example tasks | New chat? |
|-------|--------------|-----------|
| Planning | Read CSV, produce test plan | YES |
| Generation (batch 1-5) | Generate code for 5 scenarios | YES |
| Generation (batch 6-10) | Generate code for next 5 | YES |
| Running tests | Execute, diagnose, fix | YES |
| Debugging a single failure | Inspect UI, fix locator | YES |

**WHY**: Conversation context accumulates ALL prior messages. A 50-message session carries
~100K tokens of history forward with EVERY new tool call. By session 80+, you hit the ceiling.

**FORBIDDEN**: Running planning + generation + execution + debugging in a single chat thread.

---

## 2. File Reading — Targeted Ranges Only

**RULE**: Never read a file > 300 lines in full. Use file indexes and targeted ranges.

### Before reading any large file:
1. Check `config/framework_file_index.yaml` for the chunk map
2. Identify the relevant chunk by keywords/topic
3. Read ONLY that chunk: `read_file(startLine=X, endLine=Y)`

### Priority order for context loading:
```
1. config/critical_rules_digest.md     (~150 lines — covers 80% of cases)
2. config/framework_file_index.yaml    (~120 lines — chunk map for targeted reads)
3. Specific chunk from the full file   (50-200 lines — only when digest isn't enough)
```

### Token cost reference:
| Action | ~Tokens consumed |
|--------|-----------------|
| Read 100 lines of code | ~800 |
| Read 500 lines of code | ~4,000 |
| Read 2000+ line file in full | ~16,000 |
| Read same 2000-line file twice | ~32,000 (WASTED) |

**FORBIDDEN**: Reading the same file more than once in a session.
After the first read, reference the information from memory — do not re-read.

---

## 3. Edit Batching — Combine, Don't Sequence

**RULE**: When making multiple edits to the same file or across files, batch them.

```
❌ WRONG (6 tool calls = 6x token overhead):
  edit file A line 10
  edit file A line 50
  edit file A line 100
  edit file B line 20
  edit file B line 80
  edit file C line 5

✅ CORRECT (2 tool calls):
  multi_replace_string_in_file([A:10, A:50, A:100, B:20, B:80, C:5])
  OR plan all edits, apply via multi-replace in 1-2 batches
```

**Target**: ≤ 3 edit tool calls per file per session.

---

## 4. Compilation & Error Checking — Minimize Iterations

**RULE**: Read the error output carefully. Fix ALL errors in one batch, then recompile ONCE.

```
❌ WRONG (5 compile cycles):
  compile → 3 errors → fix error 1 → compile → 2 errors → fix error 2 → compile → 1 error → fix → compile

✅ CORRECT (2 compile cycles):
  compile → 3 errors → fix all 3 in one batch → compile → 0 errors ✓
```

---

## 5. Context Carryover — Use CHANGELOG + Session Memory

**RULE**: Instead of re-reading files to understand "what changed", check:
1. `CHANGELOG.md` — tracks all modifications with dates and file paths
2. `/memories/session/` — session-scoped notes for current conversation

**Before starting any task**, check the CHANGELOG to understand recent state:
```bash
head -50 CHANGELOG.md   # Recent changes at top
```

---

## 6. Requirement Documents — Write Before Coding

**RULE**: For any task involving 3+ files or 5+ scenarios:
1. Create a requirement document FIRST (use `docs/templates/requirement_template.md`)
2. Get user confirmation on the plan
3. Create an implementation plan with phases (use `docs/templates/implementation_plan_template.md`)
4. Execute phase by phase, **one chat session per phase**

**WHY**: A clear requirement doc prevents mid-session pivots that burn tokens re-reading
files and undoing work. The implementation plan gives checkpoints for clean session breaks.

---

## 7. Skills Declaration — Know Your Tools

**RULE**: Before starting complex work, check `config/skills_manifest.yaml` to understand
which tools/skills are available. Don't reinvent what already exists.

---

## 8. Token Budget Targets

| Session type | Target tool calls | Max file reads | Max edits |
|-------------|-------------------|---------------|-----------|
| Simple fix (1 file) | ≤ 10 | ≤ 3 | ≤ 3 |
| Feature (3-5 files) | ≤ 30 | ≤ 10 | ≤ 15 |
| Batch generation (5 scenarios) | ≤ 50 | ≤ 15 | ≤ 25 |
| Test run + debug cycle | ≤ 40 | ≤ 10 | ≤ 10 |

If approaching the budget ceiling, **stop and summarize** what's done + what remains.
The user can continue in a fresh session using the CHANGELOG + session notes.

---

## 9. Anti-Patterns — What Burns Quota Fastest

| Anti-pattern | Token waste | Fix |
|-------------|------------|-----|
| Reading same large file repeatedly | 16K+ per read | Read once, reference from memory |
| Many small sequential edits | 2K overhead per call | Batch into multi-replace |
| Long conversation with all prior context | Grows ~2K per exchange | New chat per phase |
| Compiling after every single edit | 4K+ per compile | Fix all errors, compile once |
| Full file read when only 20 lines needed | 15K wasted | Use framework_file_index.yaml chunks |
| Not using existing digest files | 16K vs 1.5K | Read critical_rules_digest.md first |
