from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.analyze_stock import AnalyzeStockRequest, build_analyze_stock_stub
from app.contracts import error_envelope, success_envelope
from app.status_reader import read_project_status

app = FastAPI(title="HK Alpha Team Backend", version="0.1.0")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=error_envelope(
            "VALIDATION_ERROR",
            "Request validation failed.",
            {"errors": exc.errors(), "path": str(request.url.path)},
        ),
    )


@app.get("/health")
def health() -> dict:
    return success_envelope({"service": "ok"})


@app.get("/api/v1/project-status")
def project_status() -> dict:
    return success_envelope(read_project_status())


@app.post("/api/v1/analyze-stock")
def analyze_stock(request: AnalyzeStockRequest) -> dict:
    warnings = [
        "Stub response only; no live analysis, persistence, production Supabase, or trading execution performed."
    ]
    return success_envelope(build_analyze_stock_stub(request.symbol), warnings=warnings)
