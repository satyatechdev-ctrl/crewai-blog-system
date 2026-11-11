"""Entry point for the CrewAI blog system."""

import argparse
import sys
from pathlib import Path
from typing import Sequence

from crewai_blog_system.crew import BlogCrew
from crewai_blog_system.security import ValidationError

DEFAULT_TOPIC = "The Future of AI-Powered Code Review Tools"


def generate_blog(topic: str = DEFAULT_TOPIC) -> str:
    """Run the blog crew for a given topic."""
    return BlogCrew().kickoff({"topic": topic})


def run(topic: str = DEFAULT_TOPIC) -> str:
    """Backward-compatible alias for :func:`generate_blog`."""
    return generate_blog(topic)


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Generate a technical blog post.")
    parser.add_argument("topic", nargs="?", default=DEFAULT_TOPIC, help="Blog post topic")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("output/blog-post.md"),
        help="Markdown output path (default: output/blog-post.md)",
    )
    parser.add_argument(
        "--stdout-only",
        action="store_true",
        help="Print the post without writing an output file",
    )
    args = parser.parse_args(argv)

    try:
        result = generate_blog(args.topic)
    except ValidationError as error:
        parser.error(str(error))

    print(result)
    if not args.stdout_only:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result, encoding="utf-8")
        print(f"Saved blog post to {args.output}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
