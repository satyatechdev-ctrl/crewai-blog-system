"""Entry point for the CrewAI blog system."""

import sys

from crewai_blog_system.crew import BlogCrew


def run(topic: str = "The Future of AI-Powered Code Review Tools") -> str:
    """Run the blog crew for a given topic."""
    result = BlogCrew().kickoff({"topic": topic})
    return result


def main() -> None:
    """CLI entry point."""
    topic = sys.argv[1] if len(sys.argv) > 1 else "The Future of AI-Powered Code Review Tools"
    print(f"Starting blog creation for topic: {topic}")
    print("=" * 60)
    result = run(topic)
    print("\n\n" + "=" * 60)
    print("FINAL BLOG POST:")
    print("=" * 60)
    print(result)


if __name__ == "__main__":
    main()
