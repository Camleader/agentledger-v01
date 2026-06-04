def _round_percent(value):
    return round(value, 2)


def run_heloc_agent(application_data):
    """Run a deterministic HELOC underwriting simulation."""
    credit_score = int(application_data["credit_score"])
    annual_income = float(application_data["annual_income"])
    existing_monthly_debt = float(application_data["existing_monthly_debt"])
    home_value = float(application_data["home_value"])
    mortgage_balance = float(application_data["mortgage_balance"])
    requested_heloc_amount = float(application_data["requested_heloc_amount"])
    income_docs = application_data["income_documentation_status"]

    cltv = (
        ((mortgage_balance + requested_heloc_amount) / home_value) * 100
        if home_value > 0
        else 999.0
    )
    gross_monthly_income = annual_income / 12 if annual_income > 0 else 0
    dti = (
        (existing_monthly_debt / gross_monthly_income) * 100
        if gross_monthly_income > 0
        else 999.0
    )

    reason_codes = []
    recommendation = "Approve"

    if credit_score < 620:
        recommendation = "Decline"
        reason_codes.append("CREDIT_SCORE_BELOW_MINIMUM")
    if cltv > 90:
        recommendation = "Decline"
        reason_codes.append("CLTV_ABOVE_MAXIMUM")

    if recommendation != "Decline":
        if cltv > 80:
            recommendation = "Manual Review"
            reason_codes.append("CLTV_REQUIRES_REVIEW")
        if dti > 43:
            recommendation = "Manual Review"
            reason_codes.append("DTI_REQUIRES_REVIEW")
        if income_docs in {"Partial", "Missing"}:
            recommendation = "Manual Review"
            reason_codes.append("INCOME_DOCUMENTATION_INCOMPLETE")

    if recommendation == "Approve":
        reason_codes.append("MEETS_AUTOMATED_APPROVAL_CRITERIA")

    calculations = {
        "cltv": _round_percent(cltv),
        "dti": _round_percent(dti),
        "gross_monthly_income": round(gross_monthly_income, 2),
    }

    decision_summary = (
        f"{recommendation}: credit score {credit_score}, CLTV {calculations['cltv']}%, "
        f"DTI {calculations['dti']}%, income documentation {income_docs}."
    )

    return {
        "recommendation": recommendation,
        "reason_codes": reason_codes,
        "calculations": calculations,
        "decision_summary": decision_summary,
    }
