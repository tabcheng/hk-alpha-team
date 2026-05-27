from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.contracts import error_envelope, success_envelope
from app.status_reader import read_project_status

app = FastAPI(title="HK Alpha Team Backend", version="0.1.0")


class AnalyzeStockRequest(BaseModel):
    symbol: str = Field(min_length=1, examples=["0700.HK"])


@app.get("/health")
def health() -> dict:
    return success_envelope({"service": "ok"})


@app.get("/api/v1/project-status")
def project_status() -> dict:
    return success_envelope(read_project_status())


@app.post("/api/v1/analyze-stock")
def analyze_stock(payload: AnalyzeStockRequest) -> dict:
    symbol = payload.symbol.strip().upper()
    if not symbol:
        return error_envelope(
            code="VALIDATION_ERROR",
            message="symbol is required",
            details={"field": "symbol", "rule": "non_empty"},
        )

    if not symbol.endswith(".HK"):
        return error_envelope(
            code="VALIDATION_ERROR",
            message="symbol must be a supported HK symbol format",
            details={"field": "symbol", "rule": "hk_symbol", "example": "0700.HK"},
        )

    return success_envelope(
        {
            "symbol": symbol,
            "analysis_mode": "stub",
            "human_decision_required": True,
            "recommendation": {
                "confidence": 0,
                "summary": "No real investment analysis has been performed. This is a stub contract response.",
            },
            "summary": "Contract test stub only. No real investment analysis has been performed.",
            "real_money_decision_owner": "HUMAN_USER",
        },
        warnings=[
            "Stub response for contract testing only; not an investment recommendation.",
        ],
    )
