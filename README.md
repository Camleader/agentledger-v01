# AgentLedger

**AgentLedger is a lightweight Python SDK for creating traceable, reviewable, and exportable audit records for AI-agent workflows.**

It helps developers answer:

* What did the agent do?
* Which tools did it call?
* What decision did it make?
* What risks or policy signals were recorded?
* Was human review required?
* What was the final outcome?
* Can the full workflow be exported for later review?

## Core Workflow

```text
Log → Trace → Flag Risk → Review → Approve → Export
```

AgentLedger is framework-agnostic. It can be used with custom Python agents, OpenAI workflows, LangChain, CrewAI, AutoGen, or other agent systems because it records structured workflow events instead of depending on a specific model provider.

## Install

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the package locally:

```bash
pip install -e .
```

Run the test suite:

```bash
pytest -q
```

## Quickstart

```python
from agentledger import AgentLedger

ledger = AgentLedger()

trace = ledger.create_trace(
    workflow="example_workflow",
    agent_name="ExampleAgent",
    entity_id="example_001",
    metadata={"environment": "demo"},
)

ledger.log_decision(
    agent_name="ExampleAgent",
    input_data={"request": "evaluate example workflow"},
    output_data={"decision": "approve"},
    reason_codes=["MEETS_EXAMPLE_CRITERIA"],
    trace_id=trace["trace_id"],
    risk_level="low",
    review_required=False,
    policy_status="pass",
    approval_status="approved",
)

ledger.complete_trace(
    trace_id=trace["trace_id"],
    outcome="approved",
    approval_status="approved",
)

audit_record = ledger.export_trace(trace["trace_id"])

print(audit_record["summary"])
```

Run the included quickstart:

```bash
python3 -m examples.quickstart
```

## Underwriting Audit Demo

The underwriting demo shows an AI-agent workflow that:

1. Creates a trace for a loan application.
2. Logs income-verification and credit-report tool calls.
3. Records a manual-review decision.
4. Captures risk, policy, and approval data.
5. Completes the trace.
6. Exports a complete audit record.

Run it with:

```bash
python3 -m examples.underwriting_audit_demo
```

## Core API

### Create a trace

```python
trace = ledger.create_trace(
    workflow="heloc_underwriting",
    agent_name="UnderwritingAgent",
    entity_id="application_123",
    metadata={"environment": "demo"},
)
```

### Log a tool call

```python
ledger.log_tool_call(
    agent_name="UnderwritingAgent",
    tool_name="income_verification_api",
    input_data={"application_id": "application_123"},
    output_data={"status": "partial"},
    trace_id=trace["trace_id"],
)
```

### Log a decision with review controls

```python
ledger.log_decision(
    agent_name="UnderwritingAgent",
    output_data={"decision": "manual_review"},
    reason_codes=["INCOME_DOCUMENTATION_INCOMPLETE"],
    trace_id=trace["trace_id"],
    risk_level="high",
    review_required=True,
    review_reason="Income documentation is incomplete.",
    policy_status="warning",
    approval_status="pending",
)
```

Allowed values:

```text
risk_level:
low, medium, high, critical

policy_status:
pass, warning, fail, not_evaluated

approval_status:
not_required, pending, approved, rejected
```

### Complete and export a trace

```python
ledger.complete_trace(
    trace_id=trace["trace_id"],
    outcome="manual_review_required",
    approval_status="pending",
)

trace_record = ledger.get_trace(trace["trace_id"])
audit_record = ledger.export_trace(trace["trace_id"])
```

`export_trace()` returns:

```text
Trace metadata
+ ordered workflow events
+ final outcome and approval status
+ event counts
+ review-required signal
+ highest risk level
```

## Legacy Event Queries and Exports

```python
all_events = ledger.list_events()
decision_events = ledger.get_events_by_type("decision")
agent_events = ledger.get_events_by_agent("UnderwritingAgent")
trace_events = ledger.get_events_by_trace(trace["trace_id"])

ledger.export_json("audit_events.json")
ledger.export_csv("audit_events.csv")
ledger.export_markdown_report("audit_report.md")
```

## Project Structure

```text
agentledger/
    ledger.py
    events.py
    storage.py

examples/
    quickstart.py
    underwriting_audit_demo.py

tests/
README.md
pyproject.toml
```

## Current Scope

AgentLedger v0.3.0 is a local SDK MVP for structured AI-agent accountability records.

Included:

* Local JSONL event storage
* Persistent trace records
* Tool-call and decision logging
* Risk, review, policy, and approval fields
* Trace lifecycle management
* JSON-compatible audit exports
* Runnable examples
* Automated tests

Not included yet:

* Hosted storage
* Authentication
* Multi-tenant accounts
* Dashboard UI
* Team review queues
* Retention controls
* Compliance certifications
* Legal or regulatory guarantees

## Roadmap

```text
v0.3.0 — Trace, risk, review, approval, and audit-export SDK MVP
v0.3.x — Developer-experience improvements and feedback-driven releases
v0.4.0 — Integrations and stronger storage options
v0.5.0 — Team review workflow and initial UI direction
v1.0.0 — Stable public API validated by real customer usage
```

## Status

MVP SDK. Local-first. Not production-ready.

