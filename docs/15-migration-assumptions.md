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
