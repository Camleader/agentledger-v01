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

Clone the repository and move into the project directory:

git clone https://github.com/Camleader/agentledger-v01.git


After cloning the repository, move into the AgentLedger project folder:

```bash
cd agentledger-v01
```

Confirm you are in the correct directory:

```bash
ls
```

You should see files and folders similar to:

```text
README.md
pyproject.toml
agentledger
tests
```

Only after confirming that `pyproject.toml` is present should you create and activate the virtual environment.


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

## Demo

Watch the end-to-end AgentLedger walkthrough:

[▶ Watch the AgentLedger underwriting audit demo](https://youtu.be/-O0T16owdZU)

This demo shows how to clone the repository, install the SDK, run an underwriting workflow, and generate an exportable audit record.

## v0.3.1 Evidence & Integrity

AgentLedger v0.3.1 adds stronger audit evidence for AI-agent workflows.

New in this release:

* `log_action()` for recording real-world agent actions
* `action_status` for executed, denied, failed, and held-for-review outcomes
* Attribution fields for agent, model, prompt, workflow, and policy versions
* Tamper-evident event records using `prev_hash` and `sha256`
* Offline log integrity checks with `verify_hash_chain()`
* Expanded CSV and Markdown audit exports

## Core API

### Log an action

```python
ledger.log_action(
    agent_name="UnderwritingAgent",
    action_name="request_income_documents",
    input_data={"application_id": "application_123"},
    output_data={"status": "requested"},
    trace_id=trace["trace_id"],
    action_status="held_for_review",
    agent_id="agent_001",
    model_version="gpt-5",
    prompt_version="underwriting_prompt_v1",
    workflow_version="heloc_workflow_v1",
    policy_version="credit_policy_v1",
)

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

## Event Queries, Exports, and Integrity Checks

```python
all_events = ledger.list_events()
decision_events = ledger.get_events_by_type("decision")
agent_events = ledger.get_events_by_agent("UnderwritingAgent")
trace_events = ledger.get_events_by_trace(trace["trace_id"])

integrity_result = ledger.verify_hash_chain()

ledger.export_json("audit_events.json")
ledger.export_csv("audit_events.csv")
ledger.export_markdown_report("audit_report.md")

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

AgentLedger v0.3.1 is a local-first Python SDK for structured AI-agent accountability records.

Included:

* Local JSONL event storage
* Persistent trace records
* Tool-call, decision, and action logging
* Action status tracking
* Risk, review, policy, and approval fields
* Agent, model, prompt, workflow, and policy attribution fields
* Tamper-evident event hashing
* Offline hash-chain verification
* Trace lifecycle management
* JSON, CSV, and Markdown audit exports
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

### Roadmap

```text
v0.3.0 — Trace, risk, review, approval, and audit-export SDK MVP
v0.3.1 — Evidence, attribution, action status, and tamper-evident integrity checks
v0.3.x — Developer-experience improvements and feedback-driven releases
v0.4.0 — Integrations and stronger storage options
v0.5.0 — Team review workflow and initial UI direction
v1.0.0 — Stable public API validated by real customer usage

## Status

MVP SDK. Local-first. Not production-ready.

