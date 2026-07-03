from __future__ import annotations

import json
import re
import urllib.request
from datetime import UTC, datetime
from pathlib import Path

from gcr.evidence_hash import evidence_hash


SENSITIVE_FILENAMES = {".env", ".env.local", ".env.production", "secrets.json", "credentials.json", "id_rsa", "id_ed25519"}
PASSING_CONCLUSIONS = {"success", "neutral", "skipped"}
FAILING_CONCLUSIONS = {"failure", "cancelled", "timed_out", "action_required"}


def parse_github_pr_url(url: str) -> dict:
    match = re.fullmatch(r"https://github\.com/([^/\s]+)/([^/\s]+)/pull/(\d+)", url.strip())
    if not match:
        raise ValueError("Unsupported GitHub PR URL")
    return {"owner": match.group(1), "repo": match.group(2), "pr_number": int(match.group(3))}


class GitHubPRReader:
    def from_fixture(self, path: str | Path) -> dict:
        return self.load_fixture(path)

    def load_fixture(self, path: str | Path) -> dict:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        return self.normalize_snapshot(raw, source="FIXTURE")

    def fetch_pr_snapshot(self, url: str, *, token: str | None = None) -> dict:
        parsed = parse_github_pr_url(url)
        owner = parsed["owner"]
        repo = parsed["repo"]
        pr_number = parsed["pr_number"]
        headers = {"Accept": "application/vnd.github+json", "User-Agent": "governed-action-agent"}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        pr = self._get_json(f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}", headers)
        files = self._get_json(f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files", headers)
        checks: list[dict] = []
        head_sha = pr.get("head", {}).get("sha")
        if head_sha:
            try:
                check_data = self._get_json(f"https://api.github.com/repos/{owner}/{repo}/commits/{head_sha}/check-runs", headers)
                checks = check_data.get("check_runs", [])
            except Exception:
                checks = []
        raw = {
            "owner": owner,
            "repo": repo,
            "pr_number": pr_number,
            "title": pr.get("title", ""),
            "state": pr.get("state", ""),
            "author": pr.get("user", {}).get("login", ""),
            "base_ref": pr.get("base", {}).get("ref", ""),
            "head_ref": pr.get("head", {}).get("ref", ""),
            "mergeable": pr.get("mergeable"),
            "changed_files_count": pr.get("changed_files", len(files)),
            "additions": pr.get("additions", 0),
            "deletions": pr.get("deletions", 0),
            "files": files,
            "checks": checks,
        }
        return self.normalize_snapshot(raw, source="GITHUB_API")

    def normalize_snapshot(self, raw: dict, *, source: str) -> dict:
        files = [
            {
                "filename": file.get("filename", ""),
                "status": file.get("status", ""),
                "additions": int(file.get("additions", 0)),
                "deletions": int(file.get("deletions", 0)),
            }
            for file in raw.get("files", [])
        ]
        checks = [
            {
                "name": check.get("name") or check.get("check_run_name") or check.get("context") or "",
                "status": check.get("status", ""),
                "conclusion": check.get("conclusion"),
            }
            for check in raw.get("checks", [])
        ]
        checks_passing = all((check.get("conclusion") in PASSING_CONCLUSIONS) for check in checks)
        checks_passing = checks_passing and not any(check.get("conclusion") in FAILING_CONCLUSIONS for check in checks)
        risk_flags: list[str] = []
        if any(_is_sensitive_file(file["filename"]) for file in files):
            risk_flags.append("SENSITIVE_FILE_TOUCHED")
        if not checks_passing:
            risk_flags.append("CHECKS_NOT_PASSING")
        changed_files_count = int(raw.get("changed_files_count", len(files)))
        if changed_files_count > 50:
            risk_flags.append("LARGE_CHANGESET")
        if raw.get("state", "") != "open":
            risk_flags.append("PR_NOT_OPEN")

        snapshot = {
            "schema_version": "github_pr_snapshot_v0.1",
            "source": source,
            "owner": raw.get("owner", ""),
            "repo": raw.get("repo", ""),
            "pr_number": int(raw.get("pr_number", 0)),
            "title": raw.get("title", ""),
            "state": raw.get("state", ""),
            "author": raw.get("author", ""),
            "base_ref": raw.get("base_ref", ""),
            "head_ref": raw.get("head_ref", ""),
            "mergeable": raw.get("mergeable"),
            "changed_files_count": changed_files_count,
            "additions": int(raw.get("additions", 0)),
            "deletions": int(raw.get("deletions", 0)),
            "files": files,
            "checks": checks,
            "checks_passing": checks_passing,
            "risk_flags": risk_flags,
            "fetched_at": datetime.now(UTC).isoformat(),
            "evidence_hash": "",
        }
        snapshot["evidence_hash"] = evidence_hash(snapshot)
        return snapshot

    def _get_json(self, url: str, headers: dict) -> dict | list:
        request = urllib.request.Request(url, headers=headers, method="GET")
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))


def _is_sensitive_file(filename: str) -> bool:
    lowered = filename.lower()
    name = Path(lowered).name
    return name in SENSITIVE_FILENAMES or "secret" in lowered or "credential" in lowered
