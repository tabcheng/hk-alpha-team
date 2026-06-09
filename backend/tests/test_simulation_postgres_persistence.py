from __future__ import annotations

import ast
import os
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

import pytest

from app.simulation_origin_contract import build_sample_simulation_origin_payload
from app.simulation_persistence_boundary import FALSE_BOUNDARY_FLAGS, build_paper_order_persistence_payload
from app.simulation_runtime import create_paper_order_record
from app.simulation_store import simulation_store

ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS_DIR = ROOT / "supabase" / "migrations"
APPROVED_TEST_DATABASE_NAMES = {"hk_alpha_validation", "hk_alpha_test"}
APPROVED_TEST_DATABASE_PREFIXES = ("hk_alpha_validation_", "hk_alpha_test_")


def _configured_test_dsn() -> str | None:
    return os.environ.get("HK_ALPHA_TEST_POSTGRES_DSN")


def _database_name_from_dsn(dsn: str) -> str:
    return unquote(urlsplit(dsn).path.lstrip("/"))


def _is_approved_test_database_name(database_name: str) -> bool:
    return database_name in APPROVED_TEST_DATABASE_NAMES or database_name.startswith(APPROVED_TEST_DATABASE_PREFIXES)


def _approved_test_database_name_or_skip(dsn: str | None) -> str:
    if not dsn:
        pytest.skip("HK_ALPHA_TEST_POSTGRES_DSN is required for destructive local/test PostgreSQL reset")
    database_name = _database_name_from_dsn(dsn)
    if not _is_approved_test_database_name(database_name):
        pytest.skip(
            "HK_ALPHA_TEST_POSTGRES_DSN database name must be hk_alpha_validation, hk_alpha_test, "
            "or start with hk_alpha_validation_ / hk_alpha_test_ before destructive reset"
        )
    return database_name


def _maintenance_dsn(dsn: str) -> str:
    parts = urlsplit(dsn)
    return urlunsplit((parts.scheme, parts.netloc, "/postgres", parts.query, parts.fragment))


@pytest.fixture(scope="session")
def postgres_dsn() -> str:
    dsn = _configured_test_dsn()
    dbname = _approved_test_database_name_or_skip(dsn)
    assert dsn is not None
    try:
        import psycopg as psycopg_module
        from psycopg import sql
    except ImportError as exc:
        raise AssertionError("psycopg is required when HK_ALPHA_TEST_POSTGRES_DSN is configured") from exc

    try:
        with psycopg_module.connect(_maintenance_dsn(dsn), connect_timeout=3, autocommit=True) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql.SQL("drop database if exists {}").format(sql.Identifier(dbname)))
                cursor.execute(sql.SQL("create database {}").format(sql.Identifier(dbname)))
    except psycopg_module.OperationalError as exc:
        raise AssertionError("configured local/test PostgreSQL DSN is not reachable") from exc

    with psycopg_module.connect(dsn, autocommit=True) as connection:
        with connection.cursor() as cursor:
            for migration_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
                cursor.execute(migration_file.read_text(encoding="utf-8"))
    return dsn


def test_database_url_alone_is_ignored_for_destructive_roundtrip_reset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("HK_ALPHA_TEST_POSTGRES_DSN", raising=False)
    monkeypatch.setenv("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:5432/production_app")

    assert _configured_test_dsn() is None
    with pytest.raises(pytest.skip.Exception, match="HK_ALPHA_TEST_POSTGRES_DSN is required"):
        _approved_test_database_name_or_skip(_configured_test_dsn())


def test_unsafe_hk_alpha_test_dsn_is_skipped_before_destructive_reset() -> None:
    unsafe_dsn = "postgresql://postgres:postgres@127.0.0.1:5432/production_app"

    with pytest.raises(pytest.skip.Exception, match="database name must be"):
        _approved_test_database_name_or_skip(unsafe_dsn)


