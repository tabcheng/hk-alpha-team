from __future__ import annotations

from copy import deepcopy
from typing import Any

SimulationRecord = dict[str, Any]
SimulationFixtureCollection = list[SimulationRecord]

EXPECTED_SIMULATION_RECORD_TYPES = (
    "paper_portfolio",
    "paper_order_intent",
    "paper_position",
    "portfolio_snapshot",
    "trade_review",
    "learning_proposal",
    "audit_event",
)

CANONICAL_SCHEMA_TABLE_NAMES = {
    "paper_portfolio": "paper_portfolios",
    "paper_order_intent": "paper_orders",
    "paper_position": "paper_positions",
    "portfolio_snapshot": "portfolio_snapshots",
    "trade_review": "trade_reviews",
    "learning_proposal": "learning_proposals",
    "audit_event": "audit_events",
}

LOCKED_ENDPOINT_NAMES = (
    "POST /api/v1/simulation/paper-orders",
    "GET /api/v1/paper-portfolios/{portfolio_id}",
    "POST /api/v1/strategy-recommendations",
    "GET /api/v1/strategy-recommendations/{recommendation_id}",
)

BOUNDARY_FLAG_NAMES = (
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
    "real_money_order_placed",
    "real_money_trading_automation_enabled",
)

REQUIRED_FIELDS_BY_RECORD_TYPE = {
    "paper_portfolio": {
        "record_id",
        "record_type",
        "canonical_schema_table",
        "portfolio_uuid",
        "name",
        "base_currency",
        "starting_cash",
        "status",
        "created_at",
        "boundary_flags",
        "locked_endpoint_references",
    },
    "paper_order_intent": {
        "record_id",
        "record_type",
        "canonical_schema_table",
        "portfolio_id",
        "stock_id",
        "strategy_recommendation_id",
        "side",
        "order_type",
        "quantity",
        "limit_price",
        "status",
        "submitted_at",
        "filled_at",
        "created_at",
        "boundary_flags",
        "locked_endpoint_references",
    },
    "paper_position": {
        "record_id",
        "record_type",
        "canonical_schema_table",
        "portfolio_id",
        "stock_id",
        "opened_from_order_id",
        "side",
        "quantity",
        "avg_entry_price",
        "avg_exit_price",
        "status",
        "outcome_label",
        "losing_outcome_visible",
        "opened_at",
        "closed_at",
        "created_at",
        "boundary_flags",
        "locked_endpoint_references",
    },
    "portfolio_snapshot": {
        "record_id",
        "record_type",
        "canonical_schema_table",
        "portfolio_id",
        "snapshot_time",
        "nav",
        "cash",
        "gross_exposure",
        "net_exposure",
        "drawdown_pct",
        "created_at",
        "boundary_flags",
        "locked_endpoint_references",
    },
    "trade_review": {
        "record_id",
        "record_type",
        "canonical_schema_table",
        "paper_position_id",
        "outcome_label",
        "losing_outcome_visible",
        "review_notes",
        "mistake_tags_json",
        "what_worked_json",
        "what_failed_json",
        "reviewed_at",
        "created_at",
        "boundary_flags",
        "locked_endpoint_references",
    },
    "learning_proposal": {
        "record_id",
        "record_type",
        "canonical_schema_table",
        "source_type",
        "source_id",
        "title",
        "proposal_text",
        "expected_impact",
        "risk_of_change",
        "status",
        "reviewable",
        "auto_applied",
        "created_at",
        "updated_at",
        "boundary_flags",
        "locked_endpoint_references",
    },
    "audit_event": {
        "record_id",
        "record_type",
        "canonical_schema_table",
        "event_uuid",
        "event_type",
        "entity_type",
        "entity_id",
        "actor_type",
        "actor_id",
        "event_payload_json",
        "created_at",
        "boundary_flags",
        "locked_endpoint_references",
    },
}

VALID_STATUSES_BY_RECORD_TYPE = {
    "paper_portfolio": {"active", "archived"},
    "paper_order_intent": {
        "draft_intent",
        "submitted_for_simulation",
        "simulated_filled",
        "cancelled",
    },
    "paper_position": {"open", "closed"},
    "learning_proposal": {"proposed", "under_review", "accepted_for_future_task", "rejected"},
}

VALID_OUTCOME_LABELS = {"win", "loss", "breakeven", "open"}
VALID_ORDER_SIDES = {"buy", "sell"}
VALID_POSITION_SIDES = {"long", "short"}
VALID_ORDER_TYPES = {"market", "limit"}


