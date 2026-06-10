# 14 — Codex Task Template

Use this template for future Codex task prompts to preserve consistency, scope control, and reviewability.

---

## Codex Task — PR #[NUMBER]: [SHORT TITLE]

### Context

[Describe current repository state, prerequisites, and what just merged.]

### Required Reading (Before Making Changes)

- `AGENTS.md`
- `README.md`
- `docs/13-pr-review-checklist.md`
- `docs/14-codex-task-template.md`
- `docs/20-codex-pr-factory.md`
- `docs/32-pr-review-evidence-closure-protocol.md`
- `docs/08-supabase-schema-design.md`
- `docs/09-api-and-agent-contracts.md`
- `docs/10-mvp-implementation-plan.md`
- `docs/11-project-status.md`
- `docs/decision-log.md`
- `docs/progress-log.md`

### Goal

[State exactly what this PR must accomplish.]

### Primary Deliverable

State the primary deliverable before listing scope details. Choose the best fit, or state a more specific equivalent:

- executable implementation
- tests/API-visible output
- runtime behavior
- validation evidence
- governance update
- documentation-only decision record

Fill in:

- **Primary deliverable:** [one of the examples above, or a specific equivalent]
- **Implementation-first fit:** [how this task produces runnable behavior, tests, API-visible output, or validation evidence]
- **Docs-only rationale:** [required if documentation-only; explain why implementation-limited delivery is not safe, not appropriate, or is blocked by a required governance gate]

For ordinary non-real-money product tasks, prefer executable, testable product capability over documentation-only progress when a safe implementation-limited vertical slice is available.

Use this target delivery mix unless the task explicitly requires a different balance:

- 65–75% implementation, tests, runtime behavior, or API-visible output.
- 15–20% validation, CI evidence, safety checks, and Evidence Closure.
- 10–15% documentation, status, progress, or decision updates.

If this is a docs-only task, explain why a safe implementation-limited slice is not safe, not appropriate, or blocked by a production-sensitive, security-sensitive, contract-changing, vendor/API, production Supabase, secrets, deployment, auth/payment, broker, or real-money governance gate.

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

- [ ] Primary deliverable is stated.
- [ ] All required files are present.
- [ ] Requested content is complete and internally consistent.
- [ ] Scope boundaries were respected.
- [ ] If docs-only, rationale is included for why a safe implementation-limited slice is not safe, not appropriate, or is blocked by a required governance gate.
- [ ] If implementation-limited, runnable behavior, tests, runtime behavior, or API-visible output are included where applicable.
- [ ] Validation evidence and CI expectations are documented.
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


### PR Body Metadata Limitation Rule

Codex should draft desired PR body content in its final response or PR notes.

Harness Engineering / ChatGPT reviewer must update GitHub PR body metadata directly when needed.

A PR body metadata blocker should not be assigned to Codex as a repository-file-only fix.

### PR Body Requirements

Include sections:

1. Summary
2. Primary Deliverable
3. Review Map
4. Grouped File Changes
5. Risk Areas
6. Validation Evidence
7. CI Evidence
8. Scope Compliance Check
9. Out-of-Scope Confirmation
10. Advisory-Only / No-Real-Money Boundary
11. Security / Secrets Check
12. Contract-Lock Check
13. Evidence Closure Checklist
14. Follow-Up Tasks
15. Post-Merge Verification Required

The Evidence Closure Checklist should include, at minimum:

- public web availability if used;
- authenticated GitHub source-of-truth status;
- latest reviewed head SHA;
- branch freshness;
- workflow conclusions;
- job/step inspection level;
- exact command outputs;
- local rerun classification;
- branch protection visibility;
- unresolved review thread status;
- PR body Factory sections complete;
- expected-head-SHA merge lock;
- post-merge verification requirement.

---

## Practical Guidance

- Keep PRs coherent and auditable.
- Prefer explicit checklists over implicit expectations.
- If requirements conflict, prioritize direct user request, then AGENTS governance, then prior convention.
