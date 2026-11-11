"""Config package for CrewAI blog system (agents.yaml, tasks.yaml)."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from dotenv import load_dotenv

if TYPE_CHECKING:
    from langchain_openai import ChatOpenAI

EURON_MODEL = "euri-reasoning"
EURON_BASE_URL = "https://api.euron.one/api/v1/euri"


def get_api_key() -> str:
    """Return the configured Euron key, accepting OpenAI's name for compatibility."""
    load_dotenv()
    api_key = os.environ.get("EURON_API_KEY") or os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "No Euron API key is configured. Set EURON_API_KEY in the environment "
            "or in a .env file. OPENAI_API_KEY is also accepted for compatibility."
        )
    return api_key


def get_base_url() -> str:
    """Return the configured Euron-compatible API endpoint."""
    load_dotenv()
    return os.environ.get("OPENAI_BASE_URL", EURON_BASE_URL)


def get_llm(temperature: float = 0.7) -> "ChatOpenAI":
    """Return a ChatOpenAI instance configured for Euron's API.

    Raises
    ------
    ValueError
        If no Euron API key is configured.
    """
    api_key = get_api_key()

    from langchain_openai import ChatOpenAI

    return ChatOpenAI(
        model=EURON_MODEL,
        api_key=api_key,
        base_url=get_base_url(),
        temperature=temperature,
    )
