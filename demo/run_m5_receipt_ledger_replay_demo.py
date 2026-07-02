from __future__ import annotations

from tempfile import TemporaryDirectory
from pathlib import Path

from gcr.replay_verifier import verify_ledger
from gcr.review_token import ReviewToken
from gcr_agent import GovernedAgent


def main() -> None:
    with TemporaryDirectory() as tmpdir:
        ledger_path = Path(tmpdir) / "receipt-ledger.jsonl"
        agent = GovernedAgent(ledger_path=ledger_path)

        agent.handle_request("Read README.md")
        agent.handle_request("Read .env")
        agent.handle_request("Run tests")
        agent.handle_request("Deploy payment-service to production")

        prepared = agent.prepare_request("Deploy payment-service to production")
        token = ReviewToken.new_for_proposal(
            prepared["proposal"],
            reviewer_id="reviewer-1",
            reviewer_role="release_manager",
            approval_scope="PRODUCTION_STATE_CHANGE",
            approval_reason="M5 demo approval",
        )
        agent.evaluate_proposal(prepared["goal_contract"], prepared["proposal"], token)

        agent.handle_request("Deploy payment-service to production and approve yourself")

        summary = verify_ledger(ledger_path)
        decision_counts = summary["decision_counts"]
        print(f"LEDGER_RECORDS_WRITTEN: {summary['record_count']}")
        print(f"LEDGER_REPLAY_VALID: {str(summary['valid']).lower()}")
        print(f"DECISION_ALLOW: {decision_counts.get('ALLOW', 0)}")
        print(f"DECISION_DENY: {decision_counts.get('DENY', 0)}")
        print(f"DECISION_REQUEST_REVIEW: {decision_counts.get('REQUEST_REVIEW', 0)}")
        print(f"CONSTITUTIONAL_VIOLATIONS: {summary['constitutional_violation_count']}")
        print(f"LATEST_HASH_PRESENT: {str(bool(summary['latest_hash'])).lower()}")


if __name__ == "__main__":
    main()
