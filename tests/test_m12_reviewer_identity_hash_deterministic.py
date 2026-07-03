from __future__ import annotations

from gcr.reviewer_identity import compute_reviewer_identity_hash
from gcr.reviewer_registry import load_reviewer_registry


def test_m12_reviewer_identity_hash_deterministic() -> None:
    reviewer = load_reviewer_registry().get_reviewer("alice-release")

    assert compute_reviewer_identity_hash(reviewer) == reviewer["identity_hash"]
    assert compute_reviewer_identity_hash(dict(reviewer)) == compute_reviewer_identity_hash(dict(reviewer))
