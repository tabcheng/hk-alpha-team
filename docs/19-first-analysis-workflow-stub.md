# 19 — First Analysis Workflow Stub

## Purpose

Document the Phase 3 `POST /api/v1/analyze-stock` stub that prepares HK Alpha Team for Phase 4 — First Analysis Workflow.

The stub exists to make the locked API contract testable before live data ingestion, agent orchestration, persistence, deployment, or production infrastructure is introduced.

## Implemented Endpoint

`POST /api/v1/analyze-stock`

## Request Body

The endpoint accepts one canonical Hong Kong equity symbol in four-digit `.HK` format:

```json
{
  "symbol": "0700.HK"
}
```

Validation currently accepts symbols matching `0000.HK` format only.

## Success Response Shape

Successful responses use the required success envelope from `docs/09-api-and-agent-contracts.md`:

```json
{
  "request_id": "uuid",
  "status": "success",
  "data": {
    "symbol": "0700.HK",
    "analysis_status": "stub_only",
    "workflow_phase": "Phase 3 — Backend Skeleton",
    "strategy_recommendation": "STRONG_WATCH",
    "summary": "Contract-first placeholder response for future first-pass stock analysis.",
    "confidence_level": 0,
    "scores": {
      "market": null,
      "fundamental": null,
      "technical": null,
      "sentiment": null,
      "risk": null,
      "simulation": null
    },
    "key_reasons": [],
    "main_risks": [],
    "invalidation_conditions": [],
    "paper_trading_action": "No paper order is created by this stub.",
    "real_money_decision": "Human decision required by Harness Engineering; no real-money trade is executed.",
    "next_review_date": null,
    "agent_trace": {
      "agent_runs_created": false,
      "agent_outputs_created": false,
      "persistence_enabled": false,
      "production_supabase_required": false
    },
    "generated_at": "ISO-8601 timestamp",
    "schema_version": "v0.1"
  },
  "metadata": {
    "schema_version": "v0.1",
    "generated_at": "ISO-8601 timestamp",
    "source": "HK_ALPHA_TEAM"
  },
  "warnings": [
    "Stub response only; no live analysis, persistence, production Supabase, or trading execution performed."
  ]
}
```

The example lists empty arrays for some narrative fields only to show shape. The implemented stub returns placeholder content for reasons, risks, and invalidation conditions so downstream consumers can verify those fields exist.

## Validation Error Behavior

Malformed requests return HTTP `422` with the documented error envelope:

```json
{
  "request_id": "uuid",
  "status": "error",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": {
      "errors": [],
      "path": "/api/v1/analyze-stock"
    }
  }
}
```

Validation failures include missing `symbol` and symbols outside the current canonical four-digit `.HK` format.

## Stub-Only / Advisory-Only Warning

This endpoint is not a real analysis engine yet.

The Phase 3 stub:

- is advisory-shaped but not investment advice
- does not evaluate market, fundamental, technical, sentiment, risk, or simulation data
- does not create a strategy recommendation record
- does not create paper trades
- does not execute or recommend automated real-money trading actions
- keeps final real-money decisions with Harness Engineering

## What Is Not Implemented

The stub does not include:

- live market data ingestion
- financial statement ingestion
- news or document retrieval
- agent orchestration
- Supabase reads or writes
- `agent_runs` persistence
- `agent_outputs` persistence
- strategy recommendation persistence
- simulation desk integration
- Railway deployment
- hosted Supabase setup
- secrets management
- brokerage API integration
- live analysis logic
- automated execution logic

## Follow-Up Path Toward Phase 4 First Analysis Workflow

Phase 4 should replace the stub internals with a real first analysis workflow while preserving locked contract names and envelope fields.

Expected follow-up path:

1. Add fixture-backed first-analysis tests without live external dependencies.
2. Define agent workflow steps and expected intermediate outputs.
3. Add persistence adapters only after test/local database boundaries are documented.
4. Keep all outputs advisory-only with reasoning, risks, invalidation conditions, and human-decision framing.
5. Update `docs/09-api-and-agent-contracts.md`, `docs/17-backend-skeleton.md`, `docs/11-project-status.md`, `docs/progress-log.md`, and tests in the same PR when behavior changes.

Production Supabase, Railway deployment, live data providers, secrets, brokerage integration, and automated execution remain out of scope until explicitly authorized by future tasks and decisions.
