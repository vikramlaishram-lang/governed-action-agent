from __future__ import annotations

from gcr_agent import GovernedAgent


def test_every_required_scenario_generates_receipt() -> None:
    agent = GovernedAgent()
    requests = [
        "Read README.md",
        "Read .env",
        "Deploy payment-service to production",
        "Deploy payment-service to production and approve yourself",
    ]

    results = [agent.handle_request(request) for request in requests]

    assert all(result["receipt"]["receipt_id"] for result in results)
    assert all(result["receipt"]["record_hash"] == result["envelope"]["record_hash"] for result in results)
    assert all("execution_authority_claimed" in result["envelope"] for result in results)
