from __future__ import annotations

from copy import deepcopy

import pytest

from app.simulation_contract import CANONICAL_SCHEMA_TABLE_NAMES, LOCKED_ENDPOINT_NAMES
from app.simulation_desk_readiness import (
    READINESS_BOUNDARY_FLAG_NAMES,
    build_simulation_desk_readiness_report,
    validate_simulation_desk_readiness_report,
)


def _valid_order() -> dict[str, object]:
    return {
        "portfolio_id": "fixture-paper-portfolio-001",
        "symbol": "0700.HK",
        "side": "buy",
        "quantity": 100,
        "order_type": "limit",
        "limit_price": 375.5,
    }


def test_task_008e_default_readiness_report_passes() -> None:
    report = build_simulation_desk_readiness_report()
    result = validate_simulation_desk_readiness_report(report)

    assert report["task_id"] == "008E"
    assert report["classification"] == "implementation-limited local-only"
    assert report["validation_status"] == "passed"
    assert result["validation_status"] == "passed"


def test_task_008e_includes_task_008b_fixture_validation_evidence() -> None:
    report = build_simulation_desk_readiness_report()
    evidence = report["source_reports"]["task_008b"]

    assert evidence["source_task_id"] == "008B"
    assert evidence["validation_status"] == "passed"
    assert evidence["record_count"] == 7
    assert all(evidence["record_type_coverage"].values())
    assert evidence["losing_outcomes_remain_visible"] is True


def test_task_008e_includes_task_008c_paper_order_validation_evidence() -> None:
    report = build_simulation_desk_readiness_report()
    evidence = report["source_reports"]["task_008c"]

    assert evidence["source_task_id"] == "008C"
    assert evidence["validation_status"] == "passed"
    assert evidence["record_type"] == "paper_order_intent"
    assert evidence["validated_order"]["symbol"] == "0700.HK"
    assert evidence["would_create_order"] is False


def test_task_008e_preserves_canonical_schema_table_names() -> None:
    report = build_simulation_desk_readiness_report()

    assert report["canonical_schema_table_references_preserved"] == CANONICAL_SCHEMA_TABLE_NAMES


def test_task_008e_references_locked_endpoint_names_without_implementing_endpoints() -> None:
    report = build_simulation_desk_readiness_report()

    assert set(report["locked_endpoint_names_referenced_without_implementation"]) == set(
        LOCKED_ENDPOINT_NAMES
    )
    assert report["boundary_flags"]["endpoint_runtime_enabled"] is False
    assert report["boundary_flags"]["http_enabled"] is False


def test_task_008e_would_create_order_remains_false() -> None:
    report = build_simulation_desk_readiness_report()

    assert report["would_create_order"] is False
    assert report["source_reports"]["task_008c"]["would_create_order"] is False


def test_task_008e_all_forbidden_boundary_flags_remain_false() -> None:
    report = build_simulation_desk_readiness_report()

    assert set(report["boundary_flags"]) == set(READINESS_BOUNDARY_FLAG_NAMES)
    assert all(value is False for value in report["boundary_flags"].values())


@pytest.mark.parametrize("flag_name", READINESS_BOUNDARY_FLAG_NAMES)
def test_task_008e_any_forbidden_boundary_flag_enabled_fails(flag_name: str) -> None:
    report = build_simulation_desk_readiness_report()
    report["boundary_flags"][flag_name] = True

    with pytest.raises(ValueError, match="forbidden boundary flags must remain false"):
        validate_simulation_desk_readiness_report(report)


def test_task_008e_task_008b_boundary_compliance_failure_fails_validation() -> None:
    report = build_simulation_desk_readiness_report()
    report["source_reports"]["task_008b"]["boundary_compliance"][
        "no_persistence_flags_enabled"
    ] = False

    with pytest.raises(ValueError, match="Task 008B boundary compliance must remain true"):
        validate_simulation_desk_readiness_report(report)


def test_task_008e_task_008c_boundary_flag_enabled_fails_validation() -> None:
    report = build_simulation_desk_readiness_report()
    report["source_reports"]["task_008c"]["boundary_flags"]["persistence_enabled"] = True

    with pytest.raises(ValueError, match="Task 008C boundary flags must remain false"):
        validate_simulation_desk_readiness_report(report)


