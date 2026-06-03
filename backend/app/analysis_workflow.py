from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from app.contracts import SCHEMA_VERSION, utc_timestamp
from app.department_adapters import (
    build_department_outputs,
    build_score_buckets,
    build_score_confidence,
)

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
    "Phase 4A deterministic skeleton with Phase 4B department adapter previews only; this is not live investment research.",
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

def normalize_symbol(symbol: str) -> str:
    """Normalize internal workflow input without changing API validation rules."""

    return symbol.strip().upper()


def build_static_stock_context(symbol: str) -> StockContext:
    return StockContext(
        symbol=symbol,
        exchange="HKEX",
        currency="HKD",
        context_source="static_phase4a_department_adapter_placeholder",
        live_data_used=False,
    )

def _strategy_from_scores(scores: dict[str, int]) -> StrategyLabel:
    scored_values = [value for value in scores.values() if isinstance(value, int)]
    average_score = sum(scored_values) / len(scored_values)
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
    """Build a deterministic, local-only Phase 4A analyze-stock response payload backed by Phase 4B adapters."""

    normalized_symbol = normalize_symbol(symbol)
    context = build_static_stock_context(normalized_symbol)

    department_outputs = build_department_outputs(normalized_symbol)
    numeric_scores = build_score_buckets(department_outputs)
    score_confidence = build_score_confidence(department_outputs)
    recommendation = _strategy_from_scores(numeric_scores)

    stage_names = [
        "input_normalization",
        "static_stock_context_placeholder",
        "phase4b_department_adapter_output_generation",
        "adapter_backed_market_scoring",
        "adapter_backed_fundamental_scoring",
        "adapter_backed_technical_scoring",
        "adapter_backed_sentiment_scoring",
        "adapter_backed_risk_scoring",
        "adapter_backed_simulation_scoring",
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
            f"Phase 4A deterministic local-only skeleton for {normalized_symbol} now backed by Phase 4B "
            "department adapter previews. This is not live investment research and uses placeholder scoring only."
        ),
        "confidence_level": 20,
        "scores": {
            "market": numeric_scores["market"],
            "fundamental": numeric_scores["fundamental"],
            "technical": numeric_scores["technical"],
            "sentiment": numeric_scores["sentiment"],
            "risk": numeric_scores["risk"],
            "simulation": numeric_scores["simulation"],
            "score_basis": "deterministic_phase4b_department_adapters_not_market_data_derived",
        },
        "score_confidence": score_confidence,
        "key_reasons": [
            "The endpoint delegates to deterministic local department adapters instead of inline placeholder scoring.",
            "Adapter outputs mirror the locked common agent output shape but are not persisted agent_outputs records.",
            "Placeholder scores are deterministic for the normalized symbol and are not derived from live market data.",
            "The recommendation label is conservative and contract-compatible for downstream validation only.",
        ],
        "main_risks": [
            "Do not treat this skeleton as investment advice or complete equity research.",
            "No live prices, fundamentals, news, portfolio state, or simulation performance were evaluated or fetched.",
            "Future production-quality analysis requires validated data sources, persistence design, and reviewed agent outputs.",
        ],
        "invalidation_conditions": [
            "Invalidate this output if it is presented as live investment research.",
            "Invalidate this output if any persistence, production Supabase, broker execution, or real-money order placement occurs.",
            "Replace or extend these adapters only through reviewed Phase 4 follow-up work with tests and updated docs.",
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
        "stage_rationales": {
            output["agent_name"]: output["evidence"][0] for output in department_outputs
        },
        "department_outputs": department_outputs,
        "department_output_note": (
            "Local-only deterministic adapter preview metadata; not persisted agent_outputs records and not live research."
        ),
        "agent_trace": build_agent_trace(stage_names),
        "generated_at": utc_timestamp(),
        "schema_version": SCHEMA_VERSION,
    }
