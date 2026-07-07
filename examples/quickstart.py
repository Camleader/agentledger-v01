import json
from pathlib import Path

from agentledger import AgentLedger


def run_quickstart(event_log_path, trace_log_path):
    ledger = AgentLedger(
        storage_path=str(event_log_path),
        trace_storage_path=str(trace_log_path),
    )

    trace = ledger.create_trace(
        workflow="example_workflow",
        agent_name="ExampleAgent",
        entity_id="example_001",
        metadata={"environment": "quickstart"},
    )

    ledger.log_decision(
        agent_name="ExampleAgent",
        input_data={"request": "evaluate example workflow"},
        output_data={"decision": "approve"},
        reason_codes=["MEETS_EXAMPLE_CRITERIA"],
        trace_id=trace["trace_id"],
        risk_level="low",
        review_required=False,
        review_reason=None,
        policy_status="pass",
        approval_status="approved",
    )

    ledger.complete_trace(
        trace_id=trace["trace_id"],
        outcome="approved",
        approval_status="approved",
    )

    return ledger.export_trace(trace["trace_id"])


if __name__ == "__main__":
    output_dir = Path("demo_output")
    output_dir.mkdir(exist_ok=True)

    audit_record = run_quickstart(
        event_log_path=output_dir / "quickstart_events.jsonl",
        trace_log_path=output_dir / "quickstart_traces.jsonl",
    )

    print(json.dumps(audit_record, indent=2))