from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from .replay_verifier import replay_records, verify_ledger


DECISION_KEYS = ("ALLOW", "DENY", "REQUEST_REVIEW", "BLOCKED")


def generate_report_summary(
    *,
    ledger_path: str | Path,
    project_config: dict | None = None,
    hmac_key: str | None = None,
    expected_key_id: str | None = None,
    reviewer_registry=None,
) -> dict:
    ledger_path = Path(ledger_path)
    verification = verify_ledger(
        ledger_path,
        hmac_key=hmac_key,
        expected_key_id=expected_key_id,
        reviewer_registry=reviewer_registry,
    )
    records = replay_records(ledger_path)
    decision_counts = {key: verification.get("decision_counts", {}).get(key, 0) for key in DECISION_KEYS}
    execution_auth_errors = [error for error in verification["errors"] if "EXECUTION_WITHOUT_AUTHORIZATION" in error]
    execution_auth_errors.extend(
        error
        for record in records
        for error in record.get("verification_errors", [])
        if error == "EXECUTION_WITHOUT_AUTHORIZATION"
    )

    summary = {
        "schema_version": "governed_agent_report_v0.1",
        "generated_at": datetime.now(UTC).isoformat(),
        "project": {
            "project_name": (project_config or {}).get("project_name"),
            "ledger_path": str(ledger_path),
            "policy_path": (project_config or {}).get("policy_path"),
            "ledger_auth_mode": (project_config or {}).get("ledger_auth_mode"),
            "ledger_key_id": (project_config or {}).get("ledger_key_id"),
        },
        "ledger": {
            "valid": verification["valid"],
            "record_count": verification["record_count"],
            "latest_hash": verification["latest_hash"],
            "latest_hash_present": bool(verification["latest_hash"]),
            "auth_modes_seen": verification.get("auth_modes_seen", []),
            "hmac_record_count": verification.get("hmac_record_count", 0),
            "unkeyed_record_count": verification.get("unkeyed_record_count", 0),
            "errors": verification["errors"],
        },
        "decisions": decision_counts,
        "violations": {
            "constitutional_violation_count": verification["constitutional_violation_count"],
            "execution_authorization_violation_count": len(set(execution_auth_errors)),
            "errors": verification["errors"],
        },
        "review": {
            "review_approved_count": 0,
            "review_pending_count": 0,
            "review_rejected_count": 0,
            "review_approved_actions": [],
        },
        "reviewer_identity": {
            "reviewer_registry_version": getattr(reviewer_registry, "registry_version", None),
            "reviewer_issuer_id": getattr(reviewer_registry, "issuer_id", None),
            "approved_actions_with_verified_identity": 0,
            "approved_actions_missing_identity": 0,
            "reviewer_identity_errors": [],
        },
        "actions": {
            "denied_actions": [],
            "request_review_actions": [],
            "executed_actions": [],
        },
        "github_pr_evidence": [],
        "code_change_proposals": [],
        "public_claims_allowed": [],
        "limitations": _limitations(),
    }

    for record in records:
        receipt = record.get("receipt", {})
        envelope = record.get("envelope", {})
        review_status = receipt.get("review_status") or envelope.get("review_status")
        if review_status == "APPROVED":
            summary["review"]["review_approved_count"] += 1
        elif review_status in {"PENDING", "REQUESTED"}:
            summary["review"]["review_pending_count"] += 1
        elif review_status == "REJECTED":
            summary["review"]["review_rejected_count"] += 1

        if review_status == "APPROVED" and receipt.get("approval_valid") is True and receipt.get("decision") == "ALLOW":
            summary["review"]["review_approved_actions"].append(_review_action(receipt))
            if receipt.get("reviewer_identity_verified") is True:
                summary["reviewer_identity"]["approved_actions_with_verified_identity"] += 1
            else:
                summary["reviewer_identity"]["approved_actions_missing_identity"] += 1
        summary["reviewer_identity"]["reviewer_identity_errors"].extend(receipt.get("reviewer_identity_errors", []))

        action = _action_summary(receipt)
        if receipt.get("decision") == "DENY":
            summary["actions"]["denied_actions"].append(action)
        if receipt.get("decision") == "REQUEST_REVIEW":
            summary["actions"]["request_review_actions"].append(action)
        if receipt.get("execution_status") == "EXECUTED":
            summary["actions"]["executed_actions"].append(action)

        github_pr = receipt.get("github_pr") or _github_pr_from_tool(record.get("tool_result", {}))
        if github_pr:
            summary["github_pr_evidence"].append(github_pr)
        code_change = receipt.get("code_change_proposal")
        if code_change:
            code_change = dict(code_change)
            code_change.update(
                {
                    "proposal_id": receipt.get("proposal_id"),
                    "decision": receipt.get("decision"),
                    "execution_status": receipt.get("execution_status"),
                }
            )
            summary["code_change_proposals"].append(code_change)

    summary["public_claims_allowed"] = derive_public_claims(summary)
    return summary


