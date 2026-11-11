"""Blog crew implementation – CrewAI Cloud compatible (@CrewBase)."""

from typing import Any

from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_blog_system.tools import (
    FactCheckerTool,
    StructureTool,
    SummarizeTool,
)


@CrewBase
class BlogCrew:
    """Multi-agent blog post generation crew.

    Researcher → Writer → Editor pipeline.
    Config driven from config/agents.yaml and config/tasks.yaml.
    """

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["researcher"],
            tools=[SummarizeTool(), FactCheckerTool()],
            llm=self._get_llm(),
            verbose=True,
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config["writer"],
            tools=[StructureTool()],
            llm=self._get_llm(),
            verbose=True,
        )

    @agent
    def editor(self) -> Agent:
        return Agent(
            config=self.agents_config["editor"],
            tools=[FactCheckerTool()],
            llm=self._get_llm(),
            verbose=True,
        )

    @task
    def research_task(self) -> Task:
        return Task(config=self.tasks_config["research_task"])

    @task
    def write_task(self) -> Task:
        return Task(config=self.tasks_config["write_task"])

    @task
    def edit_task(self) -> Task:
        return Task(config=self.tasks_config["edit_task"])

    @crew
    def crew(self) -> Crew:
        """Create and return the Crew."""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            memory=True,
            cache=True,
        )

    # ------------------------------------------------------------------
    # Helpers (keep env-reading logic for backwards compat)
    # ------------------------------------------------------------------

    @staticmethod
    def _get_api_key() -> str:
        import os

        return os.environ.get("OPENAI_API_KEY", "")

    @staticmethod
    def _get_base_url() -> str:
        import os

        return os.environ.get("OPENAI_BASE_URL", "https://api.euron.one/api/v1/euri")

    def _get_llm(self) -> LLM:
        return LLM(
            model="openai/euri-reasoning",
            api_key=self._get_api_key(),
            base_url=self._get_base_url(),
        )

    def kickoff(self, inputs: dict[str, Any]) -> str:
        """Run the crew with the given inputs and return the final output."""
        result = self.crew().kickoff(inputs=inputs)
        return result.raw


def build_crew() -> Crew:
    """Build the crew referenced by the CrewAI Cloud entrypoint."""
    return BlogCrew().crew()
