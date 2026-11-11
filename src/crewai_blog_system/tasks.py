"""Task definitions for each agent in the blog-creation pipeline.

Tasks are connected by input/output so that output from one becomes
context for the next.
"""

from __future__ import annotations

from crewai import Task

from crewai_blog_system.security import sanitize_topic


def create_research_task(topic: str) -> Task:
    """Task 1: Research the topic."""
    safe_topic = sanitize_topic(topic)
    return Task(
        description=(
            f"Research the topic: **{safe_topic}**\n\n"
            "Cover relevant background including:\n"
            "1. Core concepts and definitions\n"
            "2. Established concepts and current limitations\n"
            "3. Widely known technologies and projects\n"
            "4. Practical applications and use cases\n"
            "5. Challenges and limitations\n\n"
            "Structure your research as a well-organised brief with clear sections.\n"
            "Do not invent statistics, expert quotes, or references. Flag "
            "time-sensitive facts that need independent verification.\n"
            "Distinguish established concepts from uncertain or time-sensitive claims."
        ),
        expected_output=(
            "A structured research brief covering the topic with clear Markdown "
            "headings. Flag claims that need independent verification, and do not "
            "include fabricated statistics, expert quotes, or references."
        ),
        agent=None,  # Set by the Crew when tasks are assigned
    )


def create_writing_task(topic: str) -> Task:
    """Task 2: Write the blog post from the research."""
    safe_topic = sanitize_topic(topic)
    return Task(
        description=(
            f"Write a comprehensive technical blog post about **{safe_topic}** "
            "based on the research brief provided by the Researcher.\n\n"
            "Your blog post should include:\n"
            "1. **Catchy Title** – engaging and SEO-friendly\n"
            "2. **Introduction** – hook the reader, state why this topic matters\n"
            "3. **Core Concepts** – explain key ideas clearly\n"
            "4. **Current Landscape** – what's happening now, key players\n"
            "5. **Deep Dive** – technical details for the interested reader\n"
            "6. **Practical Applications** – real-world use cases\n"
            "7. **Challenges & Limitations** – honest assessment\n"
            "8. **Future Outlook** – where is this heading?\n"
            "9. **Conclusion & Key Takeaways** – bullet-point summary\n"
            "10. **Call to Action** – encourage reader engagement\n\n"
            "Writing guidelines:\n"
            "- Use a professional yet conversational tone\n"
            "- Include code examples, tables, or diagrams (described in text) where helpful\n"
            "- Keep paragraphs short (3-5 sentences)\n"
            "- Use bold for key terms on first mention\n"
            "- Write for a senior developer / technical leader audience\n"
            "- Target length: 2000-3000 words"
        ),
        expected_output=(
            "A complete, well-written technical blog post in Markdown format, "
            "2000-3000 words, with a title, introduction, body sections with "
            "headings, code examples where relevant, and a conclusion with "
            "key takeaways. The post should be engaging, accurate, and ready "
            "for final editorial review."
        ),
        agent=None,
    )


def create_editing_task(topic: str) -> Task:
    """Task 3: Edit and polish the blog post."""
    safe_topic = sanitize_topic(topic)
    return Task(
        description=(
            f"Review and polish the draft blog post about **{safe_topic}** "
            "produced by the Writer.\n\n"
            "Perform the following edits:\n"
            "1. **Technical accuracy** – verify all claims are reasonable\n"
            "2. **Grammar & spelling** – fix any errors\n"
            "3. **Style consistency** – ensure uniform tone and formatting\n"
            "4. **Logical flow** – improve transitions between sections\n"
            "5. **Markdown formatting** – proper headings, lists, code blocks\n"
            "6. **Length check** – ensure the post is substantial but not bloated\n"
            "7. **Readability** – simplify overly complex sentences\n"
            "8. **SEO optimisation** – include relevant keywords naturally\n\n"
            "Output the FINAL, publication-ready Markdown document. "
            "Do NOT include any meta-commentary or editorial notes in the "
            "final output – only the clean Markdown."
        ),
        expected_output=(
            "A final, publication-ready technical blog post in clean Markdown "
            "format. The document should be free of errors, well-structured, "
            "engaging, and ready to publish on a professional technology blog. "
            "No editorial notes or meta-commentary – only the blog post content."
        ),
        agent=None,
    )
