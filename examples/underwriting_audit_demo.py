# The script will be able to be useed into one complete AI-audit workflow:
# create_trace
# → log_tool_call
# → log_tool_call
# → log_decision
# → complete_trace
# → export_trace

import json
from pathlib import Path

from agentledger import AgentLedger


def run_underwriting_audit_demo(event_log_path, trace_log_path):
    ledger = AgentLedger(
        storage_path=str(event_log_path),
        trace_storage_path=str(trace_log_path),
    )

    trace = ledger.create_trace(
        workflow="heloc_underwriting",
        agent_name="UnderwritingAgent",
        entity_id="application_123",
        metadata={
            "environment": "demo",
            "product": "AgentLedger",
        },
    )

    ledger.log_tool_call(
        agent_name="UnderwritingAgent",
        tool_name="income_verification_api",
        input_data={
            "application_id": "application_123",
            "document_type": "paystub",
        },
        output_data={
            "status": "partial",
            "income_verified": False,
        },
        trace_id=trace["trace_id"],
    )

    ledger.log_tool_call(
        agent_name="UnderwritingAgent",
        tool_name="credit_report_api",
        input_data={
            "application_id": "application_123",
        },
        output_data={
            "credit_score": 665,
            "status": "completed",
        },
        trace_id=trace["trace_id"],
    )

    ledger.log_decision(
        agent_name="UnderwritingAgent",
        input_data={
            "credit_score": 665,
            "income_documentation_status": "partial",
        },
        output_data={
            "decision": "manual_review",
        },
        reason_codes=[
            "INCOME_DOCUMENTATION_INCOMPLETE",
        ],
        trace_id=trace["trace_id"],
        risk_level="high",
        review_required=True,
        review_reason="Income documentation is incomplete.",
        policy_status="warning",
        approval_status="pending",
    )

    ledger.complete_trace(
        trace_id=trace["trace_id"],
        outcome="manual_review_required",
        approval_status="pending",
    )

    return ledger.export_trace(trace["trace_id"])


if __name__ == "__main__":
    base_path = Path("demo_output")
    base_path.mkdir(exist_ok=True)

    audit_record = run_underwriting_audit_demo(
        event_log_path=base_path / "underwriting_events.jsonl",
        trace_log_path=base_path / "underwriting_traces.jsonl",
    )

    print(json.dumps(audit_record, indent=2))