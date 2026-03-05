#!/usr/bin/env python3
"""PostToolUse hook: Remind to compile after editing Java files."""
import json
import sys

try:
    event = json.load(sys.stdin)
    tool_name = event.get("toolName", "")
    file_path = event.get("toolResult", {}).get("filePath", "")
    
    if tool_name in ("replace_string_in_file", "create_file", "multi_replace_string_in_file"):
        if file_path.endswith(".java"):
            print(json.dumps({
                "systemMessage": (
                    "REMINDER: You edited a .java file. "
                    "Run targeted compilation before testing. "
                    "Full project compile is BROKEN — only compile changed files."
                )
            }))
except Exception:
    pass
