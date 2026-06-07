# 08 — Supabase Schema Design (Task 002)

## Purpose

Define the exact required HK Alpha Team v1 Supabase/Postgres schema table set with ERD-level details for implementation planning.

## Scope and Boundaries

- Documentation-only.
- No executable migrations in this PR.
- Advisory/reporting and simulation only.

## Exact Required HK Alpha Team Table Set

- `stocks`
- `market_indices`
- `price_bars`
- `market_snapshots`
- `company_financials`
- `news_items`
- `research_documents`
- `agent_runs`
- `agent_outputs`
- `investment_committee_reviews`
- `strategy_recommendations`
- `paper_portfolios`
- `paper_orders`
- `paper_positions`
- `portfolio_snapshots`
- `trade_reviews`
- `learning_proposals`
- `audit_events`

## Relationship Blueprint (High Level)

- `stocks` 1:N `price_bars`
- `stocks` 1:N `market_snapshots`
- `stocks` 1:N `company_financials`
- `stocks` 1:N `news_items`
- `stocks` 1:N `research_documents`
- `research_documents` 1:N `investment_committee_reviews`
- `investment_committee_reviews` 1:N `strategy_recommendations`
- `agent_runs` 1:N `agent_outputs`
- `paper_portfolios` 1:N `paper_orders`
- `paper_portfolios` 1:N `paper_positions`
- `paper_portfolios` 1:N `portfolio_snapshots`
- `paper_positions` 1:N `trade_reviews`
- `strategy_recommendations` 1:N `paper_orders`
- `paper_orders` 0:1 `learning_proposals` through reviewable learning linkage metadata when a `system_generated_learning` simulation proposes improvements
- `paper_orders` 1:N `audit_events` through `entity_type = "paper_orders"` and `entity_id`
- `learning_proposals` 1:N `audit_events` through `entity_type = "learning_proposals"` and `entity_id`

## ERD-Level Table Details

### `stocks`
- **Purpose:** Canonical equity master records for HK universe and linked analysis.
- **Primary key:** `id` (uuid).
- **Major columns:** `symbol`, `name`, `exchange`, `sector`, `industry`, `currency`, `is_active`, `created_at`, `updated_at`.
- **Important foreign keys:** None (root entity).
- **Indexes:** unique `symbol`; index on `(exchange, sector)`.
- **Notes/constraints:** `symbol` required; use normalized format (e.g., `0700.HK`).

### `market_indices`
- **Purpose:** Reference index metadata (e.g., HSI, HSCEI) for context and benchmarking.
- **Primary key:** `id` (uuid).
- **Major columns:** `index_code`, `name`, `exchange`, `currency`, `is_active`, `created_at`.
- **Important foreign keys:** None.
- **Indexes:** unique `index_code`; index on `exchange`.
- **Notes/constraints:** supports strategy-relative risk and regime context.

### `price_bars`
- **Purpose:** OHLCV time-series bars for stocks.
- **Primary key:** `id` (uuid).
- **Major columns:** `stock_id`, `timeframe`, `bar_time`, `open`, `high`, `low`, `close`, `volume`, `source`, `created_at`.
- **Important foreign keys:** `stock_id -> stocks.id`.
- **Indexes:** unique `(stock_id, timeframe, bar_time)`; index on `(stock_id, bar_time desc)`.
- **Notes/constraints:** check `high >= low`; check non-negative `volume`.

### `market_snapshots`
- **Purpose:** Intraday/period snapshots capturing market state for auditable context.
- **Primary key:** `id` (uuid).
- **Major columns:** `stock_id`, `snapshot_time`, `last_price`, `change_pct`, `turnover`, `volatility_proxy`, `source`, `created_at`.
- **Important foreign keys:** `stock_id -> stocks.id`.
- **Indexes:** index on `(stock_id, snapshot_time desc)`.
- **Notes/constraints:** append-first snapshots; no destructive rewrites.

