from pathlib import Path

log_path = Path("v031_validation_logs.jsonl")

if log_path.exists():
    log_path.unlink()


from agentledger import AgentLedger

ledger = AgentLedger(storage_path=str(log_path))

trace = ledger.create_trace(
    workflow="heloc_underwriting_v031_validation",
    agent_name="UnderwritingAgent",
    entity_id="application_123",
    metadata={"environment": "local_validation"},
)

ledger.log_action(
    agent_name="UnderwritingAgent",
    action_name="request_income_documents",
    trace_id=trace["trace_id"],
    action_status="executed",
    agent_id="underwriting_agent_001",
    agent_version="0.3.1",
    model_version="gpt-5",
    prompt_version="underwriting_prompt_v1",
    workflow_version="heloc_workflow_v1",
    policy_version="credit_policy_v1",
    input_data={"application_id": "application_123"},
    output_data={"status": "documents_requested"},
)

ledger.log_action(
    agent_name="UnderwritingAgent",
    action_name="hold_application_for_review",
    trace_id=trace["trace_id"],
    action_status="held_for_review",
    agent_id="underwriting_agent_001",
    agent_version="0.3.1",
    model_version="gpt-5",
    prompt_version="underwriting_prompt_v1",
    workflow_version="heloc_workflow_v1",
    policy_version="credit_policy_v1",
    input_data={"application_id": "application_123"},
    output_data={"reason": "income documentation incomplete"},
)

ledger.log_decision(
    agent_name="UnderwritingAgent",
    trace_id=trace["trace_id"],
    output_data={"decision": "manual_review_required"},
    reason_codes=["INCOME_DOCUMENTATION_INCOMPLETE"],
    risk_level="high",
    review_required=True,
    review_reason="Income documents need human review.",
    policy_status="warning",
    approval_status="pending",
)

ledger.complete_trace(
    trace_id=trace["trace_id"],
    outcome="manual_review_required",
    approval_status="pending",
)

events = ledger.list_events()

ledger.export_csv("v031_validation_events.csv")
ledger.export_markdown_report("v031_validation_report.md")

print("Hash chain result:")
print(ledger.verify_hash_chain())

print("\nEvents created:")
for event in events:
    print({
        "event_type": event.get("event_type"),
        "action_status": event.get("action_status"),
        "agent_id": event.get("agent_id"),
        "prev_hash": event.get("prev_hash"),
        "sha256": event.get("sha256"),
    })
    
    
