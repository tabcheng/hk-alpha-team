# 02 Agent Departments

This document defines the agreed HK Alpha Team department model. These names are fixed for downstream API contracts, database schema design, prompt templates, and Codex tasks.

## 1) Market Intelligence Agent

**Purpose**
- Track macro, policy, sector, and market-structure context relevant to Hong Kong equities.

**Main Responsibilities**
- Summarize market regime signals and key external drivers.
- Maintain context snapshots for decision cycles.
- Flag regime shifts that may affect portfolio risk.

**Expected Output**
- Structured market context brief with key signals, risks, and watch items.

**Decision Boundary**
- Provides context and alerts only; does not issue final investment instructions.

## 2) Company Research Agent

**Purpose**
- Produce company-level fundamental research for candidate securities.

**Main Responsibilities**
- Compile business model, financial profile, valuation, and thesis assumptions.
- Identify thesis catalysts and invalidation triggers.
- Track assumption changes over time.

**Expected Output**
- Structured company research memo with thesis quality indicators.

**Decision Boundary**
- Recommends research conclusions only; no autonomous trade decisions.

## 3) News & Sentiment Agent

**Purpose**
- Monitor relevant news flow and sentiment shifts impacting securities or sectors.

**Main Responsibilities**
- Capture material headlines/events.
- Classify sentiment direction and confidence.
- Highlight potential thesis-impacting updates.

**Expected Output**
- Time-stamped news/sentiment digest with impact notes.

**Decision Boundary**
- Signals information changes only; does not place or direct trades.

## 4) Technical Analysis Agent

**Purpose**
- Provide technical context on price action, momentum, trend, and support/resistance levels.

**Main Responsibilities**
- Generate technical setup summaries and trend diagnostics.
- Identify entry/exit condition candidates for discussion.
- Track technical invalidation levels.

**Expected Output**
- Technical analysis brief with chart-logic explanations in plain language.

**Decision Boundary**
- Advises on technical conditions only; cannot trigger execution.

## 5) Risk Manager Agent

**Purpose**
- Assess risk exposure and downside characteristics across strategies and portfolios.

**Main Responsibilities**
- Evaluate concentration, drawdown, and scenario risks.
- Propose risk guardrails and sizing constraints.
- Track risk changes after market events.

**Expected Output**
- Risk assessment report with risk flags and mitigation suggestions.

**Decision Boundary**
- Can recommend risk reductions but cannot execute position changes.

## 6) Investment Committee Agent

**Purpose**
- Perform multi-input synthesis and challenge assumptions before recommendations reach users.

**Main Responsibilities**
- Compare and reconcile cross-agent signals.
- Score thesis quality and confidence consistency.
- Document dissenting views and unresolved questions.

**Expected Output**
- Committee review note with recommendation posture and open issues.

**Decision Boundary**
- Produces review judgment only; final human decision remains external.

## 7) Simulation Investment Desk

**Purpose**
- Execute paper trading workflows to validate strategy behavior and learning quality.

**Main Responsibilities**
- Run simulation entries/exits from approved recommendation packets.
- Record outcomes and post-trade review metadata.
- Feed reviewable learning proposals into governance docs.

**Expected Output**
- Simulation records, performance summaries, and lessons proposals.

**Decision Boundary**
- Paper-trading only; never executes real-money trades.

## 8) Investment Strategy Office

**Purpose**
- Produce clear user-facing strategy recommendations from all upstream agents and simulation context.

**Main Responsibilities**
- Aggregate cross-department outputs into decision-ready packets.
- Standardize labels, rationale, confidence, and risk disclosures.
- Maintain recommendation history and version clarity.

**Expected Output**
- Final strategy suggestion packet for human review.

**Decision Boundary**
- Advisory layer only; does not issue automatic trade instructions.
