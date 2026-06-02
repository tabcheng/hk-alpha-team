# 21 — First Analysis Workflow Skeleton (Phase 4A)

## Purpose

Phase 4A starts Task 007 / Milestone M4 by replacing the Phase 3 static analyze-stock stub internals with a deterministic local-only workflow skeleton for `POST /api/v1/analyze-stock`.

The skeleton exists to make workflow shape, traceability, advisory framing, and tests reviewable before any live data, production persistence, agent run storage, simulation desk behavior, or broker integration is introduced.

## Relationship to the Phase 3 Analyze-Stock Stub

Phase 3 made the endpoint contract callable and testable with a static stub payload.

Phase 4A keeps the same public endpoint and required response envelope, but the endpoint now delegates to an internal workflow module that exposes explicit deterministic stages. The response should identify itself as Phase 4A skeleton behavior, not Phase 3 `stub_only` behavior.

## Workflow Stages

The local skeleton includes these internal stages:

1. Input normalization.
2. Static stock context placeholder.
3. Deterministic market placeholder scoring.
4. Deterministic fundamental placeholder scoring.
5. Deterministic technical placeholder scoring.
6. Deterministic sentiment placeholder scoring.
7. Deterministic risk placeholder scoring.
8. Advisory summary generation.
9. Key reasons generation.
10. Main risks generation.
11. Invalidation conditions generation.
12. Human decision framing.
13. Workflow trace metadata.

These stages are implementation scaffolding only. They do not yet represent complete Investment Strategy Office research.

## Deterministic and Local-Only Design

Phase 4A must be deterministic for the same normalized symbol across stable workflow fields and scores.

The skeleton does not:

- fetch live market data;
- call external APIs or network services;
- require environment secrets;
- read or write production Supabase;
- persist `agent_runs`, `agent_outputs`, `strategy_recommendations`, or paper orders;
- create paper-trading orders;
- connect to broker APIs;
- place real-money orders.

Placeholder scores are numeric only to exercise downstream contract handling. They are not market-data-derived and must be treated as local deterministic scaffolding.

## Required Output Fields

The analyze-stock `data` payload continues to include the contract-required fields:

- `symbol`
- `analysis_status`
- `workflow_phase`
- `strategy_recommendation`
- `summary`
- `confidence_level`
- `scores`
- `key_reasons`
- `main_risks`
- `invalidation_conditions`
- `paper_trading_action`
- `real_money_decision`
- `agent_trace`
- `generated_at`
- `schema_version`

Additional local-only skeleton metadata may be included when it improves reviewability and does not rename or remove required fields.

## Advisory-Only Framing

Every Phase 4A response must remain advisory-only and human-in-the-loop.

The response must make clear that:

- it is not live investment research;
- it is not investment advice;
- confidence remains conservative because scoring is placeholder-based;
- Harness Engineering remains responsible for any real-money decision;
- no autonomous trading action is performed.

Preferred strategy labels remain limited to the locked label set:

- `STRONG_WATCH`
- `WAIT_FOR_PULLBACK`
- `SMALL_POSITION`
- `ACCUMULATE`
- `HOLD`
- `REDUCE_RISK`
- `AVOID`

## Boundary Statements

### No Live Market Data

The skeleton does not ingest live prices, OHLCV bars, index data, liquidity data, financial reports, news, sentiment feeds, or broker commentary.

### No Production Supabase

The skeleton does not require or connect to production Supabase. It creates no production database records.

### No Persistence

The skeleton performs no persistence writes. It does not create recommendation records, agent run records, agent output records, paper orders, portfolio records, or audit events.

### No Broker or Real-Money Trading

The skeleton does not connect to broker execution APIs and does not place paper or real-money orders. Real-money decisions remain manual Harness Engineering decisions outside the application.

## Validation Approach

Phase 4A validation should cover:

- workflow unit tests for deterministic placeholder output;
- stable scores and fields for the same symbol;
- symbol normalization inside the workflow module;
- required analyze-stock output fields;
- explicit warning and trace metadata boundaries;
- advisory summary, risks, invalidation conditions, and human-decision framing;
- existing API validation protection for missing or non-HK symbols;
- `/health` and `/api/v1/project-status` regression coverage;
- contract validation and whitespace diff checks.

Required local commands for this PR class are:

```bash
python scripts/validate_contracts.py
PYTHONPATH=backend pytest backend/tests -q
git diff --check
```

## Phase 4B Follow-Up Path

Likely Phase 4B work should remain small and reviewed. Candidate follow-ups include:

- richer deterministic department scoring adapters that still avoid live data;
- agent-output adapter shapes that mirror the locked common agent contract without persistence;
- explicit handoff mapping from workflow stages to future `agent_runs` / `agent_outputs` records;
- additional contract tests for future strategy recommendation creation once that endpoint is explicitly authorized.

Phase 4B must not add live market data, production Supabase, broker integration, secrets, or real-money trading unless Harness Engineering explicitly authorizes a future governance-sensitive task and updates relevant source-of-truth docs.
