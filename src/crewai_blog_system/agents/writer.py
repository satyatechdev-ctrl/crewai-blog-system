"""Writer agent: drafts the blog post from research findings.

Role
----
The Writer is the second agent in the pipeline. It:

1. Reads the research brief produced by the Researcher.
2. Structures a comprehensive technical blog post including:
   - An engaging introduction with a hook
   - Clear section headings (H2, H3)
   - Code examples where relevant
   - Data visualisations described in text
   - A conclusion with key takeaways and next steps
3. Writes in a professional, engaging tone suitable for a technical audience.

The Writer uses entity memory to maintain consistency of terminology
throughout the post.
"""

from __future__ import annotations

from crewai import Agent

from crewai_blog_system.config import get_llm
from crewai_blog_system.tools import StructureTool


def create_writer() -> Agent:
    """Build and return the Writer agent."""
    llm = get_llm(temperature=0.7)  # Higher temperature for creative writing

    return Agent(
        role="Staff Technical Writer",
        goal=(
            "Transform the research brief into a polished, well-structured "
            "technical blog post. The post should be engaging, informative, "
            "and suitable for publication on a professional technology blog. "
            "Include an introduction, body sections with clear headings, "
            "code examples where applicable, a conclusion with key takeaways, "
            "and a call-to-action for readers."
        ),
        backstory=(
            "You are a staff technical writer at a leading technology media "
            "company with 10+ years of experience writing for developers and "
            "engineering leaders. You have written hundreds of technical articles "
            "covering AI, cloud infrastructure, DevOps, and emerging technologies. "
            "Your writing style is clear, authoritative, and engaging. You excel at "
            "explaining complex technical concepts in accessible language without "
            "sacrificing accuracy. You always structure your posts with clear "
            "headings, include practical examples, and end with actionable takeaways."
        ),
        tools=[StructureTool()],
        llm=llm,
        verbose=True,
        allow_delegation=False,
        memory=True,
        cache=True,
    )
