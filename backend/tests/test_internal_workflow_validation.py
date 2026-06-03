from __future__ import annotations

from copy import deepcopy

import pytest

from app.agent_handoff_mapping import build_agent_handoff_previews
from app.analysis_workflow import build_first_analysis_workflow
from app.department_adapters import DEPARTMENT_NAMES
from app.internal_workflow_validation import (
    PUBLIC_HANDOFF_FIELDS,
    REQUIRED_FALSE_AGENT_TRACE_FLAGS,
    REQUIRED_FALSE_HANDOFF_STATE_FLAGS,
    REQUIRED_NULL_HANDOFF_IDENTIFIERS,
    build_internal_workflow_validation_report,
    validate_internal_workflow_payload,
)


def _valid_payload() -> dict[str, object]:
    return build_first_analysis_workflow("0700.HK")


def test_build_first_analysis_workflow_payload_passes_internal_validation_without_mutation() -> None:
    payload = _valid_payload()
    original_payload = deepcopy(payload)

    report = validate_internal_workflow_payload(payload)

    assert report["validation_status"] == "passed"
    assert report["symbol"] == "0700.HK"
    assert report["department_count"] == 8
    assert report["handoff_preview_count"] == 8
    assert report["public_payload_changed"] is False
    assert report["persistence_enabled"] is False
    assert report["production_supabase_connected"] is False
    assert report["broker_execution_enabled"] is False
    assert report["real_money_order_placed"] is False
    assert report["schema_version"] == "v0.1"
    assert payload == original_payload


def test_build_internal_workflow_validation_report_includes_required_boundaries() -> None:
    report = build_internal_workflow_validation_report("0700.HK")

    assert report == {
        "validation_status": "passed",
        "symbol": "0700.HK",
        "validated_layers": [
            "phase4a_analyze_stock_workflow_payload",
            "phase4b_department_adapter_outputs",
            "phase4c_agent_handoff_previews",
        ],
        "department_count": 8,
        "handoff_preview_count": 8,
        "public_payload_changed": False,
        "persistence_enabled": False,
        "production_supabase_connected": False,
        "agent_runs_created": False,
        "agent_outputs_created": False,
        "broker_execution_enabled": False,
        "real_money_order_placed": False,
        "schema_version": "v0.1",
    }


def test_missing_department_outputs_fails() -> None:
    payload = _valid_payload()
    del payload["department_outputs"]

    with pytest.raises(ValueError, match="required analyze-stock payload fields"):
        validate_internal_workflow_payload(payload)


def test_duplicate_department_output_fails() -> None:
    payload = _valid_payload()
    outputs = payload["department_outputs"]
    assert isinstance(outputs, list)
    outputs[-1] = deepcopy(outputs[0])

    with pytest.raises(ValueError, match="department_outputs all-eight coverage"):
        validate_internal_workflow_payload(payload)


def test_missing_department_output_fails() -> None:
    payload = _valid_payload()
    outputs = payload["department_outputs"]
    assert isinstance(outputs, list)
    payload["department_outputs"] = outputs[:-1]

    with pytest.raises(ValueError, match="department_outputs all-eight coverage"):
        validate_internal_workflow_payload(payload)


def test_malformed_department_output_shape_fails() -> None:
    payload = _valid_payload()
    outputs = payload["department_outputs"]
    assert isinstance(outputs, list)
    malformed_output = outputs[0]
    assert isinstance(malformed_output, dict)
    del malformed_output["evidence"]

    with pytest.raises(ValueError, match="department output shape"):
        validate_internal_workflow_payload(payload)


def test_mismatched_department_output_stock_symbol_fails() -> None:
    payload = _valid_payload()
    outputs = payload["department_outputs"]
    assert isinstance(outputs, list)
    mismatched_output = outputs[0]
    assert isinstance(mismatched_output, dict)
    mismatched_output["stock_symbol"] = "0005.HK"

    with pytest.raises(ValueError, match="department output stock_symbol"):
        validate_internal_workflow_payload(payload)


def test_score_mismatch_fails() -> None:
    payload = _valid_payload()
    scores = payload["scores"]
    assert isinstance(scores, dict)
    scores["market"] = -1

    with pytest.raises(ValueError, match="scores match build_score_buckets"):
        validate_internal_workflow_payload(payload)


def test_score_confidence_mismatch_fails() -> None:
    payload = _valid_payload()
    score_confidence = payload["score_confidence"]
    assert isinstance(score_confidence, dict)
    score_confidence["market"] = -1

    with pytest.raises(ValueError, match="score_confidence match build_score_confidence"):
        validate_internal_workflow_payload(payload)


def test_stage_rationale_mismatch_fails() -> None:
    payload = _valid_payload()
    stage_rationales = payload["stage_rationales"]
    assert isinstance(stage_rationales, dict)
    stage_rationales[DEPARTMENT_NAMES[0]] = "changed rationale"

    with pytest.raises(ValueError, match="stage_rationales first evidence mapping"):
        validate_internal_workflow_payload(payload)


def test_missing_warning_disclosure_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.internal_workflow_validation.PHASE_4A_WARNINGS", [])

    with pytest.raises(ValueError, match="warning disclosure"):
        validate_internal_workflow_payload(_valid_payload())


@pytest.mark.parametrize("flag", REQUIRED_FALSE_AGENT_TRACE_FLAGS)
def test_each_required_agent_trace_false_boundary_flag_regression_fails(flag: str) -> None:
    payload = _valid_payload()
    agent_trace = payload["agent_trace"]
    assert isinstance(agent_trace, dict)
    agent_trace[flag] = True

    with pytest.raises(ValueError, match="agent_trace false boundary flags"):
        validate_internal_workflow_payload(payload)


