from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

REPORT_PATH = "/api/v1/reports/simulation-summary"


def _payload() -> dict:
    response = client.get(REPORT_PATH)
    assert response.status_code == 200
    return response.json()


def _assert_success_envelope(payload: dict) -> None:
    assert set(payload) == {"request_id", "status", "data", "metadata", "warnings"}
    assert payload["request_id"]
    assert payload["status"] == "success"
    assert isinstance(payload["data"], dict)
    assert payload["metadata"]["schema_version"] == "v0.1"
    assert payload["metadata"]["source"] == "HK_ALPHA_TEAM"
    assert payload["metadata"]["generated_at"]
    assert isinstance(payload["warnings"], list)


def test_simulation_summary_report_returns_success_envelope() -> None:
    payload = _payload()

    _assert_success_envelope(payload)
    assert payload["data"]["report_id"] == "phase6-simulation-summary-001"
    assert payload["data"]["report_type"] == "simulation_summary"


def test_simulation_summary_report_data_is_deterministic() -> None:
    first = _payload()
    second = _payload()

    assert first["data"] == second["data"]
    assert first["warnings"] == second["warnings"]
    for flag in [
        "production_supabase_connected",
        "broker_api_called",
        "real_money_order_placed",
        "vendor_api_called",
        "live_market_data_called",
        "secrets_required",
    ]:
        assert first["metadata"][flag] == second["metadata"][flag]


def test_simulation_summary_report_advisory_paper_human_framing() -> None:
    data = _payload()["data"]

    assert data["advisory_only"] is True
    assert data["paper_only"] is True
    assert data["human_decision_required"] is True
    assert data["recommendations"]
    recommendation = data["recommendations"][0]
    assert recommendation["label"] == "HOLD"
    assert recommendation["human_decision_required"] is True
    assert "No execution instruction" in recommendation["execution_instruction"]
    report_text = str(data).lower()
    assert "advisory" in report_text
    assert "paper-only" in report_text
    assert "human" in report_text


def test_simulation_summary_report_uses_existing_local_simulation_evidence() -> None:
    data = _payload()["data"]

    evidence = data["simulation_evidence_summary"]
    assert [item["simulation_origin"] for item in evidence] == ["user_recorded", "system_generated_learning"]
    for item in evidence:
        assert item["validation_status"] == "passed"
        assert item["source_endpoint_reference"] == "POST /api/v1/simulation/paper-orders"
        assert item["symbol"] == "0700.HK"
        assert item["advisory_only"] is True
        assert item["human_in_the_loop"] is True
        assert item["learning_proposals_reviewable"] is True
        assert item["learning_proposals_auto_applied"] is False
        assert item["losing_outcomes_remain_visible"] is True
        assert item["historical_recommendations_overwritten"] is False
        assert item["real_money_order_placed"] is False
        assert item["broker_api_called"] is False
        assert item["production_supabase_connected"] is False
        assert item["secrets_required"] is False


def test_simulation_summary_report_includes_risks_and_invalidation_conditions() -> None:
    data = _payload()["data"]

    assert len(data["risks"]) >= 3
    assert len(data["invalidation_conditions"]) >= 3
    assert any("live market" in risk.lower() for risk in data["risks"])
    assert any("real-money instruction" in condition.lower() for condition in data["invalidation_conditions"])


def test_simulation_summary_report_does_not_expose_plain_buy_sell_instruction() -> None:
    data = _payload()["data"]

    recommendation_labels = [recommendation["label"] for recommendation in data["recommendations"]]
    assert "BUY" not in recommendation_labels
    assert "SELL" not in recommendation_labels
    assert "buy" not in recommendation_labels
    assert "sell" not in recommendation_labels
    assert "buy" not in data["recommendations"][0]["execution_instruction"].lower()
    assert "sell" not in data["recommendations"][0]["execution_instruction"].lower()


def test_simulation_summary_report_metadata_confirms_no_external_or_real_money_runtime() -> None:
    payload = _payload()
    metadata = payload["metadata"]
    generated_from = payload["data"]["generated_from"]

    assert metadata["production_supabase_connected"] is False
    assert metadata["broker_api_called"] is False
    assert metadata["real_money_order_placed"] is False
    assert metadata["vendor_api_called"] is False
    assert metadata["live_market_data_called"] is False
    assert metadata["secrets_required"] is False
    assert metadata["report_runtime"] == "deterministic_local_non_production"
    assert generated_from["production_supabase_connected"] is False
    assert generated_from["broker_api_called"] is False
    assert generated_from["real_money_order_placed"] is False
    assert generated_from["vendor_api_called"] is False
    assert generated_from["live_market_data_called"] is False
    assert generated_from["secrets_required"] is False
    assert generated_from["source_modules"] == [
        "backend.app.report_output",
        "backend.app.simulation_origin_contract",
    ]


def test_simulation_summary_report_warnings_disclose_boundaries() -> None:
    warning_text = " ".join(_payload()["warnings"]).lower()

    for phrase in [
        "broker api",
        "real-money",
        "production supabase",
        "live market data",
        "vendor api",
        "secrets",
        "advisory-only",
        "paper-only",
        "human decision required",
    ]:
        assert phrase in warning_text
