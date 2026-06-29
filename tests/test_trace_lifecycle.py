# Start Trace Lifecycle Tests

from agentledger import AgentLedger


def test_start_trace_creates_persisted_trace(tmp_path):
    log_path = tmp_path / "events.jsonl"
    trace_path = tmp_path / "traces.jsonl"

    ledger = AgentLedger(
        storage_path=str(log_path),
        trace_storage_path=str(trace_path),
    )

    trace = ledger.create_trace(
        workflow="heloc_underwriting",
        agent_name="UnderwritingAgent",
        entity_id="application_123",
        metadata={"environment": "test"},
    )

    assert trace["trace_id"]
    assert trace["workflow"] == "heloc_underwriting"
    assert trace["agent_name"] == "UnderwritingAgent"
    assert trace["entity_id"] == "application_123"
    assert trace["metadata"] == {"environment": "test"}
    assert trace["status"] == "active"
    assert trace["outcome"] is None
    assert trace["completed_at"] is None
    assert trace_path.exists()


def test_get_trace_returns_trace_and_events(tmp_path):
    log_path = tmp_path / "events.jsonl"
    trace_path = tmp_path / "traces.jsonl"

    ledger = AgentLedger(
        storage_path=str(log_path),
        trace_storage_path=str(trace_path),
    )

    trace = ledger.create_trace(
        workflow="heloc_underwriting",
        agent_name="UnderwritingAgent",
    )

    ledger.log_tool_call(
        agent_name="UnderwritingAgent",
        tool_name="income_verification_api",
        trace_id=trace["trace_id"],
    )

    ledger.log_decision(
        agent_name="UnderwritingAgent",
        output_data={"decision": "manual_review"},
        trace_id=trace["trace_id"],
    )

    result = ledger.get_trace(trace["trace_id"])

    assert result["trace"]["trace_id"] == trace["trace_id"]
    assert len(result["events"]) == 2
    assert result["events"][0]["event_type"] == "tool_call"
    assert result["events"][1]["event_type"] == "decision"


def test_complete_trace_updates_outcome_and_status(tmp_path):
    log_path = tmp_path / "events.jsonl"
    trace_path = tmp_path / "traces.jsonl"

    ledger = AgentLedger(
        storage_path=str(log_path),
        trace_storage_path=str(trace_path),
    )

    trace = ledger.create_trace(
        workflow="heloc_underwriting",
        agent_name="UnderwritingAgent",
    )

    completed_trace = ledger.complete_trace(
        trace_id=trace["trace_id"],
        outcome="manual_review_required",
        approval_status="pending",
    )

    assert completed_trace["status"] == "completed"
    assert completed_trace["outcome"] == "manual_review_required"
    assert completed_trace["approval_status"] == "pending"
    assert completed_trace["completed_at"] is not None