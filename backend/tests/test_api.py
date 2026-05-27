from uuid import UUID

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


REQUIRED_SUCCESS_KEYS = {"request_id", "status", "data", "metadata", "warnings"}
REQUIRED_ERROR_KEYS = {"request_id", "status", "error"}


def assert_success_envelope(payload: dict) -> None:
    assert set(payload.keys()) == REQUIRED_SUCCESS_KEYS
    assert payload["status"] == "success"
    assert payload["metadata"]["schema_version"] == "v0.1"
    assert payload["metadata"]["source"] == "HK_ALPHA_TEAM"
    assert isinstance(payload["warnings"], list)
    UUID(payload["request_id"])


def assert_error_envelope(payload: dict, code: str) -> None:
    assert set(payload.keys()) == REQUIRED_ERROR_KEYS
    assert payload["status"] == "error"
    assert payload["error"]["code"] == code
    assert payload["error"]["message"]
    assert isinstance(payload["error"]["details"], dict)
    UUID(payload["request_id"])


def test_health_endpoint_returns_required_envelope() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert_success_envelope(payload)
    assert payload["data"] == {"service": "ok"}


def test_project_status_endpoint_returns_required_envelope() -> None:
    response = client.get("/api/v1/project-status")
    assert response.status_code == 200
    payload = response.json()

    assert_success_envelope(payload)
    assert "Phase 3 — Backend Skeleton" in payload["data"]["current_phase"]
    assert "M3" in payload["data"]["current_milestone"]
    assert payload["data"]["task_status"]["005"] == "Completed"
    assert payload["data"]["task_status"]["006"] == "In Progress"


def test_analyze_stock_stub_returns_contract_aligned_envelope() -> None:
    response = client.post("/api/v1/analyze-stock", json={"symbol": "0700.HK"})
    assert response.status_code == 200
    payload = response.json()

    assert_success_envelope(payload)
    assert payload["data"]["symbol"] == "0700.HK"
    assert payload["data"]["analysis_mode"] == "stub"
    assert payload["data"]["human_decision_required"] is True
    assert payload["data"]["recommendation"]["confidence"] == 0
    assert "No real investment analysis has been performed" in payload["data"]["summary"]
    assert payload["warnings"]


def test_analyze_stock_invalid_symbol_returns_validation_error_envelope() -> None:
    response = client.post("/api/v1/analyze-stock", json={"symbol": "AAPL"})
    assert response.status_code == 200
    payload = response.json()

    assert_error_envelope(payload, code="VALIDATION_ERROR")
    assert payload["error"]["details"]["rule"] == "hk_symbol"


def test_analyze_stock_empty_symbol_returns_validation_error_envelope() -> None:
    response = client.post("/api/v1/analyze-stock", json={"symbol": "   "})
    assert response.status_code == 200
    payload = response.json()

    assert_error_envelope(payload, code="VALIDATION_ERROR")
    assert payload["error"]["details"]["field"] == "symbol"


def test_analyze_stock_missing_symbol_is_rejected_by_request_validation() -> None:
    response = client.post("/api/v1/analyze-stock", json={})
    assert response.status_code == 422


def test_analyze_stock_stub_has_no_database_dependency() -> None:
    response = client.post("/api/v1/analyze-stock", json={"symbol": "0005.HK"})
    assert response.status_code == 200
    payload = response.json()

    assert_success_envelope(payload)
    assert payload["data"]["analysis_mode"] == "stub"
