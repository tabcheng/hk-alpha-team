# 26 — Phase 4F Fixture-Backed Validation and M4 Readiness

## Purpose

Phase 4F starts fixture-backed internal validation for Task 007 / Milestone M4.

The goal is to make the current local-only workflow easier to review before M4 closeout by adding deterministic positive and targeted drift fixtures for the Phase 4A analyze-stock payload, Phase 4B department outputs, Phase 4C handoff previews, Phase 4D internal-only exposure boundary, and Phase 4E validation layer.

Phase 4F also records an M4 readiness matrix so Harness Engineering can decide what remains before Task 007 / M4 closeout without moving into Task 008 Simulation Desk MVP.

## Relationship to Phase 4A / 4B / 4C / 4D / 4E

| Phase | Current role in the Phase 4 path | Phase 4F relationship |
|---|---|---|
| Phase 4A | Deterministic local-only `POST /api/v1/analyze-stock` workflow skeleton. | Fixture payloads validate that the current skeleton remains stable and advisory-only. |
| Phase 4B | Deterministic department adapter outputs for all eight HK Alpha Team departments. | Fixture payloads validate exact department coverage, common output shape, symbol consistency, score buckets, score confidence, and stage rationales. |
| Phase 4C | Local-only adapter-to-agent-run handoff preview mapping. | Fixture-backed tests validate preview reconstruction, output preview preservation, and unresolved ID boundaries. |
| Phase 4D | Governance decision that handoff previews remain internal-only for now. | Fixture-backed tests cover accidental public exposure keys and preserve the no-public-payload-change boundary. |
| Phase 4E | Internal workflow validator for Phase 4A/4B/4C plus the Phase 4D boundary. | Phase 4F adds reusable fixtures around the validator rather than changing public runtime semantics. |

## Fixture-Backed Validation Scenario List

Phase 4F adds deterministic local-only fixture builders and tests for these review scenarios:

1. Canonical valid workflow payload for `0700.HK`.
2. Valid alternate supported HK symbol payload for `0005.HK`.
3. Missing `department_outputs`.
4. Duplicate department output.
5. Missing department output.
6. Malformed department output shape.
7. Department output with mismatched `stock_symbol`.
8. Score bucket drift.
9. Score confidence drift.
10. Stage rationale drift.
11. Warning disclosure drift.
12. Explicit empty warning override drift.
13. `agent_trace` boundary flag regression.
14. Accidental public `agent_handoff_preview` exposure.
15. Accidental public `agent_handoff_previews` exposure.
16. Accidental public `handoff_preview` exposure.
17. Accidental public `handoff_previews` exposure.
18. Handoff `output_json_preview` mismatch.
19. Handoff unresolved ID regression.
20. Validation non-mutation of input payloads.

The fixtures are test-only and deterministic. They do not require live market data, external APIs, Supabase, broker APIs, secrets, paper orders, or real-money trading.

## M4 Readiness Matrix

### Satisfied in Current Phase 4 Path

| Readiness criterion | Status | Evidence / review note |
|---|---|---|
| Phase 4A deterministic local-only workflow skeleton exists. | Satisfied | `POST /api/v1/analyze-stock` internals build a deterministic local-only workflow payload. |
| Phase 4B deterministic department outputs exist. | Satisfied | The workflow payload includes deterministic `department_outputs` for the eight HK Alpha Team departments. |
| Phase 4C local-only handoff mapping exists. | Satisfied | Handoff previews can be generated internally from department outputs without persistence. |
| Phase 4D internal-only handoff exposure decision exists. | Satisfied | Public handoff preview exposure remains deferred and internal-only. |
| Phase 4E internal workflow validation exists. | Satisfied | The internal validator checks Phase 4A/4B/4C consistency and Phase 4D non-exposure. |
| Phase 4F fixture-backed validation scenarios exist after this PR. | Satisfied after this PR | Fixture-backed tests cover canonical passing payloads and targeted drift/failure payloads. |
| Public analyze-stock envelope remains unchanged. | Satisfied | Phase 4F adds tests and docs only; no public response fields are added. |
| Advisory-only and human-in-the-loop boundaries remain documented. | Satisfied | Existing project boundaries remain in force; Phase 4F does not alter recommendation behavior. |
| CI checks pass. | To verify per PR | Required validation commands are listed below and must pass before M4 closeout is considered. |

### Still Open Before M4 Closeout

