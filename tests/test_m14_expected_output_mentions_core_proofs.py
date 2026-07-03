from __future__ import annotations

from pathlib import Path


def test_m14_expected_output_mentions_core_proofs() -> None:
    output = Path("examples/public_demo_expected_output.txt").read_text(encoding="utf-8")

    for line in [
        "PUBLIC_DEMO_STARTED: true",
        "SAFE_READ: ALLOW",
        "SECRET_ACCESS: DENY",
        "PRODUCTION_DEPLOY_NO_REVIEWER: REQUEST_REVIEW",
        "SELF_AUTHORIZATION_ATTACK: CONSTITUTIONAL_VIOLATION",
        "SANDBOXED_CODE_CHANGE_NO_TOKEN: REQUEST_REVIEW",
        "VALID_REVIEWER_APPROVAL: ALLOW",
        "REAL_REPO_UNCHANGED: true",
        "LEDGER_REPLAY_VALID: true",
        "REPORT_GENERATED: true",
        "VIEWER_GENERATED: true",
        "SECRETS_EXPOSED: false",
        "PUBLIC_DEMO_PASS: true",
    ]:
        assert line in output
