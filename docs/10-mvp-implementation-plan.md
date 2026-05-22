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

## Phased Plan

## Phase 0 — Alignment and Setup

- Validate docs 08/09 with maintainers.
- Freeze v1 field definitions for critical tables and endpoint envelopes.
- Define branch and PR sequencing rules for implementation tasks.

Exit criteria:
- Sign-off comment in project status log.

## Phase 1 — Data Layer Foundation

- Create initial Supabase migration set from doc 08.
- Implement constraints/indexes for core tables (`securities`, `research_notes`, `strategy_recommendations`, `simulation_runs`, `paper_positions`, `paper_trades`).
- Enable baseline RLS policies and seed minimal reference data.

Exit criteria:
- Migrations apply cleanly in local/staging.
- Basic CRUD smoke tests pass.

## Phase 2 — API Layer (FastAPI)

- Implement `/api/v1/research/*`, `/api/v1/strategy/*`, `/api/v1/simulations/*` endpoints.
- Implement standard response envelope and error taxonomy.
- Add request validation and correlation IDs.

Exit criteria:
- OpenAPI spec generated and reviewed.
- Endpoint contract tests pass for success and error paths.

## Phase 3 — Agent Integration Layer

- Implement internal adapters for research/strategy/simulation agent departments.
- Validate agent input/output schemas against doc 09.
- Persist run traces in `agent_runs`.

Exit criteria:
- Contract conformance tests pass.
- At least one end-to-end advisory flow executes with mock data.

## Phase 4 — Simulation and Learning Loop

- Implement paper position/trade recording flow.
- Compute and persist run metrics snapshots.
- Generate improvement proposals from simulation summaries.

Exit criteria:
- Simulation report includes losing-trade analysis and explicit limitations.

## Phase 5 — Hardening and Review

- Add role-aware access checks.
- Add observability dashboards/queries for API + agent traces.
- Conduct boundary compliance review (no execution APIs, no real-money actions).

Exit criteria:
- Governance checklist passes.
- MVP readiness documented.

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
