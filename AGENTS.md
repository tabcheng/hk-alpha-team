# AGENTS.md

## Purpose

This file defines repository-wide operating instructions for human and AI contributors.

## Project Mission

Build HK Alpha Team as an AI-assisted research and strategy advisory environment for Hong Kong equities, with strict human control over real-money decisions.

## Non-Goals (Current Stage)

At this foundation stage, contributors should **not** introduce:

- Broker execution integrations.
- Autonomous trade execution logic.
- Production deployment infrastructure.
- Unrequested backend/frontend feature implementation.

## Contribution Rules

1. Keep changes aligned to the current Codex task scope.
2. Prefer explicit assumptions and clear risk disclosures in docs.
3. Maintain human-in-the-loop framing in all architecture and strategy content.
4. Update logs (`decision-log`, `progress-log`, `lessons-learned`) when significant project direction changes occur.
5. Keep documents modular, chronological, and easy to audit.

## Documentation Conventions

- Use clear section headings and short bullet points.
- Record dates in `YYYY-MM-DD` format.
- Distinguish between:
  - **Implemented now**
  - **Planned next**
  - **Out of scope**

## Change Control

When introducing or revising major project assumptions, update:

- `PROJECT_BRIEF.md`
- Relevant `docs/*.md` design files
- `docs/decision-log.md`
