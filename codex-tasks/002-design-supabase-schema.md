# Task 002 — Design Supabase Schema

## Objective

Design initial Supabase/Postgres schema for HK Alpha Team data domains using the exact required HK Alpha Team table set.

## Required Canonical Table Set

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

## Proposed Scope

- Define tables and relationships across research, strategy, simulation, and governance domains.
- Specify indexing strategy and auditability expectations.
- Document lifecycle and retention considerations.

## Deliverables

- Schema design document (ERD-level).
- SQL migration draft (design-only stage).
- Notes on RBAC and auditability implications.
