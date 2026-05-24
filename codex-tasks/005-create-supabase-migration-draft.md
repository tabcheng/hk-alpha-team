# Task 005 — Create Supabase Migration Draft

## Objective

Create a first-pass Supabase SQL migration draft that implements the canonical table contract from `docs/08-supabase-schema-design.md` without introducing out-of-scope runtime features.

## Prerequisites

- PR #2 merged.
- Canonical schema contract accepted as source of truth.
- No pending naming changes to locked contract elements.

## Migration Draft File Location

- Place migration draft SQL files under a repository-local migration draft path agreed in the task prompt (for example: `supabase/migrations/` or `docs/migration-drafts/`).
- Keep naming deterministic and reviewable (timestamp or ordered prefix + short description).
- Do not place migration drafts in ad-hoc locations outside the agreed path.

## In Scope

- Create draft SQL migration files for required MVP tables and relationships.
- Define primary keys, foreign keys, required indexes, and baseline constraints documented in the schema design.
- Keep migration artifacts readable and reviewable for contract validation.
- Include assumptions/open questions review notes tied to schema interpretation decisions.

## Out of Scope

- No backend API implementation.
- No frontend implementation.
- No deployment automation.
- No external data ingestion integrations.
- No brokerage execution integration.
- No real-money trading logic.
- No connection to production Supabase.

## Required Inputs

- `docs/08-supabase-schema-design.md`
- `docs/09-api-and-agent-contracts.md`
- `AGENTS.md`

## Deliverables

1. Initial migration SQL draft aligned to canonical schema contract.
2. Short migration-readiness note documenting assumptions/open questions.
3. Status/log updates reflecting Task 005 progress movement.

## Validation Checklist

- [ ] Table names exactly match canonical contract.
- [ ] Relationship graph matches schema design.
- [ ] Constraint/index choices are documented and minimal.
- [ ] Assumptions/open questions review notes are included.
- [ ] No connection to production Supabase is attempted.
- [ ] No prohibited implementation artifacts added.
- [ ] Documentation and status logs are updated.

## Log and Status Update Requirements

If schema contract interpretation is needed, update in the same PR:

- `docs/11-project-status.md`
- `docs/progress-log.md`
- `docs/decision-log.md`

## Definition of Done

Task 005 is done when migration draft artifacts are committed, contract-aligned, reviewable, include assumptions/open questions notes, do not touch production Supabase, and are accompanied by required status/progress/decision updates when interpretation decisions are made.
