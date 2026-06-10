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


## 2026-05-22 — Decision: Deep Audit Contract Governance Tightening

**Context:** Harness Deep Audit requested stricter contract lock and consistency governance plus explicit endpoint/error details.

**Decision:**
- Added Contract Lock, PR Completion, and Consistency Audit rules in `AGENTS.md`.
- Added endpoint-level contract details and explicit error envelope/codes in `docs/09-api-and-agent-contracts.md`.
- Added MVP acceptance criteria and schema migration planning note in docs 10 and 08.

**Implications:**
- Reduces contract drift risk during implementation.
- Strengthens reviewability and traceability requirements before coding begins.

## 2026-05-22 — Decision: Standardize PR Governance Artifacts Before Implementation

**Context:** With PR #2 merged, implementation is next. Review consistency and scope control needed strengthening before migration and backend work.

**Decision:**
- Capture original project intent in a dedicated brief doc.
- Define reusable large PR handling policy and PR review checklist.
- Define reusable Codex task prompt template.
- Prepare Task 005 as the explicit entry point for Phase 2.

**Implications:**
- Improves repeatability and review quality for implementation PRs.
- Reduces scope drift risk while contract-locked components move into code.
- Establishes a consistent prompt/review standard for subsequent tasks.

## 2026-05-24 — Decision: Establish Migration Draft Baseline with Automated Contract Checks

**Context:** Phase 2 started with Task 005 and required implementation preparation while preserving canonical schema/API naming locks.

**Decision:**
- Introduce a first draft Supabase migration file containing the canonical v1 core table set and baseline constraints/indexes.
- Add a lightweight contract validation script that fails CI if locked table names, endpoint names, response envelope keys, or strategy labels drift from source-of-truth docs.
- Record migration interpretation assumptions in a dedicated assumptions document for transparent review.

**Implications:**
- Reduces accidental contract drift as implementation work begins.
- Provides early CI guardrails before backend feature coding.
- Keeps production deployment and RLS rollout deferred to dedicated follow-up PRs.


## 2026-05-26 — Decision: Defer Branch-Protection Plan Upgrade During Phase 2

We will not upgrade GitHub account/organization immediately. During Phase 2 we will rely on manual governance, PR review protocol, GitHub Actions checks, and unresolved-thread checks. Revisit GitHub Pro / Team / Enterprise organization upgrade during Phase 3 or Phase 4.


## 2026-05-26 — Decision: Start Phase 3 with Contract-First Backend Skeleton

**Context:** PR #5 completed local/test migration validation and CI checks, allowing Phase 2 closeout and Phase 3 start.

**Decision:**
- Mark Phase 2 Database Preparation as completed in project status tracking.
- Start Backend Skeleton with only `GET /health` and `GET /api/v1/project-status` implemented first.
- Enforce required success/error envelope helpers in backend code before adding broader endpoint implementations.

**Implications:**
- Backend implementation can proceed incrementally while preserving locked contract surfaces.
- Project status can be queried from a stable contract-aligned endpoint early in Phase 3.

## 2026-06-01 — Decision: Add Analyze-Stock as a Stub Before Real Analysis

**Context:** Phase 3 needs to prepare the first analysis workflow contract while Harness Engineering remains a solo, mobile-first operator without production Supabase, Railway, or desktop-local setup requirements.

**Decision:** Implement `POST /api/v1/analyze-stock` as a contract-first FastAPI stub with request validation, required success/error envelopes, advisory-style placeholder fields, and explicit warnings. Document a mobile-first environment strategy that keeps PR #8 verifiable through repository tests and CI.

**Rationale:**

- Enables client and test integration against the locked MVP endpoint before Phase 4 real analysis logic.
- Reduces contract drift by exercising response shape and validation behavior in code.
- Preserves advisory-only and human-in-the-loop boundaries.
- Avoids requiring production secrets, hosted Supabase, Railway deployment, live market data, or brokerage execution APIs.

## 2026-06-02 — Decision: Establish Codex PR Factory Governance Workflow

**Context:** After PR #8 completed the backend skeleton milestone, Harness Engineering needed a repeatable governance workflow for ChatGPT + Codex + GitHub PR + GitHub Actions collaboration before Phase 4 work begins.

