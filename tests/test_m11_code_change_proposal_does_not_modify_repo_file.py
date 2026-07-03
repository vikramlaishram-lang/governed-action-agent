from __future__ import annotations

from gcr_agent import GovernedAgent


def test_m11_code_change_proposal_does_not_modify_repo_file(tmp_path) -> None:
    readme = tmp_path / "README.md"
    original = "# Demo\n"
    readme.write_text(original, encoding="utf-8")

    GovernedAgent(root_path=tmp_path).propose_code_change("Update README.md with governed agent summary")

    assert readme.read_text(encoding="utf-8") == original
