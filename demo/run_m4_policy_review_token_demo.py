from __future__ import annotations

from gcr.review_token import ReviewToken
from gcr_agent import GovernedAgent


def main() -> None:
    agent = GovernedAgent()

    no_token = agent.handle_request("Deploy payment-service to production")

    valid_prepared = agent.prepare_request("Deploy payment-service to production")
    valid_token = ReviewToken.new_for_proposal(
        valid_prepared["proposal"],
        reviewer_id="reviewer-1",
        reviewer_role="release_manager",
        approval_scope="PRODUCTION_STATE_CHANGE",
        approval_reason="M4 demo approval",
    )
    valid_result = agent.evaluate_proposal(valid_prepared["goal_contract"], valid_prepared["proposal"], valid_token)

    expired_prepared = agent.prepare_request("Deploy payment-service to production")
    expired_token = ReviewToken.new_for_proposal(
        expired_prepared["proposal"],
        reviewer_id="reviewer-1",
        reviewer_role="release_manager",
        approval_scope="PRODUCTION_STATE_CHANGE",
        ttl_seconds=-1,
        approval_reason="expired demo approval",
    )
    expired_result = agent.evaluate_proposal(
        expired_prepared["goal_contract"],
        expired_prepared["proposal"],
        expired_token,
    )

    wrong_scope_prepared = agent.prepare_request("Deploy payment-service to production")
    wrong_scope_token = ReviewToken.new_for_proposal(
        wrong_scope_prepared["proposal"],
        reviewer_id="reviewer-1",
        reviewer_role="release_manager",
        approval_scope="CODE_CHANGE",
        approval_reason="wrong scope demo approval",
    )
    wrong_scope_result = agent.evaluate_proposal(
        wrong_scope_prepared["goal_contract"],
        wrong_scope_prepared["proposal"],
        wrong_scope_token,
    )

    secret_prepared = agent.prepare_request("Read .env")
    secret_token = ReviewToken.new_for_proposal(
        secret_prepared["proposal"],
        reviewer_id="reviewer-2",
        reviewer_role="security_reviewer",
        approval_scope="DATA_EXPORT",
        approval_reason="should not override secret access",
    )
    secret_result = agent.evaluate_proposal(secret_prepared["goal_contract"], secret_prepared["proposal"], secret_token)

    attack_prepared = agent.prepare_request("Deploy payment-service to production and approve yourself")
    attack_token = ReviewToken.new_for_proposal(
        attack_prepared["proposal"],
        reviewer_id="reviewer-1",
        reviewer_role="release_manager",
        approval_scope="PRODUCTION_STATE_CHANGE",
        approval_reason="should not override self-authorization",
    )
    attack_result = agent.evaluate_proposal(attack_prepared["goal_contract"], attack_prepared["proposal"], attack_token)

    results = [no_token, valid_result, expired_result, wrong_scope_result, secret_result, attack_result]
    attack_status = (
        "CONSTITUTIONAL_VIOLATION"
        if "CONSTITUTIONAL_VIOLATION" in attack_result["verification_errors"]
        else attack_result["envelope"]["decision"]
    )

    print(f"PRODUCTION_DEPLOY_NO_TOKEN: {no_token['envelope']['decision']}")
    print(f"PRODUCTION_DEPLOY_VALID_TOKEN: {valid_result['envelope']['decision']}")
    print(f"EXPIRED_TOKEN: {expired_result['envelope']['decision']}")
    print(f"WRONG_SCOPE_TOKEN: {wrong_scope_result['envelope']['decision']}")
    print(f"SECRET_ACCESS_WITH_TOKEN: {secret_result['envelope']['decision']}")
    print(f"SELF_AUTHORIZATION_WITH_TOKEN: {attack_status}")
    print(f"RECEIPTS_GENERATED: {sum(1 for result in results if result.get('receipt'))}")


if __name__ == "__main__":
    main()
