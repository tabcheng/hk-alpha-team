from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from app.simulation_contract import (
    BOUNDARY_FLAG_NAMES,
    CANONICAL_SCHEMA_TABLE_NAMES,
    LOCKED_ENDPOINT_NAMES,
    build_simulation_contract_fixtures,
    build_simulation_validation_matrix,
    validate_simulation_fixture_collection,
)
from app.simulation_order_validation import (
    LOCAL_PAPER_ORDER_BOUNDARY_FLAGS,
    build_local_paper_order_validation_report,
    validate_local_paper_order_intent,
)

TASK_ID = "008E"
REPORT_NAME = "Task 008E — Local-only Simulation Desk Readiness Report / Boundary Aggregator"
CLASSIFICATION = "implementation-limited local-only"

DEFAULT_LOCAL_PAPER_ORDER_INTENT: dict[str, object] = {
    "portfolio_id": "fixture-paper-portfolio-001",
    "symbol": "0700.HK",
    "side": "buy",
    "quantity": 100,
    "order_type": "limit",
    "limit_price": 375.5,
}

TASK_008E_SPECIFIC_BOUNDARY_FLAGS = (
    "external_apis_enabled",
    "external_api_called",
    "external_api_required",
    "secrets_required",
)

READINESS_BOUNDARY_FLAG_NAMES = tuple(
    dict.fromkeys(
        (
            *BOUNDARY_FLAG_NAMES,
            *LOCAL_PAPER_ORDER_BOUNDARY_FLAGS,
            *TASK_008E_SPECIFIC_BOUNDARY_FLAGS,
        )
    )
)

APPROVAL_GATES_NOT_CROSSED = (
    "runtime approval gate",
    "persistence approval gate",
    "SQL migration approval gate",
    "Supabase client approval gate",
    "production Supabase approval gate",
    "endpoint runtime approval gate",
    "paper-order creation approval gate",
    "paper-portfolio runtime approval gate",
    "strategy recommendation persistence approval gate",
    "audit-event database creation approval gate",
    "broker integration approval gate",
    "real-money trading approval gate",
)


def _boundary_flags() -> dict[str, bool]:
    return {flag_name: False for flag_name in READINESS_BOUNDARY_FLAG_NAMES}


def _approval_gate_status() -> dict[str, bool]:
    return {gate_name: False for gate_name in APPROVAL_GATES_NOT_CROSSED}


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"Simulation Desk readiness validation failed: {message}")


def _require_mapping(value: object, field_name: str) -> Mapping[str, object]:
    _require(isinstance(value, Mapping), f"{field_name} must be a mapping")
    return value


def _require_sequence(value: object, field_name: str) -> list[object]:
    _require(isinstance(value, list), f"{field_name} must be a list")
    return value


def _build_portfolio_registry() -> dict[str, dict[str, object]]:
    return {
        "fixture-paper-portfolio-001": {
            "portfolio_uuid": "paper-portfolio-fixture-001",
            "status": "active",
        }
    }


