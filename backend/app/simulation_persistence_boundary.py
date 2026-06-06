from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

APPROVED_SIMULATION_ORIGINS = ("user_recorded", "system_generated_learning")

TRUE_BOUNDARY_FLAGS = (
    "paper_only",
    "advisory_only",
    "human_in_the_loop",
)

FALSE_BOUNDARY_FLAGS = (
    "real_money_order_placed",
    "real_money_trading_automation_enabled",
    "autonomous_real_money_execution",
    "broker_execution_enabled",
    "broker_api_called",
    "production_supabase_connected",
    "persistence_write_performed",
    "secrets_required",
    "external_api_called",
    "billing_runtime_enabled",
    "membership_runtime_enabled",
    "auth_runtime_enabled",
    "deployment_required",
)

LEARNING_LOSS_GUARDRAILS = {
    "proposals_reviewable": True,
    "proposals_auto_applied": False,
    "losing_outcomes_remain_visible": True,
    "historical_recommendations_overwritten": False,
}


class SimulationPersistenceBoundaryError(ValueError):
    """Raised when a runtime record cannot be represented as safe persistence intent."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SimulationPersistenceBoundaryError(message)


def _require_mapping(payload: Mapping[str, Any], label: str) -> dict[str, Any]:
    _require(isinstance(payload, Mapping), f"{label} must be a mapping")
    return deepcopy(dict(payload))


def _validate_origin(record: Mapping[str, Any]) -> str:
    origin = record.get("simulation_origin")
    _require(origin in APPROVED_SIMULATION_ORIGINS, "simulation_origin must remain an approved Simulation Desk origin")
    return str(origin)


def _validate_runtime_safety(record: Mapping[str, Any], *, require_learning_loss_guardrails: bool = True) -> None:
    for flag_name in TRUE_BOUNDARY_FLAGS:
        _require(flag_name in record, f"{flag_name} is required")
        _require(record[flag_name] is True, f"{flag_name} must be true")

    boundary_flags = record.get("boundary_flags")
    _require(isinstance(boundary_flags, Mapping), "boundary_flags must be a mapping")
    for flag_name in FALSE_BOUNDARY_FLAGS:
        _require(flag_name in record, f"{flag_name} is required")
        _require(record[flag_name] is False, f"{flag_name} must be false")
        _require(flag_name in boundary_flags, f"boundary_flags.{flag_name} is required")
        _require(boundary_flags[flag_name] is False, f"boundary_flags.{flag_name} must be false")

    if require_learning_loss_guardrails:
        for flag_name, expected in LEARNING_LOSS_GUARDRAILS.items():
            _require(flag_name in record, f"{flag_name} is required")
            _require(record[flag_name] is expected, f"{flag_name} must be {str(expected).lower()}")

    outcome_preview = record.get("outcome_preview")
    if isinstance(outcome_preview, Mapping) and "losing_outcome_visible" in outcome_preview:
        _require(outcome_preview["losing_outcome_visible"] is True, "outcome_preview.losing_outcome_visible must be true")

    proposal = record.get("learning_proposal_preview")
    if isinstance(proposal, Mapping):
        _require(proposal.get("requires_human_review") is True, "learning proposal preview must require human review")
        _require(proposal.get("auto_apply") is False, "learning proposal preview must not auto-apply")


def _intent_base(target_table: str, simulation_origin: str) -> dict[str, Any]:
    return {
        "target_table": target_table,
        "persistence_intent_only": True,
        "persistence_write_performed": False,
        "production_supabase_connected": False,
        "generated_from_runtime_record": True,
        "simulation_origin": simulation_origin,
        "paper_only": True,
        "advisory_only": True,
        "human_in_the_loop": True,
        **{flag_name: False for flag_name in FALSE_BOUNDARY_FLAGS},
        **deepcopy(LEARNING_LOSS_GUARDRAILS),
    }


def _boundary_flags_json() -> dict[str, bool]:
    return {
        "paper_only": True,
        "advisory_only": True,
        "human_in_the_loop": True,
        **{flag_name: False for flag_name in FALSE_BOUNDARY_FLAGS},
        **deepcopy(LEARNING_LOSS_GUARDRAILS),
    }


def build_paper_order_persistence_payload(runtime_record: Mapping[str, Any]) -> dict[str, Any]:
    """Build a deterministic paper_orders persistence-intent payload without IO."""

    record = _require_mapping(runtime_record, "runtime_record")
    _validate_runtime_safety(record)
    origin = _validate_origin(record)
    historical_fields = record.get("historical_recommendation_fields", {})
    source_metadata = record.get("source_metadata", {})
    _require(isinstance(historical_fields, Mapping), "historical_recommendation_fields must be a mapping")
    _require(isinstance(source_metadata, Mapping), "source_metadata must be a mapping")

    source_recommendation_id = historical_fields.get("source_recommendation_id")
    learning_preview = record.get("learning_proposal_preview")
    learning_proposal_id = None
    if isinstance(learning_preview, Mapping):
        learning_proposal_id = learning_preview.get("learning_proposal_preview_id") or learning_preview.get("proposal_id")

    return {
        **_intent_base("paper_orders", origin),
        "paper_order_id": record.get("paper_order_id"),
        "portfolio_id": record.get("portfolio_id"),
        "symbol": record.get("symbol"),
        "side": record.get("side"),
        "quantity": record.get("quantity"),
        "order_type": record.get("order_type"),
        "limit_price": record.get("limit_price"),
        "status": record.get("status"),
        "created_at": record.get("created_at"),
        "source_recommendation_id": source_recommendation_id,
        "strategy_recommendation_id": historical_fields.get("strategy_recommendation_id"),
        "paper_order_origin": origin,
        "created_by_type": record.get("created_by_type"),
        "user_recorded_notes": source_metadata.get("user_recorded_notes"),
        "system_learning_reason": source_metadata.get("system_learning_reason"),
        "requires_human_review": source_metadata.get("requires_human_review") is True or origin == "system_generated_learning",
        "learning_proposal_id": learning_proposal_id,
        "boundary_flags_json": _boundary_flags_json(),
        "outcome_preview_json": deepcopy(record.get("outcome_preview")),
        "historical_recommendation_fields_json": deepcopy(dict(historical_fields)),
        "source_metadata_json": deepcopy(dict(source_metadata)),
    }


def build_learning_proposal_persistence_payload(runtime_record: Mapping[str, Any]) -> dict[str, Any] | None:
    """Build a learning_proposals intent payload when a reviewable preview exists."""

    record = _require_mapping(runtime_record, "runtime_record")
    _validate_runtime_safety(record)
    origin = _validate_origin(record)
    preview = record.get("learning_proposal_preview")
    if preview is None:
        return None
    _require(isinstance(preview, Mapping), "learning_proposal_preview must be a mapping")
    _require(preview.get("requires_human_review") is True, "learning proposal intent requires human review")
    _require(preview.get("auto_apply") is False, "learning proposal intent must not auto-apply")

    return {
        **_intent_base("learning_proposals", origin),
        "learning_proposal_preview_id": preview.get("learning_proposal_preview_id"),
        "source_recommendation_id": preview.get("source_recommendation_id"),
        "proposal_type": preview.get("proposal_type"),
        "status": preview.get("status"),
        "requires_human_review": True,
        "auto_apply": False,
        "proposal_payload_json": deepcopy(dict(preview)),
        "system_learning_reason": preview.get("system_learning_reason"),
        "improvement_suggestions_json": deepcopy(preview.get("improvement_suggestions")),
    }


def build_audit_event_persistence_payload(runtime_record: Mapping[str, Any]) -> dict[str, Any]:
    """Build an append-only audit_events intent payload from a runtime audit preview."""

    record = _require_mapping(runtime_record, "runtime_record")
    _validate_runtime_safety(record)
    origin = _validate_origin(record)
    preview = record.get("audit_event_preview")
    _require(isinstance(preview, Mapping), "audit_event_preview must be a mapping")
    _require(preview.get("persistence_write_performed") is False, "audit preview must not represent a completed write")
    _require(preview.get("preview_only") is True, "audit preview must remain preview-only")

    return {
        **_intent_base("audit_events", origin),
        "audit_event_id": preview.get("audit_event_id"),
        "event_type": preview.get("event_type"),
        "entity_type": preview.get("entity_type"),
        "entity_id": preview.get("entity_id"),
        "actor_type": preview.get("actor_type"),
        "created_at": preview.get("timestamp"),
        "append_only_intent": True,
        "event_payload_json": deepcopy(dict(preview)),
    }


def build_portfolio_snapshot_persistence_payload(runtime_snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Build a deterministic portfolio_snapshots intent payload from a runtime portfolio snapshot."""

    snapshot = _require_mapping(runtime_snapshot, "runtime_snapshot")
    _validate_runtime_safety(snapshot, require_learning_loss_guardrails=False)
    orders = snapshot.get("recent_paper_orders", [])
    _require(isinstance(orders, list), "recent_paper_orders must be a list")
    _require(len(orders) > 0, "recent_paper_orders must include at least one runtime order")
    origins = [order.get("simulation_origin") for order in orders if isinstance(order, Mapping)]
    _require(len(origins) == len(orders), "recent_paper_orders must contain runtime order mappings")
    for origin in origins:
        _require(origin in APPROVED_SIMULATION_ORIGINS, "snapshot order origins must remain approved")
    origin_counts = {origin: origins.count(origin) for origin in APPROVED_SIMULATION_ORIGINS}
    primary_origin = origins[-1]

    return {
        **_intent_base("portfolio_snapshots", primary_origin),
        "simulation_origin": primary_origin,
        "portfolio_id": snapshot.get("portfolio_id"),
        "status": snapshot.get("status"),
        "base_currency": snapshot.get("base_currency"),
        "snapshot_time": None,
        "nav_placeholder_json": deepcopy(snapshot.get("nav_placeholder")),
        "cash_placeholder_json": deepcopy(snapshot.get("cash_placeholder")),
        "recent_paper_order_count": len(orders),
        "audit_event_preview_count": len(snapshot.get("audit_event_previews", [])),
        "simulation_origin_summary_json": {
            "approved_origins": list(APPROVED_SIMULATION_ORIGINS),
            "origin_counts": origin_counts,
            "primary_runtime_origin": primary_origin,
        },
    }


def build_persistence_payload_bundle(
    runtime_record: Mapping[str, Any],
    *,
    runtime_snapshot: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build all available Simulation Desk persistence-intent payloads without writing anywhere."""

    record = _require_mapping(runtime_record, "runtime_record")
    _validate_runtime_safety(record)
    origin = _validate_origin(record)
    bundle: dict[str, Any] = {
        "persistence_intent_only": True,
        "persistence_write_performed": False,
        "production_supabase_connected": False,
        "simulation_origin": origin,
        "paper_order": build_paper_order_persistence_payload(record),
        "audit_event": build_audit_event_persistence_payload(record),
        "learning_proposal": build_learning_proposal_persistence_payload(record),
    }
    if runtime_snapshot is not None:
        bundle["portfolio_snapshot"] = build_portfolio_snapshot_persistence_payload(runtime_snapshot)
    return bundle
