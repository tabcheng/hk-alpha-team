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
- **Purpose:** Simulation paper order intents and lifecycle events.
- **Primary key:** `id` (uuid).
- **Major columns:** `portfolio_id`, `stock_id`, `strategy_recommendation_id`, `side`, `order_type`, `quantity`, `limit_price`, `status`, `submitted_at`, `filled_at`, `created_at`.
- **Important foreign keys:** `portfolio_id -> paper_portfolios.id`; `stock_id -> stocks.id`; `strategy_recommendation_id -> strategy_recommendations.id`.
- **Indexes:** index on `(portfolio_id, submitted_at desc)`; index on `(stock_id, submitted_at desc)`.
- **Notes/constraints:** non-negative quantity; paper execution only.

### `paper_positions`
- **Purpose:** Open/closed simulated position records.
- **Primary key:** `id` (uuid).
- **Major columns:** `portfolio_id`, `stock_id`, `opened_from_order_id`, `side`, `quantity`, `avg_entry_price`, `avg_exit_price`, `status`, `opened_at`, `closed_at`, `created_at`.
- **Important foreign keys:** `portfolio_id -> paper_portfolios.id`; `stock_id -> stocks.id`; `opened_from_order_id -> paper_orders.id`.
- **Indexes:** index on `(portfolio_id, status)`; index on `(stock_id, status)`.
- **Notes/constraints:** preserves losing and winning positions.

### `portfolio_snapshots`
- **Purpose:** Periodic valuation snapshots for paper portfolios.
- **Primary key:** `id` (uuid).
- **Major columns:** `portfolio_id`, `snapshot_time`, `nav`, `cash`, `gross_exposure`, `net_exposure`, `drawdown_pct`, `created_at`.
- **Important foreign keys:** `portfolio_id -> paper_portfolios.id`.
- **Indexes:** unique `(portfolio_id, snapshot_time)`.
- **Notes/constraints:** supports simulation performance and risk tracking.

### `trade_reviews`
- **Purpose:** Post-trade review records with explicit learning notes.
- **Primary key:** `id` (uuid).
- **Major columns:** `paper_position_id`, `outcome_label`, `review_notes`, `mistake_tags_json`, `what_worked_json`, `what_failed_json`, `reviewed_at`, `created_at`.
- **Important foreign keys:** `paper_position_id -> paper_positions.id`.
- **Indexes:** index on `(paper_position_id, reviewed_at desc)`.
- **Notes/constraints:** losing trades must remain visible.

### `learning_proposals`
- **Purpose:** Improvement proposals derived from reviews and simulations.
- **Primary key:** `id` (uuid).
- **Major columns:** `source_type`, `source_id`, `title`, `proposal_text`, `expected_impact`, `risk_of_change`, `status`, `created_at`, `updated_at`.
- **Important foreign keys:** optional references by typed source metadata.
- **Indexes:** index on `(status, created_at desc)`.
- **Notes/constraints:** proposals are reviewable, not auto-applied.

### `audit_events`
- **Purpose:** Immutable governance and audit event log.
- **Primary key:** `id` (uuid).
- **Major columns:** `event_uuid`, `event_type`, `entity_type`, `entity_id`, `actor_type`, `actor_id`, `event_payload_json`, `created_at`.
- **Important foreign keys:** polymorphic entity references via `entity_type` + `entity_id`.
- **Indexes:** unique `event_uuid`; index on `(entity_type, entity_id, created_at desc)`.
- **Notes/constraints:** append-only; never overwrite historical events.

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
