from __future__ import annotations

from gcr_agent import GovernedAgent


def test_m4_policy_preserves_m3_defaults() -> None:
    agent = GovernedAgent(root_path=".")

    assert agent.handle_request("List files")["envelope"]["decision"] == "ALLOW"
    assert agent.handle_request("Read README.md")["envelope"]["decision"] == "ALLOW"
    assert agent.handle_request("Read .env")["envelope"]["decision"] == "DENY"
    assert agent.handle_request("Deploy payment-service to production")["envelope"]["decision"] == "REQUEST_REVIEW"
