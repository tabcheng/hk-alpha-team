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

## Task 008G Schema Addendum

- Canonical table names remain locked and unchanged.
- `paper_orders` becomes the primary origin-bearing Simulation Desk record for `user_recorded` and `system_generated_learning` paper-only workflows.
- Planned additive fields include `simulation_origin` / `paper_order_origin`, `created_by_type`, `source_recommendation_id` alongside existing `strategy_recommendation_id`, `user_recorded_notes`, `system_learning_reason`, `requires_human_review`, and `learning_proposal_id`.
- `paper_positions`, `portfolio_snapshots`, `trade_reviews`, `learning_proposals`, and `audit_events` must preserve or report origin lineage without overwriting losing outcomes or historical recommendations.
- No production Supabase migration execution, persistence writes, broker execution, live market data, deployment, or real-money trading is introduced by Task 008G.
