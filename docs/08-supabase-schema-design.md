# 08 — Supabase Schema Design (Task 002)

## Purpose

Define the exact required HK Alpha Team v1 Supabase/Postgres schema table set for documentation-first implementation planning.

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

## Domain Grouping

### Market and Reference
- `stocks`
- `market_indices`
- `price_bars`
- `market_snapshots`
- `company_financials`
- `news_items`

### Research and Strategy
- `research_documents`
- `investment_committee_reviews`
- `strategy_recommendations`

### Agent Traceability
- `agent_runs`
- `agent_outputs`

### Simulation Desk
- `paper_portfolios`
- `paper_orders`
- `paper_positions`
- `portfolio_snapshots`
- `trade_reviews`

### Learning and Governance
- `learning_proposals`
- `audit_events`

## Relationship Blueprint (High Level)

- `stocks` 1:N `price_bars`
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
- `paper_orders` 1:1 or 1:N `paper_positions` (depends on fill model)
- All major workflow tables N:1 `audit_events` by entity reference metadata.

## Design-Only SQL Draft Note

A design-only SQL draft is intentionally non-executable and must reflect this exact table set in future implementation PRs.

## RLS and Auditability Notes

- Enable RLS on user-owned workflow tables.
- Preserve append-only records for strategy, paper orders, paper positions, trade reviews, and audit events.
- Keep timestamps and actor/source metadata for traceability.

## Retention Notes

- Strategy, simulation, and audit history should remain retained for governance traceability.
- High-volume telemetry can be summarized/archived by future implementation policy.
