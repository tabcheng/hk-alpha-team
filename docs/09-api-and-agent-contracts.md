# 09 — API and Agent Contracts (Task 003)

## Purpose

Define stable v1 contracts between clients, backend API, and internal agent departments.

## Scope and Boundaries

- Contract and payload design only.
- No implementation code or live integration.
- Advisory-first outputs; no trade execution interfaces.

## Contract Principles

1. All responses include traceability metadata (`request_id`, `timestamp`, `version`).
2. Domain payloads separate data (`data`) from operational status (`meta`, `error`).
3. Agent outputs must include reasoning, risks, and invalidation conditions where strategy advice is present.
4. Versioning uses explicit `v1` pathing and semantic contract updates.

## Required Response Envelope (All MVP Endpoints)

### Success

```json
{
  "meta": {
    "request_id": "req_123",
    "timestamp": "2026-05-21T00:00:00Z",
    "version": "v1"
  },
  "data": {},
  "error": null
}
```

### Failure

```json
{
  "meta": {
    "request_id": "req_123",
    "timestamp": "2026-05-21T00:00:00Z",
    "version": "v1"
  },
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "security_id is required",
    "details": {}
  }
}
```

## MVP Endpoint Blueprint (Required)

- `POST /api/v1/research/artifacts`
- `GET /api/v1/research/artifacts/{id}`
- `GET /api/v1/research/artifacts?security_id=&status=`
- `POST /api/v1/strategy/records`
- `GET /api/v1/strategy/records/{id}`
- `GET /api/v1/strategy/records?security_id=&status=`
- `POST /api/v1/strategy/records/{id}/reviews`
- `POST /api/v1/simulation/runs`
- `GET /api/v1/simulation/runs/{id}`
- `POST /api/v1/simulation/runs/{id}/positions`
- `POST /api/v1/simulation/positions/{position_id}/events`
- `GET /api/v1/simulation/runs/{id}/metrics`

All MVP endpoints must return the required response envelope in this document.

## Agent Department Contracts

## Common Agent Input Contract

```json
{
  "run_id": "agent_run_123",
  "department": "strategy",
  "request_context": {
    "user_id": "uuid",
    "timestamp": "2026-05-21T00:00:00Z"
  },
  "payload": {},
  "constraints": {
    "advisory_only": true,
    "execution_prohibited": true
  }
}
```

## Research Agent Output

Required fields:
- `research_summary`
- `evidence_points[]`
- `confidence`
- `open_questions[]`
- `data_quality_notes[]`

## Strategy Agent Output

Required fields:
- `label` (preferred set)
- `confidence`
- `summary`
- `reasoning`
- `key_risks[]`
- `invalidation_conditions[]`
- `human_decision_required` (boolean, must be true in v1)

## Simulation Agent Output

Required fields:
- `run_summary`
- `performance_metrics`
- `losing_trades_review`
- `improvement_proposals[]`
- `limitations`


## Minimal JSON Contract Rules (Validation Targets)

- `confidence` fields must be numeric in `[0, 100]`.
- Strategy `label` must be one of: `STRONG_WATCH`, `WAIT_FOR_PULLBACK`, `SMALL_POSITION`, `ACCUMULATE`, `HOLD`, `REDUCE_RISK`, `AVOID`.
- `human_decision_required` must always be `true` in v1 strategy outputs.
- `request_id` and `run_id` are required non-empty strings for traceability.

## JSON Examples for All Eight Agent Departments

### 1) Market Intelligence Agent
```json
{"department":"Market Intelligence Agent","market_regime":"risk_off","key_drivers":["USD strength"],"watch_items":["HK rate sensitivity"],"confidence":71}
```

### 2) Company Research Agent
```json
{"department":"Company Research Agent","security":"0700.HK","thesis":"Margin discipline improving","catalysts":["ad recovery"],"invalidation_conditions":["margin compression"],"confidence":68}
```

### 3) News & Sentiment Agent
```json
{"department":"News & Sentiment Agent","security":"0700.HK","sentiment":"neutral","material_events":["earnings preview"],"confidence":62}
```

### 4) Technical Analysis Agent
```json
{"department":"Technical Analysis Agent","security":"0700.HK","trend":"uptrend","support_levels":[360.0],"resistance_levels":[392.0],"invalidation_level":352.0}
```

### 5) Risk Manager Agent
```json
{"department":"Risk Manager Agent","portfolio_risk":"moderate","concentration_flags":["internet overweight"],"guardrails":["max position 5%"],"confidence":74}
```

### 6) Investment Committee Agent
```json
{"department":"Investment Committee Agent","posture":"WAIT_FOR_PULLBACK","consensus_score":0.64,"dissenting_views":["valuation stretched"],"open_questions":["policy sensitivity"]}
```

### 7) Simulation Investment Desk
```json
{"department":"Simulation Investment Desk","run_id":"sim_2026_001","performance_metrics":{"total_return_pct":4.2},"losing_trades_review":"2 stop-outs due to gap risk","improvement_proposals":["tighter event filter"]}
```

### 8) Investment Strategy Office
```json
{"department":"Investment Strategy Office","label":"WAIT_FOR_PULLBACK","summary":"Quality intact but entry extended","reasoning":"risk/reward unfavorable at current level","key_risks":["macro shock"],"invalidation_conditions":["earnings beat with re-rating"],"human_decision_required":true}
```

## Error Taxonomy

- `VALIDATION_ERROR` (400)
- `UNAUTHORIZED` (401)
- `FORBIDDEN` (403)
- `NOT_FOUND` (404)
- `CONFLICT` (409)
- `RATE_LIMITED` (429)
- `INTERNAL_ERROR` (500)
- `AGENT_TIMEOUT` (504)
- `AGENT_CONTRACT_VIOLATION` (502)

## Traceability Requirements

- Every API request generates `request_id`.
- Every agent run generates `run_id` and links to `request_id`.
- Persist core telemetry in `api_request_logs` and `agent_runs`.

## Versioning and Compatibility Policy

- Path versioning: `/api/v1/...`
- Additive fields are backward-compatible.
- Field removals/renames require new major version (`v2`).
- Deprecated fields require 2-release deprecation notice in docs.

## Out of Scope

- Auth provider implementation.
- Webhook/event bus design.
- Client SDK generation.
