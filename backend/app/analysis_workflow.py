from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

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

WORKFLOW_PHASE = "Phase 4A — Deterministic First Analysis Workflow Skeleton"
ANALYSIS_STATUS = "phase4a_skeleton"

PHASE_4A_WARNINGS = [
    "Phase 4A deterministic skeleton only; this is not live investment research.",
    "No live market data, external data provider, or network service is used.",
    "No persistence writes, recommendation records, paper orders, or production Supabase connection are used.",
    "No broker execution, brokerage API integration, real-money order placement, or autonomous trading is performed.",
    "Advisory-only placeholder output; Harness Engineering must make any real-money decision manually.",
]


@dataclass(frozen=True)
class StockContext:
    symbol: str
    exchange: str
    currency: str
    context_source: str
    live_data_used: bool


@dataclass(frozen=True)
class StageScore:
    score: int
    confidence: int
    rationale: str


def normalize_symbol(symbol: str) -> str:
    """Normalize internal workflow input without changing API validation rules."""

    return symbol.strip().upper()


def build_static_stock_context(symbol: str) -> StockContext:
    return StockContext(
        symbol=symbol,
        exchange="HKEX",
        currency="HKD",
        context_source="static_phase4a_placeholder",
        live_data_used=False,
    )


def _symbol_seed(symbol: str) -> int:
    return sum((idx + 1) * ord(char) for idx, char in enumerate(symbol))


def score_market_placeholder(context: StockContext) -> StageScore:
    seed = _symbol_seed(context.symbol)
    return StageScore(
        score=45 + (seed % 11),
        confidence=20,
        rationale="Local deterministic market placeholder; not derived from live index, liquidity, or macro data.",
    )


def score_fundamental_placeholder(context: StockContext) -> StageScore:
    seed = _symbol_seed(context.symbol)
    return StageScore(
        score=48 + ((seed // 3) % 10),
        confidence=20,
        rationale="Local deterministic fundamental placeholder; not derived from financial statements or filings.",
    )


def score_technical_placeholder(context: StockContext) -> StageScore:
    seed = _symbol_seed(context.symbol)
    return StageScore(
        score=44 + ((seed // 5) % 12),
        confidence=20,
        rationale="Local deterministic technical placeholder; not derived from OHLCV bars, volume, or indicators.",
    )


def score_sentiment_placeholder(context: StockContext) -> StageScore:
    seed = _symbol_seed(context.symbol)
    return StageScore(
        score=46 + ((seed // 7) % 10),
        confidence=20,
        rationale="Local deterministic sentiment placeholder; not derived from news, social, or broker commentary.",
    )


def score_risk_placeholder(context: StockContext) -> StageScore:
    seed = _symbol_seed(context.symbol)
    return StageScore(
        score=40 + ((seed // 11) % 15),
        confidence=25,
        rationale="Local deterministic risk placeholder; not derived from portfolio holdings or live volatility data.",
    )


def _strategy_from_scores(scores: dict[str, int]) -> StrategyLabel:
    average_score = sum(scores.values()) / len(scores)
    risk_score = scores["risk"]

    if average_score >= 58 and risk_score >= 50:
        return "STRONG_WATCH"
    if average_score >= 53:
        return "WAIT_FOR_PULLBACK"
    if average_score >= 48:
        return "HOLD"
    return "REDUCE_RISK"


def build_agent_trace(stage_names: list[str]) -> dict[str, object]:
    return {
        "workflow_name": "first_analysis_workflow_skeleton",
        "workflow_phase": WORKFLOW_PHASE,
        "workflow_stages": stage_names,
        "agent_runs_created": False,
        "agent_outputs_created": False,
        "persistence_enabled": False,
        "production_supabase_required": False,
        "production_supabase_connected": False,
        "recommendation_record_created": False,
        "paper_order_created": False,
        "broker_execution_enabled": False,
        "broker_api_called": False,
        "real_money_order_placed": False,
        "network_services_called": False,
        "secrets_required": False,
    }


def build_first_analysis_workflow(symbol: str) -> dict[str, object]:
    """Build a deterministic, local-only Phase 4A analyze-stock response payload."""

    normalized_symbol = normalize_symbol(symbol)
    context = build_static_stock_context(normalized_symbol)

    stage_scores = {
        "market": score_market_placeholder(context),
        "fundamental": score_fundamental_placeholder(context),
        "technical": score_technical_placeholder(context),
        "sentiment": score_sentiment_placeholder(context),
        "risk": score_risk_placeholder(context),
    }
    numeric_scores = {name: score.score for name, score in stage_scores.items()}
    recommendation = _strategy_from_scores(numeric_scores)

    stage_names = [
        "input_normalization",
        "static_stock_context_placeholder",
        "deterministic_market_placeholder_scoring",
        "deterministic_fundamental_placeholder_scoring",
        "deterministic_technical_placeholder_scoring",
        "deterministic_sentiment_placeholder_scoring",
        "deterministic_risk_placeholder_scoring",
        "advisory_summary_generation",
        "key_reasons_generation",
        "main_risks_generation",
        "invalidation_conditions_generation",
        "human_decision_framing",
        "workflow_trace_metadata",
    ]

    return {
        "symbol": normalized_symbol,
        "analysis_status": ANALYSIS_STATUS,
        "workflow_phase": WORKFLOW_PHASE,
        "strategy_recommendation": recommendation,
        "summary": (
            f"Phase 4A deterministic local-only skeleton for {normalized_symbol}. "
            "This is not live investment research and uses placeholder scoring only."
        ),
        "confidence_level": 20,
        "scores": {
            "market": stage_scores["market"].score,
            "fundamental": stage_scores["fundamental"].score,
            "technical": stage_scores["technical"].score,
            "sentiment": stage_scores["sentiment"].score,
            "risk": stage_scores["risk"].score,
            "simulation": None,
            "score_basis": "deterministic_phase4a_placeholders_not_market_data_derived",
        },
        "score_confidence": {name: score.confidence for name, score in stage_scores.items()},
        "key_reasons": [
            "The endpoint now delegates to explicit local workflow stages instead of returning a Phase 3 static stub.",
            "Placeholder scores are deterministic for the normalized symbol and are not derived from live market data.",
            "The recommendation label is conservative and contract-compatible for downstream validation only.",
        ],
        "main_risks": [
            "Do not treat this skeleton as investment advice or complete equity research.",
            "No live prices, fundamentals, news, portfolio state, or simulation performance were evaluated.",
            "Future production-quality analysis requires validated data sources, persistence design, and reviewed agent outputs.",
        ],
        "invalidation_conditions": [
            "Invalidate this output if it is presented as live investment research.",
            "Invalidate this output if any persistence, production Supabase, broker execution, or real-money order placement occurs.",
            "Replace or extend this skeleton only through reviewed Phase 4 follow-up work with tests and updated docs.",
        ],
        "paper_trading_action": "No paper order is created by this Phase 4A skeleton.",
        "real_money_decision": "Harness Engineering human decision required; no real-money trade is executed or placed.",
        "next_review_date": None,
        "stock_context": {
            "exchange": context.exchange,
            "currency": context.currency,
            "context_source": context.context_source,
            "live_data_used": context.live_data_used,
        },
        "stage_rationales": {name: score.rationale for name, score in stage_scores.items()},
        "agent_trace": build_agent_trace(stage_names),
        "generated_at": utc_timestamp(),
        "schema_version": SCHEMA_VERSION,
    }
