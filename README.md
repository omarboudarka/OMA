# OMA — AI study assistant

An AI study assistant that turns weekly course uploads into a concept graph, finds the prerequisite a student is missing, and serves the next exercise at the right difficulty. The pilot course is EPFL Analysis I (MATH-101).

> **Status:** Phase 0, foundations. The skeleton runs: a FastAPI health check and an empty Next.js app.

## Getting started

You need `uv`, `pnpm`, Node 22+ and Docker.

```bash
make install   # core (uv) and web (pnpm) dependencies
make dev       # core API in Docker on :8000, web on :3000
make check     # lint, format, types, unit tests, dependency rules
```

Run `make` with no target to see the rest.

## No course material in this repo

Lecture notes, exercise sheets and solutions belong to their authors. This repo holds code and self-written fixtures only. Real course files stay on your machine (for example in an ignored `course-material/` folder) or in private storage, and are never committed.

## Planned stack

| Part                 | Tools                                                    |
| -------------------- | -------------------------------------------------------- |
| Core API and workers | Python, FastAPI, Pydantic, Procrastinate, uv             |
| Data                 | Supabase: Postgres with pgvector, Auth, Storage          |
| Web                  | Next.js, shadcn/ui, Tailwind, pnpm                       |
| AI layer             | LiteLLM router, LangChain and LangGraph agents, Langfuse |
| Delivery             | Docker, GitHub Actions, Vercel, Railway                  |

The core follows ports and adapters, so any vendor above can be swapped behind an interface.

## How work is tracked

Work is planned in Linear (team key `OMA`). Each branch and pull request carries its issue ID, for example `oma-12-ci-workflow`, so Linear moves the issue as the pull request opens and merges.

## License

MIT
