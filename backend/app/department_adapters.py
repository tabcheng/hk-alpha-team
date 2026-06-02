from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from app.contracts import SCHEMA_VERSION, utc_timestamp

AGENT_VERSION = "v0.1"

MARKET_INTELLIGENCE_AGENT = "Market Intelligence Agent"
COMPANY_RESEARCH_AGENT = "Company Research Agent"
NEWS_SENTIMENT_AGENT = "News & Sentiment Agent"
TECHNICAL_ANALYSIS_AGENT = "Technical Analysis Agent"
RISK_MANAGER_AGENT = "Risk Manager Agent"
INVESTMENT_COMMITTEE_AGENT = "Investment Committee Agent"
SIMULATION_INVESTMENT_DESK = "Simulation Investment Desk"
INVESTMENT_STRATEGY_OFFICE = "Investment Strategy Office"

DEPARTMENT_NAMES = [
    MARKET_INTELLIGENCE_AGENT,
    COMPANY_RESEARCH_AGENT,
    NEWS_SENTIMENT_AGENT,
    TECHNICAL_ANALYSIS_AGENT,
    RISK_MANAGER_AGENT,
    INVESTMENT_COMMITTEE_AGENT,
    SIMULATION_INVESTMENT_DESK,
    INVESTMENT_STRATEGY_OFFICE,
]

COMMON_AGENT_OUTPUT_FIELDS = {
    "agent_name",
    "agent_version",
    "stock_symbol",
    "input_summary",
    "evidence",
    "score",
    "confidence",
    "key_findings",
    "risks",
    "invalidation_conditions",
    "generated_at",
    "schema_version",
}

_SCORE_OFFSETS = {
    MARKET_INTELLIGENCE_AGENT: (45, 11, 1),
    COMPANY_RESEARCH_AGENT: (48, 10, 3),
    NEWS_SENTIMENT_AGENT: (46, 10, 7),
    TECHNICAL_ANALYSIS_AGENT: (44, 12, 5),
    RISK_MANAGER_AGENT: (40, 15, 11),
    INVESTMENT_COMMITTEE_AGENT: (43, 12, 13),
    SIMULATION_INVESTMENT_DESK: (41, 10, 17),
    INVESTMENT_STRATEGY_OFFICE: (44, 11, 19),
}

_CONFIDENCE = {
    MARKET_INTELLIGENCE_AGENT: 20,
    COMPANY_RESEARCH_AGENT: 20,
    NEWS_SENTIMENT_AGENT: 20,
    TECHNICAL_ANALYSIS_AGENT: 20,
    RISK_MANAGER_AGENT: 25,
    INVESTMENT_COMMITTEE_AGENT: 20,
    SIMULATION_INVESTMENT_DESK: 15,
    INVESTMENT_STRATEGY_OFFICE: 20,
}

_INPUT_SUMMARIES = {
    MARKET_INTELLIGENCE_AGENT: "Local deterministic market-context adapter preview for a Hong Kong equity symbol.",
    COMPANY_RESEARCH_AGENT: "Local deterministic company-research adapter preview for a Hong Kong equity symbol.",
    NEWS_SENTIMENT_AGENT: "Local deterministic news-and-sentiment adapter preview for a Hong Kong equity symbol.",
    TECHNICAL_ANALYSIS_AGENT: "Local deterministic technical-analysis adapter preview for a Hong Kong equity symbol.",
    RISK_MANAGER_AGENT: "Local deterministic risk-manager adapter preview for a Hong Kong equity symbol.",
    INVESTMENT_COMMITTEE_AGENT: "Local deterministic investment-committee synthesis adapter preview for a Hong Kong equity symbol.",
    SIMULATION_INVESTMENT_DESK: "Local deterministic simulation-desk adapter preview with no paper order creation.",
    INVESTMENT_STRATEGY_OFFICE: "Local deterministic strategy-office adapter preview for human decision support.",
}

