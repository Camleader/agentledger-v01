from examples.quickstart import run_quickstart


def test_quickstart_returns_completed_audit_record(tmp_path):
    audit_record = run_quickstart(
        event_log_path=tmp_path / "events.jsonl",
        trace_log_path=tmp_path / "traces.jsonl",
    )

    assert audit_record["export_type"] == "AgentLedger Trace Audit Record"
    assert audit_record["trace"]["workflow"] == "example_workflow"
    assert audit_record["trace"]["agent_name"] == "ExampleAgent"
    assert audit_record["trace"]["status"] == "completed"
    assert audit_record["trace"]["outcome"] == "approved"
    assert audit_record["trace"]["approval_status"] == "approved"

    assert audit_record["summary"]["event_count"] == 1
    assert audit_record["summary"]["decision_count"] == 1
    assert audit_record["summary"]["tool_call_count"] == 0
    assert audit_record["summary"]["review_required"] is False
    assert audit_record["summary"]["highest_risk_level"] == "low"

    