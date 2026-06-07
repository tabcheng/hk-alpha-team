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

## 2026-06-01 — PR #8 Analyze-Stock Stub and Mobile-First Strategy

### What Worked

- Adding the analyze-stock endpoint as a stub allowed backend contract testing to progress without pretending real research exists.
- Explicit stub warnings and human-decision framing preserved investment-system boundaries while enabling client integration.
- Documenting mobile-first environment tiers clarified which checks can be completed from GitHub/Codex CI and which infrastructure remains future scope.

### What to Improve

- Future Phase 4 work should replace stub internals with fixture-backed agent workflow tests before adding live data dependencies.
- Environment promotion should remain explicit so production Supabase, Railway, and secrets are not introduced as hidden prerequisites.

## 2026-06-05 — PR Review Evidence Closure Governance

### What Worked

- Converting recurring PR review limitations into explicit evidence classes and gates improves review consistency without requiring Harness Engineering to collect manual screenshots.
- Treating authenticated GitHub connector/API evidence as the source of truth for private or unindexed PRs reduces dependence on public web indexing.

### What to Improve

- Future full PR reviews should classify residual limitations explicitly instead of repeating vague caveats.
- Final review notes should pair no-known-blockers language with the latest reviewed head SHA, expected-head-SHA merge locking, review-thread status, CI depth, and post-merge source-of-truth verification.

## 2026-06-06 — Task 008G Simulation Desk Product-Concept Correction

### What Worked

- Separating `user_recorded` paper trades from `system_generated_learning` simulations clarified the Simulation Desk's product role before endpoint runtime or persistence writes were introduced.
- Encoding origin boundaries in local validation tests makes the contract easier to review without connecting production Supabase or creating paper orders.

### What to Improve

- Future Simulation Desk tasks should avoid reducing the desk to a single paper-order journal; recommendation-quality validation, losing-outcome visibility, and reviewable learning proposals are first-class product responsibilities.
- Runtime and persistence PRs should enforce origin fields at the boundary so user-entered records and system-generated learning simulations remain distinguishable and auditable.

## 2026-06-06 — Task 008H Commercial Readiness Governance

### What Worked

- Recording commercial-product expectations before implementation clarified that membership/subscription possibilities are governance and planning topics until explicit runtime PRs are approved.
- Pairing commercial-readiness language with Evidence Closure, web verification, and no-100%-certainty rules reduces the risk of overstated product claims.

### What to Improve

- Commercial-product standards should be documented before runtime, membership, subscription, billing, deployment, or public-facing product work begins.
- Future productization tasks should include explicit privacy, retention, entitlement, billing, compliance, security, and audit-trail review sections before implementation starts.

## 2026-06-06 — Task 008I Runtime Slice Follow-up

### What Worked

- Reusing the Task 008G origin contract at the API boundary kept `user_recorded` and `system_generated_learning` semantics aligned while enabling real backend behavior.
- Deterministic process-local IDs and timestamps made the in-memory runtime testable without introducing persistence, Supabase, secrets, or external services.
- Returning audit-event previews and learning-proposal previews allowed product workflow validation while preserving the no-auto-apply and no-database-write boundaries.

### What to Improve

- Future persistence work should explicitly map Task 008G/008I additive origin and boundary fields to SQL/schema changes before any Supabase write path is approved.
- Future Simulation Desk endpoint expansion should keep losing outcomes visible in fixtures and runtime responses, especially when portfolio valuation and review loops are added.
- PR scopes that cross from planning into runtime should keep status/log documentation changes in the same PR so M5 progress remains auditable without claiming completion early.

## 2026-06-06 — Task 008J Persistence Boundary Before Database Writes

### What Worked

- Introducing persistence through schema mapping, a local/test-only migration draft, and a deterministic adapter boundary creates review evidence before any database write path exists.
- Keeping persistence-intent payloads separate from a Supabase adapter makes it easier to verify that origin, advisory-only boundaries, audit lineage, learning proposal reviewability, and loss visibility survive the transition from runtime records to future table targets.

### What to Improve

- Future persistence work must not partially persist Task 008I runtime fields. Origin, guardrails, audit lineage, recommendation lineage, reviewable learning proposals, and losing outcome visibility must move together.
- Future Supabase adapter work should start from the Task 008J intent payloads and require separate approval, Evidence Closure, and tests proving that no unsafe production, vendor, broker, secret, auto-apply, loss-hiding, or overwrite behavior is introduced.
