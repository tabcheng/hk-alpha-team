# 39 — Task 008K Local/Test PostgreSQL Persistence Adapter

## Purpose

Task 008K adds the first local/test-only PostgreSQL write/read adapter for Simulation Desk paper-order persistence payloads. It builds on Task 008J persistence-intent payloads and validates that a record can be inserted into the local/test PostgreSQL schema and read back without introducing production Supabase, hosted credentials, vendor/API calls, live market data, broker execution, real-money trading, autonomous execution, or secrets.

## Scope

- Add `backend/app/simulation_postgres_persistence.py` as a local/test-only PostgreSQL adapter.
- Use Task 008J paper-order persistence-intent payloads as the adapter input shape.
- Validate both approved Simulation Desk origins: `user_recorded` and `system_generated_learning`.
- Preserve origin fields, actor/source metadata, JSON boundary flags, historical recommendation metadata, outcome preview metadata, and learning/loss guardrails through a database write/read roundtrip.
- Use only `HK_ALPHA_TEST_POSTGRES_DSN` for destructive PostgreSQL roundtrip resets; `DATABASE_URL` is intentionally ignored by the test fixture.

## Boundary

Task 008K does not add production Supabase connection logic, a Supabase client runtime, Supabase hosted credentials, vendor SDKs, vendor/API calls, live market data, broker integration, broker execution APIs, real-money trading, autonomous real-money execution, real-money account connectivity, billing/payment runtime, membership runtime, authentication runtime, deployment configuration, frontend/UI, or secrets.

## Schema Note

Task 008K adds an additive local/test migration draft for `paper_orders.historical_recommendation_fields_json` so Task 008J's historical recommendation payload can be written and read back as first-class JSON metadata in local/test PostgreSQL. This is not a production Supabase application and does not rename canonical tables, locked endpoints, response envelope fields, preferred strategy labels, MVP phase names, or Investment Strategy Office required fields.

## Validation Expectations

- `python scripts/validate_contracts.py`
- `PYTHONPATH=backend pytest backend/tests/test_simulation_postgres_persistence.py -q`
- `PYTHONPATH=backend pytest backend/tests/test_simulation_persistence_boundary.py -q`
- `PYTHONPATH=backend pytest backend/tests/test_simulation_runtime.py -q`
- `PYTHONPATH=backend pytest backend/tests -q`
- `scripts/check_migration_sql.sh` with local/test PostgreSQL available
- `git diff --check`

If `HK_ALPHA_TEST_POSTGRES_DSN` is missing, the adapter roundtrip tests are skipped locally before any destructive reset is attempted. `DATABASE_URL` alone is ignored and cannot authorize destructive reset. When `HK_ALPHA_TEST_POSTGRES_DSN` is present, the database name must be `hk_alpha_validation`, `hk_alpha_test`, or start with `hk_alpha_validation_` / `hk_alpha_test_`; unsafe names are skipped before import, connection, drop, or create operations. With an approved test-only DSN, missing `psycopg` or an unreachable PostgreSQL service fails the tests so CI cannot silently skip the roundtrip evidence.
