from __future__ import annotations

from typing import Any

from app.agent_handoff_mapping import build_agent_handoff_previews
from app.analysis_workflow import ANALYSIS_STATUS, PHASE_4A_WARNINGS, WORKFLOW_PHASE, build_first_analysis_workflow
from app.contracts import SCHEMA_VERSION
from app.department_adapters import (
    COMMON_AGENT_OUTPUT_FIELDS,
    DEPARTMENT_NAMES,
    build_score_buckets,
    build_score_confidence,
)

PUBLIC_HANDOFF_FIELDS = {
    "agent_handoff_preview",
    "agent_handoff_previews",
    "handoff_preview",
    "handoff_previews",
}

REQUIRED_PAYLOAD_FIELDS = {
    "symbol",
    "analysis_status",
    "workflow_phase",
    "strategy_recommendation",
    "summary",
    "confidence_level",
    "scores",
    "score_confidence",
    "key_reasons",
    "main_risks",
    "invalidation_conditions",
    "paper_trading_action",
    "real_money_decision",
    "agent_trace",
    "stage_rationales",
    "department_outputs",
    "department_output_note",
    "generated_at",
    "schema_version",
}

REQUIRED_WARNING_DISCLOSURES = {
    "deterministic Phase 4A skeleton": ["phase 4a deterministic skeleton", "deterministic phase 4a skeleton"],
    "Phase 4B department adapter previews": ["phase 4b department adapter previews"],
    "not live investment research": ["not live investment research"],
    "no live market data": ["no live market data"],
    "no persistence": ["no persistence", "no persistence writes"],
    "no production Supabase": ["production supabase"],
    "no broker execution": ["no broker execution"],
    "no real-money trading": ["real-money", "real money"],
}

REQUIRED_FALSE_AGENT_TRACE_FLAGS = [
    "agent_runs_created",
    "agent_outputs_created",
    "persistence_enabled",
    "production_supabase_required",
    "production_supabase_connected",
    "recommendation_record_created",
    "paper_order_created",
    "broker_execution_enabled",
    "broker_api_called",
    "real_money_order_placed",
    "network_services_called",
    "secrets_required",
]

REQUIRED_FALSE_HANDOFF_STATE_FLAGS = [
    "persistence_allowed",
    "database_write_occurred",
    "production_supabase_connected",
    "persisted_agent_run_created",
    "persisted_agent_output_created",
    "strategy_recommendation_created",
    "audit_event_created",
    "paper_order_created",
    "broker_execution_occurred",
    "real_money_order_placed",
]

REQUIRED_NULL_HANDOFF_IDENTIFIERS = [
    "stock_id_preview",
    "recommendation_id_preview",
    "agent_run_id_preview",
]


def _fail(invariant: str, detail: str) -> None:
    raise ValueError(f"Internal workflow validation failed: {invariant}; {detail}")


