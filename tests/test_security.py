"""Tests for input sanitisation and validation (security module).

These tests run without any LLM calls or network access.
"""

from __future__ import annotations

import pytest

from crewai_blog_system.security import ValidationError, sanitize_topic, shield_secret


class TestSanitizeTopic:
    """Tests for the topic sanitiser."""

    def test_valid_simple_topic(self):
        assert sanitize_topic("Quantum Computing") == "Quantum Computing"

    def test_valid_topic_with_hyphen(self):
        result = sanitize_topic("Machine Learning")
        assert result == "Machine Learning"

    def test_valid_topic_with_punctuation(self):
        result = sanitize_topic("AI in Healthcare: A Review")
        assert result == "AI in Healthcare: A Review"

    def test_valid_topic_preserves_special_chars(self):
        result = sanitize_topic("Docker & Kubernetes")
        assert result == "Docker & Kubernetes"

    def test_empty_string_rejected(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            sanitize_topic("")

    def test_whitespace_only_rejected(self):
        with pytest.raises(ValidationError, match="cannot be empty"):
            sanitize_topic("   ")

    def test_non_string_rejected(self):
        with pytest.raises(ValidationError, match="must be a string"):
            sanitize_topic(12345)  # type: ignore

    def test_none_rejected(self):
        with pytest.raises(ValidationError, match="must be a string"):
            sanitize_topic(None)  # type: ignore

    def test_too_long_topic_rejected(self):
        long_topic = "A" * 201
        with pytest.raises(ValidationError, match="too long"):
            sanitize_topic(long_topic)

    def test_disallowed_characters_rejected(self):
        with pytest.raises(ValidationError, match="disallowed"):
            sanitize_topic("test<script>alert(1)</script>")

    def test_html_injection_blocked(self):
        with pytest.raises(ValidationError, match="disallowed"):
            sanitize_topic("<b>bold</b>")

    def test_path_traversal_blocked(self):
        with pytest.raises(ValidationError, match="unsafe"):
            sanitize_topic("/etc/passwd")

    def test_template_injection_blocked(self):
        with pytest.raises(ValidationError, match="unsafe"):
            sanitize_topic("${7*7}")

    def test_credential_leak_attempt_blocked(self):
        with pytest.raises(ValidationError, match="unsafe"):
            sanitize_topic("password: secret123")

    def test_max_length_accepted(self):
        # Exactly at the limit
        topic = "A" * 200
        assert sanitize_topic(topic) is not None

    def test_valid_ampersand_is_preserved(self):
        result = sanitize_topic("A & B")
        assert result == "A & B"

    def test_numbers_and_symbols(self):
        result = sanitize_topic("Python 3.12 Features")
        assert result == "Python 3.12 Features"

    def test_url_safe_topic(self):
        result = sanitize_topic("REST APIs vs GraphQL")
        assert result == "REST APIs vs GraphQL"

    def test_emoji_blocked(self):
        # Emojis are not in the allowed character set
        with pytest.raises(ValidationError, match="disallowed"):
            sanitize_topic("AI 🚀")


class TestShieldSecret:
    """Tests for the secret redaction utility."""

    def test_normal_secret(self):
        result = shield_secret("sk-1234567890abcdef")
        assert "sk-1" in result  # first visible_chars (4) shown
        assert "****" in result  # redaction present
        assert "cdef" in result  # last 4 chars shown
        assert "1234" not in result  # middle is redacted

    def test_short_secret(self):
        result = shield_secret("abc")
        assert result == "****"

    def test_empty_secret(self):
        result = shield_secret("")
        assert result == "****"

    def test_none_secret(self):
        result = shield_secret(None)  # type: ignore
        assert result == "****"

    def test_visible_chars_parameter(self):
        result = shield_secret("sk-1234567890abcdef", visible_chars=2)
        assert result.startswith("sk")
