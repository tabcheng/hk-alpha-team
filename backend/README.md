# Backend Skeleton (Phase 3 Foundation)

This folder contains the Phase 3 backend skeleton for HK Alpha Team.

## Scope

Included in this PR:

- FastAPI app entrypoint.
- `GET /health` endpoint.
- `GET /api/v1/project-status` endpoint (status sourced from `docs/11-project-status.md`).
- Shared success/error envelope helpers aligned to `docs/09-api-and-agent-contracts.md`.
- Pytest coverage for the two implemented endpoints.

Out of scope:

- Production Supabase/database integration.
- Analyze-stock workflow implementation.
- Market data ingestion.
- Brokerage execution integration.

## Run locally

```bash
pip install -r backend/requirements.txt
PYTHONPATH=backend uvicorn app.main:app --reload
```

## Test

```bash
PYTHONPATH=backend pytest backend/tests
```
