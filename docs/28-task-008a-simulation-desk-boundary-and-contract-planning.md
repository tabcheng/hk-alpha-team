# 28 — Task 008A Simulation Desk MVP Boundary and Contract Planning

## Purpose

Task 008A starts the Simulation Desk MVP planning path by defining the smallest safe Task 008 / Milestone M5 starting scope before any runtime, persistence, production Supabase, broker, paper-order execution, or real-money trading work begins.

This document is a planning source of truth for future Simulation Desk MVP PRs. It narrows the first M5 slice to boundary, contract, schema-reference, operating-rule, approval-gate, and follow-up sequencing decisions only.

## Source of Truth Reviewed

Task 008A reviewed the current repository source of truth, including:

- `AGENTS.md`
- `README.md`
- `docs/04-simulation-investment-desk.md`
- `docs/06-codex-workflow.md`
- `docs/08-supabase-schema-design.md`
- `docs/09-api-and-agent-contracts.md`
- `docs/10-mvp-implementation-plan.md`
- `docs/11-project-status.md`
- `docs/20-codex-pr-factory.md`
- `docs/27-phase-4g-m4-closeout-readiness-review.md`
- `docs/decision-log.md`
- `docs/progress-log.md`
- `docs/lessons-learned.md`
- `backend/tests/test_api.py`

## Current Project Position

- Task 007 / Milestone M4 is **Completed** after Phase 4G closeout readiness review.
- Task 008 / Milestone M5 was **Planned** before this PR.
- This PR intentionally starts Task 008A as the first Phase 5 planning step and moves Task 008 / Milestone M5 to **In Progress** for planning only.
- Phase 4C handoff previews remain internal-only. Public exposure remains deferred until Harness Engineering explicitly approves a separate contract-changing PR.

## Task 008A Classification

- **Documentation-only:** Task 008A creates planning documentation and aligned governance/status/log updates only.
- **Governance-sensitive:** Task 008A starts Task 008 / Milestone M5 planning and therefore records status/log/decision updates, but it does not authorize implementation.

Task 008A does **not** implement paper-order runtime, paper-portfolio runtime, strategy recommendation persistence, endpoint runtime, database writes, migrations, Supabase clients, live market data, broker integration, paper-order creation, or real-money trading automation.

## Simulation Desk MVP Boundary

The Simulation Desk MVP is a paper-trading simulation and review system for learning, validation, and advisory reporting. Its v1 boundary is:

- paper-only portfolio and order-intent tracking;
- append-only or historically traceable recommendation and simulation records;
- explicit retention of winning and losing paper-trade outcomes;
- reviewable learning proposals instead of silent strategy-logic mutation;
- human-in-the-loop review for all real-money decisions;
- no autonomous or real-money order placement.

The minimum safe starting point for M5 is to define local-only contract fixtures and validation boundaries before adding any persistence, production Supabase, or endpoint runtime. Future implementation must preserve the locked API names, locked response envelope, canonical simulation table names, preferred strategy labels, and Investment Strategy Office required fields.

## Relationship to `docs/04-simulation-investment-desk.md`

`docs/04-simulation-investment-desk.md` remains the operating-rule source for the Simulation Investment Desk. Task 008A translates those rules into M5 planning gates:

- simulation evaluates recommendation quality through disciplined paper trading and structured post-outcome review;
- required simulation records should preserve original recommendation context, scores, thesis, simulated entry/exit prices, realized and unrealized PnL, holding period, outcome review, what worked, what failed, and improvement suggestions;
- output artifacts may include paper trade blotters, performance summaries, review notes, and proposed improvements, but Task 008A does not create report output or UI;
- simulation outputs remain advisory and educational, with final real-money decisions retained by Harness Engineering.

## Relationship to `docs/08` Canonical Simulation Schema Tables

Task 008A references the canonical schema table names without renaming or migrating them:

- `paper_portfolios` — paper-only portfolio containers for future Simulation Desk portfolio scope.
- `paper_orders` — paper order intents and lifecycle events for future paper-execution simulation only.
- `paper_positions` — open/closed simulated position records that preserve winning and losing outcomes.
- `portfolio_snapshots` — future paper-portfolio valuation and drawdown snapshots.
- `trade_reviews` — post-trade reviews with explicit learning notes; losing trades must remain visible.
- `learning_proposals` — reviewable improvement proposals that are not auto-applied to production logic.
- `audit_events` — append-only governance and traceability events.

Task 008A does not add schema migrations, database writes, Supabase clients, audit event creation, or production Supabase setup. Any later persistence work requires a separate approval gate.

## Relationship to `docs/09` Locked Endpoints

Task 008A references the locked endpoint names without implementing or renaming them:

- `POST /api/v1/simulation/paper-orders`
- `GET /api/v1/paper-portfolios/{portfolio_id}`
- `POST /api/v1/strategy-recommendations`
- `GET /api/v1/strategy-recommendations/{recommendation_id}`

