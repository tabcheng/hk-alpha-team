# 29 — Task 008B Local Simulation Contract Fixtures, Schemas, and Validation Matrix

## Objective

Implement Task 008B — Local-only Simulation Contract Fixtures, Schemas, and Validation Matrix.

Task 008B moves the Simulation Desk MVP from Task 008A planning into an implementation-limited local contract validation slice. It adds deterministic local fixtures and pure validation helpers for the seven canonical Simulation Desk record shapes without adding runtime behavior, persistence, production Supabase, endpoint handlers, broker integration, paper order creation, or real-money trading automation.

## Scope Classification

Task 008B is **implementation-limited, pure, and local-only**.

The allowed implementation surface is limited to:

- a pure local simulation contract module;
- deterministic fixtures for all seven canonical Simulation Desk record shapes;
- validation helpers for individual records and full fixture collections;
- a validation matrix/report helper for coverage and boundary compliance;
- positive and negative tests proving fixture, schema-reference, boundary-flag, and non-mutation behavior.

Task 008B does not change public API behavior and does not modify `docs/09-api-and-agent-contracts.md`.

## Pure Local-Only Helper Boundary

All Task 008B helpers must remain pure local contract helpers.

They must not perform or require:

- IO;
- HTTP;
- database access;
- Supabase access;
- endpoint handlers;
- paper order creation;
- persistence;
- broker integration;
- real-money trading automation.

The fixture and validation module uses deterministic in-memory dictionaries only. It does not import FastAPI, Supabase clients, HTTP clients, file-system helpers, or broker/execution integrations. Fixture records use isolated mutable lists/dictionaries so one fixture cannot accidentally mutate another fixture's endpoint references or boundary flags.

## Canonical Fixture Coverage

Task 008B covers one deterministic fixture for each required Simulation Desk record type:

| Required record type | Canonical schema table reference | Coverage intent |
|---|---|---|
| `paper_portfolio` | `paper_portfolios` | Paper-only portfolio container shape. |
| `paper_order_intent` | `paper_orders` | Paper order intent shape only; no order is created or submitted. |
| `paper_position` | `paper_positions` | Simulated closed position shape with a visible losing outcome. |
| `portfolio_snapshot` | `portfolio_snapshots` | Paper portfolio valuation/risk snapshot shape. |
| `trade_review` | `trade_reviews` | Post-trade review shape with loss visibility and learning notes. |
| `learning_proposal` | `learning_proposals` | Reviewable proposal shape that is not auto-applied. |
| `audit_event` | `audit_events` | Local fixture audit-event shape only; no persisted audit event is created. |

The singular local record types are fixture categories. The plural table names remain canonical schema references and are not renamed.

## Locked Endpoint Reference Coverage

Task 008B references the locked endpoint names needed by future Simulation Desk work without implementing endpoint runtime:

- `POST /api/v1/simulation/paper-orders`
- `GET /api/v1/paper-portfolios/{portfolio_id}`
- `POST /api/v1/strategy-recommendations`
- `GET /api/v1/strategy-recommendations/{recommendation_id}`

These strings are validation references only. Task 008B does not add route handlers, HTTP calls, request parsing, response generation, persistence, or paper-order runtime.

## Validation Matrix Coverage

The Task 008B validation matrix/report helper must show the following coverage:

| Coverage item | Required Task 008B result |
|---|---|
| All expected record types are present. | `paper_portfolio`, `paper_order_intent`, `paper_position`, `portfolio_snapshot`, `trade_review`, `learning_proposal`, and `audit_event` are all covered. |
| Canonical schema names are referenced without renaming. | Fixture categories map to the locked plural schema table names. |
| Locked endpoint names are referenced without implementation. | Endpoint strings are covered as references only. |
| Losing outcomes remain visible. | The losing `paper_position` and `trade_review` fixtures keep `losing_outcome_visible = true`. |
| Learning proposals are reviewable and not auto-applied. | The `learning_proposal` fixture keeps `reviewable = true` and `auto_applied = false`. |
| No persistence flags are enabled. | `persistence_enabled = false` and related local-only flags remain false. |
| No production Supabase flags are enabled. | `production_supabase_required = false` and `production_supabase_connected = false`. |
| No broker or real-money flags are enabled. | `broker_execution_enabled = false` and `real_money_order_placed = false`. |
| No endpoint runtime flag is enabled. | `endpoint_runtime_enabled = false`. |
| Validation does not mutate inputs. | Validators self-check deep copies, and tests compare inputs before and after validation/report generation. |

## Required Test Coverage

Task 008B test coverage includes positive and negative cases for the required record types and boundary flags:

- valid fixture per record type passes;
- full fixture collection passes;
- fixture report contains all expected record types and boundary flags;
- missing required field fails;
- unknown record type fails;
- invalid quantity fails;
- invalid status fails;
- hidden losing outcome fails;
- auto-applied learning proposal fails;
- `persistence_enabled = true` fails;
- `production_supabase_required = true` fails;
- `broker_execution_enabled = true` fails;
- `real_money_order_placed = true` fails;
- `endpoint_runtime_enabled = true` fails;
- validation does not mutate inputs.

## Non-Goals

Task 008B explicitly does not add:

- IO;
- HTTP;
- database reads or writes;
- Supabase clients;
- endpoint handlers;
- paper order creation;
- persistence;
- broker integration;
- real-money trading automation;
- live market data;
- production deployment;
- public API payload changes;
- schema migrations.

## Task 008C Entry Criteria

Task 008C may begin only after Harness Engineering confirms the next safe Simulation Desk slice. At minimum, Task 008C should enter with:

1. Task 008B tests passing in local/CI pytest.
2. The local fixture matrix preserving all seven required record types.
3. Canonical schema names and locked endpoint names still referenced without renaming.
4. Boundary flags still proving no persistence, production Supabase, endpoint runtime, broker execution, real-money order placement, or real-money trading automation.
5. A defined Task 008C objective stating whether the next slice remains pure local-only or introduces a reviewed runtime surface.
6. Same-PR updates to `docs/decision-log.md`, `docs/progress-log.md`, `docs/11-project-status.md`, and any affected contract/source-of-truth docs if Task 008C changes scope.

If Task 008C proposes persistence, endpoint runtime, production Supabase, paper-order creation, broker integration, or any real-money-adjacent capability, it requires explicit Harness Engineering approval and same-PR contract/runtime/test/governance updates before implementation.

## Review Checklist for Task 008B

- The implementation is pure and local-only.
- All seven required Simulation Desk record types have deterministic fixtures.
- Validation rejects malformed shapes, invalid quantities/statuses, hidden losses, auto-applied learning proposals, and enabled boundary flags.
- The validation matrix proves fixture coverage and boundary compliance.
- Tests prove validation does not mutate inputs.
- Fixture records do not share mutable boundary-flag or endpoint-reference objects.
- No endpoint handler, persistence, Supabase, broker, paper-order creation, or real-money trading automation was added.
