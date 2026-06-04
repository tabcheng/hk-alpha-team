from __future__ import annotations

from copy import deepcopy

import pytest

from app.simulation_order_validation import (
    LOCAL_PAPER_ORDER_BOUNDARY_FLAGS,
    build_local_paper_order_validation_report,
    validate_local_paper_order_intent,
)


def _valid_order() -> dict[str, object]:
    return {
        "portfolio_id": "fixture-paper-portfolio-001",
        "symbol": "0700.HK",
        "side": "buy",
        "quantity": 100,
        "order_type": "limit",
        "limit_price": 375.5,
    }


def _portfolio_registry() -> dict[str, dict[str, object]]:
    return {
        "fixture-paper-portfolio-001": {
            "portfolio_uuid": "paper-portfolio-fixture-001",
            "status": "active",
        }
    }


def test_task_008c_valid_local_paper_order_intent_passes() -> None:
    result = validate_local_paper_order_intent(_valid_order())

    assert result["validation_status"] == "passed"
    assert result["record_type"] == "paper_order_intent"
    assert result["canonical_schema_table"] == "paper_orders"
    assert result["locked_endpoint_reference"] == "POST /api/v1/simulation/paper-orders"


def test_task_008c_valid_market_buy_passes() -> None:
    order = _valid_order()
    order.update({"side": "buy", "order_type": "market", "limit_price": None})

    result = validate_local_paper_order_intent(order)

    assert result["side"] == "buy"
    assert result["order_type"] == "market"
    assert result["limit_price"] is None


def test_task_008c_valid_market_sell_passes() -> None:
    order = _valid_order()
    order.update({"side": "sell", "order_type": "market", "limit_price": None})

    result = validate_local_paper_order_intent(order)

    assert result["side"] == "sell"
    assert result["order_type"] == "market"


def test_task_008c_valid_limit_order_passes() -> None:
    result = validate_local_paper_order_intent(_valid_order())

    assert result["order_type"] == "limit"
    assert result["limit_price"] == 375.5


def test_task_008c_quantity_zero_passes_for_paper_order_intent() -> None:
    order = _valid_order()
    order["quantity"] = 0

    result = validate_local_paper_order_intent(order)

    assert result["quantity"] == 0


def test_task_008c_local_portfolio_registry_match_passes() -> None:
    result = validate_local_paper_order_intent(
        _valid_order(),
        portfolio_registry=_portfolio_registry(),
    )

    assert result["portfolio_id"] == "fixture-paper-portfolio-001"


def test_task_008c_validation_result_confirms_no_order_is_created() -> None:
    result = validate_local_paper_order_intent(_valid_order())

    assert result["would_create_order"] is False
    assert result["paper_order_created"] is False


def test_task_008c_validation_result_confirms_endpoint_runtime_disabled() -> None:
    result = validate_local_paper_order_intent(_valid_order())

    assert result["endpoint_runtime_enabled"] is False
    assert result["http_enabled"] is False


def test_task_008c_validation_does_not_mutate_input() -> None:
    order = _valid_order()
    before_validation = deepcopy(order)

    report = build_local_paper_order_validation_report(order)

    assert report["validation_status"] == "passed"
    assert order == before_validation


def test_task_008c_missing_portfolio_id_fails() -> None:
    order = _valid_order()
    order.pop("portfolio_id")

    with pytest.raises(ValueError, match="portfolio_id"):
        validate_local_paper_order_intent(order)


def test_task_008c_unknown_portfolio_id_fails_when_registry_is_supplied() -> None:
    order = _valid_order()
    order["portfolio_id"] = "unknown-portfolio"

    with pytest.raises(ValueError, match="not found in the local portfolio registry"):
        validate_local_paper_order_intent(order, portfolio_registry=_portfolio_registry())


def test_task_008c_missing_symbol_fails() -> None:
    order = _valid_order()
    order.pop("symbol")

    with pytest.raises(ValueError, match="symbol"):
        validate_local_paper_order_intent(order)


def test_task_008c_malformed_symbol_fails() -> None:
    order = _valid_order()
    order["symbol"] = "700.HK"

    with pytest.raises(ValueError, match="0700.HK"):
        validate_local_paper_order_intent(order)


def test_task_008c_invalid_side_fails() -> None:
    order = _valid_order()
    order["side"] = "hold"

    with pytest.raises(ValueError, match="side must be buy or sell"):
        validate_local_paper_order_intent(order)


def test_task_008c_invalid_order_type_fails() -> None:
    order = _valid_order()
    order["order_type"] = "stop"

    with pytest.raises(ValueError, match="order_type must be market or limit"):
        validate_local_paper_order_intent(order)


def test_task_008c_negative_quantity_fails() -> None:
    order = _valid_order()
    order["quantity"] = -1

    with pytest.raises(ValueError, match="quantity must be non-negative"):
        validate_local_paper_order_intent(order)


def test_task_008c_negative_limit_price_fails() -> None:
    order = _valid_order()
    order["limit_price"] = -0.01

    with pytest.raises(ValueError, match="limit_price must be non-negative"):
        validate_local_paper_order_intent(order)


@pytest.mark.parametrize(
    "flag_name",
    [
        "endpoint_runtime_enabled",
        "persistence_enabled",
        "database_write_enabled",
        "production_supabase_required",
        "supabase_client_required",
        "broker_execution_enabled",
        "broker_api_called",
        "real_money_order_placed",
        "external_api_required",
        "secrets_required",
    ],
)
def test_task_008c_forbidden_top_level_boundary_flag_true_fails(flag_name: str) -> None:
    assert flag_name in LOCAL_PAPER_ORDER_BOUNDARY_FLAGS
    order = _valid_order()
    order[flag_name] = True

    with pytest.raises(ValueError, match=f"{flag_name} must remain false"):
        validate_local_paper_order_intent(order)


@pytest.mark.parametrize(
    "flag_name",
    [
        "database_write_enabled",
        "supabase_client_required",
        "broker_api_called",
    ],
)
def test_task_008c_forbidden_nested_boundary_flag_true_fails(flag_name: str) -> None:
    assert flag_name in LOCAL_PAPER_ORDER_BOUNDARY_FLAGS
    order = _valid_order()
    order["boundary_flags"] = {flag_name: True}

    with pytest.raises(ValueError, match=f"{flag_name} must remain false"):
        validate_local_paper_order_intent(order)


@pytest.mark.parametrize(
    "field_name",
    [
        "would_create_order",
        "create_order",
        "order_created",
        "paper_order_created",
        "execute_order",
        "submit_order",
        "place_order",
    ],
)
def test_task_008c_any_input_implying_actual_order_creation_fails(field_name: str) -> None:
    order = _valid_order()
    order[field_name] = True

    with pytest.raises(ValueError, match="must be false.*must not create paper orders"):
        validate_local_paper_order_intent(order)
