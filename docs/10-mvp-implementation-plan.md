# 10 — MVP Implementation Plan (Task 004)

## Purpose

Define execution roadmap from documentation design to a testable MVP without violating advisory-only boundaries.

## Scope

- Planning artifact for upcoming implementation PRs.
- No implementation code in this task.

## MVP Outcomes

1. User can store and retrieve research notes for HK securities.
2. User can generate and review strategy recommendations with structured risk framing.
3. User can run paper-trading simulations and inspect full trade history (including losses).
4. User can review telemetry and governance logs for auditability.

## Phased Plan (Exact Required Model)

## Phase 1 — Documentation and Contracts

- Finalize documentation artifacts and required contract surfaces.
- Confirm schema names, endpoints, and response envelope are exact.

## Phase 2 — Database Preparation

- Prepare database planning artifacts for migration implementation.
- Validate table relationships and retention requirements.

## Phase 3 — Backend Skeleton

- Prepare backend module skeleton planning for required endpoints.
- Define request handling, tracing, and error mapping approach.

## Phase 4 — First Analysis Workflow

- Define first end-to-end analysis workflow around stock analysis.
- Ensure advisory-only outputs and human decision framing.

## Phase 5 — Simulation Desk MVP

- Define paper order and portfolio tracking workflow.
- Define simulation recordkeeping and trade review flow.

## Phase 6 — Simple User Interface or Report Output

- Define minimal output surface (simple UI or report generation).
- Ensure contract-aligned presentation of recommendations and warnings.

## Phase 7 — Review and Learning Loop

- Define recurring review cadence and learning proposal updates.
- Capture audit events and retrospective improvements.

## Draft Milestone Windows (Planning Baseline)

- Phase 1 — Documentation and Contracts: 2026-05-26 to 2026-05-30
- Phase 2 — Database Preparation: 2026-06-02 to 2026-06-13
- Phase 3 — Backend Skeleton: 2026-06-16 to 2026-06-27
- Phase 4 — First Analysis Workflow: 2026-06-30 to 2026-07-11
- Phase 5 — Simulation Desk MVP: 2026-07-14 to 2026-07-25
- Phase 6 — Simple User Interface or Report Output: 2026-07-28 to 2026-08-08
- Phase 7 — Review and Learning Loop: 2026-08-11 to 2026-08-22

## Suggested PR Breakdown

1. PR-A: Supabase migrations + schema tests.
2. PR-B: Research endpoints + tests.
3. PR-C: Strategy endpoints + review flow + tests.
4. PR-D: Simulation endpoints + metrics + tests.
5. PR-E: Agent contract adapters + telemetry.
6. PR-F: Hardening, docs updates, and MVP sign-off.

## Risks and Mitigations

- **Risk:** Contract drift between docs and implementation.  
  **Mitigation:** Add schema validation tests and contract fixtures early.
- **Risk:** Overreach into live trading features.  
  **Mitigation:** Boundary gate in PR template and review checklist.
- **Risk:** Insufficient simulation traceability.  
  **Mitigation:** Append-only event model and immutable timestamps.
- **Risk:** Underestimated RLS complexity.  
  **Mitigation:** Stage RLS rollout with explicit role tests.

## Dependencies

- Task 002 (schema design) and Task 003 (contracts) accepted.
- Supabase project/bootstrap available for local testing in future tasks.


## MVP Acceptance Criteria

- User can request analysis for one symbol.
- System returns structured strategy recommendation.
- System records recommendation.
- System can create paper trade record.
- System can later compare recommendation with outcome.
- All outputs are traceable and reviewable.
- Real-money decision remains with user.

## Definition of Done for MVP (Planned)

- All v1 schema objects and API endpoints implemented with tests.
- Strategy outputs include reasoning, risks, invalidation conditions, and human decision framing.
- Simulation captures full history, including losses.
- Governance and progress docs updated with release status.
