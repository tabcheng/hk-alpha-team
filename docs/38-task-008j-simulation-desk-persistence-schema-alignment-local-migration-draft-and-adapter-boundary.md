# 38 — Task 008J Simulation Desk Persistence Schema Alignment, Local Migration Draft, and Adapter Boundary

## Purpose

Task 008J moves the Task 008I in-memory Simulation Desk runtime one safe step closer to durable persistence by aligning runtime records with the future persistence schema, drafting an additive local/test-only migration, and introducing a local-only persistence-intent adapter boundary.

This task intentionally stops before any real persistence path. It does not connect Supabase, does not add a Supabase client, does not write to a database or disk, does not call vendors or external APIs, and does not enable real-money trading or autonomous execution.

## Source-of-Truth Reviewed

The Task 008J implementation was prepared against these source-of-truth files:

- `AGENTS.md`
- `README.md`
- `docs/04-simulation-investment-desk.md`
- `docs/08-supabase-schema-design.md`
- `docs/09-api-and-agent-contracts.md`
- `docs/10-mvp-implementation-plan.md`
- `docs/11-project-status.md`
- `docs/15-migration-assumptions.md`
- `docs/20-codex-pr-factory.md`
- `docs/32-pr-review-evidence-closure-protocol.md`
- `docs/35-task-008g-dual-simulation-origin-product-foundation.md`
- `docs/36-commercial-readiness-and-subscription-product-governance.md`
- `docs/37-task-008i-dual-origin-simulation-desk-runtime-slice.md`
- `docs/decision-log.md`
- `docs/progress-log.md`
- `docs/lessons-learned.md`
- `backend/app/main.py`
- `backend/app/contracts.py`
- `backend/app/simulation_origin_contract.py`
- `backend/app/simulation_runtime.py`
- `backend/app/simulation_store.py`
- Simulation runtime/origin tests
- `supabase/migrations/0001_create_core_schema.sql`
- `scripts/validate_contracts.py`
- Existing SQL migration validation workflow files

## Current Project Position

Task 008 / M5 remains **In Progress**. Task 008G adopted the dual simulation-origin model, Task 008H recorded commercial-readiness governance, and Task 008I added non-production in-memory endpoint runtime for:

- `POST /api/v1/simulation/paper-orders`
- `GET /api/v1/paper-portfolios/{portfolio_id}`

Task 008J adds schema alignment and intent payloads only. It does **not** convert the runtime into durable persistence.

## User Story

As Harness Engineering, I want a persistence schema alignment, local migration draft, and adapter boundary for the Simulation Desk runtime so that Task 008I in-memory records can be safely mapped to future database tables before any real Supabase write path is approved.

## Why 008J Is Larger Than a Docs-Only Task

Task 008J is implementation-limited rather than documentation-only because future persistence cannot be reviewed safely from prose alone. The task adds:

1. A local/test-only additive SQL migration draft to make schema gaps executable in CI/local validation.
2. A local-only adapter module that transforms runtime records into deterministic persistence-intent payloads.
3. Tests proving both approved origins, boundary flags, reviewable learning proposals, append-only audit previews, and loss-visibility guardrails are preserved without writes.

The adapter boundary is intentionally not a database adapter. It is a pre-persistence contract that shows what would be written later if a future PR explicitly approves a Supabase adapter.

## Schema Mapping Table

| Runtime concept | Future persistence target | Task 008J mapping intent | Notes |
|---|---|---|---|
| In-memory paper order record | `paper_orders` | Maps order fields, origin, actor, recommendation lineage, source metadata, outcome preview, boundary flags, and learning/loss guardrails. | Intent payload only; no write. |
| In-memory paper portfolio snapshot | `paper_portfolios` / `portfolio_snapshots` | Keeps runtime portfolio identity and maps snapshot preview metadata to `portfolio_snapshots.simulation_origin_summary_json`. | `paper_portfolios` remains canonical portfolio state; Task 008J does not create portfolio rows. |
| Runtime order-derived position implications | `paper_positions` | Adds `simulation_origin` to support future position records that preserve whether the paper exposure came from `user_recorded` or `system_generated_learning`. | No position runtime is created in 008J. |
| Runtime learning proposal preview | `learning_proposals` | Maps source recommendation lineage, origin, `requires_human_review = true`, `auto_apply = false`, reason, and suggestions. | Preview remains reviewable and not applied. |
| Runtime audit event preview | `audit_events` | Maps preview as append-only intent metadata with `simulation_origin`. | No audit row is inserted. |
| Runtime review/loss details | `trade_reviews` | Adds fields for origin, notes/reason, what worked/failed JSON, improvement suggestions, and human-review requirement. | Trade reviews remain future runtime. |

## Runtime-to-Persistence Field Map