**Decision:**
- Add `docs/20-codex-pr-factory.md` as the canonical Codex PR Factory workflow for task classes, role permissions, required gates, PR body expectations, evidence language, and source-of-truth-based follow-up handling.
- Treat Claude Code as not assumed unless Harness Engineering explicitly approves it later.
- Require Factory PRs to separate read-only planning/review roles from file-modifying implementation/log-update roles, and confirm Codex must not self-approve.

**Implications:**
- Improves repeatability and auditability for documentation-only, implementation-limited, and governance-sensitive / production-impacting PRs.
- Reduces stale-instruction risk by requiring next task recommendations to come from current GitHub/repository source-of-truth review.
- Strengthens review gates before Phase 4 analysis workflow work begins while preserving advisory-only and no-real-money-execution boundaries.


## 2026-06-02 — Decision: Align Analyze-Stock Current Contract to Phase 4A Skeleton

**Context:** PR #10 starts Task 007 / Milestone M4 by replacing the Phase 3 static analyze-stock stub internals with a deterministic local-only workflow skeleton. A review found that `docs/09-api-and-agent-contracts.md` still described the current runtime as Phase 3 `stub_only` behavior.

**Decision:** Update the canonical analyze-stock API contract so current behavior is `analysis_status = "phase4a_skeleton"` and `workflow_phase = "Phase 4A — Deterministic First Analysis Workflow Skeleton"`, while preserving the Phase 3 `stub_only` section as historical context only.

**Implications:**
- Runtime, tests, and canonical docs are aligned for Phase 4A.
- The endpoint name, success/error envelopes, preferred strategy labels, advisory-only framing, and no-real-money-execution boundaries remain locked.
- Phase 4A remains deterministic and local-only: no live market data, external APIs, persistence writes, production Supabase, broker integration, secrets, paper order creation, or real-money trading automation.


## 2026-06-02 — Decision: Expose Phase 4B Department Adapter Preview Metadata Without Runtime Semantic Rename

**Context:** Phase 4B starts Task 007 follow-up work by adding deterministic department scoring adapters that mirror the locked common agent output shape. The adapter outputs are useful for reviewability, but the workflow must remain local-only, advisory-only, and non-persistent.

**Decision:** Expose `department_outputs` and `department_output_note` as local-only analyze-stock response metadata while preserving `analysis_status = "phase4a_skeleton"`, `workflow_phase = "Phase 4A — Deterministic First Analysis Workflow Skeleton"`, locked endpoint names, and the required response envelope.

**Implications:**
- Runtime, tests, and canonical docs are aligned for Phase 4B adapter preview metadata.
- `department_outputs` mirrors the common agent output shape but is not a persisted `agent_outputs` record and does not mean `agent_runs` were created.
- Phase 4B remains deterministic and local-only: no live market data, external APIs, persistence writes, production Supabase, broker integration, secrets, paper order creation, or real-money trading automation.

## 2026-06-03 — Decision: Keep Phase 4C Handoff Previews Internal-Only for Now

**Context:** Phase 4C added deterministic local-only adapter-to-agent-run handoff mapping that creates preview-only future `agent_runs` / `agent_outputs` shapes for internal planning and validation. Those previews resemble future persistence records, but there is no persistence layer, production Supabase connection, or implemented `GET /api/v1/agent-runs/{agent_run_id}` runtime.

**Decision:** Phase 4C handoff previews remain internal-only for now. Public exposure through `POST /api/v1/analyze-stock` is deferred until Harness Engineering explicitly approves it in a future contract-changing PR.

**Implications:**
- This decision does not change public API payloads or runtime behavior.
- A future public exposure PR must update `docs/09-api-and-agent-contracts.md`, runtime response code, and API tests in the same PR.
- Future exposure must clearly warn that previews are preview-only and non-persistent, not `agent_runs` / `agent_outputs` database rows and not a `GET /api/v1/agent-runs/{agent_run_id}` response.
- No persistence writes, production Supabase, broker integration, paper orders, secrets, or real-money trading automation are authorized by this decision.

## 2026-06-04 — Decision: Close Task 007 / Milestone M4 After Phase 4G Readiness Review

