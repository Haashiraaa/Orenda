# src/providers/factory.py
from src.providers.anthropic_provider import AnthropicProvider
from src.providers.base import AIProvider


def build_provider(provider_name: str, api_key: str) -> AIProvider:
    match provider_name.lower():
        case "anthropic":
            return AnthropicProvider(api_key=api_key)
        # case "openai":
        #     return OpenAIProvider(api_key=api_key)
        case _:
            raise ValueError(f"Unknown AI_PROVIDER: {provider_name}")
