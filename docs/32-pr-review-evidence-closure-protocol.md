# 32 — PR Review Evidence Closure Protocol

## Purpose

The PR Review Evidence Closure Protocol is a governance protocol for full PR reviews in HK Alpha Team.

It defines how reviewers should close or classify evidence gaps without claiming unsupported certainty. It converts recurring review limitations into explicit evidence gates so future reviews can proceed from repository and authenticated GitHub source-of-truth evidence without requiring Harness Engineering to collect manual screenshots.

This protocol extends, but does not replace, the Codex PR Factory workflow in `docs/20-codex-pr-factory.md` and the Mandatory Full PR Review Protocol in `docs/06-codex-workflow.md`.

## Scope and Boundaries

This protocol is documentation and review governance only.

It does not add runtime code, backend routes, frontend behavior, endpoint implementation, persistence, SQL migrations, Supabase clients, production infrastructure, broker integration, real-money trading automation, or Task 008E work.

The protocol must preserve the project-wide advisory-only and human-in-the-loop investment boundary.

## Current Problem

Full PR reviews regularly encounter residual limitations that can be reduced or classified, but not always eliminated with available tools and permissions.

Recurring limitations include:

- public web search may not find the PR or repository, especially for private, newly created, or unindexed GitHub content;
- reviewers may not inspect every GitHub Actions log line for every workflow run;
- reviewers may not locally rerun every command that Codex or CI reports;
- branch protection or ruleset visibility may be unavailable because protected branch settings can require Administration-level read permission;
- the PR head commit can change between final review and merge.

These limitations should not be repeated as vague caveats. They should be converted into explicit evidence classes, review gates, and merge-lock instructions.

## Evidence Classification

Every full PR review should classify important evidence into one of three classes.

| Class | Definition | Examples | Review Handling |
|---|---|---|---|
| Closed evidence | Directly verified by GitHub connector, GitHub API, repository files, CI conclusions, review threads, changed-file diff, or local commands actually run by the reviewer. | Authenticated PR metadata, changed files, latest head SHA, repo file contents, passing CI conclusion, resolved review threads, local `git diff --check` output. | May support a no-known-blockers conclusion for the verified item. |
| Reduced-risk evidence | Partially verified with fallback evidence, but not fully closed at maximum depth. | Workflow conclusion checked but every log line not inspected; Codex exact command output present but reviewer did not locally rerun; public web search failed but authenticated GitHub connector resolved the PR and files. | May support review continuation when proportional to PR risk and explicitly disclosed. |
| Residual limitation | Cannot be fully closed with current permissions, tools, or available evidence. | Branch protection/ruleset settings hidden due to missing Administration read permission; unavailable public web indexing for a private PR; inability to download CI logs because connector capability is absent. | Must be recorded explicitly; must not be converted into unsupported certainty. |

## Public Web Availability Rule

Public web search is supplementary only.

Reviewers may use public web search to discover public repository or PR information, but public search is not the source-of-truth gate for private, newly created, or unindexed GitHub PRs.

Rules:

1. If public web search fails but an authenticated GitHub connector or GitHub API can read PR metadata, changed files, diff, CI status, review threads, and repository source files, the review can continue.
2. Public web search failure is not a blocker by itself.
3. GitHub connector or authenticated GitHub API inability to resolve the PR URL is a blocker for full PR review because the reviewer cannot establish PR source-of-truth evidence.
4. Review notes must explicitly state when public web evidence was unavailable and authenticated GitHub evidence was used instead.

## Authenticated GitHub Source-of-Truth Rule

For private, newly created, or unindexed PRs, authenticated GitHub connector or GitHub API evidence is the effective review source of truth when it can access the relevant objects.

Effective source-of-truth evidence includes:

- PR metadata, including title, body, base branch, head branch, mergeability, latest head SHA, and merge state;
- changed files and diff;
- commits and statuses associated with the PR;
- GitHub Actions workflow conclusions and, when risk requires it, jobs, steps, or logs;
- review comments and review threads;
- repository source files on the reviewed head;
- merge operations and merged PR metadata.

Review notes must explicitly disclose when public web search was unavailable and authenticated GitHub source-of-truth evidence was used instead.

## CI Depth Rule

CI evidence depth must be proportional to PR risk.

### CI Evidence Levels

| Level | Evidence Depth | Description |
|---|---|---|
| Level 1 | Workflow conclusion only | Reviewer checks workflow/status conclusions such as success, failure, cancelled, skipped, or pending. |
| Level 2 | Workflow conclusion plus job/step summaries | Reviewer checks workflow conclusions and job or step summary details for relevant workflows. |
| Level 3 | Job logs inspected or downloaded | Reviewer inspects or downloads relevant job logs, especially around failures, flakes, security, migrations, or ambiguous test output. |

### Required CI Level by PR Type

| PR Type | Minimum CI Evidence |
|---|---|
| Documentation-only low-risk | Level 1 is normally sufficient. |
| Documentation-only governance-sensitive | Level 1 plus exact command output in the PR body or final Codex response; Level 2 is required if CI ambiguity exists. |
| Implementation-limited | Level 1 plus exact command output; Level 2 is recommended. |
| Runtime / persistence / migration / production-impacting | Level 2 is required; Level 3 is required if failures, flakiness, security, migration, or test ambiguity exists. |
| Failed, flaky, or suspicious CI | Level 3 is required. |

Reviewers do not need to inspect every log line for every low-risk PR. However, if the CI evidence level used is below maximum depth, that choice must be proportional to risk and stated clearly.