**Context:** Phase 4A through Phase 4F created the deterministic local-only analyze-stock workflow skeleton, deterministic department adapters, local-only handoff mapping, an internal-only handoff preview exposure decision, internal workflow validation, and fixture-backed validation scenarios with an M4 readiness matrix. Task 007 / Milestone M4 still required a final governance-sensitive closeout decision.

**Decision:** Mark Task 007 / Milestone M4 completed after Phase 4G readiness review, while keeping Task 008 Simulation Desk MVP Planned and M5 Planned. M4 can close while Phase 4C handoff previews remain internal-only because public handoff preview exposure is not required for M4 closeout.

**Implications:**
- Public handoff preview exposure remains deferred to a separate future contract-changing PR requiring explicit Harness Engineering approval and same-PR `docs/09-api-and-agent-contracts.md`, runtime, and API test updates.
- Phase 4E / Phase 4F validation evidence is sufficient for Task 008 handoff planning readiness, not for Simulation Desk MVP runtime behavior.
- No public analyze-stock payload change, `docs/09` contract change, persistence writes, production Supabase connection, endpoint runtime, broker integration, paper orders, secrets, or real-money trading automation are authorized by M4 closeout.

## 2026-06-04 — Decision: Start Task 008 / Milestone M5 Planning With Task 008A Boundary and Contract Planning

**Context:** Task 007 / Milestone M4 is completed after Phase 4G closeout readiness review. The next source-of-truth step is to start Task 008 / Milestone M5 safely by defining Simulation Desk MVP boundaries before any runtime, persistence, production Supabase, broker, paper-order execution, or real-money trading work begins.

**Decision:** Start Task 008 / Milestone M5 as In Progress for Task 008A planning only. Task 008A records Simulation Desk MVP boundary, operating-rule, schema-reference, endpoint-reference, approval-gate, validation, and follow-up PR sequencing guidance.

**Implications:**
- Task 007 / Milestone M4 remain Completed.
- Task 008 / Milestone M5 are In Progress for documentation-only planning, not implementation.
- This decision does not authorize runtime behavior, persistence writes, production Supabase, broker integration, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit event creation, live market data, secrets, or real-money trading automation.
- Future Simulation Desk implementation requires explicit Harness Engineering review at the public API contract, persistence, production Supabase, broker / real-money, and status/log gates.

## 2026-06-04 — Decision: Implement Task 008B as Pure Local Simulation Contract Fixtures and Validation Matrix

**Context:** Task 008A defined the Simulation Desk MVP boundary and identified local-only contract fixtures as the safest first implementation-limited M5 slice before any runtime, persistence, production Supabase, broker, paper-order creation, or real-money trading work.

**Decision:** Implement Task 008B as a pure local-only Simulation Desk contract fixture and validation module with deterministic fixtures for the seven required record shapes, validation helpers, matrix/report coverage, tests, and documentation.

**Implications:**
- Task 008 / Milestone M5 remain In Progress with an implementation-limited local validation slice.
- Canonical schema table names and locked endpoint names are referenced without renaming or runtime implementation.
- Losing outcomes remain visible and learning proposals remain reviewable rather than auto-applied.
- No IO, HTTP, database access, endpoint handlers, persistence, production Supabase, paper order creation, broker integration, live market data, secrets, or real-money trading automation are authorized by this decision.
- Any Task 008C expansion beyond pure local validation requires explicit Harness Engineering review and same-PR updates to affected contracts, runtime, tests, status, and logs.

## 2026-06-04 — Task 008D Remains Planning-Only Persistence Gate Readiness

- Decision: Task 008D is limited to documentation-only, governance-sensitive persistence gate readiness and migration alignment planning for the Simulation Desk MVP.
- Rationale: Task 008B and Task 008C created local-only Simulation Desk record shapes and validation behavior, so the next safe step is to map those artifacts to canonical schema tables and approval gates before any migration, runtime, or persistence work begins.
- Boundary: This decision does not authorize SQL migration, endpoint runtime, persistence writes, Supabase client setup, production Supabase, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit-event database creation, broker integration, autonomous order placement, or real-money trading automation.
- Review requirement: Harness Engineering must explicitly approve any future task that crosses a named migration, persistence, Supabase, endpoint runtime, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit-event creation, broker, or real-money gate.

## 2026-06-05 — Decision: Adopt PR Review Evidence Closure Protocol for Full PR Reviews

