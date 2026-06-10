# 42 — Task 008N M5 Closeout and Production Supabase Readiness Gate

## Date

2026-06-10

## Purpose

Task 008N is a documentation-only, governance-sensitive source-of-truth audit after Tasks 008K, 008L, and 008M. It answers whether Task 008 / Milestone M5 can close, records the smallest remaining gap if it cannot, and defines the gate conditions for any future Production Supabase Readiness Package.

Task 008N does **not** implement production Supabase, does **not** add a Supabase client runtime, does **not** add hosted credentials or secrets, does **not** apply production migrations, and does **not** change backend runtime behavior.

## Required Source-of-Truth Review Map

Task 008N reviewed the current repository source of truth across:

- project governance and workflow: `AGENTS.md`, `README.md`, `docs/06-codex-workflow.md`, `docs/13-pr-review-checklist.md`, `docs/20-codex-pr-factory.md`, `docs/32-pr-review-evidence-closure-protocol.md`, and `docs/36-commercial-readiness-and-subscription-product-governance.md`;
- canonical contracts and phase status: `docs/08-supabase-schema-design.md`, `docs/09-api-and-agent-contracts.md`, `docs/10-mvp-implementation-plan.md`, and `docs/11-project-status.md`;
- local SQL validation and Task 008 persistence evidence: `docs/16-local-sql-validation.md`, `docs/38-task-008j-simulation-desk-persistence-schema-alignment-local-migration-draft-and-adapter-boundary.md`, `docs/39-task-008k-local-test-postgresql-persistence-adapter.md`, `docs/40-task-008l-local-test-endpoint-persistence-wiring.md`, and `docs/41-task-008m-local-test-persisted-read-model.md`;
- source/runtime/test evidence: `backend/app/main.py`, `backend/app/simulation_runtime.py`, `backend/app/simulation_postgres_persistence.py`, `backend/tests/test_simulation_endpoint_persistence.py`, `backend/tests/test_simulation_postgres_persistence.py`, and `backend/tests/test_simulation_portfolio_persistence.py`;
- CI and SQL evidence: `.github/workflows/backend-check.yml`, `.github/workflows/sql-migration-check.yml`, `.github/workflows/contract-check.yml`, `supabase/migrations/0001_create_core_schema.sql`, `supabase/migrations/0002_align_simulation_desk_persistence_fields.sql`, and `supabase/migrations/0003_add_paper_order_historical_recommendation_fields_json.sql`;
- current logs: `docs/progress-log.md` and `docs/decision-log.md`.

## Current Official Supabase Reference Review

Task 008N used current official Supabase documentation, re-checked on 2026-06-10, only for production-readiness gate framing:

| Gate Area | Official Source | Task 008N Interpretation |
| --- | --- | --- |
| Database migrations | Supabase Database Migrations documentation: <https://supabase.com/docs/guides/deployment/database-migrations> | Remote schema changes must be represented as migration files and applied in controlled order; direct remote dashboard/SQL-editor edits are not an acceptable production workflow once migrations are used. |
| Shared responsibility | Supabase Shared Responsibility Model: <https://supabase.com/docs/guides/platform/shared-responsibility-model/> | HK Alpha Team remains responsible for account access, data, schema/user management, security controls, application architecture, secret/API-key handling, and third-party-service choices. |
| Row Level Security | Supabase Row Level Security documentation: <https://supabase.com/docs/guides/database/postgres/row-level-security> | Any future user-facing production data path must complete RLS/security review before exposure; exposed schemas require RLS/policy planning. |
| Secrets and environment variables | Supabase Environment Variables / Secrets documentation: <https://supabase.com/docs/guides/functions/secrets> | Secrets must be held only in approved encrypted environment/secret stores and never committed; service/secret keys must not be browser-exposed. |

These references are used only to define future gates. They do not approve or implement production Supabase in Task 008N.

## Current Main Evidence Summary

- Task 008 / M5 entered this review as **In Progress**.
- Task 008K added local/test PostgreSQL paper-order write/read adapter evidence for both approved Simulation Desk origins.
- Task 008L wired local/test paper-order endpoint persistence behind explicit `local_test_postgres` injection gates.
- Task 008M added local/test persisted paper-portfolio readback by stable portfolio UUID after local/test endpoint writes.
- Default runtime remains process-local in-memory.
- Local/test persistence requires explicit `HK_ALPHA_SIMULATION_PERSISTENCE_MODE=local_test_postgres` and a safe `HK_ALPHA_TEST_POSTGRES_DSN`.
- `DATABASE_URL` alone does not authorize Simulation Desk endpoint persistence.
- Production Supabase connection remains **No**.
- Supabase client runtime remains **No**.
- Production runtime persistence remains **No**.
- Production migration application remains **No**.
- Vendor/API integration remains **No**.
- Broker integration remains **No**.
- Real-money trading automation remains **No**.
- Secrets committed remains **No**.

## M5 Closeout Checklist

