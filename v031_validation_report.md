# AgentLedger Audit Report

Total events: 3

## Event 1

- **Event ID:** 962ff2ad-d845-4031-a77e-f635b76485e5
- **Timestamp:** 2026-07-28T02:15:11.459323+00:00
- **Event Type:** action
- **Agent Name:** UnderwritingAgent
- **Trace ID:** 198d4c20-9f49-4a3e-8dd8-1bf30af8d043
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
- **Previous Hash:** 
- **SHA256:** d05947287ba2463bbed61ac99d7727793cc12412b1810030d71f39656085521c

## Event 2

- **Event ID:** f4fd0445-d5db-4820-8e23-4a37f2c32446
- **Timestamp:** 2026-07-28T02:15:11.459430+00:00
- **Event Type:** action
- **Agent Name:** UnderwritingAgent
- **Trace ID:** 198d4c20-9f49-4a3e-8dd8-1bf30af8d043
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
- **Previous Hash:** 
- **SHA256:** 0e35f2cfe2ac75d3680f325bd9ae8a2452ae777493268cff3b377d7d000bcc1e

## Event 3

- **Event ID:** 972092a1-18bc-4142-b758-588fc4dde95c
- **Timestamp:** 2026-07-28T02:15:11.459481+00:00
- **Event Type:** decision
- **Agent Name:** UnderwritingAgent
- **Trace ID:** 198d4c20-9f49-4a3e-8dd8-1bf30af8d043
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
- **Previous Hash:** 
- **SHA256:** e2cb788beadcc7744b534031bccadc69aa7f1e247349f97f07da7e74bbb81bb8
