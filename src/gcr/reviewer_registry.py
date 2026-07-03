from __future__ import annotations

import json
from pathlib import Path

from .reviewer_identity import compute_reviewer_identity_hash


class ReviewerAuthorityRegistry:
    def __init__(self, registry: dict) -> None:
        self.registry = dict(registry)
        reviewers = []
        for reviewer in self.registry.get("reviewers", []):
            normalized = dict(reviewer)
            expected = compute_reviewer_identity_hash(normalized)
            if normalized.get("identity_hash") in {None, "", "<computed>"}:
                normalized["identity_hash"] = expected
            reviewers.append(normalized)
        self.registry["reviewers"] = reviewers

    @classmethod
    def from_file(cls, path: str | Path) -> "ReviewerAuthorityRegistry":
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    def to_dict(self) -> dict:
        return dict(self.registry)

    def get_reviewer(self, reviewer_id: str) -> dict | None:
        for reviewer in self.registry.get("reviewers", []):
            if reviewer.get("reviewer_id") == reviewer_id:
                return reviewer
        return None

    def is_reviewer_active(self, reviewer_id: str) -> bool:
        reviewer = self.get_reviewer(reviewer_id)
        return bool(reviewer and reviewer.get("status") == "ACTIVE")

    def reviewer_has_role(self, reviewer_id: str, role: str) -> bool:
        reviewer = self.get_reviewer(reviewer_id)
        return bool(reviewer and role in reviewer.get("roles", []))

    def reviewer_has_scope(self, reviewer_id: str, scope: str) -> bool:
        reviewer = self.get_reviewer(reviewer_id)
        return bool(reviewer and scope in reviewer.get("allowed_scopes", []))

    def verify_identity_hash(self, reviewer_id: str, identity_hash: str) -> bool:
        reviewer = self.get_reviewer(reviewer_id)
        return bool(reviewer and reviewer.get("identity_hash") == identity_hash)

    @property
    def issuer_id(self) -> str:
        return self.registry["issuer_id"]

    @property
    def registry_version(self) -> str:
        return self.registry["registry_version"]


def load_reviewer_registry(path: str | Path | None = None) -> ReviewerAuthorityRegistry:
    registry_path = Path(path) if path is not None else Path(__file__).resolve().parents[2] / "configs" / "reviewers.default.json"
    return ReviewerAuthorityRegistry.from_file(registry_path)
