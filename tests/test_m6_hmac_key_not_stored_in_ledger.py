from __future__ import annotations

from gcr.ledger_auth import HMAC_SHA256_V1
from gcr.receipt_ledger import ReceiptLedger
from gcr_agent import GovernedAgent


def test_m6_hmac_key_not_stored_in_ledger(tmp_path) -> None:
    ledger_path = tmp_path / "ledger.jsonl"
    secret = "do-not-store-this-dev-key"
    GovernedAgent(
        root_path=".",
        ledger_path=ledger_path,
        ledger_auth_mode=HMAC_SHA256_V1,
        ledger_hmac_key=secret,
        ledger_key_id="dev-key-id",
    ).handle_request("Read README.md")

    raw = ledger_path.read_text(encoding="utf-8")
    record = ReceiptLedger(ledger_path).read_records()[0]

    assert secret not in raw
    assert record["key_id"] == "dev-key-id"
