from datetime import datetime

from app.department_adapters import (
    AGENT_VERSION,
    COMMON_AGENT_OUTPUT_FIELDS,
    DEPARTMENT_NAMES,
    build_department_outputs,
)


def _stable_outputs(outputs: list[dict]) -> list[dict]:
    return [{key: value for key, value in output.items() if key != "generated_at"} for output in outputs]


def test_all_eight_department_outputs_are_produced_with_locked_shape() -> None:
    outputs = build_department_outputs("0700.HK")

    assert len(outputs) == 8
    assert [output["agent_name"] for output in outputs] == DEPARTMENT_NAMES
    for output in outputs:
        assert set(output) == COMMON_AGENT_OUTPUT_FIELDS


def test_department_outputs_use_common_version_and_normalized_symbol() -> None:
    outputs = build_department_outputs(" 0700.hk ")

    for output in outputs:
        assert output["agent_version"] == AGENT_VERSION
        assert output["stock_symbol"] == "0700.HK"
        assert output["schema_version"] == "v0.1"
        datetime.fromisoformat(output["generated_at"])


def test_evidence_is_local_placeholder_and_does_not_claim_live_data() -> None:
    outputs = build_department_outputs("0005.HK")
    forbidden_claims = [
        "fetched live",
        "live market data was fetched",
        "filings were fetched",
        "news feeds were fetched",
        "broker commentary was fetched",
        "ohlcv bars were fetched",
        "simulation records were fetched",
        "paper orders were created",
        "real-money order",
    ]

    for output in outputs:
        evidence_text = " ".join(output["evidence"]).lower()
        assert output["evidence"]
        assert "local placeholder only" in evidence_text
        assert "no " in evidence_text
        assert not any(claim in evidence_text for claim in forbidden_claims)


def test_scores_confidence_and_review_lists_are_bounded_and_non_empty() -> None:
    outputs = build_department_outputs("0700.HK")

    for output in outputs:
        assert isinstance(output["score"], int)
        assert 0 <= output["score"] <= 100
        assert isinstance(output["confidence"], int)
        assert 0 <= output["confidence"] <= 100
        assert output["confidence"] <= 25
        assert output["key_findings"]
        assert output["risks"]
        assert output["invalidation_conditions"]


def test_department_outputs_are_deterministic_across_stable_fields() -> None:
    first = build_department_outputs("0700.HK")
    second = build_department_outputs(" 0700.hk ")

    assert _stable_outputs(first) == _stable_outputs(second)
