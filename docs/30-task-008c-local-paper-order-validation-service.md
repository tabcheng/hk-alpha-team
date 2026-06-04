# 30 — Task 008C Local Paper Order Validation Service / Stub

## Purpose

Task 008C adds a pure local-only paper-order validation service/stub for Simulation Desk paper-order-intent-like inputs.

The service validates the minimum paper-order intent fields against the locked schema/API contract references and the Task 008B local contract fixture conventions, then returns an in-memory validation result. It does **not** create a paper order, write persistence, expose an endpoint, call Supabase, call a broker, call external APIs, or automate real-money trading.

## Source-of-Truth Reviewed

Task 008C was implemented after reviewing the current GitHub source-of-truth documents and local validation code:

- `AGENTS.md`
- `README.md`
- `docs/04-simulation-investment-desk.md`
- `docs/06-codex-workflow.md`
- `docs/08-supabase-schema-design.md`
- `docs/09-api-and-agent-contracts.md`
- `docs/10-mvp-implementation-plan.md`
- `docs/11-project-status.md`
- `docs/20-codex-pr-factory.md`
- `docs/28-task-008a-simulation-desk-boundary-and-contract-planning.md`
- `docs/29-task-008b-local-simulation-contract-fixtures.md`
- `docs/decision-log.md`
- `docs/progress-log.md`
- `docs/lessons-learned.md`
- `backend/app/simulation_contract.py`
- `backend/tests/test_simulation_contract.py`

## Current Project Position

- Task 007 / Milestone M4 is **Completed**.
- Task 008 / Milestone M5 is **In Progress**.
- Task 008A Simulation Desk MVP planning is merged.
- Task 008B local fixtures, validators, validation matrix/report helper, and tests are merged.
- Task 008C now adds a pure local-only paper-order validation service/stub as the next implementation-limited slice.

## Task 008C Classification

Task 008C is:

- **Implementation-limited** — it adds local validation helpers and tests only.
- **Governance-sensitive** — it touches Simulation Desk paper-order intent boundaries near locked schema/API names.
- **Pure local-only** — it performs in-memory validation only and does not enable runtime infrastructure.

## Explicit Task 008C Decision

Task 008C remains pure local-only.

It introduces a reviewed local service/stub surface only through `backend/app/simulation_order_validation.py`. It does not introduce a public endpoint runtime surface and does not implement `POST /api/v1/simulation/paper-orders`.

This decision does not authorize endpoint runtime, persistence, production Supabase, broker integration, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, or real-money trading automation.

## Relationship to `docs/04` Operating Rules

`docs/04-simulation-investment-desk.md` requires paper simulation to remain learning-and-validation oriented, visible, reviewable, and human-governed. Task 008C supports that direction by validating paper-order intents before any future runtime work, while preserving the following boundaries:

- historical simulation outcomes must not be hidden or rewritten;
- simulation outputs should lead to reviewable proposals, not silent behavior changes;
- paper validation must not become real-money execution;
- all real-money decisions remain human-owned.

Task 008C validates the intent shape only. It does not fill, submit, execute, store, or report an order.

## Relationship to `docs/08` Schema References

`docs/08-supabase-schema-design.md` defines `paper_portfolios` as paper-only portfolio containers and `paper_orders` as simulation paper order intents and lifecycle events.

Task 008C references those schema concepts without creating database records:

- `portfolio_id` is required because `paper_orders` is linked to `paper_portfolios`.
- `symbol` is required as the local stock identifier input for this stub.
- `side`, `order_type`, `quantity`, and `limit_price` follow the `paper_orders` intent fields.
- `quantity` must be non-negative.
- `limit_price`, when present, must be non-negative.
- `paper_orders` is referenced as a canonical schema table name, but no migration, database table access, insert, update, or persistence path is added.

Because symbol validation is not centralized yet, Task 008C uses a conservative local HK ticker check: four digits followed by `.HK`, for example `0700.HK`.

## Relationship to `docs/09` Locked Endpoint Names

`docs/09-api-and-agent-contracts.md` locks `POST /api/v1/simulation/paper-orders` as an MVP endpoint name.

Task 008C references that locked endpoint name in validation results for traceability only. It does not implement the endpoint, add a FastAPI route, add request/response handling, alter the public analyze-stock payload, or change `docs/09-api-and-agent-contracts.md`.

