# src/scraper/extractor.py
from src.providers.base import AIProvider

class Extractor:
    def __init__(self, provider: AIProvider):
        self._provider = provider

    def extract(self, cleaned_html: str, fields: dict[str, str]) -> dict:
        tool_schema = self._build_tool_schema(fields)
        prompt = self._build_prompt(cleaned_html)
        return self._provider.extract_structured(prompt, tool_schema)

    def _build_tool_schema(self, fields: dict[str, str]) -> dict:
        properties = {name: {"type": "string", "description": desc} for name, desc in fields.items()}
        return {
            "name": "extract_data",
            "description": "Extract the requested structured fields from the page content.",
            "input_schema": {"type": "object", "properties": properties, "required": list(fields.keys())},
        }

    def _build_prompt(self, cleaned_html: str) -> str:
        return (
            "Extract the requested fields from this page content. "
            f"If a field genuinely isn't present, use an empty string.\n\nPAGE CONTENT:\n{cleaned_html}"
        )
