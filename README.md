# CrewAI Blog System

> A multi-agent system for drafting and editing technical blog posts with CrewAI.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![CrewAI](https://img.shields.io/badge/crewai-0.95+-brightgreen.svg)](https://crewai.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Three specialised AI agents work in a sequential pipeline to research, write, and edit technical blog posts. Research uses model knowledge, not live web search.

| Agent | Role |
|---|---|
| **Researcher** | Drafts a research brief from the topic and model knowledge |
| **Writer** | Transforms the brief into an engaging, structured blog post |
| **Editor** | Reviews style, clarity, and Markdown formatting |

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

### Security
- **Topic validation** — topics are checked for length and disallowed characters before agents process them
- **Environment-based config** — API keys are read from the environment or local `.env` file
- Topic validation is not a defense against prompt injection, and the fact-checking helper does not independently verify claims

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

# Print without saving to a file
crewai-blog-system "Introduction to Rust" --stdout-only

# Choose an output path
crewai-blog-system "Introduction to Rust" --output output/rust.md
```

By default, the Markdown post is saved to `output/blog-post.md` and printed to stdout.

### Programmatic

```python
from crewai_blog_system.main import generate_blog

result = generate_blog("Machine Learning MLOps")
print(result)  # The final Markdown text
```

## Project Structure

```
crewai-blog-system/
├── .crewai/
│   └── config.yaml          # CrewAI Cloud deployment + memory config
├── .github/
│   └── workflows/
│       └── crewai-deploy.yml # CI/CD pipeline for CrewAI Cloud
├── src/
│   └── crewai_blog_system/
│       ├── __main__.py       # python -m entry point
│       ├── main.py           # CLI and generate_blog() API
│       ├── security.py       # Topic validation
│       ├── tools.py          # Extractive summary, outline, review helper
│       ├── crew.py           # @CrewBase and build_crew()
│       ├── config/           # CrewAI agent/task YAML and API config
│       └── agents/           # Agent factories
├── tests/
│   ├── __init__.py
│   ├── test_config.py
│   ├── test_security.py
│   ├── test_tools.py
│   ├── test_crew.py
│   └── test_main.py
├── .env.example
├── .gitignore
├── pyproject.toml
└── README.md
```

## Configuration

### `.env` or environment

| Variable | Required | Description |
|---|---|---|
| `EURON_API_KEY` | Yes | Your Euron API key for LLM calls (preferred) |
| `OPENAI_API_KEY` | No | Accepted as a compatibility fallback |
| `OPENAI_BASE_URL` | No | Optional API endpoint override |

The application loads `.env` when it first needs configuration and raises a clear error if neither API key is set.

### `.crewai/config.yaml`

Controls CrewAI Cloud deployment settings (entry point, model, process type, and memory).

## Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=crewai_blog_system --cov-report=term-missing
```

## Linting

```bash
ruff check src/crewai_blog_system/ tests/
```

## Deployment to CrewAI Cloud

1. **Get your organization ID** from [app.crewai.com](https://app.crewai.com) → Settings
2. Confirm `.crewai/config.yaml` contains your organization ID
3. Push your code to a **GitHub repository**
4. Configure `EURON_API_KEY` in the CrewAI Cloud deployment secrets so the running crew can access the Euron API.
5. The workflow runs locked tests and lint checks on pushes and pull requests. On pushes to `main`, it validates the crew using a non-production placeholder key, then creates and pushes the deployment. The placeholder is only used to construct the crew; it is not an API credential and no API calls are made during this check.

### Local deploy (optional)

```powershell
.venv\Scripts\activate
$env:EURON_API_KEY = "your-euron-key"
crewai login
crewai deploy
```

## Agent Details

### Researcher (Senior Technical Researcher)
- **Goal**: Draft a research brief that distinguishes established knowledge from uncertain or time-sensitive claims
- **Tools**: extractive sentence helper and claim-review helper
- **Limitation**: No live web search; independently verify sources and current claims
- **Backstory**: 15+ years in technology journalism and analysis

### Writer (Staff Technical Writer)
- **Goal**: Transform the research brief into a 2000–3000 word blog post with engaging title, clear sections, code examples, and actionable takeaways
- **Tools**: Markdown outline helper
- **Backstory**: 10+ years writing for developers at leading tech media companies

### Editor (Senior Technical Editor)
- **Goal**: Review and polish the draft for unsupported claims, grammar, style, flow, and Markdown formatting
- **Tools**: `FactCheckerTool`
- **Backstory**: 20+ years editing for O'Reilly, InfoQ, and IEEE Spectrum

## Security

| Feature | Implementation |
|---|---|
| API key handling | Loaded from `.env` or the environment when needed; `EURON_API_KEY` is preferred |
| Topic validation | `sanitize_topic()` checks topic type, length, blocked patterns, and allowed characters |
| Claim review | `FactCheckerTool` flags claims for human review; it does not verify claims |
| Research | No external web search is configured; generated research may require independent sourcing |

## License

MIT — see the `pyproject.toml` for details.

## Acknowledgements

Built with [CrewAI](https://crewai.com/) using the Euron AI platform.