### `company_financials`
- **Purpose:** Structured company financial facts used by research/strategy workflows.
- **Primary key:** `id` (uuid).
- **Major columns:** `stock_id`, `fiscal_period`, `period_type`, `revenue`, `net_income`, `eps`, `balance_sheet_json`, `cashflow_json`, `source`, `created_at`.
- **Important foreign keys:** `stock_id -> stocks.id`.
- **Indexes:** unique `(stock_id, fiscal_period, period_type)`.
- **Notes/constraints:** financial payload can mix typed fields + JSON extensions.

### `news_items`
- **Purpose:** Time-stamped market/company news records.
- **Primary key:** `id` (uuid).
- **Major columns:** `stock_id`, `published_at`, `headline`, `summary`, `sentiment_label`, `source_url`, `source_name`, `created_at`.
- **Important foreign keys:** `stock_id -> stocks.id`.
- **Indexes:** index on `(stock_id, published_at desc)`; index on `sentiment_label`.
- **Notes/constraints:** keep source provenance for traceability.

### `research_documents`
- **Purpose:** Research memos and thesis artifacts authored by agents/humans.
- **Primary key:** `id` (uuid).
- **Major columns:** `stock_id`, `title`, `thesis`, `key_points_json`, `risks_json`, `invalidation_conditions_json`, `author_type`, `author_id`, `status`, `created_at`, `updated_at`.
- **Important foreign keys:** `stock_id -> stocks.id`.
- **Indexes:** index on `(stock_id, created_at desc)`; index on `status`.
- **Notes/constraints:** advisory-only reasoning artifacts; preserve revision history.

### `agent_runs`
- **Purpose:** Run-level traceability for all agent executions.
- **Primary key:** `id` (uuid).
- **Major columns:** `run_uuid`, `department_name`, `request_payload_json`, `status`, `started_at`, `finished_at`, `error_code`, `created_at`.
- **Important foreign keys:** optional `stock_id -> stocks.id`, optional `recommendation_id -> strategy_recommendations.id`.
- **Indexes:** unique `run_uuid`; index on `(department_name, started_at desc)`.
- **Notes/constraints:** `status` in (`started`,`succeeded`,`failed`,`timeout`).

### `agent_outputs`
- **Purpose:** Structured outputs from each agent run.
- **Primary key:** `id` (uuid).
- **Major columns:** `agent_run_id`, `department_name`, `output_json`, `confidence`, `created_at`.
- **Important foreign keys:** `agent_run_id -> agent_runs.id`.
- **Indexes:** index on `(agent_run_id, created_at)`.
- **Notes/constraints:** append-only linked payload artifacts.

### `investment_committee_reviews`
- **Purpose:** Cross-agent synthesis and challenge notes before recommendations.
- **Primary key:** `id` (uuid).
- **Major columns:** `research_document_id`, `review_posture`, `consensus_score`, `dissenting_views_json`, `open_questions_json`, `reviewed_at`, `reviewer_type`, `created_at`.
- **Important foreign keys:** `research_document_id -> research_documents.id`.
- **Indexes:** index on `(research_document_id, reviewed_at desc)`.
- **Notes/constraints:** captures unresolved issues and decision rationale.

### `strategy_recommendations`
- **Purpose:** Final Investment Strategy Office recommendation records using the exact required field names.
- **Primary key:** `id` (uuid).
- **Major columns (exact required Investment Strategy Office field names):**
  - `stock_id`
  - `symbol`
  - `company_name`
  - `strategy_recommendation`
  - `summary`
  - `confidence_level`
  - `market_score`
  - `fundamental_score`
  - `technical_score`
  - `sentiment_score`
  - `risk_score`
  - `simulation_score`
  - `key_reasons`
  - `main_risks`
  - `invalidation_conditions`
  - `suggested_user_action`
  - `paper_trading_action`
  - `real_money_decision_owner`
  - `created_at`
  - `next_review_date`
- **Important foreign keys:** `stock_id -> stocks.id`; optional committee linkage by review reference metadata.
- **Indexes:** index on `(symbol, created_at desc)`; index on `(next_review_date)`.
- **Notes/constraints:** `real_money_decision_owner` must remain human-owned in v1; `confidence_level` bounded `[0,100]`.

