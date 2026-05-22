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

### 1) Market Intelligence Agent
```json
{
  "agent_name": "Market Intelligence Agent",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Macro and liquidity context check for Hong Kong internet leaders.",
  "evidence": ["USD index trend", "HKD liquidity indicators"],
  "score": 64,
  "confidence": 71,
  "key_findings": ["Risk-off tone persists", "Funding conditions tighter"],
  "risks": ["Global growth slowdown"],
  "invalidation_conditions": ["Liquidity re-expansion and risk-on reversal"],
  "generated_at": "2026-05-22T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 2) Company Research Agent
```json
{
  "agent_name": "Company Research Agent",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Fundamental quality and earnings durability review.",
  "evidence": ["Latest annual report", "Margin trend analysis"],
  "score": 70,
  "confidence": 68,
  "key_findings": ["Margin quality improving", "Cash generation resilient"],
  "risks": ["Regulatory uncertainty"],
  "invalidation_conditions": ["Sustained margin compression"],
  "generated_at": "2026-05-22T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 3) News & Sentiment Agent
```json
{
  "agent_name": "News & Sentiment Agent",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Recent news-flow impact assessment.",
  "evidence": ["Earnings guidance headlines", "Sector sentiment feed"],
  "score": 58,
  "confidence": 62,
  "key_findings": ["Headline tone neutral", "Event risk still elevated"],
  "risks": ["Negative surprise headlines"],
  "invalidation_conditions": ["Consistent positive guidance revisions"],
  "generated_at": "2026-05-22T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 4) Technical Analysis Agent
```json
{
  "agent_name": "Technical Analysis Agent",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Trend and support/resistance profile review.",
  "evidence": ["Daily OHLCV bars", "Momentum indicators"],
  "score": 63,
  "confidence": 66,
  "key_findings": ["Uptrend intact", "Momentum flattening"],
  "risks": ["Break below support"],
  "invalidation_conditions": ["Close below 352.0"],
  "generated_at": "2026-05-22T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 5) Risk Manager Agent
```json
{
  "agent_name": "Risk Manager Agent",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Portfolio concentration and downside profile check.",
  "evidence": ["Sector exposure report", "Drawdown scenarios"],
  "score": 60,
  "confidence": 74,
  "key_findings": ["Moderate risk level", "Sector concentration notable"],
  "risks": ["Concentration drawdown"],
  "invalidation_conditions": ["Exposure reduced below guardrail threshold"],
  "generated_at": "2026-05-22T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 6) Investment Committee Agent
```json
{
  "agent_name": "Investment Committee Agent",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Cross-agent synthesis and dissent capture.",
  "evidence": ["Research memo", "Risk and technical briefs"],
  "score": 64,
  "confidence": 70,
  "key_findings": ["Consensus favors patience", "Valuation concerns remain"],
  "risks": ["Late-cycle volatility"],
  "invalidation_conditions": ["Material earnings beat with risk compression"],
  "generated_at": "2026-05-22T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 7) Simulation Investment Desk
```json
{
  "agent_name": "Simulation Investment Desk",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Paper-order outcomes and simulation behavior review.",
  "evidence": ["Paper order log", "Portfolio snapshots"],
  "score": 66,
  "confidence": 73,
  "key_findings": ["Execution discipline improved", "Stops triggered in volatility"],
  "risks": ["Gap risk in adverse sessions"],
  "invalidation_conditions": ["Repeated stop-out pattern without setup changes"],
  "generated_at": "2026-05-22T00:00:00Z",
  "schema_version": "v0.1"
}
```

### 8) Investment Strategy Office
```json
{
  "agent_name": "Investment Strategy Office",
  "agent_version": "v0.1",
  "stock_symbol": "0700.HK",
  "input_summary": "Final recommendation synthesis for human decision support.",
  "evidence": ["Committee review", "Simulation review", "Risk memo"],
  "score": 67,
  "confidence": 72,
  "key_findings": ["Quality remains intact", "Entry still extended"],
  "risks": ["Macro shock", "Policy uncertainty"],
  "invalidation_conditions": ["Earnings surprise with rerating"],
  "generated_at": "2026-05-22T00:00:00Z",
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
