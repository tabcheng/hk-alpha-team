from __future__ import annotations

from copy import deepcopy
from decimal import Decimal
from typing import Any, Mapping
from uuid import NAMESPACE_URL, UUID, uuid5

import psycopg
from psycopg.rows import dict_row
from psycopg.types.json import Jsonb

from app.simulation_persistence_boundary import (
    APPROVED_SIMULATION_ORIGINS,
    FALSE_BOUNDARY_FLAGS,
    LEARNING_LOSS_GUARDRAILS,
    TRUE_BOUNDARY_FLAGS,
)

LOCAL_TEST_ADAPTER_BOUNDARY_FLAGS = {
    "adapter_scope": "local_test_postgresql_only",
    "production_supabase_connected": False,
    "supabase_client_used": False,
    "vendor_api_called": False,
    "live_market_data_called": False,
    "broker_api_called": False,
    "real_money_order_placed": False,
    "secrets_required": False,
}


class SimulationPostgresPersistenceError(ValueError):
    """Raised when a paper-order payload cannot be written to local/test PostgreSQL safely."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise SimulationPostgresPersistenceError(message)


def _require_mapping(payload: Mapping[str, Any], label: str) -> dict[str, Any]:
    _require(isinstance(payload, Mapping), f"{label} must be a mapping")
    return deepcopy(dict(payload))


def _stable_uuid(label: str, value: str) -> UUID:
    return uuid5(NAMESPACE_URL, f"hk-alpha-team:local-test:{label}:{value}")


def _json_copy(value: Any, fallback: Any) -> Any:
    if value is None:
        return deepcopy(fallback)
    return deepcopy(value)


def _normalize_quantity(value: Any) -> Decimal:
    _require(isinstance(value, (int, float, Decimal)) and not isinstance(value, bool), "quantity must be numeric")
    quantity = Decimal(str(value))
    _require(quantity > 0, "quantity must be positive")
    return quantity


def _validate_boundary_payload(payload: Mapping[str, Any]) -> None:
    origin = payload.get("simulation_origin")
    _require(origin in APPROVED_SIMULATION_ORIGINS, "simulation_origin must be an approved paper-only origin")
    _require(payload.get("paper_order_origin") == origin, "paper_order_origin must match simulation_origin")

    for flag_name in TRUE_BOUNDARY_FLAGS:
        _require(payload.get(flag_name) is True, f"{flag_name} must be true")

    boundary_flags = payload.get("boundary_flags_json")
    _require(isinstance(boundary_flags, Mapping), "boundary_flags_json must be a mapping")
    for flag_name in FALSE_BOUNDARY_FLAGS:
        _require(payload.get(flag_name) is False, f"{flag_name} must be false")
        _require(boundary_flags.get(flag_name) is False, f"boundary_flags_json.{flag_name} must be false")

    for flag_name, expected in LEARNING_LOSS_GUARDRAILS.items():
        _require(payload.get(flag_name) is expected, f"{flag_name} must be {str(expected).lower()}")
        _require(boundary_flags.get(flag_name) is expected, f"boundary_flags_json.{flag_name} must be {str(expected).lower()}")

    if origin == "system_generated_learning":
        _require(payload.get("requires_human_review") is True, "system-generated learning orders require human review")

    source_metadata = payload.get("source_metadata_json")
    historical_fields = payload.get("historical_recommendation_fields_json")
    outcome_preview = payload.get("outcome_preview_json")
    _require(isinstance(source_metadata, Mapping), "source_metadata_json must be a mapping")
    _require(isinstance(historical_fields, Mapping), "historical_recommendation_fields_json must be a mapping")
    _require(isinstance(outcome_preview, Mapping), "outcome_preview_json must be a mapping")
    if "losing_outcome_visible" in outcome_preview:
        _require(outcome_preview["losing_outcome_visible"] is True, "losing outcomes must remain visible")


def _uuid_or_none(value: Any) -> UUID | None:
    if value in (None, ""):
        return None
    if isinstance(value, UUID):
        return value
    if isinstance(value, str):
        try:
            return UUID(value)
        except ValueError:
            return None
    return None


class LocalTestPostgresSimulationPersistence:
    """Local/test-only PostgreSQL adapter for Simulation Desk paper-order roundtrips.

    The adapter only writes explicit Task 008J-style persistence payloads into a
    caller-provided PostgreSQL test database. It does not import or instantiate a
    Supabase client and has no vendor, live market data, broker, real-money,
    billing, auth, deployment, or secret runtime path.
    """

    def __init__(self, dsn: str):
        _require(isinstance(dsn, str) and dsn.strip() != "", "local/test PostgreSQL DSN is required")
        self.dsn = dsn

    def write_paper_order_payload(self, payload: Mapping[str, Any]) -> dict[str, Any]:
        order = _require_mapping(payload, "payload")
        _validate_boundary_payload(order)

        portfolio_runtime_id = str(order.get("portfolio_id") or "").strip()
        symbol = str(order.get("symbol") or "").strip().upper()
        side = str(order.get("side") or "").strip().lower()
        order_type = str(order.get("order_type") or "market").strip().lower()
        _require(portfolio_runtime_id != "", "portfolio_id is required")
        _require(symbol != "", "symbol is required")
        _require(side in {"buy", "sell"}, "side must be buy or sell")
        quantity = _normalize_quantity(order.get("quantity"))

        portfolio_uuid = _stable_uuid("paper_portfolio", portfolio_runtime_id)
        with psycopg.connect(self.dsn, row_factory=dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    insert into stocks (symbol, name, exchange, currency)
                    values (%s, %s, 'HKEX', %s)
                    on conflict (symbol) do update set name = excluded.name
                    returning id
                    """,
                    (symbol, f"Local/test fixture for {symbol}", order.get("base_currency", "HKD")),
                )
                stock_id = cursor.fetchone()["id"]

                cursor.execute(
                    """
                    insert into paper_portfolios (portfolio_uuid, name, base_currency, starting_cash, status)
                    values (%s, %s, %s, 0, 'local_test_only')
                    on conflict (portfolio_uuid) do update
                      set name = excluded.name,
                          base_currency = excluded.base_currency,
                          status = excluded.status
                    returning id
                    """,
                    (portfolio_uuid, portfolio_runtime_id, order.get("base_currency", "HKD")),
                )
                portfolio_id = cursor.fetchone()["id"]

                cursor.execute(
                    """
                    insert into paper_orders (
                      portfolio_id,
                      stock_id,
                      strategy_recommendation_id,
                      source_recommendation_id,
                      side,
                      order_type,
                      quantity,
                      limit_price,
                      status,
                      submitted_at,
                      simulation_origin,
                      paper_order_origin,
                      created_by_type,
                      user_recorded_notes,
                      system_learning_reason,
                      requires_human_review,
                      learning_proposal_id,
                      boundary_flags_json,
                      outcome_preview_json,
                      source_metadata_json,
                      historical_recommendation_fields_json
                    )
                    values (
                      %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                      %s::jsonb, %s::jsonb, %s::jsonb, %s::jsonb
                    )
                    returning id
                    """,
                    (
                        portfolio_id,
                        stock_id,
                        _uuid_or_none(order.get("strategy_recommendation_id")),
                        _uuid_or_none(order.get("source_recommendation_id")),
                        side,
                        order_type,
                        quantity,
                        order.get("limit_price"),
                        order.get("status") or "local_test_recorded",
                        order.get("created_at"),
                        order["simulation_origin"],
                        order["paper_order_origin"],
                        order.get("created_by_type"),
                        order.get("user_recorded_notes"),
                        order.get("system_learning_reason"),
                        order.get("requires_human_review") is True,
                        _uuid_or_none(order.get("learning_proposal_id")),
                        Jsonb(order["boundary_flags_json"]),
                        Jsonb(_json_copy(order.get("outcome_preview_json"), {})),
                        Jsonb(_json_copy(order.get("source_metadata_json"), {})),
                        Jsonb(_json_copy(order.get("historical_recommendation_fields_json"), {})),
                    ),
                )
                paper_order_id = cursor.fetchone()["id"]
        return self.read_paper_order_payload(paper_order_id)

    def read_paper_order_payload(self, paper_order_db_id: UUID | str) -> dict[str, Any]:
        with psycopg.connect(self.dsn, row_factory=dict_row) as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    select
                      po.id,
                      pp.name as portfolio_id,
                      s.symbol,
                      po.side,
                      po.order_type,
                      po.quantity,
                      po.limit_price,
                      po.status,
                      po.submitted_at,
                      po.created_at,
                      po.strategy_recommendation_id,
                      po.source_recommendation_id,
                      po.simulation_origin,
                      po.paper_order_origin,
                      po.created_by_type,
                      po.user_recorded_notes,
                      po.system_learning_reason,
                      po.requires_human_review,
                      po.learning_proposal_id,
                      po.boundary_flags_json,
                      po.outcome_preview_json,
                      po.source_metadata_json,
                      po.historical_recommendation_fields_json
                    from paper_orders po
                    join paper_portfolios pp on pp.id = po.portfolio_id
                    join stocks s on s.id = po.stock_id
                    where po.id = %s
                    """,
                    (paper_order_db_id,),
                )
                row = cursor.fetchone()
        _require(row is not None, "paper order was not found in local/test PostgreSQL")
        result = dict(row)
        result["id"] = str(result["id"])
        for field_name in ("strategy_recommendation_id", "source_recommendation_id", "learning_proposal_id"):
            result[field_name] = str(result[field_name]) if result[field_name] is not None else None
        result["quantity"] = float(result["quantity"])
        if result["limit_price"] is not None:
            result["limit_price"] = float(result["limit_price"])
        if result["submitted_at"] is not None:
            result["submitted_at"] = result["submitted_at"].isoformat()
        result["created_at"] = result["created_at"].isoformat()
        result["local_test_adapter_boundary_flags"] = deepcopy(LOCAL_TEST_ADAPTER_BOUNDARY_FLAGS)
        return result
