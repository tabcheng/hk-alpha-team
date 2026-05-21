# HK Alpha Team

HK Alpha Team is an **AI-assisted Hong Kong equity research and investment strategy advisory system**.

It is designed to support human decision-making with structured analysis, portfolio strategy proposals, paper trading records, simulation reviews, and iterative learning artifacts.

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

## Repository Purpose (Foundation Phase)

This repository currently provides project foundations:

- Vision and project brief documentation.
- Agent department definitions and operating boundaries.
- Strategy and simulation desk role split.
- Data and storage planning documents.
- Codex workflow, task sequencing, and project logs.

## Documentation Map

- `PROJECT_BRIEF.md` — concise project charter.
- `docs/00-project-vision.md` — long-form intent, boundaries, and outcomes.
- `docs/01-system-architecture.md` — conceptual architecture for early planning.
- `docs/02-agent-departments.md` — departmental agent responsibilities.
- `docs/03-investment-strategy-office.md` — strategy recommendation workflow.
- `docs/04-simulation-investment-desk.md` — simulation and paper-trading workflow.
- `docs/05-data-and-storage-plan.md` — initial data domain and storage plan.
- `docs/06-codex-workflow.md` — Codex task execution and collaboration model.
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
