# 15 — Migration Assumptions (PR #4)

## Purpose

Capture explicit schema interpretation assumptions for the first migration draft so implementation remains aligned to canonical docs and contract-lock rules.

## Date

2026-05-24

## Assumptions

1. This migration is a **draft baseline** intended for review and iteration; it is not a production deployment instruction.
2. UUID primary keys use `gen_random_uuid()` with `pgcrypto` enabled.
3. Timestamps use `timestamptz` and default to `now()` where create-time tracking is required.
4. JSON extension fields in design docs are represented as `jsonb` with conservative defaults (`{}` or `[]`) to keep inserts explicit and auditable.
5. Foreign key `ON DELETE` actions are left as default `NO ACTION` for the draft, pending future deletion policy decisions.
6. Recommended indexes and uniqueness constraints from `docs/08-supabase-schema-design.md` are implemented where directly specified.
7. `strategy_recommendations.confidence_level` is constrained to `0..100` as explicitly required.
8. `agent_runs.status` is constrained to `started | succeeded | failed | timeout` as defined in schema design.
9. Paper trading and learning/audit tables are included as append-first records to preserve simulation traceability.
10. RLS policies are intentionally deferred to a dedicated follow-up implementation PR after schema baseline review.
11. Enum-like fields are partially constrained in this draft (`strategy_recommendations.strategy_recommendation`, `agent_runs.status`, `paper_orders.quantity`, `price_bars` high/low + volume checks); additional enumerated constraints (for example `paper_orders.side`, `paper_orders.order_type`, `paper_orders.status`, `paper_positions.status`, `trade_reviews.outcome_label`) are deferred pending implementation-level lifecycle policy finalization.
12. `strategy_recommendations` includes `investment_committee_review_id` (FK to `investment_committee_reviews.id`) to preserve review-to-recommendation lineage for governance traceability.

## Out-of-Scope in this PR

- No connection to production Supabase.
- No migration execution against hosted environments.
- No backend endpoint implementation.
- No auth or RLS policy rollout.
- No real-money or broker execution integration.

## Follow-up Needed

- Add local SQL execution checks in a dedicated environment-ready PR.
- Add RLS policy definitions and role tests after baseline schema acceptance.
- Add migration drift checks between SQL files and canonical docs as the migration set expands.

## Task 008J Migration Assumptions — Simulation Desk Persistence Alignment

Date: 2026-06-06

- `supabase/migrations/0002_align_simulation_desk_persistence_fields.sql` is a local/test-only additive migration draft.
- The draft exists to validate Task 008G/008I Simulation Desk runtime field alignment before any real Supabase write path is approved.
- Production Supabase application requires a later explicit Harness Engineering approval, separate PR scope, and Evidence Closure.
- Runtime persistence writes remain out of scope for Task 008J.
- A future Supabase adapter requires a separate PR and must not be inferred from the presence of a persistence-intent boundary.
- `0001_create_core_schema.sql` remains unchanged; Task 008J bridges gaps through additive `0002` only.
- Canonical table names must not be renamed by migration drafts.
- Destructive schema changes, column drops, production data rewrites, secrets, vendor/API calls, broker integrations, and real-money execution remain prohibited.
- Local/CI SQL validation should execute migration files in lexical order so `0001` and `0002` are validated together where PostgreSQL is available.

## Task 008J Blocker Closure — Canonical Lineage Field Types

Date: 2026-06-06

- Task 008J lineage columns that imply canonical database IDs use UUID-compatible fields in the local/test-only `0002` draft.
- `paper_orders.source_recommendation_id` references `strategy_recommendations(id)`.
- `paper_orders.learning_proposal_id` references `learning_proposals(id)`.
- `learning_proposals.source_recommendation_id` references `strategy_recommendations(id)`.
- Runtime fixture lineage strings remain preserved in JSON intent metadata rather than being stored in canonical UUID FK columns.
- Local SQL validation must check both UUID data types and lineage foreign-key constraints where PostgreSQL tooling is available.
