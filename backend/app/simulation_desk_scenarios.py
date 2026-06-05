from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

from app.simulation_contract import (
    CANONICAL_SCHEMA_TABLE_NAMES,
    LOCKED_ENDPOINT_NAMES,
    build_simulation_contract_fixtures,
    build_simulation_validation_matrix,
    validate_simulation_fixture_collection,
)
from app.simulation_desk_readiness import (
    APPROVAL_GATES_NOT_CROSSED,
    DEFAULT_LOCAL_PAPER_ORDER_INTENT,
    build_simulation_desk_readiness_report,
    validate_simulation_desk_readiness_report,
)
from app.simulation_order_validation import (
    LOCAL_PAPER_ORDER_BOUNDARY_FLAGS,
    build_local_paper_order_validation_report,
    validate_local_paper_order_intent,
)

TASK_ID = "008F"
REPORT_NAME = "Task 008F — Local Simulation Desk Scenario Pack and Gate Decision Matrix"
CLASSIFICATION = "implementation-limited local-only"
SOURCE_TASKS = ("008B", "008C", "008E")

TASK_008F_SPECIFIC_BOUNDARY_FLAGS = (
    "database_read_enabled",
    "external_apis_enabled",
    "external_api_called",
    "paper_portfolio_runtime_enabled",
    "strategy_recommendation_persistence_enabled",
    "audit_event_database_creation_enabled",
    "live_market_data_enabled",
    "deployment_enabled",
    "endpoint_handler_enabled",
    "autonomous_order_placement_enabled",
)

SCENARIO_BOUNDARY_FLAG_NAMES = tuple(
    dict.fromkeys((*LOCAL_PAPER_ORDER_BOUNDARY_FLAGS, *TASK_008F_SPECIFIC_BOUNDARY_FLAGS))
)

SCENARIO_APPROVAL_GATES_NOT_CROSSED = tuple(
    dict.fromkeys(
        (
            *APPROVAL_GATES_NOT_CROSSED,
            "external API approval gate",
            "live market data approval gate",
            "deployment approval gate",
            "autonomous order placement approval gate",
        )
    )
)

NEXT_GATE_DIRECTIONS = (
    "SQL migration gate",
    "persistence writes gate",
    "Supabase client gate",
    "production Supabase gate",
    "endpoint runtime gate",
    "paper-order creation gate",
    "paper-portfolio runtime gate",
    "strategy recommendation persistence gate",
    "audit-event database creation gate",
    "broker integration gate",
    "live market data gate",
    "external API gate",
    "deployment gate",
    "autonomous order placement gate",
    "real-money trading gate",
)

INVALID_SCENARIO_EXPECTATIONS = {
    "malformed_hk_symbol": "0700.HK",
    "invalid_side": "side must be buy or sell",
    "invalid_quantity": "quantity must be non-negative",
    "invalid_order_type": "order_type must be market or limit",
    "invalid_limit_price": "limit_price must be non-negative",
    "missing_portfolio_id": "portfolio_id must be a string",
}


def _boundary_flags() -> dict[str, bool]:
    return {flag_name: False for flag_name in SCENARIO_BOUNDARY_FLAG_NAMES}


def _approval_gate_status() -> dict[str, bool]:
    return {gate_name: False for gate_name in SCENARIO_APPROVAL_GATES_NOT_CROSSED}


def _portfolio_registry() -> dict[str, dict[str, object]]:
    return {
        "fixture-paper-portfolio-001": {
            "portfolio_uuid": "paper-portfolio-fixture-001",
            "status": "active",
        }
    }


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"Simulation Desk scenario pack validation failed: {message}")


def _require_mapping(value: object, field_name: str) -> Mapping[str, object]:
    _require(isinstance(value, Mapping), f"{field_name} must be a mapping")
    return value


def _require_sequence(value: object, field_name: str) -> list[object]:
    _require(isinstance(value, list), f"{field_name} must be a list")
    return value


def _build_valid_order() -> dict[str, object]:
    return deepcopy(DEFAULT_LOCAL_PAPER_ORDER_INTENT)


