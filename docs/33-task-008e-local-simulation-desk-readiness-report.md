# 33 — Task 008E Local Simulation Desk Readiness Report

## Purpose

Task 008E adds the next smallest safe Simulation Desk MVP slice: a deterministic local-only readiness report that aggregates existing Task 008B fixture validation evidence and Task 008C local paper-order intent validation evidence.

The report exists to prove Milestone M5 boundary compliance before any future runtime, persistence, migration, Supabase, endpoint, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit-event creation, broker, or real-money gate is considered.

## Source-of-Truth Reviewed

Task 008E was prepared against these source-of-truth artifacts:

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
- `docs/decision-log.md`
- `docs/progress-log.md`
- `docs/lessons-learned.md`
- `backend/app/simulation_contract.py`
- `backend/app/simulation_order_validation.py`
- `backend/tests/test_simulation_contract.py`
- `backend/tests/test_simulation_order_validation.py`

## Current Project Position

Task 008 / Milestone M5 remains **In Progress**. Task 008A established Simulation Desk boundaries, Task 008B added local-only contract fixtures and validation, Task 008C added local-only paper-order intent validation, and Task 008D documented persistence gate readiness and migration alignment.

Task 008E does not close M5. It adds an implementation-limited readiness aggregator so future review can inspect a single local-only report before deciding whether any separate Task 008F approval gate should be opened.

## Task 008E Classification

- Classification: **implementation-limited local-only**
- Runtime approval: **Not granted**
- Persistence approval: **Not granted**
- Migration approval: **Not granted**
- Production Supabase approval: **Not granted**
- Endpoint implementation approval: **Not granted**
- Broker / real-money approval: **Not granted**

## Explicit Task 008E Local-Only Decision

Task 008E is approved only to generate and validate a deterministic in-memory readiness report. The report may reference canonical schema table names and locked endpoint names for traceability, but those references must not become runtime, persistence, endpoint handler, SQL migration, Supabase client, broker, or real-money behavior.

## Scope

Task 008E may:

1. Build a deterministic local readiness report with `task_id = "008E"`.
2. Aggregate Task 008B fixture validation evidence from the local Simulation Desk contract fixture helpers.
3. Aggregate Task 008C local paper-order intent validation evidence from the local validation helpers.
4. Preserve canonical schema table references without renaming.
5. Reference locked MVP endpoint names without implementing endpoints.
6. Record approval gates as not crossed, including a local `approval_gate_status` map whose values must remain false.
7. Prove boundary flags remain false for IO, HTTP, database writes, persistence, production Supabase, Supabase client use, endpoint runtime, paper-order creation, broker execution, broker API calls, external APIs, secrets, real-money order placement, and real-money trading automation.
8. Keep `would_create_order = false`.
9. Preserve advisory-only, simulation-only, and human-in-the-loop framing.

## Out of Scope

Task 008E must not add or authorize:

- SQL migrations or changes under `supabase/migrations`
- Supabase client setup
- Production Supabase connections
- Database reads, writes, inserts, updates, deletes, upserts, repositories, or persistence adapters
- FastAPI routes or endpoint runtime
- `POST /api/v1/simulation/paper-orders`
- `GET /api/v1/paper-portfolios/{portfolio_id}`
- `POST /api/v1/strategy-recommendations`
- `GET /api/v1/strategy-recommendations/{recommendation_id}`
- Paper-order creation, submission, fill, or mutation
- Paper-portfolio valuation, retrieval, position lifecycle, or snapshot runtime behavior
- Strategy recommendation persistence
- Database audit-event creation
- Live market data
- External API calls
- Broker API connections
- Autonomous order placement
- Secrets, API keys, Supabase service role keys, Railway tokens, broker credentials, or real-money account information
- Production deployment
- Frontend, UI, or report-output runtime

## Relationship to Task 008B, Task 008C, and Task 008D

- **Task 008B:** Supplies deterministic Simulation Desk fixture coverage for paper portfolios, paper-order intents, paper positions, portfolio snapshots, trade reviews, learning proposals, and audit events. Task 008E consumes this local evidence and surfaces it in a readiness artifact.
- **Task 008C:** Supplies deterministic local paper-order intent validation and proves that no paper order is created. Task 008E consumes this validation evidence and keeps `would_create_order = false`.
- **Task 008D:** Documents persistence gate readiness and migration alignment without authorizing any persistence or migration work. Task 008E reinforces those gates by reporting them as not crossed.

## Validation Behavior

Task 008E validation rejects readiness reports that imply any forbidden behavior, including endpoint runtime, persistence, Supabase usage, production connection, paper-order creation, broker execution, external API usage, secrets, real-money order placement, or real-money trading automation.

Validation also checks that:

- Task 008B source evidence passed.
- Task 008C source evidence passed.
- Canonical schema table names are unchanged.
- Locked endpoint names are referenced only for traceability.
- All required boundary flags are present and false.
- Source Task 008B boundary-compliance checks remain true.
- Source Task 008C boundary flags remain false.
- Source Task 008C `record_type` remains `paper_order_intent`.
- Source Task 008C `validated_order` contains the local paper-order fields and passes `validate_local_paper_order_intent` revalidation with the local portfolio registry.
- Approval gate status values remain false.
- `would_create_order` remains false.
- Readiness report validation does not mutate inputs.

## Tests / Validation Evidence Requirements

Required local validation commands for this task are:

```bash
python scripts/validate_contracts.py
PYTHONPATH=backend pytest backend/tests -q
git diff --check
```

Task-specific tests must cover the default readiness report, Task 008B evidence, Task 008C evidence, embedded Task 008C `record_type` and `validated_order` revalidation failures, canonical schema preservation, locked endpoint references, forbidden boundary flag rejection, invalid local paper-order input, non-mutating behavior, and no runtime/persistence/external/broker/real-money behavior.

## Risk Areas

- Accidentally treating endpoint strings as implemented routes.
- Accidentally treating canonical schema references as migration approval.
- Accidentally creating paper-order runtime behavior instead of local validation evidence.
- Accidentally implying Supabase, database, external API, broker, secret, or real-money behavior.
- Failing to keep Task 008D persistence gates closed until a separate explicit approval task.

## Next Gate / Task 008F Entry Criteria

Task 008F may be considered only after Harness Engineering reviews Task 008E evidence and explicitly approves a next scope. Any future step that crosses a migration, persistence, Supabase, endpoint runtime, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit-event creation, broker, live-data, deployment, or real-money gate must be a separate reviewed PR with same-PR docs, tests, status, and log updates.

Codex must not self-approve any such gate.
