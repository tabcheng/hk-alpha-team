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

## Implementation Notes Added After PR #7

- `POST /api/v1/analyze-stock` now has a Phase 3 contract-first stub implementation.
- The stub preserves the locked endpoint name and response envelope while avoiding real analysis, persistence, production Supabase, Railway deployment, and trading execution.
- Future Phase 4 work should replace stub internals without renaming the endpoint, envelope fields, or preferred strategy labels unless the contract lock process is followed.
