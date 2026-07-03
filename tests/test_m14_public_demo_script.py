from __future__ import annotations

import subprocess
import sys


EXPECTED_LINES = [
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
]


def test_m14_public_demo_script() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/run_public_demo.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    for line in EXPECTED_LINES:
        assert line in result.stdout
