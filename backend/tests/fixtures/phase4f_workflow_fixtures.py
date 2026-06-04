from __future__ import annotations

from copy import deepcopy
from typing import Any

from app.analysis_workflow import build_first_analysis_workflow
from app.department_adapters import DEPARTMENT_NAMES

WorkflowPayload = dict[str, Any]

CANONICAL_SYMBOL = "0700.HK"
ALTERNATE_SUPPORTED_SYMBOL = "0005.HK"

PUBLIC_HANDOFF_EXPOSURE_KEYS = [
    "agent_handoff_preview",
    "agent_handoff_previews",
    "handoff_preview",
    "handoff_previews",
]

WARNING_DISCLOSURE_DRIFT = [
    "No live market data only; fixture intentionally omits the remaining disclosures.",
]
EMPTY_WARNING_OVERRIDE: list[str] = []


def canonical_workflow_payload() -> WorkflowPayload:
    """Return the canonical Phase 4F valid workflow fixture for Tencent (0700.HK)."""

    return build_first_analysis_workflow(CANONICAL_SYMBOL)


def alternate_supported_hk_workflow_payload() -> WorkflowPayload:
    """Return a second valid HK-symbol fixture to prove symbol normalization is not single-symbol only."""

    return build_first_analysis_workflow(ALTERNATE_SUPPORTED_SYMBOL)


def workflow_payload_with_missing_department_outputs() -> WorkflowPayload:
    payload = canonical_workflow_payload()
    payload.pop("department_outputs")
    return payload


def workflow_payload_with_duplicate_department_output() -> WorkflowPayload:
    payload = canonical_workflow_payload()
    department_outputs = deepcopy(payload["department_outputs"])
    department_outputs[-1] = deepcopy(department_outputs[0])
    payload["department_outputs"] = department_outputs
    return payload


def workflow_payload_with_missing_department_output() -> WorkflowPayload:
    payload = canonical_workflow_payload()
    payload["department_outputs"] = deepcopy(payload["department_outputs"][:-1])
    return payload


def workflow_payload_with_malformed_department_output_shape() -> WorkflowPayload:
    payload = canonical_workflow_payload()
    department_outputs = deepcopy(payload["department_outputs"])
    department_outputs[0].pop("evidence")
    payload["department_outputs"] = department_outputs
    return payload


def workflow_payload_with_mismatched_department_symbol() -> WorkflowPayload:
    payload = canonical_workflow_payload()
    department_outputs = deepcopy(payload["department_outputs"])
    department_outputs[0]["stock_symbol"] = ALTERNATE_SUPPORTED_SYMBOL
    payload["department_outputs"] = department_outputs
    return payload


def workflow_payload_with_score_bucket_drift() -> WorkflowPayload:
    payload = canonical_workflow_payload()
    scores = deepcopy(payload["scores"])
    scores["market"] = scores["market"] + 1
    payload["scores"] = scores
    return payload


def workflow_payload_with_score_confidence_drift() -> WorkflowPayload:
    payload = canonical_workflow_payload()
    score_confidence = deepcopy(payload["score_confidence"])
    score_confidence["risk"] = score_confidence["risk"] + 1
    payload["score_confidence"] = score_confidence
    return payload


def workflow_payload_with_stage_rationale_drift() -> WorkflowPayload:
    payload = canonical_workflow_payload()
    stage_rationales = deepcopy(payload["stage_rationales"])
    stage_rationales[DEPARTMENT_NAMES[0]] = "Phase 4F fixture-injected rationale drift."
    payload["stage_rationales"] = stage_rationales
    return payload


def workflow_payload_with_agent_trace_boundary_regression() -> WorkflowPayload:
    payload = canonical_workflow_payload()
    agent_trace = deepcopy(payload["agent_trace"])
    agent_trace["real_money_order_placed"] = True
    payload["agent_trace"] = agent_trace
    return payload


def workflow_payload_with_public_handoff_exposure(public_key: str) -> WorkflowPayload:
    payload = canonical_workflow_payload()
    payload[public_key] = []
    return payload


def fixture_handoff_previews_with_output_json_mismatch(previews: list[dict[str, Any]]) -> list[dict[str, Any]]:
    drifted_previews = deepcopy(previews)
    drifted_previews[0]["future_agent_output_preview"]["output_json_preview"] = {
        "fixture_drift": "output_json_preview no longer matches its department output"
    }
    return drifted_previews


def fixture_handoff_previews_with_unresolved_id_regression(previews: list[dict[str, Any]]) -> list[dict[str, Any]]:
    drifted_previews = deepcopy(previews)
    drifted_previews[0]["future_agent_run_preview"]["stock_id_preview"] = "fixture-non-null-stock-id"
    drifted_previews[0]["future_agent_output_preview"]["agent_run_id_preview"] = "fixture-non-null-run-id"
    return drifted_previews
