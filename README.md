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
- `docs/decision-log.md` — key project decisions.
- `docs/progress-log.md` — milestone progress tracking.
- `docs/lessons-learned.md` — retrospective notes and operational learning.
