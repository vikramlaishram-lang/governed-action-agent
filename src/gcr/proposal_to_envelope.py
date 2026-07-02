from __future__ import annotations

import copy
import hashlib
import json
from datetime import UTC, datetime


def canonical_json(value: dict) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_json(value: dict) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def proposal_to_envelope(
    proposal: dict,
    policy_result: dict,
    *,
    previous_record_hash: str | None = None,
    runtime_id: str = "local_simulator",
) -> dict:
    envelope = {
        "schema_version": "decision_envelope_v0.2",
        "created_at": datetime.now(UTC).isoformat(),
        "runtime_id": runtime_id,
        "proposal_id": proposal["proposal_id"],
        "proposal_hash": sha256_json(proposal),
        "agent_id": proposal["agent_id"],
        "agent_output_mode": proposal["agent_output_mode"],
        "agent_output_mode_basis": proposal["agent_output_mode_basis"],
        "execution_authority_claimed": proposal["execution_authority_claimed"],
        "proposal_readiness_score": proposal["proposal_readiness_score"],
        "internal_trace_id": proposal["internal_trace_id"],
        "proposed_action": proposal["proposed_action"],
        "normalized_action": proposal["normalized_action"],
        "normalized_action_hash": sha256_text(proposal["normalized_action"]),
        "consequence_classification": proposal["consequence_class"],
        "evidence_references": proposal["evidence_available"],
        "evidence_gap_summary": proposal["evidence_gaps"],
        "policy_version": policy_result["policy_version"],
        "policy_hash": policy_result["policy_hash"],
        "decision_engine_version": policy_result["decision_engine_version"],
        "decision": policy_result["decision"],
        "decision_basis": policy_result["decision_basis"],
        "decision_reason": policy_result["decision_reason"],
        "review_status": policy_result["review_status"],
        "reviewer_authority_id": policy_result.get("reviewer_id"),
        "reviewer_role": policy_result.get("reviewer_role"),
        "approval_token_id": policy_result.get("approval_token_id"),
        "approval_scope": policy_result.get("approval_scope"),
        "approval_expiry": policy_result.get("approval_expiry"),
        "approval_valid": policy_result.get("approval_valid", False),
        "approval_errors": policy_result.get("approval_errors", []),
        "execution_status": "PENDING",
        "outcome_status": "PENDING",
        "tamper_evidence_mode": "sha256_canonical_json",
        "previous_record_hash": previous_record_hash,
        "record_hash": "",
    }
    hashable = copy.deepcopy(envelope)
    hashable["record_hash"] = ""
    envelope["record_hash"] = sha256_json(hashable)
    return envelope
