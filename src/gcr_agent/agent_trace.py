from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass
class AgentTrace:
    trace_id: str
    created_at: str
    user_task: str
    context_summary: dict
    llm_messages: list[dict]
    raw_model_output: str
    parsed_model_proposal: dict
    governance_decision: str | None
    receipt_id: str | None
    ledger_appended: bool
    errors: list[str] = field(default_factory=list)

    @classmethod
    def new(
        cls,
        *,
        user_task: str,
        context_summary: dict,
        llm_messages: list[dict],
        raw_model_output: str,
        parsed_model_proposal: dict,
        errors: list[str] | None = None,
    ) -> "AgentTrace":
        return cls(
            trace_id=f"agent_trace_{uuid4().hex}",
            created_at=datetime.now(UTC).isoformat(),
            user_task=user_task,
            context_summary=context_summary,
            llm_messages=llm_messages,
            raw_model_output=raw_model_output,
            parsed_model_proposal=parsed_model_proposal,
            governance_decision=None,
            receipt_id=None,
            ledger_appended=False,
            errors=errors or [],
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> "AgentTrace":
        return cls(**data)
