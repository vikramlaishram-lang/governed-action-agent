from __future__ import annotations

import json
import sys
from pathlib import Path


FORBIDDEN = [
    "GAA_LEDGER_HMAC_KEY",
    "GITHUB_TOKEN",
    "authorization",
    "bearer",
    "hmac_key",
    "private key",
    "id_rsa",
    "id_ed25519",
    "SECRET_VALUE",
    "full diff_text",
    "patch text",
    "C:\\Users\\vikra",
    "/home/",
]


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    checks = [
        ("README.md exists", (root / "README.md").exists()),
        ("README mentions quickstart", "Quickstart" in _read(root / "README.md")),
        ("docs/PUBLIC_DEMO.md exists", (root / "docs" / "PUBLIC_DEMO.md").exists()),
        ("docs/RELEASE_PACKAGE.md exists", (root / "docs" / "RELEASE_PACKAGE.md").exists()),
        (
            "docs/PUBLIC_CLAIMS_AND_LIMITATIONS.md exists",
            (root / "docs" / "PUBLIC_CLAIMS_AND_LIMITATIONS.md").exists(),
        ),
        ("docs/EVALUATOR_QUICKSTART.md exists", (root / "docs" / "EVALUATOR_QUICKSTART.md").exists()),
        ("scripts/run_public_demo.py exists", (root / "scripts" / "run_public_demo.py").exists()),
        ("examples/public_demo_expected_output.txt exists", (root / "examples" / "public_demo_expected_output.txt").exists()),
        (
            "examples/sample_governed_agent_report.md exists",
            (root / "examples" / "sample_governed_agent_report.md").exists(),
        ),
        (
            "examples/sample_governed_agent_report.json exists",
            (root / "examples" / "sample_governed_agent_report.json").exists(),
        ),
        ("examples/sample_viewer/index.html exists", (root / "examples" / "sample_viewer" / "index.html").exists()),
        (
            "examples/sample_viewer/viewer_data.json exists",
            (root / "examples" / "sample_viewer" / "viewer_data.json").exists(),
        ),
        ("sample report JSON parses", _json_parses(root / "examples" / "sample_governed_agent_report.json")),
        ("sample viewer JSON parses", _json_parses(root / "examples" / "sample_viewer" / "viewer_data.json")),
        ("sample artifacts sanitized", _sample_artifacts_sanitized(root)),
        ("pytest command documented", "python -m pytest -q" in _read(root / "README.md")),
        ("public demo command documented", "scripts/run_public_demo.py" in _read(root / "README.md")),
    ]
    failures = [name for name, ok in checks if not ok]
    if failures:
        for failure in failures:
            print(f"RELEASE_PACKAGE_CHECK_FAILED: {failure}")
        return 1

    print("RELEASE_PACKAGE_VALID: true")
    print("README_READY: true")
    print("PUBLIC_DEMO_DOC_READY: true")
    print("CLAIMS_BOUNDARY_DOC_READY: true")
    print("SAMPLE_REPORT_READY: true")
    print("SAMPLE_VIEWER_READY: true")
    print("SAMPLE_ARTIFACTS_SANITIZED: true")
    return 0


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def _json_parses(path: Path) -> bool:
    try:
        json.loads(_read(path))
    except json.JSONDecodeError:
        return False
    return path.exists()


def _sample_artifacts_sanitized(root: Path) -> bool:
    paths = [
        root / "examples" / "sample_governed_agent_report.md",
        root / "examples" / "sample_governed_agent_report.json",
        root / "examples" / "sample_viewer" / "index.html",
        root / "examples" / "sample_viewer" / "viewer_data.json",
    ]
    combined = "\n".join(_read(path) for path in paths)
    lowered = combined.lower()
    return not any(item.lower() in lowered for item in FORBIDDEN)


if __name__ == "__main__":
    sys.exit(main())
