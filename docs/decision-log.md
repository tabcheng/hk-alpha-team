# Decision Log

| Date | Decision | Rationale | Impact |
|---|---|---|---|
| 2026-05-21 | GitHub is the source of truth for project documentation, architecture, decisions, progress, and lessons learned. | Keeps governance and design history versioned, auditable, and reviewable in one place. | Repository docs become canonical references for future tasks and reviews. |
| 2026-05-21 | Codex Web will generate and maintain repository files through PRs. | Enforces transparent, review-driven AI collaboration with explicit change sets. | All major AI-assisted updates flow through commit + PR workflows. |
| 2026-05-21 | Supabase and Railway are the planned infrastructure. | Provides a clear implementation direction while remaining in documentation-first phase. | Upcoming tasks can design schema/deployment assumptions against stable platform targets. |
| 2026-05-21 | v1 focuses on advisory/reporting, not automated trading. | Prevents scope drift and keeps risk governance human-centric from the start. | Architecture and outputs remain recommendation-focused rather than execution-focused. |
| 2026-05-21 | Paper trading and simulation are included from early design. | Enables validation and learning before any real-money confidence scaling. | Simulation desk and review loops are first-class design components. |
| 2026-05-21 | Final real-money decisions remain with the user. | Preserves explicit human authority and accountability. | System outputs must frame decisions as advisory with human approval boundaries. |
| 2026-05-21 | Project details should move into GitHub docs to keep ChatGPT Project Instructions lightweight. | Reduces prompt bloat while preserving project memory in versioned documentation. | High-level instructions remain concise; detailed governance lives in repository docs. |
