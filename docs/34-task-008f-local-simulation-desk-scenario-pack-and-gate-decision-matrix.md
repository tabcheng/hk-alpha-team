# 34 — Task 008F Local Simulation Desk Scenario Pack and Gate Decision Matrix

## Purpose

Task 008F adds a deterministic, in-memory Simulation Desk scenario pack that aggregates existing Task 008B, Task 008C, and Task 008E evidence for broader local end-to-end inspection.

The scenario pack helps Harness Engineering decide whether any future Task 008G should explicitly open a migration, persistence, Supabase, endpoint runtime, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit-event creation, broker, live-data, deployment, autonomous order placement, or real-money gate.

Task 008F does **not** open or approve any of those gates.

## Source-of-Truth Reviewed

Task 008F was prepared against the current repository source-of-truth set:

- `AGENTS.md`
- `README.md`
- `docs/04-simulation-investment-desk.md`
- `docs/06-codex-workflow.md`
- `docs/08-supabase-schema-design.md`
- `docs/09-api-and-agent-contracts.md`
- `docs/10-mvp-implementation-plan.md`
- `docs/11-project-status.md`
- `docs/20-codex-pr-factory.md`
- `docs/28-task-008a-simulation-desk-boundary-and-contract-planning.md`
- `docs/29-task-008b-local-simulation-contract-fixtures.md`
- `docs/30-task-008c-local-paper-order-validation-service.md`
- `docs/31-task-008d-persistence-gate-readiness-and-migration-alignment.md`
- `docs/32-pr-review-evidence-closure-protocol.md`
- `docs/33-task-008e-local-simulation-desk-readiness-report.md`
- `docs/decision-log.md`
- `docs/progress-log.md`
- `docs/lessons-learned.md`
- `backend/app/simulation_contract.py`
- `backend/app/simulation_order_validation.py`
- `backend/app/simulation_desk_readiness.py`
- Existing Task 008B, 008C, and 008E tests.

## Current Project Position

- Current phase: **Phase 5 — Simulation Desk MVP**.
- Task 008 / Milestone M5 status: **In Progress**.
- Task 008E has landed as implementation-limited local-only readiness evidence.
- Task 008F adds local-only scenario-pack and gate-decision evidence.
- Task 008F explicitly does **not** close M5.

## Task 008F Classification

Task 008F is:

- Implementation-limited.
- Governance-sensitive.
- Pure local-only.
- Deterministic.
- In-memory.
- Non-persistent.
- Advisory-only.
- Simulation-only.
- Human-in-the-loop.

## Explicit Local-Only Decision

Task 008F may build and validate a local scenario pack only. It may reference canonical schema table names and locked endpoint names for traceability, but those strings must not become runtime behavior.

Task 008F does not authorize:

- SQL migrations.
- Changes under `supabase/migrations`.
- Supabase client setup.
- Production Supabase connections.
- Database reads, writes, inserts, updates, deletes, upserts, repositories, or persistence adapters.
- FastAPI routes or endpoint runtime.
- Paper-order creation, submission, fill, mutation, or persistence.
- Paper-portfolio valuation, retrieval, position lifecycle, or snapshot runtime behavior.
- Strategy recommendation persistence.
- Database audit-event creation.
- Broker API connections.
- Live market data.
- External API calls.
- Secrets or environment variable requirements.
- Frontend, UI, report-output runtime, or deployment.
- Autonomous order placement or real-money trading.

## User Story

As Harness Engineering, I want a deterministic local-only Simulation Desk end-to-end scenario pack and gate decision matrix, so that I can inspect a broader set of valid, invalid, readiness, loss-visibility, learning-reviewability, and boundary-control evidence before deciding whether any future Task 008G should explicitly open a migration, persistence, Supabase, endpoint runtime, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit-event creation, broker, live-data, deployment, or real-money gate.

## Acceptance Criteria

Task 008F is complete when:

1. The scenario pack aggregates Task 008B, Task 008C, and Task 008E evidence.
2. The pack includes valid and invalid paper-order intent scenarios.
3. Invalid scenarios fail safely and do not create paper orders.
4. Task 008E readiness aggregation validates successfully.
5. Canonical schema table names are preserved.
6. Locked endpoint names are referenced only for traceability and are not implemented.
7. Approval gates remain false.
8. Forbidden boundary flags remain false.
9. Losing simulation outcomes remain visible.
10. Learning proposals remain reviewable and are not auto-applied.
11. Validation does not mutate inputs.
12. Task 008 / M5 remains In Progress.
13. Task 008F does not authorize runtime, persistence, migration, Supabase, endpoint, broker, live-data, deployment, autonomous order placement, or real-money behavior.
14. `docs/11-project-status.md`, `docs/progress-log.md`, and `docs/decision-log.md` are updated in the same PR.
15. `docs/09-api-and-agent-contracts.md` and `docs/08-supabase-schema-design.md` remain unchanged.

## Scope

In scope:

- `backend/app/simulation_desk_scenarios.py`
- `backend/tests/test_simulation_desk_scenarios.py`
- This Task 008F documentation page.
- Status, progress-log, and decision-log updates.

The local helper may consume:

- `build_simulation_contract_fixtures`
- `build_simulation_validation_matrix`
- `validate_simulation_fixture_collection`
- `validate_local_paper_order_intent`
- `build_local_paper_order_validation_report`
- `build_simulation_desk_readiness_report`
- `validate_simulation_desk_readiness_report`

