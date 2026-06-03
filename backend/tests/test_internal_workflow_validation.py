from __future__ import annotations

from copy import deepcopy

import pytest

from app.agent_handoff_mapping import build_agent_handoff_previews
from app.analysis_workflow import build_first_analysis_workflow
from app.department_adapters import DEPARTMENT_NAMES, build_score_buckets, build_score_confidence
from app.internal_workflow_validation import (
    FORBIDDEN_PUBLIC_HANDOFF_KEYS,
    REQUIRED_FALSE_AGENT_TRACE_FLAGS,
    build_internal_workflow_validation_report,
    validate_internal_workflow_payload,
)


def _payload() -> dict[str, object]:
    return build_first_analysis_workflow("0700.HK")


def _expect_validation_error(
    payload: dict[str, object],
    expected_message: str,
    *,
    warnings: list[str] | None = None,
) -> None:
    with pytest.raises(ValueError, match=expected_message):
        validate_internal_workflow_payload(payload, warnings=warnings)


def test_build_first_analysis_workflow_payload_passes_internal_validation() -> None:
    payload = _payload()

    report = validate_internal_workflow_payload(payload)

    assert report["validation_status"] == "passed"
    assert report["symbol"] == "0700.HK"
    assert report["validated_layers"] == [
        "phase4a_analyze_stock_workflow_payload",
        "phase4b_department_adapter_outputs",
        "phase4c_local_only_agent_handoff_previews",
        "phase4d_public_non_exposure_boundary",
    ]
    assert report["department_count"] == 8
    assert report["handoff_preview_count"] == 8
    assert report["public_payload_changed"] is False
    assert report["persistence_enabled"] is False
    assert report["production_supabase_connected"] is False
    assert report["agent_runs_created"] is False
    assert report["agent_outputs_created"] is False
    assert report["broker_execution_enabled"] is False
    assert report["real_money_order_placed"] is False
    assert report["schema_version"] == "v0.1"


def test_build_internal_workflow_validation_report_includes_required_local_only_flags() -> None:
    report = build_internal_workflow_validation_report("0700.HK")

    assert report["validation_status"] == "passed"
    assert report["symbol"] == "0700.HK"
    assert report["department_count"] == 8
    assert report["handoff_preview_count"] == 8
    assert report["public_payload_changed"] is False
    assert report["persistence_enabled"] is False
    assert report["production_supabase_connected"] is False
    assert report["broker_execution_enabled"] is False
    assert report["real_money_order_placed"] is False


def test_validation_does_not_mutate_analyze_stock_payload() -> None:
    payload = _payload()
    before = deepcopy(payload)

    validate_internal_workflow_payload(payload)

    assert payload == before


def test_explicit_warning_disclosure_regression_fails() -> None:
    _expect_validation_error(
        _payload(),
        "warning disclosures missing",
        warnings=["No live market data, but other disclosures are intentionally missing."],
    )


def test_explicit_empty_warning_override_fails() -> None:
    _expect_validation_error(_payload(), "warning disclosures missing", warnings=[])


def test_missing_department_outputs_fails() -> None:
    payload = _payload()
    payload.pop("department_outputs")

    _expect_validation_error(payload, "required analyze-stock payload fields missing")


def test_duplicate_department_output_fails() -> None:
    payload = _payload()
    department_outputs = deepcopy(payload["department_outputs"])
    department_outputs[-1] = deepcopy(department_outputs[0])
    payload["department_outputs"] = department_outputs

    _expect_validation_error(payload, "expected exactly one output")


def test_missing_department_output_fails() -> None:
    payload = _payload()
    payload["department_outputs"] = deepcopy(payload["department_outputs"][:-1])

    _expect_validation_error(payload, "expected exactly one output")


def test_malformed_department_output_shape_fails() -> None:
    payload = _payload()
    department_outputs = deepcopy(payload["department_outputs"])
    department_outputs[0].pop("evidence")
    payload["department_outputs"] = department_outputs

    _expect_validation_error(payload, "missing fields")


def test_mismatched_department_output_stock_symbol_fails() -> None:
    payload = _payload()
    department_outputs = deepcopy(payload["department_outputs"])
    department_outputs[0]["stock_symbol"] = "0005.HK"
    payload["department_outputs"] = department_outputs

    _expect_validation_error(payload, "stock_symbol")


def test_score_mismatch_fails() -> None:
    payload = _payload()
    scores = deepcopy(payload["scores"])
    scores["market"] = scores["market"] + 1
    payload["scores"] = scores

    _expect_validation_error(payload, "market")


