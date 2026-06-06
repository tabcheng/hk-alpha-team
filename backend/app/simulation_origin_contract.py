from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

ALLOWED_SIMULATION_ORIGINS = (
    "user_recorded",
    "system_generated_learning",
)

SIMULATION_ORIGIN_ENDPOINT_REFERENCE = "POST /api/v1/simulation/paper-orders"

BOUNDARY_FLAGS = (
    "real_money_order_placed",
    "real_money_trading_automation_enabled",
    "autonomous_real_money_execution",
    "broker_execution_enabled",
    "broker_api_called",
    "production_supabase_connected",
    "secrets_required",
)

LEARNING_PROPOSAL_FLAGS = {
    "proposals_reviewable": True,
    "proposals_auto_applied": False,
}

LOSS_VISIBILITY_FLAGS = {
    "losing_outcomes_remain_visible": True,
    "historical_recommendations_overwritten": False,
}

COMMON_REQUIRED_FIELDS = (
    "simulation_origin",
    "created_by_type",
    "advisory_only",
    "human_in_the_loop",
)

USER_RECORDED_REQUIRED_FIELDS = (
    "user_id",
    "user_recorded_notes",
    "user_decision_rationale",
    "source_actor",
)

SYSTEM_GENERATED_LEARNING_REQUIRED_FIELDS = (
    "strategy_recommendation_id",
    "source_recommendation_id",
    "original_recommendation",
    "original_scores",
    "original_thesis",
    "entry_assumptions",
    "exit_assumptions",
    "pnl",
    "holding_period",
    "what_worked",
    "what_failed",
    "improvement_suggestions",
    "system_learning_reason",
    "requires_human_review",
)

USER_CREATED_BY_TYPES = {"human", "harness_engineering", "user"}
SYSTEM_CREATED_BY_TYPES = {"system", "simulation_investment_desk", "hk_alpha_team"}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"Simulation origin contract validation failed: {message}")


def _require_present(payload: Mapping[str, Any], field_name: str) -> Any:
    _require(field_name in payload, f"{field_name} is required")
    value = payload[field_name]
    if isinstance(value, str):
        _require(value.strip() != "", f"{field_name} must be non-empty")
    elif isinstance(value, (list, tuple, dict, set)):
        _require(len(value) > 0, f"{field_name} must be non-empty")
    else:
        _require(value is not None, f"{field_name} must be present")
    return value


def _require_boolean_field(payload: Mapping[str, Any], field_name: str, expected: bool) -> None:
    _require_present(payload, field_name)
    _require(
        payload[field_name] is expected,
        f"{field_name} must be {str(expected).lower()}",
    )


def _validate_boundary_flags(payload: Mapping[str, Any]) -> dict[str, bool]:
    nested_flags = payload.get("boundary_flags")
    _require(isinstance(nested_flags, Mapping), "boundary_flags must be a mapping")

    for flag_name in BOUNDARY_FLAGS:
        _require(flag_name in nested_flags, f"boundary_flags.{flag_name} is required")
        _require(
            nested_flags[flag_name] is False,
            f"boundary_flags.{flag_name} must be false",
        )
        if flag_name in payload:
            _require(
                payload[flag_name] is False,
                f"{flag_name} must be false",
            )

    return {flag_name: False for flag_name in BOUNDARY_FLAGS}


def _validate_learning_proposal_behavior(payload: Mapping[str, Any]) -> dict[str, bool]:
    for flag_name, expected in LEARNING_PROPOSAL_FLAGS.items():
        _require_boolean_field(payload, flag_name, expected)

    if "learning_proposal" in payload:
        proposal = payload["learning_proposal"]
        _require(isinstance(proposal, Mapping), "learning_proposal must be a mapping")
        _require(
            proposal.get("requires_human_review") is True,
            "learning_proposal.requires_human_review must be true",
        )
        _require(
            proposal.get("auto_apply") is False,
            "learning_proposal.auto_apply must be false",
        )

    if "learning_proposal_auto_apply" in payload:
        _require(
            payload["learning_proposal_auto_apply"] is False,
            "learning_proposal_auto_apply must be false",
        )

    return deepcopy(LEARNING_PROPOSAL_FLAGS)


def _validate_loss_visibility_behavior(payload: Mapping[str, Any]) -> dict[str, bool]:
    for flag_name, expected in LOSS_VISIBILITY_FLAGS.items():
        _require_boolean_field(payload, flag_name, expected)
    return deepcopy(LOSS_VISIBILITY_FLAGS)


def _validate_common_payload(payload: Mapping[str, Any]) -> str:
    _require(isinstance(payload, Mapping), "payload must be a mapping")
    for field_name in COMMON_REQUIRED_FIELDS:
        _require_present(payload, field_name)

    origin = str(payload["simulation_origin"])
    _require(
        origin in ALLOWED_SIMULATION_ORIGINS,
        "simulation_origin must be user_recorded or system_generated_learning",
    )
    _require(payload["advisory_only"] is True, "advisory_only must be true")
    _require(payload["human_in_the_loop"] is True, "human_in_the_loop must be true")
    _validate_boundary_flags(payload)
    _validate_learning_proposal_behavior(payload)
    _validate_loss_visibility_behavior(payload)
    return origin


