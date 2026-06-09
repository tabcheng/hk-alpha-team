# Task 008L — Local/Test Endpoint Persistence Wiring

Date: 2026-06-08

## Purpose

Task 008L wires the existing Task 008K local/test PostgreSQL Simulation Desk persistence adapter into the `POST /api/v1/simulation/paper-orders` runtime through an explicit injection gate.

The default endpoint behavior remains the Task 008I process-local in-memory runtime. PostgreSQL writes are available only when all of the following are true:

1. `HK_ALPHA_SIMULATION_PERSISTENCE_MODE=local_test_postgres` is explicitly configured.
2. `HK_ALPHA_TEST_POSTGRES_DSN` is present.
3. The configured database name is `hk_alpha_validation`, `hk_alpha_test`, or starts with `hk_alpha_validation_` / `hk_alpha_test_`.

`DATABASE_URL` alone does not authorize Simulation Desk endpoint persistence.

## Runtime Modes

| Mode | Activation | Behavior |
| --- | --- | --- |
| `memory` | Default when `HK_ALPHA_SIMULATION_PERSISTENCE_MODE` is absent or set to `memory` | Uses only the non-production in-memory Simulation Desk runtime; no PostgreSQL write is attempted. |
| `local_test_postgres` | Requires `HK_ALPHA_SIMULATION_PERSISTENCE_MODE=local_test_postgres` and safe `HK_ALPHA_TEST_POSTGRES_DSN` | Builds the Task 008J/008K paper-order persistence payload, writes it with `LocalTestPostgresSimulationPersistence`, and reads the written paper-order row back for local/test validation evidence. |

## Endpoint Contract Preservation

The locked response envelope remains:

- `request_id`
- `status`
- `data`
- `metadata`
- `warnings`

Task 008L adds local/test runtime disclosures inside response metadata, response data, and warnings only when local/test PostgreSQL mode is explicitly enabled, without renaming endpoint paths, canonical table names, response envelope fields, preferred strategy labels, MVP phase names, or Investment Strategy Office required fields.

## Safety Boundaries

Task 008L remains local/test only.

It does not add:

- Production Supabase runtime persistence.
- Supabase client creation.
- Hosted Supabase credentials.
- Supabase service role keys.
- Production migration application.
- Broker integration or broker execution APIs.
- Real-money trading or autonomous real-money execution.
- Live market data, vendor/API calls, billing, membership, authentication, deployment, frontend/UI, or secrets.

The endpoint response explicitly discloses paper-only, advisory-only, human-in-the-loop, local/test persistence mode when enabled.

## Validation Coverage

Task 008L adds endpoint-level tests for:

- Default memory mode without PostgreSQL.
- `DATABASE_URL` not authorizing persistence.
- Safe failure when `local_test_postgres` mode lacks `HK_ALPHA_TEST_POSTGRES_DSN`.
- Safe failure for unsafe database names.
- Safe failure for unknown persistence modes.
- Local/test PostgreSQL write/read roundtrip for `user_recorded`.
- Local/test PostgreSQL write/read roundtrip for `system_generated_learning`.
- Locked success-envelope fields.
- Reviewable, non-auto-applied learning proposal previews.
- Losing outcome visibility.
- Historical recommendation metadata preservation.

## Future Production Path (Non-Binding)

Task 008L does not define production Supabase readiness. Any production persistence path should be handled in a later scoped Task 008N docs/governance PR after Task 008L and Task 008M evidence, with Harness Engineering approval and Evidence Closure.

## Status

Task 008 / M5 remains In Progress. Task 008L advances local/test endpoint persistence evidence only and must not be interpreted as production persistence readiness.
