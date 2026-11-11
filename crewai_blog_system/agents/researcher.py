"""Researcher agent: gathers information and facts about the topic.

Role
----
The Researcher is the first agent in the pipeline. It:

1. Accepts a blog post topic from the user.
2. Uses its internal knowledge and web-search tools to gather:
   - Key concepts and definitions
   - Recent developments and trends
   - Expert opinions and statistics
   - Related technologies and tools
3. Structures the research into a well-organised brief that the Writer agent can consume.

The Researcher uses short-term memory to remember what it has already found,
avoiding duplicate searches.
"""

from __future__ import annotations

from crewai import Agent

from crewai_blog_system.config import get_llm
from crewai_blog_system.tools import SummarizeTool, FactCheckerTool


def create_researcher() -> Agent:
    """Build and return the Researcher agent."""
    llm = get_llm(temperature=0.2)  # Low temperature for factual accuracy

    return Agent(
        role="Senior Technical Researcher",
        goal=(
            "Research the given topic thoroughly and produce a comprehensive "
            "research brief covering key concepts, recent developments, expert "
            "opinions, statistics, and related technologies. Provide well-structured "
            "findings that a technical writer can use to create an authoritative blog post."
        ),
        backstory=(
            "You are a senior technical researcher with 15+ years of experience "
            "in technology journalism and analysis. You have deep expertise across "
            "multiple technology domains including AI, cloud computing, cybersecurity, "
            "and emerging technologies. You excel at finding authoritative sources, "
            "cross-referencing claims, and synthesising complex information into "
            "clear, actionable research briefs. You always cite sources and distinguish "
            "between established facts and emerging trends."
        ),
        tools=[SummarizeTool(), FactCheckerTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        memory=True,
        cache=True,
    )
