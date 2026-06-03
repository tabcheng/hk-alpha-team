import pytest

from app.agent_handoff_mapping import (
    LOCAL_RUNTIME_BOUNDARY_STATEMENTS,
    NOT_PERSISTED,
    PERSISTENCE_NOT_AUTHORIZED,
    PREVIEW_ONLY,
    build_agent_handoff_previews,
    validate_department_output_shape,
)
from app.department_adapters import COMMON_AGENT_OUTPUT_FIELDS, DEPARTMENT_NAMES, build_department_outputs

FIXED_TIMESTAMP = "2026-06-03T00:00:00+00:00"
RUN_FIELDS = {
    "run_uuid_preview",
    "department_name",
    "request_payload_preview",
    "status_preview",
    "started_at_preview",
    "finished_at_preview",
    "error_code_preview",
    "stock_symbol",
    "stock_id_preview",
    "recommendation_id_preview",
    "persistence_status",
    "persistence_allowed",
}
OUTPUT_FIELDS = {
    "agent_run_id_preview",
    "department_name",
    "output_json_preview",
    "confidence",
    "created_at_preview",
    "agent_output_persistence_status",
}


def _previews() -> list[dict]:
    outputs = build_department_outputs("0700.HK")
    return build_agent_handoff_previews("0700.HK", outputs, generated_at=FIXED_TIMESTAMP)


def test_all_eight_department_outputs_produce_eight_handoff_previews() -> None:
    previews = _previews()

    assert len(previews) == 8
    assert [preview["future_agent_run_preview"]["department_name"] for preview in previews] == DEPARTMENT_NAMES


def test_every_preview_contains_future_agent_run_preview_fields() -> None:
    for preview in _previews():
        run_preview = preview["future_agent_run_preview"]

        assert set(run_preview) == RUN_FIELDS
        assert run_preview["run_uuid_preview"]
        assert run_preview["status_preview"] == PREVIEW_ONLY
        assert run_preview["started_at_preview"] == FIXED_TIMESTAMP
        assert run_preview["finished_at_preview"] == FIXED_TIMESTAMP
        assert run_preview["error_code_preview"] is None
        assert run_preview["stock_symbol"] == "0700.HK"
        assert run_preview["persistence_allowed"] is False
        assert run_preview["persistence_status"] == PERSISTENCE_NOT_AUTHORIZED
        assert run_preview["request_payload_preview"]["preview_only"] is True


def test_every_preview_contains_future_agent_output_preview_fields() -> None:
    for preview in _previews():
        output_preview = preview["future_agent_output_preview"]

        assert set(output_preview) == OUTPUT_FIELDS
        assert output_preview["created_at_preview"] == FIXED_TIMESTAMP
        assert output_preview["agent_output_persistence_status"] == NOT_PERSISTED
        assert isinstance(output_preview["confidence"], int)


def test_output_json_preview_preserves_locked_common_agent_output_shape() -> None:
    for preview in _previews():
        output_json = preview["future_agent_output_preview"]["output_json_preview"]

        assert set(output_json) == COMMON_AGENT_OUTPUT_FIELDS
        assert output_json["schema_version"] == "v0.1"


def test_department_name_matches_adapter_output_agent_name() -> None:
    outputs = build_department_outputs("0700.HK")
    previews = build_agent_handoff_previews("0700.HK", outputs, generated_at=FIXED_TIMESTAMP)

    for output, preview in zip(outputs, previews):
        assert preview["future_agent_run_preview"]["department_name"] == output["agent_name"]
        assert preview["future_agent_output_preview"]["department_name"] == output["agent_name"]
        assert preview["future_agent_output_preview"]["output_json_preview"]["agent_name"] == output["agent_name"]


def test_unresolved_persistence_identifiers_remain_null() -> None:
    for preview in _previews():
        assert preview["future_agent_run_preview"]["stock_id_preview"] is None
        assert preview["future_agent_run_preview"]["recommendation_id_preview"] is None
        assert preview["future_agent_output_preview"]["agent_run_id_preview"] is None


def test_current_runtime_state_confirms_no_persistence_or_production_integration() -> None:
    for preview in _previews():
        runtime_state = preview["current_runtime_state"]
        boundary_text = " ".join(runtime_state["boundary_statements"])

        assert runtime_state["persistence_allowed"] is False
        assert runtime_state["persistence_status"] == NOT_PERSISTED
        assert runtime_state["database_write_occurred"] is False
        assert runtime_state["production_supabase_connected"] is False
        assert runtime_state["persisted_agent_run_created"] is False
        assert runtime_state["persisted_agent_output_created"] is False
        assert runtime_state["strategy_recommendation_created"] is False
        assert runtime_state["audit_event_created"] is False
        assert runtime_state["paper_order_created"] is False
        assert runtime_state["broker_execution_occurred"] is False
        assert runtime_state["real_money_order_placed"] is False
        assert set(runtime_state["boundary_statements"]) == set(LOCAL_RUNTIME_BOUNDARY_STATEMENTS)
        assert "no database write occurred" in boundary_text
        assert "no production Supabase connection occurred" in boundary_text
        assert "no persisted agent run was created" in boundary_text
        assert "no persisted agent output was created" in boundary_text
        assert "no strategy recommendation was created" in boundary_text
        assert "no audit event was created" in boundary_text


def test_stable_handoff_mapping_fields_are_deterministic_for_same_inputs() -> None:
    outputs = build_department_outputs("0700.HK")
    first = build_agent_handoff_previews("0700.HK", outputs, generated_at=FIXED_TIMESTAMP)
    second = build_agent_handoff_previews(" 0700.hk ", outputs, generated_at=FIXED_TIMESTAMP)

    assert first == second


def test_default_timestamps_are_derived_from_adapter_outputs_for_stable_remapping() -> None:
    outputs = build_department_outputs("0700.HK")
    first = build_agent_handoff_previews("0700.HK", outputs)
    second = build_agent_handoff_previews("0700.HK", outputs)

    assert first == second
    for output, preview in zip(outputs, first):
        run_preview = preview["future_agent_run_preview"]
        output_preview = preview["future_agent_output_preview"]

        assert run_preview["started_at_preview"] == output["generated_at"]
        assert run_preview["finished_at_preview"] == output["generated_at"]
        assert output_preview["created_at_preview"] == output["generated_at"]


def test_output_json_preview_is_a_snapshot_of_adapter_output() -> None:
    outputs = build_department_outputs("0700.HK")
    previews = build_agent_handoff_previews("0700.HK", outputs, generated_at=FIXED_TIMESTAMP)

    outputs[0]["evidence"].append("mutated after handoff mapping")
    outputs[0]["key_findings"].append("mutated finding")

    output_json = previews[0]["future_agent_output_preview"]["output_json_preview"]
    assert "mutated after handoff mapping" not in output_json["evidence"]
    assert "mutated finding" not in output_json["key_findings"]


def test_malformed_adapter_output_raises_local_contract_violation() -> None:
    malformed = build_department_outputs("0700.HK")[0]
    malformed.pop("agent_name")

    with pytest.raises(ValueError, match="Department output contract violation"):
        validate_department_output_shape(malformed)


def test_mismatched_output_symbol_raises_local_contract_violation() -> None:
    outputs = build_department_outputs("0700.HK")
    outputs[0]["stock_symbol"] = "0005.HK"

    with pytest.raises(ValueError, match="stock_symbol"):
        build_agent_handoff_previews("0700.HK", outputs, generated_at=FIXED_TIMESTAMP)
