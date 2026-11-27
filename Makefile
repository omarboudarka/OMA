# One entry point for you, Claude and CI. `make` lists the targets.
.DEFAULT_GOAL := help
SHELL := /bin/bash
.SHELLFLAGS := -euo pipefail -c

CORE := cd services/core &&
WEB := pnpm --dir apps/web
COMPOSE := docker compose -f infra/compose.yaml

.PHONY: help install dev dev-down check check-fast test-int eval \
	core-lint core-unit core-types web-lint web-types web-format

help: ## List targets
	@grep -hE '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk -F':.*## ' '{printf "  %-12s %s\n", $$1, $$2}'

install: ## Install core (uv) and web (pnpm) dependencies
	$(CORE) uv sync
	$(WEB) install

dev: ## Core API in Docker on :8000, web on the host on :3000 (stop the API with make dev-down)
	$(COMPOSE) up --build --detach --wait core
	$(WEB) dev

dev-down: ## Stop the local stack
	$(COMPOSE) down

check-fast: core-lint core-unit web-lint ## Quick subset: lint, format, dependency rules, unit tests

check: check-fast core-types web-types web-format ## Everything: check-fast plus types and web format. Run before every commit.

test-int: ## Integration tests (local Postgres arrives with OMA-13)
	@$(CORE) rc=0; uv run pytest -m integration -q || rc=$$?; \
	if [ $$rc -eq 5 ]; then echo "no integration tests yet"; exit 0; fi; exit $$rc

eval: ## Smoke evals for one stage: make eval STAGE=<stage>
	@test -n "$(STAGE)" || { echo "usage: make eval STAGE=<stage>"; exit 2; }
	$(CORE) uv run python ../../evals/run.py --stage "$(STAGE)"

core-lint:
	$(CORE) uv run ruff check . ../../evals
	$(CORE) uv run ruff format --check . ../../evals
	$(CORE) uv run lint-imports

core-unit:
	$(CORE) uv run pytest -m "not integration" -q

core-types:
	$(CORE) uv run mypy
	$(CORE) uv run mypy ../../evals/run.py

web-lint:
	$(WEB) lint

web-types:
	$(WEB) typecheck

web-format:
	$(WEB) format:check
