---
# VS Code 1.111: Agent Troubleshooting — Debug Event Snapshots
# This hook captures debug context on EVERY agent interaction,
# making it easy to diagnose why an agent made a specific decision.
event: postSend
agents: [test-generator, test-runner, test-debugger, setup-project]
---

## Troubleshooting — Debug Event Capture

After each agent response, capture diagnostic context for troubleshooting:

1. **Log the action summary** — What tool calls were made, what files were read/edited, what terminal commands were run
2. **Capture decision points** — If the agent chose between alternatives (e.g., reuse existing preProcess group vs create new), log the reasoning
3. **Record failures** — Any tool call failures, compilation errors, or test failures should be noted with timestamps

This context enables post-session review of agent behavior through VS Code's debug event snapshots panel (`Developer: Show Agent Debug Events`).

### How to use debug snapshots:
- Open Command Palette -> `Developer: Show Agent Debug Events`
- Review the timeline of tool calls and decisions made by each agent
- Click on any event to see the full context (input/output of tool calls)
- Use filters to show events from a specific agent only
