from __future__ import annotations


CONSEQUENCE_CLASSES = {
    "READ_ONLY_ACCESS",
    "LOCAL_COMPUTATION",
    "TEXT_GENERATION",
    "CODE_CHANGE",
    "WORKFLOW_CHANGE",
    "SECRET_ACCESS",
    "DATA_EXPORT",
    "PRODUCTION_STATE_CHANGE",
    "IRREVERSIBLE_DELETE",
    "UNKNOWN",
}


def classify_consequence(user_request: str) -> str:
    lowered = user_request.lower()
    if ".env" in lowered or "secret" in lowered:
        return "SECRET_ACCESS"
    if "deploy" in lowered and "production" in lowered:
        return "PRODUCTION_STATE_CHANGE"
    if "delete" in lowered or "rm -rf" in lowered:
        return "IRREVERSIBLE_DELETE"
    if any(term in lowered for term in ("write", "edit", "modify")):
        return "CODE_CHANGE"
    if any(term in lowered for term in ("read", "open", "show")):
        return "READ_ONLY_ACCESS"
    return "UNKNOWN"