def _build_invalid_order_scenarios() -> dict[str, dict[str, object]]:
    valid_order = _build_valid_order()
    scenarios = {
        "malformed_hk_symbol": {**valid_order, "symbol": "700.HK"},
        "invalid_side": {**valid_order, "side": "hold"},
        "invalid_quantity": {**valid_order, "quantity": -1},
        "invalid_order_type": {**valid_order, "order_type": "stop"},
        "invalid_limit_price": {**valid_order, "limit_price": -0.01},
        "missing_portfolio_id": {
            key: value for key, value in valid_order.items() if key != "portfolio_id"
        },
    }
    return scenarios


def _validate_order_scenario(name: str, order: Mapping[str, object]) -> dict[str, object]:
    order_before = deepcopy(dict(order))
    try:
        result = validate_local_paper_order_intent(order, portfolio_registry=_portfolio_registry())
    except ValueError as exc:
        _require(dict(order) == order_before, f"{name} validation must not mutate inputs")
        return {
            "scenario_name": name,
            "validation_status": "failed_safely",
            "expected_status": "failed_safely",
            "input_order": deepcopy(dict(order)),
            "error_message": str(exc),
            "would_create_order": False,
            "mutated_inputs": False,
        }

    _require(dict(order) == order_before, f"{name} validation must not mutate inputs")
    return {
        "scenario_name": name,
        "validation_status": "passed",
        "expected_status": "passed",
        "input_order": deepcopy(dict(order)),
        "validation_result": result,
        "would_create_order": result["would_create_order"],
        "mutated_inputs": False,
    }


def _build_loss_visibility_evidence(records: list[dict[str, Any]]) -> dict[str, object]:
    losing_records = [
        {
            "record_id": record["record_id"],
            "record_type": record["record_type"],
            "outcome_label": record.get("outcome_label"),
            "drawdown_pct": record.get("drawdown_pct"),
            "losing_outcome_visible": record.get("losing_outcome_visible", True),
        }
        for record in records
        if record.get("outcome_label") == "loss" or record.get("drawdown_pct", 0) > 0
    ]
    return {
        "losing_outcomes_remain_visible": True,
        "hidden_or_overwritten_losing_outcomes": False,
        "records": losing_records,
    }


def _build_learning_reviewability_evidence(records: list[dict[str, Any]]) -> dict[str, object]:
    proposals = [
        {
            "record_id": record["record_id"],
            "status": record["status"],
            "reviewable": record["reviewable"],
            "auto_applied": record["auto_applied"],
        }
        for record in records
        if record.get("record_type") == "learning_proposal"
    ]
    return {
        "learning_proposals_remain_reviewable": True,
        "learning_proposals_auto_applied": False,
        "proposals": proposals,
    }


