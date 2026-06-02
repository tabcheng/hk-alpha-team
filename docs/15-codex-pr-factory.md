# 15 — Codex PR Factory Governance Workflow

## Purpose

The Codex PR Factory is the repeatable governance workflow for turning current GitHub source-of-truth docs into small, reviewable, auditable pull requests.

Its purpose is to:

- keep HK Alpha Team work aligned with repository contracts and status docs;
- separate reading, planning, implementation, validation, review, and log-update responsibilities;
- reduce contract drift while the project moves from documentation into implementation;
- preserve advisory-only, human-in-the-loop investment boundaries;
- make every PR reviewable through explicit evidence instead of broad certainty claims.

The Factory is a governance workflow, not a production runtime. It does not add backend features, frontend features, market data integration, production infrastructure, broker connectivity, or real-money trading automation.

## Tool Model

The approved PR Factory tool model is:

1. **ChatGPT** — task intake, source-of-truth interpretation, planning assistance, review reasoning, and follow-up task recommendations.
2. **Codex** — repository edits, validation commands, commits, and PR draft preparation under Harness Engineering review.
3. **GitHub Pull Requests** — auditable change review, discussion, approval, and merge record.
4. **GitHub Actions** — automated validation evidence for available contract, migration, backend, and future test workflows.

Claude Code is **not assumed** as part of this workflow. It may be considered later only if Harness Engineering explicitly approves it and records any required governance updates.

## Task Classes

### Documentation-Only

Documentation-only tasks may create or update repository docs, task cards, logs, checklists, templates, and governance notes.

Rules:

- Do not add backend implementation, frontend implementation, deployment code, database runtime changes, secrets, or market data integration.
- Run lightweight repository, documentation, and contract checks where available.
- Update progress/status logs when scope, phase, or governance state changes.

### Implementation-Limited

Implementation-limited tasks may add narrowly scoped code only when the active task explicitly authorizes it.

Rules:

- Keep code changes tied to locked contracts and documented scope.
- Add or update tests for changed behavior.
- Preserve the response envelope, canonical schema names, endpoint names, preferred strategy labels, MVP phase names, and Investment Strategy Office required fields unless a same-PR decision-log entry justifies a change.
- Do not silently expand into production infrastructure or real-money execution.

### Governance-Sensitive / Production-Impacting

Governance-sensitive or production-impacting tasks include changes that affect locked contracts, security boundaries, CI gates, deployment posture, database application, phase transitions, secrets handling, user-facing investment interpretation, or production runtime behavior.

Rules:

- Treat these as high-risk review items.
- Update the relevant source-of-truth docs and logs in the same PR.
- Require explicit PR body evidence for contract, advisory-only, security, status, and validation gates.
- Do not merge until Harness Engineering review confirms no known blockers remain.

## Workflow Roles

### Source-of-Truth Reader

Reads current repository docs before planning or editing.

Required sources usually include:

- `AGENTS.md`
- `README.md`
- `docs/06-codex-workflow.md`
- `docs/08-supabase-schema-design.md`
- `docs/09-api-and-agent-contracts.md`
- `docs/10-mvp-implementation-plan.md`
- `docs/11-project-status.md`
- `docs/decision-log.md`
- `docs/progress-log.md`
- `docs/lessons-learned.md`

### Task Planner

Translates task instructions and current source-of-truth state into a bounded file-change plan.

### Contract Reviewer

Checks proposed and actual changes against locked contracts:

- canonical schema table names;
- MVP API endpoint names;
- response envelope fields;
- preferred strategy labels;
- MVP phase names;
- Investment Strategy Office required fields.

### Codex Implementer

Makes approved repository edits within task scope, runs validation commands, reviews diffs, commits changes, and prepares PR metadata.

### Test Verifier

Runs available checks and distinguishes passing evidence from environment limitations or out-of-scope code checks.

### PR Reviewer

Performs GitHub PR review, checks unresolved threads, reviews CI status, and confirms scope and boundary compliance. Codex must not self-approve its own PR.

### Status/Log Updater

Updates project status, progress logs, decision logs, and lessons only when the task changes phase, progress, governance, or learning state.

## Role Permissions

