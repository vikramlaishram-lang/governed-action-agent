from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True)
class CodeChangeProposal:
    schema_version: str
    proposal_artifact_id: str
    proposal_id: str
    agent_id: str
    user_request: str
    target_files: list[str]
    change_intent: str
    sandbox_path: str
    diff_text: str
    diff_hash: str
    created_at: str
    risk_flags: list[str]
    requires_review: bool
    applied_to_real_repo: bool

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "CodeChangeProposal":
        return cls(**data)


def canonical_json(payload: dict) -> bytes:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")


def hash_diff(diff_text: str) -> str:
    return f"sha256:{hashlib.sha256(diff_text.encode('utf-8')).hexdigest()}"


def new_code_change_proposal(
    *,
    proposal_id: str,
    agent_id: str,
    user_request: str,
    target_files: list[str],
    change_intent: str,
    sandbox_path: str,
    diff_text: str,
    risk_flags: list[str],
    requires_review: bool = True,
) -> CodeChangeProposal:
    return CodeChangeProposal(
        schema_version="code_change_proposal_v0.1",
        proposal_artifact_id=f"code_change_{uuid4().hex}",
        proposal_id=proposal_id,
        agent_id=agent_id,
        user_request=user_request,
        target_files=target_files,
        change_intent=change_intent,
        sandbox_path=sandbox_path,
        diff_text=diff_text,
        diff_hash=hash_diff(diff_text),
        created_at=datetime.now(UTC).isoformat(),
        risk_flags=risk_flags,
        requires_review=requires_review,
        applied_to_real_repo=False,
    )
