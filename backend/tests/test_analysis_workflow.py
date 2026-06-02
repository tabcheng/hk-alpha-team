from datetime import datetime

from app.analysis_workflow import (
    ANALYSIS_STATUS,
    PHASE_4A_WARNINGS,
    WORKFLOW_PHASE,
    build_first_analysis_workflow,
    normalize_symbol,
)
from app.department_adapters import COMMON_AGENT_OUTPUT_FIELDS, DEPARTMENT_NAMES

REQUIRED_DATA_FIELDS = {
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
    "generated_at",
    "schema_version",
}


def test_valid_hk_symbol_produces_phase4a_workflow_payload() -> None:
    payload = build_first_analysis_workflow("0700.HK")

    assert REQUIRED_DATA_FIELDS.issubset(payload)
    assert payload["symbol"] == "0700.HK"
    assert payload["analysis_status"] == ANALYSIS_STATUS
    assert payload["workflow_phase"] == WORKFLOW_PHASE
    assert payload["analysis_status"] != "stub_only"
    assert "Phase 4A deterministic local-only skeleton" in payload["summary"]
    assert "Phase 4B department adapter previews" in payload["summary"]
    assert "not live investment research" in payload["summary"]
    assert payload["schema_version"] == "v0.1"


def _stable_workflow_subset(payload: dict) -> dict:
    stable = {key: value for key, value in payload.items() if key != "generated_at"}
    stable["department_outputs"] = [
        {key: value for key, value in output.items() if key != "generated_at"}
        for output in payload["department_outputs"]
    ]
    return stable


def test_same_symbol_returns_stable_deterministic_scores_and_fields() -> None:
    first = build_first_analysis_workflow("0700.HK")
    second = build_first_analysis_workflow("0700.HK")

    assert _stable_workflow_subset(first) == _stable_workflow_subset(second)
    assert first["scores"] == second["scores"]
    assert first["score_confidence"] == second["score_confidence"]
    assert first["strategy_recommendation"] == second["strategy_recommendation"]
    datetime.fromisoformat(first["generated_at"])
    datetime.fromisoformat(second["generated_at"])


def test_symbol_normalization_is_consistent_inside_workflow() -> None:
    assert normalize_symbol(" 0700.hk ") == "0700.HK"
    payload = build_first_analysis_workflow(" 0700.hk ")

    assert payload["symbol"] == "0700.HK"


def test_scores_are_placeholder_numeric_values_and_not_live_data_derived() -> None:
    payload = build_first_analysis_workflow("0005.HK")
    scores = payload["scores"]

    for score_name in ["market", "fundamental", "technical", "sentiment", "risk", "simulation"]:
        assert isinstance(scores[score_name], int)
        assert 0 <= scores[score_name] <= 100
    assert scores["score_basis"] == "deterministic_phase4b_department_adapters_not_market_data_derived"
    assert payload["score_confidence"] == {
        "market": 20,
        "fundamental": 20,
        "technical": 20,
        "sentiment": 20,
        "risk": 25,
        "simulation": 15,
    }
    assert payload["stock_context"]["live_data_used"] is False


def test_trace_confirms_no_persistence_supabase_broker_or_orders() -> None:
    payload = build_first_analysis_workflow("0700.HK")
    trace = payload["agent_trace"]

    assert trace["agent_runs_created"] is False
    assert trace["agent_outputs_created"] is False
    assert trace["persistence_enabled"] is False
    assert trace["production_supabase_required"] is False
    assert trace["production_supabase_connected"] is False
    assert trace["recommendation_record_created"] is False
    assert trace["paper_order_created"] is False
    assert trace["broker_execution_enabled"] is False
    assert trace["broker_api_called"] is False
    assert trace["real_money_order_placed"] is False
    assert trace["network_services_called"] is False
    assert trace["secrets_required"] is False
    assert "workflow_stages" in trace


def test_advisory_risks_invalidation_and_human_decision_framing_are_present() -> None:
    payload = build_first_analysis_workflow("0700.HK")

    assert payload["key_reasons"]
    assert payload["main_risks"]
    assert payload["invalidation_conditions"]
    assert "No paper order" in payload["paper_trading_action"]
    assert "Harness Engineering human decision required" in payload["real_money_decision"]
    assert "no real-money trade is executed" in payload["real_money_decision"]
    assert any("not treat this skeleton as investment advice" in risk for risk in payload["main_risks"])


def test_phase4a_warnings_are_explicit() -> None:
    warning_text = " ".join(PHASE_4A_WARNINGS)

    assert "deterministic skeleton" in warning_text
    assert "Phase 4B department adapter previews" in warning_text
    assert "No live market data" in warning_text
    assert "No persistence" in warning_text
    assert "production Supabase" in warning_text
    assert "No broker execution" in warning_text
    assert "real-money" in warning_text


def test_workflow_consumes_department_adapter_outputs() -> None:
    payload = build_first_analysis_workflow("0700.HK")
    department_outputs = payload["department_outputs"]

    assert [output["agent_name"] for output in department_outputs] == DEPARTMENT_NAMES
    assert all(set(output) == COMMON_AGENT_OUTPUT_FIELDS for output in department_outputs)
    assert payload["scores"]["market"] == department_outputs[0]["score"]
    assert payload["scores"]["fundamental"] == department_outputs[1]["score"]
    assert payload["scores"]["sentiment"] == department_outputs[2]["score"]
    assert payload["scores"]["technical"] == department_outputs[3]["score"]
    assert payload["scores"]["risk"] == department_outputs[4]["score"]
    assert payload["scores"]["simulation"] == department_outputs[6]["score"]
    assert "not persisted agent_outputs records" in payload["department_output_note"]
    assert payload["agent_trace"]["agent_outputs_created"] is False
