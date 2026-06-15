# Makes the SDK feel tied to your original AgentLedger vision: 
# AI decisions
# reason codes
# audit records 
# undeerwriting workflow 
# developer-friendly integration 

from agentledger import AgentLedger


def evaluate_borrower(borrower):
    reason_codes = []

    if borrower["credit_score"] < 680:
        reason_codes.append("CREDIT_SCORE_BELOW_THRESHOLD")

    if borrower["cltv"] > 80:
        reason_codes.append("CLTV_ABOVE_POLICY_LIMIT")

    if borrower["dti"] > 43:
        reason_codes.append("DTI_ABOVE_POLICY_LIMIT")

    if reason_codes:
        decision = "manual_review"
    else:
        decision = "approve"

    return {
        "decision": decision,
        "reason_codes": reason_codes,
    }


ledger = AgentLedger()

borrower = {
    "borrower_id": "demo_001",
    "credit_score": 710,
    "cltv": 82,
    "dti": 39,
    "income_verified": True,
}

result = evaluate_borrower(borrower)

event = ledger.log_decision(
    agent_name="UnderwritingAgent",
    input_data=borrower,
    output_data={
        "decision": result["decision"],
    },
    reason_codes=result["reason_codes"],
    metadata={
        "example": "underwriting_agent",
        "environment": "local",
    },
)

print("Underwriting decision logged:")
print(event)