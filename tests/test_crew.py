from crewai import Crew

from crewai_blog_system.crew import build_crew


def test_cloud_entrypoint_builds_configured_crew(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.euron.one/api/v1/euri")

    crew = build_crew()

    assert isinstance(crew, Crew)
    assert len(crew.agents) == 3
    assert len(crew.tasks) == 3
    assert all(task.agent is not None for task in crew.tasks)
