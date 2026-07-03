from __future__ import annotations

import json
from pathlib import Path


def test_m14_sample_artifacts_are_sanitized() -> None:
    paths = [
        Path("examples/sample_governed_agent_report.md"),
        Path("examples/sample_governed_agent_report.json"),
        Path("examples/sample_viewer/index.html"),
        Path("examples/sample_viewer/viewer_data.json"),
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    lowered = combined.lower()

    for forbidden in [
        "gaa_ledger_hmac_key",
        "github_token",
        "authorization",
        "bearer",
        "hmac_key",
        "private key",
        "id_rsa",
        "id_ed25519",
        "secret_value",
        "full diff_text",
        "patch text",
        "c:\\users\\vikra",
        "/home/",
    ]:
        assert forbidden not in lowered

    json.loads(Path("examples/sample_governed_agent_report.json").read_text(encoding="utf-8"))
    json.loads(Path("examples/sample_viewer/viewer_data.json").read_text(encoding="utf-8"))
