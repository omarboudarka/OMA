# evals

Smoke evals per pipeline stage.

- `datasets/<stage>/`: self-written cases for one stage (no course material, see the root README)
- `thresholds.yaml`: the minimum score per stage and metric
- `run.py`: the runner, called by `make eval STAGE=<stage>`

A stage with no dataset yet reports "no evals" and passes, so `make eval` works before any stage exists.
