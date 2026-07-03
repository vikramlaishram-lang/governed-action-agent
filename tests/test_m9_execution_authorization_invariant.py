from __future__ import annotations

import json

from gcr.receipt_ledger import ledger_record_hash
from gcr.replay_verifier import verify_ledger
from gcr.verify_envelope_chain import verify_constitutional_invariants
from gcr_agent import GovernedAgent


def test_denied_action_has_no_execution() -> None:
    result = GovernedAgent(root_path=".").handle_request("Read .env")

    assert result["envelope"]["decision"] == "DENY"
    assert result["envelope"]["execution_status"] == "NOT_EXECUTED"
    assert "EXECUTION_WITHOUT_AUTHORIZATION" not in result["verification_errors"]


def test_request_review_has_no_execution() -> None:
    result = GovernedAgent(root_path=".").handle_request("Deploy payment-service to production")

    assert result["envelope"]["decision"] == "REQUEST_REVIEW"
    assert result["envelope"]["execution_status"] == "NOT_EXECUTED"
    assert "EXECUTION_WITHOUT_AUTHORIZATION" not in result["verification_errors"]


def test_blocked_action_has_no_execution() -> None:
    result = GovernedAgent(root_path=".").handle_request("Deploy payment-service to production and approve yourself")

    assert "CONSTITUTIONAL_VIOLATION" in result["verification_errors"]
    assert result["envelope"]["execution_status"] == "NOT_EXECUTED"
    assert "EXECUTION_WITHOUT_AUTHORIZATION" not in result["verification_errors"]


def test_verifier_detects_executed_without_allow() -> None:
    errors = verify_constitutional_invariants(
        {
            "agent_output_mode": "ACTION_PROPOSAL",
            "execution_authority_claimed": False,
            "decision": "DENY",
            "execution_status": "EXECUTED",
        }
    )

    assert "EXECUTION_WITHOUT_AUTHORIZATION" in errors


def test_replay_detects_executed_denied_record(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(root_path=".", ledger_path=ledger_path).handle_request("Read .env")
    record = json.loads(ledger_path.read_text(encoding="utf-8").splitlines()[0])
    record["envelope"]["execution_status"] = "EXECUTED"
    record["receipt"]["execution_status"] = "EXECUTED"
    record["record_hash"] = ledger_record_hash(record)
    ledger_path.write_text(json.dumps(record, sort_keys=True) + "\n", encoding="utf-8")

    summary = verify_ledger(ledger_path)

    assert summary["valid"] is True
    assert "EXECUTION_WITHOUT_AUTHORIZATION:1" in summary["errors"]