def generate_markdown_report(summary: dict) -> str:
    lines = [
        "# Governed Action Agent Report",
        "",
        "## Project Summary",
        f"- Project: {summary['project']['project_name']}",
        f"- Ledger path: {summary['project']['ledger_path']}",
        f"- Policy path: {summary['project']['policy_path']}",
        "",
        "## Ledger Integrity",
        f"- Ledger valid: {str(summary['ledger']['valid']).lower()}",
        f"- Record count: {summary['ledger']['record_count']}",
        f"- Latest hash: {summary['ledger']['latest_hash']}",
        f"- Auth modes: {', '.join(summary['ledger']['auth_modes_seen']) or 'none'}",
        "",
        "## Decision Summary",
    ]
    lines.extend(f"- {key}: {value}" for key, value in summary["decisions"].items())
    lines.extend(
        [
            "",
            "## Violations",
            f"- Constitutional violations: {summary['violations']['constitutional_violation_count']}",
            f"- Execution authorization violations: {summary['violations']['execution_authorization_violation_count']}",
            "",
            "## Review-Approved Actions",
        ]
    )
    lines.extend(_bullets(summary["review"]["review_approved_actions"], "normalized_action"))
    lines.append("")
    lines.append("## Denied Actions")
    lines.extend(_bullets(summary["actions"]["denied_actions"], "normalized_action"))
    lines.append("")
    lines.append("## Request-Review Actions")
    lines.extend(_bullets(summary["actions"]["request_review_actions"], "normalized_action"))
    lines.append("")
    lines.append("## GitHub PR Evidence")
    lines.extend(_github_bullets(summary["github_pr_evidence"]))
    lines.append("")
    lines.append("## Reviewer Identity")
    lines.append(f"- Registry version: {summary['reviewer_identity']['reviewer_registry_version']}")
    lines.append(f"- Issuer id: {summary['reviewer_identity']['reviewer_issuer_id']}")
    lines.append(
        f"- Verified reviewer-approved actions: {summary['reviewer_identity']['approved_actions_with_verified_identity']}"
    )
    lines.append(f"- Reviewer identity errors: {len(summary['reviewer_identity']['reviewer_identity_errors'])}")
    lines.append("")
    lines.append("## Code Change Proposals")
    lines.extend(_code_change_bullets(summary["code_change_proposals"]))
    lines.append("")
    lines.append("## Public Claims Allowed by Evidence")
    lines.extend(f"- {claim}" for claim in summary["public_claims_allowed"])
    lines.append("")
    lines.append("## Limitations / Non-Claims")
    lines.extend(f"- {limitation}" for limitation in summary["limitations"])
    lines.append("")
    return "\n".join(lines)


def write_report_files(
    *,
    summary: dict,
    output_dir: str | Path,
    markdown_filename: str = "governed_agent_report.md",
    json_filename: str = "governed_agent_report.json",
) -> dict:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    markdown_path = output / markdown_filename
    json_path = output / json_filename
    markdown_path.write_text(generate_markdown_report(summary), encoding="utf-8")
    json_path.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {"markdown_path": markdown_path, "json_path": json_path}


