from agentledger import AgentLedger


ledger = AgentLedger()

ledger.log_decision(
    agent_name="UnderwritingAgent",
    input_data={
        "credit_score": 710,
        "cltv": 82,
    },
    output_data={
        "decision": "manual_review",
    },
    reason_codes=[
        "CLTV_ABOVE_POLICY_LIMIT",
    ],
)

ledger.log_tool_call(
    agent_name="UnderwritingAgent",
    tool_name="income_verification_api",
    input_data={
        "borrower_id": "demo_001",
    },
    output_data={
        "status": "verified",
    },
)

all_events = ledger.list_events()
decision_events = ledger.get_events_by_type("decision")
underwriting_events = ledger.get_events_by_agent("UnderwritingAgent")

print(f"Total events: {len(all_events)}")
print(f"Decision events: {len(decision_events)}")
print(f"UnderwritingAgent events: {len(underwriting_events)}")