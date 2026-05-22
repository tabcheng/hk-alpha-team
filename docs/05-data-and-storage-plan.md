# 05 Data and Storage Plan (Canonical v1)

## Canonical Primary Tables (Required Names)

1. `stocks`
2. `market_indices`
3. `price_bars`
4. `market_snapshots`
5. `company_financials`
6. `news_items`
7. `research_documents`
8. `agent_runs`
9. `agent_outputs`
10. `investment_committee_reviews`
11. `strategy_recommendations`
12. `paper_portfolios`
13. `paper_orders`
14. `paper_positions`
15. `portfolio_snapshots`
16. `trade_reviews`
17. `learning_proposals`
18. `audit_events`

## Storage Principles

- Keep raw inputs and generated outputs distinguishable.
- Preserve timestamps and authorship/agent attribution.
- Favor append-only event logs for auditable workflows.

## Contract Alignment

- API contracts must use the exact MVP endpoint set in `docs/09-api-and-agent-contracts.md`.
- All endpoint responses must use the exact required response envelope in `docs/09-api-and-agent-contracts.md`.
