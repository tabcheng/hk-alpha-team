from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.analysis_workflow import PHASE_4A_WARNINGS
from app.analyze_stock import AnalyzeStockRequest, build_analyze_stock_response
from app.contracts import error_envelope, success_envelope
from app.simulation_runtime import (
    RUNTIME_WARNINGS,
    PaperOrderRequest,
    SimulationRuntimeValidationError,
    build_paper_portfolio_snapshot,
    create_paper_order_record,
)
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
    return success_envelope(build_analyze_stock_response(request.symbol), warnings=PHASE_4A_WARNINGS)


@app.post("/api/v1/simulation/paper-orders")
def create_simulation_paper_order(request: PaperOrderRequest):
    try:
        data = create_paper_order_record(request)
    except SimulationRuntimeValidationError as exc:
        return JSONResponse(
            status_code=422,
            content=error_envelope(
                "VALIDATION_ERROR",
                "Simulation Desk paper order validation failed.",
                {"message": str(exc), "path": "/api/v1/simulation/paper-orders"},
            ),
        )
    return success_envelope(data, warnings=RUNTIME_WARNINGS)


@app.get("/api/v1/paper-portfolios/{portfolio_id}")
def get_paper_portfolio(portfolio_id: str):
    try:
        data = build_paper_portfolio_snapshot(portfolio_id)
    except SimulationRuntimeValidationError as exc:
        return JSONResponse(
            status_code=404,
            content=error_envelope(
                "NOT_FOUND",
                "Paper portfolio was not found in the non-production in-memory store.",
                {"message": str(exc), "portfolio_id": portfolio_id},
            ),
        )
    return success_envelope(data, warnings=RUNTIME_WARNINGS)
