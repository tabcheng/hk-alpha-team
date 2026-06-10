# Progress Log

## 2026-05-21

- Project Instructions v0.1 completed.
- Core HK Alpha Team departments defined.
- Simulation Investment Desk added.
- Investment Strategy Office added.
- GitHub-first documentation workflow selected.
- Codex will be used to generate and maintain repository files.
- PR #1 foundation docs created and now being aligned with Harness Engineering review.

## 2026-05-21 — Tasks 002-004 Design Documentation Completed

- Added Supabase schema design doc (`docs/08-supabase-schema-design.md`).
- Added API and agent contract doc (`docs/09-api-and-agent-contracts.md`).
- Added MVP implementation plan (`docs/10-mvp-implementation-plan.md`).
- Added current project status snapshot (`docs/11-project-status.md`).
- Added codex task definition for Task 004 (`codex-tasks/004-create-mvp-implementation-plan.md`).

Scope check: documentation-only, no implementation code, no deployment config, no external data integration.


## 2026-05-22 — PR #2 Revision (Harness Review Follow-up)

- Added design-only SQL draft section to schema doc for migration-shape validation.
- Added minimal JSON validation target rules to API/agent contracts doc.
- Added draft milestone windows to MVP implementation plan for planning clarity.
- Updated project status snapshot date to reflect revision day.

## 2026-05-22 — PR #2 Re-Review Blockers Addressed

- Updated schema doc to use agreed HK Alpha Team canonical primary table names.
- Updated API contract doc to required MVP endpoint set and required response envelope section.
- Added JSON examples for all eight agent departments.
- Aligned MVP plan phases to requested phase model.
- Updated project status to In Review / Pending Merge for Tasks 002–004.
- Maintained documentation-only scope.

## 2026-05-22 — PR #2 Final Re-Review Blockers Addressed

- Expanded `docs/08-supabase-schema-design.md` with ERD-level details for each required table.
- Added full `strategy_recommendations` field set for Investment Strategy Office outputs.
- Converted all eight agent examples to one common contract shape in `docs/09-api-and-agent-contracts.md`.
- Added final strategy recommendation JSON example using the exact required response envelope.
- Expanded `docs/11-project-status.md` with Current Phase, Tasks 001–010 table, Milestones M0–M7, and Current Decisions summary.


## 2026-05-22 — Deep Audit Contract Expansion

- Added endpoint-by-endpoint required details and explicit error envelope/codes in `docs/09-api-and-agent-contracts.md`.
- Added strict governance rules and source-of-truth map in `AGENTS.md`.
- Added MVP acceptance criteria in `docs/10-mvp-implementation-plan.md`.
- Added schema migration planning note in `docs/08-supabase-schema-design.md`.

## 2026-05-22 — PR #3 Governance Hardening and Task 005 Preparation

- Added initial intent capture in `docs/12-initial-conversation-brief.md`.
- Added reusable PR checklist and large PR policy in `docs/13-pr-review-checklist.md`.
- Added reusable Codex prompt template in `docs/14-codex-task-template.md`.
- Added Task 005 card in `codex-tasks/005-create-supabase-migration-draft.md`.
- Updated `docs/11-project-status.md` to reflect PR #2 merged and Task 005 ready-to-start.
- Maintained documentation-only scope and contract lock compliance.

## 2026-05-24 — PR #4 Supabase Migration Draft and Contract Validation Baseline

- Added initial migration draft SQL at `supabase/migrations/0001_create_core_schema.sql` with canonical v1 tables, key constraints, and baseline indexes.
- Added `scripts/validate_contracts.py` to validate locked schema names, endpoint names, envelope keys, and strategy labels against source-of-truth docs.
- Added GitHub Actions workflow `.github/workflows/contract-check.yml` to run contract validation on push/PR.
- Added `docs/15-migration-assumptions.md` documenting interpretation assumptions and explicit out-of-scope boundaries.
- Updated `docs/11-project-status.md` to mark Task 005 and Milestone M2 as In Progress.


## 2026-05-26 — PR #5 Phase 2 SQL Validation and Review Hardening

- Added `scripts/check_migration_sql.sh` to execute the draft migration against a local/test PostgreSQL database and verify baseline table/constraint checks.
- Added `.github/workflows/sql-migration-check.yml` to run migration execution validation in CI using `postgres:16`.
- Added `docs/16-local-sql-validation.md` with local run steps, CI behavior, and scope boundaries.
- Updated `docs/13-pr-review-checklist.md` with a review-thread closure gate to prevent unresolved review comments/threads from being missed.
- Recorded decision to defer branch-protection plan upgrade during Phase 2 and continue manual governance controls.


## 2026-05-26 — PR #6 Phase 2 Closeout and Backend Skeleton Foundation

