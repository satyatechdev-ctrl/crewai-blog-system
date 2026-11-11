import pytest
from crewai import Crew

import crewai_blog_system.config as config
from crewai_blog_system.crew import build_crew
from crewai_blog_system.security import ValidationError


def test_cloud_entrypoint_builds_configured_crew(monkeypatch):
    monkeypatch.setenv("EURON_API_KEY", "test-key")
    monkeypatch.setenv("OPENAI_BASE_URL", "https://api.euron.one/api/v1/euri")

    crew = build_crew()

    assert isinstance(crew, Crew)
    assert len(crew.agents) == 3
    assert len(crew.tasks) == 3
    assert all(task.agent is not None for task in crew.tasks)


def test_build_crew_reports_missing_api_key(monkeypatch):
    monkeypatch.setattr(config, "load_dotenv", lambda: None)
    monkeypatch.delenv("EURON_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="EURON_API_KEY"):
        build_crew()


def test_before_kickoff_validates_and_normalizes_topic(monkeypatch):
    monkeypatch.setenv("EURON_API_KEY", "test-key")
    crew = build_crew()

    validated = crew.before_kickoff_callbacks[0]({"topic": "  Docker & Kubernetes  "})

    assert validated["topic"] == "Docker & Kubernetes"


def test_before_kickoff_rejects_unsafe_topic(monkeypatch):
    monkeypatch.setenv("EURON_API_KEY", "test-key")
    crew = build_crew()

    with pytest.raises(ValidationError, match="disallowed characters"):
        crew.kickoff(inputs={"topic": "<script>"})
