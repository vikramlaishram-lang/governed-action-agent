from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ReviewerIdentityManifest:
    schema_version: str
    reviewer_id: str
    display_name: str
    status: str
    roles: list[str]
    allowed_scopes: list[str]
    created_at: str
    identity_hash: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ReviewerIdentityManifest":
        return cls(**data)

    def with_computed_hash(self) -> "ReviewerIdentityManifest":
        data = self.to_dict()
        data["identity_hash"] = compute_reviewer_identity_hash(data)
        return ReviewerIdentityManifest.from_dict(data)


def canonical_json(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def compute_reviewer_identity_hash(identity: dict) -> str:
    payload = dict(identity)
    payload.pop("identity_hash", None)
    return f"sha256:{hashlib.sha256(canonical_json(payload)).hexdigest()}"
