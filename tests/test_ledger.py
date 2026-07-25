# Add the First Test v0.2.1 STEP 10

import json

import pytest

import agentledger
from agentledger import AgentLedger

def test_package_exposes_version():
    assert agentledger.__version__ == "0.3.1"

def test_package_imports_agentledger_class():
    assert AgentLedger is not None


def test_log_decision_creates_event(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"

    ledger = AgentLedger(storage_path=str(log_path))

    event = ledger.log_decision(
        agent_name="TestAgent",
        input_data={"value": 1},
        output_data={"decision": "approve"},
        reason_codes=["TEST_REASON"],
    )

    assert event["event_type"] == "decision"
    assert event["agent_name"] == "TestAgent"
    assert event["input_data"] == {"value": 1}
    assert event["output_data"] == {"decision": "approve"}
    assert event["reason_codes"] == ["TEST_REASON"]
    assert "event_id" in event
    assert "timestamp" in event

    assert log_path.exists()

    lines = log_path.read_text().splitlines()
    assert len(lines) == 1

    saved_event = json.loads(lines[0])
    assert saved_event["event_id"] == event["event_id"]


def test_log_tool_call_adds_tool_name(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"

def test_log_event_defaults_action_status_to_executed(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    event = ledger.log_decision(
        agent_name="TestAgent",
        input_data={"value": 1},
        output_data={"decision": "approve"},
    )

    assert event["action_status"] == "executed"


def test_log_event_rejects_invalid_action_status(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    with pytest.raises(ValueError, match="action_status must be one of"):
        ledger.log_event(
            event_type="tool_call",
            agent_name="TestAgent",
            input_data={"query": "test"},
            output_data={"result": "ok"},
            action_status="maybe",
        )

    ledger = AgentLedger(storage_path=str(log_path))

    event = ledger.log_tool_call(
        agent_name="TestAgent",
        tool_name="search_api",
        input_data={"query": "test"},
        output_data={"result": "ok"},
    )

    assert event["event_type"] == "tool_call"
    assert event["metadata"]["tool_name"] == "search_api"

# We will add tests that prove that bad data is rejected 
# v0.2.2 should test: 
# Empty agent_name fails 
# Invalid event_type fails
# input_data must be a dictionary
# output_data must be a dictionary
# reason_codes must be a list
# metadata must be a dictionary
# tool_name is required for tool calls
# Valid decision still works
# Valid tool call still works
# This tep is important because it proves the SDK is becoming more reliable. 

# v0.2.4 version tests 

def test_list_events_returns_written_events(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    ledger.log_decision(
        agent_name="UnderwritingAgent",
        input_data={"credit_score": 710},
        output_data={"decision": "approve"},
    )

    ledger.log_tool_call(
        agent_name="UnderwritingAgent",
        tool_name="income_verification_api",
        input_data={"borrower_id": "demo_001"},
        output_data={"status": "verified"},
    )

    events = ledger.list_events()

    assert len(events) == 2
    assert events[0]["event_type"] == "decision"
    assert events[1]["event_type"] == "tool_call"


def test_list_events_returns_empty_list_when_log_file_is_missing(tmp_path):
    log_path = tmp_path / "missing_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    assert ledger.list_events() == []


def test_get_events_by_type_returns_matching_events(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    ledger.log_decision(
        agent_name="UnderwritingAgent",
        input_data={"credit_score": 710},
        output_data={"decision": "approve"},
    )

    ledger.log_tool_call(
        agent_name="UnderwritingAgent",
        tool_name="income_verification_api",
        input_data={"borrower_id": "demo_001"},
        output_data={"status": "verified"},
    )

    decision_events = ledger.get_events_by_type("decision")

    assert len(decision_events) == 1
    assert decision_events[0]["event_type"] == "decision"


def test_get_events_by_agent_returns_matching_events(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    ledger.log_decision(
        agent_name="UnderwritingAgent",
        input_data={"credit_score": 710},
        output_data={"decision": "approve"},
    )

    ledger.log_decision(
        agent_name="ResearchAgent",
        input_data={"query": "AI compliance"},
        output_data={"decision": "complete"},
    )

    underwriting_events = ledger.get_events_by_agent("UnderwritingAgent")

    assert len(underwriting_events) == 1
    assert underwriting_events[0]["agent_name"] == "UnderwritingAgent"


def test_get_events_by_type_rejects_invalid_event_type(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    with pytest.raises(ValueError, match="event_type must be one of"):
        ledger.get_events_by_type("invalid_type")


def test_get_events_by_agent_rejects_empty_agent_name(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    with pytest.raises(ValueError, match="agent_name is required"):
        ledger.get_events_by_agent("")
# v0.2.4 version tests 
def test_export_json_creates_export_file(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    export_path = tmp_path / "audit_events.json"
    ledger = AgentLedger(storage_path=str(log_path))

    ledger.log_decision(
        agent_name="UnderwritingAgent",
        input_data={"credit_score": 710},
        output_data={"decision": "approve"},
    )

    result_path = ledger.export_json(str(export_path))

    assert result_path == export_path
    assert export_path.exists()

    exported_events = json.loads(export_path.read_text())
    assert len(exported_events) == 1
    assert exported_events[0]["event_type"] == "decision"


def test_export_csv_creates_export_file(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    export_path = tmp_path / "audit_events.csv"
    ledger = AgentLedger(storage_path=str(log_path))

    ledger.log_tool_call(
        agent_name="ResearchAgent",
        tool_name="web_search",
        input_data={"query": "AI governance"},
        output_data={"status": "completed"},
    )

    result_path = ledger.export_csv(str(export_path))

    assert result_path == export_path
    assert export_path.exists()

    csv_contents = export_path.read_text()
    assert "event_type" in csv_contents
    assert "tool_call" in csv_contents
    assert "ResearchAgent" in csv_contents


def test_export_markdown_report_creates_export_file(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    export_path = tmp_path / "audit_report.md"
    ledger = AgentLedger(storage_path=str(log_path))

    ledger.log_decision(
        agent_name="UnderwritingAgent",
        input_data={"credit_score": 710},
        output_data={"decision": "manual_review"},
        reason_codes=["CLTV_ABOVE_POLICY_LIMIT"],
    )

    result_path = ledger.export_markdown_report(str(export_path))

    assert result_path == export_path
    assert export_path.exists()

    report_contents = export_path.read_text()
    assert "# AgentLedger Audit Report" in report_contents
    assert "UnderwritingAgent" in report_contents
    assert "CLTV_ABOVE_POLICY_LIMIT" in report_contents


def test_export_can_use_filtered_events(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    export_path = tmp_path / "decision_events.json"
    ledger = AgentLedger(storage_path=str(log_path))

    ledger.log_decision(
        agent_name="UnderwritingAgent",
        input_data={"credit_score": 710},
        output_data={"decision": "approve"},
    )

    ledger.log_tool_call(
        agent_name="UnderwritingAgent",
        tool_name="income_verification_api",
        input_data={"borrower_id": "demo_001"},
        output_data={"status": "verified"},
    )

    decision_events = ledger.get_events_by_type("decision")
    ledger.export_json(str(export_path), events=decision_events)

    exported_events = json.loads(export_path.read_text())

    assert len(exported_events) == 1
    assert exported_events[0]["event_type"] == "decision"

# v0.2.6 version tests
def test_start_trace_returns_non_empty_string(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    trace_id = ledger.start_trace()

    assert isinstance(trace_id, str)
    assert trace_id


def test_events_can_share_same_trace_id(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))
    trace_id = ledger.start_trace()

    decision_event = ledger.log_decision(
        agent_name="UnderwritingAgent",
        input_data={"credit_score": 710},
        output_data={"decision": "manual_review"},
        trace_id=trace_id,
    )

    tool_event = ledger.log_tool_call(
        agent_name="UnderwritingAgent",
        tool_name="income_verification_api",
        input_data={"borrower_id": "demo_001"},
        output_data={"status": "verified"},
        trace_id=trace_id,
    )

    assert decision_event["trace_id"] == trace_id
    assert tool_event["trace_id"] == trace_id


def test_get_events_by_trace_returns_related_events(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    first_trace_id = ledger.start_trace()
    second_trace_id = ledger.start_trace()

    ledger.log_decision(
        agent_name="UnderwritingAgent",
        input_data={"credit_score": 710},
        output_data={"decision": "approve"},
        trace_id=first_trace_id,
    )

    ledger.log_tool_call(
        agent_name="UnderwritingAgent",
        tool_name="income_verification_api",
        input_data={"borrower_id": "demo_001"},
        output_data={"status": "verified"},
        trace_id=first_trace_id,
    )

    ledger.log_decision(
        agent_name="ResearchAgent",
        input_data={"query": "AI compliance"},
        output_data={"decision": "complete"},
        trace_id=second_trace_id,
    )

    related_events = ledger.get_events_by_trace(first_trace_id)

    assert len(related_events) == 2
    assert all(event["trace_id"] == first_trace_id for event in related_events)


def test_get_events_by_trace_rejects_empty_trace_id(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    with pytest.raises(ValueError, match="trace_id is required"):
        ledger.get_events_by_trace("")
        
@pytest.mark.parametrize(
    "action_status",
    [
        "executed",
        "denied",
        "failed",
        "held_for_review",
    ],
)
def test_log_tool_call_accepts_valid_action_statuses(tmp_path, action_status):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    event = ledger.log_tool_call(
        agent_name="TestAgent",
        tool_name="payment_api",
        input_data={"amount": 100},
        output_data={"status": action_status},
        action_status=action_status,
    )
    assert event["action_status"] == action_status

def test_log_action_creates_action_event(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    event = ledger.log_action(
        agent_name="TestAgent",
        action_name="send_email",
        input_data={"recipient": "user@example.com"},
        output_data={"status": "sent"},
        action_status="executed",
    )

    assert event["event_type"] == "action"
    assert event["metadata"]["action_name"] == "send_email"
    assert event["action_status"] == "executed"

def test_log_event_stores_attribution_fields(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    event = ledger.log_event(
        event_type="action",
        agent_name="TestAgent",
        input_data={"value": 1},
        output_data={"status": "ok"},
        agent_id="agent_001",
        agent_version="0.1.0",
        model_version="gpt-5",
        prompt_version="prompt_v1",
        workflow_version="workflow_v1",
        policy_version="policy_v1",
    )

    assert event["agent_id"] == "agent_001"
    assert event["agent_version"] == "0.1.0"
    assert event["model_version"] == "gpt-5"
    assert event["prompt_version"] == "prompt_v1"
    assert event["workflow_version"] == "workflow_v1"
    assert event["policy_version"] == "policy_v1"


def test_log_event_rejects_empty_attribution_field(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    with pytest.raises(ValueError, match="agent_id is required"):
        ledger.log_event(
            event_type="action",
            agent_name="TestAgent",
            agent_id="",
        )
def test_log_action_stores_attribution_fields(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    event = ledger.log_action(
        agent_name="TestAgent",
        action_name="send_email",
        agent_id="agent_001",
        agent_version="0.1.0",
        model_version="gpt-5",
        prompt_version="prompt_v1",
        workflow_version="workflow_v1",
        policy_version="policy_v1",
    )

    assert event["agent_id"] == "agent_001"
    assert event["agent_version"] == "0.1.0"
    assert event["model_version"] == "gpt-5"
    assert event["prompt_version"] == "prompt_v1"
    assert event["workflow_version"] == "workflow_v1"
    assert event["policy_version"] == "policy_v1"

def test_log_decision_stores_attribution_fields(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    event = ledger.log_decision(
        agent_name="TestAgent",
        agent_id="agent_001",
        model_version="gpt-5",
        policy_version="policy_v1",
    )

    assert event["agent_id"] == "agent_001"
    assert event["model_version"] == "gpt-5"
    assert event["policy_version"] == "policy_v1"


def test_log_tool_call_stores_attribution_fields(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    event = ledger.log_tool_call(
        agent_name="TestAgent",
        tool_name="search_api",
        agent_id="agent_001",
        model_version="gpt-5",
        policy_version="policy_v1",
    )

    assert event["agent_id"] == "agent_001"
    assert event["model_version"] == "gpt-5"
    assert event["policy_version"] == "policy_v1"

def test_log_event_adds_hash_fields(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    event = ledger.log_action(
        agent_name="TestAgent",
        action_name="send_email",
    )

    assert event["prev_hash"] is None
    assert "sha256" in event
    assert len(event["sha256"]) == 64


def test_log_event_links_to_previous_event_hash(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    first_event = ledger.log_action(
        agent_name="TestAgent",
        action_name="first_action",
    )

    second_event = ledger.log_action(
        agent_name="TestAgent",
        action_name="second_action",
    )

    assert second_event["prev_hash"] == first_event["sha256"]

def test_verify_hash_chain_returns_valid_for_untampered_log(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    ledger.log_action(
        agent_name="TestAgent",
        action_name="first_action",
    )

    ledger.log_action(
        agent_name="TestAgent",
        action_name="second_action",
    )

    result = ledger.verify_hash_chain()

    assert result["valid"] is True
    assert result["total_records"] == 2

def test_verify_hash_chain_detects_tampered_log(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    ledger = AgentLedger(storage_path=str(log_path))

    ledger.log_action(
        agent_name="TestAgent",
        action_name="send_email",
        output_data={"status": "sent"},
    )

    records = [
        json.loads(line)
        for line in log_path.read_text().splitlines()
    ]

    records[0]["output_data"] = {"status": "tampered"}

    log_path.write_text(
        "\n".join(json.dumps(record) for record in records) + "\n"
    )

    result = ledger.verify_hash_chain()

    assert result["valid"] is False
    assert result["error"] == "Invalid sha256 at record 0"
    assert result["index"] == 0

def test_export_markdown_report_includes_audit_fields(tmp_path):
    log_path = tmp_path / "test_logs.jsonl"
    export_path = tmp_path / "audit_report.md"
    ledger = AgentLedger(storage_path=str(log_path))

    ledger.log_action(
        agent_name="TestAgent",
        action_name="send_email",
        action_status="held_for_review",
        agent_id="agent_001",
        model_version="gpt-5",
        policy_version="policy_v1",
    )

    events = ledger.list_events()
    ledger.storage.export_markdown_report(events, export_path)

    report = export_path.read_text(encoding="utf-8")

    assert "Action Status" in report
    assert "held_for_review" in report
    assert "Agent ID" in report
    assert "agent_001" in report
    assert "Model Version" in report
    assert "gpt-5" in report
    assert "Policy Version" in report
    assert "policy_v1" in report
    assert "SHA256" in report