_EVIDENCE = {
    MARKET_INTELLIGENCE_AGENT: [
        "Local placeholder only: normalized symbol and static HKEX/HKD context; no live index, macro, liquidity, filing, news, OHLCV, portfolio, simulation, or broker data was fetched."
    ],
    COMPANY_RESEARCH_AGENT: [
        "Local placeholder only: normalized symbol and static HKEX/HKD context; no financial statements, filings, research documents, or broker commentary were fetched."
    ],
    NEWS_SENTIMENT_AGENT: [
        "Local placeholder only: normalized symbol and static HKEX/HKD context; no news feeds, social feeds, headlines, filings, or broker commentary were fetched."
    ],
    TECHNICAL_ANALYSIS_AGENT: [
        "Local placeholder only: normalized symbol and static HKEX/HKD context; no prices, OHLCV bars, volume, indicators, or broker data were fetched."
    ],
    RISK_MANAGER_AGENT: [
        "Local placeholder only: normalized symbol and static HKEX/HKD context; no portfolio holdings, exposure records, volatility feeds, or production database data were fetched."
    ],
    INVESTMENT_COMMITTEE_AGENT: [
        "Local placeholder only: deterministic adapter previews; no persisted agent_runs, agent_outputs, research memos, filings, or live research records were fetched."
    ],
    SIMULATION_INVESTMENT_DESK: [
        "Local placeholder only: normalized symbol and static HKEX/HKD context; no simulation records, paper orders, portfolio snapshots, or trade reviews were fetched or created."
    ],
    INVESTMENT_STRATEGY_OFFICE: [
        "Local placeholder only: deterministic department adapter previews; no strategy recommendation record, production Supabase data, or broker execution data was fetched or created."
    ],
}

_KEY_FINDINGS = {
    MARKET_INTELLIGENCE_AGENT: "Market-context score is deterministic scaffolding and is not live market research.",
    COMPANY_RESEARCH_AGENT: "Company-research score is deterministic scaffolding and is not financial-statement analysis.",
    NEWS_SENTIMENT_AGENT: "News-and-sentiment score is deterministic scaffolding and is not headline or feed analysis.",
    TECHNICAL_ANALYSIS_AGENT: "Technical score is deterministic scaffolding and is not OHLCV-derived analysis.",
    RISK_MANAGER_AGENT: "Risk score is deterministic scaffolding and is not portfolio or live volatility analysis.",
    INVESTMENT_COMMITTEE_AGENT: "Committee synthesis is deterministic scaffolding and is not a persisted committee review.",
    SIMULATION_INVESTMENT_DESK: "Simulation score is deterministic scaffolding and does not create or inspect paper orders.",
    INVESTMENT_STRATEGY_OFFICE: "Strategy-office output is deterministic scaffolding for human review and is not a persisted recommendation.",
}

_RISKS = {
    MARKET_INTELLIGENCE_AGENT: "Do not interpret the placeholder market-context score as live macro, liquidity, or index analysis.",
    COMPANY_RESEARCH_AGENT: "Do not interpret the placeholder company score as valuation, filings, or earnings research.",
    NEWS_SENTIMENT_AGENT: "Do not interpret the placeholder sentiment score as live news, social, or broker-commentary analysis.",
    TECHNICAL_ANALYSIS_AGENT: "Do not interpret the placeholder technical score as chart, price, volume, or indicator analysis.",
    RISK_MANAGER_AGENT: "Do not interpret the placeholder risk score as portfolio sizing, exposure, or volatility guidance.",
    INVESTMENT_COMMITTEE_AGENT: "Do not interpret the placeholder committee score as a reviewed investment committee decision.",
    SIMULATION_INVESTMENT_DESK: "Do not interpret the placeholder simulation score as paper-trading performance or order guidance.",
    INVESTMENT_STRATEGY_OFFICE: "Do not interpret the placeholder strategy score as live investment research or real-money direction.",
}

