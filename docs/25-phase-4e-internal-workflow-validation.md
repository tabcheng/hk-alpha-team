# 25 — Phase 4E Internal Workflow Validation

## Purpose

Phase 4E starts an implementation-limited, local-only validation layer for the first analysis workflow.

Its purpose is to check that the current internal workflow artifacts remain mutually consistent across:

1. **Phase 4A** — the deterministic `POST /api/v1/analyze-stock` workflow payload.
2. **Phase 4B** — deterministic department adapter outputs.
3. **Phase 4C** — local-only adapter-to-agent-run handoff previews.
4. **Phase 4D** — the decision to keep handoff previews internal-only for now.

Phase 4E does **not** change public API semantics, does **not** expose handoff preview metadata in the analyze-stock response, and does **not** add persistence or production infrastructure.

## Relationship to Earlier Phase 4 Work

### Phase 4A

Phase 4A introduced the deterministic first analysis workflow skeleton for `POST /api/v1/analyze-stock`.

Phase 4E validates that this payload still carries the locked local-only workflow markers:

- `analysis_status = "phase4a_skeleton"`
- `workflow_phase = "Phase 4A — Deterministic First Analysis Workflow Skeleton"`

### Phase 4B

Phase 4B introduced deterministic department adapter outputs under `department_outputs`.

Phase 4E validates that the workflow payload includes exactly one output for each of the eight HK Alpha Team departments and that every output follows the locked common agent output shape.

### Phase 4C

Phase 4C introduced internal adapter-to-agent-run handoff previews.

Phase 4E validates that handoff previews can still be built from the workflow payload's `department_outputs`, that exactly eight preview records are produced, and that every preview remains preview-only and non-persistent.

### Phase 4D

Phase 4D decided that Phase 4C handoff previews remain internal-only for now.

Phase 4E preserves that decision by explicitly checking that public analyze-stock payloads do not contain `agent_handoff_preview`, `agent_handoff_previews`, `handoff_preview`, or `handoff_previews` fields.

## Internal Validation Invariants

The Phase 4E validator checks the following internal invariants:

- required analyze-stock payload fields remain present;
- `analysis_status` remains `phase4a_skeleton`;
- `workflow_phase` remains `Phase 4A — Deterministic First Analysis Workflow Skeleton`;
- warnings continue to disclose deterministic skeleton status, Phase 4B adapter preview status, no live investment research, no live market data, no persistence, no production Supabase, no broker execution, and no real-money trading automation;
- `department_outputs` contains exactly one output for each expected HK Alpha Team department;
- every department output follows the locked common agent output shape;
- every department output `stock_symbol` matches the analyze-stock payload `symbol`;
- `scores` remains limited to derived score buckets plus the locked deterministic `score_basis`;
- `score_confidence` remains derived from `build_score_confidence(department_outputs)`;
- `stage_rationales` keys exactly match department names;
- every `stage_rationales[department_name]` value equals the first evidence item from the matching department output;
- required `agent_trace` boundary flags remain `false`;
- Phase 4C handoff previews can be rebuilt from the payload's `department_outputs`;
- handoff previews remain preview-only and non-persistent;
- unresolved persistence identifiers remain `null`;
- internal handoff preview fields remain absent from the public analyze-stock payload.

## Required Analyze-Stock Payload Checks

Phase 4E validates the internal analyze-stock payload without mutating it.

The validation layer checks required payload fields including symbol, status, workflow phase, strategy recommendation, summary, confidence, score fields, rationales, department outputs, agent trace, timestamps, and schema version. It also checks warning disclosures using the current Phase 4A warnings by default or an explicit local warning list supplied by a test/helper caller.

The validator returns a local report only after all invariants pass. If an invariant fails, the validator raises a local `ValueError` identifying the failing boundary.

## Department Output Checks

Phase 4E validates department outputs as local-only Phase 4B adapter preview metadata.

The expected departments remain:

- Market Intelligence Agent
- Company Research Agent
- News & Sentiment Agent
- Technical Analysis Agent
- Risk Manager Agent
- Investment Committee Agent
- Simulation Investment Desk
- Investment Strategy Office

Every department output must follow the locked common agent output shape and must preserve the analyze-stock payload symbol.

## Handoff Preview Checks

Phase 4E rebuilds Phase 4C handoff previews internally from `department_outputs` and checks that:

- exactly eight preview records are produced;
- every preview remains `PREVIEW_ONLY` / non-persistent planning metadata;
- `persistence_allowed = false`;
- `database_write_occurred = false`;
- `production_supabase_connected = false`;
- persisted agent-run and agent-output creation flags remain `false`;
- strategy recommendation, audit event, paper order, broker execution, and real-money order creation flags remain `false`;
- `future_agent_output_preview.output_json_preview` exactly preserves the matching Phase 4B department output;
- unresolved persistence identifiers such as `stock_id_preview`, `recommendation_id_preview`, and `agent_run_id_preview` remain `null`.

## Public Payload Non-Exposure Checks

Phase 4E keeps the Phase 4D public exposure decision intact.

The public analyze-stock response must not include the following keys at the top level or nested inside existing public payload objects:

- `agent_handoff_preview`
- `agent_handoff_previews`
- `handoff_preview`
- `handoff_previews`

Any future public exposure of handoff previews would be a contract-changing PR and would require same-PR updates to runtime code, tests, and `docs/09-api-and-agent-contracts.md`.

## Advisory-Only and Human-in-the-Loop Framing

Phase 4E does not change investment recommendation behavior.

The system remains advisory/reporting-first. Any real-money decision remains with Harness Engineering, and validation reports must not be interpreted as investment advice, trade approval, or autonomous execution authorization.

## No-Persistence Boundary

Phase 4E does not add persistence writes.

It does not create or update:

- `agent_runs`
- `agent_outputs`
- `strategy_recommendations`
- `audit_events`
- paper orders
- portfolio records

## No-Production-Supabase Boundary

Phase 4E does not connect to production Supabase and does not require production Supabase credentials.

The validation path uses local deterministic Python objects only.

## No-Agent-Runs-Endpoint-Runtime Boundary

Phase 4E does not implement runtime behavior for `GET /api/v1/agent-runs/{agent_run_id}`.

The handoff preview validation remains internal preparation for possible future endpoint work, not endpoint implementation.

## No-Strategy-Recommendation-Persistence Boundary

Phase 4E does not implement `POST /api/v1/strategy-recommendations` runtime behavior and does not persist strategy recommendation records.

## No-Broker / No-Real-Money Boundary

Phase 4E does not add broker integrations, broker API calls, autonomous order placement, paper order creation, or real-money trading automation.

## Validation Approach

The internal validation module exposes local helper functions for tests and future local checks:

- `validate_internal_workflow_payload(payload)` validates an existing workflow payload and returns an internal validation report when all invariants pass.
- `build_internal_workflow_validation_report(symbol)` builds the deterministic Phase 4A workflow payload locally and validates it.

These helpers are not mounted as FastAPI routes and are not included in public API responses.

## Phase 4F Follow-Up Path

Potential Phase 4F work may continue strengthening local workflow quality while preserving contract boundaries.

Possible follow-up paths include:

- adding more fixture-backed internal validation scenarios;
- adding review-oriented diagnostics for local development only;
- preparing a future Harness Engineering-approved contract-changing proposal if public handoff preview exposure becomes desirable;
- continuing toward Simulation Desk MVP only after Task 007 / Milestone M4 readiness is reviewed.

Any future public payload change, persistence work, production Supabase connection, or endpoint runtime implementation must be explicitly approved and reviewed in its own scoped PR.