**Context:** Full PR reviews for governance-sensitive and implementation-limited work can encounter recurring limitations around public web search availability, CI log depth, local reruns, branch protection visibility, mutable PR head commits, unresolved review threads, and post-merge verification.

**Decision:** Adopt `docs/32-pr-review-evidence-closure-protocol.md` as part of the Codex PR Factory full PR review process. Future full PR reviews must classify evidence as closed evidence, reduced-risk evidence, or residual limitation; use authenticated GitHub connector/API evidence as source of truth when public web search is unavailable; choose CI depth proportional to PR risk; avoid unsupported local-rerun claims; record hidden branch protection/ruleset visibility as a limitation instead of requesting routine Harness Engineering screenshots; require expected-head-SHA merge locking; block on unresolved review threads; and perform post-merge source-of-truth verification on `main`.

**Implications:** This governance decision does not eliminate all residual review risk and does not authorize runtime, persistence, migrations, Supabase clients, production infrastructure, broker integration, real-money trading automation, or Task 008E. It converts recurring limitations into explicit evidence gates for future PR reviews.

## 2026-06-05 — Decision: Approve Task 008E as Local-Only Simulation Desk Readiness Reporting

**Context:** Task 008B provides local Simulation Desk fixture validation, Task 008C provides local paper-order intent validation, and Task 008D records persistence gate readiness without approving migration or persistence work.

**Decision:** Task 008E is approved only as an implementation-limited, pure local-only readiness reporting slice that aggregates Task 008B and Task 008C evidence into a deterministic in-memory artifact.

**Implications:** This decision does not approve runtime behavior, SQL migration, persistence writes, Supabase client setup, production Supabase, endpoint implementation, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit-event creation, broker integration, live market data, external API usage, secrets, deployment, autonomous order placement, or real-money trading automation. Any future Task 008F gate requires explicit Harness Engineering review and approval.

## 2026-06-05 — Decision: Keep Task 008F as Local-Only Scenario-Pack and Gate-Decision Evidence

**Context:** Task 008B provides local Simulation Desk fixture validation, Task 008C provides local paper-order intent validation, Task 008D records persistence and migration gate planning, and Task 008E aggregates readiness evidence without opening runtime or persistence gates.

**Decision:** Task 008F is approved only as an implementation-limited, governance-sensitive, pure local-only scenario-pack and gate-decision evidence slice. It may aggregate Task 008B, Task 008C, and Task 008E evidence; include deterministic valid and invalid scenario validation; preserve canonical schema table names; reference locked endpoint names for traceability only; and record possible future Task 008G directions without approving any gate.

**Implications:** Task 008 / Milestone M5 remains In Progress. This decision does not authorize SQL migration, persistence writes, Supabase client setup, production Supabase, endpoint runtime, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit-event database creation, broker integration, live market data, external API calls, secrets, deployment, autonomous order placement, or real-money trading automation. Any future Task 008G gate crossing requires explicit Harness Engineering approval in a separate PR scope.

## 2026-06-06 — Task 008G Non-Real-Money Productization Gates and Dual Simulation Origins

- **Decision:** Harness Engineering approves opening non-real-money productization gates after Task 008F, including schema/contract alignment, local/test migration planning, persistence design, endpoint runtime planning, paper-trading recordkeeping, system-generated learning simulations, audit events, and future non-real-money product runtime sequencing.
- **Decision:** The Simulation Investment Desk adopts a dual simulation-origin model: `user_recorded` paper trades and `system_generated_learning` simulations.
- **Rationale:** User-entered paper trade journals and system-generated recommendation-quality simulations have different provenance, required fields, review expectations, and learning impact. They must remain distinguishable so audit records, performance reviews, and learning proposals are trustworthy.
- **Contract/schema impact:** Canonical table names, locked MVP endpoint names, preferred strategy labels, Investment Strategy Office required fields, and response envelope fields remain unchanged. Additive field-level semantics such as `simulation_origin`, `paper_order_origin`, `created_by_type`, `source_recommendation_id`, `user_recorded_notes`, `system_learning_reason`, `requires_human_review`, and `learning_proposal_id` are documented for future implementation.
- **Boundary:** Real-money trading, real-money order placement, autonomous real-money execution, broker execution APIs, committed secrets, production Supabase connection, deployment, live market data, silent auto-application of learning proposals, and hiding or overwriting losing simulations remain prohibited.

