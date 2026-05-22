# 12 — Initial Conversation Brief

## Purpose

This document captures the original intent and guardrails established in the earliest HK Alpha Team conversations so implementation work can remain aligned as the repository grows.

## Original Intent Summary

HK Alpha Team is an AI-assisted Hong Kong equity research and investment strategy advisory system designed to improve human decision quality through:

- Structured multi-agent research synthesis.
- Clear recommendation framing with explicit risks.
- Paper-trading simulation before confidence scaling.
- Continuous learning through logged outcomes and review proposals.

## Core Product Boundaries (v1)

1. Advisory/reporting-first system, not auto-execution.
2. Human remains final decision-maker for all real-money actions.
3. No brokerage execution API integration.
4. No real-money trading automation.
5. Simulation outcomes are educational and process-improving, not guarantees.

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

## Why This Brief Exists

This brief protects intent continuity when future contributors join later phases. It should be referenced in implementation planning and PR reviews where scope pressure might push beyond v1 boundaries.

## Out of Scope for This Document

- No schema changes.
- No API contract edits.
- No implementation instructions.

