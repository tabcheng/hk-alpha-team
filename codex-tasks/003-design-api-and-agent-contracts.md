# Task 003 — Design API and Agent Contracts

## Objective

Define service contracts between application layers and agent departments using exact MVP endpoint names and required response envelope.

## Required MVP Endpoint Names

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

## Required Response Envelope

```json
{
  "meta": {
    "request_id": "req_123",
    "timestamp": "2026-05-22T00:00:00Z",
    "version": "v1"
  },
  "data": {},
  "error": null
}
```

## Deliverables

- Contract specification document.
- Example payloads for all eight agent departments.
- Versioning and backward-compatibility policy draft.