- Closed Task 005 and Milestone M2 after PR #5 merge validation results (`contract-check` and `sql-migration-check` passing).
- Started Task 006 / Milestone M3 with FastAPI backend skeleton implementation.
- Added two required endpoints for this phase start: `GET /health` and `GET /api/v1/project-status`.
- Added shared success/error response envelope helpers aligned to `docs/09-api-and-agent-contracts.md`.
- Added backend pytest coverage and GitHub Actions backend test workflow.

## 2026-06-01 — PR #8 Analyze-Stock Stub, Contract Hardening, and Mobile-First Strategy

- Added `POST /api/v1/analyze-stock` as a contract-first FastAPI stub for Phase 4 readiness.
- Added validation error envelope handling and backend tests for analyze-stock success and invalid requests.
- Documented the analyze-stock stub contract in `docs/09-api-and-agent-contracts.md`, `docs/17-backend-skeleton.md`, and `docs/19-first-analysis-workflow-stub.md`.
- Added `docs/18-mobile-first-environment-strategy.md` to formalize CI-first, mobile-review operation without production Supabase, Railway, secrets, or desktop setup requirements.
- Updated project status and contract-related governance artifacts while preserving advisory-only and no-real-money-execution boundaries.

## 2026-06-02 — Codex PR Factory Governance and PR #8 Status Sync

- Added `docs/20-codex-pr-factory.md` to define the Codex PR Factory governance workflow, task classes, workflow roles, required gates, PR body expectations, evidence language, and source-of-truth-based next-step handling.
- Updated `docs/06-codex-workflow.md` to reference the Codex PR Factory as the detailed governance layer for task-to-PR execution.
- Updated `README.md` documentation map entries so the new Factory workflow and existing migration/SQL validation docs are discoverable from the source-of-truth map.
- Synchronized `docs/11-project-status.md` after PR #8 merge by marking Task 006 / Milestone M3 completed, keeping the Current Phase parser-safe at Phase 3, and leaving Phase 4 planned for a dedicated task opened from current GitHub source-of-truth review.
- Preserved the parser-safe `## Current Phase` format by keeping the line after the heading as only the bold phase name and moving explanatory details into status notes and Latest Review Update.
- Maintained governance documentation plus backend test alignment scope: no runtime backend implementation, frontend implementation, Phase 4 analysis logic, market data integration, production Supabase, Railway deployment, broker API integration, secrets, or real-money trading automation. Backend project-status test coverage was strengthened to assert parser-safe current-phase formatting and synchronized project-status expectations without mirroring `status_reader.py` parsing behavior.


## 2026-06-02 — Phase 4A First Analysis Workflow Skeleton Start

- Started Task 007 / Milestone M4 with a deterministic local-only First Analysis Workflow Skeleton for `POST /api/v1/analyze-stock`.
- Replaced Phase 3 stub-only endpoint internals with explicit local workflow stages for normalization, static stock context, placeholder scoring, advisory summary, reasons, risks, invalidation conditions, human decision framing, and workflow trace metadata.
- Added backend workflow unit coverage and updated API tests while preserving the locked endpoint name and required success/error response envelopes.
- Kept Phase 4A implementation-limited: no live market data, external APIs, production Supabase, persistence writes, paper order creation, broker integration, secrets, or real-money trading automation.


## 2026-06-02 — PR #10 Contract Documentation Alignment

- Updated `docs/09-api-and-agent-contracts.md` so the canonical `POST /api/v1/analyze-stock` contract reflects current Phase 4A `phase4a_skeleton` runtime behavior.
- Kept the Phase 3 `stub_only` analyze-stock contract as historical context only, not current canonical behavior.
- Updated related README, task, status, and decision artifacts while preserving the locked endpoint name, required response envelopes, advisory-only framing, and no-production-integration boundaries.


## 2026-06-02 — Phase 4B Department Adapter Start

- Started Phase 4B inside Task 007 / Milestone M4 by adding deterministic local-only department scoring adapters for all eight HK Alpha Team departments.
- Refactored the analyze-stock workflow to consume adapter outputs that mirror the locked common agent output shape, while preserving the locked endpoint name, required success/error response envelope, `analysis_status`, and `workflow_phase`.
- Added local-only `department_outputs` review metadata and documented that it is non-persistent adapter preview output, not database-backed `agent_outputs` records or live investment research.
- Kept Phase 4B implementation-limited: no live market data, external APIs, production Supabase, persistence writes, paper order creation, broker integration, secrets, or real-money trading automation.

## 2026-06-03 — Phase 4C Agent Handoff Mapping Start

- Started Phase 4C inside Task 007 / Milestone M4 by adding deterministic local-only adapter-to-agent-run handoff mapping for the existing Phase 4B department adapter outputs.
- Added internal preview mapping coverage for all eight HK Alpha Team departments, including future run-level intent, future output-level payload, and current non-persistent runtime state.
- Kept the public analyze-stock response unchanged while preserving the locked endpoint name, required success/error response envelope, `analysis_status = "phase4a_skeleton"`, and `workflow_phase = "Phase 4A — Deterministic First Analysis Workflow Skeleton"`.
- Kept Phase 4C implementation-limited: no production Supabase connection, no persistence writes, no schema migration, no agent-runs retrieval endpoint runtime, no strategy recommendation persistence, no broker integration, no paper orders, no secrets, and no real-money trading automation.

