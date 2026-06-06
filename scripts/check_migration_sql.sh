#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MIGRATIONS_DIR="${ROOT_DIR}/supabase/migrations"

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

if [[ ! -d "${MIGRATIONS_DIR}" ]]; then
  echo "ERROR: migrations directory not found: ${MIGRATIONS_DIR}" >&2
  exit 1
fi
mapfile -t MIGRATION_FILES < <(find "${MIGRATIONS_DIR}" -maxdepth 1 -type f -name "*.sql" | sort)
if [[ "${#MIGRATION_FILES[@]}" -eq 0 ]]; then
  echo "ERROR: no migration SQL files found in ${MIGRATIONS_DIR}" >&2
  exit 1
fi

echo "[check] verifying postgres connectivity"
psql -v ON_ERROR_STOP=1 -d postgres -c 'select version();' >/dev/null

echo "[check] resetting validation database: ${PGDATABASE}"
psql -v ON_ERROR_STOP=1 -d postgres -c "drop database if exists ${PGDATABASE};"
psql -v ON_ERROR_STOP=1 -d postgres -c "create database ${PGDATABASE};"

for migration_file in "${MIGRATION_FILES[@]}"; do
  echo "[check] applying migration: ${migration_file}"
  psql -v ON_ERROR_STOP=1 -d "${PGDATABASE}" -f "${migration_file}" >/dev/null
done

echo "[check] validating expected table count"
TABLE_COUNT="$(psql -v ON_ERROR_STOP=1 -d "${PGDATABASE}" -tAc "select count(*) from information_schema.tables where table_schema='public';" | tr -d '[:space:]')"
if [[ "${TABLE_COUNT}" != "18" ]]; then
  echo "ERROR: expected 18 public tables, found ${TABLE_COUNT}" >&2
  exit 1
fi

echo "[check] validating required critical constraints"
CONSTRAINT_COUNT="$(psql -v ON_ERROR_STOP=1 -d "${PGDATABASE}" -tAc "select count(*) from pg_constraint where conname in ('ck_strategy_recommendations_confidence_level_range','ck_agent_runs_status','ck_learning_proposals_auto_apply_false');" | tr -d '[:space:]')"
if [[ "${CONSTRAINT_COUNT}" != "3" ]]; then
  echo "ERROR: expected 3 required constraints, found ${CONSTRAINT_COUNT}" >&2
  exit 1
fi

echo "[check] validating Task 008J additive migration columns"
COLUMN_COUNT="$(psql -v ON_ERROR_STOP=1 -d "${PGDATABASE}" -tAc "
  select count(*)
  from information_schema.columns
  where table_schema = 'public'
    and (table_name, column_name) in (
      ('paper_orders', 'simulation_origin'),
      ('paper_orders', 'paper_order_origin'),
      ('paper_orders', 'boundary_flags_json'),
      ('paper_positions', 'simulation_origin'),
      ('portfolio_snapshots', 'simulation_origin_summary_json'),
      ('trade_reviews', 'simulation_origin'),
      ('learning_proposals', 'auto_apply'),
      ('audit_events', 'simulation_origin')
    );
" | tr -d '[:space:]')"
if [[ "${COLUMN_COUNT}" != "8" ]]; then
  echo "ERROR: expected 8 Task 008J additive columns, found ${COLUMN_COUNT}" >&2
  exit 1
fi

echo "[check] validating Task 008J additive migration indexes"
INDEX_COUNT="$(psql -v ON_ERROR_STOP=1 -d "${PGDATABASE}" -tAc "
  select count(*)
  from pg_indexes
  where schemaname = 'public'
    and indexname in (
      'idx_paper_orders_simulation_origin_created_at_desc',
      'idx_paper_orders_source_recommendation_created_at_desc',
      'idx_paper_positions_simulation_origin_status',
      'idx_trade_reviews_simulation_origin_reviewed_at_desc',
      'idx_learning_proposals_simulation_origin_status_created_at_desc',
      'idx_audit_events_simulation_origin_created_at_desc'
    );
" | tr -d '[:space:]')"
if [[ "${INDEX_COUNT}" != "6" ]]; then
  echo "ERROR: expected 6 Task 008J additive indexes, found ${INDEX_COUNT}" >&2
  exit 1
fi

echo "Migration SQL validation passed."
