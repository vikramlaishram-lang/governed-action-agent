from __future__ import annotations


def sample_viewer_summary() -> dict:
    return {
        "schema_version": "governed_agent_report_v0.1",
        "generated_at": "2026-07-03T00:00:00+00:00",
        "project": {
            "project_name": "demo",
            "ledger_path": ".governed-agent/ledger.jsonl",
            "policy_path": ".governed-agent/policy.json",
            "ledger_auth_mode": "HMAC_SHA256_V1",
            "ledger_key_id": "local-dev-key",
        },
        "ledger": {
            "valid": True,
            "record_count": 5,
            "latest_hash": "sha256:latest",
            "latest_hash_present": True,
            "auth_modes_seen": ["HMAC_SHA256_V1"],
            "hmac_record_count": 5,
            "unkeyed_record_count": 0,
            "errors": [],
        },
        "decisions": {"ALLOW": 1, "DENY": 1, "REQUEST_REVIEW": 2, "BLOCKED": 1},
        "violations": {
            "constitutional_violation_count": 1,
            "execution_authorization_violation_count": 0,
            "errors": ["CONSTITUTIONAL_VIOLATION"],
        },
        "review": {
            "review_approved_count": 1,
            "review_pending_count": 2,
            "review_rejected_count": 0,
            "review_approved_actions": [
                {
                    "proposal_id": "proposal-approved",
                    "normalized_action": "deploy payment-service",
                    "consequence_class": "PRODUCTION_STATE_CHANGE",
                    "reviewer_id": "alice-release",
                    "reviewer_role": "release_manager",
                    "approval_token_id": "approval-token-id",
                    "approval_scope": "PRODUCTION_STATE_CHANGE",
                    "approval_expiry": "2026-07-04T00:00:00+00:00",
                }
            ],
        },
        "reviewer_identity": {
            "reviewer_registry_version": "reviewer_identity_manifest_v0.1",
            "reviewer_issuer_id": "local-reviewer-registry",
            "approved_actions_with_verified_identity": 1,
            "approved_actions_missing_identity": 0,
            "reviewer_identity_errors": [],
        },
        "actions": {
            "denied_actions": [
                {
                    "proposal_id": "proposal-denied",
                    "normalized_action": "read .env",
                    "consequence_class": "SECRET_ACCESS",
                    "decision": "DENY",
                    "execution_status": "NOT_EXECUTED",
                    "receipt_id": "receipt-denied",
                }
            ],
            "request_review_actions": [
                {
                    "proposal_id": "proposal-review",
                    "normalized_action": "update README.md",
                    "consequence_class": "CODE_CHANGE",
                    "decision": "REQUEST_REVIEW",
                    "execution_status": "NOT_EXECUTED",
                    "receipt_id": "receipt-review",
                }
            ],
            "executed_actions": [],
        },
        "github_pr_evidence": [
            {
                "owner": "vikramlaishram-lang",
                "repo": "governed-action-agent",
                "pr_number": 42,
                "evidence_hash": "sha256:evidence",
                "checks_passing": True,
                "risk_flags": ["checks_passed"],
                "patch": "do not persist this patch",
            }
        ],
        "code_change_proposals": [
            {
                "proposal_id": "proposal-code",
                "proposal_artifact_id": "code-change-1",
                "target_files": ["README.md"],
                "change_intent": "Add governed agent note",
                "diff_hash": "sha256:diff",
                "diff_text": "Governed Action Agent Note",
                "patch_text": "full patch text",
                "risk_flags": ["CODE_CHANGE"],
                "requires_review": True,
                "applied_to_real_repo": False,
                "decision": "REQUEST_REVIEW",
                "execution_status": "NOT_EXECUTED",
            }
        ],
        "public_claims_allowed": [
            "The governed agent produced a verifiable local receipt ledger.",
            "The report includes sandboxed code-change proposal records.",
        ],
        "limitations": [
            "This report does not prove production safety.",
            "This system does not perform real production deployment.",
        ],
        "GAA_LEDGER_HMAC_KEY": "super-secret-key",
        "GITHUB_TOKEN": "ghp_not_allowed",
        "authorization": "Bearer secret",
        "credentials": ".env SECRET=do-not-expose",
    }