| Open item | Why it remains open |
|---|---|
| Decide whether Task 007 needs one final local diagnostic/readiness review PR. | Phase 4F starts the readiness matrix but does not itself close M4. |
| Confirm whether M4 can close without public handoff preview exposure. | Phase 4D currently keeps previews internal-only; Harness Engineering should confirm that is acceptable for M4 closeout. |
| Confirm whether current internal validation coverage is enough for Task 008 handoff. | Phase 4F expands fixture-backed coverage, but Task 008 transition remains a separate approval point. |
| Confirm whether `docs/11-project-status.md` should mark Task 007 / M4 complete in a separate closeout PR. | This PR keeps Task 007 / M4 In Progress unless Harness Engineering separately instructs closeout. |

### Explicitly Out of Scope Before M4 Closeout

| Out-of-scope item | Boundary |
|---|---|
| Public `agent_handoff_preview` exposure. | Not exposed in Phase 4F. |
| `GET /api/v1/agent-runs/{agent_run_id}` runtime. | Not implemented. |
| `POST /api/v1/strategy-recommendations` runtime. | Not implemented. |
| Persistence writes. | Not added. |
| Production Supabase. | Not connected. |
| Live market data. | Not used. |
| Broker integration. | Not added. |
| Paper orders. | Not created. |
| Real-money trading automation. | Not added. |

### Requires Explicit Harness Engineering Approval

The following items require explicit Harness Engineering approval and a separately scoped PR:

- any public API semantics change;
- any `docs/09-api-and-agent-contracts.md` contract change;
- any persistence or production infrastructure work;
- any Task 008 Simulation Desk transition;
- any paper-order or broker-related implementation.

## Already Satisfied Readiness Criteria

The current Phase 4 path already has a deterministic analyze-stock workflow skeleton, deterministic department outputs, local-only handoff preview mapping, an internal-only handoff exposure decision, internal workflow validation, and fixture-backed scenarios after this PR.

The advisory-only and human-in-the-loop model remains documented, and the public analyze-stock envelope remains unchanged by this Phase 4F work.

## Still Open Items Before M4 Closeout

Before M4 closeout, Harness Engineering should review whether the current internal validation coverage is sufficient, whether a final local diagnostic/readiness PR is needed, whether M4 can close while handoff previews remain internal-only, and whether Task 007 / M4 should be marked complete in a separate closeout PR.

## Explicitly Out-of-Scope Items Before Task 008

Phase 4F does not start Task 008 Simulation Desk MVP.

The following remain explicitly out of scope before Task 008 begins: public handoff preview exposure, agent-runs endpoint runtime, strategy-recommendations endpoint runtime, persistence writes, production Supabase, live market data, broker integration, paper orders, real-money trading automation, autonomous order placement, frontend/UI work, secrets, and production infrastructure.

## Boundary Checklist

### No-Public-API-Change Boundary

Phase 4F does not change public analyze-stock response semantics and does not add public `agent_handoff_preview`, `agent_handoff_previews`, `handoff_preview`, or `handoff_previews` fields.

### No-Persistence Boundary

Phase 4F does not create or update `agent_runs`, `agent_outputs`, `strategy_recommendations`, `audit_events`, paper orders, portfolio records, or any other persistence records.

### No-Production-Supabase Boundary

Phase 4F does not connect to production Supabase, does not require Supabase credentials, and does not add a Supabase client.

### No-Agent-Runs-Endpoint-Runtime Boundary

Phase 4F does not implement runtime behavior for `GET /api/v1/agent-runs/{agent_run_id}`.

### No-Strategy-Recommendation-Persistence Boundary

Phase 4F does not implement `POST /api/v1/strategy-recommendations` runtime behavior and does not persist strategy recommendation records.

### No-Broker / No-Paper-Order / No-Real-Money Boundary

Phase 4F does not add broker integration, broker API calls, paper order creation, autonomous order placement, or real-money trading automation.

## Validation Commands

Required validation for this Phase 4F PR:

```bash
python scripts/validate_contracts.py
PYTHONPATH=backend pytest backend/tests -q
git diff --check
```

Reviewers should also inspect changed files and confirm no accidental endpoint runtime, persistence, production Supabase, broker, paper-order, secret, real-money trading, or public handoff-preview exposure was introduced.

## Phase 4G / M4 Closeout Follow-Up Path

A possible Phase 4G / M4 closeout follow-up should be a separate, bounded readiness review PR.

That follow-up can confirm validation evidence, decide whether M4 can close while handoff previews remain internal-only, and update `docs/11-project-status.md` only if Harness Engineering approves marking Task 007 / Milestone M4 complete.

Task 008 Simulation Desk MVP should remain planned until Harness Engineering explicitly approves the transition.
