import json
from pathlib import Path

from agentledger import AgentLedger


AGENT_CONTEXT = {
    "agent_id": "underwriting-agent-demo-001",
    "agent_version": "0.1.0",
    "model_version": "demo-rules-engine",
    "prompt_version": "underwriting_prompt_v1",
    "workflow_version": "heloc_underwriting_v1",
    "policy_version": "credit_policy_v1",
}


def verify_income(application):
    stated_income = application["stated_monthly_income"]
    verified_income = application["verified_monthly_income"]

    return {
        "status": "completed",
        "stated_monthly_income": stated_income,
        "verified_monthly_income": verified_income,
        "income_verified": verified_income >= stated_income * 0.9,
    }


def pull_credit_report(application):
    return {
        "status": "completed",
        "credit_score": application["credit_score"],
        "open_delinquencies": application["open_delinquencies"],
    }


def calculate_underwriting_metrics(application):
    monthly_debt = application["monthly_debt"]
    verified_income = application["verified_monthly_income"]
    property_value = application["property_value"]
    current_mortgage_balance = application["current_mortgage_balance"]
    requested_heloc_amount = application["requested_heloc_amount"]

    dti = monthly_debt / verified_income
    cltv = (current_mortgage_balance + requested_heloc_amount) / property_value

    return {
        "status": "completed",
        "dti": round(dti, 4),
        "cltv": round(cltv, 4),
    }


def make_underwriting_decision(income_result, credit_result, metrics_result):
    reason_codes = []

    if not income_result["income_verified"]:
        reason_codes.append("INCOME_VERIFICATION_GAP")

    if credit_result["credit_score"] < 680:
        reason_codes.append("CREDIT_SCORE_BELOW_STANDARD_THRESHOLD")

    if metrics_result["dti"] > 0.43:
        reason_codes.append("DTI_ABOVE_POLICY_THRESHOLD")

    if metrics_result["cltv"] > 0.85:
        reason_codes.append("CLTV_ABOVE_POLICY_THRESHOLD")

    if reason_codes:
        return {
            "decision": "manual_review",
            "risk_level": "high",
            "review_required": True,
            "review_reason": "Application has policy warnings requiring human review.",
            "policy_status": "warning",
            "approval_status": "pending",
            "action_status": "held_for_review",
            "reason_codes": reason_codes,
        }

    return {
        "decision": "approve",
        "risk_level": "low",
        "review_required": False,
        "review_reason": None,
        "policy_status": "pass",
        "approval_status": "approved",
        "action_status": "executed",
        "reason_codes": ["MEETS_POLICY_THRESHOLDS"],
    }


