# 09 — API and Agent Contracts (Task 003)

## Purpose

Define the exact required MVP endpoint set, exact required response envelope, and common agent contract shape for HK Alpha Team v1.

## Exact Required MVP Endpoint Set

- `GET /health`
- `POST /api/v1/analyze-stock`
- `GET /api/v1/stocks/{symbol}`
- `GET /api/v1/strategy-recommendations/{recommendation_id}`
- `POST /api/v1/strategy-recommendations`
- `POST /api/v1/simulation/paper-orders`
- `GET /api/v1/paper-portfolios/{portfolio_id}`
- `GET /api/v1/agent-runs/{agent_run_id}`
- `GET /api/v1/project-status`

## Exact Required Response Envelope

```json
{
  "request_id": "uuid",
  "status": "success",
  "data": {},
  "metadata": {
    "schema_version": "v0.1",
    "generated_at": "ISO-8601 timestamp",
    "source": "HK_ALPHA_TEAM"
  },
  "warnings": []
}
```


## Endpoint Specifications (Required Details)

### `GET /health`
- **Purpose:** Liveness/readiness check for service health.
- **Path parameters:** None.
- **Request body:** None.
- **Response shape:** Required success envelope with `data = { "service": "ok" }`.
- **Validation notes:** No authentication payload expected.
- **Error cases:** `INTERNAL_ERROR`.

### `POST /api/v1/analyze-stock`
- **Purpose:** Trigger first-pass analysis workflow scaffolding for one stock symbol.
- **Path parameters:** None.
- **Request body:** `{ "symbol": "0700.HK" }`.
- **Current Phase 4A behavior:** Deterministic local-only First Analysis Workflow Skeleton. Phase 4B adds deterministic department scoring adapters behind the same current runtime semantics. The endpoint provides contract-compatible advisory scaffolding only and does not perform live investment research.
- **Current behavior boundaries:** No live market data, no external APIs, no network services, no persistence writes, no production Supabase, no broker execution, no paper order creation, no real-money order placement, no real-money trading automation, and no secrets required.
- **Response shape:** Required success envelope with strategy/analysis payload in `data`. The current Phase 4A/4B payload must include `symbol`, `analysis_status`, `workflow_phase`, `strategy_recommendation`, `summary`, `confidence_level`, `scores`, `key_reasons`, `main_risks`, `invalidation_conditions`, `paper_trading_action`, `real_money_decision`, `agent_trace`, `generated_at`, and `schema_version`. Phase 4B also exposes local-only `department_outputs` adapter preview metadata for reviewability without changing the required envelope.
- **Current response semantics:** `analysis_status = "phase4a_skeleton"`; `workflow_phase = "Phase 4A — Deterministic First Analysis Workflow Skeleton"`; strategy labels remain limited to the preferred strategy label set; confidence remains conservative because scores are local adapter placeholders and not market-data-derived. Phase 4B intentionally preserves these values to avoid a canonical runtime semantic rename in this PR.
- **Additional Phase 4B adapter metadata:** Local-only metadata may be included when it does not rename or remove required fields, for example `score_confidence`, `stock_context`, `stage_rationales`, `department_outputs`, `department_output_note`, and `next_review_date`. `department_outputs` is deterministic adapter preview metadata using the locked common agent output shape; it is not a persisted `agent_outputs` database record, not evidence that `agent_runs` were created, and not live investment research.
- **Required warnings:** Responses must warn that the output is a deterministic Phase 4A skeleton with Phase 4B adapter previews only, is not live investment research, uses no live market data, uses no persistence, requires no production Supabase, performs no broker execution, and performs no real-money trading.
- **Required `agent_trace` boundary flags:** `agent_runs_created = false`, `agent_outputs_created = false`, `persistence_enabled = false`, `production_supabase_required = false`, `production_supabase_connected = false`, `recommendation_record_created = false`, `paper_order_created = false`, `broker_execution_enabled = false`, `broker_api_called = false`, `real_money_order_placed = false`, `network_services_called = false`, and `secrets_required = false`.
- **Advisory framing:** Output must include key reasons, main risks, invalidation conditions, paper-trading non-action framing, and explicit Harness Engineering human-decision framing for any real-money decision.
- **Validation notes:** `symbol` required; current Phase 4A skeleton accepts canonical four-digit Hong Kong equity symbols matching `0000.HK` format, for example `0700.HK`.
- **Error cases:** `VALIDATION_ERROR`, `NOT_FOUND`, `AGENT_CONTRACT_VIOLATION`, `INTERNAL_ERROR`.