| M5 / Task 008 Closeout Area | Evidence Status | Source-of-Truth Evidence |
| --- | --- | --- |
| Locked MVP Simulation Desk endpoints exist | Satisfied | `POST /api/v1/simulation/paper-orders` and `GET /api/v1/paper-portfolios/{portfolio_id}` remain locked in `docs/09-api-and-agent-contracts.md` and implemented in `backend/app/main.py`. |
| Approved simulation origins preserved | Satisfied | `user_recorded` and `system_generated_learning` are defined in `docs/09-api-and-agent-contracts.md`, mapped in schema docs, and covered by endpoint/persistence tests. |
| Advisory-only / paper-only warnings and metadata | Satisfied | Runtime warnings and metadata disclose paper-only, advisory-only, human-in-the-loop, no broker, no real-money, no production Supabase, and no secrets boundaries. |
| Loss visibility | Satisfied | Contract docs require losing outcomes remain visible; Task 008L/008M tests cover losing outcome readback in local/test mode. |
| Learning proposal non-auto-apply | Satisfied | Contract docs and migration draft preserve reviewability and `auto_apply = false`; endpoint/persistence tests cover non-auto-applied learning proposal previews/readback. |
| Historical recommendation metadata preservation | Satisfied | `0003_add_paper_order_historical_recommendation_fields_json.sql` and Task 008K/008L/008M tests preserve historical recommendation metadata in local/test write/read/read-model evidence. |
| Default in-memory mode | Satisfied | Runtime defaults to memory mode unless explicit local/test env gates are present. |
| Explicit local/test persistence mode | Satisfied | `local_test_postgres` mode requires safe test DSN and returns local/test disclosures; unsafe/missing configuration fails safely. |
| Local/test SQL migration validation | Satisfied by CI/local-test path | `docs/16-local-sql-validation.md`, `scripts/check_migration_sql.sh`, and `sql-migration-check.yml` apply the local/test migration set in lexical order. |
| CI coverage | Satisfied by configured checks | `contract-check`, `backend-check`, and `sql-migration-check` exist; Task 008N PR must rely on GitHub Actions evidence plus local command evidence where available. |
| Contract-lock compliance | Satisfied | No canonical schema table names, MVP endpoint names, response envelope fields, preferred strategy labels, MVP phase names, or Investment Strategy Office required fields are renamed by Task 008N. |
| Docs/status/log alignment | Satisfied by this PR | This document, `docs/11-project-status.md`, `docs/progress-log.md`, and `docs/decision-log.md` align Task 008N decisions. |
| Production Supabase implementation | Intentionally not satisfied / out of scope | Production Supabase is not required to close M5 and remains blocked behind the future gate below. |

## Evidence Table

| Goal / Requirement | Current Evidence | Residual Limitation |
| --- | --- | --- |
| Create paper-order simulation endpoint behavior | `backend/app/main.py` calls `create_paper_order_response_data` for `POST /api/v1/simulation/paper-orders`; endpoint tests cover memory and local/test persistence modes. | No production persistence; this is intentional. |
| Return paper-portfolio simulation state | `backend/app/main.py` calls `build_paper_portfolio_snapshot` for `GET /api/v1/paper-portfolios/{portfolio_id}`; Task 008M tests cover persisted readback in local/test mode. | Read model is local/test or in-memory, not production. |
| Preserve approved origins | Runtime and persistence payloads preserve `user_recorded` and `system_generated_learning`. | Future production schema policies must preserve this after production approval. |
| Preserve advisory/no-real-money boundary | Runtime warnings, docs, and tests preserve paper-only and no-real-money metadata. | Future commercial/product runtime must continue to prove this boundary. |
| Preserve loss and learning guardrails | Tests cover losing outcomes, human review flags, non-auto-apply learning proposals, and historical metadata. | Future production persistence must prove the same guardrails through production-ready tests and RLS/security review. |
| Validate SQL drafts locally | `0001`, `0002`, and `0003` are local/test migration drafts validated by `scripts/check_migration_sql.sh` in local/test PostgreSQL/CI. | No production migration has been applied or approved. |
| Keep hard prohibitions intact | Docs/status/tests show no broker, no live vendor/API, no secrets, no real-money execution. | Any future scope change would require separate governance; Task 008N does not propose one. |

## M5 Closeout Decision

**Decision: Task 008 / Milestone M5 is ready to close as a non-production, advisory-only Simulation Desk MVP after this Task 008N documentation/governance PR merges.**

Rationale:

1. The locked Simulation Desk endpoints are implemented and covered by tests.
2. The MVP distinguishes the approved `user_recorded` and `system_generated_learning` simulation origins.
3. The endpoint behavior preserves advisory-only, paper-only, human-in-the-loop, no-real-money, no-broker, no-production-Supabase, and no-secrets disclosures.
4. Local/test PostgreSQL evidence now covers paper-order write/read, endpoint persistence wiring, and paper-portfolio persisted readback after Tasks 008K, 008L, and 008M.
5. Default runtime remains in-memory, so local/test persistence evidence does not silently become production persistence.
6. Production Supabase was never required for M5 closeout and remains explicitly blocked.

