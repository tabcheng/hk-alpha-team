# 08 — Supabase Schema Design (Task 002)

## Purpose

Define the initial Supabase (Postgres) logical schema for HK Alpha Team v1 so future implementation PRs can build consistent migrations and application code.

## Scope and Boundaries

- Design-only artifact (no production migrations in this PR).
- Advisory/research/simulation first; no real-money execution features.
- No brokerage execution API entities.

## Design Principles

1. **Auditability first**: recommendations, simulation events, and governance updates are append-first.
2. **Human-in-the-loop**: strategy records store rationale, risks, and invalidation conditions.
3. **Separation of concerns**: research evidence, strategy outputs, and simulation outcomes are distinct domains.
4. **Extensible contracts**: JSONB used selectively for model/agent metadata while preserving strongly typed core fields.
5. **Multi-user ready**: user ownership is explicit even for single-user MVP operation.

## Logical Domains

- Identity and access
- Research workspace
- Strategy recommendations
- Simulation and portfolio tracking
- Learning and governance logs
- Operational telemetry (API + agent tracing)

## Schema Blueprint (v1)

## Primary HK Alpha Team Schema Table Names (Agreed Canonical Set)

These table names are the **primary schema contract** for v1 and align directly with the agreed data domains in project docs:

- `reference_securities`
- `research_artifacts`
- `strategy_records`
- `simulation_records`
- `governance_logs`

Supporting tables that remain part of v1:

- `profiles`
- `research_universes`
- `universe_members`
- `strategy_reviews`
- `simulation_runs`
- `paper_positions`
- `paper_trades`
- `simulation_metrics`
- `improvement_proposals`
- `api_request_logs`
- `agent_runs`

Naming rule for implementation PRs:
- When table names below differ from older draft names, implementation must use the canonical names above as the source of truth.

### 1) Identity and Access

#### `profiles`
Stores user profile metadata linked to Supabase Auth user IDs.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK | Same as `auth.users.id` |
| display_name | text | nullable |
| role | text | e.g., `owner`, `analyst`, `reviewer` |
| timezone | text | default `Asia/Hong_Kong` |
| created_at | timestamptz | default now() |
| updated_at | timestamptz | default now() |

Indexes:
- `idx_profiles_role` on `(role)`

---

### 2) Research Workspace

#### `research_universes`
Defines watchlists/universe buckets (e.g., Hang Seng Core, growth candidates).

| Column | Type | Notes |
|---|---|---|
| id | uuid PK |
| owner_user_id | uuid FK -> `profiles.id` |
| name | text | required |
| description | text | nullable |
| is_active | boolean | default true |
| created_at | timestamptz | default now() |
| updated_at | timestamptz | default now() |

#### `reference_securities`
Canonical security master records.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK |
| ticker | text | e.g., `0700.HK` |
| exchange | text | e.g., `HKEX` |
| name | text | issuer/company name |
| sector | text | nullable |
| currency | text | default `HKD` |
| is_active | boolean | default true |
| created_at | timestamptz | default now() |
| updated_at | timestamptz | default now() |

Constraints:
- Unique `(ticker, exchange)`

Indexes:
- `idx_securities_ticker`
- `idx_securities_sector`

#### `universe_members`
Many-to-many relation between universes and securities.

| Column | Type | Notes |
|---|---|---|
| universe_id | uuid FK -> `research_universes.id` |
| security_id | uuid FK -> `reference_securities.id` |
| added_by_user_id | uuid FK -> `profiles.id` |
| added_at | timestamptz | default now() |
| notes | text | nullable |

Constraints:
- Composite PK `(universe_id, security_id)`

#### `research_artifacts`
Structured qualitative/quantitative research notes.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK |
| owner_user_id | uuid FK -> `profiles.id` |
| security_id | uuid FK -> `reference_securities.id` |
| title | text | required |
| thesis | text | required |
| key_points | jsonb | list-like structure |
| sources | jsonb | links/references metadata |
| confidence | numeric(5,2) | 0–100 |
| status | text | `draft`, `reviewed`, `archived` |
| created_at | timestamptz | default now() |
| updated_at | timestamptz | default now() |

