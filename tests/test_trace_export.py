#This Feature Creates the Trace Exporter for the Agent Ledger. It allows for the export of traces to a JSON

import pytest

from agentledger import AgentLedger


def build_completed_trace(ledger):
    trace = ledger.create_trace(
        workflow="heloc_underwriting",
        agent_name="UnderwritingAgent",
        entity_id="application_123",
        metadata={"environment": "test"},
    )

    ledger.log_tool_call(
        agent_name="UnderwritingAgent",
        tool_name="income_verification_api",
        input_data={"document_type": "paystub"},
        output_data={"status": "partial"},
        trace_id=trace["trace_id"],
    )

    ledger.log_decision(
        agent_name="UnderwritingAgent",
        output_data={"decision": "manual_review"},
        reason_codes=["INCOME_DOCUMENTATION_INCOMPLETE"],
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

    return trace


def test_export_trace_returns_complete_audit_record(tmp_path):
    log_path = tmp_path / "events.jsonl"
    trace_path = tmp_path / "traces.jsonl"

    ledger = AgentLedger(
        storage_path=str(log_path),
        trace_storage_path=str(trace_path),
    )

    trace = build_completed_trace(ledger)

    audit_record = ledger.export_trace(trace["trace_id"])

    assert audit_record["export_type"] == "AgentLedger Trace Audit Record"
    assert audit_record["trace"]["trace_id"] == trace["trace_id"]
    assert audit_record["trace"]["workflow"] == "heloc_underwriting"
    assert audit_record["trace"]["status"] == "completed"
    assert audit_record["trace"]["outcome"] == "manual_review_required"
    assert audit_record["trace"]["approval_status"] == "pending"

    assert len(audit_record["events"]) == 2
    assert audit_record["events"][0]["event_type"] == "tool_call"
    assert audit_record["events"][1]["event_type"] == "decision"


def test_export_trace_includes_audit_summary(tmp_path):
    log_path = tmp_path / "events.jsonl"
    trace_path = tmp_path / "traces.jsonl"

    ledger = AgentLedger(
        storage_path=str(log_path),
        trace_storage_path=str(trace_path),
    )

    trace = build_completed_trace(ledger)

    audit_record = ledger.export_trace(trace["trace_id"])

    assert audit_record["summary"]["event_count"] == 2
    assert audit_record["summary"]["tool_call_count"] == 1
    assert audit_record["summary"]["decision_count"] == 1
    assert audit_record["summary"]["review_required"] is True
    assert audit_record["summary"]["highest_risk_level"] == "high"


def test_export_trace_rejects_unknown_trace_id(tmp_path):
    log_path = tmp_path / "events.jsonl"
    trace_path = tmp_path / "traces.jsonl"

    ledger = AgentLedger(
        storage_path=str(log_path),
        trace_storage_path=str(trace_path),
    )

    with pytest.raises(ValueError, match="Trace not found"):
        ledger.export_trace("missing-trace-id")