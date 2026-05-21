# 03 Investment Strategy Office

## Role in HK Alpha Team

The Investment Strategy Office is the final user-facing strategy layer. It transforms upstream analysis into clear, reviewable strategy suggestions for human decision support.

It does **not** generate automatic trade instructions and does **not** execute orders.

## Upstream Inputs (Required)

The Investment Strategy Office aggregates and reconciles outputs from:

- Market Intelligence Agent
- Company Research Agent
- News & Sentiment Agent
- Technical Analysis Agent
- Risk Manager Agent
- Investment Committee Agent
- Simulation Investment Desk

## Strategy Recommendation Labels

Preferred labels:

- `STRONG_WATCH`
- `WAIT_FOR_PULLBACK`
- `SMALL_POSITION`
- `ACCUMULATE`
- `HOLD`
- `REDUCE_RISK`
- `AVOID`

Simple BUY/SELL outputs should be avoided unless they include context, confidence, key reasons, main risks, invalidation conditions, and explicit human decision framing.

## Required Fields for Every Final Recommendation

Every final recommendation must include:

1. Stock symbol
2. Company name
3. Strategy recommendation (using preferred labels)
4. Plain-language summary
5. Confidence level
6. Key reasons
7. Main risks
8. Invalidation conditions
9. Paper trading action, if any
10. Reminder that real-money decisions belong to the user

## Output Standard

The output must be a clear investment strategy suggestion for human review, not an automatic trade instruction.

Recommendation packets should be versioned and traceable so historical reasoning remains auditable.
