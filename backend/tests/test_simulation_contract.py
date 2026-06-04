from __future__ import annotations

from copy import deepcopy

import pytest

from app.simulation_contract import (
    BOUNDARY_FLAG_NAMES,
    EXPECTED_SIMULATION_RECORD_TYPES,
    build_simulation_contract_fixtures,
    build_simulation_validation_matrix,
    validate_simulation_fixture_collection,
    validate_simulation_record,
)


def _fixture_by_type(record_type: str) -> dict[str, object]:
    fixtures = build_simulation_contract_fixtures()
    return next(record for record in fixtures if record["record_type"] == record_type)


@pytest.mark.parametrize("record_type", EXPECTED_SIMULATION_RECORD_TYPES)
def test_task_008b_valid_fixture_per_record_type_passes(record_type: str) -> None:
    report = validate_simulation_record(_fixture_by_type(record_type))

    assert report["validation_status"] == "passed"
    assert report["record_type"] == record_type


def test_task_008b_full_fixture_collection_passes() -> None:
    report = validate_simulation_fixture_collection(build_simulation_contract_fixtures())

    assert report["validation_status"] == "passed"
    assert report["present_record_types"] == list(EXPECTED_SIMULATION_RECORD_TYPES)
    assert report["losing_outcomes_remain_visible"] is True
    assert report["learning_proposals_reviewable_not_auto_applied"] is True


def test_task_008b_fixture_report_contains_all_expected_record_types_and_boundary_flags() -> None:
    matrix = build_simulation_validation_matrix()

    assert matrix["validation_status"] == "passed"
    assert set(matrix["record_type_coverage"]) == set(EXPECTED_SIMULATION_RECORD_TYPES)
    assert all(matrix["record_type_coverage"].values())
    assert matrix["boundary_compliance"] == {
        "losing_outcomes_remain_visible": True,
        "learning_proposals_reviewable_not_auto_applied": True,
        "no_persistence_flags_enabled": True,
        "no_production_supabase_flags_enabled": True,
        "no_broker_or_real_money_flags_enabled": True,
        "no_endpoint_runtime_flag_enabled": True,
        "validation_does_not_mutate_inputs": True,
    }
    assert set(matrix["locked_endpoint_names_referenced_without_implementation"]) == {
        "POST /api/v1/simulation/paper-orders",
        "GET /api/v1/paper-portfolios/{portfolio_id}",
        "POST /api/v1/strategy-recommendations",
        "GET /api/v1/strategy-recommendations/{recommendation_id}",
    }


def test_task_008b_fixture_builder_is_deterministic_and_uses_isolated_mutables() -> None:
    first_fixture_set = build_simulation_contract_fixtures()
    second_fixture_set = build_simulation_contract_fixtures()

    assert first_fixture_set == second_fixture_set
    assert first_fixture_set[0]["boundary_flags"] is not first_fixture_set[1]["boundary_flags"]
    assert (
        first_fixture_set[0]["locked_endpoint_references"]
        is not first_fixture_set[1]["locked_endpoint_references"]
    )


def test_task_008b_missing_locked_endpoint_reference_fails() -> None:
    record = _fixture_by_type("paper_order_intent")
    record["locked_endpoint_references"] = record["locked_endpoint_references"][:-1]

    with pytest.raises(ValueError, match="missing required names"):
        validate_simulation_record(record)


def test_task_008b_missing_required_field_fails() -> None:
    record = _fixture_by_type("paper_portfolio")
    record.pop("starting_cash")

    with pytest.raises(ValueError, match="missing required fields.*starting_cash"):
        validate_simulation_record(record)


def test_task_008b_unknown_record_type_fails() -> None:
    record = _fixture_by_type("paper_portfolio")
    record["record_type"] = "renamed_paper_portfolio"

    with pytest.raises(ValueError, match="unknown record_type"):
        validate_simulation_record(record)


def test_task_008b_paper_order_intent_zero_quantity_passes() -> None:
    record = _fixture_by_type("paper_order_intent")
    record["quantity"] = 0

    report = validate_simulation_record(record)

    assert report["validation_status"] == "passed"
    assert report["record_type"] == "paper_order_intent"


def test_task_008b_paper_order_intent_negative_quantity_fails() -> None:
    record = _fixture_by_type("paper_order_intent")
    record["quantity"] = -1

    with pytest.raises(ValueError, match="quantity.*non-negative"):
        validate_simulation_record(record)


def test_task_008b_paper_position_zero_quantity_fails() -> None:
    record = _fixture_by_type("paper_position")
    record["quantity"] = 0

    with pytest.raises(ValueError, match="quantity.*positive"):
        validate_simulation_record(record)


@pytest.mark.parametrize(
    "record_type",
    ["paper_portfolio", "paper_order_intent", "paper_position", "learning_proposal"],
)
def test_task_008b_invalid_status_fails(record_type: str) -> None:
    record = _fixture_by_type(record_type)
    record["status"] = "invalid_status"

    with pytest.raises(ValueError, match="status is invalid|status.*invalid"):
        validate_simulation_record(record)


@pytest.mark.parametrize("record_type", ["paper_position", "trade_review"])
def test_task_008b_hidden_losing_outcome_fails(record_type: str) -> None:
    record = _fixture_by_type(record_type)
    record["losing_outcome_visible"] = False

    with pytest.raises(ValueError, match="losing outcome must remain visible"):
        validate_simulation_record(record)


def test_task_008b_auto_applied_learning_proposal_fails() -> None:
    record = _fixture_by_type("learning_proposal")
    record["auto_applied"] = True

    with pytest.raises(ValueError, match="must not be auto-applied"):
        validate_simulation_record(record)


@pytest.mark.parametrize(
    "flag_name",
    [
        "persistence_enabled",
        "production_supabase_required",
        "broker_execution_enabled",
        "real_money_order_placed",
        "endpoint_runtime_enabled",
    ],
)
def test_task_008b_required_boundary_flag_true_fails(flag_name: str) -> None:
    assert flag_name in BOUNDARY_FLAG_NAMES
    record = _fixture_by_type("paper_order_intent")
    record["boundary_flags"][flag_name] = True

    with pytest.raises(ValueError, match="boundary flags must remain false"):
        validate_simulation_record(record)


def test_task_008b_validation_does_not_mutate_inputs() -> None:
    fixtures = build_simulation_contract_fixtures()
    before_validation = deepcopy(fixtures)

    record_report = validate_simulation_record(fixtures[0])
    collection_report = validate_simulation_fixture_collection(fixtures)
    matrix = build_simulation_validation_matrix(fixtures)

    assert record_report["validation_status"] == "passed"
    assert collection_report["validation_status"] == "passed"
    assert matrix["validation_status"] == "passed"
    assert fixtures == before_validation
