from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass
from typing import Any
from uuid import NAMESPACE_URL, uuid5

from app.department_adapters import COMMON_AGENT_OUTPUT_FIELDS, DEPARTMENT_NAMES

NOT_PERSISTED = "NOT_PERSISTED"
PREVIEW_ONLY = "PREVIEW_ONLY"
PERSISTENCE_NOT_AUTHORIZED = "PERSISTENCE_NOT_AUTHORIZED"
NO_DATABASE_WRITE_OCCURRED = "no database write occurred"
NO_PRODUCTION_SUPABASE_CONNECTION_OCCURRED = "no production Supabase connection occurred"
NO_PERSISTED_AGENT_RUN_CREATED = "no persisted agent run was created"
NO_PERSISTED_AGENT_OUTPUT_CREATED = "no persisted agent output was created"
NO_STRATEGY_RECOMMENDATION_CREATED = "no strategy recommendation was created"
NO_AUDIT_EVENT_CREATED = "no audit event was created"

LOCAL_RUNTIME_BOUNDARY_STATEMENTS = [
    NO_DATABASE_WRITE_OCCURRED,
    NO_PRODUCTION_SUPABASE_CONNECTION_OCCURRED,
    NO_PERSISTED_AGENT_RUN_CREATED,
    NO_PERSISTED_AGENT_OUTPUT_CREATED,
    NO_STRATEGY_RECOMMENDATION_CREATED,
    NO_AUDIT_EVENT_CREATED,
]


@dataclass(frozen=True)
class AgentRunPreview:
    run_uuid_preview: str
    department_name: str
    request_payload_preview: dict[str, Any]
    status_preview: str
    started_at_preview: str
    finished_at_preview: str
    error_code_preview: None
    stock_symbol: str
    stock_id_preview: None
    recommendation_id_preview: None
    persistence_status: str
    persistence_allowed: bool


@dataclass(frozen=True)
class AgentOutputPreview:
    agent_run_id_preview: None
    department_name: str
    output_json_preview: dict[str, Any]
    confidence: int
    created_at_preview: str
    agent_output_persistence_status: str


@dataclass(frozen=True)
class AgentHandoffPreview:
    future_agent_run_preview: AgentRunPreview
    future_agent_output_preview: AgentOutputPreview
    current_runtime_state: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _normalize_symbol(symbol: str) -> str:
    return symbol.strip().upper()


def _run_uuid_preview(symbol: str, department_name: str) -> str:
    return str(uuid5(NAMESPACE_URL, f"hk-alpha-team:phase4c:agent-run-preview:{symbol}:{department_name}"))


def validate_department_output_shape(output: dict[str, Any]) -> None:
    """Validate the local Phase 4B adapter output contract before handoff preview mapping."""

    output_fields = set(output)
    if output_fields != COMMON_AGENT_OUTPUT_FIELDS:
        missing = sorted(COMMON_AGENT_OUTPUT_FIELDS - output_fields)
        unexpected = sorted(output_fields - COMMON_AGENT_OUTPUT_FIELDS)
        raise ValueError(
            "Department output contract violation: "
            f"missing fields={missing}; unexpected fields={unexpected}"
        )

    agent_name = output["agent_name"]
    if agent_name not in DEPARTMENT_NAMES:
        raise ValueError(f"Department output contract violation: unknown agent_name={agent_name!r}")

    confidence = output["confidence"]
    if not isinstance(confidence, int):
        raise ValueError("Department output contract violation: confidence must be an integer")


def validate_department_output_collection(department_outputs: list[dict[str, Any]]) -> None:
    """Validate exact all-eight department coverage before handoff preview mapping."""

    department_names: list[str] = []
    for output in department_outputs:
        validate_department_output_shape(output)
        department_names.append(str(output["agent_name"]))

    expected_departments = set(DEPARTMENT_NAMES)
    seen_departments = set(department_names)
    missing_departments = [department for department in DEPARTMENT_NAMES if department not in seen_departments]
    duplicate_departments = [
        department
        for department in DEPARTMENT_NAMES
        if department_names.count(department) > 1
    ]

    if (
        len(department_outputs) != len(DEPARTMENT_NAMES)
        or missing_departments
        or duplicate_departments
        or seen_departments != expected_departments
    ):
        unexpected_departments = sorted(seen_departments - expected_departments)
        raise ValueError(
            "Department output collection contract violation: "
            f"expected exactly one output for each of {len(DEPARTMENT_NAMES)} departments; "
            f"received={len(department_outputs)}; "
            f"missing departments={missing_departments}; "
            f"duplicate departments={duplicate_departments}; "
            f"unexpected departments={unexpected_departments}"
        )


def build_agent_handoff_previews(
    symbol: str,
    department_outputs: list[dict[str, Any]],
    *,
    generated_at: str | None = None,
) -> list[dict[str, Any]]:
    """Map Phase 4B adapter outputs to local-only future agent run/output handoff previews.

    This function creates deterministic preview metadata only. When ``generated_at`` is not
    provided, preview timestamps are copied from each validated adapter output so repeated
    mapping of the same inputs remains stable. It does not create database records, connect
    to production Supabase, persist agent runs or agent outputs, create strategy
    recommendations, write audit events, create paper orders, or call broker APIs.
    """

    validate_department_output_collection(department_outputs)

    normalized_symbol = _normalize_symbol(symbol)
    previews: list[dict[str, Any]] = []

    for output in department_outputs:
        department_name = str(output["agent_name"])
        output_symbol = _normalize_symbol(str(output["stock_symbol"]))
        if output_symbol != normalized_symbol:
            raise ValueError(
                "Department output contract violation: "
                f"stock_symbol={output_symbol!r} does not match requested symbol={normalized_symbol!r}"
            )

        preview_timestamp = generated_at or str(output["generated_at"])

        run_preview = AgentRunPreview(
            run_uuid_preview=_run_uuid_preview(normalized_symbol, department_name),
            department_name=department_name,
            request_payload_preview={
                "stock_symbol": normalized_symbol,
                "department_name": department_name,
                "source": "phase4b_department_adapter_output",
                "preview_only": True,
                "persistence_allowed": False,
            },
            status_preview=PREVIEW_ONLY,
            started_at_preview=preview_timestamp,
            finished_at_preview=preview_timestamp,
            error_code_preview=None,
            stock_symbol=normalized_symbol,
            stock_id_preview=None,
            recommendation_id_preview=None,
            persistence_status=PERSISTENCE_NOT_AUTHORIZED,
            persistence_allowed=False,
        )
        output_preview = AgentOutputPreview(
            agent_run_id_preview=None,
            department_name=department_name,
            output_json_preview=deepcopy(output),
            confidence=int(output["confidence"]),
            created_at_preview=preview_timestamp,
            agent_output_persistence_status=NOT_PERSISTED,
        )
        handoff = AgentHandoffPreview(
            future_agent_run_preview=run_preview,
            future_agent_output_preview=output_preview,
            current_runtime_state={
                "mapping_status": PREVIEW_ONLY,
                "persistence_status": NOT_PERSISTED,
                "persistence_allowed": False,
                "preview_only": True,
                "database_write_occurred": False,
                "production_supabase_connected": False,
                "persisted_agent_run_created": False,
                "persisted_agent_output_created": False,
                "strategy_recommendation_created": False,
                "audit_event_created": False,
                "paper_order_created": False,
                "broker_execution_occurred": False,
                "real_money_order_placed": False,
                "boundary_statements": list(LOCAL_RUNTIME_BOUNDARY_STATEMENTS),
            },
        )
        previews.append(handoff.to_dict())

    return previews
