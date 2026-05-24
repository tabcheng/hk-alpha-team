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
