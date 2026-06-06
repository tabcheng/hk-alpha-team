from __future__ import annotations

import re
from copy import deepcopy
from typing import Any, Mapping

from pydantic import BaseModel, ConfigDict, Field

from app.simulation_origin_contract import validate_simulation_origin_payload
from app.simulation_store import InMemorySimulationStore, simulation_store

HK_SYMBOL_PATTERN = re.compile(r"^\d{4}\.HK$")
PORTFOLIO_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:-]{2,63}$")
VALID_ORDER_SIDES = {"buy", "sell"}
VALID_ORDER_TYPES = {"market", "limit"}

RUNTIME_FALSE_BOUNDARY_FLAGS = (
    "real_money_order_placed",
    "real_money_trading_automation_enabled",
    "autonomous_real_money_execution",
    "broker_execution_enabled",
    "broker_api_called",
    "production_supabase_connected",
    "persistence_write_performed",
    "secrets_required",
    "external_api_called",
    "billing_runtime_enabled",
    "membership_runtime_enabled",
    "auth_runtime_enabled",
    "deployment_required",
)

RUNTIME_TRUE_BOUNDARY_FLAGS = (
    "paper_only",
    "advisory_only",
    "human_in_the_loop",
)

RUNTIME_WARNINGS = [
    "Simulation Desk runtime is paper-only and advisory-only; all real-money decisions remain human-controlled.",
    "No real-money order is placed, no broker API is called, and autonomous real-money execution is disabled.",
    "This non-production runtime uses process-local in-memory records only; no production Supabase connection or persistence write is performed.",
    "No secrets, billing, membership, auth, deployment, live market data, or external API integrations are required by this slice.",
]


class PaperOrderRequest(BaseModel):
    """Additive runtime schema for the locked Simulation Desk paper-order endpoint."""

    model_config = ConfigDict(extra="allow")

    portfolio_id: str | None = None
    symbol: str | None = None
    side: str | None = None
    quantity: int | float | None = None
    order_type: str = "market"
    limit_price: int | float | None = None
    base_currency: str = "HKD"
    simulation_origin: str | None = None
    created_by_type: str | None = None
    advisory_only: bool = True
    human_in_the_loop: bool = True
    paper_only: bool = True
    boundary_flags: dict[str, bool] = Field(default_factory=dict)
    proposals_reviewable: bool = True
    proposals_auto_applied: bool = False
    losing_outcomes_remain_visible: bool = True
    historical_recommendations_overwritten: bool = False


class SimulationRuntimeValidationError(ValueError):
    pass


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SimulationRuntimeValidationError(message)


def _as_payload(request: PaperOrderRequest | Mapping[str, Any]) -> dict[str, Any]:
    if isinstance(request, PaperOrderRequest):
        return request.model_dump(mode="python")
    _require(isinstance(request, Mapping), "payload must be a mapping")
    return dict(request)


def _non_empty_string(payload: Mapping[str, Any], field_name: str) -> str:
    value = payload.get(field_name)
    _require(isinstance(value, str), f"{field_name} must be a string")
    stripped = value.strip()
    _require(stripped != "", f"{field_name} must be present")
    return stripped


def _number(payload: Mapping[str, Any], field_name: str) -> int | float:
    value = payload.get(field_name)
    _require(isinstance(value, (int, float)) and not isinstance(value, bool), f"{field_name} must be numeric")
    return value


def _merge_boundary_flags(payload: dict[str, Any]) -> dict[str, bool]:
    nested = payload.get("boundary_flags", {})
    if nested is None:
        nested = {}
    _require(isinstance(nested, Mapping), "boundary_flags must be a mapping")

    for flag_name in RUNTIME_TRUE_BOUNDARY_FLAGS:
        if flag_name in payload:
            _require(payload[flag_name] is True, f"{flag_name} must be true")

    for flag_name in RUNTIME_FALSE_BOUNDARY_FLAGS:
        if flag_name in payload:
            _require(payload[flag_name] is False, f"{flag_name} must be false")
        if flag_name in nested:
            _require(nested[flag_name] is False, f"boundary_flags.{flag_name} must be false")

    merged = {flag_name: False for flag_name in RUNTIME_FALSE_BOUNDARY_FLAGS}
    payload["boundary_flags"] = merged
    payload["paper_only"] = True
    payload["advisory_only"] = True
    payload["human_in_the_loop"] = True
    payload["proposals_reviewable"] = True
    payload["proposals_auto_applied"] = False
    payload["losing_outcomes_remain_visible"] = True
    payload["historical_recommendations_overwritten"] = False
    return merged