def _boundary_flags() -> dict[str, bool]:
    return {flag_name: False for flag_name in BOUNDARY_FLAG_NAMES}


def _locked_endpoint_references() -> list[str]:
    return list(LOCKED_ENDPOINT_NAMES)


def build_simulation_contract_fixtures() -> SimulationFixtureCollection:
    """Return deterministic local-only Task 008B Simulation Desk contract fixtures."""

    boundary_flags = _boundary_flags()
    endpoints = _locked_endpoint_references
    return [
        {
            "record_id": "fixture-paper-portfolio-001",
            "record_type": "paper_portfolio",
            "canonical_schema_table": "paper_portfolios",
            "portfolio_uuid": "paper-portfolio-fixture-001",
            "name": "Task 008B Local Simulation Portfolio",
            "base_currency": "HKD",
            "starting_cash": 100000.0,
            "status": "active",
            "created_at": "2026-06-04T00:00:00Z",
            "boundary_flags": deepcopy(boundary_flags),
            "locked_endpoint_references": endpoints(),
        },
        {
            "record_id": "fixture-paper-order-intent-001",
            "record_type": "paper_order_intent",
            "canonical_schema_table": "paper_orders",
            "portfolio_id": "fixture-paper-portfolio-001",
            "stock_id": "fixture-stock-0700-hk",
            "strategy_recommendation_id": "fixture-strategy-recommendation-001",
            "side": "buy",
            "order_type": "limit",
            "quantity": 100,
            "limit_price": 375.5,
            "status": "draft_intent",
            "submitted_at": None,
            "filled_at": None,
            "created_at": "2026-06-04T00:01:00Z",
            "boundary_flags": deepcopy(boundary_flags),
            "locked_endpoint_references": endpoints(),
        },
        {
            "record_id": "fixture-paper-position-001",
            "record_type": "paper_position",
            "canonical_schema_table": "paper_positions",
            "portfolio_id": "fixture-paper-portfolio-001",
            "stock_id": "fixture-stock-0700-hk",
            "opened_from_order_id": "fixture-paper-order-intent-001",
            "side": "long",
            "quantity": 100,
            "avg_entry_price": 375.5,
            "avg_exit_price": 360.0,
            "status": "closed",
            "outcome_label": "loss",
            "losing_outcome_visible": True,
            "opened_at": "2026-06-04T00:02:00Z",
            "closed_at": "2026-06-04T00:03:00Z",
            "created_at": "2026-06-04T00:02:00Z",
            "boundary_flags": deepcopy(boundary_flags),
            "locked_endpoint_references": endpoints(),
        },
        {
            "record_id": "fixture-portfolio-snapshot-001",
            "record_type": "portfolio_snapshot",
            "canonical_schema_table": "portfolio_snapshots",
            "portfolio_id": "fixture-paper-portfolio-001",
            "snapshot_time": "2026-06-04T00:04:00Z",
            "nav": 98450.0,
            "cash": 62450.0,
            "gross_exposure": 36000.0,
            "net_exposure": 36000.0,
            "drawdown_pct": 1.55,
            "created_at": "2026-06-04T00:04:00Z",
            "boundary_flags": deepcopy(boundary_flags),
            "locked_endpoint_references": endpoints(),
        },
        {
            "record_id": "fixture-trade-review-001",
            "record_type": "trade_review",
            "canonical_schema_table": "trade_reviews",
            "paper_position_id": "fixture-paper-position-001",
            "outcome_label": "loss",
            "losing_outcome_visible": True,
            "review_notes": (
                "Loss remains visible for review; no historical result is hidden or overwritten."
            ),
            "mistake_tags_json": ["entry_timing", "insufficient_pullback"],
            "what_worked_json": ["risk was bounded in paper-only simulation"],
            "what_failed_json": ["entry did not wait for stronger confirmation"],
            "reviewed_at": "2026-06-04T00:05:00Z",
            "created_at": "2026-06-04T00:05:00Z",
            "boundary_flags": deepcopy(boundary_flags),
            "locked_endpoint_references": endpoints(),
        },
        {
            "record_id": "fixture-learning-proposal-001",
            "record_type": "learning_proposal",
            "canonical_schema_table": "learning_proposals",
            "source_type": "trade_review",
            "source_id": "fixture-trade-review-001",
            "title": "Require pullback confirmation before similar paper entries",
            "proposal_text": (
                "Review whether future paper-order intents should require a stronger pullback gate."
            ),
            "expected_impact": "May reduce premature simulated entries.",
            "risk_of_change": "Could miss some momentum continuation opportunities.",
            "status": "proposed",
            "reviewable": True,
            "auto_applied": False,
            "created_at": "2026-06-04T00:06:00Z",
            "updated_at": "2026-06-04T00:06:00Z",
            "boundary_flags": deepcopy(boundary_flags),
            "locked_endpoint_references": endpoints(),
        },
        {
            "record_id": "fixture-audit-event-001",
            "record_type": "audit_event",
            "canonical_schema_table": "audit_events",
            "event_uuid": "audit-event-fixture-001",
            "event_type": "local_fixture_validated",
            "entity_type": "simulation_contract_fixture_collection",
            "entity_id": "task-008b-local-fixtures",
            "actor_type": "codex_local_validation",
            "actor_id": "task-008b",
            "event_payload_json": {
                "boundary": "local_only",
                "append_only_reference": True,
                "database_write_occurred": False,
            },
            "created_at": "2026-06-04T00:07:00Z",
            "boundary_flags": deepcopy(boundary_flags),
            "locked_endpoint_references": endpoints(),
        },
    ]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"Simulation contract validation failed: {message}")


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{field_name} must be a mapping")
    return value


