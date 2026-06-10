"""PostToolUse hook: run backend tests after edits to server/*.py.

Reads the hook event JSON from stdin. If the edited file is a Python file
under server/, runs the backend test suite. Exit 2 feeds failures back to
Claude; exit 0 stays silent.
"""
import json
import os
import subprocess
import sys


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0
    file_path = (event.get("tool_input") or {}).get("file_path", "")
    if not file_path or not file_path.endswith(".py"):
        return 0
    server_dir = os.path.abspath("server")
    edited = os.path.abspath(file_path)
    if not edited.startswith(server_dir + os.sep):
        return 0
    result = subprocess.run(
        ["uv", "run", "--project", "server", "pytest", "tests/backend/", "-q"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write("Backend tests failed after this edit:\n")
        sys.stderr.write(result.stdout[-2500:])
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
