from __future__ import annotations

from pathlib import Path

from gcr.policy_engine import apply_policy
from gcr.proposal_object import create_proposal_object
from gcr.proposal_to_envelope import proposal_to_envelope
from gcr.receipt_ledger import ReceiptLedger
from gcr.verify_envelope_chain import verify_constitutional_invariants

from .consequence_classifier import classify_consequence
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
    ) -> None:
        self.runtime_id = runtime_id
        self.root_path = Path(root_path or Path.cwd()).resolve()
        self.ledger = ReceiptLedger(ledger_path) if ledger_path is not None else None

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
    ) -> dict:
        policy_result = apply_policy(proposal, review_token=review_token)
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

    def handle_request(self, user_request: str, review_token: dict | None = None) -> dict:
        prepared = self.prepare_request(user_request)
        return self.evaluate_proposal(
            prepared["goal_contract"],
            prepared["proposal"],
            review_token=review_token,
        )
