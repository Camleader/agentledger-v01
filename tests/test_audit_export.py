import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agentledger.decision_agent import run_heloc_agent
from agentledger.exporter import build_audit_record, export_audit_json
from agentledger.risk_flags import (
    evaluate_risk_flags,
    highest_risk_severity,
    requires_human_review,
)


def test_highest_risk_severity():
    assert highest_risk_severity([]) == "low"
    assert highest_risk_severity([{"severity": "medium"}]) == "medium"
    assert highest_risk_severity([{"severity": "low"}, {"severity": "high"}]) == "high"


def test_requires_human_review_logic():
    approve_result = {"recommendation": "Approve"}
    manual_review_result = {"recommendation": "Manual Review"}
    decline_result = {"recommendation": "Decline"}

    assert requires_human_review(approve_result, []) is False
    assert requires_human_review(manual_review_result, []) is True
    assert requires_human_review(decline_result, []) is True
    assert requires_human_review(approve_result, [{"severity": "high"}]) is True


def test_export_audit_json_is_valid_json():
    application = {
        "borrower_name": "Alex Approved",
        "credit_score": 720,
        "annual_income": 120000,
        "existing_monthly_debt": 2500,
        "home_value": 600000,
        "mortgage_balance": 350000,
        "requested_heloc_amount": 75000,
        "employment_type": "W2",
        "income_documentation_status": "Verified",
    }
    agent_result = run_heloc_agent(application)
    risk_flags = evaluate_risk_flags(application, agent_result)
    audit_record = build_audit_record(
        run_id="demo-run-123",
        created_at="2026-06-03T00:00:00+00:00",
        selected_demo="Approve Demo",
        application_data=application,
        agent_result=agent_result,
        risk_flags=risk_flags,
        highest_risk_severity=highest_risk_severity(risk_flags),
        requires_human_review=requires_human_review(agent_result, risk_flags),
        human_review_status="Pending Human Review",
        reviewed_at=None,
        trace_events=[],
    )

    parsed = json.loads(export_audit_json(audit_record))

    assert parsed["export_type"] == "AgentLedger Audit Record"
    assert parsed["product_version"] == "v0.3.0"    
    assert parsed["product"]["version"] == "v0.3.0"
    assert parsed["run"]["run_id"] == "demo-run-123"
    assert parsed["decision"]["recommendation"] == "Approve"
    assert parsed["trace"]["event_count"] == 0
