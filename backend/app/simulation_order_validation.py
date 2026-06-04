from __future__ import annotations

import re
from copy import deepcopy
from typing import Any, Mapping

from app.simulation_contract import (
    BOUNDARY_FLAG_NAMES,
    LOCKED_ENDPOINT_NAMES,
    VALID_ORDER_SIDES,
    VALID_ORDER_TYPES,
)

LOCAL_PAPER_ORDER_RECORD_TYPE = "paper_order_intent"
LOCAL_PAPER_ORDER_SCHEMA_TABLE = "paper_orders"
LOCAL_PAPER_ORDER_ENDPOINT_REFERENCE = "POST /api/v1/simulation/paper-orders"
HK_SYMBOL_PATTERN = re.compile(r"^\d{4}\.HK$")

TASK_008C_SPECIFIC_BOUNDARY_FLAGS = (
    "external_api_required",
    "secrets_required",
)

LOCAL_PAPER_ORDER_BOUNDARY_FLAGS = tuple(
    dict.fromkeys((*BOUNDARY_FLAG_NAMES, *TASK_008C_SPECIFIC_BOUNDARY_FLAGS))
)

ORDER_CREATION_IMPLICATION_FIELDS = (
    "would_create_order",
    "create_order",
    "order_created",
    "paper_order_created",
    "execute_order",
    "submit_order",
    "place_order",
)


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(f"Local paper order validation failed: {message}")


def _is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def _require_non_empty_string(value: object, field_name: str) -> str:
    _require(isinstance(value, str), f"{field_name} must be a string")
    stripped = value.strip()
    _require(stripped != "", f"{field_name} must be present")
    return stripped


def _require_non_negative_number(value: object, field_name: str) -> int | float:
    _require(_is_number(value), f"{field_name} must be numeric")
    _require(value >= 0, f"{field_name} must be non-negative")
    return value


def _require_boundary_flags_remain_false(order: Mapping[str, object]) -> dict[str, bool]:
    flags = {flag_name: False for flag_name in LOCAL_PAPER_ORDER_BOUNDARY_FLAGS}

    nested_flags = order.get("boundary_flags")
    if nested_flags is not None:
        _require(
            isinstance(nested_flags, Mapping),
            "boundary_flags must be a mapping when present",
        )
        for flag_name in LOCAL_PAPER_ORDER_BOUNDARY_FLAGS:
            if flag_name in nested_flags:
                _require(
                    nested_flags[flag_name] is False,
                    f"{flag_name} must remain false for local-only validation",
                )

    for flag_name in LOCAL_PAPER_ORDER_BOUNDARY_FLAGS:
        if flag_name in order:
            _require(
                order[flag_name] is False,
                f"{flag_name} must remain false for local-only validation",
            )

    return flags


def _require_no_order_creation_intent(order: Mapping[str, object]) -> None:
    for field_name in ORDER_CREATION_IMPLICATION_FIELDS:
        if field_name in order:
            _require(
                order[field_name] is False,
                f"{field_name} must be false because validation must not create paper orders",
            )


def validate_local_paper_order_intent(
    order: Mapping[str, object],
    *,
    portfolio_registry: Mapping[str, Mapping[str, object]] | None = None,
) -> dict[str, object]:
    """Validate a local paper-order intent without IO, endpoints, persistence, or mutation."""

    _require(isinstance(order, Mapping), "order must be a mapping")
    before_validation = deepcopy(dict(order))

    portfolio_id = _require_non_empty_string(order.get("portfolio_id"), "portfolio_id")
    symbol = _require_non_empty_string(order.get("symbol"), "symbol")
    _require(
        HK_SYMBOL_PATTERN.fullmatch(symbol) is not None,
        "symbol must use conservative HK ticker format like 0700.HK",
    )

    side = _require_non_empty_string(order.get("side"), "side")
    _require(side in VALID_ORDER_SIDES, "side must be buy or sell")

    quantity = _require_non_negative_number(order.get("quantity"), "quantity")

    order_type_value = order.get("order_type", "market")
    order_type = _require_non_empty_string(order_type_value, "order_type")
    _require(order_type in VALID_ORDER_TYPES, "order_type must be market or limit")

    limit_price = order.get("limit_price")
    if limit_price is not None:
        limit_price = _require_non_negative_number(limit_price, "limit_price")

    if portfolio_registry is not None:
        _require(
            isinstance(portfolio_registry, Mapping),
            "portfolio_registry must be a mapping when supplied",
        )
        _require(
            portfolio_id in portfolio_registry,
            f"portfolio_id {portfolio_id!r} was not found in the local portfolio registry",
        )

    _require_no_order_creation_intent(order)
    boundary_flags = _require_boundary_flags_remain_false(order)

    _require(
        dict(order) == before_validation,
        "validation must not mutate the input paper-order intent",
    )

    return {
        "validation_status": "passed",
        "record_type": LOCAL_PAPER_ORDER_RECORD_TYPE,
        "canonical_schema_table": LOCAL_PAPER_ORDER_SCHEMA_TABLE,
        "portfolio_id": portfolio_id,
        "symbol": symbol,
        "side": side,
        "quantity": quantity,
        "order_type": order_type,
        "limit_price": limit_price,
        "would_create_order": False,
        "locked_endpoint_reference": LOCAL_PAPER_ORDER_ENDPOINT_REFERENCE,
        "locked_endpoint_references": list(LOCKED_ENDPOINT_NAMES),
        "notes": [
            "Task 008C validates a paper-order intent locally only.",
            "No paper order is created and no public endpoint runtime surface is enabled.",
        ],
        **boundary_flags,
    }


def build_local_paper_order_validation_report(
    order: Mapping[str, object],
    *,
    portfolio_registry: Mapping[str, Mapping[str, object]] | None = None,
) -> dict[str, object]:
    """Build a reviewable local-only validation report for a paper-order intent."""

    validation_result = validate_local_paper_order_intent(
        order,
        portfolio_registry=portfolio_registry,
    )
    return {
        "report_name": "Task 008C — Local-only Paper Order Validation Service / Stub",
        "validation_status": validation_result["validation_status"],
        "record_type": validation_result["record_type"],
        "validated_order": {
            "portfolio_id": validation_result["portfolio_id"],
            "symbol": validation_result["symbol"],
            "side": validation_result["side"],
            "quantity": validation_result["quantity"],
            "order_type": validation_result["order_type"],
            "limit_price": validation_result["limit_price"],
        },
        "boundary_flags": {
            flag_name: validation_result[flag_name]
            for flag_name in LOCAL_PAPER_ORDER_BOUNDARY_FLAGS
        },
        "would_create_order": validation_result["would_create_order"],
        "locked_endpoint_reference": validation_result["locked_endpoint_reference"],
        "notes": validation_result["notes"],
    }
