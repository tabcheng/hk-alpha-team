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

## Phased Plan (Requested Model)

## Phase 1 — Schema and Storage Foundation (Task 002 alignment)

- Finalize canonical v1 table names and field contracts.
- Convert design to migration-ready specs (still review-first).
- Confirm RLS intent and audit retention boundaries.

## Phase 2 — API and Envelope Contract Finalization (Task 003 alignment)

- Lock required MVP endpoint set.
- Lock required response envelope format.
- Lock error taxonomy and traceability metadata.

## Phase 3 — Agent Department Contract Finalization

- Lock input/output JSON contracts for all eight agent departments.
- Validate strategy outputs include label, reasoning, risks, invalidation, and human decision framing.

## Phase 4 — Implementation Readiness and PR Sequencing (Task 004 alignment)

- Finalize PR slicing and exit criteria.
- Confirm risks/mitigations and governance checks.
- Mark Tasks 002–004 status for review and merge readiness.

## Draft Milestone Windows (Planning Baseline)

- Phase 0: 2026-05-25 to 2026-05-29
- Phase 1: 2026-06-01 to 2026-06-12
- Phase 2: 2026-06-15 to 2026-06-26
- Phase 3: 2026-06-29 to 2026-07-10
- Phase 4: 2026-07-13 to 2026-07-24
- Phase 5: 2026-07-27 to 2026-08-07

These windows are estimates for planning and will be refined during implementation PR sequencing.

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

## Definition of Done for MVP (Planned)

- All v1 schema objects and API endpoints implemented with tests.
- Strategy outputs include reasoning, risks, invalidation conditions, and human decision framing.
- Simulation captures full history, including losses.
- Governance and progress docs updated with release status.
