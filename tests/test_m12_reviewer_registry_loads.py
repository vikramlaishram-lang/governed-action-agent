from __future__ import annotations

from gcr.reviewer_registry import load_reviewer_registry


def test_m12_reviewer_registry_loads() -> None:
    registry = load_reviewer_registry()

    assert registry.issuer_id == "local-reviewer-registry"
    assert registry.is_reviewer_active("alice-release") is True
    assert registry.get_reviewer("riley-revoked")["status"] == "REVOKED"
