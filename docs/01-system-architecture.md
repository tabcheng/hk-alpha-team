# 01 System Architecture (Conceptual)

## High-Level Components

- **Research Intake Layer**: captures watchlists, thesis prompts, and market context.
- **Analysis Agent Layer**: generates structured research and risk-aware strategy suggestions.
- **Strategy Office**: consolidates recommendations and prepares human-review packets.
- **Simulation Desk**: runs paper trading and scenario analysis.
- **Knowledge & Audit Layer**: stores outputs, decisions, and lessons learned.

## Control Flow

1. Input research question or target security set.
2. Agents produce analysis artifacts and candidate strategies.
3. Strategy Office curates and presents recommendations.
4. Harness Engineering approves/rejects proposals.
5. Approved ideas are routed to Simulation Desk for paper execution.
6. Outcomes are logged and fed back into learning loops.

## Non-Functional Priorities

- Traceability
- Explainability
- Reproducibility
- Risk visibility

## Explicit Exclusion

No autonomous live-trade execution in architecture design.
