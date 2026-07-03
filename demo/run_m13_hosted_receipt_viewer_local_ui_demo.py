from __future__ import annotations

import json
from pathlib import Path
from tempfile import TemporaryDirectory

from gcr.report_generator import generate_report_summary
from gcr.viewer_generator import write_viewer_bundle
from gcr_agent import GovernedAgent


FORBIDDEN_STRINGS = [
    "GAA_LEDGER_HMAC_KEY",
    "GITHUB_TOKEN",
    "do not persist this patch",
    "Governed Action Agent Note",
    "full patch text",
    "SECRET=do-not-store",
]


def main() -> None:
    fixture = Path(__file__).resolve().parents[1] / "tests" / "fixtures" / "github" / "pr_ready.json"
    with TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        (root / "README.md").write_text("# Demo Repo\n", encoding="utf-8")
        ledger_path = root / ".governed-agent" / "ledger.jsonl"
        ledger_path.parent.mkdir(parents=True, exist_ok=True)

        agent = GovernedAgent(root_path=root, ledger_path=ledger_path)
        agent.handle_request("Read README.md")
        agent.handle_request("Read .env")
        agent.handle_request("Deploy payment-service to production and approve yourself")
        if fixture.exists():
            agent.inspect_github_pr(
                "https://github.com/vikramlaishram-lang/governed-action-agent/pull/42",
                fixture_path=fixture,
            )
        else:
            agent.handle_request("List files")
        agent.propose_code_change("Update README.md with governed agent summary")

        summary = generate_report_summary(ledger_path=ledger_path)
        written = write_viewer_bundle(summary=summary, output_dir=root / ".governed-agent" / "viewer")
        index_path = Path(written["index_path"])
        data_path = Path(written["data_path"])
        viewer_data = json.loads(data_path.read_text(encoding="utf-8"))
        rendered = index_path.read_text(encoding="utf-8") + data_path.read_text(encoding="utf-8")

        print(f"VIEWER_GENERATED: {str(written['viewer_generated']).lower()}")
        print(f"VIEWER_INDEX_EXISTS: {str(index_path.exists()).lower()}")
        print(f"VIEWER_DATA_EXISTS: {str(data_path.exists()).lower()}")
        print(f"LEDGER_VALID: {str(viewer_data['ledger']['valid']).lower()}")
        print(f"TOTAL_RECORDS: {viewer_data['ledger']['record_count']}")
        print(f"VIOLATIONS_RENDERED: {str(viewer_data['violations']['constitutional_violation_count'] > 0).lower()}")
        print(f"GITHUB_PR_EVIDENCE_RENDERED: {str(bool(viewer_data['github_pr_evidence'])).lower()}")
        print(f"CODE_CHANGE_PROPOSALS_RENDERED: {str(bool(viewer_data['code_change_proposals'])).lower()}")
        print(f"PUBLIC_CLAIMS_RENDERED: {str(bool(viewer_data['public_claims_allowed'])).lower()}")
        print(f"SECRETS_EXPOSED: {str(any(secret in rendered for secret in FORBIDDEN_STRINGS)).lower()}")


if __name__ == "__main__":
    main()
