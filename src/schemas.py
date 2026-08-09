

# src/schemas.py

from typing import Any, TypedDict


class ToolSchema(TypedDict):
    name: str
    description: str
    input_schema: dict[str, Any]
