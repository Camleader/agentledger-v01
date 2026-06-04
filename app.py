from datetime import datetime, timezone
from uuid import uuid4

import streamlit as st

from agentledger.decision_agent import run_heloc_agent
from agentledger.exporter import build_audit_record, export_audit_json
from agentledger.ledger import AgentLedger
from agentledger.risk_flags import (
    evaluate_risk_flags,
    highest_risk_severity,
    requires_human_review,
)


PRODUCT_NAME = "AgentLedger"
PRODUCT_VERSION = "v0.1.4"
AGENT_NAME = "HELOC Underwriting Agent"
WORKFLOW = "Log → Trace → Flag risk → Explain → Approve → Export"
EMPLOYMENT_OPTIONS = ["W2", "Self-employed", "Retired"]
INCOME_DOC_OPTIONS = ["Verified", "Partial", "Missing"]

DEFAULT_FORM_VALUES = {
    "borrower_name": "",
    "credit_score": 680,
    "annual_income": 100000,
    "existing_monthly_debt": 2500,
    "home_value": 500000,
    "mortgage_balance": 300000,
    "requested_heloc_amount": 50000,
    "employment_type": "W2",
    "income_documentation_status": "Verified",
}

DEMO_PRESETS = {
    "Approve Demo": {
        "borrower_name": "Alex Approved",
        "credit_score": 720,
        "annual_income": 120000,
        "existing_monthly_debt": 2500,
        "home_value": 600000,
        "mortgage_balance": 350000,
        "requested_heloc_amount": 75000,
        "employment_type": "W2",
        "income_documentation_status": "Verified",
    },
    "Manual Review Demo": {
        "borrower_name": "Morgan Review",
        "credit_score": 665,
        "annual_income": 85000,
        "existing_monthly_debt": 4200,
        "home_value": 500000,
        "mortgage_balance": 390000,
        "requested_heloc_amount": 50000,
        "employment_type": "Self-employed",
        "income_documentation_status": "Partial",
    },
    "Decline Demo": {
        "borrower_name": "Jordan Decline",
        "credit_score": 590,
        "annual_income": 90000,
        "existing_monthly_debt": 2500,
        "home_value": 500000,
        "mortgage_balance": 300000,
        "requested_heloc_amount": 50000,
        "employment_type": "W2",
        "income_documentation_status": "Verified",
    },
}


def risk_level_for_flags(flags):
    severities = {flag["severity"] for flag in flags}
    if "high" in severities:
        return "high"
    if "medium" in severities:
        return "medium"
    return "low"


def clear_previous_run():
    for key in [
        "run_id",
        "application_data",
        "ledger",
        "agent_result",
        "risk_flags",
        "approval_action",
    ]:
        st.session_state.pop(key, None)
    st.session_state["review_status"] = "Pending Human Review"
    st.session_state["reviewed_at"] = None
    st.session_state["export_event_logged"] = False


def load_form_values(values, selected_demo):
    for key, value in values.items():
        st.session_state[key] = value
    st.session_state["selected_demo"] = selected_demo
    clear_previous_run()


def initialize_demo_state():
    for key, value in DEFAULT_FORM_VALUES.items():
        st.session_state.setdefault(key, value)
    st.session_state.setdefault("selected_demo", "None")
    st.session_state.setdefault("review_status", "Pending Human Review")
    st.session_state.setdefault("reviewed_at", None)
    st.session_state.setdefault("export_event_logged", False)


def build_audit(application_data):
    ledger = AgentLedger()
    run_id = str(uuid4())

    ledger.log_event(
        "Log",
        "Received HELOC application",
        {"run_id": run_id, "borrower_application": application_data},
        {"status": "application_logged"},
    )

    agent_result = run_heloc_agent(application_data)
    ledger.log_event(
        "Trace",
        "Ran HELOC underwriting agent",
        application_data,
        agent_result,
        risk_level="medium" if agent_result["recommendation"] == "Manual Review" else "low",
    )

    risk_flags = evaluate_risk_flags(application_data, agent_result)
    ledger.log_event(
        "Flag risk",
        "Evaluated underwriting risk flags",
        {"application": application_data, "agent_result": agent_result},
        {"risk_flags": risk_flags},
        risk_level=risk_level_for_flags(risk_flags),
    )

    ledger.log_event(
        "Explain",
        "Generated decision explanation",
        agent_result,
        {
            "summary": agent_result["decision_summary"],
            "reason_codes": agent_result["reason_codes"],
        },
        risk_level=risk_level_for_flags(risk_flags),
    )

    return run_id, ledger, agent_result, risk_flags


