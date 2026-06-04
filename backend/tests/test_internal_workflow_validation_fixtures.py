from __future__ import annotations

from copy import deepcopy

import pytest

import app.internal_workflow_validation as validation_module
from app.agent_handoff_mapping import build_agent_handoff_previews
from app.internal_workflow_validation import validate_internal_workflow_payload
from fixtures.phase4f_workflow_fixtures import (
    CANONICAL_SYMBOL,
    EMPTY_WARNING_OVERRIDE,
    PUBLIC_HANDOFF_EXPOSURE_KEYS,
    WARNING_DISCLOSURE_DRIFT,
    alternate_supported_hk_workflow_payload,
    canonical_workflow_payload,
    fixture_handoff_previews_with_output_json_mismatch,
    fixture_handoff_previews_with_unresolved_id_regression,
    workflow_payload_with_agent_trace_boundary_regression,
    workflow_payload_with_duplicate_department_output,
    workflow_payload_with_malformed_department_output_shape,
    workflow_payload_with_missing_department_output,
    workflow_payload_with_missing_department_outputs,
    workflow_payload_with_mismatched_department_symbol,
    workflow_payload_with_public_handoff_exposure,
    workflow_payload_with_score_bucket_drift,
    workflow_payload_with_score_confidence_drift,
    workflow_payload_with_stage_rationale_drift,
)


def _assert_stable_pass_report(report: dict[str, object], symbol: str) -> None:
    assert report["validation_status"] == "passed"
    assert report["symbol"] == symbol
    assert report["department_count"] == 8
    assert report["handoff_preview_count"] == 8
    assert report["public_payload_changed"] is False
    assert report["persistence_enabled"] is False
    assert report["production_supabase_connected"] is False
    assert report["broker_execution_enabled"] is False
    assert report["real_money_order_placed"] is False


@pytest.mark.parametrize(
    ("fixture_builder", "expected_symbol"),
    [
        (canonical_workflow_payload, CANONICAL_SYMBOL),
        (alternate_supported_hk_workflow_payload, "0005.HK"),
    ],
)
def test_phase4f_positive_workflow_fixtures_pass_internal_validation(fixture_builder, expected_symbol: str) -> None:
    report = validate_internal_workflow_payload(fixture_builder())

    _assert_stable_pass_report(report, expected_symbol)


@pytest.mark.parametrize(
    ("fixture_builder", "expected_message"),
    [
        (workflow_payload_with_missing_department_outputs, "required analyze-stock payload fields missing"),
        (workflow_payload_with_duplicate_department_output, "duplicate departments"),
        (workflow_payload_with_missing_department_output, "missing departments"),
        (workflow_payload_with_malformed_department_output_shape, "missing fields"),
        (workflow_payload_with_mismatched_department_symbol, "stock_symbol"),
        (workflow_payload_with_score_bucket_drift, "scores\\['market'\\] mismatch"),
        (workflow_payload_with_score_confidence_drift, "score_confidence mismatch"),
        (workflow_payload_with_stage_rationale_drift, "must equal first department evidence item"),
        (workflow_payload_with_agent_trace_boundary_regression, "real_money_order_placed.*must remain false"),
    ],
)
def test_phase4f_targeted_drift_fixtures_fail_with_useful_errors(fixture_builder, expected_message: str) -> None:
    with pytest.raises(ValueError, match=expected_message):
        validate_internal_workflow_payload(fixture_builder())


@pytest.mark.parametrize(
    ("warnings", "expected_message"),
    [
        (WARNING_DISCLOSURE_DRIFT, "warning disclosures missing"),
        (EMPTY_WARNING_OVERRIDE, "warning disclosures missing"),
    ],
)
def test_phase4f_warning_disclosure_drift_fixtures_fail(warnings: list[str], expected_message: str) -> None:
    with pytest.raises(ValueError, match=expected_message):
        validate_internal_workflow_payload(canonical_workflow_payload(), warnings=warnings)


@pytest.mark.parametrize("public_key", PUBLIC_HANDOFF_EXPOSURE_KEYS)
def test_phase4f_public_handoff_exposure_fixtures_fail(public_key: str) -> None:
    with pytest.raises(ValueError, match=f"payload.{public_key}"):
        validate_internal_workflow_payload(workflow_payload_with_public_handoff_exposure(public_key))


def test_phase4f_handoff_output_json_preview_mismatch_fixture_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = canonical_workflow_payload()
    clean_previews = build_agent_handoff_previews(str(payload["symbol"]), payload["department_outputs"])

    def _drifted_handoff_previews(symbol, department_outputs):
        return fixture_handoff_previews_with_output_json_mismatch(clean_previews)

    monkeypatch.setattr(validation_module, "build_agent_handoff_previews", _drifted_handoff_previews)

    with pytest.raises(ValueError, match="output_json_preview must preserve department output"):
        validate_internal_workflow_payload(payload)


def test_phase4f_handoff_unresolved_id_regression_fixture_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    payload = canonical_workflow_payload()
    clean_previews = build_agent_handoff_previews(str(payload["symbol"]), payload["department_outputs"])

    def _drifted_handoff_previews(symbol, department_outputs):
        return fixture_handoff_previews_with_unresolved_id_regression(clean_previews)

    monkeypatch.setattr(validation_module, "build_agent_handoff_previews", _drifted_handoff_previews)

    with pytest.raises(ValueError, match="stock_id_preview must remain null|agent_run_id_preview must remain null"):
        validate_internal_workflow_payload(payload)


def test_phase4f_validation_fixture_does_not_mutate_input_payload() -> None:
    payload = canonical_workflow_payload()
    before_validation = deepcopy(payload)

    report = validate_internal_workflow_payload(payload)

    _assert_stable_pass_report(report, CANONICAL_SYMBOL)
    assert payload == before_validation
