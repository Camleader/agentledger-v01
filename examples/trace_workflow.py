from agentledger import AgentLedger


ledger = AgentLedger()

trace_id = ledger.start_trace()

ledger.log_tool_call(
    agent_name="UnderwritingAgent",
    tool_name="income_verification_api",
    input_data={
        "borrower_id": "demo_001",
    },
    output_data={
        "status": "verified",
    },
    trace_id=trace_id,
)

ledger.log_tool_call(
    agent_name="UnderwritingAgent",
    tool_name="credit_report_api",
    input_data={
        "borrower_id": "demo_001",
    },
    output_data={
        "credit_score": 710,
    },
    trace_id=trace_id,
)

ledger.log_decision(
    agent_name="UnderwritingAgent",
    input_data={
        "credit_score": 710,
        "cltv": 82,
        "dti": 39,
    },
    output_data={
        "decision": "manual_review",
    },
    reason_codes=[
        "CLTV_ABOVE_POLICY_LIMIT",
    ],
    trace_id=trace_id,
)

workflow_events = ledger.get_events_by_trace(trace_id)

print(f"Trace ID: {trace_id}")
print(f"Events in workflow: {len(workflow_events)}")

for event in workflow_events:
    print(f"- {event['event_type']}: {event['agent_name']}")