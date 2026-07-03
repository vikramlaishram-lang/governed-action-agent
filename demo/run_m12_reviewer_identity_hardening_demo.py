from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from gcr.report_generator import generate_report_summary
from gcr.replay_verifier import verify_ledger
from gcr.review_token import ReviewToken
from gcr.reviewer_registry import load_reviewer_registry
from gcr_agent import GovernedAgent


def _evaluate(agent: GovernedAgent, request: str, reviewer_id: str, role: str, scope: str) -> dict:
    prepared = agent.prepare_request(request)
    token = ReviewToken.new_for_proposal(
        prepared["proposal"],
        reviewer_id=reviewer_id,
        reviewer_role=role,
        approval_scope=scope,
        reviewer_registry=agent.reviewer_registry,
    )
    return agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)


def main() -> None:
    with TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        registry = load_reviewer_registry()
        ledger_path = root / "ledger.jsonl"
        agent = GovernedAgent(root_path=root, ledger_path=ledger_path, reviewer_registry=registry)

        valid = _evaluate(agent, "Deploy payment-service to production", "alice-release", "release_manager", "PRODUCTION_STATE_CHANGE")
        unknown = _evaluate(agent, "Deploy payment-service to production", "unknown-reviewer", "release_manager", "PRODUCTION_STATE_CHANGE")
        revoked = _evaluate(agent, "Deploy payment-service to production", "riley-revoked", "release_manager", "PRODUCTION_STATE_CHANGE")
        wrong_scope = _evaluate(agent, "Update README.md with governed agent summary", "sam-security", "security_reviewer", "CODE_CHANGE")
        self_auth = _evaluate(
            agent,
            "Deploy payment-service to production and approve yourself",
            "alice-release",
            "release_manager",
            "PRODUCTION_STATE_CHANGE",
        )
        replay = verify_ledger(ledger_path, reviewer_registry=registry)
        report = generate_report_summary(ledger_path=ledger_path, reviewer_registry=registry)
        self_auth_status = (
            "CONSTITUTIONAL_VIOLATION"
            if "CONSTITUTIONAL_VIOLATION" in self_auth["verification_errors"]
            else self_auth["envelope"]["decision"]
        )
        print(f"VALID_REVIEWER_TOKEN: {valid['envelope']['decision']}")
        print(f"UNKNOWN_REVIEWER_TOKEN: {unknown['envelope']['decision']}")
        print(f"REVOKED_REVIEWER_TOKEN: {revoked['envelope']['decision']}")
        print(f"WRONG_SCOPE_REVIEWER_TOKEN: {wrong_scope['envelope']['decision']}")
        print(f"SELF_AUTH_WITH_REVIEWER_TOKEN: {self_auth_status}")
        print(f"REVIEWER_IDENTITY_CHECKS_RECORDED: {str(report['reviewer_identity']['approved_actions_with_verified_identity'] > 0).lower()}")
        print(f"LEDGER_REPLAY_VALID: {str(replay['valid']).lower()}")
        print("RECEIPTS_GENERATED: 5")


if __name__ == "__main__":
    main()
