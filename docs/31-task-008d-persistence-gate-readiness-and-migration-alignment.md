# 31 — Task 008D Persistence Gate Readiness and Migration Alignment

## Purpose

Task 008D creates a bounded persistence gate readiness and migration alignment plan for the Simulation Desk MVP.

It maps the reviewed Task 008B local-only Simulation Desk record fixtures and Task 008C local-only paper-order validation service/stub to the canonical schema and locked MVP endpoint names before any future migration, persistence write path, Supabase client, endpoint runtime, paper-order creation, or production infrastructure work begins.

## Source-of-Truth Reviewed

This plan is based on the current repository source-of-truth:

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
- `docs/decision-log.md`
- `docs/progress-log.md`
- `docs/lessons-learned.md`
- `backend/app/simulation_contract.py`
- `backend/app/simulation_order_validation.py`
- `backend/tests/test_simulation_contract.py`
- `backend/tests/test_simulation_order_validation.py`

## Current Project Position

- Task 007 / Milestone M4 is **Completed**.
- Task 008 / Milestone M5 is **In Progress**.
- Task 008A Simulation Desk boundary and contract planning is merged.
- Task 008B local Simulation Desk contract fixtures, validators, and validation matrix are merged.
- Task 008C local paper-order validation service/stub is merged.

## Task 008D Classification

Task 008D is:

- documentation-only;
- governance-sensitive;
- persistence / migration gate readiness only.

It is a planning and review artifact for Harness Engineering. It is not an implementation task.

## Explicit Task 008D Decision

Task 008D remains planning-only.

It does **not** authorize or introduce:

- reviewed public runtime surface;
- SQL migration;
- persistence writes;
- Supabase client;
- endpoint runtime;
- paper-order creation;
- paper-portfolio runtime;
- strategy recommendation persistence;
- audit event database creation;
- production Supabase connection;
- broker integration;
- real-money trading automation.

## Mapping Matrix: Task 008B / 008C Local Records to Canonical Tables

The gates named in this matrix refer to the approval gates listed below. RLS/auditability and proposal-review items are readiness requirements to resolve inside those named gates; they are not separate authorization paths.

| Local source | Local record shape | Canonical table from `docs/08` | Local fields already represented | Required future persistence relationships / notes | Gate before implementation |
|---|---|---|---|---|---|
| Task 008B | `paper_portfolio` | `paper_portfolios` | `portfolio_uuid`, `name`, `base_currency`, `starting_cash`, `status`, `created_at` | Optional `owner_profile_id` remains unresolved for v1 ownership/RLS planning. The record remains paper-only. RLS/auditability readiness must be reviewed before any future runtime. | SQL migration gate, Supabase client gate, persistence write gate, paper-portfolio runtime gate. |
| Task 008B / 008C | `paper_order_intent` | `paper_orders` | `portfolio_id`, `stock_id` or local `symbol`, `strategy_recommendation_id`, `side`, `order_type`, `quantity`, `limit_price`, `status`, `submitted_at`, `filled_at`, `created_at` | Requires `portfolio_id -> paper_portfolios.id`, `stock_id -> stocks.id`, and `strategy_recommendation_id -> strategy_recommendations.id` alignment. Task 008C validates intent only and returns `would_create_order = false`; any future persistence must define symbol-to-`stocks.id` resolution before writing. | SQL migration gate, Supabase client gate, persistence write gate, endpoint runtime gate, paper-order creation gate. |
| Task 008B | `paper_position` | `paper_positions` | `portfolio_id`, `stock_id`, `opened_from_order_id`, `side`, `quantity`, `avg_entry_price`, `avg_exit_price`, `status`, `opened_at`, `closed_at`, `created_at`, `outcome_label`, `losing_outcome_visible` | Requires `portfolio_id -> paper_portfolios.id`, `stock_id -> stocks.id`, and `opened_from_order_id -> paper_orders.id`. Losing outcomes must remain visible and must not be overwritten. | SQL migration gate, persistence write gate with retention / append-only readiness review, paper-portfolio runtime gate. |
| Task 008B | `portfolio_snapshot` | `portfolio_snapshots` | `portfolio_id`, `snapshot_time`, `nav`, `cash`, `gross_exposure`, `net_exposure`, `drawdown_pct`, `created_at` | Requires `portfolio_id -> paper_portfolios.id`. Future uniqueness policy must preserve the canonical unique `(portfolio_id, snapshot_time)` expectation without hiding historical drawdowns. | SQL migration gate, persistence write gate with retention / append-only readiness review, paper-portfolio runtime gate. |
| Task 008B | `trade_review` | `trade_reviews` | `paper_position_id`, `outcome_label`, `review_notes`, `mistake_tags_json`, `what_worked_json`, `what_failed_json`, `reviewed_at`, `created_at`, `losing_outcome_visible` | Requires `paper_position_id -> paper_positions.id`. Losing trades must remain visible in reports, and review notes must not rewrite historical recommendations or paper positions. | SQL migration gate, persistence write gate with retention / append-only readiness review, audit-event creation gate. |
| Task 008B | `learning_proposal` | `learning_proposals` | `source_type`, `source_id`, `title`, `proposal_text`, `expected_impact`, `risk_of_change`, `status`, `created_at`, `updated_at`, `reviewable`, `auto_applied` | Uses typed source metadata. Proposals must remain reviewable and must not silently alter production behavior. Future status transitions need review evidence before persistence. | SQL migration gate, persistence write gate, strategy recommendation persistence gate where coupled, audit-event creation gate. |
| Task 008B | `audit_event` | `audit_events` | `event_uuid`, `event_type`, `entity_type`, `entity_id`, `actor_type`, `actor_id`, `event_payload_json`, `created_at` | Uses polymorphic entity references via `entity_type` and `entity_id`. Future persisted events must be immutable and append-only. | SQL migration gate, persistence write gate with retention / append-only readiness review, audit-event creation gate. |