def _validate_order_basics(payload: dict[str, Any]) -> dict[str, Any]:
    portfolio_id = _non_empty_string(payload, "portfolio_id")
    _require(
        PORTFOLIO_ID_PATTERN.fullmatch(portfolio_id) is not None,
        "portfolio_id must use 3-64 URL-safe characters: letters, numbers, dot, underscore, colon, or hyphen",
    )
    symbol = _non_empty_string(payload, "symbol").upper()
    _require(HK_SYMBOL_PATTERN.fullmatch(symbol) is not None, "symbol must use conservative HK ticker format like 0700.HK")

    side = _non_empty_string(payload, "side").lower()
    _require(side in VALID_ORDER_SIDES, "side must be buy or sell")

    quantity = _number(payload, "quantity")
    _require(quantity > 0, "quantity must be positive")

    order_type = str(payload.get("order_type", "market")).strip().lower()
    _require(order_type in VALID_ORDER_TYPES, "order_type must be market or limit")
    limit_price = payload.get("limit_price")
    if limit_price is not None:
        _require(isinstance(limit_price, (int, float)) and not isinstance(limit_price, bool), "limit_price must be numeric")
        _require(limit_price >= 0, "limit_price must be non-negative")

    base_currency = str(payload.get("base_currency", "HKD")).strip().upper() or "HKD"
    return {
        "portfolio_id": portfolio_id,
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "order_type": order_type,
        "limit_price": limit_price,
        "base_currency": base_currency,
    }


def _learning_proposal_preview(payload: Mapping[str, Any], sequence: int) -> dict[str, Any] | None:
    if payload["simulation_origin"] != "system_generated_learning":
        return None
    supplied = payload.get("learning_proposal")
    supplied_summary = supplied if isinstance(supplied, Mapping) else {}
    return {
        "learning_proposal_preview_id": f"learning-proposal-preview-{sequence:06d}",
        "proposal_type": "reviewable_learning_proposal_preview",
        "requires_human_review": True,
        "auto_apply": False,
        "status": "preview_only_not_applied",
        "source_recommendation_id": payload.get("source_recommendation_id"),
        "system_learning_reason": payload.get("system_learning_reason"),
        "improvement_suggestions": deepcopy(payload.get("improvement_suggestions")),
        "supplied_preview_summary": deepcopy(dict(supplied_summary)),
    }


def _validate_system_learning_details(payload: Mapping[str, Any]) -> None:
    if payload["simulation_origin"] != "system_generated_learning":
        return

    original_scores = payload.get("original_scores")
    _require(isinstance(original_scores, Mapping), "original_scores must be a mapping")
    for score_name, score_value in original_scores.items():
        _require(
            isinstance(score_value, (int, float)) and not isinstance(score_value, bool),
            f"original_scores.{score_name} must be numeric",
        )
        _require(0 <= score_value <= 100, f"original_scores.{score_name} must be between 0 and 100")

    pnl = payload.get("pnl")
    _require(isinstance(pnl, (int, float)) and not isinstance(pnl, bool), "pnl must be numeric")


def validate_paper_order_request(request: PaperOrderRequest | Mapping[str, Any]) -> dict[str, Any]:
    payload = _as_payload(request)
    normalized = deepcopy(payload)
    basics = _validate_order_basics(normalized)
    _merge_boundary_flags(normalized)

    if "simulation_origin" not in normalized or normalized.get("simulation_origin") is None:
        raise SimulationRuntimeValidationError("simulation_origin is required")
    try:
        origin_validation = validate_simulation_origin_payload(normalized)
    except ValueError as exc:
        raise SimulationRuntimeValidationError(str(exc)) from exc

    normalized.update(basics)
    _validate_system_learning_details(normalized)
    normalized["origin_validation"] = origin_validation
    return normalized


