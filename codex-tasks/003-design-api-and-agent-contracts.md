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
