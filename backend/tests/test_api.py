from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint_returns_required_envelope() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "success"
    assert payload["data"] == {"service": "ok"}
    assert payload["metadata"]["schema_version"] == "v0.1"
    assert payload["metadata"]["source"] == "HK_ALPHA_TEAM"
    assert isinstance(payload["warnings"], list)
    assert payload["request_id"]


def test_project_status_endpoint_returns_required_envelope() -> None:
    response = client.get("/api/v1/project-status")
    assert response.status_code == 200
    payload = response.json()

    assert payload["status"] == "success"
    assert "Phase 3 — Backend Skeleton" in payload["data"]["current_phase"]
    assert "M3" in payload["data"]["current_milestone"]
    assert payload["data"]["task_status"]["005"] == "Completed"
    assert payload["data"]["task_status"]["006"] == "In Progress"
