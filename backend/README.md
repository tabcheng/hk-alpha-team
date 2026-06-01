# Backend Skeleton (Phase 3 Foundation)

This folder contains the Phase 3 backend skeleton for HK Alpha Team.

## Scope

Included in this PR:

- FastAPI app entrypoint.
- `GET /health` endpoint.
- `GET /api/v1/project-status` endpoint (status sourced from `docs/11-project-status.md`).
- `POST /api/v1/analyze-stock` contract-first stub endpoint.
- Shared success/error envelope helpers aligned to `docs/09-api-and-agent-contracts.md`.
- Validation error handling through the documented error envelope.
- Pytest coverage for implemented endpoints, analyze-stock validation, and envelope shape.

Out of scope:

- Production Supabase/database integration.
- Real analyze-stock workflow implementation.
- Market data ingestion.
- Brokerage execution integration.
- Railway deployment or hosted runtime setup.
- Secrets or production credentials.

## Run locally

```bash
pip install -r backend/requirements.txt
PYTHONPATH=backend uvicorn app.main:app --reload
```

## Test

```bash
PYTHONPATH=backend pytest backend/tests
```