### `paper_portfolios`
- **Purpose:** Simulation desk portfolio containers.
- **Primary key:** `id` (uuid).
- **Major columns:** `portfolio_uuid`, `name`, `base_currency`, `starting_cash`, `status`, `created_at`.
- **Important foreign keys:** optional `owner_profile_id`.
- **Indexes:** unique `portfolio_uuid`; index on `status`.
- **Notes/constraints:** paper-only scope.

### `paper_orders`
- **Purpose:** Simulation paper order intents and lifecycle events for both user-recorded paper trades and system-generated learning simulations.
- **Primary key:** `id` (uuid).
- **Major columns:** `portfolio_id`, `stock_id`, `strategy_recommendation_id`, `source_recommendation_id`, `simulation_origin`, `paper_order_origin`, `created_by_type`, `user_recorded_notes`, `system_learning_reason`, `requires_human_review`, `learning_proposal_id`, `side`, `order_type`, `quantity`, `limit_price`, `status`, `submitted_at`, `filled_at`, `created_at`.
- **Important foreign keys:** `portfolio_id -> paper_portfolios.id`; `stock_id -> stocks.id`; `strategy_recommendation_id -> strategy_recommendations.id`; `source_recommendation_id -> strategy_recommendations.id` when system-learning lineage needs explicit source terminology; `learning_proposal_id -> learning_proposals.id` when a reviewable proposal is created.
- **Indexes:** index on `(portfolio_id, submitted_at desc)`; index on `(stock_id, submitted_at desc)`; planned index on `(simulation_origin, created_at desc)`; planned index on `(source_recommendation_id, created_at desc)`.
- **Notes/constraints:** non-negative quantity; paper execution only; `simulation_origin` / `paper_order_origin` allowed values are `user_recorded` and `system_generated_learning`; `created_by_type` distinguishes human/user/Harness Engineering from Simulation Investment Desk/system; `requires_human_review` must be true for system-generated learning proposal linkage.

### `paper_positions`
- **Purpose:** Open/closed simulated position records derived from paper orders while preserving order origin.
- **Primary key:** `id` (uuid).
- **Major columns:** `portfolio_id`, `stock_id`, `opened_from_order_id`, `simulation_origin`, `side`, `quantity`, `avg_entry_price`, `avg_exit_price`, `status`, `opened_at`, `closed_at`, `created_at`.
- **Important foreign keys:** `portfolio_id -> paper_portfolios.id`; `stock_id -> stocks.id`; `opened_from_order_id -> paper_orders.id`.
- **Indexes:** index on `(portfolio_id, status)`; index on `(stock_id, status)`; planned index on `(simulation_origin, status)`.
- **Notes/constraints:** preserves losing and winning positions; position origin should be inherited from `paper_orders.simulation_origin` for auditability.

### `portfolio_snapshots`
- **Purpose:** Periodic valuation snapshots for paper portfolios.
- **Primary key:** `id` (uuid).
- **Major columns:** `portfolio_id`, `snapshot_time`, `simulation_origin_summary_json`, `nav`, `cash`, `gross_exposure`, `net_exposure`, `drawdown_pct`, `created_at`.
- **Important foreign keys:** `portfolio_id -> paper_portfolios.id`.
- **Indexes:** unique `(portfolio_id, snapshot_time)`.
- **Notes/constraints:** supports simulation performance and risk tracking; future snapshot rollups should preserve separate user-recorded and system-generated-learning attribution when both origins exist in one portfolio.

### `trade_reviews`
- **Purpose:** Post-trade review records with explicit learning notes.
- **Primary key:** `id` (uuid).
- **Major columns:** `paper_position_id`, `simulation_origin`, `outcome_label`, `review_notes`, `user_recorded_notes`, `system_learning_reason`, `mistake_tags_json`, `what_worked_json`, `what_failed_json`, `improvement_suggestions_json`, `requires_human_review`, `reviewed_at`, `created_at`.
- **Important foreign keys:** `paper_position_id -> paper_positions.id`.
- **Indexes:** index on `(paper_position_id, reviewed_at desc)`; planned index on `(simulation_origin, reviewed_at desc)`.
- **Notes/constraints:** losing trades must remain visible; user-recorded reviews preserve human notes, while system-generated learning reviews preserve the original thesis, scores, what worked, what failed, and improvement suggestions.

