# AGENTS.md

## Project Mission

HK Alpha Team is an AI-assisted Hong Kong equity research and investment strategy advisory system.
Its mission is to help humans make better investment decisions through structured research, strategy recommendations, paper-trading simulations, and continuous learning logs.

## Target Tech Stack (Planned)

- GitHub (source of truth, version control, PR workflow)
- Codex Web (AI-assisted repository maintenance through reviewed PRs)
- Supabase (planned database/auth/storage backbone)
- Railway (planned deployment/runtime platform)
- Python FastAPI (planned backend API layer)
- Optional Next.js or simple web interface (planned user-facing layer)

## Repository Layout (Foundation Phase)

- `README.md` — high-level project identity, boundaries, and doc map.
- `PROJECT_BRIEF.md` — concise charter and scope definition.
- `AGENTS.md` — Codex governance, rules, and definition of done.
- `docs/` — canonical architecture, workflow, governance, and logs.
- `codex-tasks/` — sequenced implementation and design tasks.

## Engineering Rules

1. Keep all changes aligned to the current task scope.
2. Prefer small, reviewable, auditable pull requests.
3. Clearly state assumptions and unknowns in documentation.
4. Do not add implementation code unless the active task explicitly requires it.
5. Major project decisions must update relevant docs and logs in the same PR.

## Investment System Rules

1. HK Alpha Team is advisory/reporting-first in v1.
2. This project must not implement real-money trading in v1.
3. This project must not connect to brokerage execution APIs in the current phase.
4. All real-money decisions remain with the user (Harness Engineering).
5. Recommendations must include reasoning, risk framing, and invalidation conditions.

### Preferred Strategy Recommendation Labels

- `STRONG_WATCH`
- `WAIT_FOR_PULLBACK`
- `SMALL_POSITION`
- `ACCUMULATE`
- `HOLD`
- `REDUCE_RISK`
- `AVOID`

Avoid simple BUY/SELL outputs unless accompanied by context, confidence, key reasons, main risks, invalidation conditions, and explicit human decision framing.

## Simulation Rules

1. Simulation is required for learning and validation before confidence scaling.
2. Historical simulation recommendations must not be overwritten to improve appearance.
3. Losing paper trades must remain visible in reports.
4. Simulation results do not guarantee real-world performance.
5. Simulation outputs should generate reviewable improvement proposals, not silently alter production behavior.

## Documentation Rules

1. GitHub docs are the source of truth for architecture, decisions, progress, and lessons.
2. Use clear headings, concise sections, and explicit boundaries.
3. Record dates in `YYYY-MM-DD` format.
4. Keep logs current when scope, design, or policy changes.
5. Keep project details in repository docs so ChatGPT Project Instructions can remain lightweight.

## Testing and Verification Expectations

- Run basic repository checks before commit (`git status`, file presence, diff review).
- Verify that changes match requested files and scope.
- Confirm no unintended implementation artifacts are introduced.
- Confirm docs remain internally consistent (roles, boundaries, terms).

## Review Guidelines

- Reviewers should check boundary compliance first (no real-trading automation or broker API execution).
- Validate that strategy outputs remain advisory and human-in-the-loop.
- Confirm required logs/docs were updated for major governance decisions.
- Ensure PR description clearly states what changed and what remains out of scope.

## Definition of Done (Documentation Tasks)

A documentation task is done when:

1. All required files are created/updated.
2. Content matches requested governance and domain model.
3. Logs are updated where decisions/progress changed.
4. Scope constraints are respected (documentation-only when required).
5. Changes are committed and summarized in PR metadata.

## Security & Sensitive Information Warning (Do Not Commit)

Never include any of the following in repository files, examples, screenshots, or logs:

- Secrets of any kind
- API keys
- Supabase service role keys
- Railway tokens
- Broker credentials
- Real-money account information
