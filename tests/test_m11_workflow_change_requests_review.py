from __future__ import annotations

from gcr_agent import GovernedAgent


def test_m11_workflow_change_requests_review(tmp_path) -> None:
    result = GovernedAgent(root_path=tmp_path).propose_code_change("Propose workflow change")

    assert result["proposal"]["consequence_class"] == "WORKFLOW_CHANGE"
    assert result["envelope"]["decision"] == "REQUEST_REVIEW"
    assert "WORKFLOW_CHANGE" in result["code_change_proposal"]["risk_flags"]
