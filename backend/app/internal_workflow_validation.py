from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from app.agent_handoff_mapping import (
    PREVIEW_ONLY,
    build_agent_handoff_previews,
    validate_department_output_collection,
)
from app.analysis_workflow import (
    ANALYSIS_STATUS,
    PHASE_4A_WARNINGS,
    WORKFLOW_PHASE,
    build_first_analysis_workflow,
)
from app.contracts import SCHEMA_VERSION
from app.department_adapters import (
    COMMON_AGENT_OUTPUT_FIELDS,
    DEPARTMENT_NAMES,
    build_score_buckets,
    build_score_confidence,
)

REQUIRED_ANALYZE_STOCK_FIELDS = {
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
    "next_review_date",
    "stock_context",
    "stage_rationales",
    "department_outputs",
    "department_output_note",
    "agent_trace",
    "generated_at",
    "schema_version",
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

REQUIRED_FALSE_HANDOFF_RUNTIME_FLAGS = [
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

FORBIDDEN_PUBLIC_HANDOFF_KEYS = {
    "agent_handoff_preview",
    "agent_handoff_previews",
    "handoff_preview",
    "handoff_previews",
}

REQUIRED_SCORE_BASIS = "deterministic_phase4b_department_adapters_not_market_data_derived"

VALIDATED_LAYERS = [
    "phase4a_analyze_stock_workflow_payload",
    "phase4b_department_adapter_outputs",
    "phase4c_local_only_agent_handoff_previews",
    "phase4d_public_non_exposure_boundary",
]


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"Internal workflow validation invariant failed: {message}")


def _require_mapping(value: Any, field_name: str) -> dict[str, Any]:
    _require(isinstance(value, dict), f"{field_name} must be a mapping")
    return value


def _require_list(value: Any, field_name: str) -> list[Any]:
    _require(isinstance(value, list), f"{field_name} must be a list")
    return value


def _validate_required_payload_fields(payload: dict[str, object]) -> None:
    missing = sorted(REQUIRED_ANALYZE_STOCK_FIELDS - set(payload))
    _require(not missing, f"required analyze-stock payload fields missing: {missing}")


def _find_forbidden_public_handoff_paths(value: Any, path: str = "payload") -> list[str]:
    if isinstance(value, dict):
        paths: list[str] = []
        for key, nested_value in value.items():
            nested_path = f"{path}.{key}"
            if key in FORBIDDEN_PUBLIC_HANDOFF_KEYS:
                paths.append(nested_path)
            paths.extend(_find_forbidden_public_handoff_paths(nested_value, nested_path))
        return paths

    if isinstance(value, list):
        paths = []
        for index, nested_value in enumerate(value):
            paths.extend(_find_forbidden_public_handoff_paths(nested_value, f"{path}[{index}]"))
        return paths

    return []


def _validate_public_payload_non_exposure(payload: dict[str, object]) -> None:
    exposed_paths = _find_forbidden_public_handoff_paths(payload)
    _require(
        not exposed_paths,
        f"public analyze-stock payload exposes internal handoff preview keys at paths: {sorted(exposed_paths)}",
    )


def _validate_warnings_disclose_boundaries(warnings: Sequence[str] | None = None) -> None:
    warning_text = " ".join(warnings or PHASE_4A_WARNINGS).lower()
    required_disclosures = {
        "deterministic Phase 4A skeleton": ["phase 4a deterministic skeleton", "deterministic skeleton"],
        "Phase 4B department adapter previews": ["phase 4b department adapter previews"],
        "not live investment research": ["not live investment research"],
        "no live market data": ["no live market data"],
        "no persistence": ["no persistence", "no persistence writes"],
        "no production Supabase": ["production supabase"],
        "no broker execution": ["no broker execution"],
        "no real-money trading": ["real-money"],
    }
    missing = [
        disclosure
        for disclosure, accepted_phrases in required_disclosures.items()
        if not any(phrase in warning_text for phrase in accepted_phrases)
    ]
    _require(not missing, f"warning disclosures missing required boundaries: {missing}")
    _require("trading" in warning_text, "warning disclosures missing trading boundary language")


def _validate_department_outputs(payload: dict[str, object]) -> list[dict[str, Any]]:
    raw_department_outputs = _require_list(payload.get("department_outputs"), "department_outputs")
    department_outputs = [_require_mapping(output, "department_outputs item") for output in raw_department_outputs]

    validate_department_output_collection(department_outputs)
    _require(len(department_outputs) == len(DEPARTMENT_NAMES), "department_outputs must contain exactly eight records")

    expected_symbol = str(payload["symbol"])
    for output in department_outputs:
        output_fields = set(output)
        _require(
            output_fields == COMMON_AGENT_OUTPUT_FIELDS,
            "department output common shape mismatch for "
            f"{output.get('agent_name')!r}: missing={sorted(COMMON_AGENT_OUTPUT_FIELDS - output_fields)}; "
            f"unexpected={sorted(output_fields - COMMON_AGENT_OUTPUT_FIELDS)}",
        )
        _require(
            output["stock_symbol"] == expected_symbol,
            f"department output stock_symbol mismatch for {output['agent_name']!r}: "
            f"{output['stock_symbol']!r} != {expected_symbol!r}",
        )

    return department_outputs


def _validate_scores(payload: dict[str, object], department_outputs: list[dict[str, Any]]) -> None:
    scores = _require_mapping(payload.get("scores"), "scores")
    expected_scores = build_score_buckets(department_outputs)
    expected_score_keys = set(expected_scores) | {"score_basis"}
    _require(
        set(scores) == expected_score_keys,
        "scores keys must match score buckets plus score_basis: "
        f"missing={sorted(expected_score_keys - set(scores))}; unexpected={sorted(set(scores) - expected_score_keys)}",
    )
    _require(
        scores.get("score_basis") == REQUIRED_SCORE_BASIS,
        f"scores['score_basis'] mismatch: {scores.get('score_basis')!r} != {REQUIRED_SCORE_BASIS!r}",
    )
    for score_name, expected_value in expected_scores.items():
        _require(
            scores.get(score_name) == expected_value,
            f"scores[{score_name!r}] mismatch: {scores.get(score_name)!r} != {expected_value!r}",
        )

    score_confidence = _require_mapping(payload.get("score_confidence"), "score_confidence")
    expected_confidence = build_score_confidence(department_outputs)
    _require(
        score_confidence == expected_confidence,
        f"score_confidence mismatch: {score_confidence!r} != {expected_confidence!r}",
    )


def _validate_stage_rationales(payload: dict[str, object], department_outputs: list[dict[str, Any]]) -> None:
    stage_rationales = _require_mapping(payload.get("stage_rationales"), "stage_rationales")
    expected_department_names = [str(output["agent_name"]) for output in department_outputs]
    _require(
        set(stage_rationales) == set(expected_department_names),
        "stage_rationales keys must exactly match department names: "
        f"missing={sorted(set(expected_department_names) - set(stage_rationales))}; "
        f"unexpected={sorted(set(stage_rationales) - set(expected_department_names))}",
    )

    for output in department_outputs:
        department_name = str(output["agent_name"])
        evidence = _require_list(output.get("evidence"), f"evidence for {department_name}")
        _require(evidence, f"evidence for {department_name} must contain at least one item")
        _require(
            stage_rationales[department_name] == evidence[0],
            f"stage_rationales[{department_name!r}] must equal first department evidence item",
        )


def _validate_agent_trace(payload: dict[str, object]) -> dict[str, Any]:
    agent_trace = _require_mapping(payload.get("agent_trace"), "agent_trace")
    for flag in REQUIRED_FALSE_AGENT_TRACE_FLAGS:
        _require(agent_trace.get(flag) is False, f"agent_trace[{flag!r}] must remain false")
    return agent_trace


def _validate_handoff_previews(symbol: str, department_outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    handoff_previews = build_agent_handoff_previews(symbol, department_outputs)
    _require(len(handoff_previews) == len(DEPARTMENT_NAMES), "handoff previews must contain exactly eight records")

    outputs_by_department = {str(output["agent_name"]): output for output in department_outputs}
    for preview in handoff_previews:
        preview_mapping = _require_mapping(preview, "handoff preview")
        run_preview = _require_mapping(preview_mapping.get("future_agent_run_preview"), "future_agent_run_preview")
        output_preview = _require_mapping(
            preview_mapping.get("future_agent_output_preview"), "future_agent_output_preview"
        )
        runtime_state = _require_mapping(preview_mapping.get("current_runtime_state"), "current_runtime_state")

        department_name = str(output_preview.get("department_name"))
        _require(department_name in outputs_by_department, f"handoff preview unknown department: {department_name!r}")

        for flag in REQUIRED_FALSE_HANDOFF_RUNTIME_FLAGS:
            _require(runtime_state.get(flag) is False, f"handoff current_runtime_state[{flag!r}] must remain false")

        _require(runtime_state.get("mapping_status") == PREVIEW_ONLY, "handoff mapping_status must remain PREVIEW_ONLY")
        _require(runtime_state.get("preview_only") is True, "handoff current_runtime_state.preview_only must remain true")
        _require(
            run_preview.get("status_preview") == PREVIEW_ONLY,
            "future_agent_run_preview.status_preview must remain PREVIEW_ONLY",
        )
        _require(run_preview.get("persistence_allowed") is False, "future_agent_run_preview.persistence_allowed must be false")
        _require(run_preview.get("stock_id_preview") is None, "stock_id_preview must remain null")
        _require(run_preview.get("recommendation_id_preview") is None, "recommendation_id_preview must remain null")
        _require(output_preview.get("agent_run_id_preview") is None, "agent_run_id_preview must remain null")
        _require(
            output_preview.get("output_json_preview") == outputs_by_department[department_name],
            f"handoff output_json_preview must preserve department output for {department_name!r}",
        )

    return handoff_previews


def validate_internal_workflow_payload(
    payload: dict[str, object],
    *,
    warnings: Sequence[str] | None = None,
) -> dict[str, object]:
    """Validate Phase 4A/4B/4C internal workflow consistency without mutating public payloads."""

    _require_mapping(payload, "payload")
    _validate_required_payload_fields(payload)
    _validate_public_payload_non_exposure(payload)
    _require(payload["analysis_status"] == ANALYSIS_STATUS, f"analysis_status must be {ANALYSIS_STATUS!r}")
    _require(payload["workflow_phase"] == WORKFLOW_PHASE, f"workflow_phase must be {WORKFLOW_PHASE!r}")
    _require(payload["schema_version"] == SCHEMA_VERSION, f"schema_version must be {SCHEMA_VERSION!r}")
    _validate_warnings_disclose_boundaries(warnings)

    symbol = str(payload["symbol"])
    department_outputs = _validate_department_outputs(payload)
    _validate_scores(payload, department_outputs)
    _validate_stage_rationales(payload, department_outputs)
    agent_trace = _validate_agent_trace(payload)
    handoff_previews = _validate_handoff_previews(symbol, department_outputs)

    return {
        "validation_status": "passed",
        "symbol": symbol,
        "validated_layers": list(VALIDATED_LAYERS),
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
    """Build and validate a local-only Phase 4E internal workflow validation report."""

    payload = build_first_analysis_workflow(symbol)
    return validate_internal_workflow_payload(payload)
