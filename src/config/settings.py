
import os
from typing import ClassVar

from dotenv import load_dotenv

from src.exceptions.errors import EnvVariableError

load_dotenv()

class Settings:

    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    AI_PROVIDER = os.getenv('AI_PROVIDER')
    
    _REQUIRED: ClassVar[dict[str, str | None]] = {
        'ANTHROPIC_API_KEY': ANTHROPIC_API_KEY,
        'AI_PROVIDER': AI_PROVIDER,
    }

    _missing: ClassVar[list[str]] = [name for name, value in _REQUIRED.items() if not value]
    if _missing:
        raise EnvVariableError(
            "Missing required environment variables: "
            + ", ".join(_missing)
            + ". Copy .env.example to .env and fill these in."
        )
