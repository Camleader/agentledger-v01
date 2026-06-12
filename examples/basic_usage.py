# Create the Basic Developer Example v0.2.1 STEP 7
from agentledger import AgentLedger


ledger = AgentLedger()

decision_event = ledger.log_decision(
    agent_name="UnderwritingAgent",
    input_data={
        "credit_score": 710,
        "cltv": 72,
        "dti": 38,
    },
    output_data={
        "decision": "manual_review",
        "confidence": 0.86,
    },
    reason_codes=[
        "CLTV_REVIEW",
        "INCOME_VERIFICATION_REQUIRED",
    ],
    metadata={
        "model": "demo-underwriting-agent-v1",
        "environment": "local",
    },
)

tool_event = ledger.log_tool_call(
    agent_name="UnderwritingAgent",
    tool_name="income_verification_api",
    input_data={
        "borrower_id": "demo_001",
    },
    output_data={
        "status": "requires_additional_documents",
    },
)

print("Decision event logged:")
print(decision_event)

print("\nTool call event logged:")
print(tool_event)