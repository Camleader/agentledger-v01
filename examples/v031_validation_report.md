# AgentLedger Audit Report

Total events: 3

## Event 1

- **Event ID:** ca3d52b9-5b61-4e09-9c4c-ca5b96679c58
- **Timestamp:** 2026-07-28T01:46:21.096109+00:00
- **Event Type:** action
- **Agent Name:** UnderwritingAgent
- **Trace ID:** e0e6148e-2404-4a8b-b4ba-e8376517cac6
- **Input Data:** `{"application_id": "application_123"}`
- **Output Data:** `{"status": "documents_requested"}`
- **Reason Codes:** `[]`
- **Metadata:** `{"action_name": "request_income_documents"}`
- **Action Status:** executed
- **Risk Level:** 
- **Review Required:** 
- **Review Reason:** 
- **Policy Status:** 
- **Approval Status:** 
- **Agent ID:** underwriting_agent_001
- **Agent Version:** 0.3.1
- **Model Version:** gpt-5
- **Prompt Version:** underwriting_prompt_v1
- **Workflow Version:** heloc_workflow_v1
- **Policy Version:** credit_policy_v1
- **Previous Hash:** None
- **SHA256:** 5e6e6c369ae02d0bbfb8c9bb62d71fd2431a82235fddc956b708110d3dd91808

## Event 2

- **Event ID:** ffe9f971-8c5e-4560-8470-dab997811d31
- **Timestamp:** 2026-07-28T01:46:21.096341+00:00
- **Event Type:** action
- **Agent Name:** UnderwritingAgent
- **Trace ID:** e0e6148e-2404-4a8b-b4ba-e8376517cac6
- **Input Data:** `{"application_id": "application_123"}`
- **Output Data:** `{"reason": "income documentation incomplete"}`
- **Reason Codes:** `[]`
- **Metadata:** `{"action_name": "hold_application_for_review"}`
- **Action Status:** held_for_review
- **Risk Level:** 
- **Review Required:** 
- **Review Reason:** 
- **Policy Status:** 
- **Approval Status:** 
- **Agent ID:** underwriting_agent_001
- **Agent Version:** 0.3.1
- **Model Version:** gpt-5
- **Prompt Version:** underwriting_prompt_v1
- **Workflow Version:** heloc_workflow_v1
- **Policy Version:** credit_policy_v1
- **Previous Hash:** 5e6e6c369ae02d0bbfb8c9bb62d71fd2431a82235fddc956b708110d3dd91808
- **SHA256:** b1bd1fcb258803d21852a742ac69ad478fcc60f1b9cdf0d10a994c83cf89feb4

## Event 3

- **Event ID:** 0199a1ef-7360-4300-9ad1-46b1f4afa8d9
- **Timestamp:** 2026-07-28T01:46:21.096479+00:00
- **Event Type:** decision
- **Agent Name:** UnderwritingAgent
- **Trace ID:** e0e6148e-2404-4a8b-b4ba-e8376517cac6
- **Input Data:** `{}`
- **Output Data:** `{"decision": "manual_review_required"}`
- **Reason Codes:** `["INCOME_DOCUMENTATION_INCOMPLETE"]`
- **Metadata:** `{}`
- **Action Status:** executed
- **Risk Level:** high
- **Review Required:** True
- **Review Reason:** Income documents need human review.
- **Policy Status:** warning
- **Approval Status:** pending
- **Agent ID:** None
- **Agent Version:** None
- **Model Version:** None
- **Prompt Version:** None
- **Workflow Version:** None
- **Policy Version:** None
- **Previous Hash:** b1bd1fcb258803d21852a742ac69ad478fcc60f1b9cdf0d10a994c83cf89feb4
- **SHA256:** 2bdce9c39b0ceb01f170d8dc6207ec233a348c6d02c8aff266ee6f351f8e21b7
