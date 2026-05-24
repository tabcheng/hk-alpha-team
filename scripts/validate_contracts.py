#!/usr/bin/env python3
"""Lightweight contract validation baseline for HK Alpha Team."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
API_DOC = ROOT / "docs/09-api-and-agent-contracts.md"
SCHEMA_DOC = ROOT / "docs/08-supabase-schema-design.md"
MIGRATION_SQL = ROOT / "supabase/migrations/0001_create_core_schema.sql"

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

SENSITIVE_PATTERNS = [
    "SUPABASE_SERVICE_ROLE_KEY=",
    "RAILWAY_TOKEN=",
    "BROKER_API_KEY=",
    "REAL_MONEY_ACCOUNT=",
    "PRODUCTION_BROKER_CREDENTIALS=",
]

SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    "node_modules",
    ".venv",
    "venv",
    "env",
}

ALLOWED_PATTERN_PATHS = {
    Path("scripts/validate_contracts.py"),
    Path("AGENTS.md"),
    Path("docs/15-migration-assumptions.md"),
}


MIGRATION_REQUIRED_SNIPPETS = [
    "investment_committee_review_id uuid references investment_committee_reviews(id)",
    "idx_strategy_recommendations_committee_review_created_at",
]

BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".gz", ".tar", ".sqlite", ".db", ".ico"
}


def must_contain(text: str, label: str, expected_values: list[str]) -> list[str]:
    missing = [item for item in expected_values if item not in text]
    return [f"[{label}] missing: {item}" for item in missing]


def is_binary(path: Path) -> bool:
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return True
    try:
        data = path.read_bytes()
    except OSError:
        return False
    return b"\x00" in data


def scan_sensitive_assignments() -> list[str]:
    issues: list[str] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if any(part in SKIP_DIRS for part in rel.parts):
            continue
        if rel in ALLOWED_PATTERN_PATHS:
            continue
        if is_binary(path):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern in SENSITIVE_PATTERNS:
            if pattern in text:
                issues.append(f"[Sensitive assignment] {rel}: contains '{pattern}'")
    return issues


def main() -> int:
    errors: list[str] = []

    readme_text = README.read_text(encoding="utf-8")
    api_text = API_DOC.read_text(encoding="utf-8")
    schema_text = SCHEMA_DOC.read_text(encoding="utf-8")
    migration_text = MIGRATION_SQL.read_text(encoding="utf-8")

    errors += must_contain(readme_text, "README strategy labels", EXPECTED_STRATEGY_LABELS)
    errors += must_contain(readme_text, "README table names", EXPECTED_TABLES)
    errors += must_contain(readme_text, "README endpoint names", EXPECTED_ENDPOINTS)
    errors += must_contain(readme_text, "README envelope keys", EXPECTED_ENVELOPE_KEYS)

    errors += must_contain(schema_text, "Schema doc table names", EXPECTED_TABLES)
    errors += must_contain(api_text, "API doc endpoint names", EXPECTED_ENDPOINTS)
    errors += must_contain(api_text, "API doc envelope keys", EXPECTED_ENVELOPE_KEYS)
    errors += must_contain(migration_text, "Migration SQL table names", EXPECTED_TABLES)
    errors += must_contain(migration_text, "Migration SQL lineage snippets", MIGRATION_REQUIRED_SNIPPETS)

    errors += scan_sensitive_assignments()

    if errors:
        print("Contract validation failed:\n")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Contract validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
