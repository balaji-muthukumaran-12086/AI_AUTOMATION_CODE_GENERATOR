# Agent Routing Guide

> Pick the right agent for your task. Using the wrong agent wastes time and token budget.

## Quick Decision Flow

```
What do you need?
│
├── Generate new test cases from CSV/description
│   └── @test-generator  (batch or single)
│
├── Run a test and auto-fix failures
│   └── @test-runner  (single or batch)
│
├── Debug a specific test failure
│   └── @test-debugger  (locator issues, NPEs, report analysis)
│
├── Explore SDP product UI before writing tests
│   └── @product-discovery  (discover DOM, API endpoints, edge cases)
│
├── Clone repo / configure project / set owner
│   └── @setup-project
│
├── Optimize token usage / chunk files / plan sessions
│   └── @context-optimizer
│
└── Search codebase / read files / answer questions
    └── @Explore  (fast read-only, safe for subagent)
```

## Agent Capabilities Matrix

| Agent | Generates Code | Runs Browser | Modifies Files | Safe as Subagent |
|-------|---------------|-------------|---------------|-----------------|
| test-generator | YES | NO | YES | YES |
| test-runner | YES (fixes) | YES (Playwright) | YES | NO — needs MCP |
| test-debugger | YES (fixes) | YES (Playwright) | YES | NO — needs MCP |
| product-discovery | NO | YES (Playwright) | NO | NO — needs MCP |
| setup-project | NO | NO | YES (config) | YES |
| context-optimizer | NO | NO | YES (memory) | YES |
| Explore | NO | NO | NO (read-only) | YES |

## Common Workflows

### "Generate all tests from a CSV"
```
@test-generator batch all
```

### "Generate and then run tests"
```
@test-generator batch all    ← Session 1: generate code
@test-runner batch all       ← Session 2: run + auto-fix
```

### "Fix a failing test"
```
@test-debugger SDPOD_AUTO_CH_LV_001 fails with NoSuchElementException on association tab
```

### "I don't know the UI structure for this feature"
```
@product-discovery changes/associations
```
Then use the output Feature Knowledge Doc as input to `@test-generator`.

### "Set up a new team member"
```
@setup-project
```

## Rules
- **Never run test-runner or test-debugger as a subagent** — they need Playwright MCP which is session-scoped
- **One phase per chat session** — don't generate + run + debug in the same session
- **Check CHANGELOG.md** before starting any session to understand recent state