Smallest remaining local/test-only gap if a reviewer declines closeout: none identified within the approved M5 scope. Remaining limitations are production-readiness limitations, not local/test M5 blockers.

## Residual Limitations After M5 Closeout

M5 closeout does not mean production readiness. The project still has:

- no production Supabase connection;
- no Supabase client runtime;
- no hosted credentials or repository/environment secrets;
- no production migration application;
- no production runtime persistence;
- no user-facing auth/account runtime;
- no billing/payment runtime;
- no deployment/runtime infrastructure;
- no live market data or vendor/API integration;
- no broker integration;
- no real-money trading or autonomous execution.

## Production Supabase Readiness Gate Decision

**Decision: the project may begin a future Production Supabase Readiness Package, tentatively Task 008O or later, but production Supabase remains blocked until explicit Harness Engineering approval and successful gate evidence.**

A future PR may plan production readiness only if it remains scoped and explicitly states which gates it is asking to open. No future PR may touch production Supabase, hosted credentials, production migration application, Supabase client runtime, production runtime persistence, or production user-facing data paths unless Harness Engineering has explicitly approved that scope before implementation.

### Mandatory Future Gates

Before any future PR touches the named production capabilities, it must satisfy all applicable gates below:

1. **Explicit Harness approval before production Supabase connection.**
   - No production database URL, project ref, hosted connection, or production access path may be introduced without approval.
2. **Explicit Harness approval before hosted credentials or repository/environment secrets.**
   - Secrets must be stored only in an approved encrypted secret/environment store and never committed.
3. **Explicit Harness approval before production migration application.**
   - Local/test migration drafts are not production application approval.
4. **Explicit Harness approval before Supabase client runtime.**
   - Adding `supabase-js`, Python Supabase clients, direct production Postgres clients, or equivalent runtime wiring requires a scoped PR and security review.
5. **Migration-file-only remote schema changes.**
   - Remote schema changes must go through committed migration files, not direct production dashboard or SQL-editor changes.
6. **Production migration plan.**
   - The plan must include migration apply order, rollback/repair considerations, ownership of who runs it, preflight checks, and post-deploy verification.
7. **RLS/security review before user-facing production data paths.**
   - Any exposed/user-facing production data path must include RLS, policy, role, key, and least-privilege review.
8. **Secrets handling review.**
   - Secret names, storage locations, access scope, rotation/repair expectations, and non-commit evidence must be documented.
9. **Production runtime persistence review.**
   - Production persistence must be separately reviewed with CI evidence, contract checks, security/secrets handling, Evidence Closure, and post-merge verification.
10. **No broker/real-money expansion.**
    - Broker/real-money actions remain hard prohibited unless a separate future governance framework explicitly changes product scope. Task 008N does not propose enabling them.

## Hard-Prohibition Audit

| Prohibition | Task 008N Result |
| --- | --- |
| Real-money trading | Not introduced; remains prohibited. |
| Autonomous real-money execution | Not introduced; remains prohibited. |
| Autonomous broker execution | Not introduced; remains prohibited. |
| Real-money account connectivity | Not introduced; remains prohibited. |
| Secrets leakage | Not introduced; no secrets added. |
| Hidden or irreversible investment actions | Not introduced; simulation outputs remain advisory and reviewable. |


## Backend-Check CI Hardening Note

Task 008N includes a minimal `backend-check` workflow hardening after GitHub Actions failed before checkout/tests while pulling the `postgres:16` service image for this documentation/status PR. The hardened workflow keeps full PostgreSQL-backed backend tests for runtime, persistence, migration, and non-doc/status changes, but avoids starting PostgreSQL for PRs whose changed files are limited to documentation, `README.md`, `backend/tests/test_api.py`, or the `backend-check` workflow itself.

This is safe for Task 008N because the PR changes status documentation and the project-status test expectations only; it does not change backend runtime behavior, persistence behavior, migrations, production Supabase, secrets, vendors, brokers, or real-money capabilities. For runtime/persistence changes, `backend-check` still starts PostgreSQL and runs the full `PYTHONPATH=backend pytest backend/tests` suite with `HK_ALPHA_TEST_POSTGRES_DSN`.

## Manual Setup / Android-Only Validation Note

Harness Engineering is Android-only and is not expected to run local manual validation for Task 008N. PR evidence and GitHub checks must carry validation. The PR body must include exact local command results where available, CI-equivalent evidence for local/test PostgreSQL, and explicit notes for any environment limitation.

## Follow-Up Recommendation

After Task 008N merges and M5 is closed, the next safe work is a separate, scoped Production Supabase Readiness Package that is documentation/governance-first and may include only planning artifacts unless Harness Engineering explicitly approves implementation. That package should start by defining the production environment inventory, secret ownership, migration-application runbook, RLS/security matrix, CI evidence requirements, and post-deploy verification checklist.

Task 008N does not authorize implementation of those production capabilities.
