from __future__ import annotations

import ast
import socket
from pathlib import Path
from unittest.mock import patch

import pytest

from app.simulation_origin_contract import build_sample_simulation_origin_payload
from app.simulation_persistence_boundary import (
    FALSE_BOUNDARY_FLAGS,
    SimulationPersistenceBoundaryError,
    build_audit_event_persistence_payload,
    build_learning_proposal_persistence_payload,
    build_paper_order_persistence_payload,
    build_persistence_payload_bundle,
    build_portfolio_snapshot_persistence_payload,
)
from app.simulation_runtime import create_paper_order_record, build_paper_portfolio_snapshot
from app.simulation_store import simulation_store


def _runtime_record(origin: str) -> dict:
    payload = build_sample_simulation_origin_payload(origin)
    payload["portfolio_id"] = "runtime-paper-portfolio-001"
    payload["paper_only"] = True
    payload["boundary_flags"] = {flag_name: False for flag_name in FALSE_BOUNDARY_FLAGS}
    return create_paper_order_record(payload)["paper_order"]


@pytest.fixture(autouse=True)
def reset_store() -> None:
    simulation_store.reset()


def test_user_recorded_runtime_record_maps_to_paper_orders_intent() -> None:
    record = _runtime_record("user_recorded")

    payload = build_paper_order_persistence_payload(record)

    assert payload["target_table"] == "paper_orders"
    assert payload["persistence_intent_only"] is True
    assert payload["persistence_write_performed"] is False
    assert payload["production_supabase_connected"] is False
    assert payload["generated_from_runtime_record"] is True
    assert payload["simulation_origin"] == "user_recorded"
    assert payload["paper_order_origin"] == "user_recorded"
    assert payload["paper_only"] is True
    assert payload["advisory_only"] is True
    assert payload["human_in_the_loop"] is True
    assert payload["user_recorded_notes"] == record["source_metadata"]["user_recorded_notes"]
    assert payload["source_recommendation_id"] is None


def test_system_generated_learning_runtime_record_maps_to_paper_orders_intent() -> None:
    record = _runtime_record("system_generated_learning")

    payload = build_paper_order_persistence_payload(record)

    assert payload["target_table"] == "paper_orders"
    assert payload["simulation_origin"] == "system_generated_learning"
    assert payload["paper_order_origin"] == "system_generated_learning"
    assert payload["source_recommendation_id"] == "fixture-strategy-recommendation-001"
    assert payload["strategy_recommendation_id"] == "fixture-strategy-recommendation-001"
    assert payload["system_learning_reason"] == record["source_metadata"]["system_learning_reason"]
    assert payload["requires_human_review"] is True
    assert payload["outcome_preview_json"]["pnl"] == -1550.0


def test_learning_proposal_preview_maps_to_reviewable_non_auto_applied_intent() -> None:
    record = _runtime_record("system_generated_learning")

    payload = build_learning_proposal_persistence_payload(record)

    assert payload is not None
    assert payload["target_table"] == "learning_proposals"
    assert payload["simulation_origin"] == "system_generated_learning"
    assert payload["requires_human_review"] is True
    assert payload["auto_apply"] is False
    assert payload["proposals_reviewable"] is True
    assert payload["proposals_auto_applied"] is False
    assert payload["proposal_payload_json"]["status"] == "preview_only_not_applied"


def test_user_recorded_has_no_learning_proposal_intent() -> None:
    record = _runtime_record("user_recorded")

    assert build_learning_proposal_persistence_payload(record) is None


def test_audit_event_preview_maps_to_append_only_intent_metadata() -> None:
    record = _runtime_record("system_generated_learning")

    payload = build_audit_event_persistence_payload(record)

    assert payload["target_table"] == "audit_events"
    assert payload["append_only_intent"] is True
    assert payload["event_payload_json"]["preview_only"] is True
    assert payload["event_payload_json"]["persistence_write_performed"] is False
    assert payload["persistence_write_performed"] is False
    assert payload["entity_id"] == record["paper_order_id"]


def test_paper_portfolio_snapshot_maps_to_portfolio_snapshots_intent() -> None:
    _runtime_record("user_recorded")
    _runtime_record("system_generated_learning")
    snapshot = build_paper_portfolio_snapshot("runtime-paper-portfolio-001")

    payload = build_portfolio_snapshot_persistence_payload(snapshot)

    assert payload["target_table"] == "portfolio_snapshots"
    assert payload["persistence_intent_only"] is True
    assert payload["recent_paper_order_count"] == 2
    assert payload["simulation_origin_summary_json"]["origin_counts"] == {
        "user_recorded": 1,
        "system_generated_learning": 1,
    }
    assert payload["simulation_origin"] == "system_generated_learning"


def test_origin_lineage_notes_loss_visibility_and_historical_fields_are_preserved_in_bundle() -> None:
    record = _runtime_record("system_generated_learning")

    bundle = build_persistence_payload_bundle(record)

    assert bundle["simulation_origin"] == "system_generated_learning"
    assert bundle["paper_order"]["source_recommendation_id"] == "fixture-strategy-recommendation-001"
    assert bundle["paper_order"]["source_metadata_json"]["system_learning_reason"]
    assert bundle["paper_order"]["outcome_preview_json"]["losing_outcome_visible"] is True
    assert bundle["paper_order"]["historical_recommendation_fields_json"]["original_recommendation"] == "WAIT_FOR_PULLBACK"
    assert bundle["paper_order"]["historical_recommendations_overwritten"] is False