### `learning_proposals`
- **Purpose:** Improvement proposals derived from reviews and system-generated learning simulations.
- **Primary key:** `id` (uuid).
- **Major columns:** `source_type`, `source_id`, `source_recommendation_id`, `simulation_origin`, `title`, `proposal_text`, `expected_impact`, `risk_of_change`, `requires_human_review`, `auto_apply`, `status`, `created_at`, `updated_at`.
- **Important foreign keys:** optional references by typed source metadata; `source_recommendation_id -> strategy_recommendations.id` when proposal lineage traces to a recommendation.
- **Indexes:** index on `(status, created_at desc)`; planned index on `(simulation_origin, status, created_at desc)`.
- **Notes/constraints:** proposals are reviewable, not auto-applied; `requires_human_review` must be true and `auto_apply` must be false for system-generated learning proposals.

### `audit_events`
- **Purpose:** Immutable governance and audit event log.
- **Primary key:** `id` (uuid).
- **Major columns:** `event_uuid`, `event_type`, `entity_type`, `entity_id`, `actor_type`, `actor_id`, `simulation_origin`, `event_payload_json`, `created_at`.
- **Important foreign keys:** polymorphic entity references via `entity_type` + `entity_id`.
- **Indexes:** unique `event_uuid`; index on `(entity_type, entity_id, created_at desc)`; planned index on `(simulation_origin, created_at desc)`.
- **Notes/constraints:** append-only; never overwrite historical events; audit events must distinguish user-recorded paper-trade actions from system-generated learning simulation actions.

## Simulation Origin Semantics (Task 008G)

Task 008G adopts a dual simulation-origin schema foundation without renaming canonical tables:

- `user_recorded` — paper trades entered or recorded by Harness Engineering / a human user. These records preserve user notes, user rationale, optional recommendation linkage, trade review fields, and audit provenance.
- `system_generated_learning` — paper-trading simulations generated by HK Alpha Team / the Simulation Investment Desk to validate recommendation quality. These records preserve original recommendation linkage, original scores, original thesis, entry/exit assumptions, PnL, holding period, what worked, what failed, improvement suggestions, reviewable learning proposals, and audit provenance.

Planned field-level additions are additive contract/schema clarifications, not table renames:

- `simulation_origin` or `paper_order_origin` on `paper_orders` to identify `user_recorded` vs. `system_generated_learning`.
- `created_by_type` on origin-bearing records to distinguish human/user/Harness Engineering entries from Simulation Investment Desk/system entries.
- `source_recommendation_id` and existing `strategy_recommendation_id` terminology remain recommendation-lineage fields; future implementation may use both when explicit source wording is needed without renaming the canonical endpoint or table.
- `user_recorded_notes` applies to user-entered paper-trade records and reviews.
- `system_learning_reason` applies to system-generated learning simulations.
- `requires_human_review` applies to system-learning records and learning proposals.
- `learning_proposal_id` links a paper order/review to a reviewable proposal when one is created.

Relationship impact:

- `strategy_recommendations` remain append-only source recommendations for system-generated learning simulations and optional user-recorded linkage.
- `paper_portfolios` can contain both origins, but reports and snapshots must preserve origin-level attribution.
- `paper_orders` are the primary origin-bearing paper-trade intents.
- `paper_positions` inherit origin from the opening paper order.
- `portfolio_snapshots` may aggregate both origins while retaining origin summary metadata.
- `trade_reviews` preserve human notes for `user_recorded` records and learning review fields for `system_generated_learning` records.
- `learning_proposals` are created only as reviewable artifacts and must not be auto-applied.
- `audit_events` record origin, actor type, entity linkage, and boundary confirmations for both pipelines.

The schema remains advisory-only and paper-only. Real-money trading, autonomous real-money execution, broker execution APIs, production Supabase connections, and silent learning-proposal application remain prohibited.

## RLS and Auditability Notes

- Enable RLS on user-owned workflow tables.
- Preserve append-only records for strategy recommendations, paper orders, paper positions, trade reviews, learning proposals, and audit events.
- Keep timestamps and actor/source metadata for traceability.

