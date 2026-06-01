# 17 — Backend Skeleton

## Purpose

Document the Phase 3 FastAPI backend skeleton and its contract boundaries.

The backend skeleton exists to make the locked API contracts testable before full data, agent, simulation, or deployment infrastructure is introduced.

## Implemented Endpoints

### `GET /health`

Returns the required success envelope with:

```json
{ "service": "ok" }
```

### `GET /api/v1/project-status`

Returns the required success envelope with project phase, milestone, and task status fields derived from `docs/11-project-status.md`.

### `POST /api/v1/analyze-stock`

Returns the required success envelope with a Phase 3 stub payload for a canonical Hong Kong symbol such as:

```json
{ "symbol": "0700.HK" }
```

The stub validates the request shape, returns advisory-style placeholder fields, and includes explicit warnings that no live analysis or execution occurred. Detailed stub runbook coverage lives in `docs/19-first-analysis-workflow-stub.md`.

## Analyze-Stock Stub Boundary

The analyze-stock stub is contract-first only. It is designed to prepare clients, tests, and future agent workflow integration for Phase 4.

It does not:

- fetch market data
- read or write Supabase data
- create `agent_runs` or `agent_outputs`
- create strategy recommendation records
- create paper orders
- call external data providers
- deploy to Railway
- connect to brokerage APIs
- execute or recommend real-money trades as an automated action

The stub must continue to include:

- preferred strategy label field
- reasoning placeholder
- main risks
- invalidation conditions
- paper-trading non-action statement
- real-money human decision framing
- warnings describing stub-only behavior

## Response Envelope Rules

Successful endpoint responses use:

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

Validation failures use the documented error envelope with `VALIDATION_ERROR` and details for review/debugging.

## Local/Test Commands

```bash
pip install -r backend/requirements.txt
PYTHONPATH=backend pytest backend/tests
PYTHONPATH=backend uvicorn app.main:app --reload
```

## CI Scope

Backend CI should remain lightweight and mobile-review friendly:

- install backend Python dependencies
- run backend pytest coverage
- run contract validation

CI must not require production Supabase, Railway, secrets, broker credentials, or live market data.

## Follow-Up Guidance

Future Phase 4 work may replace the stub internals with real first analysis workflow components only after contracts and tests are updated in the same PR.

Any move toward hosted infrastructure must follow `docs/18-mobile-first-environment-strategy.md` and be authorized by an explicit future task/decision.
