"""HTTP entrypoint. Run with `uvicorn oma_core.entrypoints.api.app:app`."""

from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="OMA core")


class Health(BaseModel):
    status: Literal["ok"] = "ok"


@app.get("/health")
def health() -> Health:
    return Health()
