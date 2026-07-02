from __future__ import annotations

from pathlib import Path

from .controlled_local_tools import execute_controlled_tool


def simulate_local_action(
    decision: str,
    constitutional_errors: list[str],
    *,
    root_path: str | Path,
    user_request: str,
) -> dict:
    if "CONSTITUTIONAL_VIOLATION" in constitutional_errors:
        return {
            "execution_status": "NOT_EXECUTED",
            "outcome_status": "BLOCKED",
            "tool_result": {
                "tool_name": None,
                "tool_executed": False,
                "tool_status": "NOT_INVOKED",
                "reason": "Constitutional violation",
            },
        }
    if decision == "ALLOW":
        tool_result = execute_controlled_tool(root_path, user_request)
        if tool_result["tool_status"] == "BLOCKED":
            return {"execution_status": "NOT_EXECUTED", "outcome_status": "BLOCKED", "tool_result": tool_result}
        if tool_result["tool_status"] == "FAILED":
            return {"execution_status": "NOT_EXECUTED", "outcome_status": "FAILED", "tool_result": tool_result}
        return {"execution_status": "EXECUTED", "outcome_status": "SUCCESS", "tool_result": tool_result}
    if decision == "DENY":
        return {
            "execution_status": "NOT_EXECUTED",
            "outcome_status": "BLOCKED",
            "tool_result": {
                "tool_name": None,
                "tool_executed": False,
                "tool_status": "NOT_INVOKED",
                "reason": "Policy denied request",
            },
        }
    if decision == "REQUEST_REVIEW":
        return {
            "execution_status": "NOT_EXECUTED",
            "outcome_status": "PENDING_REVIEW",
            "tool_result": {
                "tool_name": None,
                "tool_executed": False,
                "tool_status": "NOT_INVOKED",
                "reason": "Human review required",
            },
        }
    return {
        "execution_status": "NOT_EXECUTED",
        "outcome_status": "BLOCKED",
        "tool_result": {
            "tool_name": None,
            "tool_executed": False,
            "tool_status": "NOT_INVOKED",
            "reason": "Unknown policy decision",
        },
    }
