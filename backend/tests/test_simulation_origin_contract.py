from __future__ import annotations

from copy import deepcopy

import pytest

from app.simulation_origin_contract import (
    ALLOWED_SIMULATION_ORIGINS,
    build_sample_simulation_origin_payload,
    build_sample_simulation_origin_payloads,
    validate_simulation_origin_payload,
)


def _payload(origin: str) -> dict[str, object]:
    return build_sample_simulation_origin_payload(origin)


def test_task_008g_user_recorded_payload_validates_successfully() -> None:
    result = validate_simulation_origin_payload(_payload("user_recorded"))

    assert result["validation_status"] == "passed"
    assert result["simulation_origin"] == "user_recorded"
    assert result["advisory_only"] is True
    assert result["human_in_the_loop"] is True


def test_task_008g_system_generated_learning_payload_validates_successfully() -> None:
    result = validate_simulation_origin_payload(_payload("system_generated_learning"))

    assert result["validation_status"] == "passed"
    assert result["simulation_origin"] == "system_generated_learning"
    assert result["learning_proposal_behavior"]["proposals_reviewable"] is True
    assert result["learning_proposal_behavior"]["proposals_auto_applied"] is False


def test_task_008g_deterministic_sample_builder_returns_both_origins() -> None:
    samples = build_sample_simulation_origin_payloads()

    assert tuple(samples) == ALLOWED_SIMULATION_ORIGINS
    assert samples["user_recorded"]["simulation_origin"] == "user_recorded"
    assert samples["system_generated_learning"]["simulation_origin"] == "system_generated_learning"


def test_task_008g_invalid_origin_fails() -> None:
    payload = _payload("user_recorded")
    payload["simulation_origin"] = "paper_journal"

    with pytest.raises(ValueError, match="simulation_origin"):
        validate_simulation_origin_payload(payload)


@pytest.mark.parametrize(
    "field_name",
    ["user_id", "source_actor", "user_recorded_notes", "user_decision_rationale"],
)
def test_task_008g_user_recorded_payload_requires_user_source_fields(field_name: str) -> None:
    payload = _payload("user_recorded")
    payload.pop(field_name)

    with pytest.raises(ValueError, match=field_name):
        validate_simulation_origin_payload(payload)


@pytest.mark.parametrize(
    "field_name",
    [
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
    ],
)
def test_task_008g_system_generated_learning_requires_recommendation_thesis_score_linkage_fields(
    field_name: str,
) -> None:
    payload = _payload("system_generated_learning")
    payload.pop(field_name)

    with pytest.raises(ValueError, match=field_name):
        validate_simulation_origin_payload(payload)


def test_task_008g_system_generated_learning_learning_proposal_requires_human_review() -> None:
    payload = _payload("system_generated_learning")
    payload["learning_proposal_id"] = "fixture-learning-proposal-002"
    payload["learning_proposal"] = {
        "proposal_id": "fixture-learning-proposal-002",
        "requires_human_review": True,
        "auto_apply": False,
    }

    result = validate_simulation_origin_payload(payload)

    assert result["simulation_origin"] == "system_generated_learning"


def test_task_008g_system_generated_learning_requires_human_review_false_fails() -> None:
    payload = _payload("system_generated_learning")
    payload["requires_human_review"] = False

    with pytest.raises(ValueError, match="requires_human_review"):
        validate_simulation_origin_payload(payload)


def test_task_008g_learning_proposal_auto_apply_true_fails() -> None:
    payload = _payload("system_generated_learning")
    payload["learning_proposal"]["auto_apply"] = True  # type: ignore[index]

    with pytest.raises(ValueError, match="auto_apply"):
        validate_simulation_origin_payload(payload)


def test_task_008g_learning_proposal_missing_review_flag_fails() -> None:
    payload = _payload("system_generated_learning")
    payload["learning_proposal"].pop("requires_human_review")  # type: ignore[union-attr]

    with pytest.raises(ValueError, match="learning_proposal.requires_human_review"):
        validate_simulation_origin_payload(payload)


def test_task_008g_learning_proposal_missing_auto_apply_flag_fails() -> None:
    payload = _payload("system_generated_learning")
    payload["learning_proposal"].pop("auto_apply")  # type: ignore[union-attr]

    with pytest.raises(ValueError, match="learning_proposal.auto_apply"):
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
def test_task_008g_forbidden_boundary_flag_true_fails(flag_name: str) -> None:
    payload = _payload("system_generated_learning")
    payload[flag_name] = True

    with pytest.raises(ValueError, match=flag_name):
        validate_simulation_origin_payload(payload)


def test_task_008g_autonomous_real_money_execution_true_fails() -> None:
    payload = _payload("system_generated_learning")
    payload["autonomous_real_money_execution"] = True

    with pytest.raises(ValueError, match="autonomous_real_money_execution"):
        validate_simulation_origin_payload(payload)


def test_task_008g_missing_boundary_flags_mapping_fails() -> None:
    payload = _payload("system_generated_learning")
    payload.pop("boundary_flags")

    with pytest.raises(ValueError, match="boundary_flags"):
        validate_simulation_origin_payload(payload)


def test_task_008g_missing_required_boundary_flag_fails() -> None:
    payload = _payload("system_generated_learning")
    payload["boundary_flags"].pop("broker_api_called")  # type: ignore[union-attr]

    with pytest.raises(ValueError, match="boundary_flags.broker_api_called"):
        validate_simulation_origin_payload(payload)


def test_task_008g_nested_boundary_flag_true_fails() -> None:
    payload = _payload("system_generated_learning")
    payload["boundary_flags"]["broker_api_called"] = True  # type: ignore[index]

    with pytest.raises(ValueError, match="boundary_flags.broker_api_called"):
        validate_simulation_origin_payload(payload)


def test_task_008g_missing_learning_proposal_behavior_flags_fail() -> None:
    payload = _payload("system_generated_learning")
    payload.pop("proposals_reviewable")

    with pytest.raises(ValueError, match="proposals_reviewable"):
        validate_simulation_origin_payload(payload)


def test_task_008g_missing_loss_visibility_flags_fail() -> None:
    payload = _payload("system_generated_learning")
    payload.pop("losing_outcomes_remain_visible")

    with pytest.raises(ValueError, match="losing_outcomes_remain_visible"):
        validate_simulation_origin_payload(payload)


def test_task_008g_losing_outcomes_remain_visible_false_fails() -> None:
    payload = _payload("system_generated_learning")
    payload["losing_outcomes_remain_visible"] = False

    with pytest.raises(ValueError, match="losing_outcomes_remain_visible"):
        validate_simulation_origin_payload(payload)


def test_task_008g_historical_recommendations_overwritten_true_fails() -> None:
    payload = _payload("system_generated_learning")
    payload["historical_recommendations_overwritten"] = True

    with pytest.raises(ValueError, match="historical_recommendations_overwritten"):
        validate_simulation_origin_payload(payload)


def test_task_008g_validation_does_not_mutate_input_payloads() -> None:
    payload = _payload("system_generated_learning")
    before_validation = deepcopy(payload)

    validate_simulation_origin_payload(payload)

    assert payload == before_validation


@pytest.mark.parametrize("origin", ALLOWED_SIMULATION_ORIGINS)
def test_task_008g_both_origins_preserve_advisory_only_and_human_in_the_loop_framing(
    origin: str,
) -> None:
    payload = _payload(origin)

    result = validate_simulation_origin_payload(payload)

    assert payload["advisory_only"] is True
    assert payload["human_in_the_loop"] is True
    assert result["advisory_only"] is True
    assert result["human_in_the_loop"] is True
