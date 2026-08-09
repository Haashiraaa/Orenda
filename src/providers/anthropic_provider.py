# src/providers/anthropic_provider.py
from typing import Any

from anthropic import Anthropic

from src.providers.base import AIProvider
from src.schemas import ToolSchema


class AnthropicProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        self._client = Anthropic(api_key=api_key)
        self._model = model

    def extract_structured(self, prompt: str, tool_schema: ToolSchema) -> dict[str, Any]:
        msg = self._client.messages.create(
            model=self._model,
            max_tokens=4000,
            tools=[tool_schema],
            tool_choice={"type": "tool", "name": tool_schema["name"]},
            messages=[{"role": "user", "content": prompt}],
        )
        for block in msg.content:
            if block.type == "tool_use":
                return block.input
        raise RuntimeError("No tool_use block in response")
