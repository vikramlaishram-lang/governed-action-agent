from __future__ import annotations

import copy
import html
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


FORBIDDEN_KEY_PARTS = (
    "gaa_ledger_hmac_key",
    "github_token",
    "authorization",
    "token_secret",
    "hmac_key",
    "diff_text",
    "patch",
    "private_key",
)
FORBIDDEN_VALUE_PARTS = (
    "GAA_LEDGER_HMAC_KEY",
    "GITHUB_TOKEN",
    "authorization:",
    "bearer ",
    "token_secret",
    "hmac_key",
    "-----BEGIN PRIVATE KEY-----",
)


def generate_viewer_data(summary: dict) -> dict:
    data = {
        "schema_version": "governed_agent_viewer_v0.1",
        "generated_at": datetime.now(UTC).isoformat(),
        "project": summary.get("project", {}),
        "ledger": summary.get("ledger", {}),
        "decisions": summary.get("decisions", {}),
        "violations": summary.get("violations", {}),
        "review": summary.get("review", {}),
        "reviewer_identity": summary.get("reviewer_identity", {}),
        "actions": summary.get("actions", {}),
        "github_pr_evidence": summary.get("github_pr_evidence", []),
        "code_change_proposals": summary.get("code_change_proposals", []),
        "public_claims_allowed": summary.get("public_claims_allowed", []),
        "limitations": summary.get("limitations", []),
    }
    return sanitize_viewer_data(data)


def sanitize_viewer_data(data: dict) -> dict:
    return _sanitize(copy.deepcopy(data))