## Retention Notes

- Strategy, simulation, and audit history should remain retained for governance traceability.
- High-volume telemetry can be summarized/archived by future implementation policy.


## Migration Planning Note

The original schema-design PR was documentation-only: production SQL migrations were intentionally deferred and that earlier PR was not allowed to create `supabase/migrations/` files.

Task 008J is a later, implementation-limited schema-alignment task and is allowed to add `supabase/migrations/0002_align_simulation_desk_persistence_fields.sql` as a local/test-only additive migration draft. The draft may be executed by local/CI validation only. It must not be applied to production Supabase without later explicit Harness Engineering approval, a separate PR scope, and Evidence Closure.

## Task 008J Schema Alignment Note — Local/Test-Only Persistence Draft

Date: 2026-06-06

Task 008J adds a schema-alignment layer for the Task 008G/008I Simulation Desk runtime. The canonical table names remain unchanged: `paper_portfolios`, `paper_orders`, `paper_positions`, `portfolio_snapshots`, `trade_reviews`, `learning_proposals`, and `audit_events`.

The additive draft migration `supabase/migrations/0002_align_simulation_desk_persistence_fields.sql` is local/test-only. It is intended to validate how in-memory Simulation Desk records could map to future persistence before any production Supabase write path is approved. It has not been applied to production Supabase, does not connect production Supabase, does not add a Supabase client, does not perform runtime persistence writes, and requires no secrets.

### 0001 vs Task 008I Runtime Gaps

| Canonical table | Gap in `0001_create_core_schema.sql` relative to Task 008I runtime | Task 008J additive draft alignment |
|---|---|---|
| `paper_portfolios` | Canonical table exists, but Task 008I runtime portfolio IDs remain process-local strings and are not persisted. | No destructive change; future adapter must resolve portfolio identity explicitly. |
| `paper_orders` | Missing explicit `simulation_origin`, `paper_order_origin`, `created_by_type`, canonical UUID `source_recommendation_id`, user-recorded notes, system learning reason, human-review flag, canonical UUID `learning_proposal_id`, boundary flags, outcome preview, and source metadata fields. | `0002` additively drafts these fields; runtime string fixture lineage remains in JSON metadata rather than canonical UUID FK columns. |
| `paper_positions` | Missing `simulation_origin`, so future positions could lose whether they came from `user_recorded` or `system_generated_learning` records. | `0002` additively drafts `simulation_origin`. |
| `portfolio_snapshots` | Missing mixed-origin summary metadata for Task 008I runtime snapshots. | `0002` additively drafts `simulation_origin_summary_json`. |
| `trade_reviews` | Missing explicit origin, user/system note fields, improvement suggestions, and human-review flag aligned to Simulation Desk learning semantics. | `0002` additively drafts these fields while preserving existing review JSON fields. |
| `learning_proposals` | Missing canonical UUID source recommendation lineage, origin, required human-review field, and explicit non-auto-apply field. | `0002` additively drafts UUID `source_recommendation_id`, `simulation_origin`, `requires_human_review`, and `auto_apply`; runtime string fixture lineage remains in proposal JSON metadata. |
| `audit_events` | Existing `event_payload_json` can carry metadata, but there is no first-class `simulation_origin`. | `0002` additively drafts `simulation_origin`; `event_payload_json` remains append-only metadata carrier. |

### Runtime Boundary Fields to Preserve Before Persistence

Future persistence must preserve the approved origins (`user_recorded`, `system_generated_learning`) and these boundary fields together: `paper_only`, `advisory_only`, `human_in_the_loop`, `real_money_order_placed`, `real_money_trading_automation_enabled`, `autonomous_real_money_execution`, `broker_execution_enabled`, `broker_api_called`, `production_supabase_connected`, `persistence_write_performed`, `secrets_required`, `external_api_called`, `billing_runtime_enabled`, `membership_runtime_enabled`, `auth_runtime_enabled`, and `deployment_required`.

Future persistence must also preserve learning and loss guardrails: `proposals_reviewable`, `proposals_auto_applied`, `losing_outcomes_remain_visible`, and `historical_recommendations_overwritten`.
