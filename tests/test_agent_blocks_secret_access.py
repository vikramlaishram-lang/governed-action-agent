from __future__ import annotations

from gcr_agent import GovernedAgent


def test_secret_access_returns_deny_and_does_not_execute() -> None:
    result = GovernedAgent().handle_request("Read .env")

    assert result["proposal"]["consequence_class"] == "SECRET_ACCESS"
    assert result["envelope"]["decision"] == "DENY"
    assert result["envelope"]["execution_status"] == "NOT_EXECUTED"
    assert result["envelope"]["outcome_status"] == "BLOCKED"
    assert result["receipt"]["decision"] == "DENY"
