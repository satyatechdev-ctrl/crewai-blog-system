"""Tests for the config module.

We test that the config module raises on missing keys without actually
loading .env (which is a test fixture concern).
"""

from __future__ import annotations

import pytest

import crewai_blog_system.config as cfg


def test_get_llm_returns_chat_openai(monkeypatch):
    """Verify get_llm returns a ChatOpenAI instance when EURON_API_KEY is set."""
    monkeypatch.setattr(cfg, "load_dotenv", lambda: None)
    monkeypatch.setenv("EURON_API_KEY", "sk-test-key-1234")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    llm = cfg.get_llm(temperature=0.5)
    assert llm.model_name == cfg.EURON_MODEL
    assert cfg.get_base_url() == "https://api.euron.one/api/v1/euri"


def test_openai_key_is_accepted_for_compatibility(monkeypatch):
    monkeypatch.setattr(cfg, "load_dotenv", lambda: None)
    monkeypatch.delenv("EURON_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_API_KEY", "legacy-test-key")

    assert cfg.get_api_key() == "legacy-test-key"


def test_euron_key_takes_precedence(monkeypatch):
    monkeypatch.setattr(cfg, "load_dotenv", lambda: None)
    monkeypatch.setenv("EURON_API_KEY", "euron-test-key")
    monkeypatch.setenv("OPENAI_API_KEY", "legacy-test-key")

    assert cfg.get_api_key() == "euron-test-key"


def test_missing_api_key_raises(monkeypatch):
    monkeypatch.setattr(cfg, "load_dotenv", lambda: None)
    monkeypatch.delenv("EURON_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="EURON_API_KEY"):
        cfg.get_api_key()