## 2026-06-06 — Task 008H Commercial Readiness and Subscription Product Governance Baseline

**Decision:** Harness Engineering treats HK Alpha Team as a serious commercial product candidate that may later support membership or subscription offerings.

**Rationale:** Commercial-readiness standards should be recorded before runtime, persistence, membership, subscription, billing, deployment, or public-facing product work begins, so product claims, evidence expectations, user/account planning, entitlement planning, privacy, retention, audit, billing, security, and compliance boundaries can be reviewed explicitly.

**Governance impact:** Commercial readiness must be introduced through explicit PRs and evidence-based review. Major commercial, runtime, deployment, membership, subscription, billing, or governance-sensitive PRs must use full review protocol, evidence closure language, and no-100%-certainty framing.

**Boundary:** Advisory-only, no-guaranteed-return, no-real-money-trading, no autonomous real-money execution, and human-in-the-loop boundaries remain mandatory. This decision does not implement runtime, persistence, production Supabase, deployment, billing/payment integration, membership/subscription runtime, authentication runtime, live market data, broker integration, secrets, or real-money trading.

## 2026-06-06 — Task 008I Non-Production Simulation Desk Runtime Slice

**Decision:** Implement the first usable Simulation Desk backend runtime as a non-production, process-local in-memory slice for `POST /api/v1/simulation/paper-orders` and `GET /api/v1/paper-portfolios/{portfolio_id}`.

**Rationale:** Harness Engineering approved non-real-money productization, and the Simulation Desk MVP needs usable endpoint behavior before any later decision on production persistence, Supabase deployment, commercial runtime, live data, broker integration, or real-money capabilities.

**Boundary:** The runtime is paper-only, advisory-only, human-in-the-loop, and in-memory only. It does not implement SQL migration, database writes, Supabase client/runtime, production Supabase, deployment, billing/payment runtime, membership/subscription runtime, authentication runtime, live market data, external API calls, broker execution, real-money trading, or autonomous real-money execution.

**Contract impact:** Locked endpoint names and the required response envelope are preserved. Dual simulation origins remain `user_recorded` and `system_generated_learning`; Task 008 / M5 remains In Progress.


## 2026-06-06 — Vendor / External Data Source Approval Gate

**Decision:** Harness Engineering approves vendor/API integration capability as a future HK Alpha Team product direction in principle, but every specific vendor, vendor API, paid data source, production external service, broker integration, payment provider, authentication provider, live data provider, deployment provider, or third-party service requires separate discussion, current-source/web verification where facts may change, documented Evidence Closure, and explicit Harness Engineering approval before it may be selected, connected, implemented, or required.

**Rationale:** HK Alpha Team may eventually need market data, fundamentals, news, sentiment, AI/model, search/web data, billing, auth, hosting, notification, broker-sandbox, or other third-party services. Vendor choices can affect cost, licensing, redistribution rights, privacy, retention, security, reliability, auditability, investment recommendations, simulations, billing, entitlements, and user-facing claims, so they must be reviewed explicitly before implementation.

**Task 008I boundary:** Task 008I does not connect vendors, call live market data, call external APIs, add API keys/secrets, add vendor SDKs, create production third-party dependencies, or add payment, auth, broker, deployment, market data, news, financial data, or AI/model vendor integrations. Only local/in-memory behavior is implemented.

## 2026-06-06 — Task 008J Persistence Schema Alignment and Intent Boundary

Decision: Task 008J introduces Simulation Desk persistence schema alignment, a local/test-only additive migration draft, and a local-only persistence-intent adapter boundary.

Rationale: Task 008I runtime records should not move directly into a real database write path. The project needs a deterministic, reviewable mapping layer that preserves simulation origin, advisory-only boundaries, recommendation lineage, learning proposal reviewability, append-only audit previews, and loss visibility before any future persistence adapter is approved.

Boundaries:

- No real database writes are approved.
- No production Supabase connection is approved.
- No Supabase client runtime is added.
- No vendor/API calls, broker integrations, deployment, billing/auth runtime, membership runtime, secrets, real-money trading, or autonomous real-money execution are approved.
- Future production persistence or a Supabase adapter requires a separate explicit PR scope and Evidence Closure.
- Codex does not self-approve this governance-sensitive change.

