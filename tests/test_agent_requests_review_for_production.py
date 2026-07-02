from __future__ import annotations

from gcr_agent import GovernedAgent


def test_production_deploy_requests_review_and_does_not_execute() -> None:
    result = GovernedAgent().handle_request("Deploy payment-service to production")

    assert result["proposal"]["consequence_class"] == "PRODUCTION_STATE_CHANGE"
    assert result["envelope"]["decision"] == "REQUEST_REVIEW"
    assert result["envelope"]["execution_status"] == "NOT_EXECUTED"
    assert result["envelope"]["outcome_status"] == "PENDING_REVIEW"
    assert result["receipt"]["decision"] == "REQUEST_REVIEW"