def create_paper_order_record(
    request: PaperOrderRequest | Mapping[str, Any],
    *,
    store: InMemorySimulationStore = simulation_store,
) -> dict[str, Any]:
    payload = validate_paper_order_request(request)
    sequence = store.next_sequence()
    timestamp = store.timestamp_for(sequence)
    paper_order_id = f"paper-order-{sequence:06d}"
    audit_event_id = f"audit-event-preview-{sequence:06d}"

    audit_event_preview = {
        "audit_event_id": audit_event_id,
        "event_type": "create_paper_order",
        "entity_type": "paper_order",
        "entity_id": paper_order_id,
        "actor_type": payload["created_by_type"],
        "origin": payload["simulation_origin"],
        "timestamp": timestamp,
        "persistence_write_performed": False,
        "preview_only": True,
    }
    learning_proposal = _learning_proposal_preview(payload, sequence)

    record = {
        "paper_order_id": paper_order_id,
        "record_type": "paper_order_record",
        "portfolio_id": payload["portfolio_id"],
        "base_currency": payload["base_currency"],
        "symbol": payload["symbol"],
        "side": payload["side"],
        "quantity": payload["quantity"],
        "order_type": payload["order_type"],
        "limit_price": payload["limit_price"],
        "simulation_origin": payload["simulation_origin"],
        "created_by_type": payload["created_by_type"],
        "created_at": timestamp,
        "status": "recorded_in_memory_only",
        "paper_only": True,
        "advisory_only": True,
        "human_in_the_loop": True,
        **{flag_name: False for flag_name in RUNTIME_FALSE_BOUNDARY_FLAGS},
        "boundary_flags": {flag_name: False for flag_name in RUNTIME_FALSE_BOUNDARY_FLAGS},
        "proposals_reviewable": True,
        "proposals_auto_applied": False,
        "losing_outcomes_remain_visible": True,
        "historical_recommendations_overwritten": False,
        "historical_recommendation_fields": {
            "strategy_recommendation_id": payload.get("strategy_recommendation_id"),
            "source_recommendation_id": payload.get("source_recommendation_id"),
            "original_recommendation": payload.get("original_recommendation"),
            "original_scores": deepcopy(payload.get("original_scores")),
            "original_thesis": payload.get("original_thesis"),
        },
        "outcome_preview": {
            "pnl": deepcopy(payload.get("pnl")),
            "holding_period": payload.get("holding_period"),
            "losing_outcome_visible": True,
        },
        "source_metadata": {
            "user_id": payload.get("user_id"),
            "source_actor": payload.get("source_actor"),
            "user_recorded_notes": payload.get("user_recorded_notes"),
            "user_decision_rationale": payload.get("user_decision_rationale"),
            "system_learning_reason": payload.get("system_learning_reason"),
            "entry_assumptions": deepcopy(payload.get("entry_assumptions")),
            "exit_assumptions": deepcopy(payload.get("exit_assumptions")),
            "what_worked": deepcopy(payload.get("what_worked")),
            "what_failed": deepcopy(payload.get("what_failed")),
            "improvement_suggestions": deepcopy(payload.get("improvement_suggestions")),
            "requires_human_review": payload.get("requires_human_review"),
        },
        "audit_event_preview": audit_event_preview,
        "learning_proposal_preview": learning_proposal,
    }
    store.create_paper_order(record, audit_event_preview)
    return {"paper_order": deepcopy(record), "audit_event_preview": audit_event_preview, "learning_proposal_preview": learning_proposal}


def build_paper_portfolio_snapshot(
    portfolio_id: str,
    *,
    store: InMemorySimulationStore = simulation_store,
) -> dict[str, Any]:
    _require(isinstance(portfolio_id, str) and portfolio_id.strip() != "", "portfolio_id must be present")
    normalized_portfolio_id = portfolio_id.strip()
    _require(
        PORTFOLIO_ID_PATTERN.fullmatch(normalized_portfolio_id) is not None,
        "portfolio_id must use 3-64 URL-safe characters: letters, numbers, dot, underscore, colon, or hyphen",
    )
    records = store.get_portfolio_snapshot_records(normalized_portfolio_id)
    if records is None:
        raise SimulationRuntimeValidationError("paper portfolio not found")
    orders, audits = records
    base_currency = orders[-1].get("base_currency", "HKD") if orders else "HKD"
    return {
        "portfolio_id": normalized_portfolio_id,
        "record_type": "paper_portfolio_snapshot",
        "status": "in_memory_only_non_production",
        "base_currency": base_currency,
        "cash_placeholder": {"amount": 0, "currency": base_currency, "source": "placeholder_not_broker_cash"},
        "nav_placeholder": {"amount": 0, "currency": base_currency, "source": "placeholder_not_market_valuation"},
        "recent_paper_orders": orders[-20:],
        "audit_event_previews": audits[-20:],
        "paper_only": True,
        "advisory_only": True,
        "human_in_the_loop": True,
        **{flag_name: False for flag_name in RUNTIME_FALSE_BOUNDARY_FLAGS},
        "boundary_flags": {flag_name: False for flag_name in RUNTIME_FALSE_BOUNDARY_FLAGS},
    }
