# 13 — PR Review Checklist

Use this checklist for all HK Alpha Team PR reviews.

## Large PR Policy

A PR is considered **large** when any of the following are true:

- Net diff is substantial enough to risk review quality.
- More than one source-of-truth contract area is modified in one change set.
- Review cannot be completed confidently in one pass.

Large PR handling rules:

1. Prefer splitting into smaller PRs when dependency order allows.
2. If splitting is not practical, PR body must include:
   - review map
   - grouped file changes
   - explicit risk areas
   - explicit out-of-scope confirmation
3. Require explicit scope confirmation and out-of-scope list in PR body.
4. Require at least one checkpoint for boundary compliance (advisory-only, no execution integration).

## A. Scope and Boundary Compliance

- [ ] Changes match the stated task scope.
- [ ] No real-money trading automation introduced.
- [ ] No brokerage execution API integration introduced.
- [ ] No secrets or sensitive credentials included.

## B. Contract and Naming Integrity

- [ ] Canonical schema table names unchanged unless a same-PR `docs/decision-log.md` entry justifies change.
- [ ] MVP API endpoint names unchanged unless a same-PR `docs/decision-log.md` entry justifies change.
- [ ] Response envelope fields unchanged unless a same-PR `docs/decision-log.md` entry justifies change.
- [ ] Preferred strategy recommendation labels unchanged unless a same-PR `docs/decision-log.md` entry justifies change.
- [ ] MVP phase names unchanged unless a same-PR `docs/decision-log.md` entry justifies change.
- [ ] Investment Strategy Office required fields unchanged unless a same-PR `docs/decision-log.md` entry justifies change.

## C. Documentation and Log Currency

- [ ] Documentation updates are internally consistent with existing source-of-truth docs.
- [ ] `docs/progress-log.md` updated when meaningful progress changed.
- [ ] `docs/decision-log.md` updated when governance/design decisions changed.
- [ ] `docs/11-project-status.md` updated when task/milestone state changed.
- [ ] Post-merge status update plan is included when status changes are expected after merge.

## D. Consistency Audit Trigger

If `docs/09-api-and-agent-contracts.md` changed:

- [ ] `README.md` reviewed/updated.
- [ ] `codex-tasks/002-design-supabase-schema.md` reviewed/updated if schema/API coupling changed.
- [ ] `codex-tasks/003-design-api-and-agent-contracts.md` reviewed/updated.
- [ ] `docs/decision-log.md` updated.
- [ ] `docs/progress-log.md` updated.
- [ ] `docs/11-project-status.md` updated.

## E. Reviewability and Quality

- [ ] Diff is reviewable and coherent.
- [ ] Assumptions and unknowns are clearly documented.
- [ ] No unintended implementation artifacts were added for documentation-only tasks.
- [ ] Commit and PR description explain what changed and what remains out of scope.

## F. Implementation PR Validation Evidence

For implementation PRs:

- [ ] Tests were run and reported (or explicit rationale for no tests).
- [ ] Validation evidence is included (commands, outputs, or artifact checks).

## G. Completion Gate

- [ ] PR is mergeable (required for completion).
