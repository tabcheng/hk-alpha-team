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
        pytest.skip("HK_ALPHA_TEST_POSTGRES_DSN is required for local/test endpoint PostgreSQL reset")
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
def endpoint_postgres_dsn() -> str:
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


def _payload(origin: str) -> dict:
    payload = build_sample_simulation_origin_payload(origin)
    payload["portfolio_id"] = "endpoint-paper-portfolio-001"
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


def _assert_advisory_local_test_disclosures(envelope: dict) -> None:
    warning_text = " ".join(envelope["warnings"]).lower()
    for phrase in [
        "paper-only",
        "advisory-only",
        "local_test_postgres",
        "no production supabase",
        "no broker api",
        "no real-money",
        "no secrets",
    ]:
        assert phrase in warning_text


def _assert_persisted_roundtrip(envelope: dict, origin: str) -> None:
    _assert_success_envelope(envelope)
    _assert_advisory_local_test_disclosures(envelope)
    data = envelope["data"]
    assert envelope["metadata"]["simulation_persistence_mode"] == SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES
    assert envelope["metadata"]["production_supabase_connected"] is False
    assert envelope["metadata"]["broker_api_called"] is False
    assert envelope["metadata"]["real_money_order_placed"] is False
    persistence_metadata = data["local_test_persistence"]["metadata"]
    assert persistence_metadata["simulation_persistence_mode"] == SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES
    assert persistence_metadata["database_url_authorizes_persistence"] is False
    assert data["paper_order"]["simulation_origin"] == origin
    assert data["paper_order"]["persistence_write_performed"] is False

    persistence = data["local_test_persistence"]
    assert persistence["mode"] == SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES
    assert persistence["scope"] == "local_test_postgresql_only"
    assert persistence["paper_order_written_and_read_back"] is True
    assert persistence["production_supabase_connected"] is False
    assert persistence["supabase_client_used"] is False
    assert persistence["broker_api_called"] is False
    assert persistence["real_money_order_placed"] is False
    assert persistence["secrets_required"] is False

    persisted = persistence["persisted_paper_order"]
    assert persisted["simulation_origin"] == origin
    assert persisted["paper_order_origin"] == origin
    assert persisted["portfolio_id"] == data["paper_order"]["portfolio_id"]
    assert persisted["symbol"] == data["paper_order"]["symbol"]
    assert persisted["boundary_flags_json"]["paper_only"] is True
    assert persisted["boundary_flags_json"]["advisory_only"] is True
    assert persisted["boundary_flags_json"]["real_money_order_placed"] is False
    assert persisted["boundary_flags_json"]["broker_api_called"] is False
    assert persisted["boundary_flags_json"]["production_supabase_connected"] is False
    assert persisted["boundary_flags_json"]["proposals_reviewable"] is True
    assert persisted["boundary_flags_json"]["proposals_auto_applied"] is False
    assert persisted["boundary_flags_json"]["losing_outcomes_remain_visible"] is True
    assert persisted["boundary_flags_json"]["historical_recommendations_overwritten"] is False
    assert persisted["outcome_preview_json"].get("losing_outcome_visible") is True


def test_default_memory_mode_does_not_require_postgresql_or_database_url(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:5432/production_app")

    response = client.post("/api/v1/simulation/paper-orders", json=_payload("user_recorded"))

    assert response.status_code == 200
    envelope = response.json()
    _assert_success_envelope(envelope)
    assert "local_test_persistence" not in envelope["data"]
    assert "simulation_persistence_mode" not in envelope["metadata"]
    assert "database_url_authorizes_persistence" not in envelope["metadata"]
    assert "runtime_metadata" not in envelope["data"]
    assert envelope["data"]["paper_order"]["status"] == "recorded_in_memory_only"
    assert envelope["data"]["paper_order"]["persistence_write_performed"] is False


def test_local_test_postgres_mode_writes_and_reads_user_recorded(
    monkeypatch: pytest.MonkeyPatch,
    endpoint_postgres_dsn: str,
) -> None:
    monkeypatch.setenv(SIMULATION_PERSISTENCE_MODE_ENV, SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES)
    monkeypatch.setenv(TEST_POSTGRES_DSN_ENV, endpoint_postgres_dsn)

    response = client.post("/api/v1/simulation/paper-orders", json=_payload("user_recorded"))

    assert response.status_code == 200
    envelope = response.json()
    _assert_persisted_roundtrip(envelope, "user_recorded")
    assert envelope["data"]["learning_proposal_preview"] is None
    assert envelope["data"]["local_test_persistence"]["persisted_paper_order"]["source_metadata_json"]["user_recorded_notes"]
    assert envelope["data"]["local_test_persistence"]["persisted_paper_order"]["historical_recommendation_fields_json"]["original_recommendation"] is None


def test_local_test_postgres_mode_writes_and_reads_system_generated_learning(
    monkeypatch: pytest.MonkeyPatch,
    endpoint_postgres_dsn: str,
) -> None:
    monkeypatch.setenv(SIMULATION_PERSISTENCE_MODE_ENV, SIMULATION_PERSISTENCE_LOCAL_TEST_POSTGRES)
    monkeypatch.setenv(TEST_POSTGRES_DSN_ENV, endpoint_postgres_dsn)

    response = client.post("/api/v1/simulation/paper-orders", json=_payload("system_generated_learning"))

    assert response.status_code == 200
    envelope = response.json()
    _assert_persisted_roundtrip(envelope, "system_generated_learning")
    proposal = envelope["data"]["learning_proposal_preview"]
    persisted = envelope["data"]["local_test_persistence"]["persisted_paper_order"]
    assert proposal["requires_human_review"] is True
    assert proposal["auto_apply"] is False
    assert proposal["status"] == "preview_only_not_applied"
    assert persisted["requires_human_review"] is True
    assert persisted["source_metadata_json"]["system_learning_reason"]
    assert persisted["historical_recommendation_fields_json"]["original_recommendation"] == "WAIT_FOR_PULLBACK"
    assert persisted["outcome_preview_json"]["pnl"] == -1550.0
    assert persisted["outcome_preview_json"]["losing_outcome_visible"] is True


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
def test_unsafe_or_missing_local_test_postgres_config_fails_safely(
    monkeypatch: pytest.MonkeyPatch,
    env_updates: dict[str, str],
    expected_message: str,
) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql://postgres:postgres@127.0.0.1:5432/production_app")
    for key, value in env_updates.items():
        monkeypatch.setenv(key, value)

    response = client.post("/api/v1/simulation/paper-orders", json=_payload("user_recorded"))

    assert response.status_code == 500
    envelope = response.json()
    assert set(envelope) == {"request_id", "status", "error"}
    assert envelope["status"] == "error"
    assert envelope["error"]["code"] == "CONFIGURATION_ERROR"
    assert expected_message in envelope["error"]["details"]["message"]
    assert envelope["error"]["details"]["production_supabase_connected"] is False
    assert envelope["error"]["details"]["database_url_authorizes_persistence"] is False
