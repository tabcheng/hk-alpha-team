# 19 — First Analysis Workflow Stub (Contract-First)

## Purpose

Document the current contract-first stub behavior for the first analysis workflow endpoint and clarify boundaries before real analysis implementation.

## Implemented Endpoint

- `POST /api/v1/analyze-stock`

## Request Body

```json
{
  "symbol": "0700.HK"
}
```

## Success Response Shape

Success responses use the required envelope and include stub data fields:

- `symbol`
- `analysis_mode = "stub"`
- `human_decision_required = true`
- `recommendation.confidence = 0`
- clear summary that no real investment analysis has been performed
- warning indicating this is a contract test/stub response and not an investment recommendation

## Validation Error Behavior

- Missing `symbol` key returns request validation error (`422`) from FastAPI model validation.
- Blank `symbol` returns contract error envelope with `VALIDATION_ERROR`.
- Non-HK format symbol (for example `AAPL`) returns contract error envelope with `VALIDATION_ERROR`.

## Stub-Only / Advisory-Only Warning

This endpoint currently provides **contract-testing placeholder output only**.
It must not be interpreted as investment advice and must not be used for real-money decisions.

## What Is Not Implemented

- Market/fundamental/technical analysis logic
- External data provider ingestion
- Agent orchestration across departments
- Database-backed recommendation persistence
- Simulation order creation from endpoint output

## Follow-Up Path Toward Real First Analysis Workflow

1. Finalize canonical symbol-format policy and validation rules.
2. Add deterministic orchestration scaffolding for research/agent synthesis.
3. Introduce database-backed storage for recommendation and traceability records.
4. Expand error mapping coverage to all contract error classes.
5. Keep advisory-only and human-in-the-loop controls explicit in all outputs.

## Phase 4 Readiness Contribution

This stub prepares Phase 4 by locking endpoint shape, validation behavior, warning semantics, and envelope consistency **without performing real analysis**.
