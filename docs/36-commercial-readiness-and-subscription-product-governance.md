# 36 — Commercial Readiness and Subscription Product Governance

## Purpose

Task 008H establishes a documentation-only commercial-readiness governance baseline for HK Alpha Team before any further move into runtime, persistence, membership, subscription, billing, deployment, or user-facing product work.

This page records that Harness Engineering is treating HK Alpha Team as a serious market-bound product candidate that may later support membership or subscription offerings. It does not authorize implementation of subscription billing, payment processing, authentication runtime, entitlement runtime, deployment, production Supabase connection, live market data, broker integration, persistence writes, or real-money trading.

## Product Seriousness Statement

HK Alpha Team should be governed as a serious commercial product candidate even while the repository remains in foundation and MVP sequencing. Commercial seriousness means:

- GitHub `main` remains the source of truth for product scope, contracts, governance, and task status.
- Product claims must be reviewable against repository docs, code, validation output, and PR evidence.
- Market-facing language must stay conservative, advisory-only, and evidence-based.
- Future membership or subscription positioning must not imply guaranteed returns, automated wealth generation, or autonomous investment execution.
- Commercial features must be introduced through explicit PRs with scope, risks, validation evidence, and review closure.

## Market, Membership, and Subscription Readiness Framing

Future membership or subscription offerings may be considered only after explicit governance, security, privacy, compliance, entitlement, billing, support, and deployment work is approved in separate PRs.

Commercial readiness is therefore a planning posture, not an implementation claim:

- **Allowed now:** documentation, governance, readiness criteria, review protocols, product boundary language, and future-roadmap planning.
- **Not implemented by this task:** paid memberships, subscription plans, billing providers, payment collection, entitlement enforcement, authentication runtime, user dashboards, production deployment, live-data services, or runtime persistence.
- **Required later:** explicit implementation task, Harness Engineering approval, reviewed PR, validation evidence, and evidence closure for every commercial runtime capability.

## GitHub Main Source-of-Truth Rule

The repository, especially GitHub `main` after merge, is the canonical product record for:

- approved architecture and contracts;
- advisory-only and human-in-the-loop boundaries;
- Simulation Desk origin semantics;
- membership/subscription readiness decisions;
- validation evidence and known limitations;
- progress, decisions, and lessons learned.

ChatGPT Project Instructions and conversational context should remain lightweight and should defer to repository docs for project-specific contract and governance details.

## Web Verification Rule for Uncertain or Changeable Facts

Commercial-readiness reviews must verify uncertain, external, current, or changeable facts with web or primary-source evidence before using them in product claims, compliance assumptions, market positioning, competitor comparisons, technology choices, pricing assumptions, provider availability, payment terms, deployment terms, legal/regulatory statements, or user-facing subscription content.

Examples of facts requiring verification include:

- current laws, rules, regulatory guidance, platform terms, and payment-provider requirements;
- current vendor pricing, service availability, feature support, and documentation;
- market-size claims, competitor claims, benchmark claims, and public company facts;
- security, privacy, compliance, or deployment requirements that may have changed;
- any statement where uncertainty or outdated knowledge could materially mislead reviewers or users.

When verification is performed, the PR should identify the source type used, the date checked, and any remaining uncertainty. Repository docs should not overstate certainty based only on memory or unverified assumptions.

## Major PR Review Protocol

Major PRs, commercial-readiness PRs, runtime PRs, membership/subscription PRs, billing PRs, deployment PRs, or governance-sensitive PRs require full review protocol before merge.

A full review should include:

1. Confirm required-reading docs were considered.
2. Confirm branch freshness against `main`.
3. Review changed files and scope boundaries.
4. Check whether locked contract names, endpoint names, response envelope fields, canonical table names, preferred strategy labels, MVP phase names, or Investment Strategy Office required fields changed.
5. Verify local validation output and exact command output.
6. Review CI workflow conclusions and, where available, job-level logs or steps.
7. Check unresolved review threads.
8. Confirm PR body Factory sections are complete.
9. Confirm branch protection visibility or record residual limitations.
10. Use expected-head-SHA merge locking when appropriate.
11. Require post-merge source-of-truth verification for major governance changes.

Codex may prepare repository changes and draft PR evidence, but Codex does not self-approve the PR.

## Evidence Closure Language

Reviews should classify evidence precisely instead of implying impossible certainty.

### Closed Evidence

Use **closed evidence** when the reviewer directly inspected the relevant source and found it satisfies the review question. Examples include changed files reviewed locally, exact local command outputs captured, or authenticated PR metadata inspected.

### Reduced-Risk Evidence

Use **reduced-risk evidence** when the reviewer inspected evidence that lowers risk but does not fully close the question. Examples include a local rerun without access to private CI logs, public web search results for a private PR, or branch-protection assumptions that cannot be fully confirmed from the available environment.

### Residual Limitations

Use **residual limitations** for remaining gaps after review, including missing access, unavailable logs, unverified external assumptions, or environment constraints.

### Known Blockers

Use **known blockers** when review finds an issue that should prevent merge, such as failing required validation, scope violation, unresolved required review comments, missing PR body evidence, or contradiction with source-of-truth docs.

### No Known Blockers

Use **no known blockers** only when the available closed and reduced-risk evidence reveals no merge-blocking issue. This phrase must not be treated as a guarantee that no issue exists.

## No 100% Certainty Rule

HK Alpha Team review language must not claim 100% certainty, perfect correctness, guaranteed safety, guaranteed returns, or exhaustive risk elimination.