## Validation Behavior and Boundary Flags

The local validation service accepts paper-order-intent-like mappings and validates:

| Field | Validation |
|---|---|
| `portfolio_id` | Required, non-empty string. If a local registry is supplied, the portfolio id must exist in that registry. |
| `symbol` | Required, non-empty, conservative HK style such as `0700.HK`. |
| `side` | Required; must be `buy` or `sell`. |
| `quantity` | Required numeric value; must be non-negative. |
| `order_type` | Optional; defaults to `market`; when present must be `market` or `limit`. |
| `limit_price` | Optional; when present must be numeric and non-negative. |

The service returns a local validation result/report that states no paper order is created. These boundary flags must remain false whether supplied at the top level or, where applicable, through a nested `boundary_flags` mapping:

- `io_enabled`
- `http_enabled`
- `database_write_enabled`
- `persistence_enabled`
- `production_supabase_required`
- `production_supabase_connected`
- `endpoint_runtime_enabled`
- `paper_order_created`
- `broker_execution_enabled`
- `real_money_order_placed`
- `real_money_trading_automation_enabled`
- `external_api_required`
- `secrets_required`

Inputs implying actual order creation, such as `would_create_order=true`, `create_order=true`, `paper_order_created=true`, `execute_order=true`, `submit_order=true`, or `place_order=true`, fail validation.

## Test Coverage Matrix

| Coverage area | Test coverage |
|---|---|
| Valid local paper-order intent | Passing validation test. |
| Market buy | Passing validation test. |
| Market sell | Passing validation test. |
| Limit order | Passing validation test. |
| Zero quantity | Passing validation test for `paper_order_intent`. |
| Local portfolio registry match | Passing validation test. |
| No order creation result | Asserts `would_create_order=false` and `paper_order_created=false`. |
| No endpoint runtime result | Asserts `endpoint_runtime_enabled=false` and `http_enabled=false`. |
| Non-mutating validation | Deep-copy comparison around validation/report helper. |
| Missing required fields | Negative tests for missing `portfolio_id` and `symbol`. |
| Registry mismatch | Negative test for unknown `portfolio_id` when registry is supplied. |
| Malformed symbol | Negative test for non-`0700.HK` style symbol. |
| Invalid enums | Negative tests for invalid `side` and `order_type`. |
| Invalid numeric values | Negative tests for negative `quantity` and `limit_price`. |
| Forbidden boundary flags | Negative tests for endpoint, persistence, database write, production Supabase, broker, real-money, external API, and secrets flags. |
| Actual order creation implication | Negative tests for input fields that imply creating, placing, submitting, or executing an order. |

## Explicit Non-Goals

Task 008C does not add:

- `POST /api/v1/simulation/paper-orders` endpoint implementation;
- `GET /api/v1/paper-portfolios/{portfolio_id}` endpoint implementation;
- `POST /api/v1/strategy-recommendations` endpoint implementation;
- public analyze-stock payload changes;
- public handoff preview exposure;
- `docs/09-api-and-agent-contracts.md` changes;
- schema migrations;
- `supabase/migrations` changes;
- Supabase clients;
- production Supabase connections;
- persistence writes;
- database writes;
- paper order creation;
- paper portfolio runtime;
- strategy recommendation persistence;
- audit event database creation;
- live market data;
- external APIs;
- broker APIs;
- autonomous order placement;
- secrets or API keys;
- real-money trading automation;
- frontend/UI;
- report output.

## Task 008D Entry Criteria

Task 008D may begin only after Harness Engineering confirms the next safe Simulation Desk slice. At minimum, Task 008D should enter with:

1. Task 008C tests passing locally and in CI.
2. Confirmation that `docs/09-api-and-agent-contracts.md` remains unchanged unless Task 008D explicitly proposes a public contract change.
3. A clear Task 008D objective stating whether it remains local-only or proposes a reviewed runtime surface.
4. Explicit approval before any endpoint runtime, persistence, production Supabase, broker integration, paper-order creation, or real-money-adjacent capability.
5. Same-PR updates to affected docs, tests, decision logs, progress logs, and status files if Task 008D changes scope.

If Task 008D proposes endpoint runtime, persistence, production Supabase, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, broker integration, or real-money trading automation, it requires explicit Harness Engineering approval before implementation.
