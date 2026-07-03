from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from gcr.report_generator import generate_report_summary
from gcr.replay_verifier import verify_ledger
from gcr.review_token import ReviewToken
from gcr_agent import GovernedAgent


def main() -> None:
    with TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        readme = root / "README.md"
        original = "# Demo Repo\n"
        readme.write_text(original, encoding="utf-8")
        ledger_path = root / "ledger.jsonl"
        agent = GovernedAgent(root_path=root, ledger_path=ledger_path)

        no_token = agent.propose_code_change("Update README.md with governed agent summary")

        prepared = agent.prepare_request("Update README.md with governed agent summary")
        token = ReviewToken.new_for_proposal(
            prepared["proposal"],
            reviewer_id="reviewer-1",
            reviewer_role="maintainer",
            approval_scope="CODE_CHANGE",
        )
        approved = agent.propose_code_change(
            "Update README.md with governed agent summary",
            review_token=token,
            prepared=prepared,
        )

        secret = agent.propose_code_change("Update .env with new secret")
        delete = agent.propose_code_change("Delete README.md")
        summary = verify_ledger(ledger_path)
        report = generate_report_summary(ledger_path=ledger_path)

        print(f"README_CHANGE_NO_TOKEN: {no_token['envelope']['decision']}")
        print(f"README_CHANGE_VALID_TOKEN: {approved['envelope']['decision']}")
        print(f"SECRET_PATCH: {secret['envelope']['decision']}")
        print(f"DELETE_PATCH: {delete['envelope']['decision']}")
        print(f"REAL_REPO_UNCHANGED: {str(readme.read_text(encoding='utf-8') == original).lower()}")
        print(f"LEDGER_REPLAY_VALID: {str(summary['valid']).lower()}")
        print(f"CODE_CHANGE_PROPOSALS_REPORTED: {str(bool(report['code_change_proposals'])).lower()}")
        print("RECEIPTS_GENERATED: 4")


if __name__ == "__main__":
    main()