## 2026-06-03 — Phase 4C Coverage Validation Correction

- Strengthened Phase 4C handoff mapping validation so local-only previews require exactly one adapter output for each of the eight HK Alpha Team departments.
- Added duplicate, missing, extra, and unknown department collection tests while preserving the internal-only no-persistence boundary and unchanged public analyze-stock response.

## 2026-06-03 — Phase 4D Handoff Preview Exposure Decision Start

- Started Phase 4D inside Task 007 / Milestone M4 as documentation-only governance work for Phase 4C handoff preview exposure.
- Documented that Phase 4C handoff previews remain internal-only for now and public exposure through `POST /api/v1/analyze-stock` is deferred until Harness Engineering explicitly approves a future contract-changing PR.
- Preserved the current public analyze-stock payload and avoided changes to `docs/09-api-and-agent-contracts.md`, runtime code, API tests, persistence behavior, production Supabase, endpoint runtime, broker integration, secrets, paper orders, and real-money trading automation.


## 2026-06-03 — Phase 4E Internal Workflow Validation Start

- Started Phase 4E inside Task 007 / Milestone M4 as an implementation-limited, local-only internal validation expansion.
- Added validation scope for consistency across the Phase 4A analyze-stock workflow payload, Phase 4B department adapter outputs, and Phase 4C local-only handoff previews while preserving the Phase 4D internal-only exposure decision.
- Kept public analyze-stock response semantics unchanged: no public handoff preview fields, no `docs/09-api-and-agent-contracts.md` update, no agent-runs endpoint runtime, no persistence, no production Supabase, no broker integration, no secrets, no paper orders, and no real-money trading automation.

## 2026-06-04 — Phase 4F Fixture-Backed Validation and M4 Readiness Start

- Started Phase 4F inside Task 007 / Milestone M4 as implementation-limited, local-only fixture-backed internal validation work.
- Added deterministic fixture coverage for canonical passing analyze-stock workflow payloads and targeted drift/failure scenarios across Phase 4A payload fields, Phase 4B department outputs, Phase 4C handoff previews, the Phase 4D internal-only public exposure boundary, and the Phase 4E validation layer.
- Added an M4 readiness matrix documenting satisfied criteria, open closeout items, explicit out-of-scope items before Task 008, and changes requiring Harness Engineering approval.
- Preserved the no-public-payload-change, no-persistence, and no-production-boundary: no public handoff preview fields, no `docs/09-api-and-agent-contracts.md` update, no endpoint runtime, no persistence writes, no production Supabase, no broker integration, no secrets, no paper orders, and no real-money trading automation.

## 2026-06-04 — Phase 4G M4 Closeout Readiness Review

- Completed Phase 4G as a documentation-only, governance-sensitive readiness review for Task 007 / Milestone M4 after Phase 4A through Phase 4F.
- Determined that M4 can close while Phase 4C handoff previews remain internal-only because public handoff preview exposure is not required for M4 closeout and remains a separate future contract-changing PR requiring Harness Engineering approval plus same-PR `docs/09-api-and-agent-contracts.md`, runtime, and API test updates.
- Assessed Phase 4E internal validation and Phase 4F fixture-backed validation as sufficient for Task 008 handoff planning readiness, while not validating or implementing Simulation Desk MVP runtime, paper portfolios, paper orders, strategy recommendation persistence, production Supabase, live data, broker integration, or real-money trading automation.
- Marked Task 007 / Milestone M4 Completed in `docs/11-project-status.md`; kept Task 008 Simulation Desk MVP Planned and M5 Planned.
- Preserved the no-public-payload-change, no-`docs/09`-change, no-persistence, no-production-Supabase, no-endpoint-runtime, no-broker, no-paper-order, no-secrets, and no-real-money-trading boundaries.

## 2026-06-04 — Task 008A Simulation Desk MVP Boundary and Contract Planning Start

- Started Task 008A inside Task 008 / Milestone M5 as documentation-only, governance-sensitive Simulation Desk MVP boundary and contract planning.
- Added a Task 008A planning source-of-truth document defining Simulation Desk MVP boundaries, `docs/04` operating-rule alignment, `docs/08` simulation schema references, `docs/09` locked endpoint references, the first minimum M5 slice, approval gates, and follow-up PR sequence.
- Marked Task 008 / Milestone M5 In Progress for planning only while preserving Task 007 / Milestone M4 as Completed.
- Preserved no runtime, no persistence, no production Supabase, no broker, no real-money trading, no secrets, no live market data, no endpoint implementation, no paper-order creation, and no paper-portfolio runtime boundaries.

