"""Tests for the config module.

We test that the config module raises on missing keys without actually
loading .env (which is a test fixture concern).
"""

from __future__ import annotations

import os
from unittest import mock

import pytest


def test_get_llm_returns_chat_openai():
    """Verify get_llm returns a ChatOpenAI instance when EURON_API_KEY is set."""
    with mock.patch.dict(os.environ, {"EURON_API_KEY": "sk-test-key-1234"}, clear=False):
        # Re-import to pick up the patched env
        import importlib

        import crewai_blog_system.config as cfg
        importlib.reload(cfg)

        llm = cfg.get_llm(temperature=0.5)
        assert llm.model_name == cfg.EURON_MODEL
        assert cfg.EURON_BASE_URL == "https://api.euron.one/api/v1/euri"


def test_missing_api_key_raises():
    """Ensure the module refuses to load without an API key."""
    env_copy = dict(os.environ)
    os.environ.pop("EURON_API_KEY", None)

    try:
        with mock.patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError, match="EURON_API_KEY"):
                # Force re-evaluation of the module-level key check
                import importlib

                import crewai_blog_system.config as cfg
                importlib.reload(cfg)
    finally:
        # Restore env
        os.environ.update(env_copy)



# Note: placeholder key validation happens at module import time.
# The module-level check runs when the module is first loaded; mocking env vars
# after import has no effect. Integration tests should verify this end-to-end.