| Runtime field / behavior | `paper_portfolios` | `paper_orders` | `paper_positions` | `portfolio_snapshots` | `trade_reviews` | `learning_proposals` | `audit_events` |
|---|---|---|---|---|---|---|---|
| `portfolio_id` | Future lookup/identity bridge | Runtime portfolio reference | Future FK-derived context | Snapshot portfolio reference | Review context through position/order | Source context through proposal payload | Entity payload context |
| `paper_order_id` | N/A | Runtime identifier carried in intent metadata | Future `opened_from_order_id` lineage bridge | Recent order summary | Review order lineage | Source payload lineage | `entity_id` in preview payload |
| `simulation_origin` | Portfolio may aggregate mixed origins | `simulation_origin`, `paper_order_origin` | `simulation_origin` | `simulation_origin_summary_json` | `simulation_origin` | `simulation_origin` | `simulation_origin` |
| `created_by_type` | N/A | `created_by_type` | Future actor metadata | Summary metadata | Reviewer/actor context | Source actor context | `actor_type` |
| `source_recommendation_id` | N/A | `source_recommendation_id` | Future position lineage | Summary metadata | Review lineage | `source_recommendation_id` | Event payload metadata |
| `strategy_recommendation_id` | N/A | Existing canonical FK remains; runtime string is preserved as lineage metadata until FK resolution is approved. | Future position lineage | Summary metadata | Review lineage | Source payload lineage | Event payload metadata |
| `user_recorded_notes` | N/A | `user_recorded_notes`, `source_metadata_json` | Future notes context | Summary metadata | `user_recorded_notes` | N/A | Event payload metadata |
| `system_learning_reason` | N/A | `system_learning_reason`, `source_metadata_json` | Future learning context | Summary metadata | `system_learning_reason` | Proposal reason/payload | Event payload metadata |
| `learning_proposal_preview` | N/A | `learning_proposal_id` preview bridge | N/A | Summary metadata | Improvement context | Reviewable `learning_proposals` intent | Event payload metadata |
| `audit_event_preview` | N/A | N/A | N/A | Snapshot audit preview count | Review audit context | Proposal audit context | Append-only `event_payload_json` intent |
| `outcome_preview` | N/A | `outcome_preview_json` | Future realized/unrealized outcome context | Summary metadata | Future outcome review context | Learning evidence payload | Event payload metadata |
| `boundary_flags` | Governance metadata | `boundary_flags_json` | Future boundary metadata | Snapshot boundary metadata | Review boundary metadata | Proposal boundary metadata | Event payload metadata |

## Origin Coverage

Task 008J preserves both approved origins exactly:

- `user_recorded`
- `system_generated_learning`

The local boundary rejects unknown origins and keeps the origin visible in every generated persistence-intent payload.

## Boundary Field Coverage

Task 008J maps and validates the following boundary fields before producing persistence-intent payloads:

| Field | Required safe value | Intent behavior |
|---|---:|---|
| `paper_only` | `true` | Included in every payload. |
| `advisory_only` | `true` | Included in every payload. |
| `human_in_the_loop` | `true` | Included in every payload. |
| `real_money_order_placed` | `false` | Rejected if true. |
| `real_money_trading_automation_enabled` | `false` | Rejected if true. |
| `autonomous_real_money_execution` | `false` | Rejected if true. |
| `broker_execution_enabled` | `false` | Rejected if true. |
| `broker_api_called` | `false` | Rejected if true. |
| `production_supabase_connected` | `false` | Rejected if true; payload also states false. |
| `persistence_write_performed` | `false` | Rejected if true; payload also states false. |
| `secrets_required` | `false` | Rejected if true. |
| `external_api_called` | `false` | Rejected if true. |
| `billing_runtime_enabled` | `false` | Rejected if true. |
| `membership_runtime_enabled` | `false` | Rejected if true. |
| `auth_runtime_enabled` | `false` | Rejected if true. |
| `deployment_required` | `false` | Rejected if true. |

## Learning and Loss Guardrail Coverage

| Guardrail | Required safe value | Task 008J behavior |
|---|---:|---|
| `proposals_reviewable` | `true` | Included in payloads; rejected if false. |
| `proposals_auto_applied` | `false` | Included in payloads; rejected if true. |
| `losing_outcomes_remain_visible` | `true` | Included in payloads; rejected if false. |
| `historical_recommendations_overwritten` | `false` | Included in payloads; rejected if true. |

## Identified Gaps Between 0001 Migration and Task 008I Runtime

The existing `0001_create_core_schema.sql` creates the canonical simulation tables but does not yet fully encode the Task 008G/008I runtime semantics:

