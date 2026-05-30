# 18 — Lightweight Environment Strategy (Mobile-First)

## Purpose

Define the minimal environment model for current HK Alpha Team implementation work while Harness Engineering operates solo and primarily from mobile.

## Environment Model

- **DEV** = PR branch + Codex + GitHub Actions
- **UAT-like** = `main` branch + green CI + Harness Engineering review
- **PRODUCTION** = not created / disabled until explicit approval

## Operating Assumptions

1. Harness Engineering is a solo operator and mobile-first.
2. GitHub Actions is the primary validation surface for implementation quality.
3. Full DEV / UAT / PRODUCTION hosted environments are deferred in current phases.
4. Hosted Supabase, Railway, secrets, and production database wiring remain out of scope.
5. No Railway deployment, hosted Supabase setup, production secrets, or production database wiring may be added until explicitly approved.

## Trigger Conditions for Future Hosted Environments

### Hosted DEV Trigger

Only create a hosted DEV environment when **phone-accessible API testing is explicitly requested**.

### UAT Trigger

Only create UAT-like hosted infrastructure when **database-backed recommendation or simulation records require acceptance validation**.

### PRODUCTION Trigger

Only create PRODUCTION when both conditions are met:

1. Separate Harness Engineering approval is provided.
2. The same PR includes a `docs/decision-log.md` decision entry authorizing production enablement.

## Explicit Deferrals

- Railway runtime/deployment setup
- Hosted Supabase environment setup
- Production secrets
- Production database connection wiring

These remain out of scope until trigger conditions are satisfied and approved.


## Validation Surface

GitHub Actions remains the primary validation surface. PR branches and `main` branch status checks are the expected way to validate contract, backend, and migration readiness until hosted environments are explicitly approved.
