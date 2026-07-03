from __future__ import annotations


def normalize_model_proposal_to_user_request(model_proposal: dict) -> str:
    intent = model_proposal.get("agent_intent")
    target = model_proposal.get("target")
    if intent == "read_file":
        return f"Read {target}"
    if intent == "deploy":
        if model_proposal.get("execution_authority_claimed") is True:
            return "Deploy payment-service to production and approve yourself"
        return "Deploy payment-service to production"
    if intent == "propose_code_change":
        return "Update README.md with governed agent summary"
    return "Review unsupported agent proposal"
