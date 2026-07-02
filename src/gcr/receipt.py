from __future__ import annotations

from datetime import UTC, datetime
from uuid import uuid4


def create_receipt(
    *,
    goal_contract: dict,
    envelope: dict,
    constitutional_errors: list[str],
    tool_result: dict,
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
        "tool_name": tool_result.get("tool_name"),
        "tool_status": tool_result.get("tool_status"),
        "tool_summary": _summarize_tool_result(tool_result),
        "record_hash": envelope["record_hash"],
        "created_at": datetime.now(UTC).isoformat(),
    }


def _summarize_tool_result(tool_result: dict) -> str:
    status = tool_result.get("tool_status", "UNKNOWN")
    name = tool_result.get("tool_name") or "no_tool"
    if "reason" in tool_result:
        return f"{name}:{status}:{tool_result['reason']}"
    if name == "read_file_real":
        return f"{name}:{status}:read {tool_result.get('bytes_read', 0)} bytes"
    if name == "list_files_real":
        return f"{name}:{status}:listed {len(tool_result.get('entries', []))} entries"
    if name in {"git_diff_real", "run_tests_real"}:
        return f"{name}:{status}:returncode {tool_result.get('returncode')}"
    return f"{name}:{status}"