## Mapping Matrix: Locked `docs/09` Endpoint Names to Future Gates

| Locked endpoint name | Current Task 008D position | Canonical tables likely affected in a future implementation | Required gates before implementation |
|---|---|---|---|
| `POST /api/v1/simulation/paper-orders` | Referenced for planning only; not implemented. | `paper_orders`, `paper_portfolios`, `stocks`, `strategy_recommendations`, possible `audit_events`. | SQL migration gate; Supabase client gate; persistence write gate; endpoint runtime gate; paper-order creation gate; audit-event creation gate; no broker / real-money gate bypass. |
| `GET /api/v1/paper-portfolios/{portfolio_id}` | Referenced for planning only; not implemented. | `paper_portfolios`, `paper_orders`, `paper_positions`, `portfolio_snapshots`, `trade_reviews`. | SQL migration gate; Supabase client gate; persistence read/write design review before runtime; endpoint runtime gate; paper-portfolio runtime gate; RLS/auditability readiness review. |
| `POST /api/v1/strategy-recommendations` | Referenced for planning only; not implemented by Task 008D. | `strategy_recommendations`, possible `paper_orders`, possible `audit_events`. | SQL migration gate; Supabase client gate; persistence write gate; endpoint runtime gate; strategy recommendation persistence gate; audit-event creation gate. |
| `GET /api/v1/strategy-recommendations/{recommendation_id}` | Referenced for planning only; not implemented by Task 008D. | `strategy_recommendations`, possible related `paper_orders`, `trade_reviews`, `learning_proposals`. | SQL migration gate; Supabase client gate; persistence read design review before runtime; endpoint runtime gate; strategy recommendation persistence gate; RLS/auditability readiness review. |

## Persistence Readiness Checklist

Before any persistence implementation begins, the next task must verify:

- [x] Canonical schema names are preserved in planning: `paper_portfolios`, `paper_orders`, `paper_positions`, `portfolio_snapshots`, `trade_reviews`, `learning_proposals`, and `audit_events`.
- [x] Task 008B local fixture fields are mapped to canonical Simulation Desk tables.
- [x] Task 008C local paper-order intent validation fields are mapped to `paper_orders` intent fields.
- [x] Required foreign-key relationships are identified for paper portfolios, orders, positions, snapshots, and trade reviews.
- [x] Append-only / non-overwrite requirements are identified for historical recommendations, paper orders, paper positions, trade reviews, learning proposals, and audit events.
- [x] Losing outcomes visibility is preserved as a migration/runtime requirement.
- [x] Proposal reviewability is preserved; learning proposals must not be auto-applied.
- [x] Audit event requirements are identified without creating database audit events in this PR.
- [x] No production connection is assumed.

## RLS / Auditability Readiness Checklist

A future Supabase implementation must define and review:

- [ ] Which Simulation Desk tables are user-owned or portfolio-owner-scoped.
- [ ] Whether `paper_portfolios.owner_profile_id` is required for RLS enforcement before runtime.
- [ ] Read and write policies for `paper_portfolios`, `paper_orders`, `paper_positions`, `portfolio_snapshots`, `trade_reviews`, and `learning_proposals`.
- [ ] Append-only or restricted-update policies for `audit_events`.
- [ ] Actor metadata requirements for auditability, including `actor_type`, `actor_id`, and source workflow identifiers.
- [ ] Safe service-role usage boundaries, if any, with no secrets committed.
- [ ] Evidence that RLS cannot expose another user's paper portfolio, orders, positions, snapshots, reviews, or proposals.

## Retention / Append-Only Readiness Checklist

A future implementation must preserve:

- [ ] Historical simulation recommendations without overwriting them to improve appearance.
- [ ] Losing paper trades in reports and reviews.
- [ ] Original paper-order intent and lifecycle history.
- [ ] Original position entry/exit evidence and outcome labels.
- [ ] Portfolio snapshots as historical valuation/risk evidence.
- [ ] Trade reviews as review records rather than mutable performance polishing.
- [ ] Learning proposals as reviewable proposals, not automatic behavior changes.
- [ ] Audit events as immutable append-only governance records.

## Approval Gates Before Implementation

Harness Engineering approval is required before each gate below can be crossed:

1. **SQL migration gate** — before adding or changing migration files, schema DDL, indexes, constraints, or RLS SQL.
2. **Supabase client gate** — before adding a Supabase client, dependency, environment variable expectation, or local/production connection path.
3. **Production Supabase gate** — before connecting to production Supabase or assuming production project configuration.
4. **Persistence write gate** — before adding inserts, updates, deletes, upserts, persistence adapters, repositories, or database write paths.
5. **Endpoint runtime gate** — before implementing runtime behavior for locked MVP endpoint names that are not currently active.
6. **Paper-order creation gate** — before creating, submitting, filling, or lifecycle-mutating any paper order.
7. **Paper-portfolio runtime gate** — before adding runtime portfolio retrieval, valuation, position, or snapshot behavior.
8. **Strategy recommendation persistence gate** — before writing or retrieving persisted strategy recommendations through new runtime paths.
9. **Audit-event creation gate** — before creating database audit events or wiring audit events into runtime mutation paths.
10. **Broker / real-money gate** — before any broker API, real-money account integration, autonomous order placement, or real-money trading automation. This gate remains out of scope for v1 and is not authorized by Task 008D.

## Task 008E Entry Criteria

Task 008E may begin only after Harness Engineering confirms the next safe Simulation Desk slice.

Minimum entry criteria:

1. Task 008D is reviewed and merged.
2. Required validation commands for Task 008D pass in the PR evidence.
3. Harness Engineering states whether Task 008E is documentation-only, implementation-limited local-only, or explicitly approved for one named runtime/persistence gate.
4. If Task 008E proposes migration, persistence, Supabase, endpoint runtime, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, or audit-event creation, the relevant approval gate must be explicitly named before implementation begins.
5. `docs/09-api-and-agent-contracts.md` must remain unchanged unless Task 008E explicitly proposes a reviewed public contract change with same-PR docs/tests/status/log alignment.
6. Broker integration, autonomous order placement, real-money account access, and real-money trading automation remain out of scope unless Harness Engineering creates a separate explicit governance decision outside the v1 advisory-only boundary.

## Explicit Non-Goals

Task 008D does not add:

- SQL migration;
- `supabase/migrations` changes;
- Supabase client;
- production Supabase connection;
- database writes;
- persistence adapter;
- FastAPI route;
- `POST /api/v1/simulation/paper-orders` implementation;
- `GET /api/v1/paper-portfolios/{portfolio_id}` implementation;
- `POST /api/v1/strategy-recommendations` implementation;
- `GET /api/v1/strategy-recommendations/{recommendation_id}` implementation;
- public analyze-stock payload change;
- public handoff preview exposure;
- `docs/09-api-and-agent-contracts.md` changes;
- paper order creation;
- paper portfolio runtime;
- strategy recommendation persistence;
- audit event database creation;
- live market data;
- external APIs;
- broker APIs;
- autonomous order placement;
- secrets or API keys;
- real-money trading automation;
- frontend/UI;
- report output.

## Validation Commands

Required validation for this documentation-only PR:

```bash
python scripts/validate_contracts.py
git diff --check
```

Because `docs/11-project-status.md` is updated, also run:

```bash
PYTHONPATH=backend pytest backend/tests -q
```

## Review Checklist

Reviewers should confirm:

- [ ] `docs/31-task-008d-persistence-gate-readiness-and-migration-alignment.md` exists.
- [ ] Task 008D is documented as planning-only and governance-sensitive.
- [ ] Task 007 / M4 remains Completed.
- [ ] Task 008 / M5 remains In Progress.
- [ ] Task 008B / 008C local records are mapped to canonical `docs/08` tables.
- [ ] Locked `docs/09` endpoint names are mapped to future gates without implementation.
- [ ] Approval gates before migration, runtime, persistence, Supabase, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit-event creation, broker integration, and real-money trading are explicit.
- [ ] `docs/09-api-and-agent-contracts.md` is not changed.
- [ ] No backend runtime implementation is added.
- [ ] No FastAPI route is added.
- [ ] No endpoint implementation is added.
- [ ] No persistence writes or database write path are added.
- [ ] No Supabase client or migration is added.
- [ ] No secrets, broker integration, paper order creation, real-money trading automation, live market data, external API usage, frontend/UI, or report output are added.
- [ ] `docs/11-project-status.md`, `docs/progress-log.md`, and `docs/decision-log.md` are updated consistently.
- [ ] Validation evidence is included in the PR body.
- [ ] Codex does not self-approve; Harness Engineering must review.