_INVALIDATION = {
    MARKET_INTELLIGENCE_AGENT: "Invalidate if market data, macro data, liquidity data, or network services are claimed or introduced without reviewed authorization.",
    COMPANY_RESEARCH_AGENT: "Invalidate if filings, financial statements, research documents, or broker commentary are claimed or introduced without reviewed authorization.",
    NEWS_SENTIMENT_AGENT: "Invalidate if news feeds, social sentiment, headlines, or broker commentary are claimed or introduced without reviewed authorization.",
    TECHNICAL_ANALYSIS_AGENT: "Invalidate if prices, OHLCV bars, volume, or indicators are claimed or introduced without reviewed authorization.",
    RISK_MANAGER_AGENT: "Invalidate if portfolio holdings, exposure records, live volatility, persistence, or production Supabase are claimed or introduced without reviewed authorization.",
    INVESTMENT_COMMITTEE_AGENT: "Invalidate if persisted agent runs, agent outputs, committee review records, or production database writes occur.",
    SIMULATION_INVESTMENT_DESK: "Invalidate if simulation records are fetched, paper orders are created, or paper-trading behavior is implied.",
    INVESTMENT_STRATEGY_OFFICE: "Invalidate if a strategy recommendation is persisted, a broker API is called, or any real-money order is placed.",
}

SCORE_BUCKET_BY_DEPARTMENT = {
    MARKET_INTELLIGENCE_AGENT: "market",
    COMPANY_RESEARCH_AGENT: "fundamental",
    TECHNICAL_ANALYSIS_AGENT: "technical",
    NEWS_SENTIMENT_AGENT: "sentiment",
    RISK_MANAGER_AGENT: "risk",
    SIMULATION_INVESTMENT_DESK: "simulation",
}


@dataclass(frozen=True)
class DepartmentOutput:
    agent_name: str
    agent_version: str
    stock_symbol: str
    input_summary: str
    evidence: list[str]
    score: int
    confidence: int
    key_findings: list[str]
    risks: list[str]
    invalidation_conditions: list[str]
    generated_at: str
    schema_version: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _symbol_seed(symbol: str) -> int:
    return sum((idx + 1) * ord(char) for idx, char in enumerate(symbol))


def _deterministic_score(symbol: str, agent_name: str) -> int:
    floor, span, divisor = _SCORE_OFFSETS[agent_name]
    return floor + ((_symbol_seed(symbol) // divisor) % span)


def build_department_output(symbol: str, agent_name: str) -> DepartmentOutput:
    if agent_name not in DEPARTMENT_NAMES:
        raise ValueError(f"Unknown department adapter: {agent_name}")

    normalized_symbol = symbol.strip().upper()
    return DepartmentOutput(
        agent_name=agent_name,
        agent_version=AGENT_VERSION,
        stock_symbol=normalized_symbol,
        input_summary=_INPUT_SUMMARIES[agent_name],
        evidence=list(_EVIDENCE[agent_name]),
        score=_deterministic_score(normalized_symbol, agent_name),
        confidence=_CONFIDENCE[agent_name],
        key_findings=[_KEY_FINDINGS[agent_name]],
        risks=[_RISKS[agent_name]],
        invalidation_conditions=[_INVALIDATION[agent_name]],
        generated_at=utc_timestamp(),
        schema_version=SCHEMA_VERSION,
    )


def build_department_outputs(symbol: str) -> list[dict[str, Any]]:
    """Build local-only deterministic department adapter outputs.

    Stable fields are deterministic for the same normalized symbol. The only intentionally
    variable field is ``generated_at``.
    """

    return [build_department_output(symbol, agent_name).to_dict() for agent_name in DEPARTMENT_NAMES]


def build_score_buckets(department_outputs: list[dict[str, Any]]) -> dict[str, int]:
    return {
        SCORE_BUCKET_BY_DEPARTMENT[output["agent_name"]]: int(output["score"])
        for output in department_outputs
        if output["agent_name"] in SCORE_BUCKET_BY_DEPARTMENT
    }


def build_score_confidence(department_outputs: list[dict[str, Any]]) -> dict[str, int]:
    return {
        SCORE_BUCKET_BY_DEPARTMENT[output["agent_name"]]: int(output["confidence"])
        for output in department_outputs
        if output["agent_name"] in SCORE_BUCKET_BY_DEPARTMENT
    }
