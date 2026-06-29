import pytest

from agentledger import AgentLedger


def test_log_decision_stores_risk_and_review_fields(tmp_path):
    log_path = tmp_path / "events.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    event = ledger.log_decision(
        agent_name="UnderwritingAgent",
        input_data={"credit_score": 665},
        output_data={"decision": "manual_review"},
        reason_codes=["INCOME_DOCUMENTATION_INCOMPLETE"],
        risk_level="high",
        review_required=True,
        review_reason="Income documentation is incomplete.",
        policy_status="warning",
        approval_status="pending",
    )

    assert event["risk_level"] == "high"
    assert event["review_required"] is True
    assert event["review_reason"] == "Income documentation is incomplete."
    assert event["policy_status"] == "warning"
    assert event["approval_status"] == "pending"


def test_log_decision_uses_safe_review_defaults(tmp_path):
    log_path = tmp_path / "events.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    event = ledger.log_decision(
        agent_name="UnderwritingAgent",
        output_data={"decision": "approve"},
    )

    assert event["risk_level"] == "low"
    assert event["review_required"] is False
    assert event["review_reason"] is None
    assert event["policy_status"] == "not_evaluated"
    assert event["approval_status"] == "not_required"


def test_log_decision_rejects_invalid_risk_level(tmp_path):
    log_path = tmp_path / "events.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    with pytest.raises(ValueError, match="risk_level must be one of"):
        ledger.log_decision(
            agent_name="UnderwritingAgent",
            output_data={"decision": "approve"},
            risk_level="unknown",
        )
    