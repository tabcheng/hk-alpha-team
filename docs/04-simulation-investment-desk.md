# 04 Simulation Investment Desk

## Core Role

The Simulation Investment Desk is a core learning and validation module. It evaluates recommendation quality through disciplined paper trading, structured post-outcome review, and auditable learning proposals.

The desk is **not** a real-money execution desk. It must preserve advisory-only, human-in-the-loop boundaries and must never connect to brokerage execution APIs for autonomous order placement.

## Dual Simulation-Origin Pipelines

Task 008G adopts two explicit simulation-origin pipelines so Simulation Desk records are not reduced to a single paper-order journal.

| Pipeline | Origin | Primary purpose | Learning impact |
|---|---|---|---|
| `user_recorded` | Human user / Harness Engineering | Record paper trades entered or recorded by the human user, including notes, rationale, linked recommendation when available, and trade review fields. | May inform review discussions, but must not imply AI self-generated learning unless explicitly linked to a learning proposal. |
| `system_generated_learning` | HK Alpha Team / Simulation Investment Desk system process | Generate disciplined paper-trading simulations from approved recommendation packets to validate recommendation quality and produce reviewable learning proposals. | May create reviewable learning proposals, but must not silently mutate production strategy logic. |

## `user_recorded` Responsibilities

`user_recorded` records must preserve the human user's paper-trading decision context.

Required context includes:

- `simulation_origin = user_recorded` or equivalent `paper_order_origin = user_recorded` source semantics.
- `created_by_type` showing the record came from a human/user source.
- User-entered notes and rationale.
- Linked `source_recommendation_id` / `strategy_recommendation_id` when the user associates the paper trade with a recommendation.
- Trade review fields, including outcome review, what worked, what failed, and improvement suggestions when reviewed.

`user_recorded` records must not claim that HK Alpha Team generated a learning simulation unless a separate auditable link to a reviewable learning proposal exists.

## `system_generated_learning` Responsibilities

`system_generated_learning` records must preserve the original recommendation packet and the assumptions used for validation.

Required context includes:

- `simulation_origin = system_generated_learning` source semantics.
- `created_by_type` showing the record came from the Simulation Investment Desk/system process.
- Original recommendation linkage through `source_recommendation_id` / `strategy_recommendation_id`.
- Original recommendation label, original scores, and original thesis.
- Simulated entry and exit assumptions.
- Realized/unrealized PnL when available.
- Holding period and outcome review.
- What worked, what failed, and improvement suggestions.
- `requires_human_review = true` for any generated learning proposal.
- Learning proposal linkage when a proposal is generated.

`system_generated_learning` records may generate reviewable proposals, but those proposals must not be auto-applied or silently change production strategy behavior.

## Mandatory Recorded Fields

The simulation system records, as applicable to the origin pipeline:

- Simulation origin (`user_recorded` or `system_generated_learning`)
- Created-by/source type
- Original recommendation linkage when applicable
- Original recommendation
- Original scores
- Original thesis
- Simulated entry price or entry assumption
- Simulated exit price or exit assumption
- Realized and unrealized PnL
- Holding period
- Outcome review
- What worked
- What failed
- Improvement suggestions
- User-recorded notes and rationale for `user_recorded` records
- System learning reason and reviewable proposal linkage for `system_generated_learning` records

## Operating Rules

1. Historical recommendations must not be overwritten to make results look better.
2. Losing paper trades and losing system-generated simulations must remain visible in reports.
3. Simulation results do not guarantee real-world performance.
4. The simulation system must not execute real-money trades.
5. Strategy learning should produce reviewable proposals, not silently change production logic.
6. User-recorded and system-generated learning origins must remain distinguishable and auditable.

## Output Artifacts

- Paper trade blotter
- Outcome and performance summaries
- Post-simulation review notes
- Proposed strategy/process improvements for human review
- Origin-aware audit trail distinguishing `user_recorded` from `system_generated_learning`

## Boundary Reminder

Simulation outputs are advisory and educational. Final real-money decisions remain with the user / Harness Engineering.
