from __future__ import annotations

import json
import sys
from pathlib import Path


REQUIRED_DOCS = [
    "docs/external_review/README.md",
    "docs/external_review/REVIEWER_INSTRUCTIONS.md",
    "docs/external_review/FRESH_CLONE_REPRODUCTION_CHECKLIST.md",
    "docs/external_review/EXPECTED_OUTPUTS.md",
    "docs/external_review/REVIEWER_ATTESTATION_FORM.md",
    "docs/external_review/EXTERNAL_FINDINGS_LEDGER.md",
    "docs/external_review/FAILURE_LOG_TEMPLATE.md",
    "docs/external_review/REVIEW_SCOPE_AND_LIMITATIONS.md",
    "docs/external_review/REVIEW_PACKET_MANIFEST.json",
]
PUBLIC_DEMO_LINES = [
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
RELEASE_VALIDATION_LINES = [
    "RELEASE_PACKAGE_VALID: true",
    "README_READY: true",
    "PUBLIC_DEMO_DOC_READY: true",
    "CLAIMS_BOUNDARY_DOC_READY: true",
    "SAMPLE_REPORT_READY: true",
    "SAMPLE_VIEWER_READY: true",
    "SAMPLE_ARTIFACTS_SANITIZED: true",
]
FORBIDDEN_COMPLETE_CLAIMS = [
    "external review complete",
    "external audit completed",
    "external audit is complete",
    "production-safe",
    "is production safe",
    "legally certified",
    "compliance certified",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    checks = [
        ("required docs exist", all((root / path).exists() for path in REQUIRED_DOCS)),
        ("manifest valid", _manifest_valid(root)),
        ("expected outputs ready", _expected_outputs_ready(root)),
        ("attestation fields ready", _attestation_ready(root)),
        ("findings ledger columns ready", _findings_ledger_ready(root)),
        ("scope phrase ready", _scope_ready(root)),
        ("no completion overclaim", _no_completion_overclaim(root)),
        ("examples ready", _examples_ready(root)),
    ]
    failures = [name for name, ok in checks if not ok]
    if failures:
        for failure in failures:
            print(f"EXTERNAL_REVIEW_PACKET_CHECK_FAILED: {failure}")
        return 1

    print("EXTERNAL_REVIEW_PACKET_VALID: true")
    print("REVIEWER_INSTRUCTIONS_READY: true")
    print("FRESH_CLONE_CHECKLIST_READY: true")
    print("EXPECTED_OUTPUTS_READY: true")
    print("ATTESTATION_FORM_READY: true")
    print("FINDINGS_LEDGER_READY: true")
    print("FAILURE_LOG_TEMPLATE_READY: true")
    print("REVIEW_SCOPE_LIMITATIONS_READY: true")
    return 0


def _read(root: Path, path: str) -> str:
    file_path = root / path
    return file_path.read_text(encoding="utf-8") if file_path.exists() else ""


def _manifest_valid(root: Path) -> bool:
    try:
        manifest = json.loads(_read(root, "docs/external_review/REVIEW_PACKET_MANIFEST.json"))
    except json.JSONDecodeError:
        return False
    return (
        manifest.get("schema_version") == "external_review_packet_manifest_v0.1"
        and manifest.get("milestone") == "M15_EXTERNAL_REPRODUCTION_AND_REVIEW_PACKET"
        and manifest.get("packet_status") == "PREPARED_FOR_EXTERNAL_REVIEW"
        and manifest.get("external_review_complete") is False
        and manifest.get("source_release_tag") == "v0.14.0-local-release"
    )


def _expected_outputs_ready(root: Path) -> bool:
    expected = _read(root, "docs/external_review/EXPECTED_OUTPUTS.md")
    return all(line in expected for line in PUBLIC_DEMO_LINES + RELEASE_VALIDATION_LINES) and all(
        line in expected
        for line in [
            "EXTERNAL_REVIEW_PACKET_VALID: true",
            "REVIEWER_INSTRUCTIONS_READY: true",
            "FRESH_CLONE_CHECKLIST_READY: true",
            "EXPECTED_OUTPUTS_READY: true",
            "ATTESTATION_FORM_READY: true",
            "FINDINGS_LEDGER_READY: true",
            "FAILURE_LOG_TEMPLATE_READY: true",
            "REVIEW_SCOPE_LIMITATIONS_READY: true",
        ]
    )


def _attestation_ready(root: Path) -> bool:
    text = _read(root, "docs/external_review/REVIEWER_ATTESTATION_FORM.md")
    return all(
        field in text
        for field in [
            "Reviewer name:",
            "Commit hash reviewed:",
            "Commands run:",
            "Reproduced claims:",
            "Not reproduced / failed items:",
            "Attestation statement:",
        ]
    )


def _findings_ledger_ready(root: Path) -> bool:
    text = _read(root, "docs/external_review/EXTERNAL_FINDINGS_LEDGER.md")
    return all(
        column in text
        for column in [
            "Finding ID",
            "Date",
            "Reviewer",
            "Commit",
            "Severity",
            "Area",
            "Expected",
            "Observed",
            "Reproduction steps",
            "Status",
            "Resolution commit",
            "Notes",
        ]
    )


def _scope_ready(root: Path) -> bool:
    return (
        "This packet prepares external reproduction. It is not itself external validation."
        in _read(root, "docs/external_review/REVIEW_SCOPE_AND_LIMITATIONS.md")
    )


def _no_completion_overclaim(root: Path) -> bool:
    docs = "\n".join(_read(root, path) for path in REQUIRED_DOCS if path.endswith(".md"))
    lowered = docs.lower()
    allowed_phrases = [
        "external_review_not_yet_complete",
        "m15_external_review_not_yet_complete",
        "m15 does not mean an external reviewer has completed the review",
        "external review is complete only after a reviewer fills out the attestation form and findings ledger",
        "do not infer that an external audit is complete",
        "external audit completion",
    ]
    for phrase in allowed_phrases:
        lowered = lowered.replace(phrase, "")
    return not any(claim in lowered for claim in FORBIDDEN_COMPLETE_CLAIMS)


def _examples_ready(root: Path) -> bool:
    sample_attestation = _read(root, "examples/external_review/sample_attestation_completed_example.md")
    sample_failure = _read(root, "examples/external_review/sample_failure_log_example.md")
    return all(
        (root / path).exists()
        for path in [
            "examples/external_review/expected_public_demo_output.txt",
            "examples/external_review/expected_release_validation_output.txt",
            "examples/external_review/expected_m13_viewer_output.txt",
            "examples/external_review/sample_attestation_completed_example.md",
            "examples/external_review/sample_failure_log_example.md",
        ]
    ) and "SAMPLE ONLY - NOT A REAL EXTERNAL REVIEW" in sample_attestation and "SAMPLE ONLY - NOT A REAL FAILURE REPORT" in sample_failure


if __name__ == "__main__":
    sys.exit(main())
