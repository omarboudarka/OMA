# OMA — AI study assistant

Turns weekly course uploads into a concept graph, finds the prerequisite a student is missing, and serves the next exercise at the right difficulty. Pilot course: EPFL Analysis I.

## Status

Phase 0. The monorepo skeleton (OMA-9), CI (OMA-12) and the local stack (OMA-13) are not built yet, so some `make` targets below may not exist. If one is missing, say so; don't improvise a substitute.

## Where the spec lives

The Linear issue is the spec for the task in hand: acceptance criteria, plus an "Agent notes" section with pointers. Read the whole issue and its comments before planning. Longer design notes go in `docs/` (architecture, `adr/`, `features/OMA-<n>-<slug>.md`).

## Layout (target)

- `apps/web/`: Next.js App Router, shadcn/ui, Tailwind, pnpm
- `services/core/`: Python 3.12, FastAPI, Pydantic, Procrastinate, uv. Inside: `domain/`, `application/`, `ports/`, `adapters/`, `entrypoints/` (api, worker, cli)
- `packages/schemas/`: JSON Schema contracts between web and core
- `prompts/`: one file per prompt, version in the file name
- `config/model_policy.yaml`: task → tier → model routing
- `supabase/migrations/`: SQL migrations, applied in order
- `evals/`: datasets, runners, `thresholds.yaml`
- `infra/`: Dockerfiles, compose

## Commands

- `make dev`: local stack (Supabase and worker in Docker, web on the host)
- `make check`: lint, format, types, unit tests, dependency rules. Run before every commit.
- `make check-fast`: the quick subset; the Stop hook runs it when you finish with uncommitted changes
- `make test-int`: integration tests against local Postgres
- `make eval STAGE=<stage>`: smoke evals for one pipeline stage

## Workflow

- Start from a Linear issue (team `OMA`) with `/start-issue OMA-<n>`. The branch name is the issue's `gitBranchName`.
- Plan before editing anything that touches more than one file, and wait for the user to approve the plan.
- Write the failing test first, then the code, then run `make check` and show the output.
- Finish with `/open-pr`. PR title: `type: summary (OMA-<n>)` with type `feat`, `fix`, `eval`, `chore`, `docs` or `refactor`.
- PR body: `Closes OMA-<n>` when every acceptance criterion is met, `Part of OMA-<n>` when work is left.
- One concern per PR, ideally under about 400 changed lines, not counting generated files and fixtures.
- `main` changes only through pull requests. Never push to `main` and never force-push.

## Rules

- The domain never imports adapters (import-linter enforces it in CI). A new vendor goes behind a port, with a fake and the port's conformance tests.
- Every model call goes through the LLM port (LiteLLM's router, policy in `config/model_policy.yaml`). No direct provider SDK calls.
- Tests never call real model APIs. Use `FakeLLM` or recorded fixtures.
- Prompts live in `prompts/` with a version. Changing one means running its eval and reporting before → after.
- Never edit an applied migration; add a new one. A hook blocks edits to migrations already on `main`.
- Pipeline stages are idempotent, keyed by `(document_id, stage, pipeline_version)`.
- Secrets come from the environment. Never read or write `.env` files (a hook blocks edits); add new variables to `.env.example` and tell the user to set the real value.
- IMPORTANT: no course material in the repo. Fixtures are self-written; real course files stay in the ignored `course-material/` folder.

## Gotchas

- Math stays LaTeX end to end, from parsing to rendering.
- French and English names of a concept are aliases of one graph node, never two nodes.
