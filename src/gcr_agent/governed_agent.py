from __future__ import annotations

from pathlib import Path

from gcr.policy_engine import apply_policy
from gcr.proposal_object import create_proposal_object
from gcr.proposal_to_envelope import proposal_to_envelope
from gcr.verify_envelope_chain import verify_constitutional_invariants

from .consequence_classifier import classify_consequence
from .goal_contract import create_goal_contract
from .identity_manifest import get_identity_manifest
from .local_action_simulator import simulate_local_action
from .output_mode_labeler import label_output_mode
from .receipt_renderer import render_receipt


class GovernedAgent:
    def __init__(self, runtime_id: str = "local_simulator", root_path: str | Path | None = None) -> None:
        self.runtime_id = runtime_id
        self.root_path = Path(root_path or Path.cwd()).resolve()

    def handle_request(self, user_request: str) -> dict:
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
        policy_result = apply_policy(proposal)
        envelope = proposal_to_envelope(proposal, policy_result, runtime_id=self.runtime_id)
        verification_errors = verify_constitutional_invariants(envelope)

        simulation = simulate_local_action(
            envelope["decision"],
            verification_errors,
            root_path=self.root_path,
            user_request=user_request,
        )
        envelope["execution_status"] = simulation["execution_status"]
        envelope["outcome_status"] = simulation["outcome_status"]
        tool_result = simulation["tool_result"]
        receipt = render_receipt(goal_contract, envelope, verification_errors, tool_result)

        return {
            "goal_contract": goal_contract,
            "proposal": proposal,
            "envelope": envelope,
            "verification_errors": verification_errors,
            "tool_result": tool_result,
            "receipt": receipt,
        }
