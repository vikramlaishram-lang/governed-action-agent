from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

from gcr.report_generator import generate_report_summary, write_report_files
from gcr_agent import GovernedAgent


def main() -> None:
    fixture = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "github" / "pr_ready.json"
    with TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / "README.md").write_text("# Demo\n", encoding="utf-8")
        ledger_path = root / "ledger.jsonl"
        agent = GovernedAgent(root_path=root, ledger_path=ledger_path)
        agent.handle_request("Read README.md")
        agent.handle_request("Read .env")
        agent.handle_request("Deploy payment-service to production")
        agent.handle_request("Deploy payment-service to production and approve yourself")
        agent.inspect_github_pr(
            "https://github.com/vikramlaishram-lang/governed-action-agent/pull/42",
            fixture_path=fixture,
        )
        summary = generate_report_summary(ledger_path=ledger_path)
        write_report_files(summary=summary, output_dir=root / "reports")
        print("REPORT_GENERATED: true")
        print(f"LEDGER_VALID: {str(summary['ledger']['valid']).lower()}")
        print(f"TOTAL_RECORDS: {summary['ledger']['record_count']}")
        print(f"CONSTITUTIONAL_VIOLATIONS: {summary['violations']['constitutional_violation_count']}")
        print(f"EXECUTION_AUTHORIZATION_VIOLATIONS: {summary['violations']['execution_authorization_violation_count']}")
        print(f"LATEST_HASH_PRESENT: {str(summary['ledger']['latest_hash_present']).lower()}")
        print(f"PUBLIC_CLAIMS_COUNT: {len(summary['public_claims_allowed'])}")


if __name__ == "__main__":
    main()
