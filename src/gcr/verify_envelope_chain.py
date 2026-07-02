from __future__ import annotations


def verify_constitutional_invariants(envelope: dict) -> list[str]:
    errors: list[str] = []
    if "agent_output_mode" not in envelope:
        errors.append("SCHEMA_ERROR")
    if "execution_authority_claimed" not in envelope:
        errors.append("SCHEMA_ERROR")

    if envelope.get("execution_authority_claimed") is True:
        errors.append("CONSTITUTIONAL_VIOLATION")

    if envelope.get("agent_output_mode") in {"ACTION_PROPOSAL", "EXECUTION_REQUEST"} and envelope.get(
        "execution_authority_claimed"
    ) is True:
        if "CONSTITUTIONAL_VIOLATION" not in errors:
            errors.append("CONSTITUTIONAL_VIOLATION")
    return errors
