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

## Workflow Stages

1. **Task Definition**: document objective, scope, required outputs.
2. **Execution**: implement only what task scope permits.
3. **Validation**: check artifacts for coherence and boundary compliance.
4. **Commit & PR**: create traceable change sets.
5. **Log Update**: record decision/progress/lessons as needed.

## Large PR Policy

A PR is considered large when review quality may degrade due to size, cross-contract changes, or complexity.

Large PR handling:

1. Split into smaller PRs where feasible.
2. If not feasible, PR body must include review map, grouped file changes, risk areas, and out-of-scope confirmation.
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