def _require_mapping(value: object, invariant: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _fail(invariant, f"expected object, received {type(value).__name__}")
    return value


def _require_list(value: object, invariant: str) -> list[Any]:
    if not isinstance(value, list):
        _fail(invariant, f"expected list, received {type(value).__name__}")
    return value


def _validate_public_payload_non_exposure(payload: dict[str, object]) -> None:
    exposed_fields = sorted(PUBLIC_HANDOFF_FIELDS.intersection(payload))
    if exposed_fields:
        _fail("public handoff preview non-exposure", f"unexpected public fields={exposed_fields}")


def _validate_required_payload_fields(payload: dict[str, object]) -> None:
    missing_fields = sorted(REQUIRED_PAYLOAD_FIELDS - set(payload))
    if missing_fields:
        _fail("required analyze-stock payload fields", f"missing fields={missing_fields}")


def _validate_phase_markers(payload: dict[str, object]) -> None:
    if payload.get("analysis_status") != ANALYSIS_STATUS:
        _fail("analysis_status", f"expected {ANALYSIS_STATUS!r}, received {payload.get('analysis_status')!r}")
    if payload.get("workflow_phase") != WORKFLOW_PHASE:
        _fail("workflow_phase", f"expected {WORKFLOW_PHASE!r}, received {payload.get('workflow_phase')!r}")


def _validate_department_outputs(payload: dict[str, object]) -> list[dict[str, Any]]:
    raw_outputs = _require_list(payload.get("department_outputs"), "department_outputs exists")
    department_outputs: list[dict[str, Any]] = []
    for index, output in enumerate(raw_outputs):
        department_outputs.append(_require_mapping(output, f"department output at index {index} shape"))

    department_names = [str(output.get("agent_name")) for output in department_outputs]
    expected_departments = set(DEPARTMENT_NAMES)
    seen_departments = set(department_names)
    missing_departments = [department for department in DEPARTMENT_NAMES if department not in seen_departments]
    duplicate_departments = [department for department in DEPARTMENT_NAMES if department_names.count(department) > 1]
    unexpected_departments = sorted(seen_departments - expected_departments)

    if (
        len(department_outputs) != len(DEPARTMENT_NAMES)
        or missing_departments
        or duplicate_departments
        or unexpected_departments
    ):
        _fail(
            "department_outputs all-eight coverage",
            "expected exactly one output for each department; "
            f"received={len(department_outputs)}; missing={missing_departments}; "
            f"duplicates={duplicate_departments}; unexpected={unexpected_departments}",
        )

    symbol = str(payload.get("symbol"))
    for output in department_outputs:
        output_fields = set(output)
        if output_fields != COMMON_AGENT_OUTPUT_FIELDS:
            missing_fields = sorted(COMMON_AGENT_OUTPUT_FIELDS - output_fields)
            unexpected_fields = sorted(output_fields - COMMON_AGENT_OUTPUT_FIELDS)
            _fail(
                f"department output shape for {output.get('agent_name')!r}",
                f"missing fields={missing_fields}; unexpected fields={unexpected_fields}",
            )
        if output.get("stock_symbol") != symbol:
            _fail(
                f"department output stock_symbol for {output.get('agent_name')!r}",
                f"expected {symbol!r}, received {output.get('stock_symbol')!r}",
            )
        evidence = output.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            _fail(f"department output evidence for {output.get('agent_name')!r}", "expected non-empty evidence list")

    return department_outputs


def _validate_scores(payload: dict[str, object], department_outputs: list[dict[str, Any]]) -> None:
    scores = _require_mapping(payload.get("scores"), "scores")
    expected_scores = build_score_buckets(department_outputs)
    actual_scores = {key: scores.get(key) for key in expected_scores}
    if actual_scores != expected_scores:
        _fail("scores match build_score_buckets(department_outputs)", f"expected={expected_scores}; received={actual_scores}")

    score_confidence = _require_mapping(payload.get("score_confidence"), "score_confidence")
    expected_confidence = build_score_confidence(department_outputs)
    if score_confidence != expected_confidence:
        _fail(
            "score_confidence match build_score_confidence(department_outputs)",
            f"expected={expected_confidence}; received={score_confidence}",
        )


def _validate_stage_rationales(payload: dict[str, object], department_outputs: list[dict[str, Any]]) -> None:
    stage_rationales = _require_mapping(payload.get("stage_rationales"), "stage_rationales")
    expected_rationales = {output["agent_name"]: output["evidence"][0] for output in department_outputs}
    if set(stage_rationales) != set(DEPARTMENT_NAMES):
        _fail(
            "stage_rationales department keys",
            f"expected={DEPARTMENT_NAMES}; received={sorted(stage_rationales)}",
        )
    if stage_rationales != expected_rationales:
        _fail("stage_rationales first evidence mapping", f"expected={expected_rationales}; received={stage_rationales}")


def _validate_warning_disclosures(warnings: list[str]) -> None:
    warning_text = " ".join(warnings).lower()
    for disclosure, acceptable_phrases in REQUIRED_WARNING_DISCLOSURES.items():
        if not any(phrase in warning_text for phrase in acceptable_phrases):
            _fail("warning disclosure", f"missing disclosure={disclosure!r}")


def _validate_agent_trace(payload: dict[str, object]) -> dict[str, Any]:
    agent_trace = _require_mapping(payload.get("agent_trace"), "agent_trace")
    for flag in REQUIRED_FALSE_AGENT_TRACE_FLAGS:
        if agent_trace.get(flag) is not False:
            _fail("agent_trace false boundary flags", f"{flag} expected False, received {agent_trace.get(flag)!r}")
    return agent_trace


def _validate_handoff_previews(symbol: str, department_outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    handoff_previews = build_agent_handoff_previews(symbol, department_outputs)
    if len(handoff_previews) != len(DEPARTMENT_NAMES):
        _fail("handoff preview count", f"expected {len(DEPARTMENT_NAMES)}, received {len(handoff_previews)}")

    outputs_by_department = {output["agent_name"]: output for output in department_outputs}
    for preview in handoff_previews:
        preview_mapping = _require_mapping(preview, "handoff preview shape")
        run_preview = _require_mapping(preview_mapping.get("future_agent_run_preview"), "future_agent_run_preview")
        output_preview = _require_mapping(
            preview_mapping.get("future_agent_output_preview"), "future_agent_output_preview"
        )
        runtime_state = _require_mapping(preview_mapping.get("current_runtime_state"), "current_runtime_state")
        department_name = str(output_preview.get("department_name"))

        request_payload_preview = _require_mapping(
            run_preview.get("request_payload_preview"), "future_agent_run_preview.request_payload_preview"
        )

        if runtime_state.get("preview_only") is not True:
            _fail("handoff preview preview-only boundary", f"{department_name}.current_runtime_state.preview_only")
        if request_payload_preview.get("preview_only") is not True:
            _fail("handoff preview preview-only boundary", f"{department_name}.request_payload_preview.preview_only")
        if run_preview.get("persistence_allowed") is not False:
            _fail("handoff preview run persistence_allowed", f"department={department_name}")
        if request_payload_preview.get("persistence_allowed") is not False:
            _fail("handoff preview request persistence_allowed", f"department={department_name}")
        for flag in REQUIRED_FALSE_HANDOFF_STATE_FLAGS:
            if runtime_state.get(flag) is not False:
                _fail("handoff preview non-persistent boundary flags", f"{department_name}.{flag}={runtime_state.get(flag)!r}")

        unresolved_identifiers = {
            "stock_id_preview": run_preview.get("stock_id_preview"),
            "recommendation_id_preview": run_preview.get("recommendation_id_preview"),
            "agent_run_id_preview": output_preview.get("agent_run_id_preview"),
        }
        for identifier in REQUIRED_NULL_HANDOFF_IDENTIFIERS:
            if unresolved_identifiers[identifier] is not None:
                _fail("handoff preview unresolved identifier", f"{department_name}.{identifier} is not null")

        if output_preview.get("output_json_preview") != outputs_by_department.get(department_name):
            _fail("handoff preview output_json_preview preserves department output", f"department={department_name}")

    return handoff_previews


def validate_internal_workflow_payload(payload: dict[str, object]) -> dict[str, object]:
    """Validate the local-only Phase 4A/4B/4C workflow payload and return an internal report.

    The validator is intentionally not imported by API routes. It reads and cross-checks the
    payload, builds Phase 4C handoff previews in memory, and never mutates the public
    analyze-stock payload or performs persistence/network/broker work.
    """

    _validate_public_payload_non_exposure(payload)
    _validate_required_payload_fields(payload)
    _validate_phase_markers(payload)
    department_outputs = _validate_department_outputs(payload)
    _validate_scores(payload, department_outputs)
    _validate_stage_rationales(payload, department_outputs)
    _validate_warning_disclosures(PHASE_4A_WARNINGS)
    agent_trace = _validate_agent_trace(payload)
    handoff_previews = _validate_handoff_previews(str(payload["symbol"]), department_outputs)

    return {
        "validation_status": "passed",
        "symbol": payload["symbol"],
        "validated_layers": [
            "phase4a_analyze_stock_workflow_payload",
            "phase4b_department_adapter_outputs",
            "phase4c_agent_handoff_previews",
        ],
        "department_count": len(department_outputs),
        "handoff_preview_count": len(handoff_previews),
        "public_payload_changed": False,
        "persistence_enabled": agent_trace["persistence_enabled"],
        "production_supabase_connected": agent_trace["production_supabase_connected"],
        "agent_runs_created": agent_trace["agent_runs_created"],
        "agent_outputs_created": agent_trace["agent_outputs_created"],
        "broker_execution_enabled": agent_trace["broker_execution_enabled"],
        "real_money_order_placed": agent_trace["real_money_order_placed"],
        "schema_version": SCHEMA_VERSION,
    }


def build_internal_workflow_validation_report(symbol: str) -> dict[str, object]:
    """Build and validate a fresh local-only workflow payload for internal review."""

    return validate_internal_workflow_payload(build_first_analysis_workflow(symbol))
