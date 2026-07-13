from __future__ import annotations

import math

from fastapi import FastAPI, HTTPException, Request, status
from pydantic import BaseModel, Field, field_validator

from model_artifact import DoubleItModelService


class InputData(BaseModel):
    input: list[float] = Field(min_length=1, max_length=1024)

    @field_validator("input")
    @classmethod
    def finite_values(cls, values: list[float]) -> list[float]:
        if not all(math.isfinite(value) for value in values):
            raise ValueError("input values must be finite numbers")
        return values


class OutputData(BaseModel):
    output: list[float]


class HealthData(BaseModel):
    status: str
    model: str
    framework: str
    sha256: str
    contract: str


def create_app(model_service: DoubleItModelService | None = None) -> FastAPI:
    app = FastAPI(title="DoubleIt Model API")
    app.state.model_service = model_service or DoubleItModelService.from_manifest()

    @app.get("/health", response_model=HealthData)
    async def health(request: Request) -> dict[str, str]:
        manifest = request.app.state.model_service.manifest
        return {"status": "ok", **manifest.health_payload()}

    @app.post("/infer", response_model=OutputData)
    async def infer(data: InputData, request: Request) -> OutputData:
        try:
            output = request.app.state.model_service.predict(data.input)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="model inference failed",
            ) from exc
        return OutputData(output=output)

    return app


app = create_app()
