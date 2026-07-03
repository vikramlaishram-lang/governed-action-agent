from __future__ import annotations

import json

from gcr_agent.llm_client import FakeLLMClient


def test_real_agent_uses_fake_llm_to_generate_proposal() -> None:
    output = FakeLLMClient().complete([{"role": "user", "content": "Improve README with governed agent summary"}])
    proposal = json.loads(output)

    assert proposal["agent_intent"] == "propose_code_change"
    assert proposal["requested_tool"] == "sandboxed_code_change_proposal"
