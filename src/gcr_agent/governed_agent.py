from __future__ import annotations

from pathlib import Path

from gcr.policy_engine import apply_policy
from gcr.policy_loader import load_policy
from gcr.proposal_object import create_proposal_object
from gcr.proposal_to_envelope import proposal_to_envelope
from gcr.receipt_ledger import ReceiptLedger
from gcr.reviewer_registry import ReviewerAuthorityRegistry, load_reviewer_registry
from gcr.verify_envelope_chain import verify_constitutional_invariants

from .consequence_classifier import classify_consequence
from .code_change_planner import CodeChangePlanner, CodeChangePlanningError
from .github_pr_reader import GitHubPRReader
from .goal_contract import create_goal_contract
from .identity_manifest import get_identity_manifest
from .local_action_simulator import simulate_local_action
from .output_mode_labeler import label_output_mode
from .receipt_renderer import render_receipt


class GovernedAgent:
    def __init__(
        self,
        runtime_id: str = "local_simulator",
        root_path: str | Path | None = None,
        ledger_path: str | Path | None = None,
        ledger_auth_mode: str | None = None,
        ledger_hmac_key: str | None = None,
        ledger_key_id: str | None = None,
        policy_path: str | Path | None = None,
        reviewer_registry_path: str | Path | None = None,
        reviewer_registry: dict | ReviewerAuthorityRegistry | None = None,
    ) -> None:
        self.runtime_id = runtime_id
        self.root_path = Path(root_path or Path.cwd()).resolve()
        self.policy = load_policy(policy_path) if policy_path is not None else None
        if reviewer_registry is not None:
            self.reviewer_registry = (
                ReviewerAuthorityRegistry(reviewer_registry) if isinstance(reviewer_registry, dict) else reviewer_registry
            )
        elif reviewer_registry_path is not None:
            self.reviewer_registry = load_reviewer_registry(reviewer_registry_path)
        else:
            self.reviewer_registry = None
        self.ledger = (
            ReceiptLedger(
                ledger_path,
                auth_mode=ledger_auth_mode,
                hmac_key=ledger_hmac_key,
                key_id=ledger_key_id,
            )
            if ledger_path is not None
            else None
        )

    def prepare_request(self, user_request: str) -> dict:
        identity = get_identity_manifest()
        goal_contract = create_goal_contract(user_request)
        output_mode, output_mode_basis, execution_authority_claimed = label_output_mode(user_request)
        consequence_class = classify_consequence(user_request)

        proposal = create_proposal_object(
            agent_id=identity["agent_id"],
            user_request=user_request,
            agent_output_mode=output_mode,
            agent_output_mode_basis=output_mode_basis,
            execution_authority_claimed=execution_authority_claimed,
            consequence_class=consequence_class,
        )
        return {"goal_contract": goal_contract, "proposal": proposal}

    def evaluate_proposal(
        self,
        goal_contract: dict,
        proposal: dict,
        review_token: dict | None = None,
        agent_run: dict | None = None,
    ) -> dict:
        policy_result = apply_policy(
            proposal,
            review_token=review_token,
            policy=self.policy,
            reviewer_registry=self.reviewer_registry,
        )
        envelope = proposal_to_envelope(proposal, policy_result, runtime_id=self.runtime_id)
        verification_errors = verify_constitutional_invariants(envelope)

        simulation = simulate_local_action(
            envelope["decision"],
            verification_errors,
            root_path=self.root_path,
            user_request=goal_contract["user_request"],
            consequence_class=proposal["consequence_class"],
        )
        envelope["execution_status"] = simulation["execution_status"]
        envelope["outcome_status"] = simulation["outcome_status"]
        tool_result = simulation["tool_result"]
        receipt = render_receipt(goal_contract, envelope, verification_errors, tool_result)
        if agent_run is not None:
            receipt["agent_run"] = agent_run
        ledger_record = None
        if self.ledger is not None:
            ledger_record = self.ledger.append_record(
                receipt=receipt,
                envelope=envelope,
                verification_errors=verification_errors,
                tool_result=tool_result,
            )

        result = {
            "goal_contract": goal_contract,
            "proposal": proposal,
            "envelope": envelope,
            "verification_errors": verification_errors,
            "tool_result": tool_result,
            "receipt": receipt,
        }
        if ledger_record is not None:
            result["ledger_record"] = ledger_record
        return result

    def handle_request(
        self,
        user_request: str,
        review_token: dict | None = None,
        agent_run: dict | None = None,
    ) -> dict:
        prepared = self.prepare_request(user_request)
        return self.evaluate_proposal(
            prepared["goal_contract"],
            prepared["proposal"],
            review_token=review_token,
            agent_run=agent_run,
        )

    def inspect_github_pr(
        self,
        pr_url: str,
        *,
        fixture_path: str | Path | None = None,
        github_token: str | None = None,
    ) -> dict:
        reader = GitHubPRReader()
        snapshot = reader.from_fixture(fixture_path) if fixture_path is not None else reader.fetch_pr_snapshot(
            pr_url,
            token=github_token,
        )
        user_request = f"Inspect GitHub PR {pr_url}"
        goal_contract = create_goal_contract(user_request)
        goal_contract["bounded_goal"] = "Inspect GitHub PR metadata and evidence in read-only mode"
        goal_contract["non_goals"] = [
            "Do not write to GitHub",
            "Do not merge the PR",
            "Do not comment on the PR",
            "Do not expose secrets",
        ]
        goal_contract["success_criteria"] = [
            "GitHub PR snapshot created",
            "Evidence hash recorded",
            "Receipt generated",
            "No GitHub write performed",
        ]
        identity = get_identity_manifest()
        proposal = create_proposal_object(
            agent_id=identity["agent_id"],
            user_request=user_request,
            agent_output_mode="ACTION_PROPOSAL",
            agent_output_mode_basis="Read-only GitHub PR evidence inspection",
            execution_authority_claimed=False,
            consequence_class="READ_ONLY_ACCESS",
        )
        proposal["evidence_available"] = [f"github_pr_snapshot:{snapshot['evidence_hash']}"]
        proposal["evidence_gaps"] = []
        if not snapshot["checks_passing"]:
            proposal["evidence_gaps"].append("passing_checks")
        if "SENSITIVE_FILE_TOUCHED" in snapshot["risk_flags"]:
            proposal["evidence_gaps"].append("sensitive_file_review")
        proposal["risk_level"] = "LOW" if snapshot["checks_passing"] and not snapshot["risk_flags"] else "MEDIUM"

        policy_result = apply_policy(proposal, policy=self.policy, reviewer_registry=self.reviewer_registry)
        envelope = proposal_to_envelope(proposal, policy_result, runtime_id=self.runtime_id)
        verification_errors = verify_constitutional_invariants(envelope)
        envelope["execution_status"] = "EXECUTED"
        envelope["outcome_status"] = "SUCCESS"
        tool_result = {
            "tool_name": "github_pr_readonly_inspect",
            "tool_executed": True,
            "tool_status": "SUCCESS",
            "tool_result_summary": (
                f"read-only PR inspection for {snapshot['owner']}/{snapshot['repo']}#{snapshot['pr_number']}"
            ),
            "github_pr_snapshot": snapshot,
        }
        receipt = render_receipt(goal_contract, envelope, verification_errors, tool_result)
        ledger_record = None
        if self.ledger is not None:
            ledger_record = self.ledger.append_record(
                receipt=receipt,
                envelope=envelope,
                verification_errors=verification_errors,
                tool_result=tool_result,
            )
        result = {
            "goal_contract": goal_contract,
            "proposal": proposal,
            "envelope": envelope,
            "verification_errors": verification_errors,
            "tool_result": tool_result,
            "receipt": receipt,
            "github_pr_snapshot": snapshot,
        }
        if ledger_record is not None:
            result["ledger_record"] = ledger_record
        return result

    def propose_code_change(
        self,
        user_request: str,
        *,
        review_token: dict | None = None,
        prepared: dict | None = None,
        agent_run: dict | None = None,
    ) -> dict:
        prepared = prepared or self.prepare_request(user_request)
        goal_contract = prepared["goal_contract"]
        proposal = prepared["proposal"]
        consequence_class = proposal["consequence_class"]
        code_artifact = None
        planning_error: CodeChangePlanningError | None = None

        if consequence_class in {"CODE_CHANGE", "WORKFLOW_CHANGE"}:
            try:
                code_artifact = CodeChangePlanner().plan_change(
                    root=self.root_path,
                    user_request=user_request,
                    proposal_id=proposal["proposal_id"],
                    agent_id=proposal["agent_id"],
                )
            except CodeChangePlanningError as exc:
                planning_error = exc
                consequence_class = exc.consequence_class
                proposal["consequence_class"] = consequence_class
        elif consequence_class in {"SECRET_ACCESS", "IRREVERSIBLE_DELETE"}:
            planning_error = CodeChangePlanningError(consequence_class, "Unsafe code-change proposal request denied")

        policy_result = apply_policy(
            proposal,
            review_token=review_token,
            policy=self.policy,
            reviewer_registry=self.reviewer_registry,
        )
        envelope = proposal_to_envelope(proposal, policy_result, runtime_id=self.runtime_id)
        verification_errors = verify_constitutional_invariants(envelope)

        if envelope["decision"] == "ALLOW" and code_artifact is not None:
            envelope["execution_status"] = "EXECUTED"
            envelope["outcome_status"] = "SUCCESS"
            tool_result = {
                "tool_name": "sandboxed_code_change_proposal",
                "tool_executed": True,
                "tool_status": "SUCCESS",
                "tool_result_summary": "sandboxed code change proposal generated; real repo unchanged",
                "code_change_proposal": code_artifact.to_dict(),
                "diff_text": code_artifact.diff_text,
            }
        elif envelope["decision"] == "REQUEST_REVIEW":
            envelope["execution_status"] = "NOT_EXECUTED"
            envelope["outcome_status"] = "PENDING_REVIEW"
            tool_result = {
                "tool_name": "sandboxed_code_change_proposal" if code_artifact else None,
                "tool_executed": False,
                "tool_status": "PENDING_REVIEW",
                "tool_result_summary": "sandboxed code change proposal awaits review",
                "code_change_proposal": code_artifact.to_dict() if code_artifact else None,
            }
        else:
            envelope["execution_status"] = "NOT_EXECUTED"
            envelope["outcome_status"] = "BLOCKED"
            tool_result = {
                "tool_name": None,
                "tool_executed": False,
                "tool_status": "NOT_INVOKED",
                "reason": str(planning_error) if planning_error else "Policy denied code change proposal",
                "tool_result_summary": "code change proposal not created",
            }

        receipt = render_receipt(goal_contract, envelope, verification_errors, tool_result)
        if agent_run is not None:
            receipt["agent_run"] = agent_run
        ledger_record = None
        if self.ledger is not None:
            ledger_record = self.ledger.append_record(
                receipt=receipt,
                envelope=envelope,
                verification_errors=verification_errors,
                tool_result=tool_result,
            )
        result = {
            "goal_contract": goal_contract,
            "proposal": proposal,
            "envelope": envelope,
            "verification_errors": verification_errors,
            "tool_result": tool_result,
            "receipt": receipt,
        }
        if code_artifact is not None:
            result["code_change_proposal"] = code_artifact.to_dict()
        if ledger_record is not None:
            result["ledger_record"] = ledger_record
        return result
