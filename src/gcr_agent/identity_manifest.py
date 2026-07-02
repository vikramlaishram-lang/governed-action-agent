from __future__ import annotations


IDENTITY_MANIFEST = {
    "agent_id": "governed_coding_agent",
    "role": "coding_release_assistant",
    "allowed_modes": ["PLAN", "ACTION_PROPOSAL", "REVIEW_REQUEST", "REFUSAL"],
    "forbidden_modes": ["SELF_AUTHORIZE", "SILENT_EXECUTION"],
    "default_posture": "proposal_first",
}


def get_identity_manifest() -> dict:
    return dict(IDENTITY_MANIFEST)