## 2026-06-04 — Task 008B Local Simulation Contract Fixtures, Schemas, and Validation Matrix

- Implemented Task 008B as a pure local-only Simulation Desk contract validation slice.
- Added deterministic fixtures, individual-record validation, collection validation, and a validation matrix/report helper for `paper_portfolio`, `paper_order_intent`, `paper_position`, `portfolio_snapshot`, `trade_review`, `learning_proposal`, and `audit_event`.
- Added positive and negative tests for required record types, required fields, unknown record types, invalid quantities/statuses, hidden losing outcomes, auto-applied learning proposals, enabled boundary flags, full matrix coverage, and non-mutating validation.
- Added `docs/29-task-008b-local-simulation-contract-fixtures.md` to document fixture coverage, validation matrix coverage, non-goals, and Task 008C entry criteria.
- Preserved the local-only boundary: no IO, HTTP, database access, production Supabase, endpoint handlers, persistence, paper order creation, broker integration, live market data, or real-money trading automation.

## 2026-06-04 — Task 008B Review Follow-up

- Tightened Task 008B fixture helpers so endpoint-reference lists are isolated per fixture record rather than sharing a mutable object.
- Strengthened validators to self-check non-mutation with deep-copy comparisons and to fail when locked endpoint references are missing, not only when unknown endpoint names are present.
- Added targeted tests for deterministic fixture generation, isolated mutable fixture fields, and missing locked endpoint references while preserving all local-only/no-runtime boundaries.

## 2026-06-04 — Task 008C Local Paper Order Validation Service / Stub

- Started and completed Task 008C as an implementation-limited, governance-sensitive, pure local-only Simulation Desk paper-order validation service/stub.
- Added local in-memory validation helpers for paper-order-intent-like inputs, including required `portfolio_id`, `symbol`, `side`, and `quantity` checks; optional `order_type` and `limit_price` checks; conservative `0700.HK`-style symbol validation; optional local portfolio registry matching; no-order-created result fields; and false boundary flags.
- Added positive and negative tests for valid paper-order intents, market buy/sell, limit orders, zero quantity, local registry match, non-mutating validation, missing/malformed fields, invalid side/order type, negative numeric values, forbidden runtime/persistence/production/broker/real-money/external/secrets flags, and inputs implying actual order creation.
- Preserved Task 008C pure local-only scope: no endpoint runtime, no FastAPI route, no HTTP, no persistence, no database writes, no production Supabase, no Supabase client, no broker, no paper-order creation, no paper-portfolio runtime, no strategy recommendation persistence, no secrets, no live market data, no external APIs, no production infrastructure, and no real-money trading automation.
- Kept Task 007 / Milestone M4 Completed and Task 008 / Milestone M5 In Progress.

## 2026-06-04 — Task 008C Review Follow-up

- Fixed the Task 008C local-only boundary flag bypass by deriving paper-order validation boundary flags from inherited Task 008B `BOUNDARY_FLAG_NAMES` plus Task 008C-specific flags.
- Added regression tests proving top-level and nested `supabase_client_required=true` and `broker_api_called=true` fail validation.
- Preserved Task 008C pure local-only scope: no endpoint runtime, no FastAPI route, no HTTP, no persistence, no database writes, no production Supabase, no Supabase client, no broker integration, no paper-order creation, no secrets, and no real-money trading automation.

## 2026-06-04 — Task 008D Persistence Gate Readiness Planning

- Added Task 008D persistence gate readiness and migration alignment planning for the Simulation Desk MVP.
- Mapped Task 008B local-only Simulation Desk fixture record shapes and Task 008C local paper-order intent validation to canonical `docs/08-supabase-schema-design.md` tables.
- Mapped locked `docs/09-api-and-agent-contracts.md` endpoint names to future approval gates without implementing endpoint runtime.
- Recorded explicit approval gates before SQL migration, Supabase client setup, production Supabase, persistence writes, endpoint runtime, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit-event creation, broker integration, or any real-money capability.
- Scope remains documentation-only and planning-only: no migration, no persistence, no endpoint runtime, no production Supabase, no broker, no paper-order creation, no real-money trading automation, no secrets, and no live market data.

## 2026-06-05 — PR Review Evidence Closure Protocol Governance Update

- Added `docs/32-pr-review-evidence-closure-protocol.md` as a documentation-only, governance-sensitive full PR review evidence protocol.
- Extended the Codex PR Factory and mandatory full PR review workflow to classify closed evidence, reduced-risk evidence, and residual limitations.
- Recorded explicit review rules for public web availability, authenticated GitHub source-of-truth fallback, CI depth, local rerun limitations, branch protection visibility, expected-head-SHA merge locking, unresolved review threads, and post-merge source-of-truth verification.
- Preserved Task 008 / Milestone M5 as In Progress and did not start Task 008E; no runtime, persistence, migration, Supabase, production infrastructure, broker integration, secrets, or real-money trading automation was introduced.