Indexes:
- `idx_research_notes_owner_security` `(owner_user_id, security_id)`
- `idx_research_notes_status`

---

### 3) Strategy Recommendations

#### `strategy_records`
Core advisory output table.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK |
| owner_user_id | uuid FK -> `profiles.id` |
| security_id | uuid FK -> `reference_securities.id` |
| research_note_id | uuid FK -> `research_artifacts.id` nullable |
| label | text | enum-like; preferred labels from AGENTS.md |
| confidence | numeric(5,2) | 0–100 |
| summary | text | concise recommendation statement |
| reasoning | text | required rationale |
| key_risks | jsonb | explicit risk framing |
| invalidation_conditions | jsonb | scenario triggers |
| time_horizon | text | e.g., `1-3m`, `3-12m` |
| status | text | `proposed`, `confirmed`, `superseded` |
| created_by_agent | text | agent department name/id |
| created_at | timestamptz | default now() |

Constraints:
- Check `label` in (`STRONG_WATCH`,`WAIT_FOR_PULLBACK`,`SMALL_POSITION`,`ACCUMULATE`,`HOLD`,`REDUCE_RISK`,`AVOID`)

Indexes:
- `idx_strategy_security_created_at` `(security_id, created_at desc)`
- `idx_strategy_label_status` `(label, status)`

#### `strategy_reviews`
Human review/approval layer for recommendations.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK |
| recommendation_id | uuid FK -> `strategy_records.id` |
| reviewer_user_id | uuid FK -> `profiles.id` |
| decision | text | `accept`, `revise`, `reject` |
| review_notes | text | nullable |
| created_at | timestamptz | default now() |

---

### 4) Simulation and Portfolio Tracking

#### `simulation_runs`
Top-level simulation job metadata.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK |
| owner_user_id | uuid FK -> `profiles.id` |
| name | text | required |
| objective | text | nullable |
| configuration | jsonb | position sizing, stop rules, etc |
| start_date | date | required |
| end_date | date | required |
| status | text | `queued`, `running`, `completed`, `failed` |
| created_at | timestamptz | default now() |
| completed_at | timestamptz | nullable |

#### `paper_positions`
Open/closed simulated positions.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK |
| simulation_run_id | uuid FK -> `simulation_runs.id` |
| security_id | uuid FK -> `reference_securities.id` |
| recommendation_id | uuid FK -> `strategy_records.id` nullable |
| side | text | `long` only in v1 |
| quantity | numeric(18,4) | required |
| entry_price | numeric(18,6) | required |
| exit_price | numeric(18,6) | nullable |
| opened_at | timestamptz | required |
| closed_at | timestamptz | nullable |
| status | text | `open`, `closed` |

Indexes:
- `idx_paper_positions_run_status` `(simulation_run_id, status)`

#### `paper_trades`
Append-only fill/event ledger to preserve losing and winning history.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK |
| position_id | uuid FK -> `paper_positions.id` |
| event_type | text | `entry`, `scale_in`, `scale_out`, `exit`, `stop` |
| event_time | timestamptz | required |
| price | numeric(18,6) | required |
| quantity | numeric(18,4) | required |
| fees | numeric(18,6) | default 0 |
| notes | text | nullable |
| created_at | timestamptz | default now() |

#### `simulation_metrics`
Materialized per-run metrics snapshot.

| Column | Type | Notes |
|---|---|---|
| simulation_run_id | uuid PK FK -> `simulation_runs.id` |
| total_return_pct | numeric(10,4) |
| max_drawdown_pct | numeric(10,4) |
| win_rate_pct | numeric(10,4) |
| profit_factor | numeric(10,4) |
| sharpe_proxy | numeric(10,4) nullable |
| generated_at | timestamptz | default now() |

---

### 5) Learning and Governance Logs

#### `governance_logs`
Improvement actions generated from simulation/review outcomes.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK |
| source_type | text | `simulation`, `review`, `incident` |
| source_id | uuid | references source entity |
| title | text | required |
| proposal | text | required |
| expected_impact | text | nullable |
| risk_of_change | text | nullable |
| status | text | `proposed`, `approved`, `implemented`, `rejected` |
| created_by | uuid FK -> `profiles.id` nullable |
| created_at | timestamptz | default now() |

