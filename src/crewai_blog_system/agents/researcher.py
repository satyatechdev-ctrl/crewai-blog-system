"""Researcher agent: drafts a research brief from model knowledge.

Role
----
The Researcher is the first agent in the pipeline. It:

1. Accepts a blog post topic from the user.
2. Uses its available model knowledge and tools to identify:
   - Key concepts and definitions
   - Recent developments and trends
   - Expert opinions and statistics
   - Related technologies and tools
3. Structures the research into a well-organised brief that the Writer agent can consume.

No live web search is configured; claims and references should be independently verified.
"""

from __future__ import annotations

from crewai import Agent

from crewai_blog_system.config import get_llm
from crewai_blog_system.tools import FactCheckerTool, SummarizeTool


def create_researcher() -> Agent:
    """Build and return the Researcher agent."""
    llm = get_llm(temperature=0.2)  # Low temperature for factual accuracy

    return Agent(
        role="Senior Technical Researcher",
        goal=(
            "Draft a research brief covering key concepts and relevant context for "
            "the given topic. Distinguish established knowledge from uncertain or "
            "time-sensitive claims, and do not invent citations or statistics."
        ),
        backstory=(
            "You are a senior technical researcher with 15+ years of experience "
            "in technology journalism and analysis. You have deep expertise across "
            "multiple technology domains including AI, cloud computing, cybersecurity, "
            "and emerging technologies. You synthesise complex information into "
            "clear research briefs. You do not have live web access, so never claim "
            "to have cross-checked a source or invent a citation."
        ),
        tools=[SummarizeTool(), FactCheckerTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        cache=True,
    )
