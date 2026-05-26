# 16 — Local SQL Validation (PR #5)

## Purpose

Define a repeatable local/test validation procedure for the Phase 2 draft migration before Backend Skeleton work begins.

## Date

2026-05-26

## Scope

Implementation-limited validation only:

- run the draft migration against a local/test PostgreSQL instance
- verify migration applies cleanly
- verify core schema presence and key constraints

Out of scope:

- production Supabase execution
- production secrets
- Railway deployment
- backend/frontend runtime implementation

## Validation Script

- `scripts/check_migration_sql.sh` resets an isolated local database (`hk_alpha_validation` by default), applies `supabase/migrations/0001_create_core_schema.sql`, and validates:
  - migration execution succeeds
  - exactly 18 public tables exist
  - critical constraints remain present (`confidence_level` and `agent_runs.status` checks)

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

## Governance Decision: Branch Protection Warning

GitHub currently warns that protected branch rules for this private repository are not enforceable under current plan/org settings.

Decision for Phase 2:

- Defer repository plan/organization upgrade in this PR.
- Continue manual governance enforcement through:
  - required PR review checklist usage
  - contract validation CI workflows
  - mergeability verification before declaring PR complete

Revisit upgrade decision in a dedicated governance/infrastructure PR after Phase 2 readiness stabilization.

## Phase 2 Readiness Outcome

With migration execution validation and CI coverage added, Phase 2 readiness for transition planning to Backend Skeleton is improved while preserving current advisory-only, non-production boundaries.
