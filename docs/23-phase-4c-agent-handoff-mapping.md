# 23 — Phase 4C Agent Handoff Mapping

## Purpose

Phase 4C starts the next implementation-limited step inside Task 007 / Milestone M4 by defining a deterministic local-only handoff mapping from Phase 4B department adapter outputs to future `agent_runs` / `agent_outputs` preview shapes.

This phase documents and tests how the current adapter outputs would be prepared for a later persistence-backed agent-run layer after Harness Engineering explicitly authorizes persistence and endpoint runtime work in a future PR.

## Relationship to Phase 4B Department Adapters

Phase 4B produces one local-only adapter output for each HK Alpha Team department:

1. Market Intelligence Agent
2. Company Research Agent
3. News & Sentiment Agent
4. Technical Analysis Agent
5. Risk Manager Agent
6. Investment Committee Agent
7. Simulation Investment Desk
8. Investment Strategy Office

Those adapter outputs already mirror the locked common agent output shape in `docs/09-api-and-agent-contracts.md`. Phase 4C does not change the public analyze-stock response. Instead, it adds an internal mapping layer that can transform those adapter outputs into reviewable future-run and future-output previews without treating them as real database records.

## Future `agent_runs` Preview Fields

Each handoff preview includes a `future_agent_run_preview` object with these fields:

- `run_uuid_preview`
- `department_name`
- `request_payload_preview`
- `status_preview`
- `started_at_preview`
- `finished_at_preview`
- `error_code_preview`
- `stock_symbol`
- `stock_id_preview`
- `recommendation_id_preview`
- `persistence_status`
- `persistence_allowed`

`run_uuid_preview` is a deterministic preview-only identifier derived locally from the normalized stock symbol and department name. It is not a database primary key and must not be interpreted as a persisted `agent_runs.id` value.

## Future `agent_outputs` Preview Fields

Each handoff preview includes a `future_agent_output_preview` object with these fields:

- `agent_run_id_preview`
- `department_name`
- `output_json_preview`
- `confidence`
- `created_at_preview`
- `agent_output_persistence_status`

`output_json_preview` preserves the locked common agent output shape:

- `agent_name`
- `agent_version`
- `stock_symbol`
- `input_summary`
- `evidence`
- `score`
- `confidence`
- `key_findings`
- `risks`
- `invalidation_conditions`
- `generated_at`
- `schema_version`

## Unresolved Identifier Handling

Phase 4C makes unresolved persistence identifiers explicit:

- `stock_id_preview = null`
- `recommendation_id_preview = null`
- `agent_run_id_preview = null`

These null values are intentional. The handoff layer must not imply that a production `stocks` row exists, that a strategy recommendation exists, or that an `agent_runs` row has been inserted.

## Current Non-Persistent Runtime State

Each handoff preview also includes `current_runtime_state` so reviewers can distinguish current local runtime behavior from future persistence intent.

The runtime state records that:

- no database write occurred;
- no production Supabase connection occurred;
- no persisted agent run was created;
- no persisted agent output was created;
- no strategy recommendation was created;
- no audit event was created;
- no paper order was created;
- no broker execution occurred;
- no real-money order was placed.

Persistence-related status values remain explicit and conservative:

- `PREVIEW_ONLY`
- `NOT_PERSISTED`
- `PERSISTENCE_NOT_AUTHORIZED`

## No-Persistence Boundary

Phase 4C performs no persistence writes. It does not create or update records in:

- `agent_runs`
- `agent_outputs`
- `strategy_recommendations`
- `paper_orders`
- `audit_events`
- any other production table

The mapping is deterministic local metadata only.

## No-Production-Supabase Boundary

Phase 4C does not add a Supabase client, database session, environment secret requirement, migration, or production database connection.

The preview layer does not read from or write to production Supabase and does not require network access.

## No-Agent-Runs-Endpoint-Implementation Boundary

Phase 4C does not implement `GET /api/v1/agent-runs/{agent_run_id}`.

The preview shape is a planning and validation bridge for future reviewed work only. It is not an endpoint response contract and is not a retrieval runtime.

## No-Strategy-Recommendation-Persistence Boundary

Phase 4C does not implement `POST /api/v1/strategy-recommendations` and does not create `strategy_recommendations` records.

The existing analyze-stock advisory label remains local deterministic workflow output and does not become a persisted recommendation.

## Advisory-Only and Human-in-the-Loop Framing

Phase 4C keeps HK Alpha Team advisory-only and human-in-the-loop.

The handoff mapping must not imply:

- live market research;
- production-quality equity analysis;
- autonomous strategy approval;
- paper-order creation;
- broker execution;
- real-money trading automation.

All real-money decisions remain manual Harness Engineering decisions outside the application.

## Validation Approach

Phase 4C validation covers:

- all eight Phase 4B department outputs produce eight handoff previews;
- future run-level preview fields are present;
- future output-level preview fields are present;
- `output_json_preview` preserves the locked common agent output shape;
- department names match adapter output `agent_name` values;
- unresolved persistence identifiers remain null;
- `persistence_allowed` is false;
- persistence statuses state preview-only / not-persisted / not-authorized behavior;
- runtime state does not claim database writes, production Supabase connection, persisted agent runs, persisted agent outputs, strategy recommendation records, or audit events;
- stable mapping fields are deterministic for the same symbol and adapter outputs;
- malformed adapter outputs raise local contract violations.

Required validation commands remain:

```bash
python scripts/validate_contracts.py
PYTHONPATH=backend pytest backend/tests -q
git diff --check
```

## Phase 4D Follow-Up Path

Phase 4D can build on this handoff layer only through a separately reviewed and explicitly authorized task.

Potential future work includes:

- deciding whether handoff previews should remain internal or become public review metadata;
- designing the reviewed `GET /api/v1/agent-runs/{agent_run_id}` runtime when endpoint implementation is authorized;
- adding persistence-backed `agent_runs` / `agent_outputs` creation only after production Supabase and write boundaries are approved;
- adding strategy recommendation persistence only after `POST /api/v1/strategy-recommendations` is explicitly authorized;
- keeping all live market data, paper order, broker execution, and real-money trading scope out until separately approved.