### `GET /api/v1/stocks/{symbol}`
- **Purpose:** Fetch canonical stock reference and latest context.
- **Path parameters:** `symbol` (required).
- **Request body:** None.
- **Response shape:** Required success envelope with stock record in `data`.
- **Validation notes:** `symbol` must be URL-safe and canonical.
- **Error cases:** `VALIDATION_ERROR`, `NOT_FOUND`, `INTERNAL_ERROR`.

### `GET /api/v1/strategy-recommendations/{recommendation_id}`
- **Purpose:** Retrieve one strategy recommendation by identifier.
- **Path parameters:** `recommendation_id` (required).
- **Request body:** None.
- **Response shape:** Required success envelope with recommendation object in `data`.
- **Validation notes:** `recommendation_id` must be valid id format.
- **Error cases:** `VALIDATION_ERROR`, `NOT_FOUND`, `INTERNAL_ERROR`.

### `POST /api/v1/strategy-recommendations`
- **Purpose:** Persist/create a strategy recommendation record.
- **Path parameters:** None.
- **Request body:** Strategy recommendation payload fields defined in this document.
- **Response shape:** Required success envelope with created recommendation in `data`.
- **Validation notes:** required fields must be present; labels/score ranges validated.
- **Error cases:** `VALIDATION_ERROR`, `AGENT_CONTRACT_VIOLATION`, `INTERNAL_ERROR`.

### `POST /api/v1/simulation/paper-orders`
- **Purpose:** Create a paper-trading order record for the Simulation Desk while preserving the origin distinction between human-recorded paper trades and system-generated learning simulations.
- **Path parameters:** None.
- **Request body:** `{ "portfolio_id": "...", "symbol": "...", "side": "buy|sell", "quantity": n, "simulation_origin": "user_recorded|system_generated_learning" }`.
- **Response shape:** Required success envelope with created paper order data in `data`; the required envelope fields (`request_id`, `status`, `data`, `metadata`, `schema_version`, `generated_at`, `source`, `warnings`) must not be renamed or removed.
- **Validation notes:** non-negative quantity; portfolio must exist; `simulation_origin` must be either `user_recorded` or `system_generated_learning`; response warnings/metadata must state paper-only, advisory-only behavior and no real-money order placement.
- **`user_recorded` validation:** requires human/user source semantics such as `created_by_type`, `user_recorded_notes`, user/source notes, user rationale, and optional `source_recommendation_id` / `strategy_recommendation_id` when linked to a recommendation. It must not imply AI self-generated learning unless an explicit learning-proposal linkage exists.
- **`system_generated_learning` validation:** requires original recommendation linkage, original scores, original thesis, entry/exit assumptions, `system_learning_reason`, `learning_proposal_id` when applicable, and `requires_human_review = true` for learning proposal references. It may create reviewable learning proposals in later persistence/runtime PRs, but proposals must not be auto-applied or silently mutate production strategy logic.
- **Prohibited metadata states:** `real_money_order_placed`, `real_money_trading_automation_enabled`, `autonomous_real_money_execution`, `broker_execution_enabled`, `broker_api_called`, `production_supabase_connected`, and `secrets_required` must remain false for Task 008G local validation and for any later non-real-money runtime until explicitly approved.
- **Error cases:** `VALIDATION_ERROR`, `NOT_FOUND`, `INTERNAL_ERROR`.

