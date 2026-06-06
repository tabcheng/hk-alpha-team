from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

SimulationOriginPayload = dict[str, Any]

USER_RECORDED_ORIGIN = "user_recorded"
SYSTEM_GENERATED_LEARNING_ORIGIN = "system_generated_learning"
ALLOWED_SIMULATION_ORIGINS = (
    USER_RECORDED_ORIGIN,
    SYSTEM_GENERATED_LEARNING_ORIGIN,
)

SIMULATION_ORIGIN_BOUNDARY_FLAGS = (
    "real_money_order_placed",
    "real_money_trading_automation_enabled",
    "autonomous_real_money_execution",
    "broker_execution_enabled",
    "broker_api_called",
    "production_supabase_connected",
    "secrets_required",
)

LEARNING_PROPOSAL_BEHAVIOR = {
    "proposals_reviewable": True,
    "proposals_auto_applied": False,
}

LOSS_VISIBILITY_BEHAVIOR = {
    "losing_outcomes_remain_visible": True,
    "historical_recommendations_overwritten": False,
}

COMMON_REQUIRED_FIELDS = (
    "simulation_origin",
    "created_by_type",
    "portfolio_id",
    "symbol",
    "advisory_only",
    "human_in_the_loop",
)

USER_RECORDED_REQUIRED_FIELDS = (
    "user_id",
    "user_recorded_notes",
    "user_decision_rationale",
    "paper_order_origin",
)

SYSTEM_GENERATED_LEARNING_REQUIRED_FIELDS = (
    "source_recommendation_id",
    "original_recommendation_label",
    "original_scores",
    "original_thesis",
    "entry_assumptions",
    "exit_assumptions",
    "system_learning_reason",
    "requires_human_review",
)

ORIGIN_CREATED_BY_TYPE = {
    USER_RECORDED_ORIGIN: "human_user",
    SYSTEM_GENERATED_LEARNING_ORIGIN: "simulation_investment_desk",
}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"Simulation origin contract validation failed: {message}")


def _require_mapping(value: object, field_name: str) -> Mapping[str, object]:
    _require(isinstance(value, Mapping), f"{field_name} must be a mapping")
    return value


def _require_non_empty_string(value: object, field_name: str) -> str:
    _require(isinstance(value, str), f"{field_name} must be a string")
    stripped = value.strip()
    _require(stripped != "", f"{field_name} must be present")
    return stripped


def _require_bool(value: object, field_name: str, expected: bool) -> bool:
    _require(isinstance(value, bool), f"{field_name} must be a boolean")
    _require(value is expected, f"{field_name} must be {expected}")
    return value


def _require_fields(payload: Mapping[str, object], fields: tuple[str, ...]) -> None:
    for field_name in fields:
        _require(field_name in payload, f"{field_name} is required")


def _require_boundary_flags(payload: Mapping[str, object]) -> dict[str, bool]:
    flags = {flag_name: False for flag_name in SIMULATION_ORIGIN_BOUNDARY_FLAGS}
    nested_flags = payload.get("boundary_flags")
    if nested_flags is not None:
        nested = _require_mapping(nested_flags, "boundary_flags")
        for flag_name in SIMULATION_ORIGIN_BOUNDARY_FLAGS:
            if flag_name in nested:
                _require(nested[flag_name] is False, f"{flag_name} must remain false")
    for flag_name in SIMULATION_ORIGIN_BOUNDARY_FLAGS:
        if flag_name in payload:
            _require(payload[flag_name] is False, f"{flag_name} must remain false")
    return flags