#### `governance_events`
Immutable project/system governance record (policy changes, boundary changes).

| Column | Type | Notes |
|---|---|---|
| id | uuid PK |
| event_type | text | e.g., `policy_update`, `scope_change` |
| title | text | required |
| details | text | required |
| effective_date | date | required |
| recorded_by | uuid FK -> `profiles.id` nullable |
| created_at | timestamptz | default now() |

---

### 6) Operational Telemetry

#### `api_request_logs`
Request-level observability and traceability.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK |
| request_id | text | globally unique correlation id |
| actor_user_id | uuid FK -> `profiles.id` nullable |
| endpoint | text | required |
| method | text | required |
| status_code | int | required |
| latency_ms | int | required |
| error_code | text | nullable |
| created_at | timestamptz | default now() |

#### `agent_runs`
Execution envelope for agent calls.

| Column | Type | Notes |
|---|---|---|
| id | uuid PK |
| run_id | text | external/internal correlation id |
| department | text | e.g., `research`, `strategy`, `simulation` |
| input_payload | jsonb | redacted where necessary |
| output_payload | jsonb | contract-compliant output |
| status | text | `started`, `succeeded`, `failed` |
| error_code | text | nullable |
| started_at | timestamptz | required |
| finished_at | timestamptz | nullable |


## Design-Only SQL Migration Draft (Illustrative)

> This section is intentionally non-executable as-is and exists to validate naming/shape decisions before implementation PRs.

```sql
-- draft_v1_schema_outline.sql (design draft only)
create table profiles (
  id uuid primary key,
  display_name text,
  role text not null default 'owner',
  timezone text not null default 'Asia/Hong_Kong',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table securities (
  id uuid primary key default gen_random_uuid(),
  ticker text not null,
  exchange text not null,
  name text not null,
  sector text,
  currency text not null default 'HKD',
  is_active boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (ticker, exchange)
);

create table strategy_recommendations (
  id uuid primary key default gen_random_uuid(),
  owner_user_id uuid not null references profiles(id),
  security_id uuid not null references securities(id),
  label text not null check (label in (
    'STRONG_WATCH','WAIT_FOR_PULLBACK','SMALL_POSITION',
    'ACCUMULATE','HOLD','REDUCE_RISK','AVOID'
  )),
  confidence numeric(5,2) not null check (confidence >= 0 and confidence <= 100),
  summary text not null,
  reasoning text not null,
  key_risks jsonb not null default '[]'::jsonb,
  invalidation_conditions jsonb not null default '[]'::jsonb,
  created_at timestamptz not null default now()
);

create table simulation_runs (
  id uuid primary key default gen_random_uuid(),
  owner_user_id uuid not null references profiles(id),
  name text not null,
  configuration jsonb not null default '{}'::jsonb,
  start_date date not null,
  end_date date not null,
  status text not null check (status in ('queued','running','completed','failed')),
  created_at timestamptz not null default now()
);
```

## Relationship Summary

- One `profile` owns many universes, notes, recommendations, and simulation runs.
- One `security` links to many notes, recommendations, and positions.
- One recommendation may reference one research note and may have many human reviews.
- One simulation run has many positions; one position has many trade events.
- Improvement proposals can be linked back to simulation or review origins.

## Suggested Row-Level Security (RLS) Policy Model

- Enable RLS on all user-domain tables.
- Default policy: user can `select/insert/update` rows where `owner_user_id = auth.uid()`.
- Review/governance tables may use stricter roles (`reviewer`, `owner`).
- Service-role usage must be restricted to backend services only.

## Data Retention and Lifecycle

- Strategy and simulation history: retain indefinitely for auditability.
- API/agent telemetry: retain 180 days in MVP, then archive summaries.
- Soft-delete pattern preferred for research notes and universes (`is_active`/`status`) rather than hard delete.

## Out of Scope for This Document

- Concrete SQL migration files.
- Trigger/function implementation.
- Performance benchmarking and partitioning implementation.
