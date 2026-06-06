# Task 003 — Design API and Agent Contracts

## Objective

Define service contracts between application layers and agent departments using the exact required MVP endpoint set and exact required response envelope.

## Required MVP Endpoint Set

- `GET /health`
- `POST /api/v1/analyze-stock`
- `GET /api/v1/stocks/{symbol}`
- `GET /api/v1/strategy-recommendations/{recommendation_id}`
- `POST /api/v1/strategy-recommendations`
- `POST /api/v1/simulation/paper-orders`
- `GET /api/v1/paper-portfolios/{portfolio_id}`
- `GET /api/v1/agent-runs/{agent_run_id}`
- `GET /api/v1/project-status`

## Required Response Envelope

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

## Deliverables

- Contract specification document.
- Example payloads for all eight agent departments.
- Versioning and backward-compatibility policy draft.

## Implementation Notes Added After PR #10

- `POST /api/v1/analyze-stock` now has a Phase 4A deterministic local-only workflow skeleton implementation.
- Phase 4B adds deterministic local-only department adapter preview outputs that mirror the locked common agent output shape while preserving the locked endpoint name, required response envelope, `analysis_status`, and `workflow_phase`.
- The Phase 4A/4B skeleton preserves the locked endpoint name and response envelope while avoiding live market data, external APIs, persistence, production Supabase, Railway deployment, broker execution, paper order creation, secrets, and real-money trading automation.
- The historical Phase 3 contract-first stub used `analysis_status = "stub_only"`; the current canonical runtime contract uses `analysis_status = "phase4a_skeleton"`.
- Future Phase 4 work should extend the skeleton without renaming the endpoint, envelope fields, or preferred strategy labels unless the contract lock process is followed.

## Task 008G Contract Addendum

- `POST /api/v1/simulation/paper-orders` remains the locked Simulation Desk endpoint name.
- The required response envelope remains unchanged.
- The endpoint contract now distinguishes `simulation_origin = "user_recorded"` from `simulation_origin = "system_generated_learning"`.
- `user_recorded` records require human/user/Harness Engineering source metadata and notes.
- `system_generated_learning` records require original recommendation, original scores, original thesis, entry/exit assumptions, PnL, holding period, what worked, what failed, improvement suggestions, and `requires_human_review = true`.
- Learning proposals remain reviewable only and must not be auto-applied.
- Real-money trading, autonomous real-money execution, broker execution APIs, production Supabase connection, secrets, live market data, deployment, and persistence writes remain out of scope until separately approved.


## Task 008I Runtime Addendum

- `POST /api/v1/simulation/paper-orders` now has a non-production process-local in-memory runtime slice for both Task 008G origins.
- `GET /api/v1/paper-portfolios/{portfolio_id}` now returns non-production in-memory paper portfolio snapshots for portfolios created within the current process.
- The required response envelope remains unchanged.
- Audit-event previews are generated in memory only; learning-proposal previews remain reviewable and are not auto-applied.
- SQL migration, Supabase persistence, production Supabase, deployment, billing/payment runtime, membership/subscription runtime, auth runtime, live data, broker integration, secrets, real-money trading, and autonomous real-money execution remain out of scope.
- Task 008 / M5 remains In Progress.
