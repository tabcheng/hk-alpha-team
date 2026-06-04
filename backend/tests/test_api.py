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


def test_project_status_current_phase_line_is_parser_safe() -> None:
    lines = _project_status_doc_lines()
    current_phase_idx = lines.index("## Current Phase")
    current_phase_line = lines[current_phase_idx + 2].strip()

    assert current_phase_line == "**Phase 4 — First Analysis Workflow**"
    assert current_phase_line.startswith("**")
    assert current_phase_line.endswith("**")
    assert current_phase_line.count("**") == 2
    assert "(" not in current_phase_line
    assert ")" not in current_phase_line


def test_project_status_endpoint_returns_required_envelope() -> None:
    response = client.get("/api/v1/project-status")
    assert response.status_code == 200
    payload = response.json()

    assert_success_envelope(payload)

    status_doc_lines = _project_status_doc_lines()
    assert _extract_table_status(status_doc_lines, "M3") == "Completed"
    assert _extract_table_status(status_doc_lines, "M4") == "Completed"
    assert _extract_table_status(status_doc_lines, "005") == "Completed"
    assert _extract_table_status(status_doc_lines, "006") == "Completed"
    assert _extract_table_status(status_doc_lines, "007") == "Completed"

    assert payload["data"]["current_phase"] == "Phase 4 — First Analysis Workflow"
    assert payload["data"]["current_milestone"] == "M4 (Completed)"
    assert payload["data"]["task_status"]["005"] == "Completed"
    assert payload["data"]["task_status"]["006"] == "Completed"
    assert payload["data"]["task_status"]["007"] == "Completed"


def test_analyze_stock_contract_doc_matches_phase4a_runtime() -> None:
    contract_path = Path(__file__).resolve().parents[2] / "docs" / "09-api-and-agent-contracts.md"
    contract_text = contract_path.read_text(encoding="utf-8")
    endpoint_section = contract_text.split("### `POST /api/v1/analyze-stock`", maxsplit=1)[1].split(
        "### `GET /api/v1/stocks/{symbol}`", maxsplit=1
    )[0]
    historical_section = contract_text.split("## Analyze-Stock Stub Contract (Phase 3 History)", maxsplit=1)[
        1
    ].split("## Explicit Error Envelope", maxsplit=1)[0]

    assert "Current Phase 4A behavior" in endpoint_section
    assert "Phase 4B adapter metadata" in endpoint_section
    assert 'analysis_status = "phase4a_skeleton"' in endpoint_section
    assert 'workflow_phase = "Phase 4A — Deterministic First Analysis Workflow Skeleton"' in endpoint_section
    assert "Current Phase 3 behavior" not in endpoint_section
    assert 'analysis_status = "stub_only"' not in endpoint_section
    assert "Required `agent_trace` boundary flags" in endpoint_section
    assert "real_money_order_placed = false" in endpoint_section
    assert "network_services_called = false" in endpoint_section
    assert "secrets_required = false" in endpoint_section

    assert 'analysis_status = "stub_only"' in historical_section
    assert "historical" in historical_section.lower()
    assert "must not be used as the current runtime contract after Phase 4A" in historical_section

    common_examples_section = contract_text.split("## Agent Department JSON Examples (All 8, Common Shape)", maxsplit=1)[
        1
    ].split("## Final Strategy Recommendation JSON Example", maxsplit=1)[0]
    assert "current Phase 4B local-only adapter preview semantics" in common_examples_section
    for forbidden_example in [
        "Latest annual report",
        "Sector sentiment feed",
        "Daily OHLCV bars",
        "Paper order log",
        '"confidence": 71',
        '"confidence": 73',
    ]:
        assert forbidden_example not in common_examples_section


def test_analyze_stock_returns_phase4a_deterministic_workflow_payload() -> None:
    response = client.post("/api/v1/analyze-stock", json={"symbol": "0700.HK"})
    assert response.status_code == 200
    payload = response.json()

    assert_success_envelope(payload)
    warning_text = " ".join(payload["warnings"])
    assert "Phase 4A deterministic skeleton" in warning_text
    assert "Phase 4B department adapter previews" in warning_text
    assert "No live market data" in warning_text
    assert "No persistence" in warning_text
    assert "production Supabase" in warning_text
    assert "No broker execution" in warning_text
    assert "real-money" in warning_text

    data = payload["data"]
    required_fields = {
        "symbol",
        "analysis_status",
        "workflow_phase",
        "strategy_recommendation",
        "summary",
        "confidence_level",
        "scores",
        "key_reasons",
        "main_risks",
        "invalidation_conditions",
        "paper_trading_action",
        "real_money_decision",
        "agent_trace",
        "department_outputs",
        "department_output_note",
        "generated_at",
        "schema_version",
    }
    assert required_fields.issubset(data)
    assert data["symbol"] == "0700.HK"
    assert data["analysis_status"] == "phase4a_skeleton"
    assert data["analysis_status"] != "stub_only"
    assert data["workflow_phase"] == "Phase 4A — Deterministic First Analysis Workflow Skeleton"
    assert data["strategy_recommendation"] in {
        "STRONG_WATCH",
        "WAIT_FOR_PULLBACK",
        "SMALL_POSITION",
        "ACCUMULATE",
        "HOLD",
        "REDUCE_RISK",
        "AVOID",
    }
    assert data["confidence_level"] == 20
    assert data["scores"]["score_basis"] == "deterministic_phase4b_department_adapters_not_market_data_derived"
    assert len(data["department_outputs"]) == 8
    assert "not persisted agent_outputs records" in data["department_output_note"]
    assert data["key_reasons"]
    assert data["main_risks"]
    assert data["invalidation_conditions"]
    assert data["paper_trading_action"] == "No paper order is created by this Phase 4A skeleton."
    assert data["real_money_decision"] == "Harness Engineering human decision required; no real-money trade is executed or placed."
    assert data["agent_trace"]["agent_runs_created"] is False
    assert data["agent_trace"]["agent_outputs_created"] is False
    assert data["agent_trace"]["persistence_enabled"] is False
    assert data["agent_trace"]["production_supabase_required"] is False
    assert data["agent_trace"]["broker_execution_enabled"] is False
    assert data["agent_trace"]["recommendation_record_created"] is False
    assert data["agent_trace"]["paper_order_created"] is False
    assert data["agent_trace"]["broker_api_called"] is False
    assert data["agent_trace"]["real_money_order_placed"] is False
    assert data["agent_trace"]["network_services_called"] is False
    assert data["agent_trace"]["secrets_required"] is False
    assert data["schema_version"] == "v0.1"
    for forbidden_handoff_key in {
        "agent_handoff_preview",
        "agent_handoff_previews",
        "handoff_preview",
        "handoff_previews",
    }:
        assert forbidden_handoff_key not in data


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
