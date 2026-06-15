# Add the First Test v0.2.1 STEP 10

import json
from pathlib import Path

from agentledger import AgentLedger


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