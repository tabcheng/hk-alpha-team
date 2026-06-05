from __future__ import annotations

from copy import deepcopy

import pytest

from app.simulation_contract import CANONICAL_SCHEMA_TABLE_NAMES, LOCKED_ENDPOINT_NAMES
from app.simulation_desk_scenarios import (
    INVALID_SCENARIO_EXPECTATIONS,
    SCENARIO_APPROVAL_GATES_NOT_CROSSED,
    SCENARIO_BOUNDARY_FLAG_NAMES,
    build_simulation_desk_scenario_pack,
    validate_simulation_desk_scenario_pack,
)


def test_task_008f_default_scenario_pack_builds_successfully() -> None:
    pack = build_simulation_desk_scenario_pack()

    assert pack["task_id"] == "008F"
    assert pack["report_name"] == "Task 008F — Local Simulation Desk Scenario Pack and Gate Decision Matrix"
    assert pack["classification"] == "implementation-limited local-only"
    assert pack["validation_status"] == "passed"


def test_task_008f_default_scenario_pack_validates_successfully() -> None:
    pack = build_simulation_desk_scenario_pack()
    result = validate_simulation_desk_scenario_pack(pack)

    assert result["validation_status"] == "passed"
    assert result["task_id"] == "008F"
    assert result["validation_mutates_inputs"] is False


def test_task_008f_scenario_pack_includes_task_008b_evidence() -> None:
    pack = build_simulation_desk_scenario_pack()
    evidence = pack["source_reports"]["task_008b"]

    assert evidence["source_task_id"] == "008B"
    assert evidence["fixture_collection_report"]["validation_status"] == "passed"
    assert evidence["validation_matrix"]["validation_status"] == "passed"


def test_task_008f_scenario_pack_includes_task_008c_evidence() -> None:
    pack = build_simulation_desk_scenario_pack()
    evidence = pack["source_reports"]["task_008c"]

    assert evidence["source_task_id"] == "008C"
    assert evidence["paper_order_validation_report"]["validation_status"] == "passed"
    assert evidence["paper_order_validation_report"]["would_create_order"] is False


def test_task_008f_scenario_pack_includes_task_008e_readiness_evidence() -> None:
    pack = build_simulation_desk_scenario_pack()
    evidence = pack["source_reports"]["task_008e"]

    assert evidence["source_task_id"] == "008E"
    assert evidence["readiness_report"]["validation_status"] == "passed"
    assert evidence["readiness_validation"]["validation_status"] == "passed"


def test_task_008f_valid_hk_paper_order_intent_scenario_passes() -> None:
    pack = build_simulation_desk_scenario_pack()
    scenario = pack["scenario_matrix"]["paper_order_intent_scenarios"][
        "valid_paper_order_intent"
    ]

    assert scenario["validation_status"] == "passed"
    assert scenario["validation_result"]["symbol"] == "0700.HK"
    assert scenario["would_create_order"] is False


@pytest.mark.parametrize(
    "scenario_name",
    [
        "malformed_hk_symbol",
        "invalid_side",
        "invalid_quantity",
        "invalid_order_type",
        "invalid_limit_price",
        "missing_portfolio_id",
    ],
)
def test_task_008f_invalid_paper_order_intent_scenarios_fail_safely(
    scenario_name: str,
) -> None:
    pack = build_simulation_desk_scenario_pack()
    scenario = pack["scenario_matrix"]["paper_order_intent_scenarios"][scenario_name]

    assert scenario["validation_status"] == "failed_safely"
    assert scenario["would_create_order"] is False
    assert scenario["mutated_inputs"] is False
    assert INVALID_SCENARIO_EXPECTATIONS[scenario_name] in scenario["error_message"]


def test_task_008f_readiness_aggregation_scenario_passes() -> None:
    pack = build_simulation_desk_scenario_pack()
    scenario = pack["scenario_matrix"]["readiness_aggregation"]

    assert scenario["source_task_id"] == "008E"
    assert scenario["validation_status"] == "passed"
    assert scenario["would_create_order"] is False


def test_task_008f_canonical_schema_table_names_are_preserved() -> None:
    pack = build_simulation_desk_scenario_pack()

    assert pack["canonical_schema_table_references_preserved"] == CANONICAL_SCHEMA_TABLE_NAMES


def test_task_008f_locked_endpoint_names_are_referenced_without_implementation() -> None:
    pack = build_simulation_desk_scenario_pack()

    assert set(pack["locked_endpoint_names_referenced_without_implementation"]) == set(
        LOCKED_ENDPOINT_NAMES
    )
    assert pack["boundary_flags"]["endpoint_runtime_enabled"] is False
    assert pack["boundary_flags"]["endpoint_handler_enabled"] is False


def test_task_008f_approval_gates_remain_false() -> None:
    pack = build_simulation_desk_scenario_pack()

    assert set(pack["approval_gate_status"]) == set(SCENARIO_APPROVAL_GATES_NOT_CROSSED)
    assert all(value is False for value in pack["approval_gate_status"].values())


@pytest.mark.parametrize("gate_name", SCENARIO_APPROVAL_GATES_NOT_CROSSED)
def test_task_008f_any_crossed_approval_gate_causes_validation_failure(
    gate_name: str,
) -> None:
    pack = build_simulation_desk_scenario_pack()
    pack["approval_gate_status"][gate_name] = True

    with pytest.raises(ValueError, match="approval gates must remain not crossed"):
        validate_simulation_desk_scenario_pack(pack)


def test_task_008f_all_forbidden_boundary_flags_remain_false() -> None:
    pack = build_simulation_desk_scenario_pack()

    assert set(pack["boundary_flags"]) == set(SCENARIO_BOUNDARY_FLAG_NAMES)
    assert all(value is False for value in pack["boundary_flags"].values())


