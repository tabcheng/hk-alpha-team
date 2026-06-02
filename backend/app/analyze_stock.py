from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from app.analysis_workflow import build_first_analysis_workflow

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


def build_analyze_stock_response(symbol: str) -> dict:
    """Return the Phase 4A deterministic local-only first analysis workflow payload."""

    return build_first_analysis_workflow(symbol)
