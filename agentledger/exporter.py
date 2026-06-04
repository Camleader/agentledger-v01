import json


PRODUCT_VERSION = "v0.1.4"


def build_audit_record(
    run_id,
    created_at,
    selected_demo,
    application_data,
    agent_result,
    risk_flags,
    highest_risk_severity,
    requires_human_review,
    human_review_status,
    reviewed_at,
    trace_events,
):
    return {
        "export_type": "AgentLedger Audit Record",
        "product_version": PRODUCT_VERSION,
        "product": {
            "name": "AgentLedger",
            "version": PRODUCT_VERSION,
            "description": (
                "Traceable, reviewable, exportable audit records for AI agent decisions."
            ),
        },
        "run": {
            "run_id": run_id,
            "created_at": created_at,
            "agent_name": "HELOC Underwriting Agent",
            "workflow": "Log → Trace → Flag risk → Explain → Approve → Export",
            "selected_demo": selected_demo,
        },
        "application": application_data,
        "decision": {
            "recommendation": agent_result["recommendation"],
            "decision_summary": agent_result["decision_summary"],
            "reason_codes": agent_result["reason_codes"],
            "calculations": agent_result["calculations"],
        },
        "risk": {
            "risk_flags": risk_flags,
            "highest_risk_severity": highest_risk_severity,
            "requires_human_review": requires_human_review,
        },
        "human_review": {
            "status": human_review_status,
            "reviewed_at": reviewed_at,
            "reviewer": "Demo User",
        },
        "trace": {
            "event_count": len(trace_events),
            "events": trace_events,
        },
        "compliance_note": {
            "note": (
                "This export is a point-in-time audit record showing agent inputs, "
                "calculations, decision logic, risk flags, human review status, "
                "and trace events."
            )
        },
    }


def export_audit_json(audit_record):
    return json.dumps(audit_record, indent=2, sort_keys=True)
