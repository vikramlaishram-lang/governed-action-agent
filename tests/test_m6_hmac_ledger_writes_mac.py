from __future__ import annotations

from gcr.ledger_auth import HMAC_SHA256_V1
from gcr.receipt_ledger import ReceiptLedger
from gcr_agent import GovernedAgent


def test_m6_hmac_ledger_writes_mac(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    GovernedAgent(
        root_path=".",
        ledger_path=ledger_path,
        ledger_auth_mode=HMAC_SHA256_V1,
        ledger_hmac_key="test-dev-key",
        ledger_key_id="test-key",
    ).handle_request("Read README.md")

    record = ReceiptLedger(ledger_path).read_records()[0]

    assert record["tamper_evidence_mode"] == "HMAC_SHA256_V1"
    assert record["ledger_auth_version"] == "HMAC_SHA256_V1"
    assert record["key_id"] == "test-key"
    assert record["record_mac"].startswith("hmac-sha256:")
