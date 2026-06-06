-- Task 008J local/test-only additive migration draft for Simulation Desk persistence alignment.
-- Do not apply to production Supabase without explicit Harness Engineering approval and Evidence Closure.
-- This draft does not connect production Supabase, does not introduce runtime persistence writes, and requires no secrets.
-- It is additive only: no canonical table renames, no column drops, and no destructive data rewrites.
-- Date: 2026-06-06

alter table paper_orders
  add column if not exists source_recommendation_id uuid,
  add column if not exists simulation_origin text check (simulation_origin in ('user_recorded', 'system_generated_learning')),
  add column if not exists paper_order_origin text check (paper_order_origin in ('user_recorded', 'system_generated_learning')),
  add column if not exists created_by_type text,
  add column if not exists user_recorded_notes text,
  add column if not exists system_learning_reason text,
  add column if not exists requires_human_review boolean not null default false,
  add column if not exists learning_proposal_id uuid,
  add column if not exists boundary_flags_json jsonb not null default '{}'::jsonb,
  add column if not exists outcome_preview_json jsonb not null default '{}'::jsonb,
  add column if not exists source_metadata_json jsonb not null default '{}'::jsonb;

alter table paper_positions
  add column if not exists simulation_origin text check (simulation_origin in ('user_recorded', 'system_generated_learning'));

alter table portfolio_snapshots
  add column if not exists simulation_origin_summary_json jsonb not null default '{}'::jsonb;

alter table trade_reviews
  add column if not exists simulation_origin text check (simulation_origin in ('user_recorded', 'system_generated_learning')),
  add column if not exists user_recorded_notes text,
  add column if not exists system_learning_reason text,
  add column if not exists improvement_suggestions_json jsonb not null default '[]'::jsonb,
  add column if not exists requires_human_review boolean not null default false;

alter table learning_proposals
  add column if not exists source_recommendation_id uuid,
  add column if not exists simulation_origin text check (simulation_origin in ('user_recorded', 'system_generated_learning')),
  add column if not exists requires_human_review boolean not null default true,
  add column if not exists auto_apply boolean not null default false;

do $$
begin
  if not exists (
    select 1
    from pg_constraint
    where conname = 'ck_learning_proposals_auto_apply_false'
  ) then
    alter table learning_proposals
      add constraint ck_learning_proposals_auto_apply_false check (auto_apply is false);
  end if;

  if not exists (
    select 1
    from pg_constraint
    where conname = 'fk_paper_orders_source_recommendation_id'
  ) then
    alter table paper_orders
      add constraint fk_paper_orders_source_recommendation_id
      foreign key (source_recommendation_id) references strategy_recommendations(id);
  end if;

  if not exists (
    select 1
    from pg_constraint
    where conname = 'fk_paper_orders_learning_proposal_id'
  ) then
    alter table paper_orders
      add constraint fk_paper_orders_learning_proposal_id
      foreign key (learning_proposal_id) references learning_proposals(id);
  end if;

  if not exists (
    select 1
    from pg_constraint
    where conname = 'fk_learning_proposals_source_recommendation_id'
  ) then
    alter table learning_proposals
      add constraint fk_learning_proposals_source_recommendation_id
      foreign key (source_recommendation_id) references strategy_recommendations(id);
  end if;
end;
$$;

alter table audit_events
  add column if not exists simulation_origin text check (simulation_origin in ('user_recorded', 'system_generated_learning'));

create index if not exists idx_paper_orders_simulation_origin_created_at_desc
  on paper_orders (simulation_origin, created_at desc);

create index if not exists idx_paper_orders_source_recommendation_created_at_desc
  on paper_orders (source_recommendation_id, created_at desc);

create index if not exists idx_paper_positions_simulation_origin_status
  on paper_positions (simulation_origin, status);

create index if not exists idx_trade_reviews_simulation_origin_reviewed_at_desc
  on trade_reviews (simulation_origin, reviewed_at desc);

create index if not exists idx_learning_proposals_simulation_origin_status_created_at_desc
  on learning_proposals (simulation_origin, status, created_at desc);

create index if not exists idx_audit_events_simulation_origin_created_at_desc
  on audit_events (simulation_origin, created_at desc);
