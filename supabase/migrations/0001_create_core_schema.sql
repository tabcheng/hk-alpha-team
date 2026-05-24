-- DRAFT migration for HK Alpha Team v1.
-- Do not apply to production Supabase without Harness Engineering review.
-- Generated from docs/08-supabase-schema-design.md.
-- This PR does not connect to production Supabase.
-- Date: 2026-05-24

create extension if not exists "pgcrypto";

create table if not exists stocks (
  id uuid primary key default gen_random_uuid(),
  symbol text not null unique,
  name text not null,
  exchange text not null,
  sector text,
  industry text,
  currency text not null default 'HKD',
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_stocks_exchange_sector on stocks (exchange, sector);

create table if not exists market_indices (
  id uuid primary key default gen_random_uuid(),
  index_code text not null unique,
  name text not null,
  exchange text not null,
  currency text not null default 'HKD',
  is_active boolean not null default true,
  created_at timestamptz not null default now()
);

create index if not exists idx_market_indices_exchange on market_indices (exchange);

create table if not exists price_bars (
  id uuid primary key default gen_random_uuid(),
  stock_id uuid not null references stocks(id),
  timeframe text not null,
  bar_time timestamptz not null,
  open numeric(18,6) not null,
  high numeric(18,6) not null,
  low numeric(18,6) not null,
  close numeric(18,6) not null,
  volume bigint not null default 0,
  source text,
  created_at timestamptz not null default now(),
  constraint uq_price_bars_stock_time unique (stock_id, timeframe, bar_time),
  constraint ck_price_bars_high_low check (high >= low),
  constraint ck_price_bars_volume_non_negative check (volume >= 0)
);

create index if not exists idx_price_bars_stock_bar_time_desc on price_bars (stock_id, bar_time desc);

create table if not exists market_snapshots (
  id uuid primary key default gen_random_uuid(),
  stock_id uuid not null references stocks(id),
  snapshot_time timestamptz not null,
  last_price numeric(18,6),
  change_pct numeric(9,4),
  turnover numeric(20,2),
  volatility_proxy numeric(9,4),
  source text,
  created_at timestamptz not null default now()
);

create index if not exists idx_market_snapshots_stock_snapshot_time_desc on market_snapshots (stock_id, snapshot_time desc);

create table if not exists company_financials (
  id uuid primary key default gen_random_uuid(),
  stock_id uuid not null references stocks(id),
  fiscal_period date not null,
  period_type text not null,
  revenue numeric(20,2),
  net_income numeric(20,2),
  eps numeric(12,6),
  balance_sheet_json jsonb not null default '{}'::jsonb,
  cashflow_json jsonb not null default '{}'::jsonb,
  source text,
  created_at timestamptz not null default now(),
  constraint uq_company_financials_period unique (stock_id, fiscal_period, period_type)
);

create table if not exists news_items (
  id uuid primary key default gen_random_uuid(),
  stock_id uuid not null references stocks(id),
  published_at timestamptz not null,
  headline text not null,
  summary text,
  sentiment_label text,
  source_url text,
  source_name text,
  created_at timestamptz not null default now()
);

create index if not exists idx_news_items_stock_published_at_desc on news_items (stock_id, published_at desc);
create index if not exists idx_news_items_sentiment_label on news_items (sentiment_label);

create table if not exists research_documents (
  id uuid primary key default gen_random_uuid(),
  stock_id uuid not null references stocks(id),
  title text not null,
  thesis text not null,
  key_points_json jsonb not null default '[]'::jsonb,
  risks_json jsonb not null default '[]'::jsonb,
  invalidation_conditions_json jsonb not null default '[]'::jsonb,
  author_type text not null,
  author_id text,
  status text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_research_documents_stock_created_at_desc on research_documents (stock_id, created_at desc);
create index if not exists idx_research_documents_status on research_documents (status);

create table if not exists strategy_recommendations (
  id uuid primary key default gen_random_uuid(),
  stock_id uuid not null references stocks(id),
  symbol text not null,
  company_name text not null,
  strategy_recommendation text not null check (strategy_recommendation in ('STRONG_WATCH', 'WAIT_FOR_PULLBACK', 'SMALL_POSITION', 'ACCUMULATE', 'HOLD', 'REDUCE_RISK', 'AVOID')),
  summary text not null,
  confidence_level integer not null check (confidence_level between 0 and 100),
  market_score numeric(6,2),
  fundamental_score numeric(6,2),
  technical_score numeric(6,2),
  sentiment_score numeric(6,2),
  risk_score numeric(6,2),
  simulation_score numeric(6,2),
  key_reasons jsonb not null default '[]'::jsonb,
  main_risks jsonb not null default '[]'::jsonb,
  invalidation_conditions jsonb not null default '[]'::jsonb,
  suggested_user_action text not null,
  paper_trading_action text,
  real_money_decision_owner text not null default 'HUMAN_USER',
  created_at timestamptz not null default now(),
  next_review_date date
);

create index if not exists idx_strategy_recommendations_symbol_created_at_desc on strategy_recommendations (symbol, created_at desc);
create index if not exists idx_strategy_recommendations_next_review_date on strategy_recommendations (next_review_date);

create table if not exists agent_runs (
  id uuid primary key default gen_random_uuid(),
  run_uuid uuid not null unique,
  stock_id uuid references stocks(id),
  recommendation_id uuid references strategy_recommendations(id),
  department_name text not null,
  request_payload_json jsonb not null default '{}'::jsonb,
  status text not null check (status in ('started', 'succeeded', 'failed', 'timeout')),
  started_at timestamptz,
  finished_at timestamptz,
  error_code text,
  created_at timestamptz not null default now()
);

create index if not exists idx_agent_runs_department_started_at_desc on agent_runs (department_name, started_at desc);

create table if not exists agent_outputs (
  id uuid primary key default gen_random_uuid(),
  agent_run_id uuid not null references agent_runs(id),
  department_name text not null,
  output_json jsonb not null default '{}'::jsonb,
  confidence numeric(6,2),
  created_at timestamptz not null default now()
);

create index if not exists idx_agent_outputs_run_created_at on agent_outputs (agent_run_id, created_at);

create table if not exists investment_committee_reviews (
  id uuid primary key default gen_random_uuid(),
  research_document_id uuid not null references research_documents(id),
  review_posture text not null,
  consensus_score numeric(6,2),
  dissenting_views_json jsonb not null default '[]'::jsonb,
  open_questions_json jsonb not null default '[]'::jsonb,
  reviewed_at timestamptz not null,
  reviewer_type text not null,
  created_at timestamptz not null default now()
);

create index if not exists idx_investment_committee_reviews_doc_reviewed_at_desc on investment_committee_reviews (research_document_id, reviewed_at desc);

create table if not exists paper_portfolios (
  id uuid primary key default gen_random_uuid(),
  portfolio_uuid uuid not null unique,
  name text not null,
  base_currency text not null default 'HKD',
  starting_cash numeric(20,2) not null,
  status text not null,
  created_at timestamptz not null default now()
);

create index if not exists idx_paper_portfolios_status on paper_portfolios (status);

create table if not exists paper_orders (
  id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references paper_portfolios(id),
  stock_id uuid not null references stocks(id),
  strategy_recommendation_id uuid references strategy_recommendations(id),
  side text not null,
  order_type text not null,
  quantity numeric(20,6) not null check (quantity >= 0),
  limit_price numeric(18,6),
  status text not null,
  submitted_at timestamptz,
  filled_at timestamptz,
  created_at timestamptz not null default now()
);

create index if not exists idx_paper_orders_portfolio_submitted_at_desc on paper_orders (portfolio_id, submitted_at desc);
create index if not exists idx_paper_orders_stock_submitted_at_desc on paper_orders (stock_id, submitted_at desc);

create table if not exists paper_positions (
  id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references paper_portfolios(id),
  stock_id uuid not null references stocks(id),
  opened_from_order_id uuid references paper_orders(id),
  side text not null,
  quantity numeric(20,6) not null,
  avg_entry_price numeric(18,6),
  avg_exit_price numeric(18,6),
  status text not null,
  opened_at timestamptz,
  closed_at timestamptz,
  created_at timestamptz not null default now()
);

create index if not exists idx_paper_positions_portfolio_status on paper_positions (portfolio_id, status);
create index if not exists idx_paper_positions_stock_status on paper_positions (stock_id, status);

create table if not exists portfolio_snapshots (
  id uuid primary key default gen_random_uuid(),
  portfolio_id uuid not null references paper_portfolios(id),
  snapshot_time timestamptz not null,
  nav numeric(20,2) not null,
  cash numeric(20,2) not null,
  gross_exposure numeric(20,2),
  net_exposure numeric(20,2),
  drawdown_pct numeric(9,4),
  created_at timestamptz not null default now(),
  constraint uq_portfolio_snapshots_portfolio_snapshot_time unique (portfolio_id, snapshot_time)
);

create table if not exists trade_reviews (
  id uuid primary key default gen_random_uuid(),
  paper_position_id uuid not null references paper_positions(id),
  outcome_label text not null,
  review_notes text,
  mistake_tags_json jsonb not null default '[]'::jsonb,
  what_worked_json jsonb not null default '[]'::jsonb,
  what_failed_json jsonb not null default '[]'::jsonb,
  reviewed_at timestamptz not null,
  created_at timestamptz not null default now()
);

create index if not exists idx_trade_reviews_position_reviewed_at_desc on trade_reviews (paper_position_id, reviewed_at desc);

create table if not exists learning_proposals (
  id uuid primary key default gen_random_uuid(),
  source_type text not null,
  source_id uuid,
  title text not null,
  proposal_text text not null,
  expected_impact text,
  risk_of_change text,
  status text not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists idx_learning_proposals_status_created_at_desc on learning_proposals (status, created_at desc);

create table if not exists audit_events (
  id uuid primary key default gen_random_uuid(),
  event_uuid uuid not null unique,
  event_type text not null,
  entity_type text not null,
  entity_id uuid,
  actor_type text not null,
  actor_id text,
  event_payload_json jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create index if not exists idx_audit_events_entity_created_at_desc on audit_events (entity_type, entity_id, created_at desc);
