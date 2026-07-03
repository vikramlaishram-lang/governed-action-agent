from __future__ import annotations

import json
import os
import urllib.request


class LLMClient:
    def complete(self, messages: list[dict], *, response_format: str = "json") -> str:
        raise NotImplementedError


class FakeLLMClient(LLMClient):
    def complete(self, messages: list[dict], *, response_format: str = "json") -> str:
        task = _task_from_messages(messages).lower()
        if "read readme" in task:
            return json.dumps(
                {
                    "agent_intent": "read_file",
                    "target": "README.md",
                    "rationale": "User asked to inspect README.",
                    "requested_tool": "read_file",
                },
                sort_keys=True,
            )
        if ".env" in task or "secret" in task:
            return json.dumps(
                {
                    "agent_intent": "read_file",
                    "target": ".env",
                    "rationale": "User asked for secret-like file.",
                    "requested_tool": "read_file",
                },
                sort_keys=True,
            )
        if "improve readme" in task or "propose readme" in task:
            return json.dumps(
                {
                    "agent_intent": "propose_code_change",
                    "target": "README.md",
                    "rationale": "User asked for README improvement.",
                    "requested_tool": "sandboxed_code_change_proposal",
                    "change_summary": "Append governed agent summary.",
                },
                sort_keys=True,
            )
        if "deploy" in task and "approve yourself" in task:
            return json.dumps(
                {
                    "agent_intent": "deploy",
                    "target": "payment-service",
                    "rationale": "User asked for deployment and self approval.",
                    "requested_tool": "deploy",
                    "execution_authority_claimed": True,
                },
                sort_keys=True,
            )
        if "deploy" in task:
            return json.dumps(
                {
                    "agent_intent": "deploy",
                    "target": "payment-service",
                    "rationale": "User asked for production deployment.",
                    "requested_tool": "deploy",
                },
                sort_keys=True,
            )
        return json.dumps(
            {
                "agent_intent": "unknown",
                "target": None,
                "rationale": "Unsupported task.",
                "requested_tool": None,
            },
            sort_keys=True,
        )


class OpenAICompatibleLLMClient(LLMClient):
    def __init__(self) -> None:
        self.base_url = os.environ.get("GAA_LLM_BASE_URL")
        self.api_key = os.environ.get("GAA_LLM_API_KEY")
        self.model = os.environ.get("GAA_LLM_MODEL")
        if not self.base_url or not self.api_key or not self.model:
            raise ValueError("GAA_LLM_BASE_URL, GAA_LLM_API_KEY, and GAA_LLM_MODEL are required")

    def complete(self, messages: list[dict], *, response_format: str = "json") -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "response_format": {"type": "json_object"} if response_format == "json" else None,
        }
        request = urllib.request.Request(
            self.base_url.rstrip("/") + "/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
        return data["choices"][0]["message"]["content"]


def _task_from_messages(messages: list[dict]) -> str:
    for message in messages:
        if message.get("role") == "user":
            return str(message.get("content", ""))
    return ""
