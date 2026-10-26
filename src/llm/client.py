"""LLM client wrapper.

Centralizes model calls so the rest of the codebase does not depend
directly on a specific provider SDK.
"""

import os


class LLMClient:
    """Thin wrapper around an LLM provider's API."""

    def __init__(self, model: str = "claude-sonnet-4-6", api_key: str | None = None):
        self.model = model
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Missing ANTHROPIC_API_KEY. Set it in your .env file.")

    def complete(self, prompt: str) -> str:
        """Send a prompt to the model and return the text response."""
        # TODO: wire up the real API call (anthropic / openai / etc.)
        raise NotImplementedError


def get_llm_client() -> LLMClient:
    return LLMClient()