def build_export_record():
    agent_result = st.session_state["agent_result"]
    risk_flags = st.session_state["risk_flags"]
    return build_audit_record(
        run_id=st.session_state["run_id"],
        created_at=datetime.now(timezone.utc).isoformat(),
        selected_demo=st.session_state["selected_demo"],
        application_data=st.session_state["application_data"],
        agent_result=agent_result,
        risk_flags=risk_flags,
        highest_risk_severity=highest_risk_severity(risk_flags),
        requires_human_review=requires_human_review(agent_result, risk_flags),
        human_review_status=st.session_state["review_status"],
        reviewed_at=st.session_state["reviewed_at"],
        trace_events=st.session_state["ledger"].get_trace(),
    )


def ensure_export_event():
    if not st.session_state.get("export_event_logged"):
        st.session_state["ledger"].log_event(
            "Export",
            "Made audit record available for JSON export",
            {"run_id": st.session_state["run_id"]},
            {"export_type": "AgentLedger Audit Record", "format": "json"},
        )
        st.session_state["export_event_logged"] = True


st.set_page_config(page_title=f"{PRODUCT_NAME} {PRODUCT_VERSION}", layout="wide")
initialize_demo_state()

with st.sidebar:
    st.subheader("Product")
    st.write(PRODUCT_NAME)
    st.write(f"Version: {PRODUCT_VERSION}")
    st.write(f"Demo: {AGENT_NAME}")
    st.write(f"Workflow: {WORKFLOW}")
    st.write("Status: Local Demo")
    st.subheader("Pricing concept")
    st.write("Pro: $49/month")
    st.write("Team: $299/month")

st.title(f"{PRODUCT_NAME} {PRODUCT_VERSION}")
st.caption("Prove what your AI agent did.")
st.write(
    "AgentLedger is an audit and approval layer for AI agents operating in "
    "regulated workflows."
)
st.write(
    "It helps AI builders generate traceable, reviewable, and exportable audit "
    "records for agent decisions."
)
st.write(f"Core workflow: {WORKFLOW}")
st.write(f"First demo: {AGENT_NAME}")
st.write(
    "Target buyer: AI startups selling into fintech and regulated enterprise customers."
)

st.subheader("What this demo proves")
st.write("- Agent activity can be logged")
st.write("- Agent decisions can be traced")
st.write("- Risk can be flagged automatically")
st.write("- Reason codes can explain outcomes")
st.write("- Human approval can be captured")
st.write("- Audit records can be exported")

st.subheader(f"Demo: {AGENT_NAME}")
st.write(f"This sample agent follows the full workflow: {WORKFLOW}.")

st.subheader("Demo Presets")
st.write(
    "Load a sample borrower scenario to quickly demonstrate how AgentLedger captures "
    "decisions, risk flags, explanations, approvals, and exportable audit records."
)
preset_cols = st.columns(4)
if preset_cols[0].button("Load Approve Demo", use_container_width=True):
    load_form_values(DEMO_PRESETS["Approve Demo"], "Approve Demo")
if preset_cols[1].button("Load Manual Review Demo", use_container_width=True):
    load_form_values(DEMO_PRESETS["Manual Review Demo"], "Manual Review Demo")
if preset_cols[2].button("Load Decline Demo", use_container_width=True):
    load_form_values(DEMO_PRESETS["Decline Demo"], "Decline Demo")
if preset_cols[3].button("Clear Form", use_container_width=True):
    load_form_values(DEFAULT_FORM_VALUES, "None")

st.info(f"Selected demo: {st.session_state['selected_demo']}")

with st.form("heloc_application"):
    st.subheader("Borrower application")

    left, right = st.columns(2)
    with left:
        borrower_name = st.text_input("Borrower name", key="borrower_name")
        credit_score = st.number_input(
            "Credit score", min_value=300, max_value=850, key="credit_score"
        )
        annual_income = st.number_input(
            "Annual income", min_value=0, step=5000, format="%d", key="annual_income"
        )
        existing_monthly_debt = st.number_input(
            "Existing monthly debt",
            min_value=0,
            step=100,
            format="%d",
            key="existing_monthly_debt",
        )
        employment_type = st.selectbox(
            "Employment type",
            EMPLOYMENT_OPTIONS,
            key="employment_type",
        )

    with right:
        home_value = st.number_input(
            "Home value", min_value=1, step=10000, format="%d", key="home_value"
        )
        mortgage_balance = st.number_input(
            "Mortgage balance", min_value=0, step=10000, format="%d", key="mortgage_balance"
        )
        requested_heloc_amount = st.number_input(
            "Requested HELOC amount",
            min_value=0,
            step=5000,
            format="%d",
            key="requested_heloc_amount",
        )
        income_documentation_status = st.selectbox(
            "Income documentation status",
            INCOME_DOC_OPTIONS,
            key="income_documentation_status",
        )

    run_agent = st.form_submit_button("Run HELOC Agent", type="primary")

