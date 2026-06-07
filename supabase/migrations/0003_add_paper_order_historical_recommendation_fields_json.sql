-- Task 008K local/test PostgreSQL roundtrip alignment for Simulation Desk paper-order history metadata.
-- Do not apply to production Supabase without explicit Harness Engineering review and Evidence Closure.
-- This additive draft preserves original recommendation fields for local/test write/read validation only.
-- Date: 2026-06-07

alter table paper_orders
  add column if not exists historical_recommendation_fields_json jsonb not null default '{}'::jsonb;