def build_simulation_desk_readiness_report(
    order: Mapping[str, object] | None = None,
) -> dict[str, Any]:
    """Build the deterministic, in-memory Task 008E local-only readiness report."""

    paper_order_intent = (
        deepcopy(DEFAULT_LOCAL_PAPER_ORDER_INTENT) if order is None else deepcopy(dict(order))
    )
    fixture_records = build_simulation_contract_fixtures()
    fixture_collection_report = validate_simulation_fixture_collection(fixture_records)
    fixture_validation_matrix = build_simulation_validation_matrix(fixture_records)
    paper_order_validation_report = build_local_paper_order_validation_report(
        paper_order_intent,
        portfolio_registry=_build_portfolio_registry(),
    )
    paper_order_validation_result = validate_local_paper_order_intent(
        paper_order_intent,
        portfolio_registry=_build_portfolio_registry(),
    )

    report = {
        "task_id": TASK_ID,
        "report_name": REPORT_NAME,
        "classification": CLASSIFICATION,
        "validation_status": "passed",
        "source_reports": {
            "task_008b": {
                "source_task_id": "008B",
                "source_report_name": fixture_validation_matrix["matrix_name"],
                "validation_status": fixture_validation_matrix["validation_status"],
                "record_count": fixture_collection_report["record_count"],
                "record_type_coverage": fixture_validation_matrix["record_type_coverage"],
                "boundary_compliance": fixture_validation_matrix["boundary_compliance"],
                "losing_outcomes_remain_visible": fixture_collection_report[
                    "losing_outcomes_remain_visible"
                ],
                "learning_proposals_reviewable_not_auto_applied": fixture_collection_report[
                    "learning_proposals_reviewable_not_auto_applied"
                ],
            },
            "task_008c": {
                "source_task_id": "008C",
                "source_report_name": paper_order_validation_report["report_name"],
                "validation_status": paper_order_validation_report["validation_status"],
                "record_type": paper_order_validation_report["record_type"],
                "validated_order": paper_order_validation_report["validated_order"],
                "would_create_order": paper_order_validation_report["would_create_order"],
                "boundary_flags": paper_order_validation_report["boundary_flags"],
            },
        },
        "canonical_schema_table_references_preserved": dict(CANONICAL_SCHEMA_TABLE_NAMES),
        "locked_endpoint_names_referenced_without_implementation": list(LOCKED_ENDPOINT_NAMES),
        "approval_gates_not_crossed": list(APPROVAL_GATES_NOT_CROSSED),
        "approval_gate_status": _approval_gate_status(),
        "boundary_flags": _boundary_flags(),
        "would_create_order": False,
        "advisory_only": True,
        "simulation_only": True,
        "human_in_the_loop": True,
        "deterministic": True,
        "in_memory": True,
        "non_persistent": True,
        "local_only": True,
        "notes": [
            "Task 008E aggregates Task 008B and Task 008C local evidence only.",
            "The report is deterministic, in-memory, non-persistent, and local-only.",
            "Endpoint strings are referenced for traceability only and are not implemented.",
            "No IO, HTTP, database writes, persistence, production Supabase, Supabase client, endpoint runtime, paper-order creation, broker execution, external API, secrets, real-money order placement, or real-money trading automation is introduced.",
            "HK Alpha Team v1 remains advisory-only, simulation-only, and human-in-the-loop.",
        ],
    }

    validate_simulation_desk_readiness_report(report)
    _require(
        paper_order_validation_result["would_create_order"] is False,
        "Task 008C evidence must not create orders",
    )
    return report


