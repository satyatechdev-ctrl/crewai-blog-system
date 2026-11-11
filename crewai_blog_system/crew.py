"""Crew orchestration: assembles agents, tasks, and memory into a Crew.

This module builds the Crew object and runs it. It is the main entry point
for both local execution and CrewAI Cloud deployment.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

from crewai import Crew, Process

from crewai_blog_system.agents import create_researcher, create_writer, create_editor
from crewai_blog_system.tasks import create_research_task, create_writing_task, create_editing_task

logger = logging.getLogger("crewai_blog_system.crew")


def build_crew(topic: str) -> Crew:
    """Build the three-agent Crew for a given topic.

    All agents share memory (short-term + entity).
    Process is SEQUENTIAL so each agent receives the output of the previous one.
    """
    researcher = create_researcher()
    writer = create_writer()
    editor = create_editor()

    research_task = create_research_task(topic)
    writing_task = create_writing_task(topic)
    editing_task = create_editing_task(topic)

    # Assign agents to tasks
    research_task.agent = researcher
    writing_task.agent = writer
    editing_task.agent = editor

    return Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=True,
        # Memory configuration – both short-term and entity memory enabled
        memory=True,
        embedder={
            "config": {
                "model": "text-embedding-3-small",
                "api_key": "",  # Uses EURON_API_KEY from env via langchain-openai
            }
        },
        # Cache LLM responses to avoid redundant calls
        cache=True,
    )


def run_crew(
    topic: str,
    output_dir: Optional[str] = None,
) -> str:
    """Run the blog-creation crew and return the final Markdown output.

    Parameters
    ----------
    topic : str
        The blog post topic (will be sanitised).
    output_dir : str, optional
        Directory to write the output Markdown file. Defaults to ``output/``.

    Returns
    -------
    str
        The final Markdown content of the blog post.
    """
    logger.info("Starting blog post generation for topic: %s", topic)

    crew = build_crew(topic)
    result = crew.kickoff()

    # Extract the raw Markdown from the Crew result
    # CrewAI returns a CrewOutput; get the raw string
    final_md = str(result)

    # Write output file
    if output_dir is None:
        output_dir = "output"
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    safe_filename = topic.lower().replace(" ", "-")[:80]
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    md_file = out_path / f"{safe_filename}-{timestamp}.md"

    md_file.write_text(final_md, encoding="utf-8")
    logger.info("Blog post written to %s", md_file)

    # Write a JSON metadata file alongside the Markdown
    meta = {
        "topic": topic,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "agents": ["Researcher", "Writer", "Editor"],
        "process": "sequential",
        "memory_enabled": True,
        "output_file": str(md_file),
    }
    meta_file = out_path / f"{safe_filename}-{timestamp}.json"
    meta_file.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")

    return final_md
