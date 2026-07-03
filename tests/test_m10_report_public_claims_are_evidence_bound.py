from __future__ import annotations

from gcr.report_generator import generate_report_summary
from gcr_agent import GovernedAgent


def test_m10_report_public_claims_are_evidence_bound(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=".", ledger_path=ledger_path).handle_request("Read README.md")
    claims = generate_report_summary(ledger_path=ledger_path)["public_claims_allowed"]
    forbidden = ["production safety", "complete security", "tamper-proof", "legal", "certification"]

    assert claims
    assert not any(term in " ".join(claims).lower() for term in forbidden)
