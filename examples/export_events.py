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

json_path = ledger.export_json("audit_events.json")
csv_path = ledger.export_csv("audit_events.csv")
report_path = ledger.export_markdown_report(
    "underwriting_audit_report.md",
    events=decision_events,
)

print(f"Exported {len(all_events)} total events to: {json_path}")
print(f"Exported {len(all_events)} total events to: {csv_path}")
print(
    f"Exported {len(decision_events)} decision events to: {report_path}"
)