def derive_public_claims(summary: dict) -> list[str]:
    if not summary["ledger"]["valid"]:
        return ["A report was generated, but the ledger did not verify."]
    claims: list[str] = []
    if summary["ledger"]["record_count"] > 0:
        claims.extend(
            [
                "The governed agent produced a verifiable local receipt ledger.",
                "The ledger replay verified successfully.",
                "The report summarizes decisions from verified local ledger records.",
            ]
        )
    if summary["ledger"]["latest_hash_present"]:
        claims.append("The report includes the latest ledger hash.")
    if summary["ledger"]["hmac_record_count"] > 0:
        claims.append("The ledger includes HMAC-authenticated records verified with the provided key.")
    if summary["violations"]["constitutional_violation_count"] > 0:
        claims.append("The ledger records at least one self-authorization attempt detected as CONSTITUTIONAL_VIOLATION.")
    if summary["violations"]["execution_authorization_violation_count"] == 0:
        claims.append("No execution-without-ALLOW violation was detected during replay.")
    if summary["github_pr_evidence"]:
        claims.append("The report includes read-only GitHub PR evidence snapshots.")
    if summary.get("code_change_proposals"):
        claims.append("The report includes sandboxed code-change proposal records.")
        if all(item.get("applied_to_real_repo") is False for item in summary["code_change_proposals"]):
            claims.append("The recorded code-change proposals indicate applied_to_real_repo=false.")
    if summary.get("reviewer_identity", {}).get("approved_actions_with_verified_identity", 0) > 0:
        claims.append("The report includes reviewer-approved actions with local reviewer identity verification.")
    return claims


def _action_summary(receipt: dict) -> dict:
    return {
        "proposal_id": receipt.get("proposal_id"),
        "agent_id": receipt.get("agent_id"),
        "user_request": receipt.get("user_request"),
        "normalized_action": receipt.get("normalized_action"),
        "consequence_class": receipt.get("consequence_class"),
        "decision": receipt.get("decision"),
        "execution_status": receipt.get("execution_status"),
        "outcome_status": receipt.get("outcome_status"),
        "receipt_id": receipt.get("receipt_id"),
    }


def _review_action(receipt: dict) -> dict:
    return {
        "proposal_id": receipt.get("proposal_id"),
        "normalized_action": receipt.get("normalized_action"),
        "consequence_class": receipt.get("consequence_class"),
        "reviewer_id": receipt.get("reviewer_id"),
        "reviewer_role": receipt.get("reviewer_role"),
        "approval_token_id": receipt.get("approval_token_id"),
        "approval_scope": receipt.get("approval_scope"),
        "approval_expiry": receipt.get("approval_expiry"),
    }


def _github_pr_from_tool(tool_result: dict) -> dict | None:
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


def _bullets(items: list[dict], field: str) -> list[str]:
    if not items:
        return ["- none"]
    return [f"- {item.get(field)} ({item.get('decision', item.get('consequence_class'))})" for item in items]


def _github_bullets(items: list[dict]) -> list[str]:
    if not items:
        return ["- none"]
    return [
        f"- {item['owner']}/{item['repo']}#{item['pr_number']} checks_passing={str(item['checks_passing']).lower()} risk_flags={','.join(item['risk_flags']) or 'none'}"
        for item in items
    ]


def _code_change_bullets(items: list[dict]) -> list[str]:
    if not items:
        return ["- none"]
    return [
        f"- {','.join(item['target_files'])} decision={item['decision']} applied_to_real_repo={str(item['applied_to_real_repo']).lower()} diff_hash={item['diff_hash']}"
        for item in items
    ]


def _limitations() -> list[str]:
    return [
        "This report is generated from local ledger records.",
        "Ledger verification is only as strong as the available ledger and key material.",
        "UNKEYED_HASH_CHAIN mode is tamper-evident, not authenticated.",
        "HMAC_SHA256_V1 mode requires correct key handling outside this prototype.",
        "This report does not prove production safety.",
        "This report does not prove that all possible governance violations are detected.",
        "This report does not certify external audit completion.",
        "This system does not perform real production deployment.",
    ]
