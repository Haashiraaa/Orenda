# src/providers/anthropic_provider.py
from anthropic import Anthropic

from src.providers.base import AIProvider


class AnthropicProvider(AIProvider):
    def __init__(self, api_key: str, model: str = "claude-sonnet-4-6"):
        self._client = Anthropic(api_key=api_key)
        self._model = model

    def extract_structured(self, prompt: str, tool_schema: dict) -> dict:
        msg = self._client.messages.create(
            model=self._model,
            max_tokens=1024,
            tools=[tool_schema],
            tool_choice={"type": "tool", "name": tool_schema["name"]},
            messages=[{"role": "user", "content": prompt}],
        )
        for block in msg.content:
            if block.type == "tool_use":
                return block.input
        raise RuntimeError("No tool_use block in response")
