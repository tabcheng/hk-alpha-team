# Decision Log

| Date | Decision | Rationale | Impact |
|---|---|---|---|
| 2026-05-21 | GitHub is the source of truth for project documentation, architecture, decisions, progress, and lessons learned. | Keeps governance and design history versioned, auditable, and reviewable in one place. | Repository docs become canonical references for future tasks and reviews. |
| 2026-05-21 | Codex Web will generate and maintain repository files through PRs. | Enforces transparent, review-driven AI collaboration with explicit change sets. | All major AI-assisted updates flow through commit + PR workflows. |
| 2026-05-21 | Supabase and Railway are the planned infrastructure. | Provides a clear implementation direction while remaining in documentation-first phase. | Upcoming tasks can design schema/deployment assumptions against stable platform targets. |
| 2026-05-21 | v1 focuses on advisory/reporting, not automated trading. | Prevents scope drift and keeps risk governance human-centric from the start. | Architecture and outputs remain recommendation-focused rather than execution-focused. |
| 2026-05-21 | Paper trading and simulation are included from early design. | Enables validation and learning before any real-money confidence scaling. | Simulation desk and review loops are first-class design components. |
| 2026-05-21 | Final real-money decisions remain with the user. | Preserves explicit human authority and accountability. | System outputs must frame decisions as advisory with human approval boundaries. |
| 2026-05-21 | Project details should move into GitHub docs to keep ChatGPT Project Instructions lightweight. | Reduces prompt bloat while preserving project memory in versioned documentation. | High-level instructions remain concise; detailed governance lives in repository docs. |

## 2026-05-21 — Decision: Adopt Append-First Advisory Data Model for MVP

**Context:** Tasks 002-004 required a coherent design for schema, contracts, and rollout sequencing.

**Decision:**
- Use append-first records for strategy and simulation history.
- Standardize API envelopes with traceability metadata (`request_id`, `timestamp`, `version`).
- Require strategy outputs to include reasoning, key risks, invalidation conditions, and explicit human decision framing.
- Keep v1 strictly advisory and simulation-only (no execution APIs).

**Implications:**
- Improves auditability and governance.
- Enables contract-driven implementation sequencing in subsequent PRs.
- Defers non-essential infrastructure details until implementation phase.


## 2026-05-22 — Decision: Include Design-Only SQL Draft and Validation Rules Before Implementation

**Context:** Harness review requested clearer implementation readiness without adding executable code.

**Decision:**
- Add an illustrative SQL draft section to validate table/constraint shapes.
- Add explicit minimal JSON contract validation targets for API/agent payloads.
- Add draft milestone windows to improve implementation planning readability.

**Implications:**
- Reduces ambiguity for upcoming implementation PRs.
- Preserves documentation-only scope and boundary compliance.

## 2026-05-22 — Decision: Enforce Canonical Schema/Contract Naming for PR #2

**Context:** Harness re-review requested exact blocker fixes to align schema naming, endpoint set, envelope format, and phase/status model.

**Decision:**
- Treat canonical HK Alpha Team table names as the primary v1 schema contract.
- Treat required MVP endpoint set and response envelope as fixed v1 contract surfaces.
- Require JSON examples for all eight defined agent departments.
- Update status state for Tasks 002–004 to In Review / Pending Merge.

**Implications:**
- Reduces ambiguity in implementation PRs.
- Aligns design docs with agreed project governance artifacts.

## 2026-05-22 — Decision: Standardize Agent Example Payloads on a Common Contract Shape

**Context:** Final Harness re-review required all eight agent examples to share a single contract shape and include a final strategy recommendation envelope example.

**Decision:**
- All agent examples use `agent_name`, `agent_version`, `stock_symbol`, `input_summary`, `evidence`, `score`, `confidence`, `key_findings`, `risks`, `invalidation_conditions`, `generated_at`, `schema_version`.
- Final strategy recommendation examples use the exact required response envelope.

**Implications:**
- Reduces interpretation drift across departments and implementation stages.
- Improves API/agent contract consistency and testability for subsequent implementation PRs.
