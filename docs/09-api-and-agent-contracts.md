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

## Common Agent Contract Shape

All agent outputs use this structure in `data`:

```json
{
  "agent_run_id": "uuid",
  "department": "Agent Department Name",
  "status": "success",
  "output": {},
  "confidence": 0,
  "generated_at": "ISO-8601 timestamp",
  "notes": []
}
```

## Agent Department JSON Examples (All 8, Common Shape)

### 1) Market Intelligence Agent
```json
{
  "agent_run_id": "run_market_001",
  "department": "Market Intelligence Agent",
  "status": "success",
  "output": {
    "market_regime": "risk_off",
    "key_drivers": ["USD strength"],
    "watch_items": ["HK liquidity"]
  },
  "confidence": 71,
  "generated_at": "2026-05-22T00:00:00Z",
  "notes": []
}
```

### 2) Company Research Agent
```json
{
  "agent_run_id": "run_company_001",
  "department": "Company Research Agent",
  "status": "success",
  "output": {
    "symbol": "0700.HK",
    "thesis": "Margin quality improving",
    "catalysts": ["ad demand"],
    "invalidation_conditions": ["margin compression"]
  },
  "confidence": 68,
  "generated_at": "2026-05-22T00:00:00Z",
  "notes": []
}
```

### 3) News & Sentiment Agent
```json
{
  "agent_run_id": "run_news_001",
  "department": "News & Sentiment Agent",
  "status": "success",
  "output": {
    "symbol": "0700.HK",
    "sentiment": "neutral",
    "material_events": ["earnings guidance"]
  },
  "confidence": 62,
  "generated_at": "2026-05-22T00:00:00Z",
  "notes": []
}
```

### 4) Technical Analysis Agent
```json
{
  "agent_run_id": "run_technical_001",
  "department": "Technical Analysis Agent",
  "status": "success",
  "output": {
    "symbol": "0700.HK",
    "trend": "uptrend",
    "support_levels": [360.0],
    "resistance_levels": [392.0],
    "invalidation_level": 352.0
  },
  "confidence": 66,
  "generated_at": "2026-05-22T00:00:00Z",
  "notes": []
}
```

### 5) Risk Manager Agent
```json
{
  "agent_run_id": "run_risk_001",
  "department": "Risk Manager Agent",
  "status": "success",
  "output": {
    "risk_level": "moderate",
    "concentration_flags": ["internet overweight"],
    "guardrails": ["max position 5%"]
  },
  "confidence": 74,
  "generated_at": "2026-05-22T00:00:00Z",
  "notes": []
}
```

### 6) Investment Committee Agent
```json
{
  "agent_run_id": "run_committee_001",
  "department": "Investment Committee Agent",
  "status": "success",
  "output": {
    "posture": "WAIT_FOR_PULLBACK",
    "consensus_score": 0.64,
    "dissenting_views": ["valuation stretched"],
    "open_questions": ["policy sensitivity"]
  },
  "confidence": 70,
  "generated_at": "2026-05-22T00:00:00Z",
  "notes": []
}
```

### 7) Simulation Investment Desk
```json
{
  "agent_run_id": "run_simulation_001",
  "department": "Simulation Investment Desk",
  "status": "success",
  "output": {
    "portfolio_id": "paper_001",
    "paper_order_summary": "entered 2 orders",
    "review_notes": "2 stop-outs due to volatility",
    "improvement_candidates": ["event filter"]
  },
  "confidence": 73,
  "generated_at": "2026-05-22T00:00:00Z",
  "notes": []
}
```

### 8) Investment Strategy Office
```json
{
  "agent_run_id": "run_strategy_001",
  "department": "Investment Strategy Office",
  "status": "success",
  "output": {
    "label": "WAIT_FOR_PULLBACK",
    "summary": "Quality intact, entry extended",
    "reasoning": "near-term risk/reward not favorable",
    "key_risks": ["macro shock"],
    "invalidation_conditions": ["earnings surprise with rerating"],
    "human_decision_required": true
  },
  "confidence": 72,
  "generated_at": "2026-05-22T00:00:00Z",
  "notes": []
}
```

## Final Strategy Recommendation JSON Example

```json
{
  "request_id": "c06b2f5e-e4f7-4a26-a1f2-d650f2a4b9bc",
  "status": "success",
  "data": {
    "recommendation_id": "rec_001",
    "symbol": "0700.HK",
    "label": "WAIT_FOR_PULLBACK",
    "confidence": 72,
    "summary": "Quality intact, entry extended",
    "reasoning": "near-term risk/reward not favorable",
    "key_risks": ["macro shock", "policy uncertainty"],
    "invalidation_conditions": ["earnings surprise with rerating"],
    "time_horizon": "3-12m",
    "entry_guidance": "Prefer staggered entries on pullbacks",
    "position_sizing_note": "Start small and scale with confirmation",
    "human_decision_required": true
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
