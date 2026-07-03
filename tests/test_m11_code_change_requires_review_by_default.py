from __future__ import annotations

from gcr_agent import GovernedAgent


def test_m11_code_change_requires_review_by_default(tmp_path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    result = GovernedAgent(root_path=tmp_path).propose_code_change("Update README.md with governed agent summary")

    assert result["proposal"]["consequence_class"] == "CODE_CHANGE"
    assert result["envelope"]["decision"] == "REQUEST_REVIEW"
    assert result["envelope"]["execution_status"] == "NOT_EXECUTED"
    assert result["code_change_proposal"]["requires_review"] is True
