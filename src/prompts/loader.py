"""Loads prompt templates from the prompts/ directory."""

import os

PROMPTS_DIR = "prompts"


def load_prompt(name: str, **kwargs) -> str:
    """Load a prompt template by file name (without extension) and format it."""
    path = os.path.join(PROMPTS_DIR, f"{name}.txt")
    with open(path, "r") as f:
        template = f.read()
    return template.format(**kwargs)
