# CrewAI Blog System

> A production-ready multi-agent system that automates technical blog post generation using CrewAI.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/crewai-0.95+-brightgreen.svg)](https://crewai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Three specialised AI agents work together in a sequential pipeline to research, write, and edit high-quality technical blog posts:

| Agent | Role | Temperature |
|---|---|---|
| **Researcher** | Gathers facts, statistics, and expert opinions on the topic | 0.2 (factual) |
| **Writer** | Transforms research into an engaging, well-structured blog post | 0.7 (creative) |
| **Editor** | Reviews for accuracy, style, and Markdown formatting | 0.3 (balanced) |

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Researcher   │────▶│    Writer     │────▶│    Editor    │
│  (Gather)     │     │  (Compose)    │     │  (Polish)    │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
  Research Brief    Draft Blog Post    Final Markdown
```

### Memory
Each agent has **short-term memory** (conversation context), **long-term memory** (cross-run knowledge), and **entity memory** (consistent terminology). The Crew-level configuration in `.crewai/config.yaml` enables all three.

### Security
- **Input sanitisation** — blocked patterns (shell commands, eval/exec, pickle) are rejected before any agent processes the topic
- **Secret shielding** — API keys are redacted in logs and error messages
- **No eval/exec** — all tools use safe JSON serialisation
- **Environment-based config** — secrets live in `.env`, never in source code

## Prerequisites

- **Python** 3.10 or later (3.13 tested)
- **Euron API key** — obtain one from [euron.one](https://euron.one)

## Installation

```bash
# 1. Clone or copy the project
cd crewai-blog-system

# 2. Create a virtual environment (if you haven't already)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS / Linux

# 3. Install dependencies
pip install -e ".[dev]"

# 4. Configure your API key
cp .env.example .env
# Edit .env and put your real Euron API key:
#   EURON_API_KEY=sk-your-real-key-here
```

## Usage

### Command Line

```bash
# Generate a blog post on a topic
crewai-blog-system "The Future of Quantum Computing"

# Or run as a module
python -m crewai_blog_system "Introduction to Rust"
```

The output is written to `output/blog-post.md` in clean Markdown format.

### Programmatic

```python
from crewai_blog_system.main import generate_blog

result = generate_blog("Machine Learning MLOps")
print(result.raw)  # The final Markdown text
```

## Project Structure

```
crewai-blog-system/
├── .crewai/
│   └── config.yaml          # CrewAI Cloud deployment + memory config
├── .github/
│   └── workflows/
│       └── crewai-deploy.yml # CI/CD pipeline for CrewAI Cloud
├── crewai_blog_system/
│   ├── __init__.py
│   ├── __main__.py           # python -m entry point
│   ├── main.py               # CLI entry point, generate_blog()
│   ├── config.py             # .env loading, get_llm()
│   ├── security.py           # sanitize_topic(), shield_secret()
│   ├── tools.py              # SummarizeTool, StructureTool, FactCheckerTool
│   ├── crew.py               # build_crew()
│   ├── tasks.py              # create_research_task/writing_task/editing_task()
│   └── agents/
│       ├── __init__.py       # Exports create_researcher/writer/editor
│       ├── researcher.py
│       ├── writer.py
│       └── editor.py
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_security.py
│   └── test_tools.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Configuration

### `.env`

| Variable | Required | Description |
|---|---|---|
| `EURON_API_KEY` | Yes | Your Euron API key for LLM calls |

The config module validates on import and raises `ValueError` if the key is missing.

### `.crewai/config.yaml`

Controls CrewAI Cloud deployment settings (name, version, process type, memory). The GitHub Actions workflow pushes to this config on every push to `main`.

## Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=crewai_blog_system --cov-report=term-missing
```

## Linting

```bash
ruff check crewai_blog_system/ tests/
```

## Deployment to CrewAI Cloud

1. **Get your organization ID** from [app.crewai.com](https://app.crewai.com) → Settings
2. Open `.crewai/config.yaml` and replace `your-organization-id` with your real ID
3. Push your code to a **GitHub repository**
4. Add these GitHub secrets (**Settings → Secrets and variables → Actions**):

   | Secret | Get from |
   |---|---|
   | `CREWAI_USERNAME` | Your CrewAI Cloud login email/username |
   | `CREWAI_PASSWORD` | Your CrewAI Cloud password |
   | `EURON_API_KEY` | Your Euron API key from [euron.one](https://euron.one) |

5. The `.github/workflows/crewai-deploy.yml` workflow triggers automatically on pushes to `main` —
   it runs `crewai login`, then `crewai deploy`, using your `.crewai/config.yaml` for deployment settings

### Local deploy (optional)

```powershell
.venv\Scripts\activate
set EURON_API_KEY=your-euron-key
crewai login
crewai deploy
```

## Agent Details

### Researcher (Senior Technical Researcher)
- **Goal**: Produce a comprehensive research brief (1500–2500 words) with key concepts, recent developments, expert opinions, and statistics
- **Tools**: `SummarizeTool`, `FactCheckerTool`
- **Temperature**: 0.2 (prioritises factual accuracy)
- **Backstory**: 15+ years in technology journalism and analysis

### Writer (Staff Technical Writer)
- **Goal**: Transform the research brief into a 2000–3000 word blog post with engaging title, clear sections, code examples, and actionable takeaways
- **Tools**: `StructureTool`
- **Temperature**: 0.7 (allows creative expression)
- **Backstory**: 10+ years writing for developers at leading tech media companies

### Editor (Senior Technical Editor)
- **Goal**: Review and polish the draft for technical accuracy, grammar, style, logical flow, and proper Markdown formatting
- **Tools**: `FactCheckerTool`
- **Temperature**: 0.3 (balanced precision)
- **Backstory**: 20+ years editing for O'Reilly, InfoQ, and IEEE Spectrum

## Security

| Feature | Implementation |
|---|---|
| API key handling | Loaded from `.env` at import time; validated on startup |
| Secret shielding | `shield_secret()` redacts keys in logs (shows only last 4 chars) |
| Input sanitisation | `sanitize_topic()` blocks shell injection, eval/exec, and pickle patterns |
| Safe tools | All `BaseTool` subclasses use JSON serialisation; no shell commands |

## License

MIT — see the `pyproject.toml` for details.

## Acknowledgements

Built with [CrewAI](https://crewai.com/) using the Euron AI platform.
