# 36 — Commercial Readiness and Subscription Product Governance

## Purpose

Task 008H established a commercial-readiness governance baseline for HK Alpha Team. Task 008K-Baseline clarifies the current Harness Engineering productization decision after Tasks 008I and 008J: **non-real-money productization is approved in principle and should move forward through scoped implementation PRs.**

This page records that Harness Engineering is treating HK Alpha Team as a serious market-bound product candidate that may later support membership or subscription offerings. It also records that real-money trading, autonomous real-money execution, and autonomous broker execution remain the hard prohibition. Other non-real-money productization work may proceed when each PR clearly states scope, evidence, tests, security handling, and post-merge verification.

## Product Seriousness Statement

HK Alpha Team should be governed as a serious commercial product candidate even while the repository remains in foundation and MVP sequencing. Commercial seriousness means:

- GitHub `main` remains the source of truth for product scope, contracts, governance, and task status.
- Product claims must be reviewable against repository docs, code, validation output, and PR evidence.
- Market-facing language must stay conservative, advisory-only, and evidence-based.
- Future membership or subscription positioning must not imply guaranteed returns, automated wealth generation, or autonomous investment execution.
- Commercial features must be introduced through explicit PRs with scope, risks, validation evidence, and review closure.

## Non-Real-Money Productization Approval Baseline

Harness Engineering has approved HK Alpha Team to move beyond planning into real non-real-money product development. This approval covers scoped implementation PRs for product capabilities such as:

- local/test database persistence;
- Supabase adapter design and later non-production/prod Supabase integration;
- backend service layers;
- endpoint runtime expansion;
- Simulation Desk write/read workflows;
- paper portfolio and paper trade recordkeeping;
- audit-event persistence;
- reviewable learning proposal persistence;
- deployment preparation;
- authentication and account models;
- membership/subscription and billing planning/runtime;
- vendor/API architecture and integrations;
- live market/fundamentals/news/search data integrations;
- non-real-money broker-sandbox research or paper-only broker-sandbox workflows.

This approval is not a blanket permission to merge unsafe or vague changes. Every implementation PR must still:

1. define exact scope and out-of-scope items;
2. preserve advisory-only, human-in-the-loop, and no-guaranteed-return framing;
3. preserve locked contracts unless the PR explicitly proposes a governance-sensitive contract change;
4. include tests and validation evidence proportional to risk;
5. update status, progress, decisions, and lessons in the same PR when product state changes;
6. classify evidence under the Evidence Closure Protocol;
7. avoid committing secrets, credentials, tokens, private keys, or real-money account information;
8. include post-merge source-of-truth verification.

The standing hard prohibition remains:

- no real-money trading;
- no autonomous real-money execution;
- no autonomous broker execution;
- no real-money account connection;
- no secrets leakage;
- no hidden or irreversible investment action.

## Market, Membership, and Subscription Readiness Framing

Future membership or subscription offerings may proceed through scoped implementation PRs after the relevant product, security, privacy, entitlement, billing, support, and deployment assumptions are documented and validated.

Commercial readiness is a productization posture, not a claim that all commercial runtime already exists:

- **Allowed now:** scoped non-real-money implementation work, local/test persistence, service adapters, deployment preparation, account/auth planning, entitlement/billing work, vendor/API integration work, and commercial-readiness documentation.
- **Still not implemented unless a PR adds it:** paid memberships, subscription plans, billing providers, payment collection, entitlement enforcement, authentication runtime, user dashboards, production deployment, live-data services, runtime persistence, or production Supabase.
- **Still required for every capability:** explicit implementation task, reviewed PR, validation evidence, Evidence Closure, and post-merge verification.

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

## Vendor / External Data Source Approval Gate

HK Alpha Team is expected to require external vendors, vendor APIs, online data sources, or third-party services over time. These may include market data providers, financial statement/fundamentals providers, news and sentiment providers, AI/model providers, search/web data providers, payment/billing providers, authentication providers, deployment/hosting providers, notification providers, and broker or broker-sandbox providers.

Harness Engineering approves the product architecture to include vendor/API integration capability in principle. Every specific vendor, vendor API, provider, paid data source, production external service, broker-sandbox provider, payment provider, authentication provider, live-data provider, deployment provider, or third-party service still requires separate discussion and explicit Harness Engineering approval in the scoped PR before it is selected, connected, implemented, required, or made production-facing or user-facing. This explicit per-vendor/provider approval gate is mandatory for single-vendor and multi-vendor cases; vendor discussion is not optional merely because only one vendor appears viable.

The responsible scoped PR must identify the vendor/service, current-source evidence where facts may change, cost/licensing/security implications, secret-management approach, validation evidence, Evidence Closure classification, and post-merge verification plan.

Before selecting, connecting, implementing, requiring, or making production-facing/user-facing any vendor, vendor API, or provider, the responsible PR must document:

1. vendor name and service category;
2. intended product use;
3. data fields or capabilities required;
4. whether the integration is read-only, write-capable, paid, production-facing, or user-facing;
5. pricing / usage-limit assumptions, checked against current vendor sources;
6. terms-of-service / licensing / redistribution constraints, checked against current vendor sources;
7. privacy, retention, and user-data implications;
8. security and secret-management plan;
9. failure modes, fallback behavior, and audit logging;
10. whether the integration could influence investment recommendations, simulations, billing, entitlements, or user-facing claims;
11. exact validation evidence and Evidence Closure classification.

Until a vendor PR is approved, implementation may include local interfaces, mock adapters, deterministic fixtures, or placeholder contracts that do not call the vendor, require secrets, fetch live data, incur cost, or create production dependency.

Real-money trading, autonomous real-money execution, and broker execution APIs for autonomous order placement remain prohibited unless Harness Engineering later makes a separate governance decision. v1 remains advisory-only and human-in-the-loop.

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

The following roadmap identifies governance areas that must be planned and reviewed before commercial launch. It does not claim these capabilities are already implemented.

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
- introduce secrets or production connections outside the approved task scope and secret-management plan;
- implement real-money trading, autonomous real-money execution, autonomous broker execution, or real-money account connectivity;
- silently change locked contracts or product boundaries.

ChatGPT / Harness Engineering performs full review, evidence closure, final approval judgment, and merge decision.

## Task 008H Scope Compliance

Task 008H was documentation-only. It recorded commercial-readiness governance before broader productization work began.

Task 008K-Baseline supersedes any reading that non-real-money productization is generally blocked. Non-real-money productization is approved in principle and may proceed through scoped PRs with Evidence Closure. Real-money trading, autonomous real-money execution, autonomous broker execution, real-money account connectivity, secrets leakage, and hidden or irreversible investment actions remain prohibited.