if run_agent:
    application_data = {
        "borrower_name": st.session_state["borrower_name"],
        "credit_score": st.session_state["credit_score"],
        "annual_income": st.session_state["annual_income"],
        "existing_monthly_debt": st.session_state["existing_monthly_debt"],
        "home_value": st.session_state["home_value"],
        "mortgage_balance": st.session_state["mortgage_balance"],
        "requested_heloc_amount": st.session_state["requested_heloc_amount"],
        "employment_type": st.session_state["employment_type"],
        "income_documentation_status": st.session_state["income_documentation_status"],
    }

    run_id, ledger, agent_result, risk_flags = build_audit(application_data)
    st.session_state["run_id"] = run_id
    st.session_state["application_data"] = application_data
    st.session_state["ledger"] = ledger
    st.session_state["agent_result"] = agent_result
    st.session_state["risk_flags"] = risk_flags
    st.session_state["approval_action"] = None
    st.session_state["review_status"] = "Pending Human Review"
    st.session_state["reviewed_at"] = None
    st.session_state["export_event_logged"] = False

if "agent_result" in st.session_state:
    ledger = st.session_state["ledger"]
    agent_result = st.session_state["agent_result"]
    risk_flags = st.session_state["risk_flags"]
    highest_severity = highest_risk_severity(risk_flags)

    st.divider()
    rec = agent_result["recommendation"]
    if rec == "Approve":
        st.success(f"Final recommendation: {rec}")
    elif rec == "Manual Review":
        st.warning(f"Final recommendation: {rec}")
    else:
        st.error(f"Final recommendation: {rec}")

    st.subheader("Run Summary")
    summary = {
        "Agent": AGENT_NAME,
        "Workflow": WORKFLOW,
        "Decision": rec,
        "Human Review Status": st.session_state["review_status"],
        "Audit Export": "Available",
    }
    st.table(summary)

    metric_cols = st.columns(3)
    metric_cols[0].metric("CLTV", f"{agent_result['calculations']['cltv']}%")
    metric_cols[1].metric("DTI", f"{agent_result['calculations']['dti']}%")
    metric_cols[2].metric(
        "Gross monthly income", f"${agent_result['calculations']['gross_monthly_income']:,.2f}"
    )

    left, right = st.columns([1, 1])
    with left:
        st.subheader("Reason codes")
        for code in agent_result["reason_codes"]:
            st.write(f"- {code}")

        st.subheader("Risk flags")
        if risk_flags:
            st.dataframe(risk_flags, use_container_width=True, hide_index=True)
        else:
            st.write("No risk flags.")

    with right:
        st.subheader("Decision explanation")
        st.write(agent_result["decision_summary"])

        st.subheader("Approval controls")
        approve_col, reject_col = st.columns(2)
        if approve_col.button("Approve Agent Decision", use_container_width=True):
            st.session_state["review_status"] = "Approved"
            st.session_state["reviewed_at"] = datetime.now(timezone.utc).isoformat()
            event = ledger.log_event(
                "Approve",
                "Reviewer approved agent decision",
                {"recommendation": rec},
                {
                    "human_review_status": "Approved",
                    "reviewed_at": st.session_state["reviewed_at"],
                },
            )
            st.session_state["approval_action"] = event
            st.session_state["export_event_logged"] = False
            st.rerun()
        if reject_col.button("Reject Agent Decision", use_container_width=True):
            st.session_state["review_status"] = "Rejected"
            st.session_state["reviewed_at"] = datetime.now(timezone.utc).isoformat()
            event = ledger.log_event(
                "Approve",
                "Reviewer rejected agent decision",
                {"recommendation": rec},
                {
                    "human_review_status": "Rejected",
                    "reviewed_at": st.session_state["reviewed_at"],
                },
                risk_level="medium",
            )
            st.session_state["approval_action"] = event
            st.session_state["export_event_logged"] = False
            st.rerun()

        st.info(f"Current review status: {st.session_state['review_status']}")

    ensure_export_event()
    st.subheader("Chronological trace log")
    st.dataframe(ledger.get_trace(), use_container_width=True, hide_index=True)

    audit_record = build_export_record()
    audit_json = export_audit_json(audit_record)

    st.subheader("Audit Export Preview")
    preview = {
        "Run ID": st.session_state["run_id"],
        "Agent": AGENT_NAME,
        "Decision": rec,
        "Highest Risk Severity": highest_severity,
        "Human Review Status": st.session_state["review_status"],
        "Event Count": audit_record["trace"]["event_count"],
    }
    st.table(preview)

    st.download_button(
        "Export audit record as JSON",
        data=audit_json,
        file_name=f"agentledger_audit_record_{st.session_state['run_id']}.json",
        mime="application/json",
    )
    with st.expander("View Full Audit JSON"):
        st.code(audit_json, language="json")
