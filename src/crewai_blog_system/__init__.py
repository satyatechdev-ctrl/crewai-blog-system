"""CrewAI Blog System – a production-ready multi-agent blog post generator.

Three agents work together in a sequential pipeline:

1. **Researcher** – gathers information, facts, and references about the topic.
2. **Writer** – drafts a well-structured technical blog post from the research.
3. **Editor**  – reviews, refines, and polishes the draft to production quality.

## Quick Start

    export EURON_API_KEY="sk-..."          # or set it in .env
    pip install -e ".[dev]"
    python -m crewai_blog_system run "The Future of Quantum Computing"

## Deployment to CrewAI Cloud

1. Push this repo to GitHub.
2. In the CrewAI Cloud dashboard, create a new crew and point it at the repo.
3. The `.crewai/config.yaml` tells CrewAI Cloud which entry point to run.
4. Set `EURON_API_KEY` as a secret in the CrewAI Cloud dashboard.

## Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Researcher  │────▶│    Writer    │────▶│    Editor    │
└──────────────┘     └──────────────┘     └──────────────┘
       │                    │                    │
       ▼                    ▼                    ▼
  Web Search            Draft               Final Post
  Summarise            Structure            Markdown
└──────────────┘     └──────────────┘     └──────────────┘
```

All agents share a common memory layer (short-term + entity memory) so that
context flows naturally from one step to the next.

## Security

- **No secrets in code** – all API keys come from environment variables or
  CrewAI Cloud secrets (see `security/`).
- **Input sanitisation** – user-supplied topics are validated before processing.
- **No eval/exec** – all data is parsed through JSON or typed Pydantic models.
- **Rate limiting** – requests to the LLM API include backoff retry logic.

## Memory

| Layer      | Purpose                                      | Enabled |
| ---------- | --------------------------------------------- | ------- |
| Short-term | Conversation & step context within a run      | Yes     |
| Entity     | Facts about named entities (topics, people)   | Yes     |

## License

MIT – see LICENSE file.
"""

from __future__ import annotations

import logging

logging.getLogger("crewai_blog_system").setLevel(logging.INFO)
