"""Tools available to agents.

All tools are safe – no shell commands, no eval/exec, no unsafe deserialisation.
"""

from __future__ import annotations

import json
import re

from crewai.tools import BaseTool


class SummarizeTool(BaseTool):
    """Extract leading sentences from text as bullet points.

    This is an extractive helper, not an LLM-based semantic summarizer.
    """

    name: str = "summarize_text"
    description: str = (
        "Extract up to 10 leading sentences from text as bullet points. "
        "This is extractive and does not verify facts."
    )

    def _run(self, text: str) -> str:
        if not text or not isinstance(text, str):
            return "Error: No valid text provided to summarize."
        sentences = [
            sentence.strip()
            for sentence in re.split(r"(?<=[.!?])\s+|\r?\n+", text.strip())
            if sentence.strip()
        ]
        if not sentences:
            return "Error: No valid text provided to summarize."
        return "\n".join(f"- {sentence}" for sentence in sentences[:10])


class StructureTool(BaseTool):
    """Create a Markdown outline using headings from research notes when available."""

    name: str = "create_outline"
    description: str = (
        "Create a structured outline for a blog post from research notes. "
        "Accepts research text and returns a markdown outline with H2/H3 headings."
    )

    def _run(self, topic: str, research_notes: str) -> str:
        if not topic or not research_notes:
            return "Error: Both topic and research notes are required."
        headings = [
            re.sub(r"^#{1,6}\s+", "", line).strip()
            for line in research_notes.splitlines()
            if re.match(r"^#{1,6}\s+\S", line)
        ]
        sections = headings[:8] or [
            "Introduction",
            "Core Concepts",
            "Current Landscape",
            "Practical Applications",
            "Challenges and Limitations",
            "Future Outlook",
            "Key Takeaways",
        ]
        return f"# {topic}\n\n" + "\n".join(f"## {section}" for section in sections)


class FactCheckerTool(BaseTool):
    """Flag claims for human review; this tool does not independently verify them."""

    name: str = "fact_check"
    description: str = (
        "Flag a factual claim for human review. This tool does not verify claims; "
        "it returns a NEEDS_REVIEW verdict and any supplied context."
    )

    def _run(self, claim: str, context: str | None = None) -> str:
        if not claim or not isinstance(claim, str):
            return "Error: No valid claim provided."
        result = {
            "claim": claim,
            "verdict": "NEEDS_REVIEW",
            "review_context": context,
            "notes": "This tool does not verify claims. Check the claim against reliable sources.",
        }
        return json.dumps(result, ensure_ascii=False, indent=2)
