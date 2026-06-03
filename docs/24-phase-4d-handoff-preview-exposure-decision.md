# 24 — Phase 4D Handoff Preview Exposure Decision

## Purpose

Phase 4D starts a documentation-only governance decision inside Task 007 / Milestone M4 for the Phase 4C adapter-to-agent-run handoff previews.

The purpose is to decide whether the Phase 4C handoff preview shapes should remain internal planning metadata or become public review metadata in the `POST /api/v1/analyze-stock` response.

## Decision

Phase 4C handoff previews remain **internal-only for now**.

Public exposure through `POST /api/v1/analyze-stock` is deferred until Harness Engineering explicitly approves it in a future contract-changing PR.

This Phase 4D decision does not change public API payloads, runtime behavior, persistence behavior, endpoint availability, or strategy recommendation persistence.

## Why Public Exposure Is Deferred

Public exposure is deferred because:

- exposing handoff previews would change `POST /api/v1/analyze-stock` public response semantics;
- a public response change would require same-PR updates to `docs/09-api-and-agent-contracts.md`, runtime response code, and API tests;
- handoff preview fields resemble future `agent_runs` / `agent_outputs` records and could be misread as persisted database records;
- no persistence layer is implemented yet;
- no production Supabase connection is approved or implemented;
- no runtime for `GET /api/v1/agent-runs/{agent_run_id}` is implemented yet;
- keeping the previews internal preserves contract stability while still making future implementation planning reviewable in repository docs and tests.

## Relationship to Phase 4C Handoff Mapping

Phase 4C created deterministic local-only mapping from Phase 4B department adapter outputs to preview-only future `agent_runs` / `agent_outputs` shapes.

Phase 4D does not undo or rename that mapping. It clarifies the exposure boundary:

- Phase 4C mapping may remain available to internal workflow code and tests as preview-only planning metadata.
- Phase 4C mapping must not be presented as persisted `agent_runs` or `agent_outputs` records.
- Phase 4C mapping must not be added to the public analyze-stock response unless a future approved PR intentionally changes the public contract.

## Current Internal-Only Usage Policy

Until a future approved contract-changing PR says otherwise, handoff previews may be used only for:

- local deterministic validation;
- internal workflow assertions;
- developer review of future persistence intent;
- documentation of how adapter outputs could later map into `agent_runs` / `agent_outputs` records;
- planning a future retrieval endpoint or persistence-backed workflow.

Handoff previews must not be used as:

- public analyze-stock response fields;
- persisted database rows;
- production Supabase payloads;
- live agent-run records;
- live agent-output records;
- strategy recommendation records;
- trading signals for autonomous execution.

## Public Exposure Gate Checklist

A future PR may expose handoff previews publicly only if all of the following are true:

1. Harness Engineering explicitly approves public exposure.
2. The public field name is chosen and documented, for example `agent_handoff_preview`.
3. `docs/09-api-and-agent-contracts.md` documents the new public field.
4. Runtime exposes the field without removing existing required fields.
5. API tests assert the field shape.
6. Workflow tests assert no persistence, no production Supabase, no real agent run, and no real agent output creation.
7. Warnings explain preview-only / non-persistent behavior.
8. `agent_trace.agent_runs_created` remains false unless persistence is separately approved.
9. `agent_trace.agent_outputs_created` remains false unless persistence is separately approved.
10. The exposed field is clearly not a `GET /api/v1/agent-runs/{agent_run_id}` response.
11. No database writes, production Supabase, broker integration, or trading automation are introduced.
12. The PR body explicitly flags the public contract change and includes validation evidence.

## Future Public Metadata Requirements If Approved Later

If Harness Engineering later approves public handoff preview metadata, the exposed metadata must be documented as preview-only and non-persistent.

At minimum, the public response documentation and warnings must explain that:

- preview identifiers are not database primary keys;
- preview timestamps are local deterministic workflow metadata unless separately documented otherwise;
- unresolved identifiers such as stock, recommendation, agent-run, and agent-output IDs remain null until persistence is approved;
- the public metadata is not a retrieval endpoint response;
- the metadata does not indicate that `agent_runs`, `agent_outputs`, `strategy_recommendations`, `audit_events`, or paper-order rows were created;
- existing analyze-stock required fields remain backward-compatible unless a separate approved contract decision authorizes a breaking change.

## No-Persistence Boundary

Phase 4D does not authorize persistence writes.

No records may be created or updated in:

- `agent_runs`;
- `agent_outputs`;
- `strategy_recommendations`;
- `paper_orders`;
- `audit_events`;
- any other production table.

## No-Production-Supabase Boundary

Phase 4D does not authorize a production Supabase client, production database session, production database credentials, environment secret requirements, migrations, or networked database access.

The handoff preview exposure decision remains documentation-only and does not require production infrastructure.

## No-Agent-Runs-Endpoint-Runtime Boundary

Phase 4D does not implement `GET /api/v1/agent-runs/{agent_run_id}`.

The internal handoff preview shape is not an endpoint response contract and must not be represented as a completed retrieval runtime.

## No-Strategy-Recommendation-Persistence Boundary

Phase 4D does not implement `POST /api/v1/strategy-recommendations` and does not create `strategy_recommendations` rows.

Any local advisory label produced by the current analyze-stock workflow remains non-persistent and human-reviewed.

## Advisory-Only and Human-in-the-Loop Framing

HK Alpha Team remains advisory-only and human-in-the-loop.

The Phase 4D decision must not be interpreted as approval for:

- live market data ingestion;
- production-quality investment research;
- autonomous strategy approval;
- paper order creation;
- broker execution;
- real-money trading automation.

All real-money decisions remain manual Harness Engineering decisions outside the application.

## Validation Approach

Phase 4D validation should confirm that documentation records the internal-only exposure decision without changing runtime or public contract behavior.

Required checks are:

```bash
python scripts/validate_contracts.py
PYTHONPATH=backend pytest backend/tests -q
git diff --check
```

Reviewers should also confirm:

- changed files are documentation-only;
- `docs/09-api-and-agent-contracts.md` is unchanged unless public API semantics are intentionally changed;
- the public analyze-stock payload is unchanged;
- no endpoint implementation is added;
- no persistence writes are added;
- no Supabase client is added;
- no secrets are added;
- no broker integration is added;
- no real-money trading automation is added;
- `docs/11-project-status.md` contains no stale “until this PR is merged” wording;
- Task 007 and Milestone M4 remain In Progress.

## Phase 4E Follow-On Path

Phase 4E selects the internal-validation path from current repository source-of-truth while preserving this Phase 4D exposure decision.

The next implementation-limited step is to keep Phase 4C handoff previews internal while expanding local workflow validation across:

- the existing Phase 4A analyze-stock workflow payload;
- Phase 4B department adapter outputs; and
- Phase 4C handoff preview records built in memory for validation only.

Phase 4E must not expose handoff previews through `POST /api/v1/analyze-stock`, must not change public API semantics, must not implement `GET /api/v1/agent-runs/{agent_run_id}` runtime, and must not add persistence, production Supabase, broker integration, secrets, paper orders, or real-money trading automation.

Any future work after Phase 4E that changes public API semantics, persistence behavior, production infrastructure, or endpoint runtime must be explicitly approved and must update contracts, runtime code, tests, status, and logs in the same PR.
