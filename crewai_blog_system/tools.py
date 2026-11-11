"""Tools available to agents.

All tools are safe – no shell commands, no eval/exec, no unsafe deserialisation.
"""

from __future__ import annotations

import json
from typing import Optional

from crewai.tools import BaseTool


class SummarizeTool(BaseTool):
    """Summarise a block of text into key bullet points.

    The agent calls this to condense research material.
    """

    name: str = "summarize_text"
    description: str = (
        "Summarise a block of text into 5-10 key bullet points. "
        "Accepts any text string and returns a concise summary."
    )

    def _run(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return "Error: No valid text provided to summarise."
        # Pure in-memory summarisation via truncation + extraction
        # (The actual summarisation happens at the LLM level; this is a passthrough marker)
        return f"[SUMMARISE] Text length: {len(text)} chars. Ready for agent summarisation."


class StructureTool(BaseTool):
    """Outline a blog post structure from research notes.

    Returns a markdown outline with headings and sub-sections.
    """

    name: str = "create_outline"
    description: str = (
        "Create a structured outline for a blog post from research notes. "
        "Accepts research text and returns a markdown outline with H2/H3 headings."
    )

    def _run(self, topic: str, research_notes: str) -> str:
        if not topic or not research_notes:
            return "Error: Both topic and research notes are required."
        return (
            f"[OUTLINE] Topic: {topic!r}\n"
            f"Research notes length: {len(research_notes)} chars.\n"
            "The agent should now create a structured outline."
        )


class FactCheckerTool(BaseTool):
    """Cross-check a claim against a knowledge base (mock for production).

    In a real deployment this would connect to a RAG backend or external API.
    """

    name: str = "fact_check"
    description: str = (
        "Verify a factual claim. Accepts a claim string and returns "
        "a verdict: VERIFIED, UNVERIFIED, or NEEDS_REVIEW."
    )

    def _run(self, claim: str, context: Optional[str] = None) -> str:
        if not claim or not isinstance(claim, str):
            return "Error: No valid claim provided."
        # Safe JSON output – no eval/exec
        result = {
            "claim": claim,
            "verdict": "NEEDS_REVIEW",
            "confidence": 0.5,
            "notes": "Automated fact check – requires human review in production.",
        }
        return json.dumps(result, ensure_ascii=False, indent=2)
