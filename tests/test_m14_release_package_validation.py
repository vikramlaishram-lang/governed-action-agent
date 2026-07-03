from __future__ import annotations

import subprocess
import sys


def test_m14_release_package_validation() -> None:
    result = subprocess.run(
        [sys.executable, "scripts/validate_release_package.py"],
        check=True,
        capture_output=True,
        text=True,
    )

    for line in [
        "RELEASE_PACKAGE_VALID: true",
        "README_READY: true",
        "PUBLIC_DEMO_DOC_READY: true",
        "CLAIMS_BOUNDARY_DOC_READY: true",
        "SAMPLE_REPORT_READY: true",
        "SAMPLE_VIEWER_READY: true",
        "SAMPLE_ARTIFACTS_SANITIZED: true",
    ]:
        assert line in result.stdout
