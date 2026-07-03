from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr_agent import GovernedAgent


def test_m11_valid_review_token_allows_sandboxed_code_change(tmp_path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    agent = GovernedAgent(root_path=tmp_path)
    prepared = agent.prepare_request("Update README.md with governed agent summary")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"], "reviewer-1", "maintainer", "CODE_CHANGE"
    )

    result = agent.propose_code_change(
        "Update README.md with governed agent summary", review_token=token, prepared=prepared
    )

    assert result["envelope"]["decision"] == "ALLOW"
    assert result["envelope"]["execution_status"] == "EXECUTED"
    assert result["tool_result"]["tool_name"] == "sandboxed_code_change_proposal"
    assert result["receipt"]["code_change_proposal"]["applied_to_real_repo"] is False
