#!/usr/bin/env python3
"""Stop hook: before Claude ends a turn with uncommitted changes, run `make check-fast`.

If the checks fail, exit 2: Claude Code keeps the turn going and shows Claude the failure.
It never blocks twice in a row (`stop_hook_active`), so a check Claude can't fix
can't trap the session; Claude then reports the failure instead.

Skips quietly when nothing changed or when the Makefile has no check-fast target yet.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

TARGET = "check-fast"
TIMEOUT_S = 170
TAIL_LINES = 60


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        data = {}

    if data.get("stop_hook_active"):
        return 0

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".")

    status = subprocess.run(
        ["git", "status", "--porcelain"], cwd=project, capture_output=True, text=True
    )
    if status.returncode != 0 or not status.stdout.strip():
        return 0

    if not has_target(project / "Makefile", TARGET):
        return 0

    try:
        result = subprocess.run(
            ["make", TARGET], cwd=project, capture_output=True, text=True, timeout=TIMEOUT_S
        )
    except subprocess.TimeoutExpired:
        return 0

    if result.returncode == 0:
        return 0

    output = (result.stdout + result.stderr).strip().splitlines()
    print(
        f"`make {TARGET}` failed on your uncommitted changes. Fix it before finishing, "
        "or tell the user exactly what fails and why you stopped.\n\n"
        + "\n".join(output[-TAIL_LINES:]),
        file=sys.stderr,
    )
    return 2


def has_target(makefile: Path, target: str) -> bool:
    if not makefile.is_file():
        return False
    pattern = re.compile(rf"^{re.escape(target)}\s*:", re.MULTILINE)
    return bool(pattern.search(makefile.read_text(encoding="utf-8", errors="ignore")))


if __name__ == "__main__":
    sys.exit(main())
