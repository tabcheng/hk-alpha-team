# 12 — Initial Conversation Brief

## Purpose

This document captures the original intent and guardrails established in the earliest HK Alpha Team conversations so implementation work can remain aligned as the repository grows.

## Primary User Role

The primary human operating role is **Harness Engineering**.

Harness Engineering is responsible for:

- Final real-money decision ownership.
- Oversight of AI research quality and recommendation framing quality.
- Enforcing advisory-only boundaries and contract-governed delivery.

## Original Intent Summary

HK Alpha Team is an AI-assisted Hong Kong equity research and investment strategy advisory system designed to improve human decision quality through:

- Structured multi-agent research synthesis.
- Clear investment strategy suggestions for human review.
- Paper-trading simulation before confidence scaling.
- Continuous learning through logged outcomes and review proposals.

## Product Positioning Clarification

The user does **not** want a professional trading dashboard as the primary product.

Primary value target for v1 is high-clarity, reviewable strategy guidance artifacts that help human decision-making under uncertainty.

## Core Product Boundaries (v1)

1. Advisory/reporting-first system, not auto-execution.
2. Human remains final decision-maker for all real-money actions.
3. No brokerage execution API integration.
4. No real-money trading automation.
5. Simulation outcomes are educational and process-improving, not guarantees.

## Exact HK Alpha Team Department Model

1. Market Intelligence Agent
2. Company Research Agent
3. News & Sentiment Agent
4. Technical Analysis Agent
5. Risk Manager Agent
6. Investment Committee Agent
7. Simulation Investment Desk
8. Investment Strategy Office

## Why Simulation Investment Desk Exists

Simulation Investment Desk exists to validate recommendation behavior through auditable paper-trading workflows before any confidence scaling. It preserves losing and winning outcomes for learning integrity and provides evidence for iterative improvement proposals.

## Why Investment Strategy Office Exists

Investment Strategy Office exists to convert cross-agent analysis into clear, human-reviewable strategy suggestion packets with consistent labels, rationale, risk framing, invalidation conditions, and confidence context.

## Required Recommendation Framing

Recommendations should be expressed using preferred labels:

- `STRONG_WATCH`
- `WAIT_FOR_PULLBACK`
- `SMALL_POSITION`
- `ACCUMULATE`
- `HOLD`
- `REDUCE_RISK`
- `AVOID`

Each recommendation should include:

- Key reasons and evidence summary.
- Main risk factors.
- Invalidation conditions.
- Confidence framing.
- Explicit human-decision reminder.

## System Design Direction from Early Conversations

- GitHub documentation and PR workflow are the source of truth.
- Contract-first design precedes implementation.
- Supabase + Railway remain planned platform targets.
- FastAPI is the planned backend surface.
- Optional lightweight UI/reporting layer after core workflows are stable.

## GitHub Source-of-Truth Rule

GitHub is the source of truth for project memory, progress, decisions, lessons, prompts, schemas, and Codex instructions.

## Why This Brief Exists

This brief protects intent continuity when future contributors join later phases. It should be referenced in implementation planning and PR reviews where scope pressure might push beyond v1 boundaries.

## Out of Scope for This Document

- No schema changes.
- No API contract edits.
- No implementation instructions.
