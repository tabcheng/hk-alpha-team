from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.contracts import SCHEMA_VERSION, utc_timestamp

StrategyLabel = Literal[
    "STRONG_WATCH",
    "WAIT_FOR_PULLBACK",
    "SMALL_POSITION",
    "ACCUMULATE",
    "HOLD",
    "REDUCE_RISK",
    "AVOID",
]

SUPPORTED_SYMBOL_PATTERN = r"^\d{4}\.HK$"


class AnalyzeStockRequest(BaseModel):
    symbol: str = Field(
        ...,
        pattern=SUPPORTED_SYMBOL_PATTERN,
        description="Hong Kong equity symbol in canonical four-digit .HK format, for example 0700.HK.",
    )


def build_analyze_stock_stub(symbol: str) -> dict:
    """Return a contract-shaped placeholder for the first analysis workflow.

    The payload intentionally avoids live market data, persistence, production Supabase,
    and real-money trading actions while Phase 3 prepares the Phase 4 workflow.
    """

    generated_at = utc_timestamp()
    recommendation: StrategyLabel = "STRONG_WATCH"

    return {
        "symbol": symbol,
        "analysis_status": "stub_only",
        "workflow_phase": "Phase 3 — Backend Skeleton",
        "strategy_recommendation": recommendation,
        "summary": "Contract-first placeholder response for future first-pass stock analysis.",
        "confidence_level": 0,
        "scores": {
            "market": None,
            "fundamental": None,
            "technical": None,
            "sentiment": None,
            "risk": None,
            "simulation": None,
        },
        "key_reasons": [
            "Endpoint contract is available for client and test integration.",
            "No live market, financial, news, or simulation data has been analyzed in this stub.",
        ],
        "main_risks": [
            "Do not interpret this stub as investment advice.",
            "Future analysis quality depends on validated data sources and agent workflow implementation.",
        ],
        "invalidation_conditions": [
            "Replace this stub once Phase 4 first analysis workflow is implemented and tested.",
            "Reject outputs that omit reasoning, risk framing, invalidation conditions, or human decision framing.",
        ],
        "paper_trading_action": "No paper order is created by this stub.",
        "real_money_decision": "Human decision required by Harness Engineering; no real-money trade is executed.",
        "next_review_date": None,
        "agent_trace": {
            "agent_runs_created": False,
            "agent_outputs_created": False,
            "persistence_enabled": False,
            "production_supabase_required": False,
        },
        "generated_at": generated_at,
        "schema_version": SCHEMA_VERSION,
    }
