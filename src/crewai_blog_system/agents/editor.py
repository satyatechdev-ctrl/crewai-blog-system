"""Editor agent: reviews, refines, and polishes the draft.

Role
----
The Editor is the final agent in the pipeline. It:

1. Reads the draft blog post produced by the Writer.
2. Reviews it for:
   - Technical accuracy and consistency
   - Grammar, spelling, and style
   - Logical flow and readability
   - Proper formatting (Markdown structure)
   - Appropriate length and depth
3. Produces a final, publication-ready Markdown document.

The Editor has full memory of the research brief and the draft so it can
ensure all facts are consistent.
"""

from __future__ import annotations

from crewai import Agent

from crewai_blog_system.config import get_llm
from crewai_blog_system.tools import FactCheckerTool


def create_editor() -> Agent:
    """Build and return the Editor agent."""
    llm = get_llm(temperature=0.3)  # Moderate temperature for balanced editing

    return Agent(
        role="Senior Technical Editor",
        goal=(
            "Review and refine the draft blog post to produce a final, "
            "publication-ready document. Ensure technical accuracy, proper "
            "grammar and style, logical flow, consistent formatting, and "
            "appropriate depth. The final output must be valid Markdown "
            "suitable for direct publication."
        ),
        backstory=(
            "You are a senior technical editor with 20+ years of experience "
            "editing technical content for publications like O'Reilly, InfoQ, "
            "and IEEE Spectrum. You have an exceptional eye for detail and a "
            "deep understanding of technical writing standards. You excel at "
            "identifying logical gaps, improving sentence clarity, ensuring "
            "consistent terminology, and polishing Markdown formatting. You "
            "always preserve the author's voice while elevating the overall "
            "quality of the piece. You are meticulous about fact-checking and "
            "ensuring that all claims are supported by evidence."
        ),
        tools=[FactCheckerTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        cache=True,
    )
