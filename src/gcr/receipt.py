from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4


def create_receipt(
    *,
    goal_contract: dict,
    envelope: dict,
    constitutional_errors: list[str],
) -> dict:
    return {
        "receipt_id": f"receipt_{uuid4().hex}",
        "proposal_id": envelope["proposal_id"],
        "agent_id": envelope["agent_id"],
        "user_request": goal_contract["user_request"],
        "bounded_goal": goal_contract["bounded_goal"],
        "agent_output_mode": envelope["agent_output_mode"],
        "proposed_action": envelope["proposed_action"],
        "normalized_action": envelope["normalized_action"],
        "consequence_class": envelope["consequence_classification"],
        "decision": envelope["decision"],
        "decision_reason": envelope["decision_reason"],
        "execution_status": envelope["execution_status"],
        "outcome_status": envelope["outcome_status"],
        "execution_authority_claimed": envelope["execution_authority_claimed"],
        "constitutional_errors": constitutional_errors,
        "record_hash": envelope["record_hash"],
        "created_at": datetime.now(UTC).isoformat(),
    }
