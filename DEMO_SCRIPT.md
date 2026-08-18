# AgentLedger v0.3.2 Founder Demo Script

## 10-second positioning

AgentLedger is a lightweight evidence layer for AI agents. It records actions, tool calls, decisions, review status, and workflow outcomes, then lets you inspect the records and verify whether they changed.

## Run the official demo

From the repository root with the virtual environment active:

```bash
python -m examples.end_to_end_agent_demo
```

## Walkthrough

“This is a deterministic HELOC underwriting assistant. The mock agent receives one application, calls three local tools, makes a decision, and routes the case for human review.

AgentLedger is not the underwriting agent. The application calls AgentLedger as the workflow runs so there is an ordered evidence record of what happened.”

Point to the terminal summary:

- Six total events
- Three tool calls
- One decision
- High risk
- Manual review required
- Four reason codes

“The decision is held for review because verified income is below the stated amount, the credit score is below the demo threshold, DTI is high, and CLTV is high. These are evidence fields supplied by the workflow, not conclusions AgentLedger invented.”

Point to both integrity results:

- `hash_check.valid: true` for six event records
- `trace_hash_check.valid: true` for the completed trace record

“The hash chains make later modification detectable. They do not independently prove that the original application data was true.”

## Inspect the output

Open one or both of these files:

```text
demo_output/end_to_end_agent/trace_audit_record.json
demo_output/end_to_end_agent/audit_report.md
```

In the trace record, show:

1. The completed workflow status
2. The `manual_review_required` outcome
3. The pending approval status
4. The six ordered events
5. The summary counts

In the Markdown report, show that the same evidence is readable without custom tooling.

## Close

“AgentLedger gives developers a small, framework-agnostic way to capture inspectable evidence around agent behavior. It does not replace the agent, enforce policy, or certify compliance. v0.3.2 focuses on making that value understandable and runnable in about a minute.”
