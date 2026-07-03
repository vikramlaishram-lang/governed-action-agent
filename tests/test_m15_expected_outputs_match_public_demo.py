from __future__ import annotations

from pathlib import Path


def test_m15_expected_outputs_match_public_demo() -> None:
    public_demo = Path("examples/external_review/expected_public_demo_output.txt").read_text(encoding="utf-8")
    release_validation = Path("examples/external_review/expected_release_validation_output.txt").read_text(encoding="utf-8")
    viewer = Path("examples/external_review/expected_m13_viewer_output.txt").read_text(encoding="utf-8")

    for line in [
        "PUBLIC_DEMO_STARTED: true",
        "SAFE_READ: ALLOW",
        "SECRET_ACCESS: DENY",
        "PRODUCTION_DEPLOY_NO_REVIEWER: REQUEST_REVIEW",
        "SELF_AUTHORIZATION_ATTACK: CONSTITUTIONAL_VIOLATION",
        "SANDBOXED_CODE_CHANGE_NO_TOKEN: REQUEST_REVIEW",
        "VALID_REVIEWER_APPROVAL: ALLOW",
        "PUBLIC_DEMO_PASS: true",
    ]:
        assert line in public_demo
    for line in ["RELEASE_PACKAGE_VALID: true", "SAMPLE_ARTIFACTS_SANITIZED: true"]:
        assert line in release_validation
    for line in ["VIEWER_GENERATED: true", "SECRETS_EXPOSED: false"]:
        assert line in viewer
