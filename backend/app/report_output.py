from __future__ import annotations

from typing import Any

from app.simulation_origin_contract import (
    ALLOWED_SIMULATION_ORIGINS,
    build_sample_simulation_origin_payloads,
    validate_simulation_origin_payload,
)

REPORT_OUTPUT_METADATA: dict[str, bool | str] = {
    "report_runtime": "deterministic_local_non_production",
    "production_supabase_connected": False,
    "broker_api_called": False,
    "real_money_order_placed": False,
    "vendor_api_called": False,
    "live_market_data_called": False,
    "secrets_required": False,
}

REPORT_OUTPUT_WARNINGS: list[str] = [
    "Report output is research, simulation, and decision-support only; it is advisory-only and paper-only.",
    "Human decision required: HK Alpha Team does not place, route, or authorize real-money orders.",
    "No broker API is connected or called; no real-money trading or autonomous execution is available.",
    "No production Supabase connection, production persistence, or Supabase client runtime is used by this report.",
    "No live market data, vendor API, external API, or paid data provider is called; report data is deterministic local/test data.",
    "No secrets, hosted credentials, broker credentials, or real-money account information are required or used.",
]


def _build_simulation_evidence_summary() -> list[dict[str, Any]]:
    sample_payloads = build_sample_simulation_origin_payloads()
    summaries: list[dict[str, Any]] = []
    for origin in ALLOWED_SIMULATION_ORIGINS:
        payload = sample_payloads[origin]
        validation = validate_simulation_origin_payload(payload)
        summaries.append(
            {
                "simulation_origin": origin,
                "validation_status": validation["validation_status"],
                "source_endpoint_reference": validation["endpoint_reference"],
                "symbol": payload["symbol"],
                "portfolio_id": payload["portfolio_id"],
                "advisory_only": validation["advisory_only"],
                "human_in_the_loop": validation["human_in_the_loop"],
                "learning_proposals_reviewable": validation["learning_proposal_behavior"][
                    "proposals_reviewable"
                ],
                "learning_proposals_auto_applied": validation["learning_proposal_behavior"][
                    "proposals_auto_applied"
                ],
                "losing_outcomes_remain_visible": validation["loss_visibility_behavior"][
                    "losing_outcomes_remain_visible"
                ],
                "historical_recommendations_overwritten": validation["loss_visibility_behavior"][
                    "historical_recommendations_overwritten"
                ],
                "real_money_order_placed": validation["boundary_flags"]["real_money_order_placed"],
                "broker_api_called": validation["boundary_flags"]["broker_api_called"],
                "production_supabase_connected": validation["boundary_flags"]["production_supabase_connected"],
                "secrets_required": validation["boundary_flags"]["secrets_required"],
            }
        )
    return summaries


def build_simulation_summary_report() -> dict[str, Any]:
    """Build the minimal deterministic Phase 6 report-output surface."""

    simulation_evidence_summary = _build_simulation_evidence_summary()

    return {
        "report_id": "phase6-simulation-summary-001",
        "report_type": "simulation_summary",
        "title": "Phase 6 Minimal Simulation Summary Report",
        "summary": (
            "Deterministic local report output for the non-production Simulation Desk. "
            "The report summarizes paper-only learning evidence and presents advisory decision support "
            "for Harness Engineering review; it is not market data, not a live recommendation feed, "
            "and not an execution instruction."
        ),
        "simulation_evidence_summary": simulation_evidence_summary,
        "sections": [
            {
                "section_id": "scope",
                "heading": "Scope and source",
                "body": (
                    "Generated from local deterministic HK Alpha Team backend fixtures and Simulation Desk "
                    "boundary rules. No database persistence, production Supabase, vendor feed, live market data, "
                    "broker, or secret is required."
                ),
            },
            {
                "section_id": "simulation_learning",
                "heading": "Simulation learning posture",
                "body": (
                    "Current evidence supports continued paper-only observation. Losing paper trades and weak "
                    "signals must remain visible in future reports so review proposals can improve the process "
                    "without rewriting historical simulation outcomes."
                ),
            },
            {
                "section_id": "decision_framing",
                "heading": "Human decision framing",
                "body": (
                    "Harness Engineering remains responsible for any real-world decision. This output can help "
                    "prioritize review questions, but HK Alpha Team does not create hidden or irreversible actions."
                ),
            },
        ],
        "recommendations": [
            {
                "label": "HOLD",
                "confidence": "low_to_moderate_deterministic_fixture_only",
                "reasoning": [
                    "The Simulation Desk MVP is available for non-production paper-only learning evidence.",
                    "Phase 6 should first validate that reports present recommendations with risks, invalidation conditions, and warnings before adding any broader surface.",
                    "No live market data or vendor feed is present, so confidence must remain constrained.",
                ],
                "human_decision_required": True,
                "execution_instruction": "No execution instruction is provided; review only.",
            }
        ],
        "risks": [
            "Deterministic local fixtures are not live market evidence and may not reflect current Hong Kong equity conditions.",
            "Paper-only simulation outcomes do not guarantee future real-world performance.",
            "Without production persistence, this report should not be treated as an auditable production record.",
            "Without vendor/API data, price, liquidity, news, and event risks are intentionally unknown.",
        ],
        "invalidation_conditions": [
            "Treat the report as stale if used as live market evidence or as a real-money instruction.",
            "Reassess if production Supabase, vendor data, broker connectivity, auth, deployment, or secrets are introduced in a future approved scope.",
            "Reassess if simulation evidence shows repeated losses, missing risk fields, or recommendations without human review framing.",
        ],
        "human_decision_required": True,
        "advisory_only": True,
        "paper_only": True,
        "generated_from": {
            "source": "deterministic_local_backend_report_output",
            "source_modules": [
                "backend.app.report_output",
                "backend.app.simulation_origin_contract",
            ],
            "phase": "Phase 6 — Simple User Interface or Report Output",
            "simulation_origin_scope": list(ALLOWED_SIMULATION_ORIGINS),
            "production_supabase_connected": False,
            "broker_api_called": False,
            "real_money_order_placed": False,
            "vendor_api_called": False,
            "live_market_data_called": False,
            "secrets_required": False,
        },
        "next_actions": [
            "Review this report shape for clarity before adding any larger UI surface.",
            "Keep future Phase 6 output advisory-only, paper-only, and human-in-the-loop.",
            "Use backend tests and CI evidence before expanding report sources or presentation layers.",
        ],
    }
