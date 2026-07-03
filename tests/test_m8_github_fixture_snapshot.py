from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator

from gcr.evidence_hash import evidence_hash
from gcr_agent.github_pr_reader import GitHubPRReader


FIXTURE = Path("tests/fixtures/github/pr_ready.json")


def test_m8_fixture_snapshot_validates_and_hashes() -> None:
    snapshot = GitHubPRReader().from_fixture(FIXTURE)
    schema = json.loads(Path("schemas/github_pr_snapshot_v0.1.schema.json").read_text(encoding="utf-8"))

    Draft202012Validator(schema).validate(snapshot)

    assert snapshot["checks_passing"] is True
    assert snapshot["evidence_hash"] == evidence_hash(snapshot)
    assert snapshot["evidence_hash"].startswith("sha256:")


def test_m8_snapshot_strips_patch_content() -> None:
    snapshot = GitHubPRReader().from_fixture(FIXTURE)

    assert "patch" not in json.dumps(snapshot)
    assert "do not persist this patch" not in json.dumps(snapshot)
