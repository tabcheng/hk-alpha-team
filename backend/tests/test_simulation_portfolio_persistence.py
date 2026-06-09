from __future__ import annotations

import os
from pathlib import Path
from urllib.parse import unquote, urlsplit, urlunsplit

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.simulation_origin_contract import build_sample_simulation_origin_payload
from app.simulation_runtime import (
    RUNTIME_FALSE_BOUNDARY_FLAGS,
    SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES,
    SIMULATION_PERSISTENCE_MODE_ENV,
    TEST_POSTGRES_DSN_ENV,
)
from app.simulation_store import simulation_store

ROOT = Path(__file__).resolve().parents[2]
MIGRATIONS_DIR = ROOT / "supabase" / "migrations"
APPROVED_TEST_DATABASE_NAMES = {"hk_alpha_validation", "hk_alpha_test"}
APPROVED_TEST_DATABASE_PREFIXES = ("hk_alpha_validation_", "hk_alpha_test_")

client = TestClient(app)


def _configured_test_dsn() -> str | None:
    return os.environ.get(TEST_POSTGRES_DSN_ENV)


def _database_name_from_dsn(dsn: str) -> str:
    return unquote(urlsplit(dsn).path.lstrip("/"))


def _is_approved_test_database_name(database_name: str) -> bool:
    return database_name in APPROVED_TEST_DATABASE_NAMES or database_name.startswith(APPROVED_TEST_DATABASE_PREFIXES)


def _approved_test_database_name_or_skip(dsn: str | None) -> str:
    if not dsn:
        pytest.skip("HK_ALPHA_TEST_POSTGRES_DSN is required for local/test portfolio PostgreSQL reset")
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
def portfolio_postgres_dsn() -> str:
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


@pytest.fixture(autouse=True)
def clean_env_and_store(monkeypatch: pytest.MonkeyPatch) -> None:
    simulation_store.reset()
    monkeypatch.delenv(SIMULATION_PERSISTENCE_MODE_ENV, raising=False)
    monkeypatch.delenv(TEST_POSTGRES_DSN_ENV, raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)


def _payload(origin: str, portfolio_id: str = "portfolio-persist-008m") -> dict:
    payload = build_sample_simulation_origin_payload(origin)
    payload["portfolio_id"] = portfolio_id
    payload["paper_only"] = True
    payload["boundary_flags"] = {flag_name: False for flag_name in RUNTIME_FALSE_BOUNDARY_FLAGS}
    return payload


def _assert_success_envelope(envelope: dict) -> None:
    assert set(envelope) == {"request_id", "status", "data", "metadata", "warnings"}
    assert envelope["status"] == "success"
    assert envelope["metadata"]["schema_version"] == "v0.1"
    assert envelope["metadata"]["source"] == "HK_ALPHA_TEAM"
    assert envelope["metadata"]["generated_at"]
    assert isinstance(envelope["warnings"], list)


def _assert_local_test_readback_disclosures(envelope: dict) -> None:
    warning_text = " ".join(envelope["warnings"]).lower()
    for phrase in [
        "paper-only",
        "advisory-only",
        "local/test postgresql persistence is enabled",
        "local_test_postgres",
        "hk_alpha_test_postgres_dsn",
        "database_url alone is ignored",
        "no production supabase",
        "no broker api",
        "no real-money",
        "no vendor api",
        "no live market data",
        "no secrets",
    ]:
        assert phrase in warning_text
    for contradictory_phrase in [
        "process-local in-memory records only",
        "no persistence write is performed",
        "in-memory records only",
    ]:
        assert contradictory_phrase not in warning_text


def _assert_configuration_error(envelope: dict, expected_message: str) -> None:
    assert set(envelope) == {"request_id", "status", "error"}
    assert envelope["status"] == "error"
    assert envelope["error"]["code"] == "CONFIGURATION_ERROR"
    assert expected_message in envelope["error"]["details"]["message"]
    assert envelope["error"]["details"]["production_supabase_connected"] is False
    assert envelope["error"]["details"]["database_url_authorizes_persistence"] is False