def _validate_user_recorded(payload: Mapping[str, Any]) -> None:
    for field_name in USER_RECORDED_REQUIRED_FIELDS:
        _require_present(payload, field_name)
    _require(
        payload["created_by_type"] in USER_CREATED_BY_TYPES,
        "created_by_type must identify a human/user source for user_recorded payloads",
    )


def _validate_system_generated_learning(payload: Mapping[str, Any]) -> None:
    for field_name in SYSTEM_GENERATED_LEARNING_REQUIRED_FIELDS:
        _require_present(payload, field_name)
    _require(
        payload["created_by_type"] in SYSTEM_CREATED_BY_TYPES,
        "created_by_type must identify a system source for system_generated_learning payloads",
    )
    _require(
        payload["requires_human_review"] is True,
        "requires_human_review must be true for system_generated_learning payloads",
    )


def validate_simulation_origin_payload(payload: Mapping[str, Any]) -> dict[str, Any]:
    """Validate a Simulation Desk origin payload without IO, persistence, or mutation."""

    _require(isinstance(payload, Mapping), "payload must be a mapping")
    before_validation = deepcopy(dict(payload))
    origin = _validate_common_payload(payload)
    if origin == "user_recorded":
        _validate_user_recorded(payload)
    else:
        _validate_system_generated_learning(payload)

    _require(dict(payload) == before_validation, "validation must not mutate input payload")

    return {
        "validation_status": "passed",
        "simulation_origin": origin,
        "allowed_simulation_origins": list(ALLOWED_SIMULATION_ORIGINS),
        "endpoint_reference": SIMULATION_ORIGIN_ENDPOINT_REFERENCE,
        "advisory_only": True,
        "human_in_the_loop": True,
        "boundary_flags": _validate_boundary_flags(payload),
        "learning_proposal_behavior": _validate_learning_proposal_behavior(payload),
        "loss_visibility_behavior": _validate_loss_visibility_behavior(payload),
    }


def _common_sample_fields(origin: str, created_by_type: str) -> dict[str, Any]:
    return {
        "simulation_origin": origin,
        "created_by_type": created_by_type,
        "advisory_only": True,
        "human_in_the_loop": True,
        "boundary_flags": {flag_name: False for flag_name in BOUNDARY_FLAGS},
        **LEARNING_PROPOSAL_FLAGS,
        **LOSS_VISIBILITY_FLAGS,
    }


def build_sample_simulation_origin_payload(origin: str) -> dict[str, Any]:
    """Build a deterministic sample payload for either approved simulation origin."""

    _require(
        origin in ALLOWED_SIMULATION_ORIGINS,
        "origin must be user_recorded or system_generated_learning",
    )

    if origin == "user_recorded":
        return {
            **_common_sample_fields("user_recorded", "harness_engineering"),
            "user_id": "harness-engineering",
            "source_actor": "Harness Engineering",
            "portfolio_id": "fixture-paper-portfolio-001",
            "symbol": "0700.HK",
            "side": "buy",
            "quantity": 100,
            "user_recorded_notes": "Human-recorded paper trade journal entry.",
            "user_decision_rationale": "Harness Engineering recorded a paper-only decision for review.",
            "strategy_recommendation_id": "fixture-strategy-recommendation-001",
        }

    return {
        **_common_sample_fields("system_generated_learning", "simulation_investment_desk"),
        "portfolio_id": "fixture-paper-portfolio-001",
        "symbol": "0700.HK",
        "side": "buy",
        "quantity": 100,
        "strategy_recommendation_id": "fixture-strategy-recommendation-001",
        "source_recommendation_id": "fixture-strategy-recommendation-001",
        "original_recommendation": "WAIT_FOR_PULLBACK",
        "original_scores": {
            "market_score": 52,
            "fundamental_score": 48,
            "technical_score": 44,
            "sentiment_score": 46,
            "risk_score": 42,
            "simulation_score": 49,
        },
        "original_thesis": "Local deterministic thesis retained for simulation learning review.",
        "entry_assumptions": "Paper entry assumes reviewed recommendation packet and local-only price fixture.",
        "exit_assumptions": "Paper exit assumes predetermined review window and no real execution.",
        "pnl": -1550.0,
        "holding_period": "5 trading days",
        "what_worked": ["Risk remained paper-only and bounded."],
        "what_failed": ["Entry timing did not wait for stronger pullback confirmation."],
        "improvement_suggestions": ["Require clearer pullback evidence before similar simulations."],
        "system_learning_reason": "Validate recommendation quality and produce reviewable learning proposal.",
        "requires_human_review": True,
        "learning_proposal_id": "fixture-learning-proposal-001",
        "learning_proposal": {
            "proposal_id": "fixture-learning-proposal-001",
            "requires_human_review": True,
            "auto_apply": False,
        },
    }


def build_sample_simulation_origin_payloads() -> dict[str, dict[str, Any]]:
    """Return deterministic sample payloads keyed by approved origin."""

    return {
        origin: build_sample_simulation_origin_payload(origin)
        for origin in ALLOWED_SIMULATION_ORIGINS
    }