def _require_sequence(value: Any, field_name: str) -> list[Any]:
    _require(isinstance(value, list), f"{field_name} must be a list")
    return value


def _is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _require_non_negative_number(value: Any, field_name: str) -> None:
    _require(_is_number(value), f"{field_name} must be numeric")
    _require(value >= 0, f"{field_name} must be non-negative")


def _require_positive_number(value: Any, field_name: str) -> None:
    _require(_is_number(value), f"{field_name} must be numeric")
    _require(value > 0, f"{field_name} must be positive")


def _validate_boundary_flags(record: SimulationRecord) -> dict[str, bool]:
    flags = _require_mapping(record.get("boundary_flags"), "boundary_flags")
    missing = sorted(set(BOUNDARY_FLAG_NAMES) - set(flags))
    unexpected = sorted(set(flags) - set(BOUNDARY_FLAG_NAMES))
    _require(not missing, f"boundary_flags missing required flags: {missing}")
    _require(not unexpected, f"boundary_flags contains unexpected flags: {unexpected}")
    enabled_flags = sorted(
        flag_name
        for flag_name in BOUNDARY_FLAG_NAMES
        if flags.get(flag_name) is not False
    )
    _require(not enabled_flags, f"boundary flags must remain false: {enabled_flags}")
    return {flag_name: bool(flags[flag_name]) for flag_name in BOUNDARY_FLAG_NAMES}


