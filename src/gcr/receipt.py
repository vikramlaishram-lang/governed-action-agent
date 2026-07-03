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
        "review_status": envelope["review_status"],
        "approval_valid": envelope["approval_valid"],
        "approval_errors": envelope["approval_errors"],
        "reviewer_id": envelope["reviewer_authority_id"],
        "reviewer_role": envelope["reviewer_role"],
        "approval_token_id": envelope["approval_token_id"],
        "approval_scope": envelope["approval_scope"],
        "approval_expiry": envelope["approval_expiry"],
        "reviewer_identity_verified": envelope.get("reviewer_identity_verified", False),
        "reviewer_identity_errors": envelope.get("reviewer_identity_errors", []),
        "reviewer_identity_hash": envelope.get("reviewer_identity_hash"),
        "reviewer_registry_version": envelope.get("reviewer_registry_version"),
        "reviewer_issuer_id": envelope.get("reviewer_issuer_id"),
        "execution_status": envelope["execution_status"],
        "outcome_status": envelope["outcome_status"],
        "execution_authority_claimed": envelope["execution_authority_claimed"],
        "constitutional_errors": constitutional_errors,
        "tool_name": tool_result.get("tool_name"),
        "tool_executed": tool_result.get("tool_executed", False),
        "tool_status": tool_result.get("tool_status"),
        "tool_summary": _summarize_tool_result(tool_result),
        "tool_result_summary": _summarize_tool_result(tool_result),
        "evidence_references": envelope.get("evidence_references", []),
        "evidence_gaps": envelope.get("evidence_gap_summary", []),
        "github_pr": _github_pr_summary(tool_result),
        "code_change_proposal": _code_change_summary(tool_result),
        "record_hash": envelope["record_hash"],
        "created_at": datetime.now(UTC).isoformat(),
    }


def _summarize_tool_result(tool_result: dict) -> str:
    if "tool_result_summary" in tool_result:
        return tool_result["tool_result_summary"]
    if "summary" in tool_result:
        return tool_result["summary"]
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


def _github_pr_summary(tool_result: dict) -> dict | None:
    snapshot = tool_result.get("github_pr_snapshot")
    if not snapshot:
        return None
    return {
        "owner": snapshot["owner"],
        "repo": snapshot["repo"],
        "pr_number": snapshot["pr_number"],
        "evidence_hash": snapshot["evidence_hash"],
        "checks_passing": snapshot["checks_passing"],
        "risk_flags": snapshot["risk_flags"],
    }


def _code_change_summary(tool_result: dict) -> dict | None:
    proposal = tool_result.get("code_change_proposal")
    if not proposal:
        return None
    return {
        "proposal_artifact_id": proposal["proposal_artifact_id"],
        "target_files": proposal["target_files"],
        "change_intent": proposal["change_intent"],
        "diff_hash": proposal["diff_hash"],
        "risk_flags": proposal["risk_flags"],
        "requires_review": proposal["requires_review"],
        "applied_to_real_repo": proposal["applied_to_real_repo"],
    }
