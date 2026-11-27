#!/usr/bin/env python3
"""PreToolUse hook for Edit, Write and MultiEdit.

Blocks two kinds of edits:
- any .env file except .env.example (secrets stay out of Claude's hands)
- a migration in supabase/migrations/ that already exists on main (applied migrations are immutable)

Exit code 2 blocks the tool call; Claude Code shows stderr to Claude as the reason.
Exit code 0 lets the call through. Standard library only, so it runs before any dependency is installed.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

MIGRATIONS = ("supabase", "migrations")


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    raw_path = (data.get("tool_input") or {}).get("file_path")
    if not raw_path:
        return 0

    path = Path(raw_path.replace("\\", "/"))
    name = path.name

    if name.startswith(".env") and name != ".env.example":
        print(
            f"Blocked: {name} holds secrets and is off limits. "
            "Add new variables to .env.example and ask the user to set the real value.",
            file=sys.stderr,
        )
        return 2

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".").resolve()
    try:
        rel = path.resolve().relative_to(project)
    except ValueError:
        return 0

    if rel.parts[: len(MIGRATIONS)] == MIGRATIONS and on_main(project, rel):
        print(
            f"Blocked: {rel.as_posix()} is already on main, so it may have been applied. "
            "Never edit an applied migration; create a new migration file instead.",
            file=sys.stderr,
        )
        return 2

    return 0


def on_main(project: Path, rel: Path) -> bool:
    """True when the file exists on origin/main (or local main if there is no remote)."""
    for ref in ("origin/main", "main"):
        result = subprocess.run(
            ["git", "-C", str(project), "cat-file", "-e", f"{ref}:{rel.as_posix()}"],
            capture_output=True,
        )
        if result.returncode == 0:
            return True
    return False


if __name__ == "__main__":
    sys.exit(main())
