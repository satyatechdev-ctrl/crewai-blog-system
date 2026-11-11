"""Security helpers: input sanitisation, secret shielding, and safe topic validation.

All validation is done through typed Pydantic models – never eval/exec.
"""

from __future__ import annotations

import re
import html
from typing import Any

# Characters allowed in a blog topic (letters, numbers, basic punctuation)
_TOPIC_PATTERN = re.compile(r"^[\w\s\-\/'.,:;?!\(\)\+#@&=]+$")

# Maximum length for a user-supplied topic
MAX_TOPIC_LENGTH = 200

# Sensitive patterns that must never appear in user input
_BLOCKED_PATTERNS = [
    r"\b(?:password|secret|token|api[_-]?key)\b\s*[:=]",  # credential leak attempt
    r"(?i)\/etc\/passwd",                                  # path traversal
    r"\$\{.*?\}",                                          # template injection
]


class ValidationError(Exception):
    """Raised when user input fails sanitisation."""


def sanitize_topic(raw: Any) -> str:
    """Validate and sanitise a user-supplied blog topic.

    Returns a safe string suitable for passing to agents.
    Raises ``ValidationError`` on bad input.
    """
    if not isinstance(raw, str):
        raise ValidationError("Topic must be a string.")

    topic = raw.strip()

    if not topic:
        raise ValidationError("Topic cannot be empty.")

    if len(topic) > MAX_TOPIC_LENGTH:
        raise ValidationError(
            f"Topic is too long ({len(topic)} chars). Maximum {MAX_TOPIC_LENGTH}."
        )

    # Check blocked patterns BEFORE character validation
    # so injection attempts get a specific "unsafe" error
    for pattern in _BLOCKED_PATTERNS:
        if re.search(pattern, topic):
            raise ValidationError("Topic contains potentially unsafe content.")

    if not _TOPIC_PATTERN.match(topic):
        raise ValidationError(
            "Topic contains disallowed characters. "
            "Only letters, numbers, spaces, and basic punctuation are allowed."
        )

    # HTML-encode to prevent any injection in downstream markdown
    return html.escape(topic)


def shield_secret(secret: str | None, visible_chars: int = 4) -> str:
    """Return a redacted version of a secret for logging."""
    if not secret or len(secret) <= visible_chars + 4:
        return "****"
    return secret[:visible_chars] + "*" * (len(secret) - visible_chars - 4) + secret[-4:]