The endpoints above remain contract references for future M5 design and implementation. Task 008A does not change `docs/09-api-and-agent-contracts.md`, does not add endpoint handlers, does not change the public `POST /api/v1/analyze-stock` payload, and does not create paper orders or persisted strategy recommendations.

## Required Operating Rules

Future Simulation Desk MVP work must preserve these rules:

1. Historical recommendations must not be overwritten.
2. Losing paper trades must remain visible.
3. Simulation results do not guarantee real-world performance.
4. No real-money trades may be executed or automated.
5. Strategy learning produces reviewable proposals, not silent production logic changes.
6. Paper-order simulation must remain clearly distinguished from broker execution and real-money order placement.
7. Human review by Harness Engineering remains required before any production, persistence, public-contract, broker, or real-money boundary expansion.

## Proposed First Minimum Simulation Desk MVP Slice

The first minimum M5 implementation-adjacent slice should be **local-only contract fixtures and schemas** that make the simulation boundary reviewable without creating runtime effects.

Recommended minimum contents for the first implementation-adjacent PR:

- local-only fixture examples for paper portfolio, paper order intent, simulated position, trade review, and learning proposal shapes;
- validation-only schemas or typed fixtures that reference the canonical table and endpoint names without database writes;
- tests proving no fixture implies production Supabase, broker execution, real-money trading, or paper-order persistence;
- explicit warnings or metadata stating that fixtures are non-persistent and local-only;
- no endpoint implementation and no public API payload change unless Harness Engineering separately approves a contract-changing PR.

## Explicit Non-Goals for Task 008A

Task 008A does not include:

- runtime implementation;
- `POST /api/v1/simulation/paper-orders` implementation;
- `GET /api/v1/paper-portfolios/{portfolio_id}` implementation;
- `POST /api/v1/strategy-recommendations` implementation;
- `GET /api/v1/strategy-recommendations/{recommendation_id}` implementation;
- public analyze-stock payload changes;
- public handoff preview exposure;
- `docs/09-api-and-agent-contracts.md` contract changes;
- schema migrations or `supabase/migrations` changes;
- Supabase clients or production Supabase connections;
- persistence writes;
- paper-order creation;
- paper-portfolio runtime;
- strategy recommendation persistence;
- audit event creation;
- live market data or external APIs;
- broker APIs or autonomous order placement;
- secrets, API keys, or real-money account data;
- frontend/UI work;
- report output.

## Future PR Sequence Proposal

- **Task 008B: local-only simulation contract fixtures / schemas, no persistence.** Define deterministic fixture and validation shapes for Simulation Desk records while preserving locked contracts and no-runtime boundaries.
- **Task 008C: local-only paper order validation service or stub, no database writes unless separately approved.** Add validation logic only if Harness Engineering approves the implementation-limited scope and confirms that no persistence or endpoint behavior is introduced without same-PR authorization.
- **Task 008D: persistence planning or migration alignment, only if Harness Engineering approves.** Prepare persistence/migration alignment separately, with approval gates for schema migration, Supabase, audit-event handling, and retention policy.

## Required Validation Commands

Task 008A requires these validation commands before commit:

```bash
python scripts/validate_contracts.py
git diff --check
```

Because this PR intentionally updates `docs/11-project-status.md` and aligns the backend status parser tests, it should also run:

```bash
PYTHONPATH=backend pytest backend/tests -q
```

## Approval Gates Before Implementation

Before any Simulation Desk implementation begins, Harness Engineering must review the relevant gate:

- **Public API contract gate:** required before changing `docs/09-api-and-agent-contracts.md`, adding endpoint behavior, exposing new public payload fields, or changing response envelope behavior.
- **Persistence gate:** required before database writes, strategy recommendation persistence, paper-order persistence, portfolio snapshots, trade reviews, learning proposals, or audit events are created.
- **Production Supabase gate:** required before any production Supabase connection, service role usage, deployed database migration, RLS policy activation, or secret-backed production configuration.
- **Broker / real-money gate:** required before any broker API, execution workflow, account credential handling, autonomous order placement, or real-money trading-related capability. The v1 boundary remains no broker execution and no real-money trading automation.
- **Status/log gate:** required whenever Task 008 / M5 status, scope, governance decisions, or implementation readiness changes; updates must be recorded in `docs/11-project-status.md`, `docs/progress-log.md`, and, when a decision is made, `docs/decision-log.md`.

## Review Checklist for Task 008A

Reviewers should confirm:

- Task 007 / M4 remain Completed.
- Task 008 / M5 are intentionally In Progress for planning only.
- `docs/09-api-and-agent-contracts.md` is unchanged.
- No runtime endpoint implementation was added.
- No persistence writes, Supabase client, migration, live data, broker integration, secrets, paper-order creation, paper-portfolio runtime, or real-money trading automation was added.
- The future PR sequence remains small, reviewable, and auditable.
