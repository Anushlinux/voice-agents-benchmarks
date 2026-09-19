"""Import-safe API shell. Starting it never initializes provider clients."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from voice_bench import __version__
from voice_bench.readiness import scaffold_status


def create_app() -> FastAPI:
    app = FastAPI(
        title="Voice Agent Benchmark",
        version=__version__,
        description="Local scaffold API. Live calls and business tools are not implemented.",
    )

    @app.get("/healthz")
    def health() -> dict[str, str]:
        return {"status": "ok", "stage": "scaffold"}

    @app.get("/readyz", status_code=503)
    def readiness() -> JSONResponse:
        return JSONResponse(status_code=503, content=scaffold_status())

    return app