### `GET /api/v1/paper-portfolios/{portfolio_id}`
- **Purpose:** Return paper portfolio state and recent snapshots.
- **Path parameters:** `portfolio_id` (required).
- **Request body:** None.
- **Response shape:** Required success envelope with portfolio object in `data`.
- **Validation notes:** `portfolio_id` must be valid id format.
- **Error cases:** `VALIDATION_ERROR`, `NOT_FOUND`, `INTERNAL_ERROR`.

### `GET /api/v1/agent-runs/{agent_run_id}`
- **Purpose:** Return traceability details for one agent run.
- **Path parameters:** `agent_run_id` (required).
- **Request body:** None.
- **Response shape:** Required success envelope with run and output summary in `data`.
- **Validation notes:** `agent_run_id` must be valid id format.
- **Error cases:** `VALIDATION_ERROR`, `NOT_FOUND`, `INTERNAL_ERROR`.

### `GET /api/v1/project-status`
- **Purpose:** Provide current project/task status snapshot from source-of-truth docs.
- **Path parameters:** None.
- **Request body:** None.
- **Response shape:** Required success envelope with phase, milestone, and task statuses in `data`.
- **Validation notes:** read-only endpoint.
- **Error cases:** `INTERNAL_ERROR`.


## Analyze-Stock Stub Contract (Phase 3 History)

The Phase 3 implementation of `POST /api/v1/analyze-stock` was intentionally a contract-first stub that prepared client, test, and workflow integration for Phase 4. It did not claim to perform investment research or produce a real recommendation.

Historical Phase 3 stub characteristics:

- Returned the exact success envelope.
- Returned `analysis_status = "stub_only"`.
- Returned one preferred strategy label so downstream clients could validate enum handling.
- Included reasoning, risks, invalidation conditions, and human-decision framing even though the content was placeholder.
- Included warnings that no live analysis, persistence, production Supabase, or trading execution occurred.
- Included `agent_trace` flags showing that agent runs, agent outputs, persistence, and production Supabase were not active.

PR #10 / Phase 4A replaces the current runtime behavior with the deterministic local-only `phase4a_skeleton` workflow described in the endpoint specification above. This Phase 3 section is historical and must not be used as the current runtime contract after Phase 4A.

## Explicit Error Envelope

```json
{
  "request_id": "uuid",
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable error message",
    "details": {}
  }
}
```

## Basic Error Codes

- `VALIDATION_ERROR`
- `NOT_FOUND`
- `AGENT_CONTRACT_VIOLATION`
- `INTERNAL_ERROR`

## Common Agent Contract Shape

All eight agent outputs use this exact field set:

```json
{
  "agent_name": "string",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "string",
  "evidence": [],
  "score": 0,
  "confidence": 0,
  "key_findings": [],
  "risks": [],
  "invalidation_conditions": [],
  "generated_at": "ISO-8601 timestamp",
  "schema_version": "v0.1"
}
```

## Agent Department JSON Examples (All 8, Common Shape)

These examples show the current Phase 4B local-only adapter preview semantics. They demonstrate the common shape without claiming live data, filings, news feeds, OHLCV bars, portfolio records, simulation records, broker commentary, production Supabase reads, persistence writes, paper orders, or real-money orders.

