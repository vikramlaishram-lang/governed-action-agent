from __future__ import annotations

from dataclasses import asdict, dataclass
from uuid import uuid4


@dataclass(frozen=True)
class GoalContract:
    goal_id: str
    user_request: str
    bounded_goal: str
    non_goals: list[str]
    success_criteria: list[str]


def create_goal_contract(user_request: str) -> dict:
    lowered = user_request.lower()
    if "deploy" in lowered and "production" in lowered:
        bounded_goal = "Prepare a governed deployment proposal for payment-service to production"
        non_goals = ["Do not execute deployment without review", "Do not claim approval"]
        success_criteria = [
            "Consequence classified",
            "Decision envelope created",
            "Review requested if required",
        ]
    elif ".env" in lowered or "secret" in lowered:
        bounded_goal = f"Prepare a governed access proposal for: {user_request}"
        non_goals = ["Do not read secrets", "Do not expose sensitive values"]
        success_criteria = ["Consequence classified", "Decision envelope created", "Unsafe access denied"]
    else:
        bounded_goal = f"Prepare a governed action proposal for: {user_request}"
        non_goals = ["Do not execute outside the policy decision", "Do not claim approval"]
        success_criteria = ["Consequence classified", "Decision envelope created", "Receipt generated"]

    return asdict(
        GoalContract(
            goal_id=f"goal_{uuid4().hex}",
            user_request=user_request,
            bounded_goal=bounded_goal,
            non_goals=non_goals,
            success_criteria=success_criteria,
        )
    )
