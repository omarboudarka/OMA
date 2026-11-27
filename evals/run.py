"""Run the smoke evals for one pipeline stage: `make eval STAGE=<stage>`.

Phase 0: no stage has a dataset yet, so every stage reports "no evals" and passes.
Scoring against thresholds.yaml arrives with the first stage's dataset.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATASETS = ROOT / "evals" / "datasets"
STAGE_NAME = re.compile(r"^[a-z][a-z0-9_]*$")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", required=True, help="pipeline stage, e.g. extract_concepts")
    args = parser.parse_args(argv)

    if not STAGE_NAME.match(args.stage):
        parser.error(f"invalid stage name {args.stage!r}: use lowercase snake_case")

    dataset = DATASETS / args.stage
    if not dataset.is_dir():
        print(f"no evals for stage {args.stage!r} yet ({dataset.relative_to(ROOT)} missing)")
        return 0

    print(f"stage {args.stage!r} has a dataset, but no runner is wired up yet", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
