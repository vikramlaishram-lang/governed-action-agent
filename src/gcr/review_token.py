from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import UTC, datetime, timedelta
from uuid import uuid4


@dataclass(frozen=True)
class ReviewToken:
    schema_version: str
    token_id: str
    proposal_id: str
    reviewer_id: str
    reviewer_role: str
    approval_status: str
    approved_normalized_action: str
    approved_consequence_class: str
    approval_scope: str
    issued_at: str
    expires_at: str
    approval_reason: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "ReviewToken":
        return cls(**data)

    @classmethod
    def new_for_proposal(
        cls,
        proposal: dict,
        reviewer_id: str,
        reviewer_role: str,
        approval_scope: str,
        ttl_seconds: int = 3600,
        approval_reason: str = "",
    ) -> "ReviewToken":
        issued_at = datetime.now(UTC)
        expires_at = issued_at + timedelta(seconds=ttl_seconds)
        return cls(
            schema_version="review_token_v0.1",
            token_id=f"review_{uuid4().hex}",
            proposal_id=proposal["proposal_id"],
            reviewer_id=reviewer_id,
            reviewer_role=reviewer_role,
            approval_status="APPROVED",
            approved_normalized_action=proposal["normalized_action"],
            approved_consequence_class=proposal["consequence_class"],
            approval_scope=approval_scope,
            issued_at=issued_at.isoformat(),
            expires_at=expires_at.isoformat(),
            approval_reason=approval_reason,
        )
