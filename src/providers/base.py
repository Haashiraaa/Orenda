# src/providers/base.py
from abc import ABC, abstractmethod
from typing import Any

class AIProvider(ABC):
    @abstractmethod
    def extract_structured(self, prompt: str, tool_schema: dict) -> dict[str, Any]:
        """Send prompt + schema, return parsed structured output as a dict."""
        ...
