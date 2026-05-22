# 09 — API and Agent Contracts (Task 003)

## Purpose

Define the exact required MVP endpoint set, response envelope, and agent contract examples for HK Alpha Team v1.

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

## Agent Department JSON Examples (All 8)

### 1) Market Intelligence Agent
```json
{"department":"Market Intelligence Agent","market_regime":"risk_off","key_drivers":["USD strength"],"watch_items":["HK liquidity"],"confidence":71}
```

### 2) Company Research Agent
```json
{"department":"Company Research Agent","symbol":"0700.HK","thesis":"Margin quality improving","catalysts":["ad demand"],"invalidation_conditions":["margin compression"],"confidence":68}
```

### 3) News & Sentiment Agent
```json
{"department":"News & Sentiment Agent","symbol":"0700.HK","sentiment":"neutral","material_events":["earnings guidance"],"confidence":62}
```

### 4) Technical Analysis Agent
```json
{"department":"Technical Analysis Agent","symbol":"0700.HK","trend":"uptrend","support_levels":[360.0],"resistance_levels":[392.0],"invalidation_level":352.0}
```

### 5) Risk Manager Agent
```json
{"department":"Risk Manager Agent","risk_level":"moderate","concentration_flags":["internet overweight"],"guardrails":["max position 5%"],"confidence":74}
```

### 6) Investment Committee Agent
```json
{"department":"Investment Committee Agent","posture":"WAIT_FOR_PULLBACK","consensus_score":0.64,"dissenting_views":["valuation stretched"],"open_questions":["policy sensitivity"]}
```

### 7) Simulation Investment Desk
```json
{"department":"Simulation Investment Desk","portfolio_id":"paper_001","paper_order_summary":"entered 2 orders","review_notes":"2 stop-outs due to volatility","improvement_candidates":["event filter"]}
```

### 8) Investment Strategy Office
```json
{"department":"Investment Strategy Office","label":"WAIT_FOR_PULLBACK","summary":"Quality intact, entry extended","reasoning":"near-term risk/reward not favorable","key_risks":["macro shock"],"invalidation_conditions":["earnings surprise with rerating"],"human_decision_required":true}
```

## Contract Rules

- All endpoint responses must use the exact required response envelope.
- All strategy outputs must include reasoning, key risks, invalidation conditions, and human-decision framing.
- v1 remains advisory-only and non-execution for real-money trading.
