# 16 — Local SQL Validation

## Purpose

Define a repeatable local/test validation procedure for HK Alpha Team SQL migration drafts before they are trusted as merge-ready schema artifacts.

This runbook began with PR #5, which introduced local/test SQL validation for the Phase 2 baseline migration. Task 008J expands the same validator so it now applies every migration file under `supabase/migrations/` in lexical order and validates the baseline schema plus the Simulation Desk persistence-alignment draft together.

## Date

2026-06-06

## Scope

Implementation-limited validation only:

- run draft migrations against an isolated local/test PostgreSQL instance;
- reset only an explicitly test-named local validation database before applying migrations;
- discover SQL migration files under `supabase/migrations/`;
- apply all discovered migration files in lexical order, including `0001_create_core_schema.sql`, `0002_align_simulation_desk_persistence_fields.sql`, and `0003_add_paper_order_historical_recommendation_fields_json.sql`;
- verify migration execution succeeds;
- verify core schema presence, baseline constraints, Task 008J additive schema alignment checks, and the Task 008K historical recommendation metadata column.

Out of scope:

- production Supabase execution;
- production Supabase connection;
- Supabase client runtime;
- backend runtime persistence writes;
- disk persistence from backend runtime;
- production secrets;
- Railway deployment;
- vendor/API calls;
- broker integration or broker credentials;
- billing/payment/auth runtime;
- live market data;
- real-money trading;
- autonomous real-money execution.

## Historical Context

### PR #5 Baseline

PR #5 introduced `scripts/check_migration_sql.sh` for the baseline Phase 2 migration. At that point, the script applied only `supabase/migrations/0001_create_core_schema.sql` and checked the initial public table count plus the core Phase 2 constraints.

### Task 008J Expansion

Task 008J adds `supabase/migrations/0002_align_simulation_desk_persistence_fields.sql` as a **local/test-only additive migration draft** for Simulation Desk persistence alignment. The migration remains draft-only and must not be applied to production Supabase without later explicit Harness Engineering approval, separate PR scope, and Evidence Closure.

After Task 008K, `scripts/check_migration_sql.sh` validates `0001`, `0002`, and `0003` together by applying all migration files in lexical order.

## Validation Script Behavior

`scripts/check_migration_sql.sh` currently performs the following steps:

1. Reads PostgreSQL connection settings from environment variables, defaulting to a local/test validation database named `hk_alpha_validation`.
2. Rejects destructive reset unless `PGDATABASE` is `hk_alpha_validation`, `hk_alpha_test`, or starts with `hk_alpha_validation_` / `hk_alpha_test_`.
3. Verifies `psql` is available.
4. Confirms `supabase/migrations/` exists.
5. Discovers `*.sql` files in `supabase/migrations/` and sorts them lexically.
6. Verifies PostgreSQL connectivity against the `postgres` database.
7. Drops and recreates the isolated validation database.
8. Applies every discovered migration file in lexical order.
9. Validates exactly **18** public tables exist.
10. Validates required baseline and Task 008J constraints.
11. Validates Task 008J/008K additive columns.
12. Validates Task 008J UUID lineage column types.
13. Validates Task 008J lineage foreign-key constraints.
14. Validates Task 008J additive indexes.


The destructive reset guard accepts only these local/test database names:

- `hk_alpha_validation`
- `hk_alpha_test`
- names starting with `hk_alpha_validation_`
- names starting with `hk_alpha_test_`

Do not point this script at production, shared staging, hosted Supabase, or application databases.

## Current Constraint Checks

The script validates the presence of these critical constraints:

- `ck_strategy_recommendations_confidence_level_range`
- `ck_agent_runs_status`
- `ck_learning_proposals_auto_apply_false`
- `fk_paper_orders_source_recommendation_id`
- `fk_paper_orders_learning_proposal_id`
- `fk_learning_proposals_source_recommendation_id`

## Task 008J Additive Column Checks

The script validates the expected Task 008J/008K additive columns, including Simulation Desk origin, boundary, lineage, and metadata fields across:

- `paper_orders`
- `paper_positions`
- `portfolio_snapshots`
- `trade_reviews`
- `learning_proposals`
- `audit_events`

The lineage fields that imply canonical database IDs are expected to be UUID-compatible fields:

- `paper_orders.source_recommendation_id`
- `paper_orders.learning_proposal_id`
- `learning_proposals.source_recommendation_id`

Runtime fixture string lineage must remain in JSON metadata payloads and must not be treated as canonical UUID FK values.

## Task 008J Foreign-Key Checks

The script validates the Task 008J lineage foreign keys:

- `paper_orders.source_recommendation_id -> strategy_recommendations(id)`
- `paper_orders.learning_proposal_id -> learning_proposals(id)`
- `learning_proposals.source_recommendation_id -> strategy_recommendations(id)`

## Task 008J Index Checks

The script validates the Task 008J additive indexes:

- `idx_paper_orders_simulation_origin_created_at_desc`
- `idx_paper_orders_source_recommendation_created_at_desc`
- `idx_paper_positions_simulation_origin_status`
- `idx_trade_reviews_simulation_origin_reviewed_at_desc`
- `idx_learning_proposals_simulation_origin_status_created_at_desc`
- `idx_audit_events_simulation_origin_created_at_desc`

## Local Execution

Example (defaults expect local postgres credentials `postgres/postgres`):

```bash
./scripts/check_migration_sql.sh
```

Optional environment overrides:

```bash
PGHOST=127.0.0.1 PGPORT=5432 PGUSER=postgres PGPASSWORD=postgres PGDATABASE=hk_alpha_validation ./scripts/check_migration_sql.sh
```

## CI Automation

- `.github/workflows/sql-migration-check.yml` runs on pull requests and pushes to `main`.
- It starts `postgres:16`, installs `postgresql-client`, and executes `./scripts/check_migration_sql.sh`.
- CI therefore validates the ordered migration set and Task 008J schema-alignment checks in a local/test PostgreSQL service, not production Supabase.

## Governance Decision: Branch Protection Warning

GitHub previously warned that protected branch rules for this private repository were not enforceable under current plan/org settings.

Decision for the Phase 2 baseline remains:

- Defer repository plan/organization upgrade in that PR context.
- Continue manual governance enforcement through:
  - required PR review checklist usage;
  - contract validation CI workflows;
  - unresolved-thread checks before approval/merge;
  - mergeability verification before declaring PR complete.

Revisit upgrade decision in a dedicated governance/infrastructure PR after readiness stabilization.

## Governance Boundary

Local SQL validation does not approve production persistence. For Task 008J:

- `0002_align_simulation_desk_persistence_fields.sql` is local/test-only.
- Production Supabase application remains out of scope.
- Production Supabase application requires later explicit Harness Engineering approval and Evidence Closure.
- Supabase client runtime remains out of scope.
- Runtime persistence writes remain out of scope.
- Secrets, vendor/API calls, broker integration, deployment, billing/payment/auth runtime, real-money trading, and autonomous real-money execution remain out of scope.

## Current Readiness Outcome

With ordered migration execution and Task 008J/008K schema-alignment checks, local/test SQL validation now covers both the baseline schema and Simulation Desk persistence-alignment draft while preserving advisory-only, paper-only, non-production boundaries.
