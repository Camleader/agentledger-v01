#Define the demo contract with a test. The demo should prove that a developer can run
# one script and receive a complete trace-level audit artifact.

from examples.underwriting_audit_demo import run_underwriting_audit_demo


def test_underwriting_audit_demo_returns_completed_audit_record(tmp_path):
    audit_record = run_underwriting_audit_demo(
        event_log_path=tmp_path / "events.jsonl",
        trace_log_path=tmp_path / "traces.jsonl",
    )

    assert audit_record["export_type"] == "AgentLedger Trace Audit Record"
    assert audit_record["trace"]["workflow"] == "heloc_underwriting"
    assert audit_record["trace"]["agent_name"] == "UnderwritingAgent"
    assert audit_record["trace"]["status"] == "completed"
    assert audit_record["trace"]["outcome"] == "manual_review_required"
    assert audit_record["trace"]["approval_status"] == "pending"

    assert audit_record["summary"]["event_count"] == 3
    assert audit_record["summary"]["tool_call_count"] == 2
    assert audit_record["summary"]["decision_count"] == 1
    assert audit_record["summary"]["review_required"] is True
    assert audit_record["summary"]["highest_risk_level"] == "high"

    event_types = [event["event_type"] for event in audit_record["events"]]
    assert event_types == ["tool_call", "tool_call", "decision"]