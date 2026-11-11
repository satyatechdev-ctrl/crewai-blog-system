"""Main entry point for the CrewAI Blog System.

Usage:
    python -m crewai_blog_system run "Your blog topic here"
    python -m crewai_blog_system run "Your blog topic here" --output-dir ./my-output
"""

from __future__ import annotations

import argparse
import logging
import sys

from crewai_blog_system import security
from crewai_blog_system.crew import run_crew

logger = logging.getLogger("crewai_blog_system")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="crewai-blog-system",
        description="Automated technical blog post generation using CrewAI multi-agent system.",
    )
    parser.add_argument(
        "topic",
        nargs="?",
        default=None,
        help="The blog post topic (e.g. 'The Future of Quantum Computing').",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to write the output Markdown file (default: output/).",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable debug-level logging.",
    )
    return parser.parse_args(argv)


def run(argv: list[str] | None = None) -> None:
    """Run the blog generation pipeline."""
    args = parse_args(argv)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if not args.topic:
        parser = argparse.ArgumentParser()
        parser.error("the following arguments are required: topic")

    # Sanitise the topic (raises on bad input)
    try:
        safe_topic = security.sanitize_topic(args.topic)
    except security.ValidationError as exc:
        logger.error("Invalid topic: %s", exc)
        sys.exit(1)

    logger.info("=" * 60)
    logger.info("CrewAI Blog System v1.0.0")
    logger.info("Topic: %s", safe_topic)
    logger.info("Output directory: %s", args.output_dir)
    logger.info("=" * 60)

    try:
        final_md = run_crew(safe_topic, output_dir=args.output_dir)
        print("\n" + "=" * 60)
        print("BLOG POST GENERATED SUCCESSFULLY")
        print("=" * 60)
        print(final_md)
    except KeyboardInterrupt:
        logger.warning("Interrupted by user.")
        sys.exit(130)
    except Exception as exc:
        logger.error("Failed to generate blog post: %s", exc, exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run()
