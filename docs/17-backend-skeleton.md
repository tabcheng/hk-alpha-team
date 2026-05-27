# 17 — Backend Skeleton (Phase 3 Foundation)

## Purpose

Define the Phase 3 contract-first backend skeleton baseline for HK Alpha Team.

This artifact documents what is implemented now, how it is validated, and what remains explicitly out of scope.

## Scope Boundary

This backend skeleton is **local/test only**.

- No production Supabase connection.
- No Railway deployment.
- No real stock analysis logic.
- No broker integration.
- No real-money trading logic.

## Implemented Endpoints

Current implemented endpoints:

- `GET /health`
- `GET /api/v1/project-status`

These endpoints are intentionally minimal and are used to validate envelope consistency, routing, and test/CI flow before broader endpoint implementation.

## Success Response Envelope Rules

Success responses must use the required envelope from `docs/09-api-and-agent-contracts.md`:

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

Rules:

1. `status` must be `success`.
2. `metadata.schema_version` must remain contract-aligned (`v0.1` currently).
3. `metadata.generated_at` must be generated at response time in ISO-8601 format.
4. `metadata.source` must be `HK_ALPHA_TEAM`.
5. `warnings` must be present as an array (empty when no warnings).

## Error Envelope Rules

Error responses must use the explicit error envelope contract:

```json
{
  "request_id": "uuid",
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable error message",
    "details": {}
  }
}
```

Rules:

1. `status` must be `error`.
2. `error.code` must use a contract-approved code.
3. `error.message` must be human readable.
4. `error.details` must be an object (empty object allowed).

## Local Test Instructions

Install backend dependencies:

```bash
pip install -r backend/requirements.txt
```

Run backend tests:

```bash
PYTHONPATH=backend pytest backend/tests
```

Run contract validation:

```bash
python scripts/validate_contracts.py
```

## CI Behavior

`backend-check` workflow runs:

1. dependency installation (`backend/requirements.txt`)
2. backend tests (`PYTHONPATH=backend pytest backend/tests`)
3. contract validation (`python scripts/validate_contracts.py`)

Related unchanged workflows:

- `contract-check` (contract lock validation)
- `sql-migration-check` (local/test migration execution validation)

## Out-of-Scope Items (This Phase Slice)

- Production Supabase runtime/database wiring.
- Production secrets.
- Railway deployment/runtime operations.
- Frontend/UI implementation.
- Market data ingestion.
- Brokerage execution integration.
- Real-money trading automation.
- `POST /api/v1/analyze-stock` implementation logic.

## Follow-up Tasks for `POST /api/v1/analyze-stock`

1. Define request model validation and symbol-format policy.
2. Define initial stub flow for advisory-only analysis orchestration.
3. Add deterministic test fixtures for strategy envelope shape.
4. Add contract tests for error mapping (`VALIDATION_ERROR`, `NOT_FOUND`, `AGENT_CONTRACT_VIOLATION`, `INTERNAL_ERROR`).
5. Add explicit human-decision framing checks in response payload tests.
