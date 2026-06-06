from __future__ import annotations

from pathlib import Path
from pprint import pformat
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.simulation_origin_contract import build_sample_simulation_origin_payload
from app.simulation_runtime import RUNTIME_FALSE_BOUNDARY_FLAGS, create_paper_order_record
from app.simulation_store import simulation_store

client = TestClient(app)


def _payload(origin: str) -> dict:
    payload = build_sample_simulation_origin_payload(origin)
    payload["portfolio_id"] = "runtime-paper-portfolio-001"
    payload["paper_only"] = True
    payload["boundary_flags"] = {flag_name: False for flag_name in RUNTIME_FALSE_BOUNDARY_FLAGS}
    return payload


@pytest.fixture(autouse=True)
def reset_store() -> None:
    simulation_store.reset()


def assert_success_envelope(payload: dict) -> None:
    assert set(payload) == {"request_id", "status", "data", "metadata", "warnings"}
    assert payload["request_id"]
    assert payload["status"] == "success"
    assert isinstance(payload["data"], dict)
    assert payload["metadata"]["schema_version"] == "v0.1"
    assert payload["metadata"]["source"] == "HK_ALPHA_TEAM"
    assert payload["metadata"]["generated_at"]
    assert isinstance(payload["warnings"], list)


def assert_error_envelope(payload: dict, code: str = "VALIDATION_ERROR") -> None:
    assert set(payload) == {"request_id", "status", "error"}
    assert payload["request_id"]
    assert payload["status"] == "error"
    assert payload["error"]["code"] == code
    assert payload["error"]["message"]
    assert isinstance(payload["error"]["details"], dict)


def error_details_text(payload: dict) -> str:
    return pformat(payload["error"]["details"])


def assert_runtime_warnings(warnings: list[str]) -> None:
    warning_text = " ".join(warnings).lower()
    for phrase in ["paper-only", "advisory-only", "no real-money", "no broker", "no production supabase"]:
        assert phrase in warning_text


def test_post_paper_orders_creates_user_recorded_in_memory_record() -> None:
    response = client.post("/api/v1/simulation/paper-orders", json=_payload("user_recorded"))
    assert response.status_code == 200
    payload = response.json()

    assert_success_envelope(payload)
    assert_runtime_warnings(payload["warnings"])
    record = payload["data"]["paper_order"]
    assert record["paper_order_id"] == "paper-order-000001"
    assert record["simulation_origin"] == "user_recorded"
    assert record["source_metadata"]["user_recorded_notes"]
    assert record["learning_proposal_preview"] is None
    assert record["paper_only"] is True
    assert record["real_money_order_placed"] is False
    assert record["broker_api_called"] is False
    assert record["production_supabase_connected"] is False
    assert record["persistence_write_performed"] is False
    assert record["secrets_required"] is False


def test_post_paper_orders_creates_system_generated_learning_record_with_reviewable_preview() -> None:
    response = client.post("/api/v1/simulation/paper-orders", json=_payload("system_generated_learning"))
    assert response.status_code == 200
    payload = response.json()

    assert_success_envelope(payload)
    record = payload["data"]["paper_order"]
    proposal = record["learning_proposal_preview"]
    assert record["simulation_origin"] == "system_generated_learning"
    assert record["outcome_preview"]["pnl"] == -1550.0
    assert record["outcome_preview"]["losing_outcome_visible"] is True
    assert record["historical_recommendation_fields"]["original_recommendation"] == "WAIT_FOR_PULLBACK"
    assert record["historical_recommendations_overwritten"] is False
    assert proposal["requires_human_review"] is True
    assert proposal["auto_apply"] is False
    assert proposal["status"] == "preview_only_not_applied"