## 2026-06-05 — PR Review Checklist Evidence Closure Correction

- Updated `docs/13-pr-review-checklist.md` so the reusable checklist enforces the Evidence Closure Protocol from `docs/32-pr-review-evidence-closure-protocol.md`.
- Added concise checklist items for public web availability, authenticated GitHub fallback, latest reviewed head SHA, branch freshness, CI depth, workflow conclusions, job/log inspection requirements, exact command outputs, local rerun classification, branch protection visibility, unresolved review thread count, expected-head-SHA merge lock, and post-merge source-of-truth verification.
- Preserved documentation-only and governance-only scope: no backend runtime, frontend, `docs/09`, schema/migration, workflow, production infrastructure, broker, real-money trading automation, or Task 008E work was introduced.

## 2026-06-05 — Task 008E Local Simulation Desk Readiness Report

**Scope:** Added an implementation-limited, pure local-only Simulation Desk readiness report that aggregates Task 008B local fixture validation evidence and Task 008C local paper-order intent validation evidence.

**Validation behavior:** The readiness helper builds deterministic in-memory evidence, preserves canonical schema table names, references locked MVP endpoint names without implementing endpoints, records approval gates as not crossed, keeps `would_create_order = false`, and validates that all forbidden boundary flags remain false.

**Boundaries:** Task 008E does not add or authorize SQL migration, endpoint runtime, persistence writes, Supabase client setup, production Supabase, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit-event creation, broker integration, live market data, external API calls, secrets, production deployment, autonomous order placement, or real-money trading automation.

**Status:** Task 008 / Milestone M5 remains In Progress. Task 008E is readiness evidence only; any Task 008F gate crossing requires separate Harness Engineering approval and same-PR source-of-truth updates.

## 2026-06-05 — Task 008F Local Simulation Desk Scenario Pack and Gate Decision Matrix

**Scope:** Added an implementation-limited, governance-sensitive, pure local-only Simulation Desk scenario pack that aggregates Task 008B fixture validation evidence, Task 008C local paper-order intent validation evidence, and Task 008E readiness aggregation evidence.

**Validation behavior:** The scenario pack includes a valid HK paper-order intent scenario, malformed `700.HK` symbol fail-safe evidence, invalid side, invalid quantity, invalid order type, invalid limit price, missing portfolio id, Task 008E readiness aggregation, canonical schema table references, locked endpoint traceability, false approval gates, false forbidden boundary flags, loss visibility evidence, learning proposal reviewability evidence, and a next-gate matrix that approves no gate.

**Boundaries:** Task 008F does not add or authorize SQL migration, endpoint runtime, persistence writes, Supabase client setup, production Supabase, paper-order creation, paper-portfolio runtime, strategy recommendation persistence, audit-event creation, broker integration, live market data, external API calls, secrets, production deployment, autonomous order placement, or real-money trading automation.

**Status:** Task 008 / Milestone M5 remains In Progress. Task 008F is local scenario-pack/readiness evidence only; any Task 008G gate crossing requires separate explicit Harness Engineering approval and same-PR source-of-truth updates.


## 2026-06-05 — Task 008F Review Follow-up

- Strengthened the Task 008F scenario-pack validator so stored valid and invalid paper-order scenario evidence is revalidated against the local Task 008C helper instead of being trusted only by status strings.
- Added deeper fail-safe checks for hidden losing records, auto-applied learning proposal evidence, exact locked endpoint reference preservation, and complete next-gate direction preservation.
- Added regression tests for stale valid/invalid scenario inputs, hidden loss evidence, auto-applied learning proposals, missing next-gate directions, and duplicate locked endpoint references.
- Preserved Task 008F pure local-only scope: no runtime, no persistence, no Supabase client or production Supabase connection, no endpoint handler, no paper-order creation, no paper-portfolio runtime, no strategy persistence, no audit-event database creation, no live market data, no external API calls, no secrets, no deployment, no autonomous order placement, and no real-money trading automation.


## 2026-06-05 — Task 008F Valid Scenario Stored Evidence Review Fix

- Fixed the PR #25 review blocker by requiring the stored valid paper-order scenario `validation_result` to be a mapping, to keep `would_create_order = false`, and to exactly match fresh local Task 008C revalidation of the scenario `input_order`.
- Added regression coverage proving edited stored valid-scenario evidence fails when `would_create_order` is set true, when the stored symbol changes to `700.HK`, when side is changed to an invalid value, when quantity is changed negative, and when a stored boundary flag claims persistence.
- Preserved Task 008F local-only scope and did not modify `docs/09-api-and-agent-contracts.md`, `docs/08-supabase-schema-design.md`, migrations, Supabase clients, endpoint runtime, persistence, paper-order creation, paper-portfolio runtime, strategy persistence, audit-event runtime, broker/live-data/external API integrations, secrets, deployment, autonomous order placement, or real-money trading automation.