def test_score_confidence_mismatch_fails() -> None:
    payload = _payload()
    score_confidence = deepcopy(payload["score_confidence"])
    score_confidence["risk"] = score_confidence["risk"] + 1
    payload["score_confidence"] = score_confidence

    _expect_validation_error(payload, "score_confidence mismatch")


def test_stage_rationale_mismatch_fails() -> None:
    payload = _payload()
    stage_rationales = deepcopy(payload["stage_rationales"])
    stage_rationales[DEPARTMENT_NAMES[0]] = "Altered rationale"
    payload["stage_rationales"] = stage_rationales

    _expect_validation_error(payload, "must equal first department evidence item")


def test_missing_warning_disclosure_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr("app.internal_workflow_validation.PHASE_4A_WARNINGS", [])

    _expect_validation_error(_payload(), "warning disclosures missing")


@pytest.mark.parametrize("flag", REQUIRED_FALSE_AGENT_TRACE_FLAGS)
def test_each_required_agent_trace_false_boundary_flag_regression_fails(flag: str) -> None:
    payload = _payload()
    agent_trace = deepcopy(payload["agent_trace"])
    agent_trace[flag] = True
    payload["agent_trace"] = agent_trace

    _expect_validation_error(payload, f"agent_trace.*{flag}.*must remain false")


@pytest.mark.parametrize(
    "public_key",
    ["agent_handoff_preview", "agent_handoff_previews", "handoff_preview", "handoff_previews"],
)
def test_injected_public_handoff_preview_fields_fail(public_key: str) -> None:
    assert public_key in FORBIDDEN_PUBLIC_HANDOFF_KEYS
    payload = _payload()
    payload[public_key] = []

    _expect_validation_error(payload, "exposes internal handoff preview keys")


def test_nested_public_handoff_preview_field_fails() -> None:
    payload = _payload()
    agent_trace = deepcopy(payload["agent_trace"])
    agent_trace["nested"] = {"handoff_preview": []}
    payload["agent_trace"] = agent_trace

    _expect_validation_error(payload, "payload.agent_trace.nested.handoff_preview")


def test_extra_score_key_fails() -> None:
    payload = _payload()
    scores = deepcopy(payload["scores"])
    scores["unexpected"] = 1
    payload["scores"] = scores

    _expect_validation_error(payload, "scores keys must match")


def test_score_basis_mismatch_fails() -> None:
    payload = _payload()
    scores = deepcopy(payload["scores"])
    scores["score_basis"] = "live_market_data"
    payload["scores"] = scores

    _expect_validation_error(payload, "score_basis")


def test_handoff_preview_output_json_preserves_department_output_payloads() -> None:
    payload = _payload()
    department_outputs = payload["department_outputs"]
    previews = build_agent_handoff_previews(str(payload["symbol"]), department_outputs)
    outputs_by_department = {output["agent_name"]: output for output in department_outputs}

    validate_internal_workflow_payload(payload)

    for preview in previews:
        output_preview = preview["future_agent_output_preview"]
        department_name = output_preview["department_name"]
        assert output_preview["output_json_preview"] == outputs_by_department[department_name]


def test_validation_uses_local_only_artifacts_without_runtime_infrastructure() -> None:
    payload = _payload()
    report = validate_internal_workflow_payload(payload)
    agent_trace = payload["agent_trace"]
    handoff_previews = build_agent_handoff_previews(str(payload["symbol"]), payload["department_outputs"])

    assert agent_trace["production_supabase_required"] is False
    assert agent_trace["production_supabase_connected"] is False
    assert agent_trace["network_services_called"] is False
    assert agent_trace["secrets_required"] is False
    assert agent_trace["paper_order_created"] is False
    assert agent_trace["broker_execution_enabled"] is False
    assert agent_trace["broker_api_called"] is False
    assert agent_trace["real_money_order_placed"] is False
    assert report["persistence_enabled"] is False
    assert report["production_supabase_connected"] is False
    assert report["broker_execution_enabled"] is False
    assert report["real_money_order_placed"] is False
    for preview in handoff_previews:
        runtime_state = preview["current_runtime_state"]
        assert runtime_state["persistence_allowed"] is False
        assert runtime_state["database_write_occurred"] is False
        assert runtime_state["production_supabase_connected"] is False
        assert runtime_state["paper_order_created"] is False
        assert runtime_state["broker_execution_occurred"] is False
        assert runtime_state["real_money_order_placed"] is False


def test_validation_rejects_score_builders_drift() -> None:
    payload = _payload()
    department_outputs = payload["department_outputs"]

    assert {key: payload["scores"][key] for key in build_score_buckets(department_outputs)} == build_score_buckets(
        department_outputs
    )
    assert payload["score_confidence"] == build_score_confidence(department_outputs)