def run_demo(output_dir="demo_output/end_to_end_agent"):
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    event_log_path = output_path / "events.jsonl"
    trace_log_path = output_path / "traces.jsonl"
    json_export_path = output_path / "events_export.json"
    csv_export_path = output_path / "events_export.csv"
    markdown_export_path = output_path / "audit_report.md"
    trace_export_path = output_path / "trace_audit_record.json"

    for path in [
        event_log_path,
        trace_log_path,
        json_export_path,
        csv_export_path,
        markdown_export_path,
        trace_export_path,
    ]:
        if path.exists():
            path.unlink()

    ledger = AgentLedger(
        storage_path=str(event_log_path),
        trace_storage_path=str(trace_log_path),
    )

    application = {
        "application_id": "heloc_app_1001",
        "borrower_type": "demo_customer",
        "stated_monthly_income": 9200,
        "verified_monthly_income": 7900,
        "monthly_debt": 3650,
        "credit_score": 665,
        "open_delinquencies": 0,
        "property_value": 620000,
        "current_mortgage_balance": 410000,
        "requested_heloc_amount": 145000,
    }

    trace = ledger.create_trace(
        workflow="heloc_underwriting",
        agent_name="AI Agent Underwriting Assistant",
        entity_id=application["application_id"],
        metadata={
            "environment": "local_end_to_end_demo",
            "task": "Evaluate HELOC application and produce audit evidence.",
        },
    )

    ledger.log_action(
        agent_name="AI Agent Underwriting Assistant",
        action_name="receive_underwriting_task",
        input_data={"task": "Evaluate HELOC application."},
        output_data={
            "application_id": application["application_id"],
            "accepted": True,
        },
        trace_id=trace["trace_id"],
        action_status="executed",
        reason_codes=["TASK_ACCEPTED"],
        **AGENT_CONTEXT,
    )

    income_result = verify_income(application)
    ledger.log_tool_call(
        agent_name="AI Agent Underwriting Assistant",
        tool_name="income_verification_tool",
        input_data={
            "application_id": application["application_id"],
            "stated_monthly_income": application["stated_monthly_income"],
        },
        output_data=income_result,
        trace_id=trace["trace_id"],
        action_status="executed",
        **AGENT_CONTEXT,
    )

    credit_result = pull_credit_report(application)
    ledger.log_tool_call(
        agent_name="AI Agent Underwriting Assistant",
        tool_name="credit_report_tool",
        input_data={"application_id": application["application_id"]},
        output_data=credit_result,
        trace_id=trace["trace_id"],
        action_status="executed",
        **AGENT_CONTEXT,
    )

    metrics_result = calculate_underwriting_metrics(application)
    ledger.log_tool_call(
        agent_name="AI Agent Underwriting Assistant",
        tool_name="underwriting_metrics_calculator",
        input_data={
            "verified_monthly_income": application["verified_monthly_income"],
            "monthly_debt": application["monthly_debt"],
            "property_value": application["property_value"],
            "current_mortgage_balance": application["current_mortgage_balance"],
            "requested_heloc_amount": application["requested_heloc_amount"],
        },
        output_data=metrics_result,
        trace_id=trace["trace_id"],
        action_status="executed",
        **AGENT_CONTEXT,
    )

    decision = make_underwriting_decision(
        income_result=income_result,
        credit_result=credit_result,
        metrics_result=metrics_result,
    )

    ledger.log_decision(
        agent_name="AI Agent Underwriting Assistant",
        input_data={
            "income_result": income_result,
            "credit_result": credit_result,
            "metrics_result": metrics_result,
        },
        output_data={"decision": decision["decision"]},
        reason_codes=decision["reason_codes"],
        trace_id=trace["trace_id"],
        risk_level=decision["risk_level"],
        review_required=decision["review_required"],
        review_reason=decision["review_reason"],
        policy_status=decision["policy_status"],
        approval_status=decision["approval_status"],
        action_status=decision["action_status"],
        **AGENT_CONTEXT,
    )

    ledger.log_action(
        agent_name="AI Agent Underwriting Assistant",
        action_name="route_to_human_review_queue",
        input_data={
            "application_id": application["application_id"],
            "decision": decision["decision"],
        },
        output_data={
            "queue": "senior_underwriter_review",
            "status": "queued",
        },
        trace_id=trace["trace_id"],
        action_status="held_for_review",
        reason_codes=decision["reason_codes"],
        **AGENT_CONTEXT,
    )

    completed_trace = ledger.complete_trace(
        trace_id=trace["trace_id"],
        outcome="manual_review_required",
        approval_status="pending",
    )

    events = ledger.get_events_by_trace(trace["trace_id"])
    audit_record = ledger.export_trace(trace["trace_id"])
    hash_check = ledger.verify_hash_chain()
    trace_hash_check = ledger.trace_storage.verify_hash_chain()

    ledger.export_json(json_export_path, events=events)
    ledger.export_csv(csv_export_path, events=events)
    ledger.export_markdown_report(markdown_export_path, events=events)
    trace_export_path.write_text(
        json.dumps(audit_record, indent=2),
        encoding="utf-8",
    )

    checklist = {
        "1_agent_received_tasks": events[0]["metadata"]["action_name"] == "receive_underwriting_task",
        "2_agent_called_tools_or_made_decisions": any(
            event["event_type"] == "tool_call" for event in events
        ) and any(event["event_type"] == "decision" for event in events),
        "3_agentledger_recorded_actions": any(
            event["event_type"] == "action" for event in events
        ),
        "4_agent_completed_workflow": completed_trace["status"] == "completed",
        "5_records_can_be_inspected": len(events) == audit_record["summary"]["event_count"],
        "6_records_can_be_exported": all(
            path.exists()
            for path in [json_export_path, csv_export_path, markdown_export_path, trace_export_path]
        ),
        "7_hash_chains_verify": (
            hash_check["valid"] is True and trace_hash_check["valid"] is True
        ),
    }

    result = {
        "trace_id": trace["trace_id"],
        "final_decision": decision["decision"],
        "review_required": decision["review_required"],
        "reason_codes": decision["reason_codes"],
        "summary": audit_record["summary"],
        "hash_check": hash_check,
        "trace_hash_check": trace_hash_check,
        "checklist": checklist,
        "exports": {
            "event_log": str(event_log_path),
            "trace_log": str(trace_log_path),
            "json": str(json_export_path),
            "csv": str(csv_export_path),
            "markdown": str(markdown_export_path),
            "trace_audit_record": str(trace_export_path),
        },
    }

    return result


if __name__ == "__main__":
    print(json.dumps(run_demo(), indent=2))
