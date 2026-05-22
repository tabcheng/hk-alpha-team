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

## Standard API Envelope

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

## MVP Endpoint Blueprint

## 1) Research

- `POST /api/v1/research/notes`
- `GET /api/v1/research/notes/{id}`
- `GET /api/v1/research/notes?security_id=&status=`

### Example request (`POST /research/notes`)

```json
{
  "security_id": "uuid",
  "title": "Tencent ad monetization thesis update",
  "thesis": "Revenue quality improving on margin discipline.",
  "key_points": ["point_a", "point_b"],
  "sources": [{"type": "filing", "url": "https://example.com"}],
  "confidence": 67.5
}
```

## 2) Strategy

- `POST /api/v1/strategy/recommendations`
- `GET /api/v1/strategy/recommendations/{id}`
- `GET /api/v1/strategy/recommendations?security_id=&status=`
- `POST /api/v1/strategy/recommendations/{id}/reviews`

### Example strategy response payload (`data`)

```json
{
  "recommendation_id": "uuid",
  "security_id": "uuid",
  "label": "WAIT_FOR_PULLBACK",
  "confidence": 64.0,
  "summary": "Attractive long-term quality but near-term entry is extended.",
  "reasoning": "Valuation has moved ahead of baseline assumptions.",
  "key_risks": ["macro slowdown", "regulatory tightening"],
  "invalidation_conditions": ["re-acceleration in earnings surprises"]
}
```

## 3) Simulation

- `POST /api/v1/simulations/runs`
- `GET /api/v1/simulations/runs/{id}`
- `POST /api/v1/simulations/runs/{id}/positions`
- `POST /api/v1/simulations/positions/{position_id}/events`
- `GET /api/v1/simulations/runs/{id}/metrics`

### Example simulation run create request

```json
{
  "name": "Q3 Pullback Discipline Test",
  "objective": "Evaluate pullback entries under volatile regime.",
  "configuration": {
    "max_positions": 8,
    "position_size_pct": 5,
    "stop_loss_pct": 8
  },
  "start_date": "2024-01-01",
  "end_date": "2024-12-31"
}
```

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
