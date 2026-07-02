from __future__ import annotations

from dataclasses import asdict, dataclass
from uuid import uuid4


@dataclass(frozen=True)
class ProposalObject:
    schema_version: str
    proposal_id: str
    agent_id: str
    agent_output_mode: str
    agent_output_mode_basis: str
    execution_authority_claimed: bool
    proposed_action: str
    normalized_action: str
    consequence_class: str
    evidence_available: list[str]
    evidence_gaps: list[str]
    risk_level: str
    requires_human_review: bool
    proposal_readiness_score: float
    internal_trace_id: str


def normalize_action(user_request: str) -> str:
    return " ".join(user_request.strip().lower().split())


def risk_for_consequence(consequence_class: str, execution_authority_claimed: bool) -> str:
    if execution_authority_claimed or consequence_class in {"SECRET_ACCESS", "IRREVERSIBLE_DELETE"}:
        return "HIGH"
    if consequence_class in {"PRODUCTION_STATE_CHANGE", "WORKFLOW_CHANGE", "UNKNOWN"}:
        return "MEDIUM"
    return "LOW"


def create_proposal_object(
    *,
    agent_id: str,
    user_request: str,
    agent_output_mode: str,
    agent_output_mode_basis: str,
    execution_authority_claimed: bool,
    consequence_class: str,
) -> dict:
    risk_level = risk_for_consequence(consequence_class, execution_authority_claimed)
    requires_review = consequence_class in {"PRODUCTION_STATE_CHANGE", "WORKFLOW_CHANGE", "UNKNOWN"}
    if execution_authority_claimed:
        requires_review = True

    proposal = ProposalObject(
        schema_version="proposal_object_v0.1",
        proposal_id=f"proposal_{uuid4().hex}",
        agent_id=agent_id,
        agent_output_mode=agent_output_mode,
        agent_output_mode_basis=agent_output_mode_basis,
        execution_authority_claimed=execution_authority_claimed,
        proposed_action=user_request,
        normalized_action=normalize_action(user_request),
        consequence_class=consequence_class,
        evidence_available=["user_request", "identity_manifest", "local_policy_rules"],
        evidence_gaps=[] if consequence_class != "UNKNOWN" else ["No exact classifier rule matched"],
        risk_level=risk_level,
        requires_human_review=requires_review,
        proposal_readiness_score=0.95 if consequence_class != "UNKNOWN" else 0.5,
        internal_trace_id=f"trace_{uuid4().hex}",
    )
    return asdict(proposal)
