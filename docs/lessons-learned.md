# Lessons Learned

## 2026-05-21

### What Worked

- Starting with explicit scope boundaries clarified expected deliverables.
- Separating strategy and simulation responsibilities improved role clarity.

### What to Improve

- Add measurable quality criteria for research artifact reviews.
- Define minimal metadata standard early to reduce schema churn.

## 2026-05-22

### What Worked

- Enforcing exact naming/contracts from re-review comments reduced ambiguity.
- Keeping all updates documentation-only preserved scope compliance.

### What to Improve

- Apply exact required names/endpoints/envelope/phase model in all related files on first pass.
- Update status documents concurrently to avoid follow-up correction cycles.

## 2026-05-23 — PR #3 Governance Hardening Follow-up

### What Worked

- Governance hardening surfaced reusable assets (brief, checklist, task template) that improve repeatability.
- Converting reviewer feedback into explicit checklist/workflow rules improved auditability.
- Explicit required-reading and rebase guidance reduced avoidable review friction.

### What to Improve

- Update cross-linked source-of-truth files (`README.md`, workflow docs, lessons) in the same PR when governance artifacts are added.
- Include post-merge status handling expectations in review checklists earlier.
- Treat large-PR body structure requirements as mandatory from first draft, not as follow-up edits.

## 2026-05-24 — PR #4 Review Blockers Follow-up

### What Worked

- Converting review blockers into explicit repository links in `README.md` improved discoverability for migration/validation artifacts.
- Adding automated sensitive-assignment scanning to contract validation strengthened security guardrails early in implementation.

### What to Improve

- Treat scope wording in `docs/11-project-status.md` as a required consistency item whenever a PR crosses from documentation-only into implementation-limited work.
- Prefer adding enum/check-constraint policy notes in migration assumptions at the same time SQL constraints are introduced to reduce follow-up review cycles.


## 2026-05-26 — PR #5 Phase 2 SQL Validation Governance Follow-up

### What Worked

- Migration SQL execution checks were formalized for local/test DB usage before backend work.
- CI and review protocols identified FK/table creation order issues early.

### What to Improve

- Migration SQL must be executed in a local/test database before backend skeleton implementation begins.
- Foreign key and table creation order must be validated explicitly in migration drafts.
- Validation checks must assert results (for example counts/expected names), not only run `SELECT` statements.
- Unresolved review threads must be checked before final approval.



## 2026-05-26 — PR #6 Backend Skeleton Foundation

### What Worked

- Contract-first endpoint scaffolding reduced ambiguity before analysis-feature implementation.
- Adding backend CI coverage early improves confidence for subsequent Phase 3 endpoint work.

### What to Improve

- Add structured fixture-based contract tests for envelope shape reuse across future endpoints.
- Add consistent backend dependency management strategy (`requirements.txt` vs lockfile) in a follow-up infra task.


## 2026-05-26 — PR #6 Full Protocol Follow-up

### What Worked

- Full-protocol review surfaced repository-file fixes and governance gaps before merge.

### What to Improve

- PR body metadata updates must be applied by Harness Engineering / ChatGPT reviewer directly in GitHub when needed.
- Codex should treat PR body metadata blockers as guidance for draft content, not as repository-file-only completion blockers.


## 2026-05-27 — PR #7 Analyze-Stock Stub Hardening

### What Worked

- Stub-first endpoint delivery allowed contract progress without production integrations.
- Reusable envelope assertions made contract checks clearer and easier to extend for upcoming endpoints.

### What to Improve

- Add explicit symbol-format policy tests once canonical validation regex is approved.
- Add shared backend fixtures as endpoint count grows to reduce repeated assertion logic.

## 2026-05-30 — PR #7 Mobile-First Stub Review Follow-up

### What Worked

- Contract-first stubbing before real analysis clarified endpoint shape while preserving advisory-only boundaries.
- Mobile-first execution benefits from explicit PR/main/no-production environment contracts to avoid accidental infrastructure scope drift.

### What to Improve

- Advisory-only warnings should be embedded before live analysis starts so future outputs cannot be confused with investment recommendations.
- Keep hosted environment triggers explicit before adding Supabase, Railway, secrets, or production database wiring.
