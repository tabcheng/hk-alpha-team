from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def assert_success_envelope(payload: dict) -> None:
    assert set(payload) == {"request_id", "status", "data", "metadata", "warnings"}
    assert payload["request_id"]
    assert payload["status"] == "success"
    assert isinstance(payload["data"], dict)
    assert payload["metadata"]["schema_version"] == "v0.1"
    assert payload["metadata"]["source"] == "HK_ALPHA_TEAM"
    assert payload["metadata"]["generated_at"]
    assert isinstance(payload["warnings"], list)


def assert_error_envelope(payload: dict) -> None:
    assert set(payload) == {"request_id", "status", "error"}
    assert payload["request_id"]
    assert payload["status"] == "error"
    assert payload["error"]["code"] == "VALIDATION_ERROR"
    assert payload["error"]["message"] == "Request validation failed."
    assert isinstance(payload["error"]["details"]["errors"], list)


def test_health_endpoint_returns_required_envelope() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert_success_envelope(payload)
    assert payload["data"] == {"service": "ok"}
    assert payload["warnings"] == []


def _project_status_doc_lines() -> list[str]:
    status_path = Path(__file__).resolve().parents[2] / "docs" / "11-project-status.md"
    return status_path.read_text(encoding="utf-8").splitlines()


def _extract_table_status(lines: list[str], row_id: str) -> str:
    for line in lines:
        row = line.strip()
        if row.startswith(f"| {row_id} |"):
            parts = [part.strip() for part in row.split("|") if part.strip()]
            return parts[2]
    raise AssertionError(f"Missing status row for {row_id}")


def test_project_status_endpoint_returns_required_envelope() -> None:
    response = client.get("/api/v1/project-status")
    assert response.status_code == 200
    payload = response.json()

    assert_success_envelope(payload)

    status_doc_lines = _project_status_doc_lines()
    current_phase_idx = status_doc_lines.index("## Current Phase")
    expected_current_phase = status_doc_lines[current_phase_idx + 2].strip().strip("*")
    expected_m3_status = _extract_table_status(status_doc_lines, "M3")
    expected_task_005_status = _extract_table_status(status_doc_lines, "005")
    expected_task_006_status = _extract_table_status(status_doc_lines, "006")

    assert payload["data"]["current_phase"] == expected_current_phase
    assert payload["data"]["current_milestone"] == f"M3 ({expected_m3_status})"
    assert payload["data"]["task_status"]["005"] == expected_task_005_status
    assert payload["data"]["task_status"]["006"] == expected_task_006_status


def test_analyze_stock_stub_returns_contract_first_payload() -> None:
    response = client.post("/api/v1/analyze-stock", json={"symbol": "0700.HK"})
    assert response.status_code == 200
    payload = response.json()

    assert_success_envelope(payload)
    assert payload["warnings"] == [
        "Stub response only; no live analysis, persistence, production Supabase, or trading execution performed."
    ]

    data = payload["data"]
    assert data["symbol"] == "0700.HK"
    assert data["analysis_status"] == "stub_only"
    assert data["workflow_phase"] == "Phase 3 — Backend Skeleton"
    assert data["strategy_recommendation"] == "STRONG_WATCH"
    assert data["confidence_level"] == 0
    assert data["scores"] == {
        "market": None,
        "fundamental": None,
        "technical": None,
        "sentiment": None,
        "risk": None,
        "simulation": None,
    }
    assert data["key_reasons"]
    assert data["main_risks"]
    assert data["invalidation_conditions"]
    assert data["paper_trading_action"] == "No paper order is created by this stub."
    assert data["real_money_decision"] == "Human decision required by Harness Engineering; no real-money trade is executed."
    assert data["agent_trace"] == {
        "agent_runs_created": False,
        "agent_outputs_created": False,
        "persistence_enabled": False,
        "production_supabase_required": False,
    }
    assert data["schema_version"] == "v0.1"


def test_analyze_stock_requires_symbol() -> None:
    response = client.post("/api/v1/analyze-stock", json={})
    assert response.status_code == 422
    payload = response.json()

    assert_error_envelope(payload)
    assert payload["error"]["details"]["path"] == "/api/v1/analyze-stock"


def test_analyze_stock_rejects_non_hk_symbol_format() -> None:
    response = client.post("/api/v1/analyze-stock", json={"symbol": "AAPL"})
    assert response.status_code == 422
    payload = response.json()

    assert_error_envelope(payload)
    assert payload["error"]["details"]["path"] == "/api/v1/analyze-stock"