def test_approved_test_database_names_are_allowed_before_destructive_reset() -> None:
    approved_names = [
        "hk_alpha_validation",
        "hk_alpha_test",
        "hk_alpha_validation_pr33",
        "hk_alpha_test_roundtrip",
    ]

    for database_name in approved_names:
        dsn = f"postgresql://postgres:postgres@127.0.0.1:5432/{database_name}"
        assert _approved_test_database_name_or_skip(dsn) == database_name


def test_non_approved_database_names_are_not_allowed_before_destructive_reset() -> None:
    unsafe_names = ["postgres", "hk_alpha", "hk_alpha_prod", "production_app", "app_hk_alpha_test"]

    for database_name in unsafe_names:
        dsn = f"postgresql://postgres:postgres@127.0.0.1:5432/{database_name}"
        with pytest.raises(pytest.skip.Exception, match="database name must be"):
            _approved_test_database_name_or_skip(dsn)


@pytest.fixture(autouse=True)
def reset_store() -> None:
    simulation_store.reset()


def _persistence_payload(origin: str) -> dict:
    runtime_payload = build_sample_simulation_origin_payload(origin)
    runtime_payload["portfolio_id"] = "runtime-paper-portfolio-001"
    runtime_payload["paper_only"] = True
    runtime_payload["boundary_flags"] = {flag_name: False for flag_name in FALSE_BOUNDARY_FLAGS}
    runtime_record = create_paper_order_record(runtime_payload)["paper_order"]
    return build_paper_order_persistence_payload(runtime_record)


def _assert_roundtrip_preserves_payload(intent: dict, persisted: dict) -> None:
    assert persisted["portfolio_id"] == intent["portfolio_id"]
    assert persisted["symbol"] == intent["symbol"]
    assert persisted["side"] == intent["side"]
    assert persisted["quantity"] == float(intent["quantity"])
    assert persisted["simulation_origin"] == intent["simulation_origin"]
    assert persisted["paper_order_origin"] == intent["paper_order_origin"]
    assert persisted["created_by_type"] == intent["created_by_type"]
    assert persisted["requires_human_review"] == intent["requires_human_review"]
    assert persisted["boundary_flags_json"] == intent["boundary_flags_json"]
    assert persisted["source_metadata_json"] == intent["source_metadata_json"]
    assert persisted["historical_recommendation_fields_json"] == intent["historical_recommendation_fields_json"]
    assert persisted["outcome_preview_json"] == intent["outcome_preview_json"]

    assert persisted["boundary_flags_json"]["paper_only"] is True
    assert persisted["boundary_flags_json"]["advisory_only"] is True
    assert persisted["boundary_flags_json"]["human_in_the_loop"] is True
    assert persisted["boundary_flags_json"]["real_money_order_placed"] is False
    assert persisted["boundary_flags_json"]["broker_api_called"] is False
    assert persisted["boundary_flags_json"]["production_supabase_connected"] is False
    assert persisted["boundary_flags_json"]["secrets_required"] is False
    assert persisted["boundary_flags_json"]["proposals_reviewable"] is True
    assert persisted["boundary_flags_json"]["proposals_auto_applied"] is False
    assert persisted["boundary_flags_json"]["losing_outcomes_remain_visible"] is True
    assert persisted["boundary_flags_json"]["historical_recommendations_overwritten"] is False
    assert persisted["outcome_preview_json"]["losing_outcome_visible"] is True

    adapter_flags = persisted["local_test_adapter_boundary_flags"]
    assert adapter_flags["production_supabase_connected"] is False
    assert adapter_flags["supabase_client_used"] is False
    assert adapter_flags["vendor_api_called"] is False
    assert adapter_flags["live_market_data_called"] is False
    assert adapter_flags["broker_api_called"] is False
    assert adapter_flags["real_money_order_placed"] is False
    assert adapter_flags["secrets_required"] is False


