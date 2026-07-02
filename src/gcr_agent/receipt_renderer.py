from __future__ import annotations

from gcr.receipt import create_receipt


def render_receipt(
    goal_contract: dict,
    envelope: dict,
    constitutional_errors: list[str],
    tool_result: dict,
) -> dict:
    return create_receipt(
        goal_contract=goal_contract,
        envelope=envelope,
        constitutional_errors=constitutional_errors,
        tool_result=tool_result,
    )
