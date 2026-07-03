from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr.reviewer_registry import load_reviewer_registry
from gcr_agent import GovernedAgent


def test_m12_token_cannot_override_irreversible_delete(tmp_path) -> None:
    registry = load_reviewer_registry()
    agent = GovernedAgent(root_path=tmp_path, reviewer_registry=registry)
    prepared = agent.prepare_request("Delete README.md")
    token = ReviewToken.new_for_proposal(prepared["proposal"], "alice-release", "release_manager", "CODE_CHANGE", reviewer_registry=registry)

    result = agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    assert result["envelope"]["decision"] == "DENY"
