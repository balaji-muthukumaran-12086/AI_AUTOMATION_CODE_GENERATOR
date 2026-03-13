---
# VS Code 1.111: Agent-scoped hook (Preview)
# Runs AFTER the test-debugger agent completes a response.
# Ensures cleanup and recompilation after fixes.
event: postSend
agents: [test-debugger]
---

## Post-Debug Cleanup

After completing a debug session:

1. **Cleanup test data** — Delete ALL entities created via `sdpAPICall()` during Playwright debugging:
   ```javascript
   () => sdpAPICall('<module>/<id>', 'del').responseJSON
   ```
2. **Recompile fixed files** — If any `.java` file was modified, run targeted compilation
3. **Verify fix** — If a locator or logic was fixed, confirm the fix by running the test:
   ```bash
   .venv/bin/python run_test.py 2>&1
   ```
4. **Report** — Summarize: what failed, root cause, what was fixed, verification result

Never close a debug session without cleaning up created test data.