Acceptable review language should distinguish:

- what was directly checked;
- what was inferred from available evidence;
- what remains limited by access, environment, or uncertainty;
- what requires future verification or Harness Engineering approval.

## Product Concept Guardrails

HK Alpha Team is an AI investment research team, not a single paper trade app.

The product concept includes:

- multi-agent and multi-department research workflows;
- an Investment Strategy Office that produces structured strategy recommendations;
- a Simulation Desk that validates recommendation quality through paper-only review loops;
- advisory reports that include reasoning, risks, confidence, invalidation conditions, and human decision framing;
- learning logs and reviewable improvement proposals.

Mandatory guardrails:

- The Investment Strategy Office produces strategy recommendations, not autonomous real-money orders.
- The Simulation Desk supports two origins: `user_recorded` and `system_generated_learning`.
- `user_recorded` records are paper-only entries recorded by Harness Engineering / a human user.
- `system_generated_learning` simulations are paper-only system-generated simulations used to validate recommendation quality and produce reviewable learning proposals.
- Learning proposals must be reviewable and must not auto-apply.
- Losing simulations and losing paper trades must remain visible in reports and logs.
- Historical simulation recommendations must not be overwritten to improve appearance.
- Real-money trading must not be automated.
- Broker execution APIs for autonomous order placement remain prohibited unless a later explicit governance change approves tightly scoped non-autonomous behavior; v1 remains no-real-money-trading.
- Human review and Harness Engineering approval remain mandatory for real-money decisions.

## Commercial Readiness Roadmap

The following roadmap identifies governance areas that must be planned and reviewed before commercial launch. It does not implement any of these capabilities.

### Membership and Subscription Boundary

Future membership/subscription work must define what users receive, what remains advisory-only, what is not financial advice, what is paper-only, what is human-in-the-loop, and what outcomes are not guaranteed.

### User and Account Model

Future user/account planning must define account ownership, roles, profile fields, authentication approach, account lifecycle, support workflows, and administrative access limits before runtime auth is implemented.

### Entitlement and Access Control Planning

Future entitlement work must define plan capabilities, access levels, trial behavior, revocation behavior, downgrade behavior, auditability, and failure modes before enforcing paid access.

### Data Privacy and Retention

Future privacy work must define what user data is collected, why it is collected, how long it is retained, how it can be exported or deleted, and how simulation/history records are preserved for audit while respecting privacy obligations.

### Audit Trail

Future commercial runtime must preserve audit trails for recommendations, simulation events, user-entered paper trades, system-generated learning simulations, learning proposals, entitlement changes, billing status changes, administrative actions, and review decisions.

### Billing and Entitlement Planning

Future billing work must choose providers only after current provider documentation, terms, fees, regional availability, tax handling, dispute handling, refund workflows, and integration security requirements are verified. Billing status must not silently grant or revoke investment functionality without auditable entitlement records.

### Security and Secrets Policy

Future commercial implementation must keep secrets out of repository files, screenshots, logs, examples, and PR text. Supabase keys, Railway tokens, payment-provider secrets, broker credentials, and real-money account information must not be committed. Production secrets must use approved secret-management mechanisms only after explicit approval.

### Production Deployment Checklist

Future deployment PRs should include at minimum:

- environment separation;
- secret-management plan;
- production Supabase approval if applicable;
- migration and rollback plan;
- logging and audit plan;
- monitoring and incident response plan;
- privacy and retention review;
- billing/entitlement failure-mode review if commercial access is enabled;
- advisory-only and no-real-money-trading boundary checks;
- post-deployment verification steps.

### Compliance Disclaimers

Future public-facing materials must include clear advisory-only and no-guaranteed-return wording, and must avoid suggesting that HK Alpha Team replaces licensed professional advice where such advice is required. Legal, regulatory, and compliance claims must be verified against current primary sources or qualified review before publication.

### No-Guaranteed-Return / Advisory-Only Wording

Commercial copy should preserve wording such as:

- HK Alpha Team provides AI-assisted investment research and strategy-support artifacts for human review.
- Outputs are advisory-only and do not guarantee returns.
- Simulations and historical paper-trading outcomes do not guarantee future real-world performance.
- Real-money decisions remain solely with the human user / Harness Engineering.
- HK Alpha Team does not autonomously place real-money trades.

## Codex Role Boundary

Codex may:

- implement repository changes within the approved task scope;
- update docs, tests, and local validation artifacts when explicitly in scope;
- run local commands and report exact outputs;
- draft PR metadata and evidence maps for Harness Engineering review.

Codex must not:

- self-approve its own PR;
- claim merge readiness without evidence closure language;
- bypass Harness Engineering review;
- introduce secrets or production connections;
- implement runtime, persistence, billing, membership, auth, deployment, live data, broker integration, or real-money trading unless explicitly approved by a later task;
- silently change locked contracts or product boundaries.

ChatGPT / Harness Engineering performs full review, evidence closure, final approval judgment, and merge decision.

## Task 008H Scope Compliance

Task 008H is documentation-only. It records commercial-readiness governance before productization work begins.

Task 008H does not implement frontend/UI, backend runtime, FastAPI endpoints, persistence writes, SQL migrations, Supabase clients, production Supabase connections, billing/payment integration, membership/subscription runtime, authentication runtime, live market data, broker integration, deployment configuration, secrets, real-money trading, autonomous real-money execution, or locked contract renames.
