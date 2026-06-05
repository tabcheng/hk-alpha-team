# 06 Codex Workflow

## Purpose

Define how Codex tasks are planned, executed, reviewed, and logged.

## Required Reading Rule

Before starting a non-trivial Codex task, read at minimum:

- `AGENTS.md`
- `README.md`
- `docs/08-supabase-schema-design.md`
- `docs/09-api-and-agent-contracts.md`
- `docs/10-mvp-implementation-plan.md`
- `docs/11-project-status.md`
- `docs/decision-log.md`
- `docs/progress-log.md`

## Codex PR Factory

For recurring task-to-PR execution, use the Codex PR Factory governance workflow in `docs/20-codex-pr-factory.md`. The Factory defines task classes, role permissions, required gates, PR body expectations, evidence language, and source-of-truth-based follow-up handling.

The workflow below remains the compact execution model; the Factory document is the detailed review and governance layer for documentation-only, implementation-limited, and governance-sensitive / production-impacting PRs.

## Workflow Stages

1. **Task Definition**: document objective, scope, required outputs.
2. **Execution**: implement only what task scope permits.
3. **Validation**: check artifacts for coherence, Codex PR Factory gates, and boundary compliance.
4. **Commit & PR**: create traceable change sets.
5. **Log Update**: record decision/progress/lessons as needed.

## Large PR Policy

A PR is considered large when review quality may degrade due to size, cross-contract changes, or complexity.

Large PR handling:

1. Split into smaller PRs where feasible.
2. If not feasible, PR body must include the Factory PR body elements: summary, review map, grouped file changes, risk areas, validation evidence, scope compliance check, out-of-scope confirmation, and follow-up tasks.
3. Keep explicit scope/boundary checkpoint in the PR body.

## Mergeability Rule

A PR is not complete until it is mergeable.

## Review Loop Policy

When Harness Engineering provides re-review blockers:

1. Fix blockers exactly.
2. Update all explicitly required files.
3. Re-run validation checks and summarize evidence.
4. Keep out-of-scope changes out of the PR.

## Codex Rebase Guidance

Use:

```bash
git fetch origin main
git status --short
git rebase origin/main
```

Do **not** use `git rebase main` unless local `main` exists.

## Re-Review Rule

When Harness Engineering provides re-review blockers, fix blockers exactly:

- Use exact required schema table names.
- Use exact required MVP API endpoint names.
- Use exact required response envelope.
- Use exact required MVP phase model.
- Update all explicitly required files in the review note.

## Quality Expectations

- Explicitly state assumptions.
- Keep docs easy to skim and audit.
- Keep tasks documentation-only when requested.
- Do not claim 100% certainty; use "no known blockers" only when supported by review and validation evidence.
- Base next-task recommendations on current GitHub/repository source-of-truth review, not hard-coded temporary ChatGPT Project Instruction text.


## Mandatory Full PR Review Protocol

For every implementation-limited or governance-sensitive PR, reviewers must perform all checks below before approval:

1. Read PR metadata (title, body, scope, and explicit out-of-scope statements).
2. Check mergeability status.
3. List changed files and identify high-risk files first.
4. Check review threads and unresolved comments.
5. Check workflow/status checks (required and relevant non-required checks).
6. Inspect key changed files directly (not only summary views).
7. Check contract drift against source-of-truth docs (`README.md`, `docs/08`, `docs/09`, `docs/10`).
8. Check advisory-only / no-real-trading boundaries.
9. Check logs and project status updates (`docs/decision-log.md`, `docs/progress-log.md`, `docs/11-project-status.md`).
10. Approve only when no known blockers remain.

A PR must not be considered approved if unresolved review threads remain, even if top-level comments are positive.

Evidence closure for full PR reviews is defined in `docs/32-pr-review-evidence-closure-protocol.md`. Reviewers must use that protocol to classify public web search gaps, authenticated GitHub source-of-truth fallback, CI depth, local rerun limitations, branch protection visibility, expected-head-SHA merge locking, unresolved review threads, and post-merge source-of-truth verification.

