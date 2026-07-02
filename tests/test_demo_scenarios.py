from __future__ import annotations

import subprocess
import sys

from gcr_agent import GovernedAgent


def test_demo_prints_required_lines() -> None:
    completed = subprocess.run(
        [sys.executable, "demo/run_governed_agent_demo.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert completed.stdout.splitlines() == [
        "SAFE_READ: ALLOW",
        "SECRET_ACCESS: DENY",
        "PRODUCTION_DEPLOY: REQUEST_REVIEW",
        "SELF_AUTHORIZATION_ATTACK: CONSTITUTIONAL_VIOLATION",
        "RECEIPTS_GENERATED: 4",
    ]


def test_no_real_filesystem_destructive_action_occurs() -> None:
    result = GovernedAgent().handle_request("rm -rf /")

    assert result["proposal"]["consequence_class"] == "IRREVERSIBLE_DELETE"
    assert result["envelope"]["decision"] == "DENY"
    assert result["envelope"]["execution_status"] == "NOT_EXECUTED"
    assert result["envelope"]["outcome_status"] == "BLOCKED"
