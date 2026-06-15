# This shows that AgentLedger is not only for underwriting. it can also log: 
# Search Tools
# API Calls
# Database lookups 
# calculators 
#internal services
# Model Calls 

from agentledger import AgentLedger


ledger = AgentLedger()

event = ledger.log_tool_call(
    agent_name="ResearchAgent",
    tool_name="web_search",
    input_data={
        "query": "latest AI compliance requirements",
    },
    output_data={
        "status": "completed",
        "results_found": 5,
    },
    metadata={
        "example": "tool_call_demo",
        "environment": "local",
    },
)

print("Tool call logged:")
print(event)