def test_user_recorded_notes_are_preserved_in_bundle() -> None:
    record = _runtime_record("user_recorded")

    bundle = build_persistence_payload_bundle(record)

    assert bundle["paper_order"]["user_recorded_notes"] == "Human-recorded paper trade journal entry."
    assert bundle["learning_proposal"] is None


@pytest.mark.parametrize(
    "flag_name",
    [
        "real_money_order_placed",
        "broker_api_called",
        "production_supabase_connected",
        "persistence_write_performed",
        "external_api_called",
        "secrets_required",
    ],
)
def test_unsafe_false_boundary_flags_are_rejected(flag_name: str) -> None:
    record = _runtime_record("system_generated_learning")
    record[flag_name] = True

    with pytest.raises(SimulationPersistenceBoundaryError, match=flag_name):
        build_paper_order_persistence_payload(record)


@pytest.mark.parametrize(
    ("flag_name", "unsafe_value"),
    [
        ("proposals_auto_applied", True),
        ("losing_outcomes_remain_visible", False),
        ("historical_recommendations_overwritten", True),
    ],
)
def test_unsafe_learning_and_loss_guardrails_are_rejected(flag_name: str, unsafe_value: bool) -> None:
    record = _runtime_record("system_generated_learning")
    record[flag_name] = unsafe_value

    with pytest.raises(SimulationPersistenceBoundaryError, match=flag_name):
        build_persistence_payload_bundle(record)


def test_non_reviewable_or_auto_applied_learning_preview_is_rejected() -> None:
    record = _runtime_record("system_generated_learning")
    record["learning_proposal_preview"]["auto_apply"] = True

    with pytest.raises(SimulationPersistenceBoundaryError, match="auto-apply"):
        build_learning_proposal_persistence_payload(record)


def test_no_supabase_import_exists_in_boundary_module() -> None:
    source_path = Path("backend/app/simulation_persistence_boundary.py")
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.append(node.module)

    assert not any("supabase" in module.lower() for module in imported_modules)
    assert not any(module in {"requests", "httpx", "urllib.request", "sqlite3", "psycopg", "psycopg2"} for module in imported_modules)


def test_no_vendor_network_disk_or_database_dependency_is_used() -> None:
    record = _runtime_record("system_generated_learning")

    with patch("builtins.open", side_effect=AssertionError("disk write/read is not allowed")), patch.object(
        Path, "open", side_effect=AssertionError("disk write/read is not allowed")
    ), patch.object(socket.socket, "connect", side_effect=AssertionError("network is not allowed")):
        payload = build_persistence_payload_bundle(record)

    assert payload["persistence_intent_only"] is True
    assert payload["persistence_write_performed"] is False


def test_output_is_deterministic_for_identical_input() -> None:
    record = _runtime_record("system_generated_learning")

    first = build_persistence_payload_bundle(record)
    second = build_persistence_payload_bundle(record)

    assert first == second


def test_runtime_response_envelope_remains_untouched() -> None:
    from app.main import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    response = client.post("/api/v1/simulation/paper-orders", json={**build_sample_simulation_origin_payload("user_recorded"), "paper_only": True})

    assert response.status_code == 200
    payload = response.json()
    assert set(payload) == {"request_id", "status", "data", "metadata", "warnings"}


def test_missing_boundary_flags_are_rejected_instead_of_synthesized() -> None:
    record = _runtime_record("system_generated_learning")
    record.pop("external_api_called")

    with pytest.raises(SimulationPersistenceBoundaryError, match="external_api_called is required"):
        build_paper_order_persistence_payload(record)


def test_missing_nested_boundary_flags_are_rejected_instead_of_synthesized() -> None:
    record = _runtime_record("system_generated_learning")
    record["boundary_flags"].pop("broker_api_called")

    with pytest.raises(SimulationPersistenceBoundaryError, match="boundary_flags.broker_api_called is required"):
        build_persistence_payload_bundle(record)


def test_missing_learning_loss_guardrails_are_rejected_for_order_intents() -> None:
    record = _runtime_record("system_generated_learning")
    record.pop("losing_outcomes_remain_visible")

    with pytest.raises(SimulationPersistenceBoundaryError, match="losing_outcomes_remain_visible is required"):
        build_paper_order_persistence_payload(record)


def test_empty_portfolio_snapshot_is_rejected_without_synthesizing_an_origin() -> None:
    snapshot = {
        "portfolio_id": "runtime-paper-portfolio-empty",
        "status": "in_memory_only_non_production",
        "base_currency": "HKD",
        "cash_placeholder": {"amount": 0, "currency": "HKD", "source": "placeholder_not_broker_cash"},
        "nav_placeholder": {"amount": 0, "currency": "HKD", "source": "placeholder_not_market_valuation"},
        "recent_paper_orders": [],
        "audit_event_previews": [],
        "paper_only": True,
        "advisory_only": True,
        "human_in_the_loop": True,
        **{flag_name: False for flag_name in FALSE_BOUNDARY_FLAGS},
        "boundary_flags": {flag_name: False for flag_name in FALSE_BOUNDARY_FLAGS},
    }

    with pytest.raises(SimulationPersistenceBoundaryError, match="recent_paper_orders"):
        build_portfolio_snapshot_persistence_payload(snapshot)