def test_default_memory_portfolio_mode_still_uses_in_memory_without_postgresql(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:5432/production_app")
    portfolio_id = "memory-portfolio-008m"
    post_response = client.post("/api/v1/simulation/paper-orders", json=_payload("user_recorded", portfolio_id))
    assert post_response.status_code == 200

    get_response = client.get(f"/api/v1/paper-portfolios/{portfolio_id}")

    assert get_response.status_code == 200
    envelope = get_response.json()
    _assert_success_envelope(envelope)
    assert "simulation_persistence_mode" not in envelope["metadata"]
    assert envelope["data"]["status"] == "in_memory_only_non_production"
    assert "local_test_persistence" not in envelope["data"]
    assert envelope["data"]["recent_paper_orders"][0]["simulation_origin"] == "user_recorded"
    warning_text = " ".join(envelope["warnings"]).lower()
    assert "process-local in-memory records only" in warning_text
    assert "no production supabase connection or persistence write is performed" in warning_text


def test_database_url_alone_does_not_enable_persisted_portfolio_readback(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:5432/hk_alpha_validation")

    response = client.get("/api/v1/paper-portfolios/database-url-only-008m")

    assert response.status_code == 404
    envelope = response.json()
    assert envelope["status"] == "error"
    assert envelope["error"]["code"] == "NOT_FOUND"
    assert "CONFIGURATION_ERROR" not in str(envelope)


def test_local_test_postgres_post_then_portfolio_get_reads_user_recorded_order(
    monkeypatch: pytest.MonkeyPatch,
    portfolio_postgres_dsn: str,
) -> None:
    portfolio_id = "persisted-user-008m"
    monkeypatch.setenv(SIMULATION_PERSISTENCE_MODE_ENV, SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES)
    monkeypatch.setenv(TEST_POSTGRES_DSN_ENV, portfolio_postgres_dsn)

    post_response = client.post("/api/v1/simulation/paper-orders", json=_payload("user_recorded", portfolio_id))
    assert post_response.status_code == 200
    get_response = client.get(f"/api/v1/paper-portfolios/{portfolio_id}")

    assert get_response.status_code == 200
    envelope = get_response.json()
    _assert_success_envelope(envelope)
    _assert_local_test_readback_disclosures(envelope)
    assert envelope["metadata"]["simulation_persistence_mode"] == SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES
    data = envelope["data"]
    assert data["status"] == "local_test_postgresql_readback_non_production"
    assert data["local_test_persistence"]["paper_orders_read_back"] is True
    assert data["local_test_persistence"]["paper_order_count"] == 1
    order = data["recent_paper_orders"][0]
    assert order["portfolio_id"] == portfolio_id
    assert order["simulation_origin"] == "user_recorded"
    assert order["paper_order_origin"] == "user_recorded"
    assert order["source_metadata_json"]["user_recorded_notes"] == "Human-recorded paper trade journal entry."
    assert order["historical_recommendation_fields_json"]["original_recommendation"] is None
    assert order["learning_proposal_readback"] is None
    assert order["boundary_flags_json"]["paper_only"] is True
    assert order["boundary_flags_json"]["advisory_only"] is True
    assert order["boundary_flags_json"]["real_money_order_placed"] is False
    assert order["local_test_adapter_boundary_flags"]["vendor_api_called"] is False


def test_local_test_postgres_portfolio_readback_preserves_system_learning_evidence(
    monkeypatch: pytest.MonkeyPatch,
    portfolio_postgres_dsn: str,
) -> None:
    portfolio_id = "persisted-learning-008m"
    monkeypatch.setenv(SIMULATION_PERSISTENCE_MODE_ENV, SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES)
    monkeypatch.setenv(TEST_POSTGRES_DSN_ENV, portfolio_postgres_dsn)

    post_response = client.post("/api/v1/simulation/paper-orders", json=_payload("system_generated_learning", portfolio_id))
    assert post_response.status_code == 200
    proposal = post_response.json()["data"]["learning_proposal_preview"]
    get_response = client.get(f"/api/v1/paper-portfolios/{portfolio_id}")

    assert get_response.status_code == 200
    envelope = get_response.json()
    _assert_success_envelope(envelope)
    _assert_local_test_readback_disclosures(envelope)
    order = envelope["data"]["recent_paper_orders"][0]
    assert order["simulation_origin"] == "system_generated_learning"
    assert order["paper_order_origin"] == "system_generated_learning"
    assert order["created_by_type"] == "system_agent"
    assert order["requires_human_review"] is True
    assert proposal["requires_human_review"] is True
    assert proposal["auto_apply"] is False
    assert proposal["status"] == "preview_only_not_applied"
    learning_readback = order["learning_proposal_readback"]
    assert learning_readback["proposal_type"] == "reviewable_learning_proposal_readback"
    assert learning_readback["requires_human_review"] is True
    assert learning_readback["auto_apply"] is False
    assert learning_readback["proposals_auto_applied"] is False
    assert learning_readback["status"] == "preview_only_not_applied"
    assert learning_readback["production_strategy_logic_changed"] is False
    assert learning_readback["readback_source"] == "local_test_postgresql_paper_orders"
    assert learning_readback["system_learning_reason"]
    assert learning_readback["improvement_suggestions"]
    assert order["boundary_flags_json"]["proposals_reviewable"] is True
    assert order["boundary_flags_json"]["proposals_auto_applied"] is False
    assert order["source_metadata_json"]["requires_human_review"] is True
    assert order["source_metadata_json"]["system_learning_reason"]
    assert order["source_metadata_json"]["improvement_suggestions"]
    assert order["historical_recommendation_fields_json"]["original_recommendation"] == "WAIT_FOR_PULLBACK"
    assert order["historical_recommendation_fields_json"]["original_scores"]["market_score"] == 62
    assert order["historical_recommendation_fields_json"]["original_thesis"]
    assert order["outcome_preview_json"]["pnl"] == -1550.0
    assert order["outcome_preview_json"]["losing_outcome_visible"] is True
    assert order["local_test_adapter_boundary_flags"]["real_money_order_placed"] is False


@pytest.mark.parametrize(
    "env_updates, expected_message",
    [
        (
            {SIMULATION_PERSISTENCE_MODE_ENV: SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES},
            "HK_ALPHA_TEST_POSTGRES_DSN is required",
        ),
        (
            {
                SIMULATION_PERSISTENCE_MODE_ENV: SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES,
                TEST_POSTGRES_DSN_ENV: "postgresql://postgres:postgres@127.0.0.1:5432/production_app",
            },
            "database name must be",
        ),
        (
            {SIMULATION_PERSISTENCE_MODE_ENV: "supabase"},
            "must be memory or local_test_postgres",
        ),
    ],
)
def test_unsafe_missing_or_unknown_portfolio_persistence_config_fails_safely(
    monkeypatch: pytest.MonkeyPatch,
    env_updates: dict[str, str],
    expected_message: str,
) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:5432/production_app")
    for key, value in env_updates.items():
        monkeypatch.setenv(key, value)

    response = client.get("/api/v1/paper-portfolios/config-fails-008m")

    assert response.status_code == 500
    _assert_configuration_error(response.json(), expected_message)