## 2026-06-06 — Task 008G Dual Simulation Origin Product Foundation

- Started Task 008G after Task 008F to align source-of-truth docs, schema/API contract planning, and local-only validation around the corrected Simulation Desk product concept.
- Documented two distinct paper-only origins: `user_recorded` records entered by Harness Engineering / a human user, and `system_generated_learning` simulations generated by the Simulation Investment Desk to validate recommendation quality and produce reviewable learning proposals.
- Added local validation coverage for allowed origins, required user/source fields, required original recommendation/thesis/score linkage fields, human-review-only learning proposal behavior, loss visibility, historical recommendation preservation, advisory-only framing, and non-mutation of payloads.
- Preserved boundaries: no FastAPI endpoint runtime, no persistence writes, no production Supabase connection, no secrets, no broker execution APIs, no real-money trading, no autonomous real-money order placement, no live market data, no deployment, no auto-applied learning proposals, and no hidden or overwritten losing simulations.
- Task 008 / M5 remains In Progress and is not claimed complete.

## 2026-06-06 — Task 008H Commercial Readiness and Subscription Product Governance Baseline

- Added documentation-only commercial-readiness governance before runtime, persistence, membership, subscription, billing, deployment, or user-facing product work begins.
- Recorded that Harness Engineering treats HK Alpha Team as a serious commercial product candidate with possible future membership/subscription offerings, subject to explicit PRs and evidence-based review.
- Documented GitHub `main` source-of-truth expectations, web verification for uncertain/changeable facts, full PR review protocol, Evidence Closure language, no-100%-certainty rule, commercial-readiness roadmap, and Codex/reviewer role boundaries.
- Preserved the Task 008G dual Simulation Desk origin model: `user_recorded` and `system_generated_learning` remain paper-only, advisory-only, auditable, and human-in-the-loop.
- Preserved out-of-scope boundaries: no frontend/UI, backend runtime, FastAPI endpoints, persistence writes, SQL migrations, Supabase client or production Supabase connection, billing/payment integration, membership/subscription runtime, authentication runtime, live market data, broker integration, deployment configuration, secrets, real-money trading, autonomous real-money execution, or locked contract renames.
- Task 008 / M5 remains In Progress and is not claimed complete.

## 2026-06-06 — Task 008I Dual-Origin Simulation Desk Runtime Slice

- Added a non-production FastAPI runtime slice for the locked Simulation Desk endpoints: `POST /api/v1/simulation/paper-orders` and `GET /api/v1/paper-portfolios/{portfolio_id}`.
- Added deterministic process-local in-memory recordkeeping for paper order records, paper portfolio snapshots, audit-event previews, and reviewable learning-proposal previews.
- Preserved both Task 008G simulation origins: `user_recorded` and `system_generated_learning`.
- Confirmed Task 008I does not add SQL migration, Supabase persistence, production Supabase, deployment, billing/payment runtime, membership/subscription runtime, auth runtime, live data, external API calls, broker integration, secrets, real-money trading, or autonomous real-money execution.
- Task 008 / M5 remains In Progress.


## 2026-06-06 — Task 008I Vendor / External Data Source Boundary

- Recorded Harness Engineering approval for vendor/API capability as a future product direction in principle.
- Added the Vendor / External Data Source Approval Gate: every specific vendor, vendor API, paid data source, production external service, broker integration, payment provider, authentication provider, live data provider, deployment provider, or third-party service requires separate discussion, current-source/web verification where facts may change, Evidence Closure documentation, and explicit Harness Engineering approval before implementation.
- Confirmed Task 008I does not connect vendors, call live market data, call external APIs, add API keys/secrets, add vendor SDKs, create production third-party dependencies, or add payment, auth, broker, deployment, market data, news, financial data, or AI/model vendor integrations.
- Task 008 / M5 remains In Progress.

## 2026-06-06 — Task 008J Simulation Desk Persistence Alignment

- Added a Task 008J documentation page covering purpose, source-of-truth review, runtime-to-persistence mapping, 0001 schema gaps, local/test-only migration boundary, adapter boundary design, validation strategy, risk areas, and Task 008K entry criteria.
- Added `supabase/migrations/0002_align_simulation_desk_persistence_fields.sql` as an additive local/test-only draft that preserves canonical table names and does not alter `0001_create_core_schema.sql`.
- Added a local-only Simulation Desk persistence-intent boundary that builds deterministic payloads for future `paper_orders`, `portfolio_snapshots`, `learning_proposals`, and `audit_events` targets without database, disk, Supabase, vendor, or network writes.
- Added deterministic tests for both approved simulation origins, unsafe boundary rejection, reviewable/non-auto-applied learning proposal previews, append-only audit event previews, portfolio snapshot mapping, no Supabase/vendor/network/disk dependency, and runtime response envelope continuity.
- Updated local SQL validation to execute migration files in lexical order so `0001` and `0002` are validated together where PostgreSQL is available.
- Task 008 / M5 remains In Progress; production Supabase, Supabase client runtime, runtime persistence writes, vendor/API integration, broker integration, billing/auth/deployment runtime, secrets, autonomous real-money execution, and real-money trading remain out of scope.

