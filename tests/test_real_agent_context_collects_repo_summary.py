from __future__ import annotations

from gcr_agent.agent_context import collect_repo_context


def test_real_agent_context_collects_repo_summary(tmp_path) -> None:
    (tmp_path / "README.md").write_text("# Demo\n", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET_VALUE=hidden\n", encoding="utf-8")
    (tmp_path / ".git").mkdir()
    (tmp_path / "tests").mkdir()

    context = collect_repo_context(tmp_path)

    assert context["readme_exists"] is True
    assert context["tests_exists"] is True
    assert ".env" not in context["top_level_files"]
    assert ".git" not in context["top_level_files"]
    assert "SECRET_VALUE" not in str(context)