def validate_simulation_desk_readiness_report(report: Mapping[str, object]) -> dict[str, Any]:
    """Validate that a Task 008E readiness report stays inside local-only boundaries."""

    _require_mapping(report, "report")
    before_validation = deepcopy(dict(report))

    _require(report.get("task_id") == TASK_ID, "task_id must be 008E")
    _require(report.get("report_name") == REPORT_NAME, "report_name is not recognized")
    _require(
        report.get("classification") == CLASSIFICATION,
        "classification must remain implementation-limited local-only",
    )
    _require(report.get("validation_status") == "passed", "validation_status must be passed")

    source_reports = _require_mapping(report.get("source_reports"), "source_reports")
    task_008b = _require_mapping(source_reports.get("task_008b"), "source_reports.task_008b")
    task_008c = _require_mapping(source_reports.get("task_008c"), "source_reports.task_008c")
    _require(
        task_008b.get("source_task_id") == "008B",
        "Task 008B evidence must identify source_task_id",
    )
    _require(
        task_008c.get("source_task_id") == "008C",
        "Task 008C evidence must identify source_task_id",
    )
    _require(task_008b.get("validation_status") == "passed", "Task 008B evidence must pass")
    _require(task_008c.get("validation_status") == "passed", "Task 008C evidence must pass")
    _require(
        task_008b.get("record_count") == len(CANONICAL_SCHEMA_TABLE_NAMES),
        "Task 008B evidence must cover all Simulation Desk fixture records",
    )

    record_type_coverage = _require_mapping(
        task_008b.get("record_type_coverage"),
        "source_reports.task_008b.record_type_coverage",
    )
    missing_record_types = sorted(
        set(CANONICAL_SCHEMA_TABLE_NAMES) - set(record_type_coverage)
    )
    _require(not missing_record_types, f"Task 008B evidence missing record types: {missing_record_types}")
    uncovered_record_types = sorted(
        record_type
        for record_type, covered in record_type_coverage.items()
        if covered is not True
    )
    _require(
        not uncovered_record_types,
        f"Task 008B record coverage must remain true: {uncovered_record_types}",
    )

    boundary_compliance = _require_mapping(
        task_008b.get("boundary_compliance"),
        "source_reports.task_008b.boundary_compliance",
    )
    failed_boundary_checks = sorted(
        check_name
        for check_name, passed in boundary_compliance.items()
        if passed is not True
    )
    _require(
        not failed_boundary_checks,
        f"Task 008B boundary compliance must remain true: {failed_boundary_checks}",
    )
    _require(
        task_008b.get("losing_outcomes_remain_visible") is True,
        "Task 008B losing outcomes must remain visible",
    )
    _require(
        task_008b.get("learning_proposals_reviewable_not_auto_applied") is True,
        "Task 008B learning proposals must remain reviewable and not auto-applied",
    )

    task_008c_flags = _require_mapping(
        task_008c.get("boundary_flags"),
        "source_reports.task_008c.boundary_flags",
    )
    task_008c_missing_flags = sorted(
        set(LOCAL_PAPER_ORDER_BOUNDARY_FLAGS) - set(task_008c_flags)
    )
    _require(
        not task_008c_missing_flags,
        f"Task 008C boundary flags missing required flags: {task_008c_missing_flags}",
    )
    task_008c_enabled_flags = sorted(
        flag_name
        for flag_name in LOCAL_PAPER_ORDER_BOUNDARY_FLAGS
        if task_008c_flags.get(flag_name) is not False
    )
    _require(
        not task_008c_enabled_flags,
        f"Task 008C boundary flags must remain false: {task_008c_enabled_flags}",
    )
    _require(task_008c.get("would_create_order") is False, "Task 008C must not create orders")

    schema_references = _require_mapping(
        report.get("canonical_schema_table_references_preserved"),
        "canonical_schema_table_references_preserved",
    )
    _require(
        dict(schema_references) == CANONICAL_SCHEMA_TABLE_NAMES,
        "canonical schema table names must be preserved without renaming",
    )

    endpoints = _require_sequence(
        report.get("locked_endpoint_names_referenced_without_implementation"),
        "locked_endpoint_names_referenced_without_implementation",
    )
    _require(
        set(endpoints) == set(LOCKED_ENDPOINT_NAMES),
        "locked endpoint names must be referenced without adding or removing names",
    )

    gates = _require_sequence(report.get("approval_gates_not_crossed"), "approval_gates_not_crossed")
    _require(
        set(gates) == set(APPROVAL_GATES_NOT_CROSSED),
        "approval gates must remain recorded as not crossed",
    )
    gate_status = _require_mapping(report.get("approval_gate_status"), "approval_gate_status")
    missing_gates = sorted(set(APPROVAL_GATES_NOT_CROSSED) - set(gate_status))
    unexpected_gates = sorted(set(gate_status) - set(APPROVAL_GATES_NOT_CROSSED))
    _require(not missing_gates, f"approval_gate_status missing required gates: {missing_gates}")
    _require(not unexpected_gates, f"approval_gate_status contains unexpected gates: {unexpected_gates}")
    crossed_gates = sorted(
        gate_name
        for gate_name in APPROVAL_GATES_NOT_CROSSED
        if gate_status.get(gate_name) is not False
    )
    _require(not crossed_gates, f"approval gates must remain not crossed: {crossed_gates}")

    boundary_flags = _require_mapping(report.get("boundary_flags"), "boundary_flags")
    missing_flags = sorted(set(READINESS_BOUNDARY_FLAG_NAMES) - set(boundary_flags))
    unexpected_flags = sorted(set(boundary_flags) - set(READINESS_BOUNDARY_FLAG_NAMES))
    _require(not missing_flags, f"boundary_flags missing required flags: {missing_flags}")
    _require(not unexpected_flags, f"boundary_flags contains unexpected flags: {unexpected_flags}")
    enabled_flags = sorted(
        flag_name
        for flag_name in READINESS_BOUNDARY_FLAG_NAMES
        if boundary_flags.get(flag_name) is not False
    )
    _require(not enabled_flags, f"forbidden boundary flags must remain false: {enabled_flags}")

    for field_name in (
        "would_create_order",
        "advisory_only",
        "simulation_only",
        "human_in_the_loop",
        "deterministic",
        "in_memory",
        "non_persistent",
        "local_only",
    ):
        expected_value = field_name != "would_create_order"
        _require(
            report.get(field_name) is expected_value,
            f"{field_name} must be {expected_value!r}",
        )

    _require(
        dict(report) == before_validation,
        "readiness report validation must not mutate inputs",
    )

    return {
        "validation_status": "passed",
        "task_id": TASK_ID,
        "boundary_flags": {flag_name: False for flag_name in READINESS_BOUNDARY_FLAG_NAMES},
        "would_create_order": False,
        "validation_mutates_inputs": False,
    }
