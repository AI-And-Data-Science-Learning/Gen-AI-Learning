# Gen-AI-Learning

A hands-on learning repository for exploring Generative AI concepts: LLM integration, prompt engineering, retrieval-augmented generation (RAG), embeddings, and building small end-to-end AI-powered applications.

## 🎯 Overview

This repository is organized as a modular codebase for experimenting with and learning Generative AI techniques. It separates concerns into clear components: LLM client wrappers, prompt management, retrieval/embeddings for RAG, configuration, and tests — so each part can be built, tested, and understood independently.

### Objectives
1. Learn to structure a Gen-AI project with proper Git practices (branching, issue templates, PR templates, `.gitignore`, GitHub Actions)
2. Build reusable LLM client wrappers that are provider-agnostic
3. Implement prompt templating and management
4. Build a basic RAG pipeline (embeddings + vector store + retriever)
5. Practice safe handling of API keys and secrets via `.env`
6. Write unit and integration tests for AI-powered code

### 📋 Prerequisites

| Requirement | Specified Version / Component |
| :--- | :--- |
| OS / Environment | Windows 11 + WSL2 (Ubuntu) or macOS/Linux |
| Python | Python 3.10+ |
| Package Manager | `pip` (or `uv`, optional) |
| LLM Provider | Anthropic API key and/or OpenAI API key |
| Vector Store | ChromaDB (local, no external service required) |

## Setup and installation instructions

### 🚀 Quick Start

```bash
# Clone the repo and move into it
git clone <repo-url>
cd Gen-AI-Learning

# Set up Python virtual environment
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements/requirements.txt
pip install -r requirements/requirements-dev.txt

# Set up your environment variables
cp .env.example .env
# Then edit .env and add your real API keys
```

Or run the one-step setup script:

```bash
bash scripts/setup_env.sh
```

### Environment variables

This project uses a `.env` file (never committed) for secrets, based on `.env.example`:

```bash
ANTHROPIC_API_KEY=your_anthropic_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
DEFAULT_MODEL=claude-sonnet-4-6
VECTOR_STORE_PATH=embeddings
LOG_LEVEL=INFO
```

`src/config/settings.py` loads these automatically via `python-dotenv`.

## Steps to run

```bash
# Run the main entry point
python3 src/main.py

# Run tests
pytest tests/

# Format and lint
black .
ruff check .
```

## Folder structure

```plaintext
Gen-AI-Learning/
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── workflows/
│   └── CODEOWNERS
│
├── src/
│   ├── main.py                  # Application entry point
│   ├── llm/
│   │   └── client.py            # LLM provider wrapper (model-agnostic)
│   ├── rag/
│   │   ├── retriever.py         # Retrieval logic for RAG
│   │   └── vector_store.py      # Vector store wrapper (Chroma/FAISS/etc.)
│   ├── prompts/
│   │   └── loader.py            # Loads and formats prompt templates
│   ├── config/
│   │   └── settings.py          # Centralized settings, loaded from .env
│   └── utils/
│       └── logger.py            # Shared structured logger
│
├── prompts/                     # Raw prompt template files (.txt)
│   ├── system_prompt.txt
│   └── rag_query_prompt.txt
│
├── embeddings/                  # Persisted vector store data (gitignored)
│
├── notebooks/                   # Jupyter notebooks for experiments
│
├── data/
│   ├── raw/                     # Raw source data (gitignored)
│   └── processed/               # Processed/cleaned data (gitignored)
│
├── models/                      # Locally cached or fine-tuned models (gitignored)
│
├── logs/                        # Application logs (gitignored)
│
├── docs/                        # Project documentation
│
├── scripts/
│   └── setup_env.sh             # One-time environment setup script
│
├── config/
│   └── config.yaml              # Non-secret app configuration
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── requirements/
│   ├── requirements.txt
│   └── requirements-dev.txt
│
├── .env.example                 # Template for environment variables
├── .gitignore
├── pyproject.toml
├── setup.cfg
├── LICENSE
└── README.md
```

## 🤝 Contributing Guidelines

1. **Find or create an issue** describing the bug or feature, using the templates in `.github/ISSUE_TEMPLATE/`.
2. **Branch from `main`** using the issue number and a short description:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b <issue-number>-<short-description>
   ```
3. **Write clean, documented code** following the structure above.
4. **Format before committing**:
   ```bash
   black .
   ruff check .
   ```
5. **Open a pull request** using the template in `.github/PULL_REQUEST_TEMPLATE.md`, filling in description, linked issue, and testing notes.
