import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from agentledger.decision_agent import run_heloc_agent


def base_application(**overrides):
    application = {
        "borrower_name": "Alex Rivera",
        "credit_score": 720,
        "annual_income": 120000,
        "existing_monthly_debt": 3000,
        "home_value": 500000,
        "mortgage_balance": 300000,
        "requested_heloc_amount": 75000,
        "employment_type": "W2",
        "income_documentation_status": "Verified",
    }
    application.update(overrides)
    return application


def test_approve_case():
    result = run_heloc_agent(base_application())

    assert result["recommendation"] == "Approve"
    assert "MEETS_AUTOMATED_APPROVAL_CRITERIA" in result["reason_codes"]
    assert result["calculations"]["cltv"] == 75.0
    assert result["calculations"]["dti"] == 30.0


def test_manual_review_because_of_high_cltv():
    result = run_heloc_agent(
        base_application(mortgage_balance=365000, requested_heloc_amount=50000)
    )

    assert result["recommendation"] == "Manual Review"
    assert "CLTV_REQUIRES_REVIEW" in result["reason_codes"]


def test_manual_review_because_of_missing_income_docs():
    result = run_heloc_agent(base_application(income_documentation_status="Missing"))

    assert result["recommendation"] == "Manual Review"
    assert "INCOME_DOCUMENTATION_INCOMPLETE" in result["reason_codes"]


def test_decline_because_credit_score_is_too_low():
    result = run_heloc_agent(base_application(credit_score=610))

    assert result["recommendation"] == "Decline"
    assert "CREDIT_SCORE_BELOW_MINIMUM" in result["reason_codes"]


def test_demo_presets_produce_expected_recommendations():
    presets = [
        (
            "Approve",
            {
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
        ),
        (
            "Manual Review",
            {
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
        ),
        (
            "Decline",
            {
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
        ),
    ]

    for expected_recommendation, preset in presets:
        result = run_heloc_agent(preset)
        assert result["recommendation"] == expected_recommendation
