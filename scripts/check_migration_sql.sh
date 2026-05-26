#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MIGRATION_FILE="${ROOT_DIR}/supabase/migrations/0001_create_core_schema.sql"

: "${PGHOST:=127.0.0.1}"
: "${PGPORT:=5432}"
: "${PGUSER:=postgres}"
: "${PGPASSWORD:=postgres}"
: "${PGDATABASE:=hk_alpha_validation}"
export PGHOST PGPORT PGUSER PGPASSWORD PGDATABASE

if ! command -v psql >/dev/null 2>&1; then
  echo "ERROR: psql is required for SQL migration validation." >&2
  exit 1
fi

if [[ ! -f "${MIGRATION_FILE}" ]]; then
  echo "ERROR: migration file not found: ${MIGRATION_FILE}" >&2
  exit 1
fi

echo "[check] verifying postgres connectivity"
psql -v ON_ERROR_STOP=1 -d postgres -c 'select version();' >/dev/null

echo "[check] resetting validation database: ${PGDATABASE}"
psql -v ON_ERROR_STOP=1 -d postgres -c "drop database if exists ${PGDATABASE};"
psql -v ON_ERROR_STOP=1 -d postgres -c "create database ${PGDATABASE};"

echo "[check] applying migration: ${MIGRATION_FILE}"
psql -v ON_ERROR_STOP=1 -d "${PGDATABASE}" -f "${MIGRATION_FILE}" >/dev/null

echo "[check] validating expected table count"
TABLE_COUNT="$(psql -v ON_ERROR_STOP=1 -d "${PGDATABASE}" -tAc "select count(*) from information_schema.tables where table_schema='public';" | tr -d '[:space:]')"
if [[ "${TABLE_COUNT}" != "18" ]]; then
  echo "ERROR: expected 18 public tables, found ${TABLE_COUNT}" >&2
  exit 1
fi

echo "[check] validating required critical constraints"
CONSTRAINT_COUNT="$(psql -v ON_ERROR_STOP=1 -d "${PGDATABASE}" -tAc "select count(*) from pg_constraint where conname in ('ck_strategy_recommendations_confidence_level_range','ck_agent_runs_status');" | tr -d '[:space:]')"
if [[ "${CONSTRAINT_COUNT}" != "2" ]]; then
  echo "ERROR: expected 2 required constraints, found ${CONSTRAINT_COUNT}" >&2
  exit 1
fi

echo "Migration SQL validation passed."
