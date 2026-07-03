from __future__ import annotations

import subprocess
import sys


def test_m15_validate_external_review_packet() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_external_review_packet.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    for line in [
        "EXTERNAL_REVIEW_PACKET_VALID: true",
        "REVIEWER_INSTRUCTIONS_READY: true",
        "FRESH_CLONE_CHECKLIST_READY: true",
        "EXPECTED_OUTPUTS_READY: true",
        "ATTESTATION_FORM_READY: true",
        "FINDINGS_LEDGER_READY: true",
        "FAILURE_LOG_TEMPLATE_READY: true",
        "REVIEW_SCOPE_LIMITATIONS_READY: true",
    ]:
        assert line in result.stdout
