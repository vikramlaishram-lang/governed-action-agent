from __future__ import annotations

from gcr_agent import GovernedAgent


def test_m4_missing_token_keeps_request_review() -> None:
    result = GovernedAgent(root_path=".").handle_request("Deploy payment-service to production")

    assert result["envelope"]["decision"] == "REQUEST_REVIEW"
    assert result["envelope"]["review_status"] == "PENDING"
    assert result["envelope"]["approval_valid"] is False
    assert "REVIEW_TOKEN_MISSING" in result["envelope"]["approval_errors"]
