# 14 — Codex Task Template

Use this template for future Codex task prompts to preserve consistency, scope control, and reviewability.

---

## Codex Task — PR #[NUMBER]: [SHORT TITLE]

### Context

[Describe current repository state, prerequisites, and what just merged.]

### Required Reading (Before Making Changes)

- `AGENTS.md`
- `README.md`
- `docs/08-supabase-schema-design.md`
- `docs/09-api-and-agent-contracts.md`
- `docs/10-mvp-implementation-plan.md`
- `docs/11-project-status.md`
- `docs/decision-log.md`
- `docs/progress-log.md`

### Goal

[State exactly what this PR must accomplish.]

### Scope Boundary

This PR is [documentation-only / implementation-limited].

Do not create:
- [item]
- [item]

Do not rename (unless explicitly approved with same-PR decision-log entry):
- canonical schema table names
- MVP API endpoint names
- response envelope fields
- strategy labels
- MVP phase names
- Investment Strategy Office required fields

Follow `AGENTS.md`.

### Git Sync / Rebase Guidance

Use:

```bash
git fetch origin main
git status --short
git rebase origin/main
```

Do **not** use `git rebase main` unless local `main` exists.

### Required Files to Add

Create:

```text
[path-1]
[path-2]
```

### Required Files to Update

Update:

```text
[path-3]
[path-4]
```

### Content Requirements

1. [requirement]
2. [requirement]
3. [requirement]

### Acceptance Criteria

- [ ] All required files are present.
- [ ] Requested content is complete and internally consistent.
- [ ] Scope boundaries were respected.
- [ ] Logs/status updated where needed.
- [ ] PR is mergeable.

### Commit Message Format

Use:

```text
[area]: [concise summary]
```

Examples:
- `docs: add PR review checklist and task template`
- `governance: update project status after PR #2 merge`

### PR Body Requirements

Include sections:

1. Summary of changes
2. Scope compliance check
3. Out-of-scope confirmation
4. Follow-up task linkage

---

## Practical Guidance

- Keep PRs coherent and auditable.
- Prefer explicit checklists over implicit expectations.
- If requirements conflict, prioritize direct user request, then AGENTS governance, then prior convention.