def validate_simulation_record(record: SimulationRecord) -> dict[str, Any]:
    """Validate one local-only Simulation Desk contract record without mutating it."""

    _require_mapping(record, "record")
    before_validation = deepcopy(record)
    record_type = record.get("record_type")
    _require(
        record_type in EXPECTED_SIMULATION_RECORD_TYPES,
        f"unknown record_type: {record_type!r}",
    )

    expected_fields = REQUIRED_FIELDS_BY_RECORD_TYPE[str(record_type)]
    missing = sorted(expected_fields - set(record))
    _require(not missing, f"{record_type} missing required fields: {missing}")
    expected_schema_table = CANONICAL_SCHEMA_TABLE_NAMES[str(record_type)]
    _require(
        record.get("canonical_schema_table") == expected_schema_table,
        f"{record_type} canonical_schema_table must reference {expected_schema_table!r}",
    )

    endpoints = _require_sequence(
        record.get("locked_endpoint_references"),
        "locked_endpoint_references",
    )
    unknown_endpoints = sorted(set(endpoints) - set(LOCKED_ENDPOINT_NAMES))
    missing_endpoints = sorted(set(LOCKED_ENDPOINT_NAMES) - set(endpoints))
    _require(
        not unknown_endpoints,
        f"locked endpoint references contain unknown names: {unknown_endpoints}",
    )
    _require(
        not missing_endpoints,
        f"locked endpoint references missing required names: {missing_endpoints}",
    )
    boundary_flags = _validate_boundary_flags(record)

    if record_type == "paper_order_intent":
        _require(
            record.get("side") in VALID_ORDER_SIDES,
            "paper_order_intent side must be buy or sell",
        )
        _require(
            record.get("order_type") in VALID_ORDER_TYPES,
            "paper_order_intent order_type must be market or limit",
        )
        _require(
            record.get("status") in VALID_STATUSES_BY_RECORD_TYPE["paper_order_intent"],
            "paper_order_intent status is invalid",
        )
        _require_positive_number(record.get("quantity"), "paper_order_intent quantity")
        if record.get("limit_price") is not None:
            _require_non_negative_number(
                record.get("limit_price"),
                "paper_order_intent limit_price",
            )
    elif record_type == "paper_position":
        _require(
            record.get("side") in VALID_POSITION_SIDES,
            "paper_position side must be long or short",
        )
        _require(
            record.get("status") in VALID_STATUSES_BY_RECORD_TYPE["paper_position"],
            "paper_position status is invalid",
        )
        _require(
            record.get("outcome_label") in VALID_OUTCOME_LABELS,
            "paper_position outcome_label is invalid",
        )
        _require_positive_number(record.get("quantity"), "paper_position quantity")
        _require_non_negative_number(
            record.get("avg_entry_price"),
            "paper_position avg_entry_price",
        )
        if record.get("avg_exit_price") is not None:
            _require_non_negative_number(
                record.get("avg_exit_price"),
                "paper_position avg_exit_price",
            )
        if record.get("outcome_label") == "loss":
            _require(
                record.get("losing_outcome_visible") is True,
                "losing outcome must remain visible",
            )
    elif record_type == "trade_review":
        _require(
            record.get("outcome_label") in VALID_OUTCOME_LABELS,
            "trade_review outcome_label is invalid",
        )
        if record.get("outcome_label") == "loss":
            _require(
                record.get("losing_outcome_visible") is True,
                "losing outcome must remain visible",
            )
    elif record_type == "learning_proposal":
        _require(
            record.get("status") in VALID_STATUSES_BY_RECORD_TYPE["learning_proposal"],
            "learning_proposal status is invalid",
        )
        _require(
            record.get("reviewable") is True,
            "learning_proposal must remain reviewable",
        )
        _require(
            record.get("auto_applied") is False,
            "learning_proposal must not be auto-applied",
        )
    elif record_type == "paper_portfolio":
        _require(
            record.get("status") in VALID_STATUSES_BY_RECORD_TYPE["paper_portfolio"],
            "paper_portfolio status is invalid",
        )
        _require_non_negative_number(
            record.get("starting_cash"),
            "paper_portfolio starting_cash",
        )
    elif record_type == "portfolio_snapshot":
        for numeric_field in (
            "nav",
            "cash",
            "gross_exposure",
            "net_exposure",
            "drawdown_pct",
        ):
            _require_non_negative_number(
                record.get(numeric_field),
                f"portfolio_snapshot {numeric_field}",
            )

    _require(record == before_validation, "record validation must not mutate inputs")

    return {
        "validation_status": "passed",
        "record_type": record_type,
        "canonical_schema_table": record["canonical_schema_table"],
        "locked_endpoint_references": list(endpoints),
        "boundary_flags": boundary_flags,
    }


