from __future__ import annotations

import hashlib
import json
from pathlib import Path

from gcr.proposal import normalize_model_proposal_to_user_request

from .agent_context import collect_repo_context
from .agent_trace import AgentTrace
from .governed_agent import GovernedAgent
from .llm_client import FakeLLMClient, LLMClient


SYSTEM_PROMPT = (
    "You are an AI coding/release agent. You may propose actions but you may not authorize execution. "
    "Return only JSON."
)


class GovernedAgentRuntime:
    def __init__(
        self,
        *,
        root: Path,
        governed_agent: GovernedAgent,
        llm_client: LLMClient | None = None,
    ) -> None:
        self.root = Path(root)
        self.governed_agent = governed_agent
        self.llm_client = llm_client or FakeLLMClient()

    def run_task(self, user_task: str, *, review_token=None) -> dict:
        context = collect_repo_context(self.root)
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_task},
            {"role": "system", "content": json.dumps({"repo_context": context}, sort_keys=True)},
        ]
        raw_output = self.llm_client.complete(messages, response_format="json")
        errors: list[str] = []
        try:
            model_proposal = json.loads(raw_output)
        except json.JSONDecodeError:
            model_proposal = {"agent_intent": "unknown", "target": None, "requested_tool": None}
            errors.append("MODEL_OUTPUT_JSON_PARSE_FAILED")
        if "decision" in model_proposal:
            errors.append("MODEL_DECISION_CLAIM_IGNORED")
        if "execution_status" in model_proposal:
            errors.append("MODEL_EXECUTION_STATUS_CLAIM_IGNORED")

        trace = AgentTrace.new(
            user_task=user_task,
            context_summary=context,
            llm_messages=messages,
            raw_model_output=raw_output,
            parsed_model_proposal=model_proposal,
            errors=errors,
        )
        agent_run = {
            "trace_id": trace.trace_id,
            "model_provider": self.llm_client.__class__.__name__,
            "model_proposal_hash": _hash_text(raw_output),
            "model_intent": model_proposal.get("agent_intent"),
            "requested_tool": model_proposal.get("requested_tool"),
            "model_decision_claim_ignored": "MODEL_DECISION_CLAIM_IGNORED" in errors,
            "model_execution_status_claim_ignored": "MODEL_EXECUTION_STATUS_CLAIM_IGNORED" in errors,
        }

        normalized_request = normalize_model_proposal_to_user_request(model_proposal)
        if model_proposal.get("agent_intent") == "propose_code_change":
            governed_result = self.governed_agent.propose_code_change(
                normalized_request,
                review_token=review_token,
                agent_run=agent_run,
            )
        else:
            governed_result = self.governed_agent.handle_request(
                normalized_request,
                review_token=review_token,
                agent_run=agent_run,
            )

        decision = governed_result["envelope"]["decision"]
        if "CONSTITUTIONAL_VIOLATION" in governed_result["verification_errors"]:
            decision = "CONSTITUTIONAL_VIOLATION"
        trace.governance_decision = decision
        trace.receipt_id = governed_result["receipt"]["receipt_id"]
        trace.ledger_appended = "ledger_record" in governed_result
        trace_dict = trace.to_dict()
        return {
            "agent_run": True,
            "trace": trace_dict,
            "decision": decision,
            "consequence_class": governed_result["proposal"]["consequence_class"],
            "receipt_id": governed_result["receipt"]["receipt_id"],
            "ledger_appended": "ledger_record" in governed_result,
            "real_repo_modified": False,
            "model_proposal": model_proposal,
            "governed_result": governed_result,
        }


def _hash_text(value: str) -> str:
    return f"sha256:{hashlib.sha256(value.encode('utf-8')).hexdigest()}"
