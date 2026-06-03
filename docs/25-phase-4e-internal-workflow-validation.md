# 25 — Phase 4E Internal Workflow Validation

## Purpose

Phase 4E starts an implementation-limited, local-only validation expansion inside Task 007 / Milestone M4.

Its purpose is to validate consistency across the existing Phase 4A analyze-stock workflow payload, Phase 4B department adapter outputs, and Phase 4C agent handoff previews without changing public API semantics.

Phase 4E is an internal workflow quality gate. It is not a public response contract expansion, not persistence, not production infrastructure, and not trading automation.

## Relationship to Phase 4A / 4B / 4C / 4D

- **Phase 4A** introduced the deterministic local-only first-analysis workflow skeleton behind `POST /api/v1/analyze-stock`.
- **Phase 4B** added deterministic department adapter outputs for all eight HK Alpha Team departments and exposes `department_outputs` as local-only adapter preview metadata in the existing analyze-stock payload.
- **Phase 4C** added deterministic adapter-to-agent-run handoff previews for internal planning.
- **Phase 4D** documented that Phase 4C handoff previews remain internal-only and are not exposed publicly through the analyze-stock response.
- **Phase 4E** keeps the Phase 4D internal-only decision in place while adding validation helpers that check whether the Phase 4A payload, Phase 4B outputs, and Phase 4C previews remain mutually consistent.

## Internal Validation Invariants

Phase 4E validation checks that:

1. required analyze-stock payload fields remain present;
2. `analysis_status` remains `phase4a_skeleton`;
3. `workflow_phase` remains `Phase 4A — Deterministic First Analysis Workflow Skeleton`;
4. `department_outputs` contains exactly one output for each of the eight HK Alpha Team departments;
5. every department output follows the locked common agent output shape;
6. every department output `stock_symbol` matches the analyze-stock payload symbol;
7. payload scores match scores rebuilt from department outputs;
8. payload score confidence values match confidence values rebuilt from department outputs;
9. stage rationale keys match department names;
10. each stage rationale equals the first evidence item for its corresponding department output;
11. warning disclosures preserve local-only, no-live-research, no-persistence, no-production-Supabase, no-broker, and no-real-money boundaries;
12. required `agent_trace` boundary flags remain `false`;
13. Phase 4C handoff previews can be built from the payload’s `department_outputs`;
14. exactly eight handoff preview records are produced;
15. every handoff preview remains preview-only and non-persistent;
16. every handoff preview output payload preserves the matching department output;
17. unresolved persistence identifiers remain `null`; and
18. public analyze-stock payloads do not include handoff preview fields.

## Required Analyze-Stock Payload Checks

The internal validator checks the existing local workflow payload for the fields already required by Phase 4A / Phase 4B behavior, including strategy framing, reasons, risks, invalidation conditions, `agent_trace`, `department_outputs`, stage rationales, timestamps, and schema version.

The validator does not add new public fields to `POST /api/v1/analyze-stock` and does not change the response envelope or endpoint semantics.

## Department Output Checks

Phase 4E validates that department adapter output coverage remains exactly all eight departments:

- Market Intelligence Agent
- Company Research Agent
- News & Sentiment Agent
- Technical Analysis Agent
- Risk Manager Agent
- Investment Committee Agent
- Simulation Investment Desk
- Investment Strategy Office

Each output must retain the locked common agent output shape used by the existing adapter preview contract. The validator also verifies that score buckets, score confidence buckets, and stage rationales are derived from those adapter outputs rather than drifting independently.

## Handoff Preview Checks

Phase 4E builds Phase 4C handoff previews in memory from the validated `department_outputs` and checks that the previews remain planning artifacts only.

The validation confirms that handoff previews:

- produce exactly eight preview records;
- preserve each department output in `future_agent_output_preview.output_json_preview`;
- keep `persistence_allowed = false`;
- keep database write, production Supabase, agent-run persistence, agent-output persistence, strategy recommendation, audit event, paper order, broker execution, and real-money order flags false; and
- keep unresolved persistence identifiers such as `stock_id_preview`, `recommendation_id_preview`, and `agent_run_id_preview` null.

## Public Payload Non-Exposure Checks

Phase 4E preserves the Phase 4D internal-only exposure decision.

The internal validator fails if the analyze-stock payload contains public handoff-preview fields such as:

- `agent_handoff_preview`
- `agent_handoff_previews`
- `handoff_preview`
- `handoff_previews`

Any future decision to expose handoff previews publicly must be handled by a Harness Engineering-approved contract-changing PR with same-PR updates to API contracts, runtime response code, tests, and governance logs.

## Advisory-Only and Human-in-the-Loop Framing

Phase 4E does not alter the advisory-only nature of HK Alpha Team.

The workflow remains for structured research support and validation scaffolding only. Harness Engineering remains responsible for final investment judgment, risk acceptance, and any real-money decision.

## No-Persistence Boundary

Phase 4E does not add persistence writes and does not create database rows.

It does not create:

- `agent_runs`
- `agent_outputs`
- `strategy_recommendations`
- `audit_events`
- `paper_orders`

The validator only reads local in-memory payload structures and builds local in-memory preview records for validation.

## No-Production-Supabase Boundary

Phase 4E does not add a Supabase client, connect to production Supabase, require Supabase credentials, or apply schema migrations.

The production Supabase boundary remains unchanged.

## No-Agent-Runs-Endpoint-Runtime Boundary

Phase 4E does not implement runtime behavior for `GET /api/v1/agent-runs/{agent_run_id}`.

The Phase 4C handoff preview shape remains a local planning aid for future reviewed implementation work, not a served endpoint resource.

## No-Strategy-Recommendation-Persistence Boundary

Phase 4E does not implement `POST /api/v1/strategy-recommendations` runtime and does not persist strategy recommendations.

The Investment Strategy Office adapter output remains local-only placeholder support for human review.

## No-Broker / No-Real-Money Boundary

Phase 4E does not add broker APIs, brokerage credentials, paper orders, real-money order placement, autonomous execution, or trading automation.

The validator explicitly checks that broker and real-money boundary flags remain false.

## Validation Approach

The internal validation module provides two helpers:

- `validate_internal_workflow_payload(payload)` validates an existing local workflow payload and returns an internal report when all checks pass.
- `build_internal_workflow_validation_report(symbol)` builds a fresh deterministic workflow payload and validates it for internal review.

Both helpers are internal-only. They are not imported by public API routes and do not mutate public analyze-stock payloads.

## Phase 4F Follow-Up Path

Possible Phase 4F follow-up work should remain source-of-truth-derived and reviewed by Harness Engineering. Candidate follow-ups include:

- deciding whether internal validation should run in CI as a dedicated lightweight check;
- adding additional drift checks for future workflow layers;
- preparing a separate contract-changing proposal if Harness Engineering later wants public handoff preview exposure; or
- continuing toward Simulation Desk MVP planning only after Task 007 / Milestone M4 review indicates readiness.

Any follow-up must preserve the advisory-only, human-in-the-loop, no-production-Supabase, no-broker, and no-real-money-trading boundaries unless explicitly changed through approved governance.
