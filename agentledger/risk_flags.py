def highest_risk_severity(risk_flags):
    severities = {flag["severity"] for flag in risk_flags}
    if "high" in severities:
        return "high"
    if "medium" in severities:
        return "medium"
    return "low"


def requires_human_review(agent_result, risk_flags):
    recommendation = agent_result["recommendation"]
    return (
        recommendation in {"Manual Review", "Decline"}
        or highest_risk_severity(risk_flags) == "high"
    )


def evaluate_risk_flags(application_data, agent_result):
    flags = []
    calculations = agent_result["calculations"]
    recommendation = agent_result["recommendation"]

    if calculations["cltv"] > 80:
        severity = "high" if calculations["cltv"] > 90 else "medium"
        flags.append(
            {
                "flag_name": "High CLTV",
                "severity": severity,
                "explanation": f"Combined loan-to-value is {calculations['cltv']}%.",
            }
        )

    if calculations["dti"] > 43:
        flags.append(
            {
                "flag_name": "High DTI",
                "severity": "medium",
                "explanation": f"Debt-to-income ratio is {calculations['dti']}%.",
            }
        )

    if int(application_data["credit_score"]) < 620:
        flags.append(
            {
                "flag_name": "Low credit score",
                "severity": "high",
                "explanation": "Credit score is below the automated underwriting minimum.",
            }
        )

    if application_data["income_documentation_status"] == "Missing":
        flags.append(
            {
                "flag_name": "Missing income documentation",
                "severity": "high",
                "explanation": "Income documentation is missing and requires human review.",
            }
        )
    elif application_data["income_documentation_status"] == "Partial":
        flags.append(
            {
                "flag_name": "Missing income documentation",
                "severity": "medium",
                "explanation": "Income documentation is partial and requires human review.",
            }
        )

    if recommendation == "Manual Review":
        flags.append(
            {
                "flag_name": "Manual review required",
                "severity": "medium",
                "explanation": "One or more underwriting rules require a reviewer.",
            }
        )

    if recommendation == "Decline":
        flags.append(
            {
                "flag_name": "Decline decision",
                "severity": "high",
                "explanation": "Application failed a decline threshold.",
            }
        )

    return flags
