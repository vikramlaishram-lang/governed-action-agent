from __future__ import annotations

from gcr_agent import GovernedAgent


def test_safe_read_returns_allow_and_executes() -> None:
    result = GovernedAgent().handle_request("Read README.md")

    assert result["proposal"]["consequence_class"] == "READ_ONLY_ACCESS"
    assert result["envelope"]["decision"] == "ALLOW"
    assert result["envelope"]["execution_status"] == "EXECUTED"
    assert result["receipt"]["decision"] == "ALLOW"
    assert "execution_authority_claimed" in result["envelope"]
