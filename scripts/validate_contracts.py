#!/usr/bin/env python3
"""Lightweight contract validation baseline for HK Alpha Team.

Validates that the canonical documentation keeps the locked contract surfaces:
- schema table names
- MVP API endpoint names
- response envelope keys
- strategy labels
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
API_DOC = ROOT / "docs/09-api-and-agent-contracts.md"
SCHEMA_DOC = ROOT / "docs/08-supabase-schema-design.md"

EXPECTED_TABLES = [
    "stocks",
    "market_indices",
    "price_bars",
    "market_snapshots",
    "company_financials",
    "news_items",
    "research_documents",
    "agent_runs",
    "agent_outputs",
    "investment_committee_reviews",
    "strategy_recommendations",
    "paper_portfolios",
    "paper_orders",
    "paper_positions",
    "portfolio_snapshots",
    "trade_reviews",
    "learning_proposals",
    "audit_events",
]

EXPECTED_ENDPOINTS = [
    "GET /health",
    "POST /api/v1/analyze-stock",
    "GET /api/v1/stocks/{symbol}",
    "GET /api/v1/strategy-recommendations/{recommendation_id}",
    "POST /api/v1/strategy-recommendations",
    "POST /api/v1/simulation/paper-orders",
    "GET /api/v1/paper-portfolios/{portfolio_id}",
    "GET /api/v1/agent-runs/{agent_run_id}",
    "GET /api/v1/project-status",
]

EXPECTED_ENVELOPE_KEYS = [
    '"request_id"',
    '"status"',
    '"data"',
    '"metadata"',
    '"schema_version"',
    '"generated_at"',
    '"source"',
    '"warnings"',
]

EXPECTED_STRATEGY_LABELS = [
    "STRONG_WATCH",
    "WAIT_FOR_PULLBACK",
    "SMALL_POSITION",
    "ACCUMULATE",
    "HOLD",
    "REDUCE_RISK",
    "AVOID",
]


def must_contain(text: str, label: str, expected_values: list[str]) -> list[str]:
    missing = [item for item in expected_values if item not in text]
    if missing:
        return [f"[{label}] missing: {item}" for item in missing]
    return []


def main() -> int:
    errors: list[str] = []

    readme_text = README.read_text(encoding="utf-8")
    api_text = API_DOC.read_text(encoding="utf-8")
    schema_text = SCHEMA_DOC.read_text(encoding="utf-8")

    errors += must_contain(readme_text, "README strategy labels", EXPECTED_STRATEGY_LABELS)
    errors += must_contain(readme_text, "README table names", EXPECTED_TABLES)
    errors += must_contain(readme_text, "README endpoint names", EXPECTED_ENDPOINTS)
    errors += must_contain(readme_text, "README envelope keys", EXPECTED_ENVELOPE_KEYS)

    errors += must_contain(schema_text, "Schema doc table names", EXPECTED_TABLES)

    errors += must_contain(api_text, "API doc endpoint names", EXPECTED_ENDPOINTS)
    errors += must_contain(api_text, "API doc envelope keys", EXPECTED_ENVELOPE_KEYS)

    if errors:
        print("Contract validation failed:\n")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Contract validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