GitHub Actions logs can be viewed or downloaded when tooling and permissions support it. If log access is unavailable, record the limitation and decide whether the PR risk requires blocking review until deeper CI evidence is available.

## Local Rerun Evidence Rule

A reviewer must not claim a local command rerun unless the reviewer actually performed it.

Rules:

1. ChatGPT reviewers must distinguish between commands personally rerun, CI-reported commands, and Codex-reported commands.
2. Codex must report exact command results in the PR body or final response for required validation.
3. CI success on the latest reviewed head plus exact Codex command output can support a no-known-blockers statement when proportional to PR risk, but it does not equal 100% certainty.
4. High-risk PRs may require a Codex rerun after the final commit, especially if the last commit changes runtime, persistence, migrations, security controls, workflow files, or locked contracts.
5. If a reviewer relies on Codex output instead of local rerun, the review note should classify that item as reduced-risk evidence unless CI or another direct source closes it.

## Branch Protection / Merge Rules Visibility Rule

Reviewers should attempt to inspect branch protection or ruleset evidence using available GitHub connector or GitHub API tooling when possible.

Rules:

1. Protected branch settings may include required status checks, strict up-to-date requirements, and conversation-resolution requirements.
2. Branch protection and ruleset API visibility can require Administration read permission.
3. If visibility is unavailable because the connector or token lacks permission, record it as a residual limitation.
4. Do not require Harness Engineering screenshots as part of routine review evidence closure.
5. If the repository later gains a connector action that can read branch protection or rulesets, the full PR review protocol should use it automatically.
6. Required status checks and conversation-resolution protection are preferred repository governance.
7. Hidden branch protection settings alone should not block a documentation-only PR if PR metadata, changed-file review, CI conclusions, review threads, and source-of-truth docs are otherwise clean.
8. Hidden branch protection settings may remain a blocker for production-impacting work if the reviewer cannot establish required merge safeguards by other evidence.

## Expected Head SHA Merge Rule

Every final full PR review must include the latest reviewed head SHA.

Required language:

```text
Merge only with expected head SHA: <sha>.
```

Rules:

1. Every final review must state the latest reviewed head SHA.
2. Every final review must say `merge only with expected head SHA`.
3. If ChatGPT, a GitHub connector, or GitHub API tooling performs the merge, it must use `expected_head_sha` or equivalent head-SHA safety checking when the tool supports it.
4. The GitHub merge API supports a head-SHA safety check: the PR head SHA must match the expected SHA before merge; if it does not match, merge should fail.
5. If the expected head SHA changes after final review, re-review is required before merge.

## Review Thread Closure Rule

Unresolved review threads are blockers.

Rules:

1. Any unresolved review thread is a blocker.
2. An outdated unresolved thread remains a blocker until it is resolved or explicitly superseded by a same-PR note and then resolved.
3. Top-level positive comments, approvals, or general “looks good” statements do not override unresolved review threads.
4. Reviewers must inspect review-thread status separately from top-level PR comments.
5. Final review language may only state no known review-thread blockers after unresolved thread evidence is checked.

## PR Body Evidence Closure Template

PR Factory PR bodies for full PR reviews should include the following reusable section when the PR is implementation-limited, governance-sensitive, or production-impacting.

```markdown
## Evidence Closure Checklist

- Public web result:
- Authenticated GitHub PR metadata checked:
- Latest reviewed head SHA:
- Branch freshness:
- Changed files reviewed:
- CI level used:
- Workflow conclusions:
- Job steps/logs inspected:
- Exact command outputs present:
- Local rerun performed:
- Branch protection visibility:
- Review threads unresolved:
- PR body Factory sections complete:
- Expected head SHA merge lock:
- Post-merge verification required:
```

The checklist should state whether each item is closed evidence, reduced-risk evidence, or a residual limitation when ambiguity exists.

## Final Review Language

Acceptable final review language includes:

- “No known blockers based on reviewed PR metadata, changed files, CI conclusions, resolved threads, and source-of-truth docs.”
- “Residual limitations remain and are listed below.”
- “Do not claim 100% certainty.”
- “Merge only with expected head SHA: `<sha>`.”

Reviewers must not claim 100% certainty. “No known blockers” is allowed only when tied to reviewed evidence and any residual limitations are listed.

## Post-Merge Verification Rule

After merge, perform a Source-of-Truth Reader pass on `main`.

Post-merge verification should confirm:

1. PR merged metadata, including merge commit or squash commit and merged timestamp when available.
2. Relevant docs, status files, and logs landed on `main`.
3. No out-of-scope runtime, persistence, migration, security-sensitive, production infrastructure, broker, or real-money trading automation changes landed.
4. The next-step recommendation is based on `main` branch source-of-truth, not stale PR branch assumptions.
5. If a post-merge check finds drift, missing files, failed required checks, or unexpected out-of-scope changes, open a follow-up issue or PR rather than silently treating the merge as fully verified.

## Relationship to Codex PR Factory

The Codex PR Factory remains the primary task-to-PR workflow. This protocol adds a review-evidence closure layer for full PR review.

Future Factory PRs should use this protocol to:

- decide whether web search failure is a blocker or a supplemental limitation;
- record authenticated GitHub evidence used as source of truth;
- choose CI depth proportional to risk;
- avoid unsupported local rerun claims;
- classify branch protection visibility gaps;
- enforce expected-head-SHA merge locking;
- block on unresolved review threads;
- require post-merge source-of-truth verification.