def test_origins_are_distinguishable_in_responses() -> None:
    user_response = client.post("/api/v1/simulation/paper-orders", json=_payload("user_recorded")).json()
    system_response = client.post("/api/v1/simulation/paper-orders", json=_payload("system_generated_learning")).json()

    assert user_response["data"]["paper_order"]["simulation_origin"] == "user_recorded"
    assert system_response["data"]["paper_order"]["simulation_origin"] == "system_generated_learning"
    assert user_response["data"]["paper_order"]["paper_order_id"] == "paper-order-000001"
    assert system_response["data"]["paper_order"]["paper_order_id"] == "paper-order-000002"


@pytest.mark.parametrize(
    ("mutation", "expected_message"),
    [
        (lambda p: p.pop("simulation_origin"), "simulation_origin"),
        (lambda p: p.update({"simulation_origin": "broker_imported"}), "simulation_origin"),
        (lambda p: p.update({"portfolio_id": "invalid portfolio/id"}), "portfolio_id"),
        (lambda p: p.update({"symbol": "TENCENT"}), "symbol"),
        (lambda p: p.update({"side": "short"}), "side"),
        (lambda p: p.update({"quantity": -1}), "quantity"),
        (lambda p: p.update({"paper_only": False}), "paper_only"),
        (lambda p: p.update({"boundary_flags": []}), "boundary_flags"),
        (lambda p: p.pop("user_recorded_notes"), "user_recorded_notes"),
    ],
)
def test_invalid_user_recorded_payloads_fail(mutation, expected_message: str) -> None:
    payload = _payload("user_recorded")
    mutation(payload)

    response = client.post("/api/v1/simulation/paper-orders", json=payload)

    assert response.status_code == 422
    error_payload = response.json()
    assert_error_envelope(error_payload)
    assert expected_message in error_details_text(error_payload)


@pytest.mark.parametrize(
    ("field_name", "expected_message"),
    [
        ("source_recommendation_id", "source_recommendation_id"),
        ("original_scores", "original_scores"),
        ("original_thesis", "original_thesis"),
        ("entry_assumptions", "entry_assumptions"),
        ("exit_assumptions", "exit_assumptions"),
        ("system_learning_reason", "system_learning_reason"),
    ],
)
def test_missing_system_generated_learning_lineage_fields_fail(field_name: str, expected_message: str) -> None:
    payload = _payload("system_generated_learning")
    payload.pop(field_name)

    response = client.post("/api/v1/simulation/paper-orders", json=payload)

    assert response.status_code == 422
    error_payload = response.json()
    assert_error_envelope(error_payload)
    assert expected_message in error_details_text(error_payload)


def test_system_generated_learning_rejects_invalid_original_scores() -> None:
    payload = _payload("system_generated_learning")
    payload["original_scores"]["market_score"] = 101

    response = client.post("/api/v1/simulation/paper-orders", json=payload)

    assert response.status_code == 422
    assert "original_scores.market_score" in error_details_text(response.json())


def test_system_generated_learning_rejects_non_numeric_pnl() -> None:
    payload = _payload("system_generated_learning")
    payload["pnl"] = "loss"

    response = client.post("/api/v1/simulation/paper-orders", json=payload)

    assert response.status_code == 422
    assert "pnl" in error_details_text(response.json())


def test_system_generated_learning_requires_human_review_false_fails() -> None:
    payload = _payload("system_generated_learning")
    payload["requires_human_review"] = False

    response = client.post("/api/v1/simulation/paper-orders", json=payload)

    assert response.status_code == 422
    assert "requires_human_review" in error_details_text(response.json())


def test_auto_apply_true_fails() -> None:
    payload = _payload("system_generated_learning")
    payload["learning_proposal"]["auto_apply"] = True

    response = client.post("/api/v1/simulation/paper-orders", json=payload)

    assert response.status_code == 422
    assert "auto_apply" in error_details_text(response.json())


@pytest.mark.parametrize("flag_name", RUNTIME_FALSE_BOUNDARY_FLAGS)
def test_forbidden_boundary_flags_true_fail(flag_name: str) -> None:
    payload = _payload("system_generated_learning")
    payload[flag_name] = True

    response = client.post("/api/v1/simulation/paper-orders", json=payload)

    assert response.status_code == 422
    assert flag_name in error_details_text(response.json())