def build_simulation_desk_scenario_pack() -> dict[str, Any]:
    """Build a deterministic local-only Task 008F scenario pack without IO or persistence."""

    fixture_records = build_simulation_contract_fixtures()
    fixture_collection_report = validate_simulation_fixture_collection(fixture_records)
    fixture_validation_matrix = build_simulation_validation_matrix(fixture_records)
    valid_order = _build_valid_order()
    paper_order_validation_report = build_local_paper_order_validation_report(
        valid_order,
        portfolio_registry=_portfolio_registry(),
    )
    readiness_report = build_simulation_desk_readiness_report(valid_order)
    readiness_validation = validate_simulation_desk_readiness_report(readiness_report)

    order_scenarios = {
        "valid_paper_order_intent": _validate_order_scenario(
            "valid_paper_order_intent",
            valid_order,
        )
    }
    for scenario_name, order in _build_invalid_order_scenarios().items():
        order_scenarios[scenario_name] = _validate_order_scenario(scenario_name, order)

    pack = {
        "task_id": TASK_ID,
        "report_name": REPORT_NAME,
        "classification": CLASSIFICATION,
        "validation_status": "passed",
        "source_tasks": list(SOURCE_TASKS),
        "source_reports": {
            "task_008b": {
                "source_task_id": "008B",
                "fixture_collection_report": fixture_collection_report,
                "validation_matrix": fixture_validation_matrix,
            },
            "task_008c": {
                "source_task_id": "008C",
                "paper_order_validation_report": paper_order_validation_report,
            },
            "task_008e": {
                "source_task_id": "008E",
                "readiness_report": readiness_report,
                "readiness_validation": readiness_validation,
            },
        },
        "scenario_matrix": {
            "paper_order_intent_scenarios": order_scenarios,
            "readiness_aggregation": {
                "scenario_name": "task_008e_readiness_aggregation",
                "validation_status": readiness_validation["validation_status"],
                "expected_status": "passed",
                "source_task_id": "008E",
                "would_create_order": readiness_report["would_create_order"],
                "boundary_flags": readiness_report["boundary_flags"],
            },
        },
        "canonical_schema_table_references_preserved": dict(CANONICAL_SCHEMA_TABLE_NAMES),
        "locked_endpoint_names_referenced_without_implementation": list(LOCKED_ENDPOINT_NAMES),
        "approval_gate_status": _approval_gate_status(),
        "boundary_flags": _boundary_flags(),
        "loss_visibility_evidence": _build_loss_visibility_evidence(fixture_records),
        "learning_proposal_reviewability_evidence": _build_learning_reviewability_evidence(
            fixture_records
        ),
        "advisory_only": True,
        "simulation_only": True,
        "human_in_the_loop": True,
        "deterministic": True,
        "in_memory": True,
        "non_persistent": True,
        "local_only": True,
        "task_008f_does_not_close_m5": True,
        "m5_status": "In Progress",
        "next_gate_matrix": [
            {
                "gate_direction": gate_direction,
                "task_008f_approves_gate": False,
                "future_task_required": "008G or later with explicit Harness Engineering approval",
            }
            for gate_direction in NEXT_GATE_DIRECTIONS
        ],
        "notes": [
            "Task 008F aggregates Task 008B, Task 008C, and Task 008E local-only evidence.",
            "Endpoint strings are referenced only for traceability and are not implemented.",
            "No runtime, persistence, Supabase, endpoint handler, paper-order creation, paper-portfolio runtime, strategy persistence, audit-event database creation, broker, live-data, external API, deployment, autonomous order placement, or real-money gate is opened.",
            "Task 008F does not close M5; Task 008 / M5 remains In Progress.",
        ],
    }

    validate_simulation_desk_scenario_pack(pack)
    return pack