def _require_learning_behavior(payload: Mapping[str, object]) -> dict[str, bool]:
    proposals_reviewable = payload.get("proposals_reviewable", True)
    proposals_auto_applied = payload.get("proposals_auto_applied", False)
    if "proposals_auto_applied" in payload:
        _require(payload["proposals_auto_applied"] is False, "proposals_auto_applied must be false")
    if "proposals_reviewable" in payload:
        _require(payload["proposals_reviewable"] is True, "proposals_reviewable must be true")
    if "learning_proposal" in payload:
        learning_proposal = _require_mapping(payload["learning_proposal"], "learning_proposal")
        proposals_reviewable = learning_proposal.get("proposals_reviewable", proposals_reviewable)
        proposals_auto_applied = learning_proposal.get("proposals_auto_applied", proposals_auto_applied)
        if "auto_apply" in learning_proposal:
            _require(learning_proposal["auto_apply"] is False, "learning proposal auto_apply must be false")
    if "auto_apply" in payload:
        _require(payload["auto_apply"] is False, "learning proposal auto_apply must be false")
    _require(proposals_reviewable is True, "proposals_reviewable must be true")
    _require(proposals_auto_applied is False, "proposals_auto_applied must be false")
    return {
        "proposals_reviewable": True,
        "proposals_auto_applied": False,
    }


def _require_loss_visibility(payload: Mapping[str, object]) -> dict[str, bool]:
    losing_visible = payload.get("losing_outcomes_remain_visible", True)
    historical_overwritten = payload.get("historical_recommendations_overwritten", False)
    _require(losing_visible is True, "losing_outcomes_remain_visible must be true")
    _require(
        historical_overwritten is False,
        "historical_recommendations_overwritten must be false",
    )
    return {
        "losing_outcomes_remain_visible": True,
        "historical_recommendations_overwritten": False,
    }


def _validate_user_recorded(payload: Mapping[str, object]) -> dict[str, object]:
    _require_fields(payload, USER_RECORDED_REQUIRED_FIELDS)
    _require_non_empty_string(payload.get("user_id"), "user_id")
    _require_non_empty_string(payload.get("user_recorded_notes"), "user_recorded_notes")
    _require_non_empty_string(payload.get("user_decision_rationale"), "user_decision_rationale")
    paper_order_origin = _require_non_empty_string(payload.get("paper_order_origin"), "paper_order_origin")
    _require(paper_order_origin == USER_RECORDED_ORIGIN, "paper_order_origin must be user_recorded")
    source_recommendation_id = payload.get("source_recommendation_id")
    if source_recommendation_id is not None:
        _require_non_empty_string(source_recommendation_id, "source_recommendation_id")
    return {
        "user_recorded_notes": payload["user_recorded_notes"],
        "source_recommendation_id": source_recommendation_id,
    }


def _validate_system_generated_learning(payload: Mapping[str, object]) -> dict[str, object]:
    _require_fields(payload, SYSTEM_GENERATED_LEARNING_REQUIRED_FIELDS)
    for field_name in (
        "source_recommendation_id",
        "original_recommendation_label",
        "original_thesis",
        "system_learning_reason",
    ):
        _require_non_empty_string(payload.get(field_name), field_name)
    _require_mapping(payload.get("original_scores"), "original_scores")
    _require_mapping(payload.get("entry_assumptions"), "entry_assumptions")
    _require_mapping(payload.get("exit_assumptions"), "exit_assumptions")
    _require_bool(payload.get("requires_human_review"), "requires_human_review", True)
    if "learning_proposal_id" in payload:
        _require_non_empty_string(payload.get("learning_proposal_id"), "learning_proposal_id")
    return {
        "source_recommendation_id": payload["source_recommendation_id"],
        "requires_human_review": True,
        "learning_proposal_id": payload.get("learning_proposal_id"),
    }


