"""Tests for tool classes.

All tests run in-memory without LLM calls or network access.
"""

from __future__ import annotations

import pytest

from crewai_blog_system.tools import SummarizeTool, StructureTool, FactCheckerTool


class TestSummarizeTool:
    """Tests for the SummarizeTool."""

    def test_summarize_normal_text(self):
        tool = SummarizeTool()
        result = tool._run("This is some test text for summarisation.")
        assert "SUMMARISE" in result
        assert "chars" in result

    def test_summarize_empty_string(self):
        tool = SummarizeTool()
        result = tool._run("")
        assert "Error" in result

    def test_summarize_none(self):
        tool = SummarizeTool()
        result = tool._run(None)  # type: ignore
        assert "Error" in result

    def test_summarize_non_string(self):
        tool = SummarizeTool()
        result = tool._run(12345)  # type: ignore
        assert "Error" in result

    def test_tool_name(self):
        tool = SummarizeTool()
        assert tool.name == "summarize_text"

    def test_tool_description(self):
        tool = SummarizeTool()
        assert "summarise" in tool.description.lower()


class TestStructureTool:
    """Tests for the StructureTool."""

    def test_create_outline(self):
        tool = StructureTool()
        result = tool._run("Quantum Computing", "Research notes go here...")
        assert "OUTLINE" in result
        assert "Quantum Computing" in result

    def test_missing_topic(self):
        tool = StructureTool()
        result = tool._run("", "Research notes...")
        assert "Error" in result

    def test_missing_research(self):
        tool = StructureTool()
        result = tool._run("Topic", "")
        assert "Error" in result

    def test_tool_name(self):
        tool = StructureTool()
        assert tool.name == "create_outline"


class TestFactCheckerTool:
    """Tests for the FactCheckerTool."""

    def test_fact_check_valid_claim(self):
        tool = FactCheckerTool()
        result = tool._run("Quantum computers use qubits.")
        import json
        data = json.loads(result)
        assert data["verdict"] == "NEEDS_REVIEW"
        assert data["claim"] == "Quantum computers use qubits."

    def test_fact_check_empty_claim(self):
        tool = FactCheckerTool()
        result = tool._run("")
        assert "Error" in result

    def test_fact_check_non_string(self):
        tool = FactCheckerTool()
        result = tool._run(42)  # type: ignore
        assert "Error" in result

    def test_fact_check_with_context(self):
        tool = FactCheckerTool()
        result = tool._run("AI will replace all jobs", context="This is a debated claim.")
        import json
        data = json.loads(result)
        assert data["verdict"] == "NEEDS_REVIEW"

    def test_output_is_valid_json(self):
        """Ensure all outputs are valid JSON (no eval/exec needed to parse)."""
        import json
        tool = FactCheckerTool()
        result = tool._run("Test claim")
        # Should not raise
        json.loads(result)

    def test_tool_name(self):
        tool = FactCheckerTool()
        assert tool.name == "fact_check"