def test_user_recorded_paper_order_write_read_roundtrip(postgres_dsn: str) -> None:
    intent = _persistence_payload("user_recorded")
    from app.simulation_postgres_persistence import LocalTestPostgresSimulationPersistence

    adapter = LocalTestPostgresSimulationPersistence(postgres_dsn)

    persisted = adapter.write_paper_order_payload(intent)

    _assert_roundtrip_preserves_payload(intent, persisted)
    assert persisted["simulation_origin"] == "user_recorded"
    assert persisted["source_metadata_json"]["user_recorded_notes"] == "Human-recorded paper trade journal entry."
    assert persisted["historical_recommendation_fields_json"]["original_recommendation"] is None


def test_system_generated_learning_paper_order_write_read_roundtrip(postgres_dsn: str) -> None:
    intent = _persistence_payload("system_generated_learning")
    from app.simulation_postgres_persistence import LocalTestPostgresSimulationPersistence

    adapter = LocalTestPostgresSimulationPersistence(postgres_dsn)

    persisted = adapter.write_paper_order_payload(intent)

    _assert_roundtrip_preserves_payload(intent, persisted)
    assert persisted["simulation_origin"] == "system_generated_learning"
    assert persisted["requires_human_review"] is True
    assert persisted["source_metadata_json"]["system_learning_reason"]
    assert persisted["historical_recommendation_fields_json"]["original_recommendation"] == "WAIT_FOR_PULLBACK"
    assert persisted["outcome_preview_json"]["pnl"] == -1550.0
    assert persisted["outcome_preview_json"]["losing_outcome_visible"] is True


def test_postgres_adapter_has_no_supabase_vendor_broker_or_secret_imports() -> None:
    source_path = Path("backend/app/simulation_postgres_persistence.py")
    source_text = source_path.read_text(encoding="utf-8").lower()
    tree = ast.parse(source_path.read_text(encoding="utf-8"))
    imported_modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported_modules.extend(alias.name for alias in node.names)
        if isinstance(node, ast.ImportFrom) and node.module:
            imported_modules.append(node.module)

    assert not any("supabase" in module.lower() for module in imported_modules)
    forbidden_tokens = [
        "supabase.create_client",
        "import requests",
        "urllib.request",
        "place_real_money_order",
        "fetch_live_market_data",
        "api_key",
        "service_role",
    ]
    for token in forbidden_tokens:
        assert token not in source_text


def test_read_paper_orders_for_portfolio_returns_deterministic_order_evidence(postgres_dsn: str) -> None:
    from app.simulation_postgres_persistence import LocalTestPostgresSimulationPersistence

    adapter = LocalTestPostgresSimulationPersistence(postgres_dsn)
    user_intent = _persistence_payload("user_recorded")
    learning_intent = _persistence_payload("system_generated_learning")
    user_intent["portfolio_id"] = "runtime-paper-portfolio-read-model-008m"
    learning_intent["portfolio_id"] = user_intent["portfolio_id"]

    adapter.write_paper_order_payload(user_intent)
    adapter.write_paper_order_payload(learning_intent)
    persisted_orders = adapter.read_paper_orders_for_portfolio(user_intent["portfolio_id"])

    assert [order["simulation_origin"] for order in persisted_orders] == ["user_recorded", "system_generated_learning"]
    assert persisted_orders[0]["source_metadata_json"]["user_recorded_notes"] == "Human-recorded paper trade journal entry."
    assert persisted_orders[0]["learning_proposal_readback"] is None
    assert persisted_orders[1]["requires_human_review"] is True
    learning_readback = persisted_orders[1]["learning_proposal_readback"]
    assert learning_readback["requires_human_review"] is True
    assert learning_readback["auto_apply"] is False
    assert learning_readback["status"] == "preview_only_not_applied"
    assert learning_readback["readback_source"] == "local_test_postgresql_paper_orders"
    assert persisted_orders[1]["historical_recommendation_fields_json"]["original_recommendation"] == "WAIT_FOR_PULLBACK"
    assert persisted_orders[1]["outcome_preview_json"]["losing_outcome_visible"] is True
    assert persisted_orders[1]["local_test_adapter_boundary_flags"]["broker_api_called"] is False
