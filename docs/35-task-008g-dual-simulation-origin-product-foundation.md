# 35 — Task 008G Dual Simulation Origin Product Foundation

## Purpose

Task 008G formally aligns the Simulation Investment Desk product contract and schema foundation around two distinct paper-only simulation-origin pipelines before endpoint runtime and persistence writes are implemented.

## Source-of-Truth Reviewed

Task 008G reviewed the project governance, Simulation Desk, schema, API, workflow, PR Factory, evidence-closure, Task 008F, logs, local Simulation Desk helpers/tests, draft migration baseline, migration assumptions, and contract validator source-of-truth listed in the task request.

## Current Project Position

- Task 008 / M5 remains **In Progress**.
- Task 008F established local scenario pack and gate decision matrix evidence.
- Task 008G opens the next non-real-money productization gate for contract/schema alignment and local-only validation.
- M5 is not complete, and runtime endpoint/persistence implementation remains deferred.

## Harness Engineering Approval Summary

Harness Engineering approved opening non-real-money productization gates after Task 008F. Approved gates include schema/contract alignment, local/test migration planning, persistence design, endpoint runtime planning, paper-trading recordkeeping, system-generated learning simulations, audit events, and future non-real-money product runtime sequencing.

The approval does not authorize real-money trading, autonomous real-money execution, broker execution APIs for autonomous order placement, production Supabase connection, secrets, deployment, live market data, or silent auto-application of learning proposals.

## User Story

As Harness Engineering, I need HK Alpha Team to distinguish human-recorded paper trades from system-generated learning simulations so that paper-trade records, recommendation validation, reviewable learning proposals, and audit evidence remain clear, safe, and reviewable.

## Product Concept

HK Alpha Team is an AI-assisted Hong Kong equity research and investment strategy advisory system. The Simulation Investment Desk is not only a paper-order journal; it is also a learning and validation desk that runs paper-trading simulations from approved recommendation packets and produces reviewable learning proposals.

## Two Simulation-Origin Pipelines

### `user_recorded`

- **Origin:** Human user / Harness Engineering / user.
- **Purpose:** Record user-entered paper trading decisions and outcomes.
- **Required records:** User/source metadata, user-recorded notes, user rationale, optional linked recommendation, paper order/position fields, trade review fields, and audit provenance.
- **Learning impact:** May support later reviewed lessons, but does not imply AI-generated learning unless explicitly linked.

### `system_generated_learning`

- **Origin:** Simulation Investment Desk / HK Alpha Team system.
- **Purpose:** Validate strategy recommendation quality through disciplined paper trading and post-outcome review.
- **Required records:** Original recommendation linkage, original scores, original thesis, entry/exit assumptions, PnL, holding period, what worked, what failed, improvement suggestions, system learning reason, learning proposal linkage where applicable, and audit provenance.
- **Learning impact:** May create reviewable learning proposals but must not silently alter production strategy logic.

## Schema Impact

Task 008G documents additive schema semantics while preserving canonical table names:

- `paper_orders`: primary origin-bearing record with `simulation_origin` / `paper_order_origin`, `created_by_type`, recommendation linkage, user notes, system-learning reason, `requires_human_review`, and `learning_proposal_id` where applicable.
- `strategy_recommendations`: append-only source recommendation lineage for system-generated learning simulations and optional human-linked paper trades.
- `paper_portfolios`: may hold both origins, but reporting must preserve origin attribution.
- `paper_positions`: inherit origin from opening paper order.
- `portfolio_snapshots`: may aggregate portfolio performance while retaining origin summary metadata.
- `trade_reviews`: preserve user notes for `user_recorded` records and learning review fields for `system_generated_learning` records.
- `learning_proposals`: reviewable only; `auto_apply` must remain false.
- `audit_events`: append-only origin, actor, entity, and boundary evidence.

## API Contract Impact

Task 008G preserves locked endpoint names and the required response envelope. `POST /api/v1/simulation/paper-orders` supports `simulation_origin` values:

- `user_recorded`
- `system_generated_learning`

The API contract must emit warnings/metadata confirming paper-only advisory scope, human-in-the-loop control, no real-money order placement, no broker execution API call, no autonomous real-money execution, no production Supabase connection unless separately approved, and no secrets required.

## Validation Behavior

Local validation must prove:

- Only `user_recorded` and `system_generated_learning` are valid origins.
- `user_recorded` payloads require user/source fields and notes.
- `system_generated_learning` payloads require original recommendation, thesis, score, assumptions, PnL, holding-period, review, and learning fields.
- `requires_human_review` remains true for system-learning learning proposals, including nested learning-proposal references.
- `proposals_reviewable` and `proposals_auto_applied` must be explicitly present, with `proposals_reviewable = true` and `proposals_auto_applied = false`.
- `losing_outcomes_remain_visible` and `historical_recommendations_overwritten` must be explicitly present, with `losing_outcomes_remain_visible = true` and `historical_recommendations_overwritten = false`.
- Real-money, broker execution, production Supabase, and secrets flags must be explicitly present in `boundary_flags` and remain false.
- Validation does not mutate caller-provided payloads.

## Local Helper/Test Scope

Task 008G adds `backend/app/simulation_origin_contract.py` and `backend/tests/test_simulation_origin_contract.py` for deterministic local-only validation. The helper has no IO, endpoint runtime, persistence writes, production Supabase connection, broker API integration, secrets, live data, deployment, or real-money execution behavior.

## Out-of-Scope

- FastAPI endpoint runtime implementation.
- Actual persistence writes.
- Production Supabase connection.
- Secrets or API keys.
- Broker execution APIs.
- Real-money trading.
- Autonomous real-money order placement.
- Live market data integration.
- Production deployment.
- Auto-application of learning proposals.
- Hiding or overwriting losing simulations.
- Renaming canonical table names.
- Renaming locked MVP endpoint names.
- Changing required response envelope fields.
- Removing existing local-only Task 008B–008F behavior.

## Risk Areas

- Future runtime may blur human-recorded and system-generated origins unless origin fields are enforced.
- Learning proposals may be misinterpreted as auto-applied strategy changes unless review flags remain mandatory.
- Aggregated portfolio reporting may hide losing simulations unless origin and outcome visibility rules are preserved.
- Schema/API additions must remain additive and must not rename locked contract surfaces.

## Task 008H Entry Criteria

Task 008H may begin only after Task 008G evidence confirms:

1. Source-of-truth docs align on the dual-origin product concept.
2. Schema and API contract docs preserve locked names/envelope while documenting additive origin fields.
3. Local validation helper and tests pass for both origins and boundary failures.
4. Real-money trading, autonomous execution, broker execution APIs, production Supabase, secrets, deployment, live market data, and auto-applied learning remain out of scope.
5. Task 008 / M5 remains In Progress and M5 is not claimed complete.
