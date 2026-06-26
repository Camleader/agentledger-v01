# AgentLedger

AgentLedger is an audit and approval layer for AI agents operating in regulated workflows.

Prove what your AI agent did.

## Problem

AI agents are beginning to take actions and make recommendations in workflows where trust, compliance, and accountability matter.

Developers and companies need a way to answer:

- What did the agent do?
- What inputs did it use?
- What decision did it make?
- What risks were flagged?
- Why did it make that decision?
- Was there human approval?
- Can the record be exported for review?

## Quickstart

AgentLedger is a lightweight Python SDK for logging AI agent decisions, tool calls, inputs, outputs, reason codes, and metadata into a structured audit trail.

## Solution

AgentLedger creates structured audit records for AI agent decisions.

Core workflow:

Log → Trace → Flag risk → Explain → Approve → Export

## Event Validation

AgentLedger validates event structure before writing logs. Required fields such as `agent_name`, `event_type`, and `tool_name` are checked to prevent incomplete audit records. Validation currently checks that:

- `event_type` is one of the supported event types: `event`, `decision`, or `tool_call`
- `agent_name` is a non-empty string
- `input_data` is a dictionary
- `output_data` is a dictionary
- `reason_codes` is a list
- `metadata` is a dictionary
- `tool_name` is required for tool call events

## Querying Events

AgentLedger can read previously logged events from its JSONL audit file.

```python
from agentledger import AgentLedger

ledger = AgentLedger()

all_events = ledger.list_events()
decision_events = ledger.get_events_by_type("decision")
underwriting_events = ledger.get_events_by_agent("UnderwritingAgent")

## Exporting Events

AgentLedger can export audit events into JSON, CSV, and Markdown reports.

```python
from agentledger import AgentLedger

ledger = AgentLedger()

ledger.export_json("audit_events.json")
ledger.export_csv("audit_events.csv")

decision_events = ledger.get_events_by_type("decision")

ledger.export_markdown_report(
    "decision_audit_report.md",
    events=decision_events,
)

## Tracing Agent Workflows

AgentLedger can connect multiple events from the same AI-agent workflow using a shared `trace_id`.

```python
from agentledger import AgentLedger

ledger = AgentLedger()

trace_id = ledger.start_trace()

ledger.log_tool_call(
    agent_name="UnderwritingAgent",
    tool_name="income_verification_api",
    trace_id=trace_id,
)

ledger.log_decision(
    agent_name="UnderwritingAgent",
    output_data={"decision": "manual_review"},
    trace_id=trace_id,
)

workflow_events = ledger.get_events_by_trace(trace_id)

## Current Demo

AgentLedger v0.1.4 includes a local HELOC underwriting agent demo.

The demo:

- Accepts borrower application data
- Runs a simulated HELOC underwriting agent
- Calculates CLTV and DTI
- Produces an approval, manual review, or decline recommendation
- Generates reason codes
- Flags risk
- Captures human review status
- Exports a structured JSON audit record

## Demo Presets

The app includes three borrower scenarios:

- Approve Demo
- Manual Review Demo
- Decline Demo

These allow quick live demonstrations without manually entering data.

## Audit Export

The JSON audit export includes:

- Product metadata
- Agent run metadata
- Borrower application data
- Decision summary
- Calculations
- Reason codes
- Risk flags
- Highest risk severity
- Human review status
- Trace events
- Compliance note

## Run Examples

```bash
PYTHONPATH=. python3 examples/basic_usage.py
PYTHONPATH=. python3 examples/underwriting_agent.py
PYTHONPATH=. python3 examples/tool_call_demo.py
PYTHONPATH=. python3 examples/query_events.py
PYTHONPATH=. python3 examples/export_events.py
PYTHONPATH=. python3 examples/trace_workflow.py

## Target User

AI developers building agents that operate in regulated, sensitive, or high-accountability workflows.

## First Buyer

AI startups selling into fintech and regulated enterprise customers.

## Pricing Concept

- Pro: $49/month
- Team: $299/month

## How to Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the app:

```bash
streamlit run app.py
```

Run tests:

```bash
pytest
```

## Project Structure

```text
app.py
agentledger/
tests/
README.md
requirements.txt
screenshots/
```

## Version History

v0.1.0 - Core local HELOC agent demo
v0.1.1 - UI and run summary polish
v0.1.2 - Demo presets
v0.1.3 - Structured audit export polish
v0.1.4 - GitHub-ready README and demo presentation polish

## Roadmap

v0.2 - Developer SDK
v0.3 - Hosted dashboard
v0.4 - Team workspaces and paid beta
v0.5 - Agent integration templates

## Status

Local prototype.
Not production-ready.
No external APIs.
No authentication.
No database.
No legal/compliance guarantee.

## Founder Note

AgentLedger is being built as a founder-led prototype to explore how AI agent activity can be made traceable, reviewable, and exportable for regulated workflows.