### 1) Market Intelligence Agent
```json
{
  "agent_name": "Market Intelligence Agent",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Local deterministic market-context adapter preview for a Hong Kong equity symbol.",
  "evidence": [
    "Local placeholder only: normalized symbol and static HKEX/HKD context; no live index, macro, liquidity, filing, news, OHLCV, portfolio, simulation, or broker data was fetched."
  ],
  "score": 54,
  "confidence": 20,
  "key_findings": [
    "Market-context score is deterministic scaffolding and is not live market research."
  ],
  "risks": [
    "Do not interpret the placeholder market-context score as live macro, liquidity, or index analysis."
  ],
  "invalidation_conditions": [
    "Invalidate if market data, macro data, liquidity data, or network services are claimed or introduced without reviewed authorization."
  ],
  "generated_at": "2026-06-02T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 2) Company Research Agent
```json
{
  "agent_name": "Company Research Agent",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Local deterministic company-research adapter preview for a Hong Kong equity symbol.",
  "evidence": [
    "Local placeholder only: normalized symbol and static HKEX/HKD context; no financial statements, filings, research documents, or broker commentary were fetched."
  ],
  "score": 48,
  "confidence": 20,
  "key_findings": [
    "Company-research score is deterministic scaffolding and is not financial-statement analysis."
  ],
  "risks": [
    "Do not interpret the placeholder company score as valuation, filings, or earnings research."
  ],
  "invalidation_conditions": [
    "Invalidate if filings, financial statements, research documents, or broker commentary are claimed or introduced without reviewed authorization."
  ],
  "generated_at": "2026-06-02T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 3) News & Sentiment Agent
```json
{
  "agent_name": "News & Sentiment Agent",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Local deterministic news-and-sentiment adapter preview for a Hong Kong equity symbol.",
  "evidence": [
    "Local placeholder only: normalized symbol and static HKEX/HKD context; no news feeds, social feeds, headlines, filings, or broker commentary were fetched."
  ],
  "score": 46,
  "confidence": 20,
  "key_findings": [
    "News-and-sentiment score is deterministic scaffolding and is not headline or feed analysis."
  ],
  "risks": [
    "Do not interpret the placeholder sentiment score as live news, social, or broker-commentary analysis."
  ],
  "invalidation_conditions": [
    "Invalidate if news feeds, social sentiment, headlines, or broker commentary are claimed or introduced without reviewed authorization."
  ],
  "generated_at": "2026-06-02T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 4) Technical Analysis Agent
```json
{
  "agent_name": "Technical Analysis Agent",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Local deterministic technical-analysis adapter preview for a Hong Kong equity symbol.",
  "evidence": [
    "Local placeholder only: normalized symbol and static HKEX/HKD context; no prices, OHLCV bars, volume, indicators, or broker data were fetched."
  ],
  "score": 44,
  "confidence": 20,
  "key_findings": [
    "Technical score is deterministic scaffolding and is not OHLCV-derived analysis."
  ],
  "risks": [
    "Do not interpret the placeholder technical score as chart, price, volume, or indicator analysis."
  ],
  "invalidation_conditions": [
    "Invalidate if prices, OHLCV bars, volume, or indicators are claimed or introduced without reviewed authorization."
  ],
  "generated_at": "2026-06-02T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 5) Risk Manager Agent
```json
{
  "agent_name": "Risk Manager Agent",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Local deterministic risk-manager adapter preview for a Hong Kong equity symbol.",
  "evidence": [
    "Local placeholder only: normalized symbol and static HKEX/HKD context; no portfolio holdings, exposure records, volatility feeds, or production database data were fetched."
  ],
  "score": 42,
  "confidence": 25,
  "key_findings": [
    "Risk score is deterministic scaffolding and is not portfolio or live volatility analysis."
  ],
  "risks": [
    "Do not interpret the placeholder risk score as portfolio sizing, exposure, or volatility guidance."
  ],
  "invalidation_conditions": [
    "Invalidate if portfolio holdings, exposure records, live volatility, persistence, or production Supabase are claimed or introduced without reviewed authorization."
  ],
  "generated_at": "2026-06-02T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 6) Investment Committee Agent
```json
{
  "agent_name": "Investment Committee Agent",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Local deterministic investment-committee synthesis adapter preview for a Hong Kong equity symbol.",
  "evidence": [
    "Local placeholder only: deterministic adapter previews; no persisted agent_runs, agent_outputs, research memos, filings, or live research records were fetched."
  ],
  "score": 52,
  "confidence": 20,
  "key_findings": [
    "Committee synthesis is deterministic scaffolding and is not a persisted committee review."
  ],
  "risks": [
    "Do not interpret the placeholder committee score as a reviewed investment committee decision."
  ],
  "invalidation_conditions": [
    "Invalidate if persisted agent runs, agent outputs, committee review records, or production database writes occur."
  ],
  "generated_at": "2026-06-02T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 7) Simulation Investment Desk
```json
{
  "agent_name": "Simulation Investment Desk",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Local deterministic simulation-desk adapter preview with no paper order creation.",
  "evidence": [
    "Local placeholder only: normalized symbol and static HKEX/HKD context; no simulation records, paper orders, portfolio snapshots, or trade reviews were fetched or created."
  ],
  "score": 49,
  "confidence": 15,
  "key_findings": [
    "Simulation score is deterministic scaffolding and does not create or inspect paper orders."
  ],
  "risks": [
    "Do not interpret the placeholder simulation score as paper-trading performance or order guidance."
  ],
  "invalidation_conditions": [
    "Invalidate if simulation records are fetched, paper orders are created, or paper-trading behavior is implied."
  ],
  "generated_at": "2026-06-02T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 8) Investment Strategy Office
```json
{
  "agent_name": "Investment Strategy Office",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Local deterministic strategy-office adapter preview for human decision support.",
  "evidence": [
    "Local placeholder only: deterministic department adapter previews; no strategy recommendation record, production Supabase data, or broker execution data was fetched or created."
  ],
  "score": 44,
  "confidence": 20,
  "key_findings": [
    "Strategy-office output is deterministic scaffolding for human review and is not a persisted recommendation."
  ],
  "risks": [
    "Do not interpret the placeholder strategy score as live investment research or real-money direction."
  ],
  "invalidation_conditions": [
    "Invalidate if a strategy recommendation is persisted, a broker API is called, or any real-money order is placed."
  ],
  "generated_at": "2026-06-02T00:00:00Z",
  "schema_version": "v0.1"
}
```
## Final Strategy Recommendation JSON Example

```json
{
  "request_id": "c06b2f5e-e4f7-4a26-a1f2-d650f2a4b9bc",
  "status": "success",
  "data": {
    "symbol": "0700.HK",
    "company_name": "Tencent Holdings Limited",
    "strategy_recommendation": "WAIT_FOR_PULLBACK",
    "summary": "Business quality remains strong, but near-term entry is extended.",
    "confidence_level": 72,
    "scores": {
      "market": 64,
      "fundamental": 70,
      "technical": 63,
      "sentiment": 58,
      "risk": 60,
      "simulation": 66
    },
    "key_reasons": [
      "Margin quality trend is improving",
      "Committee consensus favors patience on entry",
      "Simulation outcomes support staggered entries"
    ],
    "main_risks": [
      "Macro shock",
      "Policy uncertainty",
      "Volatility-driven stop-outs"
    ],
    "invalidation_conditions": [
      "Sustained margin compression",
      "Break below critical support",
      "Repeated adverse simulation outcomes without adaptation"
    ],
    "paper_trading_action": "Place staggered paper buy orders only on pullback zones.",
    "real_money_decision": "Human decision required by Harness Engineering.",
    "next_review_date": "2026-06-05"
  },
  "metadata": {
    "schema_version": "v0.1",
    "generated_at": "2026-05-22T00:00:00Z",
    "source": "HK_ALPHA_TEAM"
  },
  "warnings": []
}
```

## Contract Rules

- All endpoint responses must use the exact required response envelope.
- All strategy outputs must include reasoning, key risks, invalidation conditions, and human-decision framing.
- v1 remains advisory-only and non-execution for real-money trading.
