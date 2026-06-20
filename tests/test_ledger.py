# Add the First Test v0.2.1 STEP 10

import json

import pytest

import agentledger
from agentledger import AgentLedger

def test_package_exposes_version():
    assert agentledger.__version__ == "0.2.4"

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