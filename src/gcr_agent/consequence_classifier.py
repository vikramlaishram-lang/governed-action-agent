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
    if ".env" in lowered or "secret" in lowered or "credentials" in lowered:
        return "SECRET_ACCESS"
    if "deploy" in lowered and "production" in lowered:
        return "PRODUCTION_STATE_CHANGE"
    if "delete" in lowered or "rm -rf" in lowered or "remove file" in lowered:
        return "IRREVERSIBLE_DELETE"
    if "workflow" in lowered or "github workflow" in lowered or "ci yaml" in lowered:
        return "WORKFLOW_CHANGE"
    if "propose readme update" in lowered or "update readme" in lowered or "patch readme" in lowered:
        return "CODE_CHANGE"
    if "run tests" in lowered or "pytest" in lowered or "test suite" in lowered:
        return "LOCAL_COMPUTATION"
    if any(term in lowered for term in ("write", "edit", "modify")):
        return "CODE_CHANGE"
    if "list files" in lowered or lowered.strip() == "ls" or "show files" in lowered:
        return "READ_ONLY_ACCESS"
    if "git diff" in lowered or "show diff" in lowered or "status" in lowered:
        return "READ_ONLY_ACCESS"
    if any(term in lowered for term in ("read", "open", "show")):
        return "READ_ONLY_ACCESS"
    return "UNKNOWN"