## 2026-06-06 — Task 008J PR #30 Blocker Closure

- Resolved the `docs/08` migration-planning contradiction by clarifying that the earlier schema-design PR was documentation-only, while Task 008J may add a local/test-only additive migration draft that is not approved for production Supabase.
- Resolved `docs/11` status drift by distinguishing a local/test-only SQL migration draft from production migration application, production Supabase connection, Supabase client runtime, and runtime persistence writes.
- Aligned `0002` lineage fields with canonical UUID/FK semantics and preserved runtime string fixture lineage in JSON intent metadata.
- Expanded migration validation expectations to check Task 008J UUID lineage column types and foreign-key constraints where PostgreSQL tooling is available.

## 2026-06-06 — Task 008J PR #30 SQL Validation Runbook Closure

- Updated `docs/16-local-sql-validation.md` to match the current `scripts/check_migration_sql.sh` behavior after Task 008J.
- Clarified that PR #5 introduced baseline local/test SQL validation for `0001`, while Task 008J expands validation to all migration files in lexical order, including local/test-only `0002`.
- Documented Task 008J validation coverage for additive columns, UUID lineage column types, lineage foreign keys, and additive indexes.
- Reconfirmed that local SQL validation does not approve production Supabase application, Supabase client runtime, runtime persistence writes, secrets, vendor/API calls, broker integration, deployment, billing/payment/auth runtime, real-money trading, or autonomous real-money execution.

## 2026-06-07 — PR #31 Source-of-Truth Approval Alignment

- Clarified the standing non-real-money productization approval baseline so GitHub source-of-truth docs no longer read as if production/service/vendor/auth/billing/deployment work is categorically blocked by default.
- Removed the over-conservative documentation interpretation that blocked product progress after Harness Engineering approved non-real-money scope in principle.
- Prepared Task 008K direction toward a local/test PostgreSQL persistence adapter and write/read roundtrip unless review finds blockers.
- Preserved the per-vendor explicit approval gate: every specific vendor/API/provider requires separate discussion and explicit Harness Engineering approval in the scoped PR before it is selected, connected, implemented, required, or made production-facing/user-facing.
- Reconfirmed current implementation status: no production Supabase connection, Supabase client, runtime persistence writes, vendor/API integration, payment/auth/deployment runtime, broker integration, real-money automation, or committed secrets.

## 2026-06-07 — Task 008K Local/Test PostgreSQL Persistence Adapter

- Added a local/test-only PostgreSQL adapter for Simulation Desk paper-order persistence payloads using Task 008J persistence-intent shape as the input boundary.
- Added write/read roundtrip coverage for both approved origins: `user_recorded` and `system_generated_learning`.
- Added local/test schema alignment for `paper_orders.historical_recommendation_fields_json` so original recommendation metadata, source metadata, boundary flags, and outcome preview metadata can be preserved through PostgreSQL.
- Added ephemeral PostgreSQL service coverage to backend CI so adapter tests run without hosted Supabase credentials or production infrastructure.
- Reconfirmed Task 008K does not add production Supabase connection logic, Supabase hosted credentials, vendor/API calls, live market data, broker integration, broker execution APIs, real-money trading, autonomous real-money execution, real-money account connectivity, billing/payment runtime, membership runtime, auth runtime, deployment config, frontend/UI, or secrets.
- Task 008 / M5 remains In Progress; this PR is one local/test persistence step and does not claim full Simulation Desk MVP completion.


## 2026-06-07 — Task 008K PR #33 Destructive Reset Blocker Closure

- Tightened PostgreSQL roundtrip tests so destructive reset is authorized only by `HK_ALPHA_TEST_POSTGRES_DSN`; `DATABASE_URL` alone is ignored and cannot trigger drop/create database operations.
- Added test-only database-name guards accepting only `hk_alpha_validation`, `hk_alpha_test`, or names starting with `hk_alpha_validation_` / `hk_alpha_test_` before reset logic can run.
- Added regression tests proving `DATABASE_URL` cannot trigger destructive reset, unsafe explicit DSNs are skipped before destructive SQL, and approved local/test database names are allowed.
- Hardened `scripts/check_migration_sql.sh` with the same test-only database-name boundary for local SQL validation.
- Reconfirmed the fix does not add production Supabase, hosted credentials, Supabase client runtime, vendor/API calls, live market data, broker integration, real-money trading, autonomous execution, or secrets.

## 2026-06-08 — Task 008L Local/Test Endpoint Persistence Wiring

