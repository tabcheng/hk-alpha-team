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

    return success_envelope(
        {
            "symbol": symbol,
            "workflow_status": "stub",
            "strategy_label": "WAIT_FOR_PULLBACK",
            "summary": "Stub response only. Real analysis is not implemented yet.",
            "key_reasons": [
                "Contract-first endpoint is active for Phase 3 readiness.",
                "No market, fundamental, or technical analysis has been executed.",
            ],
            "main_risks": [
                "Do not use this stub payload as an investment recommendation.",
            ],
            "invalidation_conditions": [
                "Phase 4 implementation replaces stub with real analysis workflow.",
            ],
            "suggested_user_action": "Review stub status and wait for Phase 4 implementation.",
            "paper_trading_action": "No paper order suggested from stub output.",
            "real_money_decision_owner": "HUMAN_USER",
        },
        warnings=[
            "analyze-stock is a contract stub and returns non-actionable placeholder data.",
        ],
    )
