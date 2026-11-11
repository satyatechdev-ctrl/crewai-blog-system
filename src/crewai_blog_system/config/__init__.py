"""Config package for CrewAI blog system (agents.yaml, tasks.yaml)."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from langchain_openai import ChatOpenAI

EURON_MODEL = "euri-reasoning"
EURON_BASE_URL = "https://api.euron.one/api/v1/euri"


def _check_api_key() -> str:
    """Return the API key from the environment, or raise ValueError."""
    api_key = os.environ.get("EURON_API_KEY")
    if not api_key:
        raise ValueError(
            "EURON_API_KEY environment variable is not set. "
            "Set it to your Euron API key before running."
        )
    return api_key


# Raise at import time so missing keys fail fast
_checked_api_key = _check_api_key()


def get_llm(temperature: float = 0.7) -> "ChatOpenAI":
    """Return a ChatOpenAI instance configured for Euron's API.

    Raises
    ------
    ValueError
        If EURON_API_KEY is not set in the environment.
    """
    api_key = _check_api_key()

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=EURON_MODEL,
        api_key=api_key,
        base_url=EURON_BASE_URL,
        temperature=temperature,
    )