- Added an explicit Simulation Desk persistence mode contract: default `memory`, with opt-in `local_test_postgres` enabled only by `HK_ALPHA_SIMULATION_PERSISTENCE_MODE=local_test_postgres` plus safe `HK_ALPHA_TEST_POSTGRES_DSN`.
- Wired the paper-order endpoint through a local/test dependency-injection path so the default endpoint remains in-memory, while explicit local/test mode builds the Task 008J/008K persistence payload, writes it with the local/test PostgreSQL adapter, and reads back the written paper-order row.
- Added endpoint-level tests covering default memory behavior, `DATABASE_URL` not authorizing persistence, safe failure for missing/unsafe config, `user_recorded` PostgreSQL write/read, `system_generated_learning` PostgreSQL write/read, locked envelope fields, reviewable/non-auto-applied learning previews, losing outcome visibility, and historical recommendation preservation.
- Preserved out-of-scope boundaries: no production Supabase, no Supabase client runtime, no hosted credentials, no vendor/API calls, no live market data, no broker integration, no real-money trading, no autonomous execution, no real-money account connectivity, no billing/auth/deployment/frontend runtime, and no secrets.
- No new `docs/decision-log.md` entry was required because Task 008L stays inside the existing Harness Engineering local/test approval scope and does not introduce a new governance decision.
- Task 008 / M5 remains In Progress and is not claimed complete.

## 2026-06-09 — Task 008M Local/Test Persisted Portfolio Readback

- Added an explicit local/test PostgreSQL read path for `GET /api/v1/paper-portfolios/{portfolio_id}` so paper orders written by the explicit `local_test_postgres` paper-order endpoint path can be read back as portfolio snapshot evidence.
- Preserved default memory behavior: `DATABASE_URL` alone does not authorize persisted writes or readback, and default portfolio snapshots remain process-local in-memory.
- Added adapter and endpoint tests for persisted portfolio consistency across both approved origins, including `user_recorded` source metadata and `system_generated_learning` human-review flags, persisted learning-proposal readback evidence, non-auto-apply behavior, historical recommendation metadata, and losing outcome visibility.
- Preserved safe-failure behavior for missing/unsafe DSN values and unknown persistence modes using contract-compliant configuration errors.
- Reconfirmed Task 008M does not add production Supabase, Supabase client runtime, hosted credentials, vendor/API calls, live market data, broker integration, broker execution APIs, real-money trading, autonomous execution, real-money account connectivity, hidden/irreversible investment actions, billing/payment/auth/deployment/frontend runtime, or secrets.
- No new `docs/decision-log.md` entry was required because Task 008M stays inside the existing Harness Engineering local/test, paper-only, advisory-only, non-real-money approval scope and does not introduce a new governance decision.
- Task 008 / M5 remains In Progress and is not claimed complete.

## 2026-06-10 — Task 008M PR #35 Stable UUID Readback Blocker Closure

- Fixed the local/test PostgreSQL portfolio readback predicate to use the stable `paper_portfolios.portfolio_uuid` identity derived from the runtime `portfolio_id`, instead of non-unique `paper_portfolios.name`.
- Added regression coverage that inserts a decoy `paper_portfolios` row with the same display name but a different stable identity and proves readback returns only the target portfolio order.
- Fixed backend-check expectation mismatches for the current deterministic system-generated-learning fixture values.
- Preserved Task 008M local/test-only scope and did not add production Supabase, Supabase client runtime, hosted credentials, vendor/API calls, live market data, broker integration, real-money trading, autonomous execution, real-money account connectivity, hidden/irreversible investment actions, or secrets.

## 2026-06-10 — Task 008N M5 Closeout Readiness and Production Supabase Readiness Gate

- Added `docs/42-task-008n-m5-closeout-and-production-supabase-readiness-gate.md` as the Task 008N source-of-truth audit after Tasks 008K, 008L, and 008M.
- Closed Task 008 / Milestone M5 as a non-production, advisory-only Simulation Desk MVP based on current endpoint, local/test PostgreSQL adapter, local/test endpoint persistence, and local/test persisted portfolio readback evidence.
- Recorded that no smallest remaining local/test-only M5 gap was identified; remaining limitations are production-readiness limitations, not M5 blockers.
- Created a formal Production Supabase Readiness Gate for any future Production Supabase Readiness Package: explicit Harness approval remains required before production Supabase connection, hosted credentials/secrets, production migration application, Supabase client runtime, production persistence, or user-facing production data paths.
- Preserved hard prohibitions: no production Supabase implementation, no Supabase client runtime, no hosted credentials or secrets, no production migration application, no vendor/API or live market data integration, no broker integration, no real-money trading, no autonomous execution, no real-money account connectivity, and no hidden or irreversible investment actions.
- Updated `docs/11-project-status.md` to mark Task 008 / M5 Completed while explicitly keeping production Supabase not implemented and not approved.
- Added a `docs/decision-log.md` entry because Task 008N marks M5 closed and creates a formal Production Supabase Readiness Gate.
