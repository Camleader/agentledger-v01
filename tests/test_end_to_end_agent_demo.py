import csv
import json

from examples.end_to_end_agent_demo import run_demo


def test_end_to_end_agent_demo_is_repeatable_and_verifiable(tmp_path):
    output_dir = tmp_path / "end_to_end_agent"

    first_result = run_demo(output_dir)
    second_result = run_demo(output_dir)

    assert first_result["final_decision"] == "manual_review"
    assert first_result["review_required"] is True
    assert len(first_result["reason_codes"]) == 4
    assert first_result["summary"] == {
        "event_count": 6,
        "tool_call_count": 3,
        "decision_count": 1,
        "review_required": True,
        "highest_risk_level": "high",
    }
    assert all(first_result["checklist"].values())
    assert first_result["hash_check"] == {"valid": True, "total_records": 6}
    assert first_result["trace_hash_check"] == {
        "valid": True,
        "total_records": 1,
    }

    event_log_path = output_dir / "events.jsonl"
    trace_log_path = output_dir / "traces.jsonl"
    json_export_path = output_dir / "events_export.json"
    csv_export_path = output_dir / "events_export.csv"
    markdown_export_path = output_dir / "audit_report.md"
    trace_export_path = output_dir / "trace_audit_record.json"

    expected_paths = [
        event_log_path,
        trace_log_path,
        json_export_path,
        csv_export_path,
        markdown_export_path,
        trace_export_path,
    ]
    assert all(path.exists() for path in expected_paths)

    events = json.loads(json_export_path.read_text(encoding="utf-8"))
    assert [event["event_type"] for event in events] == [
        "action",
        "tool_call",
        "tool_call",
        "tool_call",
        "decision",
        "action",
    ]
    assert len(event_log_path.read_text(encoding="utf-8").splitlines()) == 6

    with csv_export_path.open(newline="", encoding="utf-8") as csv_file:
        assert len(list(csv.DictReader(csv_file))) == 6

    markdown_report = markdown_export_path.read_text(encoding="utf-8")
    assert markdown_report.count("## Event ") == 6

    trace_export = json.loads(trace_export_path.read_text(encoding="utf-8"))
    assert len(trace_export["events"]) == 6
    assert trace_export["trace"]["status"] == "completed"
    assert trace_export["trace"]["outcome"] == "manual_review_required"
    assert trace_export["trace"]["approval_status"] == "pending"

    assert second_result["summary"]["event_count"] == 6
    assert second_result["hash_check"]["valid"] is True
    assert second_result["trace_hash_check"]["valid"] is True
    assert len(event_log_path.read_text(encoding="utf-8").splitlines()) == 6
    assert len(trace_log_path.read_text(encoding="utf-8").splitlines()) == 1
