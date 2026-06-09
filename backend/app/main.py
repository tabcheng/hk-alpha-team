from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.analysis_workflow import PHASE_4A_WARNINGS
from app.analyze_stock import AnalyzeStockRequest, build_analyze_stock_response
from app.contracts import error_envelope, success_envelope
from app.simulation_runtime import (
    PaperOrderRequest,
    SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES,
    SimulationPersistenceConfig,
    SimulationRuntimeConfigurationError,
    SimulationRuntimeNotFoundError,
    SimulationRuntimeValidationError,
    build_paper_portfolio_snapshot,
    create_paper_order_response_data,
    runtime_warnings_for_persistence_config,
    simulation_persistence_config_from_env,
)
from app.status_reader import read_project_status

app = FastAPI(title="HK Alpha Team Backend", version="0.1.0")


def resolve_simulation_persistence_config() -> SimulationPersistenceConfig:
    return simulation_persistence_config_from_env()


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


@app.exception_handler(SimulationRuntimeConfigurationError)
async def simulation_configuration_exception_handler(
    request: Request,
    exc: SimulationRuntimeConfigurationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content=error_envelope(
            "CONFIGURATION_ERROR",
            "Simulation Desk local/test persistence configuration failed safely.",
            {
                "message": str(exc),
                "path": str(request.url.path),
                "production_supabase_connected": False,
                "database_url_authorizes_persistence": False,
            },
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
def create_simulation_paper_order(
    request: PaperOrderRequest,
    persistence_config: SimulationPersistenceConfig = Depends(resolve_simulation_persistence_config),
):
    try:
        data = create_paper_order_response_data(request, persistence_config=persistence_config)
    except SimulationRuntimeValidationError as exc:
        return JSONResponse(
            status_code=422,
            content=error_envelope(
                "VALIDATION_ERROR",
                "Simulation Desk paper order validation failed.",
                {"message": str(exc), "path": "/api/v1/simulation/paper-orders"},
            ),
        )
    except SimulationRuntimeConfigurationError as exc:
        return JSONResponse(
            status_code=500,
            content=error_envelope(
                "CONFIGURATION_ERROR",
                "Simulation Desk local/test persistence configuration failed safely.",
                {
                    "message": str(exc),
                    "path": "/api/v1/simulation/paper-orders",
                    "production_supabase_connected": False,
                    "database_url_authorizes_persistence": False,
                },
            ),
        )
    metadata_extra = (
        persistence_config.metadata
        if persistence_config.mode == SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES
        else None
    )
    return success_envelope(
        data,
        warnings=runtime_warnings_for_persistence_config(persistence_config),
        metadata_extra=metadata_extra,
    )


@app.get("/api/v1/paper-portfolios/{portfolio_id}")
def get_paper_portfolio(
    portfolio_id: str,
    persistence_config: SimulationPersistenceConfig = Depends(resolve_simulation_persistence_config),
):
    try:
        data = build_paper_portfolio_snapshot(portfolio_id, persistence_config=persistence_config)
    except SimulationRuntimeValidationError as exc:
        return JSONResponse(
            status_code=422,
            content=error_envelope(
                "VALIDATION_ERROR",
                "Paper portfolio request validation failed.",
                {"message": str(exc), "portfolio_id": portfolio_id},
            ),
        )
    except SimulationRuntimeConfigurationError as exc:
        return JSONResponse(
            status_code=500,
            content=error_envelope(
                "CONFIGURATION_ERROR",
                "Simulation Desk local/test persistence configuration failed safely.",
                {
                    "message": str(exc),
                    "path": f"/api/v1/paper-portfolios/{portfolio_id}",
                    "production_supabase_connected": False,
                    "database_url_authorizes_persistence": False,
                },
            ),
        )
    except SimulationRuntimeNotFoundError as exc:
        return JSONResponse(
            status_code=404,
            content=error_envelope(
                "NOT_FOUND",
                "Paper portfolio was not found in the non-production Simulation Desk store.",
                {"message": str(exc), "portfolio_id": portfolio_id},
            ),
        )
    metadata_extra = (
        persistence_config.metadata
        if persistence_config.mode == SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES
        else None
    )
    return success_envelope(
        data,
        warnings=runtime_warnings_for_persistence_config(persistence_config),
        metadata_extra=metadata_extra,
    )