def validate_simulation_origin_payload(payload: Mapping[str, object]) -> dict[str, object]:
    """Validate Task 008G dual-origin Simulation Desk payloads without IO or mutation."""

    _require(isinstance(payload, Mapping), "payload must be a mapping")
    before_validation = deepcopy(dict(payload))
    _require_fields(payload, COMMON_REQUIRED_FIELDS)

    simulation_origin = _require_non_empty_string(payload.get("simulation_origin"), "simulation_origin")
    _require(
        simulation_origin in ALLOWED_SIMULATION_ORIGINS,
        "simulation_origin must be user_recorded or system_generated_learning",
    )
    created_by_type = _require_non_empty_string(payload.get("created_by_type"), "created_by_type")
    _require(
        created_by_type == ORIGIN_CREATED_BY_TYPE[simulation_origin],
        f"created_by_type must be {ORIGIN_CREATED_BY_TYPE[simulation_origin]} for {simulation_origin}",
    )
    _require_non_empty_string(payload.get("portfolio_id"), "portfolio_id")
    _require_non_empty_string(payload.get("symbol"), "symbol")
    _require_bool(payload.get("advisory_only"), "advisory_only", True)
    _require_bool(payload.get("human_in_the_loop"), "human_in_the_loop", True)

    origin_details = (
        _validate_user_recorded(payload)
        if simulation_origin == USER_RECORDED_ORIGIN
        else _validate_system_generated_learning(payload)
    )
    boundary_flags = _require_boundary_flags(payload)
    learning_behavior = _require_learning_behavior(payload)
    loss_visibility = _require_loss_visibility(payload)

    _require(dict(payload) == before_validation, "validation must not mutate the input payload")

    return {
        "validation_status": "passed",
        "simulation_origin": simulation_origin,
        "created_by_type": created_by_type,
        "canonical_schema_table": "paper_orders",
        "locked_endpoint_reference": "POST /api/v1/simulation/paper-orders",
        "advisory_only": True,
        "human_in_the_loop": True,
        **origin_details,
        **boundary_flags,
        **learning_behavior,
        **loss_visibility,
    }


def build_simulation_origin_sample_payload(origin: str) -> SimulationOriginPayload:
    """Return deterministic local-only sample payloads for either Task 008G origin."""

    _require(origin in ALLOWED_SIMULATION_ORIGINS, "origin must be user_recorded or system_generated_learning")
    common: SimulationOriginPayload = {
        "simulation_origin": origin,
        "created_by_type": ORIGIN_CREATED_BY_TYPE[origin],
        "portfolio_id": "fixture-paper-portfolio-001",
        "symbol": "0700.HK",
        "advisory_only": True,
        "human_in_the_loop": True,
        "boundary_flags": {flag_name: False for flag_name in SIMULATION_ORIGIN_BOUNDARY_FLAGS},
        **LEARNING_PROPOSAL_BEHAVIOR,
        **LOSS_VISIBILITY_BEHAVIOR,
    }
    if origin == USER_RECORDED_ORIGIN:
        common.update(
            {
                "paper_order_origin": USER_RECORDED_ORIGIN,
                "user_id": "harness-engineering-user",
                "user_recorded_notes": "Human-entered paper trade note for review.",
                "user_decision_rationale": "Harness Engineering recorded the paper decision manually.",
                "source_recommendation_id": "strategy-rec-optional-001",
            }
        )
        return common

    common.update(
        {
            "source_recommendation_id": "strategy-rec-008g-001",
            "original_recommendation_label": "SMALL_POSITION",
            "original_scores": {
                "market_score": 68,
                "fundamental_score": 72,
                "technical_score": 61,
                "sentiment_score": 58,
                "risk_score": 54,
                "simulation_score": 0,
            },
            "original_thesis": "Approved recommendation packet requires paper-trading validation.",
            "entry_assumptions": {"entry_price": 375.5, "entry_rule": "fixture limit assumption"},
            "exit_assumptions": {"exit_rule": "review after invalidation or target window"},
            "system_learning_reason": "Validate recommendation quality and capture reviewable learning.",
            "requires_human_review": True,
            "learning_proposal_id": "learning-proposal-008g-001",
            "learning_proposal": {
                "proposals_reviewable": True,
                "proposals_auto_applied": False,
                "auto_apply": False,
            },
        }
    )
    return common


def build_simulation_origin_sample_payloads() -> dict[str, SimulationOriginPayload]:
    """Return deterministic samples keyed by allowed origin."""

    return {
        origin: build_simulation_origin_sample_payload(origin)
        for origin in ALLOWED_SIMULATION_ORIGINS
    }