| Role | Permission Level | May Modify Files? | Notes |
|---|---|---:|---|
| Source-of-Truth Reader | Read-only | No | Reads repository docs and current PR/task context. |
| Task Planner | Read-only planning | No | Produces a plan; does not edit files directly. |
| Contract Reviewer | Read-only review | No | Flags drift and required same-PR updates. |
| Codex Implementer | Edit under task scope | Yes | May modify files explicitly needed for the task and must commit changes. |
| Test Verifier | Validation/reporting | Usually no | May add or update validation artifacts only if task scope permits. |
| PR Reviewer | Review-only | No | Reviews and approves/rejects in GitHub; Codex must not self-approve. |
| Status/Log Updater | Edit governance docs | Yes | May update status/log docs when progress, phase, or decisions change. |

Codex can implement, validate, commit, and draft PR metadata, but Codex must not self-approve or claim final approval. Final review authority remains with Harness Engineering through the GitHub PR process.

## Required Gates

Every PR Factory task must address the gates below in proportion to task class and risk.

### Source-of-Truth Gate

Before editing, read current relevant docs and use GitHub/repository state as the source of truth. Do not rely on stale chat memory for phase, contract, or task status.

### Status-Sync Gate

If a task follows a merge, review current repository history and status docs. Update `docs/11-project-status.md` and progress logs when the project phase, task state, or milestone state changes.

### Scope Gate

Confirm the PR changes only what the task authorizes. Documentation-only tasks must remain documentation-only.

### Contract Lock Gate

Do not rename or reshape locked schema tables, API endpoints, response envelope fields, preferred strategy labels, MVP phase names, or Investment Strategy Office required fields without an explicit same-PR decision-log entry.

### Advisory-Only / No-Real-Money Gate

Confirm the PR does not introduce real-money trading automation, broker execution APIs, autonomous order placement, or output framing that replaces human investment judgment.

### Security/Secrets Gate

Confirm no secrets, API keys, Supabase service role keys, Railway tokens, broker credentials, real-money account details, or sensitive screenshots/logs are committed.

### CI/Validation Evidence Gate

Run available checks appropriate to the task and report exact commands/results. If code checks are unnecessary for documentation-only changes, say so clearly and still run available lightweight docs/contract checks.

### PR Review Gate

A PR is not complete until it is mergeable, relevant checks are reviewed, and unresolved review threads are addressed. Codex must not self-approve.

### Logs/Status Gate

Update progress/status/decision logs when the task changes governance state, project state, or implementation readiness. If a decision log is not changed, the PR body should explain why no new decision was recorded.

## PR Body Expectations

Each PR Factory pull request body should include:

- **Summary** — concise description of what changed.
- **Review Map** — files or sections reviewers should inspect first.
- **Grouped File Changes** — docs, code, tests, CI, logs, and status grouped separately where applicable.
- **Risk Areas** — known high-risk or governance-sensitive areas.
- **Validation Evidence** — exact commands and results, plus CI status when available.
- **Scope Compliance Check** — explicit confirmation against task scope.
- **Out-of-Scope Confirmation** — explicit statement of intentionally excluded work.
- **Follow-Up Tasks** — recommended next work based on current repository source-of-truth review.

## Evidence Language

PRs and review notes must avoid unsupported certainty claims.

Use evidence-based language such as:

- "validated by `python scripts/validate_contracts.py`";
- "no known blockers based on changed-file review and passing checks";
- "no code checks were required because this PR is documentation-only; lightweight contract validation was run."

Do not claim **100% certainty**. Use **"no known blockers"** only when supported by specific review evidence.

## Next-Step Handling Rule

Do not hard-code temporary next tasks inside ChatGPT Project Instructions.

Next task recommendations must be based on current GitHub source-of-truth review, including:

- `docs/10-mvp-implementation-plan.md` for the phase model;
- `docs/11-project-status.md` for current task and milestone state;
- `docs/09-api-and-agent-contracts.md` for locked API/agent contracts;
- current merged PR history and open review status.

After this Factory workflow is merged, Phase 4 recommendations should be framed as source-of-truth-derived follow-up work, not as permanent project-instruction text.
