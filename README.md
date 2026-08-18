# AgentLedger

AgentLedger is a lightweight Python evidence layer for AI-agent workflows. It records what an agent did, when it did it, which tools and decisions were involved, what workflow context was attached, and whether the resulting records still verify afterward.

## Run the official demo in 60 seconds

Requirements: Python 3.9 or newer and Git.

```bash
git clone https://github.com/Camleader/agentledger-v01.git
cd agentledger-v01
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
python -m examples.end_to_end_agent_demo
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

A successful run prints a manual-review result with:

- 6 ordered events
- 3 tool calls
- 1 decision
- 4 reason codes
- A valid six-record event hash chain
- A valid one-record trace hash chain
- Seven successful demo checks

Inspect these generated files:

- `demo_output/end_to_end_agent/trace_audit_record.json` — the completed trace and all six events
- `demo_output/end_to_end_agent/audit_report.md` — a readable event-by-event report
- `demo_output/end_to_end_agent/events_export.json` — portable structured events
- `demo_output/end_to_end_agent/events_export.csv` — spreadsheet-friendly events
- `demo_output/end_to_end_agent/events.jsonl` — raw hash-linked event records
- `demo_output/end_to_end_agent/traces.jsonl` — raw hash-linked trace records

Run the automated checks:

```bash
python -m pytest -q
```

## What the demo shows

The deterministic HELOC underwriting demo:

1. Receives an application-review task.
2. Records an income-verification tool call.
3. Records a credit-report tool call.
4. Records an underwriting-metrics tool call.
5. Records a high-risk manual-review decision with reason codes.
6. Records routing the application to a human-review queue.
7. Completes and exports the trace.
8. Verifies both hash chains.

The mock tools keep the demo local and repeatable. Running it again replaces its prior output, so the result remains exactly six events instead of accumulating records.

## How AgentLedger Works

1. Your application or agent starts a trace for one workflow.
2. It logs actions, tool calls, and decisions as the workflow runs.
3. AgentLedger stores ordered evidence records linked with `prev_hash` and `sha256`.
4. Your application completes the trace with its outcome and approval status.
5. The records can be queried, exported, and checked for later modification.

AgentLedger does not replace or run the agent, determine whether the agent's claims are true, enforce policy, or provide compliance certification. It records the evidence supplied by the workflow and makes later record modification detectable.

A valid hash chain means the stored records are internally consistent at verification time. It does not independently prove that the original inputs were accurate.

## Minimal SDK example

```python
from agentledger import AgentLedger

ledger = AgentLedger(
    storage_path="events.jsonl",
    trace_storage_path="traces.jsonl",
)

trace = ledger.create_trace(
    workflow="example_workflow",
    agent_name="ExampleAgent",
    entity_id="example_001",
    metadata={"environment": "demo"},
)

ledger.log_action(
    agent_name="ExampleAgent",
    action_name="receive_task",
    input_data={"task": "Evaluate request"},
    output_data={"accepted": True},
    trace_id=trace["trace_id"],
)

ledger.log_decision(
    agent_name="ExampleAgent",
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
integrity_result = ledger.verify_hash_chain()

print(audit_record["summary"])
print(integrity_result)
```

## Core API

### Traces

- `create_trace()` starts a persistent workflow record.
- `get_trace()` returns a trace and its related events.
- `complete_trace()` records the outcome, approval status, and completion time.
- `export_trace()` returns the trace, ordered events, and summary counts.

### Events

- `log_action()` records an agent action and its status.
- `log_tool_call()` records a tool name, inputs, and outputs.
- `log_decision()` records the decision, reasons, risk, review, policy, and approval fields.
- `log_event()` provides the generic event interface.

Supported decision fields include:

```text
risk_level: low, medium, high, critical
policy_status: pass, warning, fail, not_evaluated
approval_status: not_required, pending, approved, rejected
```

Supported action statuses include `executed`, `denied`, `failed`, and `held_for_review`.

### Queries, exports, and verification

```python
all_events = ledger.list_events()
decision_events = ledger.get_events_by_type("decision")
agent_events = ledger.get_events_by_agent("ExampleAgent")
trace_events = ledger.get_events_by_trace(trace["trace_id"])

ledger.export_json("audit_events.json")
ledger.export_csv("audit_events.csv")
ledger.export_markdown_report("audit_report.md")

integrity_result = ledger.verify_hash_chain()
```

Exports contain attribution fields for agent, model, prompt, workflow, and policy versions when the calling workflow supplies them.

## Included examples

| Example | Purpose | Command |
|---|---|---|
| End-to-end agent demo | Official six-event workflow, exports, and verification | `python -m examples.end_to_end_agent_demo` |
| Quickstart | Minimal trace and decision | `python -m examples.quickstart` |
| Underwriting audit demo | Compact three-event SDK example | `python -m examples.underwriting_audit_demo` |

## Project structure

```text
agentledger/
    __init__.py
    events.py
    ledger.py
    storage.py

examples/
    __init__.py
    end_to_end_agent_demo.py
    quickstart.py
    underwriting_audit_demo.py

tests/
CHANGELOG.md
DEMO_SCRIPT.md
README.md
pyproject.toml
```

## Current scope

AgentLedger v0.3.2 is a local-first Python SDK.

Included:

- Local JSONL event and trace storage
- Action, tool-call, and decision logging
- Risk, review, policy, approval, and attribution fields
- Trace lifecycle management
- JSON, CSV, Markdown, and trace-level exports
- Tamper-evident event and trace hash chains
- Offline integrity verification
- Runnable, tested examples

Not included:

- Hosted storage or a SaaS backend
- Authentication or multi-tenant accounts
- Dashboard or team review queues
- Broad third-party integrations
- Retention controls
- Compliance certification or legal guarantees

## Status

Developer-preview SDK. Local-first. Not production-ready.