def validate_simulation_desk_scenario_pack(pack: Mapping[str, object]) -> dict[str, Any]:
    """Validate a Task 008F scenario pack while preserving local-only boundaries."""

    _require_mapping(pack, "pack")
    before_validation = deepcopy(dict(pack))

    _require(pack.get("task_id") == TASK_ID, "task_id must be 008F")
    _require(pack.get("report_name") == REPORT_NAME, "report_name is not recognized")
    _require(
        pack.get("classification") == CLASSIFICATION,
        "classification must remain implementation-limited local-only",
    )
    _require(pack.get("validation_status") == "passed", "validation_status must be passed")
    _require(pack.get("source_tasks") == list(SOURCE_TASKS), "source_tasks must remain 008B, 008C, and 008E")

    source_reports = _require_mapping(pack.get("source_reports"), "source_reports")
    task_008b = _require_mapping(source_reports.get("task_008b"), "source_reports.task_008b")
    task_008c = _require_mapping(source_reports.get("task_008c"), "source_reports.task_008c")
    task_008e = _require_mapping(source_reports.get("task_008e"), "source_reports.task_008e")
    _require(task_008b.get("source_task_id") == "008B", "Task 008B evidence must be present")
    _require(task_008c.get("source_task_id") == "008C", "Task 008C evidence must be present")
    _require(task_008e.get("source_task_id") == "008E", "Task 008E evidence must be present")

    fixture_collection_report = _require_mapping(
        task_008b.get("fixture_collection_report"),
        "source_reports.task_008b.fixture_collection_report",
    )
    fixture_validation_matrix = _require_mapping(
        task_008b.get("validation_matrix"),
        "source_reports.task_008b.validation_matrix",
    )
    _require(fixture_collection_report.get("validation_status") == "passed", "Task 008B fixture evidence must pass")
    _require(fixture_validation_matrix.get("validation_status") == "passed", "Task 008B validation matrix must pass")
    _require(
        fixture_collection_report.get("losing_outcomes_remain_visible") is True,
        "Task 008B losing outcomes must remain visible",
    )
    _require(
        fixture_collection_report.get("learning_proposals_reviewable_not_auto_applied") is True,
        "Task 008B learning proposals must remain reviewable and not auto-applied",
    )

    paper_order_report = _require_mapping(
        task_008c.get("paper_order_validation_report"),
        "source_reports.task_008c.paper_order_validation_report",
    )
    _require(paper_order_report.get("validation_status") == "passed", "Task 008C evidence must pass")
    _require(paper_order_report.get("would_create_order") is False, "Task 008C must not create paper orders")
    validated_order = _require_mapping(
        paper_order_report.get("validated_order"),
        "source_reports.task_008c.paper_order_validation_report.validated_order",
    )
    validated_order_before = deepcopy(dict(validated_order))
    task_008c_revalidation = validate_local_paper_order_intent(
        validated_order,
        portfolio_registry=_portfolio_registry(),
    )
    _require(
        dict(validated_order) == validated_order_before,
        "Task 008C paper-order evidence revalidation must not mutate inputs",
    )
    _require(
        task_008c_revalidation.get("would_create_order") is False,
        "Task 008C paper-order evidence revalidation must not create paper orders",
    )

    readiness_report = _require_mapping(
        task_008e.get("readiness_report"),
        "source_reports.task_008e.readiness_report",
    )
    stored_readiness_validation = _require_mapping(
        task_008e.get("readiness_validation"),
        "source_reports.task_008e.readiness_validation",
    )
    _require(
        stored_readiness_validation.get("validation_status") == "passed",
        "Task 008E stored readiness validation evidence must pass",
    )
    readiness_validation = validate_simulation_desk_readiness_report(readiness_report)
    _require(readiness_validation.get("validation_status") == "passed", "Task 008E readiness evidence must pass")

    scenario_matrix = _require_mapping(pack.get("scenario_matrix"), "scenario_matrix")
    order_scenarios = _require_mapping(
        scenario_matrix.get("paper_order_intent_scenarios"),
        "scenario_matrix.paper_order_intent_scenarios",
    )
    valid_scenario = _require_mapping(
        order_scenarios.get("valid_paper_order_intent"),
        "scenario_matrix.paper_order_intent_scenarios.valid_paper_order_intent",
    )
    _require(valid_scenario.get("validation_status") == "passed", "valid paper-order intent scenario must pass")
    _require(valid_scenario.get("expected_status") == "passed", "valid paper-order intent scenario expected_status must pass")
    _require(valid_scenario.get("would_create_order") is False, "valid scenario must not create a paper order")
    _require(valid_scenario.get("mutated_inputs") is False, "valid scenario validation must not mutate inputs")
    valid_input_order = _require_mapping(
        valid_scenario.get("input_order"),
        "scenario_matrix.paper_order_intent_scenarios.valid_paper_order_intent.input_order",
    )
    valid_input_before = deepcopy(dict(valid_input_order))
    valid_revalidation = validate_local_paper_order_intent(
        valid_input_order,
        portfolio_registry=_portfolio_registry(),
    )
    _require(
        dict(valid_input_order) == valid_input_before,
        "valid paper-order intent scenario revalidation must not mutate inputs",
    )
    _require(valid_revalidation.get("would_create_order") is False, "valid scenario revalidation must not create a paper order")
    stored_valid_result = _require_mapping(
        valid_scenario.get("validation_result"),
        "scenario_matrix.paper_order_intent_scenarios.valid_paper_order_intent.validation_result",
    )
    _require(
        stored_valid_result.get("would_create_order") is False,
        "valid scenario stored validation_result must not claim paper-order creation",
    )
    _require(
        dict(stored_valid_result) == valid_revalidation,
        "valid scenario stored validation_result must match fresh local revalidation",
    )

    for scenario_name, expected_error_fragment in INVALID_SCENARIO_EXPECTATIONS.items():
        scenario = _require_mapping(order_scenarios.get(scenario_name), f"scenario {scenario_name}")
        _require(
            scenario.get("validation_status") == "failed_safely",
            f"{scenario_name} must fail safely",
        )
        _require(
            scenario.get("expected_status") == "failed_safely",
            f"{scenario_name} expected_status must remain failed_safely",
        )
        _require(scenario.get("would_create_order") is False, f"{scenario_name} must not create a paper order")
        _require(scenario.get("mutated_inputs") is False, f"{scenario_name} validation must not mutate inputs")
        _require(
            expected_error_fragment in str(scenario.get("error_message")),
            f"{scenario_name} must preserve expected fail-safe error evidence",
        )
        invalid_input_order = _require_mapping(
            scenario.get("input_order"),
            f"scenario {scenario_name}.input_order",
        )
        invalid_input_before = deepcopy(dict(invalid_input_order))
        try:
            validate_local_paper_order_intent(
                invalid_input_order,
                portfolio_registry=_portfolio_registry(),
            )
        except ValueError as exc:
            _require(
                dict(invalid_input_order) == invalid_input_before,
                f"{scenario_name} fail-safe revalidation must not mutate inputs",
            )
            _require(
                expected_error_fragment in str(exc),
                f"{scenario_name} input_order must still fail for the expected reason",
            )
        else:
            raise ValueError(
                "Simulation Desk scenario pack validation failed: "
                f"{scenario_name} input_order must fail safely during revalidation"
            )

    readiness_scenario = _require_mapping(
        scenario_matrix.get("readiness_aggregation"),
        "scenario_matrix.readiness_aggregation",
    )
    _require(readiness_scenario.get("validation_status") == "passed", "readiness aggregation scenario must pass")
    _require(readiness_scenario.get("would_create_order") is False, "readiness aggregation must not create orders")

    schema_references = _require_mapping(
        pack.get("canonical_schema_table_references_preserved"),
        "canonical_schema_table_references_preserved",
    )
    _require(
        dict(schema_references) == CANONICAL_SCHEMA_TABLE_NAMES,
        "canonical schema table names must be preserved",
    )
    endpoints = _require_sequence(
        pack.get("locked_endpoint_names_referenced_without_implementation"),
        "locked_endpoint_names_referenced_without_implementation",
    )
    _require(
        list(endpoints) == list(LOCKED_ENDPOINT_NAMES),
        "locked endpoint names must be referenced without implementation",
    )

    gate_status = _require_mapping(pack.get("approval_gate_status"), "approval_gate_status")
    missing_gates = sorted(set(SCENARIO_APPROVAL_GATES_NOT_CROSSED) - set(gate_status))
    unexpected_gates = sorted(set(gate_status) - set(SCENARIO_APPROVAL_GATES_NOT_CROSSED))
    _require(not missing_gates, f"approval_gate_status missing required gates: {missing_gates}")
    _require(not unexpected_gates, f"approval_gate_status contains unexpected gates: {unexpected_gates}")
    crossed_gates = sorted(
        gate_name
        for gate_name in SCENARIO_APPROVAL_GATES_NOT_CROSSED
        if gate_status.get(gate_name) is not False
    )
    _require(not crossed_gates, f"approval gates must remain not crossed: {crossed_gates}")

    boundary_flags = _require_mapping(pack.get("boundary_flags"), "boundary_flags")
    missing_flags = sorted(set(SCENARIO_BOUNDARY_FLAG_NAMES) - set(boundary_flags))
    unexpected_flags = sorted(set(boundary_flags) - set(SCENARIO_BOUNDARY_FLAG_NAMES))
    _require(not missing_flags, f"boundary_flags missing required flags: {missing_flags}")
    _require(not unexpected_flags, f"boundary_flags contains unexpected flags: {unexpected_flags}")
    enabled_flags = sorted(
        flag_name
        for flag_name in SCENARIO_BOUNDARY_FLAG_NAMES
        if boundary_flags.get(flag_name) is not False
    )
    _require(not enabled_flags, f"forbidden boundary flags must remain false: {enabled_flags}")

    loss_evidence = _require_mapping(pack.get("loss_visibility_evidence"), "loss_visibility_evidence")
    _require(loss_evidence.get("losing_outcomes_remain_visible") is True, "losing simulation outcomes must remain visible")
    _require(loss_evidence.get("hidden_or_overwritten_losing_outcomes") is False, "losing simulations must not be hidden or overwritten")
    loss_records = _require_sequence(loss_evidence.get("records"), "loss_visibility_evidence.records")
    _require(bool(loss_records), "loss visibility evidence must include at least one losing record")
    hidden_loss_records = []
    for index, record in enumerate(loss_records):
        record_mapping = _require_mapping(record, f"loss_visibility_evidence.records[{index}]")
        if record_mapping.get("outcome_label") == "loss":
            if record_mapping.get("losing_outcome_visible") is not True:
                hidden_loss_records.append(record_mapping.get("record_id"))
    _require(
        not hidden_loss_records,
        f"losing simulation outcomes must remain visible: {hidden_loss_records}",
    )

    learning_evidence = _require_mapping(
        pack.get("learning_proposal_reviewability_evidence"),
        "learning_proposal_reviewability_evidence",
    )
    _require(learning_evidence.get("learning_proposals_remain_reviewable") is True, "learning proposals must remain reviewable")
    _require(learning_evidence.get("learning_proposals_auto_applied") is False, "learning proposals must not be auto-applied")
    learning_proposals = _require_sequence(
        learning_evidence.get("proposals"),
        "learning_proposal_reviewability_evidence.proposals",
    )
    _require(bool(learning_proposals), "learning proposal evidence must include proposals")
    non_reviewable_or_auto_applied_proposals = []
    for index, proposal in enumerate(learning_proposals):
        proposal_mapping = _require_mapping(
            proposal,
            f"learning_proposal_reviewability_evidence.proposals[{index}]",
        )
        if (
            proposal_mapping.get("reviewable") is not True
            or proposal_mapping.get("auto_applied") is not False
        ):
            non_reviewable_or_auto_applied_proposals.append(proposal_mapping.get("record_id"))
    _require(
        not non_reviewable_or_auto_applied_proposals,
        "learning proposals must remain reviewable and not auto-applied: "
        f"{non_reviewable_or_auto_applied_proposals}",
    )

    for field_name in (
        "advisory_only",
        "simulation_only",
        "human_in_the_loop",
        "deterministic",
        "in_memory",
        "non_persistent",
        "local_only",
        "task_008f_does_not_close_m5",
    ):
        _require(pack.get(field_name) is True, f"{field_name} must be true")
    _require(pack.get("m5_status") == "In Progress", "Task 008F must not imply M5 is closed")

    next_gate_matrix = _require_sequence(pack.get("next_gate_matrix"), "next_gate_matrix")
    _require(next_gate_matrix, "next_gate_matrix must record possible future gate directions")
    gate_directions = []
    approved_gate_directions = []
    for index, gate in enumerate(next_gate_matrix):
        gate_mapping = _require_mapping(gate, f"next_gate_matrix[{index}]")
        gate_direction = gate_mapping.get("gate_direction")
        gate_directions.append(gate_direction)
        if gate_mapping.get("task_008f_approves_gate") is not False:
            approved_gate_directions.append(gate_direction)
        _require(
            gate_mapping.get("future_task_required")
            == "008G or later with explicit Harness Engineering approval",
            f"next_gate_matrix[{index}] must require explicit future Harness Engineering approval",
        )
    _require(
        gate_directions == list(NEXT_GATE_DIRECTIONS),
        "next_gate_matrix must preserve every possible Task 008G direction without changes",
    )
    _require(
        not approved_gate_directions,
        f"Task 008F must not approve next gates: {approved_gate_directions}",
    )

    _require(dict(pack) == before_validation, "scenario pack validation must not mutate inputs")

    return {
        "validation_status": "passed",
        "task_id": TASK_ID,
        "source_tasks": list(SOURCE_TASKS),
        "boundary_flags": _boundary_flags(),
        "approval_gate_status": _approval_gate_status(),
        "would_create_order": False,
        "validation_mutates_inputs": False,
    }
