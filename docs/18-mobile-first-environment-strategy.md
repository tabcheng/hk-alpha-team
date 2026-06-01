# 18 — Mobile-First Environment Strategy

## Purpose

Document the lightweight environment strategy for Harness Engineering while HK Alpha Team is operated primarily from mobile devices with ChatGPT, Codex Web, and GitHub.

This strategy supports Phase 3 backend skeleton hardening and Phase 4 first analysis workflow preparation without requiring local desktop setup, production secrets, Railway deployment, or hosted Supabase setup.

## Current Operating Assumption

Harness Engineering is a solo developer/operator and may review, guide, and merge work from a mobile device.

Therefore, near-term implementation should optimize for:

- repository-native documentation and tests
- GitHub pull request reviewability
- CI-based verification
- Codex-executable tasks
- clear out-of-scope boundaries for production infrastructure

## Environment Tiers

### Tier 0 — Mobile Review and Governance

**Primary user:** Harness Engineering on mobile.

**Tools:** ChatGPT, Codex Web, GitHub mobile/browser, repository docs, pull request checks.

**Expected capabilities:**

- review diffs and PR descriptions
- verify CI results
- inspect docs and task cards
- approve or request changes
- keep scope decisions in logs

**Not required:**

- local Python setup
- local Docker setup
- Supabase dashboard access
- Railway dashboard access
- secrets management

### Tier 1 — Codex/GitHub CI Development

**Primary user:** Codex-assisted implementation flow.

**Tools:** repository branch, pytest, contract validation, GitHub Actions.

**Expected capabilities:**

- implement small backend stubs and tests
- run `PYTHONPATH=backend pytest backend/tests`
- run `python scripts/validate_contracts.py`
- update docs, decisions, progress, and lessons in the same PR

**Not required:**

- production database connection
- hosted deployment
- live market data integration
- broker execution API integration

### Tier 2 — Optional Local/Test Infrastructure

**Primary user:** future desktop or cloud development session.

**Tools:** local/test PostgreSQL, local backend server, optional Supabase-compatible test setup.

**Expected capabilities:**

- execute migration validation against local/test PostgreSQL
- run backend locally for manual endpoint checks
- test persistence adapters before production setup

**Not required for PR #8:**

- production Supabase project
- Railway service
- real secrets
- real-money account data

### Tier 3 — Future Hosted Runtime

**Primary user:** future deployment operator after explicit approval.

**Tools:** Railway, hosted Supabase, managed secrets, monitoring.

**Entry gate:** a future explicit task/decision must authorize hosted setup and define secret handling.

**Out of scope now:** PR #8 must not require or configure hosted runtime infrastructure.

## PR #8 Environment Rule

For the analyze-stock stub, the backend must remain usable through tests and CI only:

- `POST /api/v1/analyze-stock` returns a contract-shaped stub response.
- No production Supabase connection is required.
- No Railway deployment is required.
- No market data provider is required.
- No brokerage or real-money execution API is allowed.
- No secrets are required or committed.

## Verification Model

The near-term verification model is CI-first:

1. Backend tests verify endpoint behavior and response envelope shape.
2. Contract validation checks locked endpoint, envelope, schema, and strategy label surfaces.
3. Documentation review confirms advisory-only, human-in-the-loop boundaries.
4. Pull request review confirms no production setup or secrets were introduced.

## Promotion Criteria for Future Hosted Setup

Before moving beyond mobile-first CI verification, a future PR should document:

- which hosted services are being introduced
- which secrets are required and where they are stored
- how production and test environments are separated
- rollback expectations
- human approval gates
- audit/logging expectations

Until then, HK Alpha Team remains repository-first and advisory-only.
