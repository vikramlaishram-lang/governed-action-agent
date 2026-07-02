from __future__ import annotations

import os
import subprocess
import sys


def test_m7_cli_demo_passes() -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    completed = subprocess.run(
        [sys.executable, "demo/run_m7_cli_packaging_demo.py"],
        check=True,
        capture_output=True,
        text=True,
        env=env,
        timeout=60,
    )

    assert completed.stdout.splitlines() == [
        "CLI_INIT: OK",
        "CLI_STATUS: INITIALIZED",
        "CLI_SAFE_READ: ALLOW",
        "CLI_SECRET_ACCESS: DENY",
        "CLI_VERIFY_LEDGER: true",
        "CLI_HMAC_INIT: OK",
        "CLI_HMAC_VERIFY: true",
    ]