## 2026-06-07 — Decision: Standing Non-Real-Money Productization Approval Baseline

**Decision:** Harness Engineering approves non-real-money productization categories to proceed through scoped implementation PRs. This standing approval covers non-real-money product capabilities in principle; it does not claim those capabilities are already implemented and does not remove per-PR review requirements.

**Approved in-principle examples:**

- local/test persistence;
- Supabase adapter / production Supabase work;
- endpoint runtime expansion;
- deployment preparation;
- auth/account flows;
- membership/subscription/billing work;
- vendor/API integration;
- live data integration.

**Required for each PR:** Every productization PR still needs a scoped implementation PR, explicit scope definition, validation/tests, Evidence Closure, security/secrets handling, current-source verification where facts may change, and post-merge verification. PRs that rely on current, external, legal, vendor, pricing, availability, security, deployment, billing, auth, or compliance facts must verify those facts against current sources before making product claims or implementation choices. Every specific vendor/API/provider also requires separate discussion and explicit Harness Engineering approval in the scoped PR before it is selected, connected, implemented, required, or made production-facing/user-facing.

**Hard prohibitions:** This standing approval does not authorize real-money trading, autonomous real-money execution, autonomous broker execution, real-money account connection, secrets leakage, or hidden or irreversible investment actions.

## 2026-06-10 — Decision: Close M5 as Non-Production Simulation Desk MVP and Establish Production Supabase Readiness Gate

**Context:** Tasks 008K, 008L, and 008M added local/test-only PostgreSQL evidence for Simulation Desk paper-order persistence payloads, explicit local/test endpoint persistence wiring, and persisted paper-portfolio readback while preserving default in-memory runtime and no-production boundaries.

**Decision:** Task 008 / Milestone M5 is closed as a non-production, advisory-only Simulation Desk MVP. The project may begin a future Production Supabase Readiness Package, but production Supabase remains blocked until explicit Harness Engineering approval and gate evidence.

**Production Supabase Gate:** Future PRs must receive explicit Harness approval before any production Supabase connection, hosted credentials or repository/environment secrets, production migration application, Supabase client runtime, production runtime persistence, or user-facing production data path. Remote schema changes must go through migration files rather than direct production dashboard/SQL-editor changes. A production migration plan must include apply order, rollback/repair considerations, ownership, and post-deploy verification. RLS/security review, secrets handling, CI evidence, Evidence Closure, and post-merge verification are mandatory before production persistence can be approved.

**Boundary:** This decision does not implement production Supabase, does not add a Supabase client, does not add hosted credentials or secrets, does not apply production migrations, does not add production runtime persistence, does not connect vendors or live market data, does not add broker integration, and does not authorize real-money trading, autonomous real-money execution, autonomous broker execution, real-money account connectivity, secrets leakage, or hidden/irreversible investment actions.

## 2026-06-10 — Decision: Adopt Implementation-First Delivery Balance Guardrail

**Context:** Harness Engineering requested a better balance between planning/docs and executable implementation after M5 closeout, while preserving governance gates for production-sensitive, security-sensitive, contract-changing, vendor/API, production Supabase, secrets, deployment, auth/payment, broker, and real-money boundaries.

**Decision:** Future HK Alpha Team task recommendations should default to executable, testable product capability for ordinary non-real-money product work. Codex prompts should state the primary deliverable, and docs-only recommendations should first check whether a safe implementation-limited vertical slice can deliver runnable behavior, API-visible output, tests, and CI evidence without crossing hard prohibitions. Docs-only recommendations must explain why implementation-limited delivery is not safe, not appropriate, or blocked by a required governance gate.

**Delivery mix target:** Ordinary scoped non-real-money product tasks should aim for 65–75% executable implementation/tests/runtime behavior/API-visible output, 15–20% validation/CI/safety checks/Evidence Closure, and 10–15% concise documentation/status/progress/decision updates, unless the task scope or a governance gate requires a different balance.

**Boundary:** This decision does not weaken advisory-only rules, contract locks, security/secrets gates, production Supabase gates, vendor/API approval requirements, deployment/auth/payment gates, broker prohibitions, real-money trading prohibitions, or Harness Engineering review authority.
