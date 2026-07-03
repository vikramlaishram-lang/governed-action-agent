from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from gcr.replay_verifier import verify_ledger
from gcr_agent import GovernedAgent


def main() -> None:
    fixture = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "github" / "pr_ready.json"
    with TemporaryDirectory() as tmpdir:
        ledger_path = Path(tmpdir) / "ledger.jsonl"
        result = GovernedAgent(ledger_path=ledger_path).inspect_github_pr(
            "https://github.com/vikramlaishram-lang/governed-action-agent/pull/42",
            fixture_path=fixture,
        )
        snapshot = result["github_pr_snapshot"]
        summary = verify_ledger(ledger_path)
        risk_flags = ",".join(snapshot["risk_flags"]) if snapshot["risk_flags"] else "none"
        print(f"PR_INSPECT: {result['envelope']['decision']}")
        print(f"PR_OWNER: {snapshot['owner']}")
        print(f"PR_REPO: {snapshot['repo']}")
        print(f"PR_NUMBER: {snapshot['pr_number']}")
        print(f"PR_CHECKS_PASSING: {str(snapshot['checks_passing']).lower()}")
        print(f"PR_RISK_FLAGS: {risk_flags}")
        print(f"PR_EVIDENCE_RECORDED: {str(bool(snapshot['evidence_hash'])).lower()}")
        print(f"LEDGER_REPLAY_VALID: {str(summary['valid']).lower()}")


if __name__ == "__main__":
    main()
