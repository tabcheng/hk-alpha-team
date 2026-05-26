# HK Alpha Team

HK Alpha Team is an **AI-assisted Hong Kong equity research and investment strategy advisory system**.

It supports human decision-making through structured analysis, strategy proposals, paper trading records, simulation reviews, and iterative learning artifacts.

## Important Scope Boundary

HK Alpha Team is **not** an automated trading system.

- It does not execute real-money trades.
- It does not connect to broker execution APIs for autonomous order placement.
- It does not replace human judgment.

All real-money decisions remain under human control.

## Human-in-the-Loop Governance

The human user acts as **Harness Engineering** and is responsible for:

- Final investment decision approval.
- Risk acceptance and capital allocation decisions.
- Oversight of research quality, model behavior, and simulation integrity.

## Strategy Recommendation Labels

Preferred strategy labels:

- `STRONG_WATCH`
- `WAIT_FOR_PULLBACK`
- `SMALL_POSITION`
- `ACCUMULATE`
- `HOLD`
- `REDUCE_RISK`
- `AVOID`

## v1 Canonical Design Contracts

### Primary Schema Table Names

- `stocks`
- `market_indices`
- `price_bars`
- `market_snapshots`
- `company_financials`
- `news_items`
- `research_documents`
- `agent_runs`
- `agent_outputs`
- `investment_committee_reviews`
- `strategy_recommendations`
- `paper_portfolios`
- `paper_orders`
- `paper_positions`
- `portfolio_snapshots`
- `trade_reviews`
- `learning_proposals`
- `audit_events`

### Required MVP API Endpoints

- `GET /health`
- `POST /api/v1/analyze-stock`
- `GET /api/v1/stocks/{symbol}`
- `GET /api/v1/strategy-recommendations/{recommendation_id}`
- `POST /api/v1/strategy-recommendations`
- `POST /api/v1/simulation/paper-orders`
- `GET /api/v1/paper-portfolios/{portfolio_id}`
- `GET /api/v1/agent-runs/{agent_run_id}`
- `GET /api/v1/project-status`

### Required Response Envelope

```json
{
  "request_id": "uuid",
  "status": "success",
  "data": {},
  "metadata": {
    "schema_version": "v0.1",
    "generated_at": "ISO-8601 timestamp",
    "source": "HK_ALPHA_TEAM"
  },
  "warnings": []
}
```

## Phase 2 Migration/Validation Baseline (PR #4)

- `supabase/migrations/0001_create_core_schema.sql` — **draft-only** core schema migration baseline generated from canonical schema docs.
- `docs/15-migration-assumptions.md` — explicit schema interpretation assumptions and deferred items for the draft migration.
- `scripts/validate_contracts.py` — lightweight validator for contract-lock surfaces and sensitive-assignment scanning.
- `.github/workflows/contract-check.yml` — CI workflow that runs contract validation on PRs and pushes to `main`.

This migration is draft-only and **must not be applied to production Supabase** without Harness Engineering review and explicit approval.

Applying this draft migration to production Supabase remains out of scope during Phase 2.


## Phase 2 Local/Test SQL Validation (PR #5)

- `scripts/check_migration_sql.sh` — local/test PostgreSQL migration execution validator.
- `.github/workflows/sql-migration-check.yml` — CI workflow that runs contract + migration checks.
- `docs/16-local-sql-validation.md` — runbook and governance notes for local/test validation.
- `docs/17-backend-skeleton.md` — Phase 3 backend skeleton baseline, local/test scope, and CI/testing contract notes.

Phase 2 validation is limited to local/test PostgreSQL execution checks. Applying migrations to production Supabase remains out of scope in this phase.

The `sql-migration-check` workflow validates that the draft migration executes successfully in local/test PostgreSQL context before backend skeleton work proceeds.


## Phase 3 Backend Skeleton Foundation (PR #6)

- `backend/app/main.py` — FastAPI application entrypoint with `GET /health` and `GET /api/v1/project-status`.
- `backend/app/contracts.py` — shared success/error response envelope helpers aligned to `docs/09-api-and-agent-contracts.md`.
- `backend/tests/test_api.py` — pytest coverage for implemented endpoints and envelope shape checks.
- `.github/workflows/backend-check.yml` — CI workflow for backend test execution and contract validation.
- `docs/17-backend-skeleton.md` — backend skeleton scope, envelope rules, CI behavior, and follow-up guidance.


## Documentation Map

- `PROJECT_BRIEF.md` — concise project charter.
- `AGENTS.md` — Codex governance, rules, and definition of done.
- `docs/00-project-vision.md` — long-form intent, boundaries, and outcomes.
- `docs/01-system-architecture.md` — conceptual architecture for early planning.
- `docs/02-agent-departments.md` — fixed eight-department model.
- `docs/03-investment-strategy-office.md` — final recommendation standards.
- `docs/04-simulation-investment-desk.md` — simulation learning and validation rules.
- `docs/05-data-and-storage-plan.md` — canonical v1 data and storage naming.
- `docs/06-codex-workflow.md` — Codex task execution and collaboration model.
- `docs/07-chatgpt-project-instructions.md` — GitHub copy of high-level project instructions.
- `docs/08-supabase-schema-design.md` — Supabase schema design.
- `docs/09-api-and-agent-contracts.md` — required API and agent contracts.
- `docs/10-mvp-implementation-plan.md` — requested phase model plan.
- `docs/11-project-status.md` — task status and merge readiness.
- `docs/12-initial-conversation-brief.md` — original intent and boundary continuity brief.
- `docs/13-pr-review-checklist.md` — reusable PR checklist and large PR review policy.
- `docs/14-codex-task-template.md` — reusable Codex task prompt template.
- `codex-tasks/005-create-supabase-migration-draft.md` — Task 005 phase-entry card for migration draft planning.
- `docs/decision-log.md` — key project decisions.
- `docs/progress-log.md` — milestone progress tracking.
- `docs/lessons-learned.md` — retrospective notes and operational learning.