@pytest.mark.parametrize("field", sorted(PUBLIC_HANDOFF_FIELDS))
def test_injected_public_handoff_preview_field_fails(field: str) -> None:
    payload = _valid_payload()
    payload[field] = []

    with pytest.raises(ValueError, match="public handoff preview non-exposure"):
        validate_internal_workflow_payload(payload)


def test_analysis_status_regression_fails() -> None:
    payload = _valid_payload()
    payload["analysis_status"] = "stub_only"

    with pytest.raises(ValueError, match="analysis_status"):
        validate_internal_workflow_payload(payload)


def test_workflow_phase_regression_fails() -> None:
    payload = _valid_payload()
    payload["workflow_phase"] = "Phase 4E"

    with pytest.raises(ValueError, match="workflow_phase"):
        validate_internal_workflow_payload(payload)


@pytest.mark.parametrize("flag", REQUIRED_FALSE_HANDOFF_STATE_FLAGS)
def test_handoff_preview_false_boundary_flag_regression_fails(
    monkeypatch: pytest.MonkeyPatch, flag: str
) -> None:
    payload = _valid_payload()

    def build_regressed_handoff_previews(symbol: str, department_outputs: list[dict[str, object]]) -> list[dict[str, object]]:
        previews = build_agent_handoff_previews(symbol, department_outputs)
        previews[0]["current_runtime_state"][flag] = True
        return previews

    monkeypatch.setattr(
        "app.internal_workflow_validation.build_agent_handoff_previews", build_regressed_handoff_previews
    )

    with pytest.raises(ValueError, match="handoff preview non-persistent boundary flags"):
        validate_internal_workflow_payload(payload)


@pytest.mark.parametrize("identifier", REQUIRED_NULL_HANDOFF_IDENTIFIERS)
def test_handoff_preview_unresolved_identifier_regression_fails(
    monkeypatch: pytest.MonkeyPatch, identifier: str
) -> None:
    payload = _valid_payload()

    def build_regressed_handoff_previews(symbol: str, department_outputs: list[dict[str, object]]) -> list[dict[str, object]]:
        previews = build_agent_handoff_previews(symbol, department_outputs)
        if identifier == "agent_run_id_preview":
            previews[0]["future_agent_output_preview"][identifier] = "persisted-run-id"
        else:
            previews[0]["future_agent_run_preview"][identifier] = "persisted-id"
        return previews

    monkeypatch.setattr(
        "app.internal_workflow_validation.build_agent_handoff_previews", build_regressed_handoff_previews
    )

    with pytest.raises(ValueError, match="handoff preview unresolved identifier"):
        validate_internal_workflow_payload(payload)


def test_handoff_preview_count_regression_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _valid_payload()

    def build_short_handoff_previews(symbol: str, department_outputs: list[dict[str, object]]) -> list[dict[str, object]]:
        return build_agent_handoff_previews(symbol, department_outputs)[:-1]

    monkeypatch.setattr("app.internal_workflow_validation.build_agent_handoff_previews", build_short_handoff_previews)

    with pytest.raises(ValueError, match="handoff preview count"):
        validate_internal_workflow_payload(payload)


def test_handoff_preview_output_json_regression_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _valid_payload()

    def build_regressed_handoff_previews(symbol: str, department_outputs: list[dict[str, object]]) -> list[dict[str, object]]:
        previews = build_agent_handoff_previews(symbol, department_outputs)
        previews[0]["future_agent_output_preview"]["output_json_preview"] = {"changed": True}
        return previews

    monkeypatch.setattr(
        "app.internal_workflow_validation.build_agent_handoff_previews", build_regressed_handoff_previews
    )

    with pytest.raises(ValueError, match="handoff preview output_json_preview preserves department output"):
        validate_internal_workflow_payload(payload)


def test_handoff_preview_request_persistence_regression_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = _valid_payload()

    def build_regressed_handoff_previews(symbol: str, department_outputs: list[dict[str, object]]) -> list[dict[str, object]]:
        previews = build_agent_handoff_previews(symbol, department_outputs)
        previews[0]["future_agent_run_preview"]["request_payload_preview"]["persistence_allowed"] = True
        return previews

    monkeypatch.setattr(
        "app.internal_workflow_validation.build_agent_handoff_previews", build_regressed_handoff_previews
    )

    with pytest.raises(ValueError, match="handoff preview request persistence_allowed"):
        validate_internal_workflow_payload(payload)

def test_handoff_preview_output_json_preserves_department_output_payloads() -> None:
    payload = _valid_payload()
    department_outputs = payload["department_outputs"]
    assert isinstance(department_outputs, list)

    handoff_previews = build_agent_handoff_previews("0700.HK", department_outputs)

    outputs_by_department = {output["agent_name"]: output for output in department_outputs}
    assert len(handoff_previews) == 8
    for preview in handoff_previews:
        output_preview = preview["future_agent_output_preview"]
        department_name = output_preview["department_name"]
        assert output_preview["output_json_preview"] == outputs_by_department[department_name]


def test_validation_path_keeps_all_runtime_integration_boundaries_false() -> None:
    payload = _valid_payload()
    report = validate_internal_workflow_payload(payload)
    agent_trace = payload["agent_trace"]
    assert isinstance(agent_trace, dict)

    assert report["persistence_enabled"] is False
    assert report["production_supabase_connected"] is False
    assert report["agent_runs_created"] is False
    assert report["agent_outputs_created"] is False
    assert report["broker_execution_enabled"] is False
    assert report["real_money_order_placed"] is False
    assert agent_trace["network_services_called"] is False
    assert agent_trace["secrets_required"] is False
    assert agent_trace["paper_order_created"] is False
    assert agent_trace["broker_api_called"] is False