@pytest.mark.parametrize("flag_name", ["broker_execution_enabled", "production_supabase_connected", "secrets_required"])
def test_forbidden_nested_boundary_flags_true_fail(flag_name: str) -> None:
    payload = _payload("system_generated_learning")
    payload["boundary_flags"][flag_name] = True

    response = client.post("/api/v1/simulation/paper-orders", json=payload)

    assert response.status_code == 422
    assert flag_name in error_details_text(response.json())


def test_get_paper_portfolio_returns_state_recent_records_and_audit_previews() -> None:
    client.post("/api/v1/simulation/paper-orders", json=_payload("user_recorded"))
    client.post("/api/v1/simulation/paper-orders", json=_payload("system_generated_learning"))

    response = client.get("/api/v1/paper-portfolios/runtime-paper-portfolio-001")

    assert response.status_code == 200
    payload = response.json()
    assert_success_envelope(payload)
    assert_runtime_warnings(payload["warnings"])
    snapshot = payload["data"]
    assert snapshot["portfolio_id"] == "runtime-paper-portfolio-001"
    assert snapshot["status"] == "in_memory_only_non_production"
    assert snapshot["cash_placeholder"]["source"] == "placeholder_not_broker_cash"
    assert snapshot["nav_placeholder"]["source"] == "placeholder_not_market_valuation"
    assert [order["simulation_origin"] for order in snapshot["recent_paper_orders"]] == [
        "user_recorded",
        "system_generated_learning",
    ]
    assert len(snapshot["audit_event_previews"]) == 2
    assert snapshot["audit_event_previews"][0]["event_type"] == "create_paper_order"
    assert snapshot["audit_event_previews"][0]["preview_only"] is True


@pytest.mark.parametrize("portfolio_id", ["ab", "invalid%20portfolio"])
def test_invalid_paper_portfolio_id_returns_validation_error_envelope(portfolio_id: str) -> None:
    response = client.get(f"/api/v1/paper-portfolios/{portfolio_id}")

    assert response.status_code == 422
    error_payload = response.json()
    assert_error_envelope(error_payload, code="VALIDATION_ERROR")
    assert "portfolio_id" in error_details_text(error_payload)


def test_unknown_paper_portfolio_returns_not_found_error_envelope() -> None:
    response = client.get("/api/v1/paper-portfolios/valid-but-unknown-portfolio")

    assert response.status_code == 404
    error_payload = response.json()
    assert_error_envelope(error_payload, code="NOT_FOUND")
    assert "paper portfolio not found" in error_details_text(error_payload)


def test_direct_runtime_does_not_write_database_or_call_external_services() -> None:
    payload = _payload("user_recorded")
    with patch("urllib.request.urlopen") as urlopen_mock, patch("httpx.Client.request") as httpx_mock:
        result = create_paper_order_record(payload)

    assert result["paper_order"]["persistence_write_performed"] is False
    assert result["paper_order"]["external_api_called"] is False
    assert result["paper_order"]["broker_api_called"] is False
    urlopen_mock.assert_not_called()
    httpx_mock.assert_not_called()


def test_runtime_source_does_not_import_supabase_or_commercial_runtime_dependencies() -> None:
    source_paths = [
        Path("backend/app/simulation_runtime.py"),
        Path("backend/app/simulation_store.py"),
        Path("backend/app/main.py"),
    ]
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in source_paths)
    forbidden_tokens = [
        "import supabase",
        "from supabase",
        "stripe",
        "place_real_money_order",
        "railway",
    ]
    for token in forbidden_tokens:
        assert token not in combined


def test_audit_event_preview_is_in_memory_not_persisted() -> None:
    response = client.post("/api/v1/simulation/paper-orders", json=_payload("user_recorded"))
    audit = response.json()["data"]["audit_event_preview"]

    assert audit["audit_event_id"] == "audit-event-preview-000001"
    assert audit["persistence_write_performed"] is False
    assert audit["preview_only"] is True
