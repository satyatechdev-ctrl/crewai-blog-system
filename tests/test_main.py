from pathlib import Path

import crewai_blog_system.main as cli


def test_main_writes_blog_post_to_output_file(tmp_path, monkeypatch, capsys):
    output = tmp_path / "nested" / "post.md"
    monkeypatch.setattr(cli, "generate_blog", lambda topic: f"# {topic}\n")

    assert cli.main(["Test Topic", "--output", str(output)]) == 0

    assert output.read_text(encoding="utf-8") == "# Test Topic\n"
    assert "# Test Topic" in capsys.readouterr().out


def test_main_stdout_only_does_not_create_file(tmp_path, monkeypatch):
    monkeypatch.setattr(cli, "generate_blog", lambda topic: "Post body")
    monkeypatch.chdir(tmp_path)

    assert cli.main(["Test Topic", "--stdout-only"]) == 0
    assert not Path("output/blog-post.md").exists()
