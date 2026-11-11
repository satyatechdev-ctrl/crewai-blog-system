"""Configuration & environment loading with security checks.

Never reads secrets from code; always from environment variables or .env.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load .env (does NOT override already-set env vars – explicit wins)
# ---------------------------------------------------------------------------
_env_path = Path(__file__).resolve().parent.parent / ".env"
if _env_path.exists():
    load_dotenv(str(_env_path), override=False)

# ---------------------------------------------------------------------------
# Required settings
# ---------------------------------------------------------------------------

EURON_API_KEY: str = os.environ.get("EURON_API_KEY", "")

if not EURON_API_KEY or EURON_API_KEY.startswith("your-"):
    raise ValueError(
        "EURON_API_KEY is not set or still has the placeholder value.\n"
        "Set it in your .env file or as an environment variable.\n"
        "NEVER hard-code real keys in source code."
    )

# ---------------------------------------------------------------------------
# Optional settings with safe defaults
# ---------------------------------------------------------------------------

EURON_BASE_URL: str = os.environ.get(
    "EURON_BASE_URL", "https://api.euron.one/api/v1/euri"
)
EURON_MODEL: str = os.environ.get("EURON_MODEL", "euri-auto")

CREWAI_API_KEY: str = os.environ.get("CREWAI_API_KEY", "")

# ---------------------------------------------------------------------------
# LLM factory – returns the LangChain chat model configured for Euron
# ---------------------------------------------------------------------------

from langchain_openai import ChatOpenAI


def get_llm(temperature: float = 0.4) -> ChatOpenAI:
    """Return a ChatOpenAI instance wired to the Euron API."""
    return ChatOpenAI(
        model=EURON_MODEL,
        api_key=EURON_API_KEY,
        base_url=EURON_BASE_URL,
        temperature=temperature,
    )