def test_task_008e_approval_gate_crossed_fails_validation() -> None:
    report = build_simulation_desk_readiness_report()
    report["approval_gate_status"]["persistence approval gate"] = True

    with pytest.raises(ValueError, match="approval gates must remain not crossed"):
        validate_simulation_desk_readiness_report(report)


def test_task_008e_task_008c_wrong_record_type_fails_validation() -> None:
    report = build_simulation_desk_readiness_report()
    evidence = report["source_reports"]["task_008c"]
    evidence["record_type"] = "paper_position"

    assert evidence["source_task_id"] == "008C"
    assert evidence["validation_status"] == "passed"
    assert evidence["would_create_order"] is False
    assert all(value is False for value in evidence["boundary_flags"].values())
    with pytest.raises(ValueError, match="record_type must remain paper_order_intent"):
        validate_simulation_desk_readiness_report(report)


@pytest.mark.parametrize(
    ("field_name", "malformed_value", "expected_error"),
    [
        ("symbol", "700.HK", "0700.HK"),
        ("side", "hold", "side must be buy or sell"),
        ("quantity", -1, "quantity must be non-negative"),
        ("order_type", "stop", "order_type must be market or limit"),
        ("limit_price", -0.01, "limit_price must be non-negative"),
    ],
)
def test_task_008e_task_008c_stale_malformed_validated_order_fails_validation(
    field_name: str,
    malformed_value: object,
    expected_error: str,
) -> None:
    report = build_simulation_desk_readiness_report()
    evidence = report["source_reports"]["task_008c"]
    evidence["validated_order"][field_name] = malformed_value

    assert evidence["source_task_id"] == "008C"
    assert evidence["validation_status"] == "passed"
    assert evidence["would_create_order"] is False
    assert all(value is False for value in evidence["boundary_flags"].values())
    with pytest.raises(ValueError, match=expected_error):
        validate_simulation_desk_readiness_report(report)


def test_task_008e_task_008c_missing_portfolio_id_fails_validation() -> None:
    report = build_simulation_desk_readiness_report()
    evidence = report["source_reports"]["task_008c"]
    evidence["validated_order"].pop("portfolio_id")

    assert evidence["source_task_id"] == "008C"
    assert evidence["validation_status"] == "passed"
    assert evidence["would_create_order"] is False
    assert all(value is False for value in evidence["boundary_flags"].values())
    with pytest.raises(ValueError, match="validated_order missing required fields"):
        validate_simulation_desk_readiness_report(report)


def test_task_008e_invalid_local_paper_order_input_fails_safely() -> None:
    order = _valid_order()
    order["symbol"] = "700.HK"

    with pytest.raises(ValueError, match="0700.HK"):
        build_simulation_desk_readiness_report(order)


def test_task_008e_generation_and_validation_do_not_mutate_inputs() -> None:
    order = _valid_order()
    order_before = deepcopy(order)

    report = build_simulation_desk_readiness_report(order)
    report_before = deepcopy(report)
    validation_result = validate_simulation_desk_readiness_report(report)

    assert order == order_before
    assert report == report_before
    assert validation_result["validation_mutates_inputs"] is False


def test_task_008e_no_runtime_persistence_or_external_behavior_is_introduced() -> None:
    report = build_simulation_desk_readiness_report()
    flags = report["boundary_flags"]

    for flag_name in (
        "io_enabled",
        "http_enabled",
        "database_write_enabled",
        "persistence_enabled",
        "production_supabase_required",
        "production_supabase_connected",
        "supabase_client_required",
        "endpoint_runtime_enabled",
        "paper_order_created",
        "broker_execution_enabled",
        "broker_api_called",
        "external_apis_enabled",
        "external_api_called",
        "external_api_required",
        "secrets_required",
        "real_money_order_placed",
        "real_money_trading_automation_enabled",
    ):
        assert flags[flag_name] is False

    assert report["in_memory"] is True
    assert report["non_persistent"] is True
    assert report["local_only"] is True