def validate_simulation_fixture_collection(records: SimulationFixtureCollection) -> dict[str, Any]:
    """Validate a full local fixture collection without mutating it."""

    _require_sequence(records, "records")
    before_validation = deepcopy(records)
    record_reports = [validate_simulation_record(record) for record in records]
    present_record_types = tuple(report["record_type"] for report in record_reports)
    _require(
        set(present_record_types) == set(EXPECTED_SIMULATION_RECORD_TYPES),
        "fixture collection must contain all expected record types: "
        f"missing={sorted(set(EXPECTED_SIMULATION_RECORD_TYPES) - set(present_record_types))}; "
        f"unexpected={sorted(set(present_record_types) - set(EXPECTED_SIMULATION_RECORD_TYPES))}",
    )
    _require(
        len(present_record_types) == len(set(present_record_types)),
        f"fixture collection must contain one fixture per record type: {present_record_types}",
    )

    schema_names = tuple(report["canonical_schema_table"] for report in record_reports)
    _require(
        set(schema_names) == set(CANONICAL_SCHEMA_TABLE_NAMES.values()),
        "fixture collection must reference canonical schema names without renaming",
    )

    endpoint_references = sorted(
        {
            endpoint
            for report in record_reports
            for endpoint in report["locked_endpoint_references"]
        }
    )
    _require(
        set(endpoint_references) == set(LOCKED_ENDPOINT_NAMES),
        "fixture collection must reference locked endpoint names without implementation: "
        f"missing={sorted(set(LOCKED_ENDPOINT_NAMES) - set(endpoint_references))}; "
        f"unexpected={sorted(set(endpoint_references) - set(LOCKED_ENDPOINT_NAMES))}",
    )

    losing_records = [
        record
        for record in records
        if record.get("outcome_label") == "loss" or record.get("drawdown_pct", 0) > 0
    ]
    hidden_losing_records = [
        record.get("record_id")
        for record in losing_records
        if record.get("outcome_label") == "loss"
        and record.get("losing_outcome_visible") is not True
    ]
    _require(losing_records, "fixture collection must include visible losing outcomes")
    _require(
        not hidden_losing_records,
        f"losing outcomes must remain visible: {hidden_losing_records}",
    )

    learning_proposals = [
        record for record in records if record.get("record_type") == "learning_proposal"
    ]
    _require(learning_proposals, "fixture collection must include a learning_proposal")
    _require(
        all(
            record.get("reviewable") is True and record.get("auto_applied") is False
            for record in learning_proposals
        ),
        "learning proposals must be reviewable and not auto-applied",
    )
    _require(records == before_validation, "collection validation must not mutate inputs")

    return {
        "validation_status": "passed",
        "record_count": len(record_reports),
        "expected_record_types": list(EXPECTED_SIMULATION_RECORD_TYPES),
        "present_record_types": list(present_record_types),
        "canonical_schema_names": list(schema_names),
        "locked_endpoint_names": list(LOCKED_ENDPOINT_NAMES),
        "locked_endpoint_names_referenced_without_implementation": True,
        "losing_outcomes_remain_visible": True,
        "learning_proposals_reviewable_not_auto_applied": True,
        "boundary_flags": {flag_name: False for flag_name in BOUNDARY_FLAG_NAMES},
        "validation_mutates_inputs": False,
    }


def build_simulation_validation_matrix(
    records: SimulationFixtureCollection | None = None,
) -> dict[str, Any]:
    """Build a Task 008B fixture coverage and boundary-compliance matrix."""

    fixture_records = build_simulation_contract_fixtures() if records is None else records
    collection_report = validate_simulation_fixture_collection(fixture_records)
    boundary_flags = collection_report["boundary_flags"]
    matrix_name = (
        "Task 008B — Local-only Simulation Contract Fixtures, "
        "Schemas, and Validation Matrix"
    )
    return {
        "matrix_name": matrix_name,
        "validation_status": collection_report["validation_status"],
        "record_type_coverage": {
            record_type: record_type in collection_report["present_record_types"]
            for record_type in EXPECTED_SIMULATION_RECORD_TYPES
        },
        "canonical_schema_names_referenced_without_renaming": {
            record_type: CANONICAL_SCHEMA_TABLE_NAMES[record_type]
            for record_type in EXPECTED_SIMULATION_RECORD_TYPES
        },
        "locked_endpoint_names_referenced_without_implementation": list(
            LOCKED_ENDPOINT_NAMES
        ),
        "boundary_compliance": {
            "losing_outcomes_remain_visible": collection_report[
                "losing_outcomes_remain_visible"
            ],
            "learning_proposals_reviewable_not_auto_applied": collection_report[
                "learning_proposals_reviewable_not_auto_applied"
            ],
            "no_persistence_flags_enabled": boundary_flags["persistence_enabled"] is False,
            "no_production_supabase_flags_enabled": (
                boundary_flags["production_supabase_required"] is False
                and boundary_flags["production_supabase_connected"] is False
            ),
            "no_broker_or_real_money_flags_enabled": (
                boundary_flags["broker_execution_enabled"] is False
                and boundary_flags["real_money_order_placed"] is False
            ),
            "no_endpoint_runtime_flag_enabled": (
                boundary_flags["endpoint_runtime_enabled"] is False
            ),
            "validation_does_not_mutate_inputs": (
                collection_report["validation_mutates_inputs"] is False
            ),
        },
        "non_goals": [
            "no IO",
            "no HTTP",
            "no database",
            "no Supabase",
            "no endpoint handlers",
            "no paper order creation",
            "no persistence",
            "no broker integration",
            "no real-money trading automation",
        ],
    }