@pytest.mark.parametrize("flag_name", SCENARIO_BOUNDARY_FLAG_NAMES)
def test_task_008f_any_forbidden_boundary_flag_enabled_causes_validation_failure(
    flag_name: str,
) -> None:
    pack = build_simulation_desk_scenario_pack()
    pack["boundary_flags"][flag_name] = True

    with pytest.raises(ValueError, match="forbidden boundary flags must remain false"):
        validate_simulation_desk_scenario_pack(pack)


def test_task_008f_losing_simulation_outcomes_remain_visible() -> None:
    pack = build_simulation_desk_scenario_pack()
    evidence = pack["loss_visibility_evidence"]

    assert evidence["losing_outcomes_remain_visible"] is True
    assert evidence["hidden_or_overwritten_losing_outcomes"] is False
    assert evidence["records"]
    assert any(record["outcome_label"] == "loss" for record in evidence["records"])


def test_task_008f_learning_proposals_remain_reviewable_and_not_auto_applied() -> None:
    pack = build_simulation_desk_scenario_pack()
    evidence = pack["learning_proposal_reviewability_evidence"]

    assert evidence["learning_proposals_remain_reviewable"] is True
    assert evidence["learning_proposals_auto_applied"] is False
    assert evidence["proposals"]
    assert all(proposal["reviewable"] is True for proposal in evidence["proposals"])
    assert all(proposal["auto_applied"] is False for proposal in evidence["proposals"])


def test_task_008f_scenario_pack_validation_does_not_mutate_inputs() -> None:
    pack = build_simulation_desk_scenario_pack()
    before_validation = deepcopy(pack)
    result = validate_simulation_desk_scenario_pack(pack)

    assert pack == before_validation
    assert result["validation_mutates_inputs"] is False


def test_task_008f_no_local_only_or_boundary_behavior_is_introduced() -> None:
    pack = build_simulation_desk_scenario_pack()
    flags = pack["boundary_flags"]

    for flag_name in (
        "io_enabled",
        "http_enabled",
        "database_read_enabled",
        "database_write_enabled",
        "persistence_enabled",
        "production_supabase_required",
        "production_supabase_connected",
        "supabase_client_required",
        "endpoint_runtime_enabled",
        "endpoint_handler_enabled",
        "external_apis_enabled",
        "external_api_called",
        "external_api_required",
        "broker_execution_enabled",
        "broker_api_called",
        "secrets_required",
        "paper_order_created",
        "paper_portfolio_runtime_enabled",
        "strategy_recommendation_persistence_enabled",
        "audit_event_database_creation_enabled",
        "live_market_data_enabled",
        "deployment_enabled",
        "autonomous_order_placement_enabled",
        "real_money_order_placed",
        "real_money_trading_automation_enabled",
    ):
        assert flags[flag_name] is False

    assert pack["advisory_only"] is True
    assert pack["simulation_only"] is True
    assert pack["human_in_the_loop"] is True
    assert pack["deterministic"] is True
    assert pack["in_memory"] is True
    assert pack["non_persistent"] is True
    assert pack["local_only"] is True
    assert pack["task_008f_does_not_close_m5"] is True
    assert all(gate["task_008f_approves_gate"] is False for gate in pack["next_gate_matrix"])


def test_task_008f_stale_valid_scenario_input_fails_revalidation() -> None:
    pack = build_simulation_desk_scenario_pack()
    scenario = pack["scenario_matrix"]["paper_order_intent_scenarios"][
        "valid_paper_order_intent"
    ]
    scenario["input_order"]["symbol"] = "700.HK"

    with pytest.raises(ValueError, match="0700.HK"):
        validate_simulation_desk_scenario_pack(pack)


def test_task_008f_stale_invalid_scenario_input_must_still_fail() -> None:
    pack = build_simulation_desk_scenario_pack()
    scenario = pack["scenario_matrix"]["paper_order_intent_scenarios"][
        "malformed_hk_symbol"
    ]
    scenario["input_order"]["symbol"] = "0700.HK"

    with pytest.raises(ValueError, match="malformed_hk_symbol input_order must fail safely"):
        validate_simulation_desk_scenario_pack(pack)


def test_task_008f_hidden_losing_outcome_evidence_fails_validation() -> None:
    pack = build_simulation_desk_scenario_pack()
    loss_record = next(
        record
        for record in pack["loss_visibility_evidence"]["records"]
        if record["outcome_label"] == "loss"
    )
    loss_record["losing_outcome_visible"] = False

    with pytest.raises(ValueError, match="losing simulation outcomes must remain visible"):
        validate_simulation_desk_scenario_pack(pack)


def test_task_008f_auto_applied_learning_proposal_evidence_fails_validation() -> None:
    pack = build_simulation_desk_scenario_pack()
    proposal = pack["learning_proposal_reviewability_evidence"]["proposals"][0]
    proposal["auto_applied"] = True

    with pytest.raises(ValueError, match="learning proposals must remain reviewable"):
        validate_simulation_desk_scenario_pack(pack)


def test_task_008f_missing_next_gate_direction_fails_validation() -> None:
    pack = build_simulation_desk_scenario_pack()
    pack["next_gate_matrix"].pop()

    with pytest.raises(ValueError, match="next_gate_matrix must preserve every possible Task 008G direction"):
        validate_simulation_desk_scenario_pack(pack)


def test_task_008f_locked_endpoint_duplicate_or_reorder_fails_validation() -> None:
    pack = build_simulation_desk_scenario_pack()
    endpoints = pack["locked_endpoint_names_referenced_without_implementation"]
    endpoints.append(endpoints[0])

    with pytest.raises(ValueError, match="locked endpoint names must be referenced without implementation"):
        validate_simulation_desk_scenario_pack(pack)