def generate_viewer_html(viewer_data: dict) -> str:
    data = sanitize_viewer_data(viewer_data)
    json_data = json.dumps(data, sort_keys=True)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Governed Action Agent Receipt Viewer</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; color: #17202a; background: #f7f8fa; }}
    main {{ max-width: 1120px; margin: 0 auto; padding: 32px 20px 48px; }}
    h1 {{ font-size: 32px; margin: 0 0 24px; }}
    h2 {{ font-size: 18px; margin: 0 0 12px; }}
    section {{ background: white; border: 1px solid #d8dee6; border-radius: 8px; padding: 16px; margin: 12px 0; }}
    dl {{ display: grid; grid-template-columns: minmax(180px, 260px) 1fr; gap: 8px 16px; margin: 0; }}
    dt {{ font-weight: 700; color: #334155; }}
    dd {{ margin: 0; overflow-wrap: anywhere; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border-bottom: 1px solid #e6eaf0; padding: 8px; text-align: left; vertical-align: top; overflow-wrap: anywhere; }}
    th {{ color: #334155; font-size: 13px; }}
    ul {{ margin: 0; padding-left: 20px; }}
    .status-true {{ color: #087443; font-weight: 700; }}
    .status-false {{ color: #b42318; font-weight: 700; }}
    .empty {{ color: #64748b; }}
  </style>
</head>
<body>
  <main>
    <h1>Governed Action Agent Receipt Viewer</h1>
    {_section_project(data)}
    {_section_ledger(data)}
    {_section_decisions(data)}
    {_section_violations(data)}
    {_section_reviewer_identity(data)}
    {_section_actions('Review-Approved Actions', data.get('review', {}).get('review_approved_actions', []))}
    {_section_actions('Denied Actions', data.get('actions', {}).get('denied_actions', []))}
    {_section_actions('Request-Review Actions', data.get('actions', {}).get('request_review_actions', []))}
    {_section_github(data)}
    {_section_code_changes(data)}
    {_section_list('Public Claims Allowed by Evidence', data.get('public_claims_allowed', []))}
    {_section_list('Limitations / Non-Claims', data.get('limitations', []))}
    {_section_latest_hash(data)}
  </main>
  <script type="application/json" id="viewer-data">{html.escape(json_data)}</script>
</body>
</html>
"""


def write_viewer_bundle(
    *,
    summary: dict,
    output_dir: str | Path,
    index_filename: str = "index.html",
    data_filename: str = "viewer_data.json",
) -> dict:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    viewer_data = generate_viewer_data(summary)
    index_path = output / index_filename
    data_path = output / data_filename
    index_path.write_text(generate_viewer_html(viewer_data), encoding="utf-8")
    data_path.write_text(json.dumps(viewer_data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "viewer_generated": True,
        "index_path": str(index_path),
        "data_path": str(data_path),
        "record_count": int(viewer_data.get("ledger", {}).get("record_count", 0)),
        "ledger_valid": bool(viewer_data.get("ledger", {}).get("valid", False)),
        "public_claims_count": len(viewer_data.get("public_claims_allowed", [])),
    }


def _sanitize(value: Any) -> Any:
    if isinstance(value, dict):
        cleaned = {}
        for key, item in value.items():
            key_text = str(key)
            lowered = key_text.lower()
            if any(part in lowered for part in FORBIDDEN_KEY_PARTS):
                cleaned[key_text] = "[REDACTED]"
            else:
                cleaned[key_text] = _sanitize(item)
        return cleaned
    if isinstance(value, list):
        return [_sanitize(item) for item in value]
    if isinstance(value, str):
        lowered = value.lower()
        if any(part.lower() in lowered for part in FORBIDDEN_VALUE_PARTS):
            return "[REDACTED]"
        if ".env" in lowered and ("=" in value or "secret" in lowered or "password" in lowered):
            return "[REDACTED]"
    return value


def _section_project(data: dict) -> str:
    project = data.get("project", {})
    return _details(
        "Project Summary",
        {
            "Project": project.get("project_name"),
            "Ledger path": project.get("ledger_path"),
            "Policy path": project.get("policy_path"),
            "Auth mode": project.get("ledger_auth_mode"),
            "Key id": project.get("ledger_key_id"),
        },
    )


def _section_ledger(data: dict) -> str:
    ledger = data.get("ledger", {})
    return _details(
        "Ledger Integrity",
        {
            "Ledger valid": _bool_text(ledger.get("valid")),
            "Record count": ledger.get("record_count"),
            "Latest hash present": _bool_text(ledger.get("latest_hash_present")),
            "Auth modes seen": ", ".join(ledger.get("auth_modes_seen", [])) or "none",
            "HMAC record count": ledger.get("hmac_record_count"),
            "Unkeyed record count": ledger.get("unkeyed_record_count"),
        },
    )


def _section_decisions(data: dict) -> str:
    return _details("Decision Summary", data.get("decisions", {}))


def _section_violations(data: dict) -> str:
    violations = data.get("violations", {})
    return _details(
        "Violations",
        {
            "Constitutional violations": violations.get("constitutional_violation_count"),
            "Execution authorization violations": violations.get("execution_authorization_violation_count"),
        },
    )


def _section_reviewer_identity(data: dict) -> str:
    identity = data.get("reviewer_identity", {})
    return _details(
        "Reviewer Identity",
        {
            "Registry version": identity.get("reviewer_registry_version"),
            "Issuer id": identity.get("reviewer_issuer_id"),
            "Verified approved actions": identity.get("approved_actions_with_verified_identity"),
            "Approved actions missing identity": identity.get("approved_actions_missing_identity"),
            "Reviewer identity errors": len(identity.get("reviewer_identity_errors", [])),
        },
    )


def _section_actions(title: str, items: list[dict]) -> str:
    if not items:
        return f"<section><h2>{html.escape(title)}</h2><p class=\"empty\">none</p></section>"
    rows = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{_esc(item.get('receipt_id') or item.get('proposal_id'))}</td>"
            f"<td>{_esc(item.get('normalized_action'))}</td>"
            f"<td>{_esc(item.get('consequence_class'))}</td>"
            f"<td>{_esc(item.get('decision'))}</td>"
            f"<td>{_esc(item.get('execution_status'))}</td>"
            "</tr>"
        )
    return (
        f"<section><h2>{html.escape(title)}</h2><table><thead><tr><th>ID</th><th>Action</th>"
        "<th>Consequence</th><th>Decision</th><th>Execution</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></section>"
    )


def _section_github(data: dict) -> str:
    items = data.get("github_pr_evidence", [])
    if not items:
        return '<section><h2>GitHub PR Evidence</h2><p class="empty">none</p></section>'
    rows = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{_esc(item.get('owner'))}/{_esc(item.get('repo'))}#{_esc(item.get('pr_number'))}</td>"
            f"<td>{_esc(item.get('evidence_hash'))}</td>"
            f"<td>{_esc(item.get('checks_passing'))}</td>"
            f"<td>{_esc(', '.join(item.get('risk_flags', [])) or 'none')}</td>"
            "</tr>"
        )
    return (
        "<section><h2>GitHub PR Evidence</h2><table><thead><tr><th>PR</th><th>Evidence hash</th>"
        "<th>Checks passing</th><th>Risk flags</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></section>"
    )


def _section_code_changes(data: dict) -> str:
    items = data.get("code_change_proposals", [])
    if not items:
        return '<section><h2>Code Change Proposals</h2><p class="empty">none</p></section>'
    rows = []
    for item in items:
        rows.append(
            "<tr>"
            f"<td>{_esc(item.get('proposal_artifact_id') or item.get('proposal_id'))}</td>"
            f"<td>{_esc(', '.join(item.get('target_files', [])))}</td>"
            f"<td>{_esc(item.get('diff_hash'))}</td>"
            f"<td>{_esc(item.get('applied_to_real_repo'))}</td>"
            f"<td>{_esc(', '.join(item.get('risk_flags', [])) or 'none')}</td>"
            "</tr>"
        )
    return (
        "<section><h2>Code Change Proposals</h2><table><thead><tr><th>Proposal</th><th>Targets</th>"
        "<th>Diff hash</th><th>Applied to real repo</th><th>Risk flags</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></section>"
    )


def _section_list(title: str, items: list[str]) -> str:
    rendered = "".join(f"<li>{_esc(item)}</li>" for item in items) or '<li class="empty">none</li>'
    return f"<section><h2>{html.escape(title)}</h2><ul>{rendered}</ul></section>"


def _section_latest_hash(data: dict) -> str:
    return _details("Latest Hash", {"Latest hash": data.get("ledger", {}).get("latest_hash") or "none"})


def _details(title: str, values: dict) -> str:
    rows = "".join(f"<dt>{_esc(key)}</dt><dd>{_format_value(value)}</dd>" for key, value in values.items())
    return f"<section><h2>{html.escape(title)}</h2><dl>{rows}</dl></section>"


def _format_value(value: Any) -> str:
    if isinstance(value, str) and value in {"true", "false"}:
        return f'<span class="status-{value}">{value}</span>'
    return _esc(value if value is not None else "null")


def _bool_text(value: Any) -> str:
    return "true" if bool(value) else "false"


def _esc(value: Any) -> str:
    return html.escape(str(value))