| Table | 0001 gap | 008J local/test-only bridge |
|---|---|---|
| `paper_orders` | No explicit dual-origin fields, created-by type, source recommendation text lineage, user-recorded notes, system learning reason, human-review flag, learning-proposal preview bridge, boundary flag JSON, outcome preview JSON, or source metadata JSON. | `0002` additively drafts these columns. |
| `paper_positions` | No explicit `simulation_origin`. | `0002` additively drafts `simulation_origin`. |
| `portfolio_snapshots` | No origin summary for mixed-origin runtime snapshots. | `0002` additively drafts `simulation_origin_summary_json`. |
| `trade_reviews` | Does not carry explicit origin, user/system notes, improvement suggestions, or human-review requirement aligned to runtime learning previews. | `0002` additively drafts these fields while preserving existing review JSON columns. |
| `learning_proposals` | No source recommendation text lineage, origin, required human-review flag, or explicit non-auto-apply field. | `0002` additively drafts these fields and constrains `auto_apply` false in the local/test draft. |
| `audit_events` | No first-class `simulation_origin` column. | `0002` additively drafts `simulation_origin`; existing `event_payload_json` remains append-only metadata carrier. |

## Local/Test-Only Migration Draft Boundary

`supabase/migrations/0002_align_simulation_desk_persistence_fields.sql` is a local/test-only additive migration draft. It may be executed by local/CI SQL validation after `0001`, but it is not approved for production Supabase.

The draft:

- Adds columns only.
- Adds indexes only.
- Does not rename canonical tables.
- Does not drop columns.
- Does not backfill production data.
- Does not connect production Supabase.
- Does not require secrets.
- Does not authorize runtime persistence writes.

## Adapter Boundary Design

`backend/app/simulation_persistence_boundary.py` creates deterministic persistence-intent payloads for future table targets:

- `build_paper_order_persistence_payload()`
- `build_audit_event_persistence_payload()`
- `build_learning_proposal_persistence_payload()`
- `build_portfolio_snapshot_persistence_payload()`
- `build_persistence_payload_bundle()`

Every payload includes:

- `persistence_intent_only = true`
- `persistence_write_performed = false`
- `production_supabase_connected = false`
- `generated_from_runtime_record = true`
- `target_table`
- `simulation_origin`
- `paper_only = true`
- `advisory_only = true`
- `human_in_the_loop = true`

The module contains no database client, no Supabase import, no external API call, no disk write, and no secret requirement.

## Validation Strategy

Task 008J is validated through:

1. Contract validation: `python scripts/validate_contracts.py`
2. Targeted boundary tests: `PYTHONPATH=backend pytest backend/tests/test_simulation_persistence_boundary.py -q`
3. Existing Simulation Desk runtime tests: `PYTHONPATH=backend pytest backend/tests/test_simulation_runtime.py -q`
4. Full backend test suite: `PYTHONPATH=backend pytest backend/tests -q`
5. SQL migration validation: local/test PostgreSQL execution of migrations in lexical order (`0001`, then `0002`) via `scripts/check_migration_sql.sh` where PostgreSQL is available.
6. Diff hygiene: `git diff --check`

## Out of Scope

Task 008J does not add or approve:

- Production Supabase connection
- Supabase client runtime
- Database writes
- Disk persistence
- Vendor SDKs
- Vendor/API calls
- Live market data
- Broker integration or broker execution APIs
- Billing/payment runtime
- Membership/subscription runtime
- Authentication runtime
- Deployment config
- Frontend/UI
- Secrets
- Real-money trading
- Autonomous real-money execution
- Auto-applied learning proposals
- Hidden losing outcomes
- Overwritten historical recommendations
- Renamed locked endpoints, response envelope fields, MVP phase names, or canonical schema tables

## Risk Areas

- A future implementation could mistakenly treat persistence-intent payloads as completed writes. The payloads explicitly state `persistence_intent_only = true` and `persistence_write_performed = false` to prevent that confusion.
- Future FK resolution must decide how runtime string lineage maps to UUID-backed canonical tables without losing auditability.
- The local/test-only `0002` draft must not be applied to production Supabase without a separate explicit PR, Evidence Closure, and Harness Engineering approval.
- Future persistence must preserve both origins, learning guardrails, audit lineage, and losing outcome visibility together; partial persistence would be unsafe.

## Task 008K Entry Criteria

A future Task 008K may only start after:

1. Task 008J tests and migration validation pass locally/CI.
2. Harness Engineering explicitly approves the next persistence scope.
3. Evidence Closure identifies the latest reviewed head SHA, CI status, changed files, and unresolved review-thread status.
4. The future PR states whether it is still intent-only or introduces a real local/test persistence write path.
5. Any Supabase adapter remains separately scoped and must not be introduced implicitly.
6. Real-money trading, broker execution APIs, autonomous real-money execution, production vendor/API connections, and secrets remain prohibited unless an explicit future governance decision changes the boundary.
