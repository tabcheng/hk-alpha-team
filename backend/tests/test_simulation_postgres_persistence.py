from __future__ import annotations

import ast
import os
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import pytest

from app.simulation_origin_contract import build_sample_simulation_origin_payload
from app.simulation_persistence_boundary import FALSE_BOUNDARY_FLAGS, build_paper_order_persistence_payload
from app.simulation_runtime import create_paper_order_record
from app.simulation_store import simulation_store

ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS_DIR = ROOT / "supabase" / "migrations"
DEFAULT_DSN = "postgresql://postgres:postgres@127.0.0.1:5432/hk_alpha_validation"


def _explicit_dsn_requested() -> bool:
    return "HK_ALPHA_TEST_POSTGRES_DSN" in os.environ or "DATABASE_URL" in os.environ


def _dsn() -> str:
    return os.environ.get("HK_ALPHA_TEST_POSTGRES_DSN") or os.environ.get("DATABASE_URL") or DEFAULT_DSN


def _maintenance_dsn(dsn: str) -> str:
    parts = urlsplit(dsn)
    return urlunsplit((parts.scheme, parts.netloc, "/postgres", parts.query, parts.fragment))


def _database_name(dsn: str) -> str:
    return urlsplit(dsn).path.lstrip("/") or "hk_alpha_validation"


@pytest.fixture(scope="session")
def postgres_dsn() -> str:
    dsn = _dsn()
    try:
        import psycopg as psycopg_module
        from psycopg import sql
    except ImportError as exc:
        if _explicit_dsn_requested():
            raise AssertionError("psycopg is required when PostgreSQL DSN is explicitly configured") from exc
        pytest.skip(f"psycopg is unavailable for optional local PostgreSQL roundtrip validation: {exc}")

    try:
        with psycopg_module.connect(_maintenance_dsn(dsn), connect_timeout=3, autocommit=True) as connection:
            dbname = _database_name(dsn)
            with connection.cursor() as cursor:
                cursor.execute(sql.SQL("drop database if exists {}").format(sql.Identifier(dbname)))
                cursor.execute(sql.SQL("create database {}").format(sql.Identifier(dbname)))
    except psycopg_module.OperationalError as exc:
        if _explicit_dsn_requested():
            raise AssertionError("explicitly configured local/test PostgreSQL DSN is not reachable") from exc
        pytest.skip(f"local/test PostgreSQL is unavailable for Task 008K roundtrip validation: {exc}")

    with psycopg_module.connect(dsn, autocommit=True) as connection:
        with connection.cursor() as cursor:
            for migration_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
                cursor.execute(migration_file.read_text(encoding="utf-8"))
    return dsn


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
