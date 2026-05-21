# HK Alpha Team

HK Alpha Team is an **AI-assisted Hong Kong equity research and investment strategy advisory system**.

It supports human decision-making through structured analysis, strategy proposals, paper trading records, simulation reviews, and iterative learning artifacts.

## Important Scope Boundary

HK Alpha Team is **not** an automated trading system.

- It does not execute real-money trades.
- It does not connect to broker execution APIs for autonomous order placement.
- It does not replace human judgment.

All real-money decisions remain under human control.

## Human-in-the-Loop Governance

The human user acts as **Harness Engineering** and is responsible for:

- Final investment decision approval.
- Risk acceptance and capital allocation decisions.
- Oversight of research quality, model behavior, and simulation integrity.

## Strategy Recommendation Labels

Preferred strategy labels:

- `STRONG_WATCH`
- `WAIT_FOR_PULLBACK`
- `SMALL_POSITION`
- `ACCUMULATE`
- `HOLD`
- `REDUCE_RISK`
- `AVOID`

Simple BUY/SELL outputs should be avoided unless they include context, confidence, key reasons, main risks, invalidation conditions, and explicit human decision framing.

## Repository Purpose (Foundation Phase)

This repository currently provides project foundations:

- Vision and project brief documentation.
- Agent department definitions and operating boundaries.
- Strategy and simulation desk role split.
- Data and storage planning documents.
- Codex workflow, task sequencing, and project logs.

## Documentation Map

- `PROJECT_BRIEF.md` — concise project charter.
- `AGENTS.md` — Codex governance, rules, and definition of done.
- `docs/00-project-vision.md` — long-form intent, boundaries, and outcomes.
- `docs/01-system-architecture.md` — conceptual architecture for early planning.
- `docs/02-agent-departments.md` — fixed eight-department model.
- `docs/03-investment-strategy-office.md` — final recommendation standards.
- `docs/04-simulation-investment-desk.md` — simulation learning and validation rules.
- `docs/05-data-and-storage-plan.md` — initial data domain and storage plan.
- `docs/06-codex-workflow.md` — Codex task execution and collaboration model.
- `docs/07-chatgpt-project-instructions.md` — GitHub copy of high-level project instructions.
- `docs/decision-log.md` — key project decisions.
- `docs/progress-log.md` — milestone progress tracking.
- `docs/lessons-learned.md` — retrospective notes and operational learning.

## Task Backlog (Codex)

- `codex-tasks/001-create-project-foundation.md`
- `codex-tasks/002-design-supabase-schema.md`
- `codex-tasks/003-design-api-and-agent-contracts.md`

## Current Status

Project is in **Phase 0: Foundation & Documentation**.
No backend/frontend/database implementation is included yet.
