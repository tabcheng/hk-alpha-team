# 41 — Task 008M Local/Test Persisted Read Model

## Purpose

Task 008M adds a local/test-only persisted read path for Simulation Desk paper-portfolio consistency evidence. In explicit `local_test_postgres` mode, a paper order written through `POST /api/v1/simulation/paper-orders` can be read back through `GET /api/v1/paper-portfolios/{portfolio_id}` from local/test PostgreSQL paper-order records.

## Scope

- Implementation-limited backend/local-test persistence read scope only.
- Default endpoint runtime remains process-local in-memory.
- Local/test PostgreSQL readback requires both:
  - `HK_ALPHA_SIMULATION_PERSISTENCE_MODE=local_test_postgres`
  - safe `HK_ALPHA_TEST_POSTGRES_DSN`
- `DATABASE_URL` alone does not authorize persistence writes or persisted readback.
- Approved local/test database names remain `hk_alpha_validation`, `hk_alpha_test`, or names starting with `hk_alpha_validation_` / `hk_alpha_test_`.

## Readback Behavior

In memory mode, `GET /api/v1/paper-portfolios/{portfolio_id}` keeps the existing in-memory snapshot behavior and warnings.

In explicit local/test PostgreSQL mode, the endpoint reads persisted `paper_orders` by the same stable local/test `paper_portfolios.portfolio_uuid` identity used by the write path, not by the non-unique portfolio display `name`, and returns a non-production portfolio snapshot containing recent persisted paper-order evidence, including:

- simulation origin and paper-order origin;
- source metadata;
- boundary flags;
- human-review flags;
- reviewable/non-auto-applied learning proposal guardrails and `learning_proposal_readback` evidence for `system_generated_learning`;
- historical recommendation metadata;
- outcome preview and losing outcome visibility.

## Safety Boundary

Task 008M does not add production Supabase readiness, production Supabase credentials, Supabase client runtime, hosted credentials, vendor/API calls, live market data, broker integration, broker execution APIs, real-money trading, autonomous real-money execution, real-money account connectivity, hidden or irreversible investment actions, billing/payment runtime, auth runtime, deployment config, frontend/UI, or secrets.

## Contract Boundary

Task 008M does not rename endpoints and does not change the required top-level success envelope fields: `request_id`, `status`, `data`, `metadata`, and `warnings`. Local/test readback is disclosed through additive metadata, data, and warnings only.

## Governance Note

No new `docs/decision-log.md` entry is required for Task 008M because the work stays inside the already approved local/test, paper-only, advisory-only, non-real-money scope and does not introduce a new governance decision.
