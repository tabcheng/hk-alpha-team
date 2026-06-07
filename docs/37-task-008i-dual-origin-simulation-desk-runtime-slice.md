# 37 — Task 008I Dual-Origin Simulation Desk Runtime Slice

## Snapshot Date

2026-06-06

## Purpose

Task 008I implements the first contract-aligned, non-production backend runtime slice for the Simulation Desk MVP after Task 008G and Task 008H.

The slice enables the locked MVP endpoints to accept and return paper-only in-memory Simulation Desk records for both approved simulation origins:

- `user_recorded` — human / Harness Engineering / user-recorded paper trades.
- `system_generated_learning` — HK Alpha Team / Simulation Investment Desk generated paper-only learning simulations used to validate recommendation quality and produce reviewable learning proposals.

## Runtime Added

Task 008I adds FastAPI runtime behavior for:

- `POST /api/v1/simulation/paper-orders`
- `GET /api/v1/paper-portfolios/{portfolio_id}`

Both endpoints preserve the locked success/error envelope from `backend/app/contracts.py`.

## In-Memory Recordkeeping Boundary

The runtime uses deterministic, process-local in-memory recordkeeping only.

It creates:

- deterministic paper order IDs;
- deterministic audit-event preview IDs;
- deterministic record timestamps derived from process-local sequence numbers;
- in-memory paper portfolio snapshots containing recent paper orders and audit-event previews.

The store does not persist to disk, does not write to a database, and resets when the process restarts or tests reset it.

## Dual-Origin Validation

The runtime aligns endpoint validation with the Task 008G origin contract in `backend/app/simulation_origin_contract.py`.

For `user_recorded`, the runtime requires human/user/Harness metadata and user rationale/notes.

For `system_generated_learning`, the runtime requires recommendation lineage, original recommendation fields, original scores, original thesis, entry and exit assumptions, outcome/learning fields, system learning reason, and `requires_human_review = true`.

## Learning Proposal Behavior

`system_generated_learning` records may return a reviewable learning-proposal preview.

The preview must remain review-only:

- `requires_human_review = true`
- `auto_apply = false`
- status is preview-only / not applied

Task 008I does not mutate strategy logic and does not auto-apply learning proposals.

## Loss Visibility and Historical Recommendation Protection

Task 008I keeps losing outcomes visible in returned records and portfolio snapshots.

Historical recommendation fields are preserved in record output and must not be overwritten to improve appearance.

## Mandatory Boundary Flags

Created records and snapshots explicitly preserve the non-production product boundary:

- `paper_only = true`
- `advisory_only = true`
- `human_in_the_loop = true`
- `real_money_order_placed = false`
- `real_money_trading_automation_enabled = false`
- `autonomous_real_money_execution = false`
- `broker_execution_enabled = false`
- `broker_api_called = false`
- `production_supabase_connected = false`
- `persistence_write_performed = false`
- `secrets_required = false`
- `external_api_called = false`
- `billing_runtime_enabled = false`
- `membership_runtime_enabled = false`
- `auth_runtime_enabled = false`
- `deployment_required = false`


## Vendor / External Data Source Boundary

Harness Engineering approves vendor/API capability as a future product direction in principle. HK Alpha Team may later need external vendors, vendor APIs, online data sources, market data providers, financial data providers, news providers, AI/model providers, payment providers, authentication providers, deployment providers, notification providers, and broker or broker-sandbox providers.

Task 008I does not select, connect, implement, require, or depend on any specific vendor or vendor API. It does not call live market data, call external APIs, add API keys or secrets, add vendor SDKs, create production third-party dependencies, or add payment provider, auth provider, broker provider, deployment provider, market data provider, news provider, financial data provider, or AI/model vendor integration.

Every future specific vendor, vendor API, or provider requires separate discussion, current-source/web verification where facts may change, documented pricing/terms/privacy/security/failure-mode implications, Evidence Closure classification, and explicit Harness Engineering approval in the scoped PR before it is selected, connected, implemented, required, or made production-facing or user-facing. Until that per-vendor/provider approval is recorded, implementation may include only local interfaces, mock adapters, deterministic fixtures, or placeholder contracts that do not call a vendor, require secrets, fetch live data, incur cost, or create production dependency.

## Explicit Non-Goals

Task 008I does not implement:

- SQL migrations;
- Supabase persistence;
- production Supabase;
- database writes;
- disk persistence;
- live market data;
- external API calls;
- broker integration;
- broker execution APIs;
- real-money order placement;
- autonomous real-money execution;
- billing/payment runtime;
- membership/subscription runtime;
- authentication runtime;
- deployment;
- frontend/UI;
- secrets or credentials;
- vendor SDKs;
- paid data providers;
- payment providers;
- authentication providers;
- deployment providers;
- market data providers;
- news providers;
- financial data providers;
- AI/model vendor integrations;
- production third-party service dependencies.

## Product Runtime Decision

Harness Engineering has approved non-real-money productization, so Task 008I intentionally moves beyond documentation-only planning.

The Task 008I product step is limited to a backend, in-memory, non-production Simulation Desk runtime slice that can be exercised locally and in tests. Later non-real-money persistence, production Supabase, deployment, commercial runtime, auth, live data, and vendor/API capabilities are approved in principle and may proceed only through scoped PRs with tests, validation evidence, Evidence Closure, security/secret handling, current-source verification where facts may change, post-merge verification, and any required explicit per-vendor/provider approval. Real-money trading, autonomous real-money execution, autonomous broker execution, real-money account connectivity, secrets leakage, and hidden/irreversible investment actions remain prohibited.

## Status

Task 008 / Milestone M5 remains **In Progress**.

Codex does not self-approve this PR.
