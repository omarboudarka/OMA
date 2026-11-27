#!/usr/bin/env python3
"""PostToolUse hook for Edit, Write and MultiEdit: format the file Claude just changed.

- Python: ruff format, using the core service's environment when it exists
- TypeScript, JavaScript, JSON, CSS, Markdown, YAML: the web app's Prettier

Formatting only, never lint fixes: `ruff check --fix` would delete an import Claude
added one edit before using it. Linting runs in `make check`.

Silent when a formatter isn't installed yet (Phase 0), so it never gets in the way.
Always exits 0: the edit already happened, and formatting problems surface in `make check`.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

PRETTIER_SUFFIXES = {
    ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs",
    ".json", ".css", ".md", ".mdx", ".yaml", ".yml",
}


def run(cmd: list[str], cwd: Path) -> None:
    try:
        subprocess.run(cmd, cwd=cwd, capture_output=True, timeout=25)
    except (OSError, subprocess.TimeoutExpired):
        pass


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    raw_path = (data.get("tool_input") or {}).get("file_path")
    if not raw_path:
        return 0
    path = Path(raw_path)
    if not path.is_file():
        return 0

    project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or ".")

    if path.suffix == ".py":
        core = project / "services" / "core"
        if shutil.which("uv") and (core / ".venv").is_dir():
            run(["uv", "run", "--no-sync", "ruff", "format", "--quiet", str(path)], core)
        elif shutil.which("ruff"):
            run(["ruff", "format", "--quiet", str(path)], project)
    elif path.suffix in PRETTIER_SUFFIXES:
        prettier = project / "apps" / "web" / "node_modules" / ".bin" / "prettier"
        if prettier.exists():
            run([str(prettier), "--write", "--log-level", "silent", str(path)], project / "apps" / "web")

    return 0


if __name__ == "__main__":
    sys.exit(main())
