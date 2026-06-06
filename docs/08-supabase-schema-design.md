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
- `paper_orders` 0:N `learning_proposals` through reviewable source metadata when system-generated learning simulations produce proposals
- `paper_orders` 1:N `audit_events` through `entity_type = paper_orders` and `entity_id`

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
- **Major columns:** `portfolio_id`, `stock_id`, `strategy_recommendation_id`, `simulation_origin` or `paper_order_origin`, `created_by_type`, `source_recommendation_id`, `user_recorded_notes`, `system_learning_reason`, `requires_human_review`, `learning_proposal_id`, `side`, `order_type`, `quantity`, `limit_price`, `status`, `submitted_at`, `filled_at`, `created_at`.
- **Important foreign keys:** `portfolio_id -> paper_portfolios.id`; `stock_id -> stocks.id`; `strategy_recommendation_id -> strategy_recommendations.id`; `source_recommendation_id -> strategy_recommendations.id` when used as the explicit origin-link alias; `learning_proposal_id -> learning_proposals.id` when a system-generated learning simulation creates a reviewable proposal.
- **Indexes:** index on `(portfolio_id, submitted_at desc)`; index on `(stock_id, submitted_at desc)`; future migration should add an index on `(simulation_origin, submitted_at desc)` or `(paper_order_origin, submitted_at desc)` after final field naming is selected.
- **Notes/constraints:** non-negative quantity; paper execution only; `simulation_origin` / `paper_order_origin` allowed values are `user_recorded` and `system_generated_learning`; `user_recorded` records require user/source notes and must not imply AI-generated learning unless explicitly linked; `system_generated_learning` records require original recommendation/thesis/score linkage, `system_learning_reason`, `requires_human_review = true`, and no auto-application of learning proposals.

### `paper_positions`
- **Purpose:** Open/closed simulated position records.
- **Primary key:** `id` (uuid).
- **Major columns:** `portfolio_id`, `stock_id`, `opened_from_order_id`, `simulation_origin` or inherited `paper_order_origin`, `side`, `quantity`, `avg_entry_price`, `avg_exit_price`, `status`, `opened_at`, `closed_at`, `created_at`.
- **Important foreign keys:** `portfolio_id -> paper_portfolios.id`; `stock_id -> stocks.id`; `opened_from_order_id -> paper_orders.id`.
- **Indexes:** index on `(portfolio_id, status)`; index on `(stock_id, status)`.
- **Notes/constraints:** preserves losing and winning positions.

### `portfolio_snapshots`
- **Purpose:** Periodic valuation snapshots for paper portfolios, including mixed-origin portfolios where `user_recorded` and `system_generated_learning` records must remain distinguishable through linked orders/positions.
- **Primary key:** `id` (uuid).
- **Major columns:** `portfolio_id`, `snapshot_time`, `nav`, `cash`, `gross_exposure`, `net_exposure`, `drawdown_pct`, `created_at`.
- **Important foreign keys:** `portfolio_id -> paper_portfolios.id`.
- **Indexes:** unique `(portfolio_id, snapshot_time)`.
- **Notes/constraints:** supports simulation performance and risk tracking.

### `trade_reviews`
- **Purpose:** Post-trade review records with explicit learning notes.
- **Primary key:** `id` (uuid).
- **Major columns:** `paper_position_id`, `simulation_origin` or inherited origin metadata, `outcome_label`, `review_notes`, `mistake_tags_json`, `what_worked_json`, `what_failed_json`, `reviewed_at`, `created_at`.
- **Important foreign keys:** `paper_position_id -> paper_positions.id`.
- **Indexes:** index on `(paper_position_id, reviewed_at desc)`.
- **Notes/constraints:** losing trades must remain visible.

### `learning_proposals`
- **Purpose:** Improvement proposals derived from reviews and system-generated learning simulations.
- **Primary key:** `id` (uuid).
- **Major columns:** `source_type`, `source_id`, `simulation_origin`, `requires_human_review`, `auto_applied`, `title`, `proposal_text`, `expected_impact`, `risk_of_change`, `status`, `created_at`, `updated_at`.
- **Important foreign keys:** optional references by typed source metadata.
- **Indexes:** index on `(status, created_at desc)`.
- **Notes/constraints:** proposals are reviewable, not auto-applied; `system_generated_learning` proposals require `requires_human_review = true` and `auto_applied = false`.

### `audit_events`
- **Purpose:** Immutable governance and audit event log.
- **Primary key:** `id` (uuid).
- **Major columns:** `event_uuid`, `event_type`, `entity_type`, `entity_id`, `simulation_origin`, `actor_type`, `actor_id`, `event_payload_json`, `created_at`.
- **Important foreign keys:** polymorphic entity references via `entity_type` + `entity_id`.
- **Indexes:** unique `event_uuid`; index on `(entity_type, entity_id, created_at desc)`.
- **Notes/constraints:** append-only; never overwrite historical events.


## Simulation Origin Semantics (Task 008G)

Task 008G adds schema-level source semantics without renaming canonical table names. Future migrations should preserve the locked table set while adding explicit origin fields where needed.

### Allowed Origin Values

- `user_recorded` — paper trades entered or recorded by the human user / Harness Engineering.
- `system_generated_learning` — paper-trading simulations generated by HK Alpha Team / Simulation Investment Desk to validate recommendation quality and produce reviewable learning proposals.

### Required Field Semantics

- `simulation_origin` or `paper_order_origin` identifies whether the record is `user_recorded` or `system_generated_learning`. Final migration naming should choose one canonical column while preserving the documented semantics.
- `created_by_type` distinguishes human/user-created records from Simulation Investment Desk/system-created records.
- `source_recommendation_id` and `strategy_recommendation_id` both refer to recommendation lineage; `strategy_recommendation_id` remains the canonical existing FK name, while `source_recommendation_id` may be used in payloads/docs as the explicit origin-link alias.
- `user_recorded_notes` applies to `user_recorded` records and preserves human notes/rationale.
- `system_learning_reason` applies to `system_generated_learning` records and explains why the system generated the learning simulation.
- `requires_human_review` applies to system-generated learning proposals and must remain true when a proposal can affect future process changes.
- `learning_proposal_id` links system-generated learning simulations to reviewable proposals when created.

### Table Relationship Impact

- `strategy_recommendations` remain the original recommendation source for system-generated learning simulations and may optionally link to user-recorded paper trades.
- `paper_portfolios` may contain both origins, but downstream queries must preserve origin filters.
- `paper_orders` carry the primary origin/source semantics.
- `paper_positions` inherit origin from `opened_from_order_id` and may denormalize origin for queryability.
- `portfolio_snapshots` summarize portfolio state and must not collapse or hide origin-specific losing outcomes.
- `trade_reviews` preserve review context for both origins, with system-generated learning reviews feeding proposals only through human-review gates.
- `learning_proposals` are generated only as reviewable proposals and are never auto-applied.
- `audit_events` should log origin-aware creation, review, proposal, and rejection/acceptance events without overwriting history.

## RLS and Auditability Notes

- Enable RLS on user-owned workflow tables.
- Preserve append-only records for strategy recommendations, paper orders, paper positions, trade reviews, learning proposals, and audit events.
- Keep timestamps and actor/source metadata for traceability.

## Retention Notes

- Strategy, simulation, and audit history should remain retained for governance traceability.
- High-volume telemetry can be summarized/archived by future implementation policy.


## Migration Planning Note

Production SQL migrations must be created in a later task after this schema design is reviewed.
Do not create `supabase/migrations/` files in this PR.
