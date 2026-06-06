from __future__ import annotations

from copy import deepcopy

import pytest

from app.simulation_origin_contract import (
    ALLOWED_SIMULATION_ORIGINS,
    SIMULATION_ORIGIN_BOUNDARY_FLAGS,
    SYSTEM_GENERATED_LEARNING_ORIGIN,
    USER_RECORDED_ORIGIN,
    build_simulation_origin_sample_payload,
    build_simulation_origin_sample_payloads,
    validate_simulation_origin_payload,
)


def _payload(origin: str) -> dict[str, object]:
    return build_simulation_origin_sample_payload(origin)


def test_task_008g_user_recorded_payload_validates_successfully() -> None:
    result = validate_simulation_origin_payload(_payload(USER_RECORDED_ORIGIN))

    assert result["validation_status"] == "passed"
    assert result["simulation_origin"] == "user_recorded"
    assert result["created_by_type"] == "human_user"
    assert result["canonical_schema_table"] == "paper_orders"


def test_task_008g_system_generated_learning_payload_validates_successfully() -> None:
    result = validate_simulation_origin_payload(_payload(SYSTEM_GENERATED_LEARNING_ORIGIN))

    assert result["validation_status"] == "passed"
    assert result["simulation_origin"] == "system_generated_learning"
    assert result["created_by_type"] == "simulation_investment_desk"
    assert result["source_recommendation_id"] == "strategy-rec-008g-001"


def test_task_008g_deterministic_samples_cover_both_origins() -> None:
    payloads = build_simulation_origin_sample_payloads()

    assert tuple(payloads) == ALLOWED_SIMULATION_ORIGINS
    assert set(payloads) == {"user_recorded", "system_generated_learning"}


def test_task_008g_invalid_origin_fails() -> None:
    payload = _payload(USER_RECORDED_ORIGIN)
    payload["simulation_origin"] = "paper_journal_only"

    with pytest.raises(ValueError, match="simulation_origin must be user_recorded or system_generated_learning"):
        validate_simulation_origin_payload(payload)


@pytest.mark.parametrize(
    "field_name",
    ["user_id", "user_recorded_notes", "user_decision_rationale", "paper_order_origin"],
)
def test_task_008g_user_recorded_payload_requires_user_source_fields(field_name: str) -> None:
    payload = _payload(USER_RECORDED_ORIGIN)
    payload.pop(field_name)

    with pytest.raises(ValueError, match=f"{field_name} is required"):
        validate_simulation_origin_payload(payload)


@pytest.mark.parametrize(
    "field_name",
    [
        "source_recommendation_id",
        "original_recommendation_label",
        "original_scores",
        "original_thesis",
        "entry_assumptions",
        "exit_assumptions",
        "system_learning_reason",
    ],
)
def test_task_008g_system_generated_learning_requires_original_linkage_fields(field_name: str) -> None:
    payload = _payload(SYSTEM_GENERATED_LEARNING_ORIGIN)
    payload.pop(field_name)

    with pytest.raises(ValueError, match=f"{field_name} is required"):
        validate_simulation_origin_payload(payload)


def test_task_008g_system_generated_learning_learning_proposal_requires_human_review() -> None:
    payload = _payload(SYSTEM_GENERATED_LEARNING_ORIGIN)
    payload["learning_proposal_id"] = "learning-proposal-reviewable-002"
    payload["requires_human_review"] = True

    result = validate_simulation_origin_payload(payload)

    assert result["requires_human_review"] is True
    assert result["learning_proposal_id"] == "learning-proposal-reviewable-002"
    assert result["proposals_reviewable"] is True
    assert result["proposals_auto_applied"] is False


def test_task_008g_system_generated_learning_requires_human_review_true() -> None:
    payload = _payload(SYSTEM_GENERATED_LEARNING_ORIGIN)
    payload["requires_human_review"] = False

    with pytest.raises(ValueError, match="requires_human_review must be True"):
        validate_simulation_origin_payload(payload)


@pytest.mark.parametrize(
    "auto_apply_payload",
    [
        {"auto_apply": True},
        {"learning_proposal": {"proposals_reviewable": True, "proposals_auto_applied": False, "auto_apply": True}},
        {"proposals_auto_applied": True},
    ],
)
def test_task_008g_learning_proposal_auto_apply_true_fails(auto_apply_payload: dict[str, object]) -> None:
    payload = _payload(SYSTEM_GENERATED_LEARNING_ORIGIN)
    payload.update(auto_apply_payload)

    with pytest.raises(ValueError, match="auto_apply|proposals_auto_applied"):
        validate_simulation_origin_payload(payload)


@pytest.mark.parametrize(
    "flag_name",
    [
        "real_money_order_placed",
        "real_money_trading_automation_enabled",
        "broker_execution_enabled",
        "broker_api_called",
        "production_supabase_connected",
        "secrets_required",
    ],
)
def test_task_008g_forbidden_top_level_boundary_flags_true_fail(flag_name: str) -> None:
    assert flag_name in SIMULATION_ORIGIN_BOUNDARY_FLAGS
    payload = _payload(USER_RECORDED_ORIGIN)
    payload[flag_name] = True

    with pytest.raises(ValueError, match=f"{flag_name} must remain false"):
        validate_simulation_origin_payload(payload)


def test_task_008g_autonomous_real_money_execution_true_fails() -> None:
    payload = _payload(SYSTEM_GENERATED_LEARNING_ORIGIN)
    payload["boundary_flags"]["autonomous_real_money_execution"] = True  # type: ignore[index]

    with pytest.raises(ValueError, match="autonomous_real_money_execution must remain false"):
        validate_simulation_origin_payload(payload)


def test_task_008g_losing_outcomes_remain_visible_false_fails() -> None:
    payload = _payload(SYSTEM_GENERATED_LEARNING_ORIGIN)
    payload["losing_outcomes_remain_visible"] = False

    with pytest.raises(ValueError, match="losing_outcomes_remain_visible must be true"):
        validate_simulation_origin_payload(payload)


def test_task_008g_historical_recommendations_overwritten_true_fails() -> None:
    payload = _payload(SYSTEM_GENERATED_LEARNING_ORIGIN)
    payload["historical_recommendations_overwritten"] = True

    with pytest.raises(ValueError, match="historical_recommendations_overwritten must be false"):
        validate_simulation_origin_payload(payload)


@pytest.mark.parametrize("origin", ALLOWED_SIMULATION_ORIGINS)
def test_task_008g_validation_does_not_mutate_input_payloads(origin: str) -> None:
    payload = _payload(origin)
    before_validation = deepcopy(payload)

    validate_simulation_origin_payload(payload)

    assert payload == before_validation


@pytest.mark.parametrize("origin", ALLOWED_SIMULATION_ORIGINS)
def test_task_008g_both_origins_preserve_advisory_only_and_human_loop_framing(origin: str) -> None:
    result = validate_simulation_origin_payload(_payload(origin))

    assert result["advisory_only"] is True
    assert result["human_in_the_loop"] is True
    assert result["real_money_order_placed"] is False
    assert result["broker_execution_enabled"] is False
