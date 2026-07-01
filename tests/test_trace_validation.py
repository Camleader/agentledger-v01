# Add edge-case tests 

import pytest

from agentledger import AgentLedger


def test_create_trace_rejects_non_dictionary_metadata(tmp_path):
    ledger = AgentLedger(
        storage_path=str(tmp_path / "events.jsonl"),
        trace_storage_path=str(tmp_path / "traces.jsonl"),
    )

    with pytest.raises(ValueError, match="metadata must be a dictionary"):
        ledger.create_trace(
            workflow="heloc_underwriting",
            agent_name="UnderwritingAgent",
            metadata=["not", "a", "dictionary"],
        )


def test_get_trace_rejects_unknown_trace_id(tmp_path):
    ledger = AgentLedger(
        storage_path=str(tmp_path / "events.jsonl"),
        trace_storage_path=str(tmp_path / "traces.jsonl"),
    )

    with pytest.raises(ValueError, match="Trace not found"):
        ledger.get_trace("missing-trace-id")


def test_complete_trace_rejects_invalid_approval_status(tmp_path):
    ledger = AgentLedger(
        storage_path=str(tmp_path / "events.jsonl"),
        trace_storage_path=str(tmp_path / "traces.jsonl"),
    )

    trace = ledger.create_trace(
        workflow="heloc_underwriting",
        agent_name="UnderwritingAgent",
    )

    with pytest.raises(ValueError, match="approval_status must be one of"):
        ledger.complete_trace(
            trace_id=trace["trace_id"],
            outcome="manual_review_required",
            approval_status="unknown_status",
        )


def test_export_trace_uses_safe_defaults_without_decision_events(tmp_path):
    ledger = AgentLedger(
        storage_path=str(tmp_path / "events.jsonl"),
        trace_storage_path=str(tmp_path / "traces.jsonl"),
    )

    trace = ledger.create_trace(
        workflow="document_collection",
        agent_name="DocumentAgent",
    )

    ledger.log_tool_call(
        agent_name="DocumentAgent",
        tool_name="document_upload_check",
        trace_id=trace["trace_id"],
    )

    audit_record = ledger.export_trace(trace["trace_id"])

    assert audit_record["summary"]["event_count"] == 1
    assert audit_record["summary"]["tool_call_count"] == 1
    assert audit_record["summary"]["decision_count"] == 0
    assert audit_record["summary"]["review_required"] is False
    assert audit_record["summary"]["highest_risk_level"] == "low"