## Out of Scope

Task 008F does not add or authorize:

- SQL migrations or migration edits.
- Supabase clients or production Supabase connectivity.
- Database persistence or repositories.
- FastAPI routes or endpoint handlers.
- Runtime implementations for locked MVP endpoint names.
- Paper-order creation or paper-portfolio runtime behavior.
- Strategy recommendation persistence.
- Audit-event database creation.
- Live market data or external API calls.
- Broker execution or broker API calls.
- Secrets, deployment, frontend/UI, autonomous order placement, or real-money trading.
- Public API contract changes.
- `docs/09-api-and-agent-contracts.md` changes.
- `docs/08-supabase-schema-design.md` changes.

## Relationship to Tasks 008B, 008C, 008D, and 008E

| Task | Relationship to 008F |
|---|---|
| 008B | Supplies deterministic Simulation Desk fixture records, canonical schema table references, locked endpoint traceability, loss visibility, learning reviewability, and local boundary evidence. |
| 008C | Supplies local paper-order intent validation behavior for valid and invalid order-like inputs without creating orders. |
| 008D | Supplies persistence-gate and migration-alignment planning context; 008F does not cross those gates. |
| 008E | Supplies readiness aggregation helpers that 008F validates as one scenario in the pack. |

## Scenario Matrix

| Scenario | Expected Behavior | Boundary Result |
|---|---|---|
| Valid HK paper-order intent | Passes local validation for `0700.HK`-style input. | `would_create_order = false`. |
| Malformed HK symbol | `700.HK` fails safely because conservative HK symbol format requires four digits. | No mutation, no order creation. |
| Invalid side | Non-`buy` / non-`sell` side fails safely. | No mutation, no order creation. |
| Invalid quantity | Negative quantity fails safely. | No mutation, no order creation. |
| Invalid order type | Non-`market` / non-`limit` order type fails safely. | No mutation, no order creation. |
| Invalid limit price | Negative limit price fails safely. | No mutation, no order creation. |
| Missing portfolio id | Missing `portfolio_id` fails safely. | No mutation, no order creation. |
| Task 008E readiness aggregation | Existing readiness helper validates successfully. | All Task 008E boundary flags and approval gates remain false. |
| Loss visibility | Losing fixture records remain visible. | Losing records are not hidden or overwritten. |
| Learning reviewability | Learning proposal remains reviewable. | Proposal is not auto-applied. |
| Gate decision matrix | Possible future Task 008G directions are listed. | No gate is approved by Task 008F. |

## Validation Behavior

`validate_simulation_desk_scenario_pack(pack)` rejects a pack that:

- Claims endpoint runtime or endpoint handlers are enabled.
- Claims persistence, database writes, Supabase client setup, or production Supabase connectivity.
- Claims paper orders are created.
- Claims paper-portfolio runtime exists.
- Claims strategy recommendations are persisted.
- Claims audit events are created in a database.
- Claims broker execution, broker API calls, live market data, external API calls, secrets, deployment, autonomous order placement, real-money order placement, or real-money trading automation.
- Crosses any approval gate.
- Hides losing simulations.
- Auto-applies learning proposals.
- Changes canonical schema table names.
- Changes locked endpoint names.
- Mutates inputs during validation.
- Provides stale scenario evidence whose stored pass/fail status no longer matches local paper-order intent revalidation.
- Omits, reorders, duplicates, or changes locked endpoint names or next-gate directions.
- Implies Task 008F closes M5.

## Tests / Validation Evidence Requirements

Required local validation commands:

- `python scripts/validate_contracts.py`
- `PYTHONPATH=backend pytest backend/tests/test_simulation_desk_scenarios.py -q`
- `PYTHONPATH=backend pytest backend/tests -q`
- `git diff --check`

Expected evidence:

- Valid pack build and validation pass.
- Task 008B, 008C, and 008E source evidence included.
- Stored scenario evidence is revalidated rather than trusted blindly.
- Valid order scenario passes.
- Invalid order scenarios fail safely.
- Readiness aggregation scenario passes.
- Canonical schema table names and locked endpoint names are preserved.
- Approval gates and forbidden boundary flags remain false.
- Loss visibility and learning reviewability evidence remains visible.
- Validation does not mutate inputs.
- No runtime, persistence, Supabase, endpoint, external API, broker, secrets, deployment, paper-order creation, paper-portfolio runtime, strategy persistence, audit-event runtime, live-data, autonomous order placement, or real-money behavior is introduced.

## Risk Areas

- Treating endpoint strings as implementation instead of traceability references.
- Treating local validation reports as permission to create orders.
- Accidentally crossing persistence or Supabase gates while expanding evidence.
- Hiding losing simulations to make output look better.
- Auto-applying learning proposals instead of keeping them reviewable.
- Reinterpreting Task 008F as M5 closeout.

## Task 008G Entry Criteria

A future Task 008G may be considered only if Harness Engineering explicitly approves its gate in a separate task/PR scope.

Potential Task 008G directions include:

- Migration design or SQL migration work.
- Persistence adapter or repository design.
- Supabase client setup.
- Endpoint runtime implementation.
- Paper-order creation or paper-portfolio runtime design.
- Strategy recommendation persistence.
- Audit-event database creation.
- Live market data or external API integration.
- Broker integration.
- Deployment.
- Real-money trading capability.

None of these are approved by Task 008F.
