from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr.reviewer_registry import ReviewerAuthorityRegistry
from gcr_agent import GovernedAgent


def test_m12_suspended_reviewer_rejected(tmp_path) -> None:
    registry = ReviewerAuthorityRegistry(
        {
            "schema_version": "reviewer_authority_registry_v0.1",
            "registry_version": "test",
            "issuer_id": "issuer",
            "reviewers": [
                {
                    "schema_version": "reviewer_identity_manifest_v0.1",
                    "reviewer_id": "sue",
                    "display_name": "Sue",
                    "status": "SUSPENDED",
                    "roles": ["release_manager"],
                    "allowed_scopes": ["PRODUCTION_STATE_CHANGE"],
                    "created_at": "2026-01-01T00:00:00+00:00",
                    "identity_hash": "<computed>",
                }
            ],
        }
    )
    agent = GovernedAgent(root_path=tmp_path, reviewer_registry=registry)
    prepared = agent.prepare_request("Deploy payment-service to production")
    token = ReviewToken.new_for_proposal(
        prepared["proposal"], "sue", "release_manager", "PRODUCTION_STATE_CHANGE", reviewer_registry=registry
    )

    result = agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

    assert "REVIEWER_NOT_ACTIVE" in result["envelope"]["approval_errors"]
