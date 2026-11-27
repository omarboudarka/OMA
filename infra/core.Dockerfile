# Core API image. Build context is the repo root (see infra/compose.yaml).
FROM ghcr.io/astral-sh/uv:0.13.10-python3.12-trixie-slim

WORKDIR /app
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Dependencies first, so code changes don't reinstall them
COPY services/core/pyproject.toml services/core/uv.lock services/core/.python-version ./
RUN uv sync --frozen --no-dev --no-install-project

COPY services/core/src ./src
RUN uv sync --frozen --no-dev

EXPOSE 8000
CMD ["uv", "run", "--no-sync", "uvicorn", "oma_core.entrypoints.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
