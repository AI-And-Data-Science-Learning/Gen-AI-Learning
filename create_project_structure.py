#!/usr/bin/env python3
"""
create_project_structure.py

Creates the Gen-AI-Learning project directory structure: source code for
LLM wrappers, prompt management, RAG/embeddings pipelines, notebooks,
tests, configs, and environment setup.

Run this from the root of your project (where .git lives):
    python3 create_project_structure.py

Safe to re-run: existing files are left untouched, only missing ones are created.
"""

import os

PY_INIT = "\"\"\"Package initializer.\"\"\"\n"

PROJECT_STRUCTURE = {

    # -------------------- src: core application code --------------------
    "src": {
        "__init__.py": PY_INIT,
        "main.py": (
            '"""Entry point for running the Gen-AI application."""\n\n'
            "from src.llm.client import get_llm_client\n"
            "from src.utils.logger import get_logger\n\n"
            "logger = get_logger(__name__)\n\n\n"
            "def main():\n"
            "    client = get_llm_client()\n"
            "    response = client.complete(\"Hello, world!\")\n"
            "    logger.info(response)\n\n\n"
            "if __name__ == \"__main__\":\n"
            "    main()\n"
        ),
    },

    # -------------------- src/llm: model clients / wrappers --------------------
    "src/llm": {
        "__init__.py": PY_INIT,
        "client.py": (
            '"""LLM client wrapper.\n\n'
            'Centralizes model calls so the rest of the codebase does not depend\n'
            'directly on a specific provider SDK.\n"""\n\n'
            "import os\n\n\n"
            "class LLMClient:\n"
            "    \"\"\"Thin wrapper around an LLM provider's API.\"\"\"\n\n"
            "    def __init__(self, model: str = \"claude-sonnet-4-6\", api_key: str | None = None):\n"
            "        self.model = model\n"
            "        self.api_key = api_key or os.environ.get(\"ANTHROPIC_API_KEY\")\n"
            "        if not self.api_key:\n"
            "            raise ValueError(\"Missing ANTHROPIC_API_KEY. Set it in your .env file.\")\n\n"
            "    def complete(self, prompt: str) -> str:\n"
            "        \"\"\"Send a prompt to the model and return the text response.\"\"\"\n"
            "        # TODO: wire up the real API call (anthropic / openai / etc.)\n"
            "        raise NotImplementedError\n\n\n"
            "def get_llm_client() -> LLMClient:\n"
            "    return LLMClient()\n"
        ),
    },

    # -------------------- src/rag: retrieval-augmented generation --------------------
    "src/rag": {
        "__init__.py": PY_INIT,
        "retriever.py": (
            '"""Retrieval logic for RAG: embed a query and fetch nearest documents."""\n\n'
            "from src.rag.vector_store import VectorStore\n\n\n"
            "class Retriever:\n"
            "    def __init__(self, vector_store: VectorStore):\n"
            "        self.vector_store = vector_store\n\n"
            "    def retrieve(self, query: str, top_k: int = 5) -> list[str]:\n"
            "        \"\"\"Return the top_k most relevant chunks for a query.\"\"\"\n"
            "        # TODO: embed query and call vector_store.search\n"
            "        return []\n"
        ),
        "vector_store.py": (
            '"""Vector store wrapper for storing and searching embeddings."""\n\n\n'
            "class VectorStore:\n"
            "    \"\"\"Minimal interface for a vector database (Chroma, FAISS, Pinecone, etc.).\"\"\"\n\n"
            "    def __init__(self, persist_directory: str = \"embeddings\"):\n"
            "        self.persist_directory = persist_directory\n\n"
            "    def add(self, texts: list[str], metadatas: list[dict] | None = None):\n"
            "        \"\"\"Embed and store a batch of text chunks.\"\"\"\n"
            "        # TODO: implement embedding + storage\n"
            "        raise NotImplementedError\n\n"
            "    def search(self, query: str, top_k: int = 5) -> list[str]:\n"
            "        \"\"\"Return the top_k most similar stored chunks.\"\"\"\n"
            "        # TODO: implement similarity search\n"
            "        raise NotImplementedError\n"
        ),
    },

    # -------------------- src/prompts: prompt loading/templating --------------------
    "src/prompts": {
        "__init__.py": PY_INIT,
        "loader.py": (
            '"""Loads prompt templates from the prompts/ directory."""\n\n'
            "import os\n\n"
            "PROMPTS_DIR = \"prompts\"\n\n\n"
            "def load_prompt(name: str, **kwargs) -> str:\n"
            "    \"\"\"Load a prompt template by file name (without extension) and format it.\"\"\"\n"
            "    path = os.path.join(PROMPTS_DIR, f\"{name}.txt\")\n"
            "    with open(path, \"r\") as f:\n"
            "        template = f.read()\n"
            "    return template.format(**kwargs)\n"
        ),
    },

    # -------------------- src/utils --------------------
    "src/utils": {
        "__init__.py": PY_INIT,
        "logger.py": (
            '"""Shared structured logger used across the project."""\n\n'
            "import logging\n\n\n"
            "def get_logger(name: str) -> logging.Logger:\n"
            "    logger = logging.getLogger(name)\n"
            "    if not logger.handlers:\n"
            "        handler = logging.StreamHandler()\n"
            "        formatter = logging.Formatter(\"%(asctime)s | %(name)s | %(levelname)s | %(message)s\")\n"
            "        handler.setFormatter(formatter)\n"
            "        logger.addHandler(handler)\n"
            "        logger.setLevel(logging.INFO)\n"
            "    return logger\n"
        ),
    },

    # -------------------- src/config: settings / env loading --------------------
    "src/config": {
        "__init__.py": PY_INIT,
        "settings.py": (
            '"""Centralized configuration, loaded from environment variables (.env).\"\"\"\n\n'
            "import os\n\n"
            "from dotenv import load_dotenv\n\n"
            "load_dotenv()\n\n\n"
            "class Settings:\n"
            "    ANTHROPIC_API_KEY: str | None = os.environ.get(\"ANTHROPIC_API_KEY\")\n"
            "    OPENAI_API_KEY: str | None = os.environ.get(\"OPENAI_API_KEY\")\n"
            "    DEFAULT_MODEL: str = os.environ.get(\"DEFAULT_MODEL\", \"claude-sonnet-4-6\")\n"
            "    VECTOR_STORE_PATH: str = os.environ.get(\"VECTOR_STORE_PATH\", \"embeddings\")\n"
            "    LOG_LEVEL: str = os.environ.get(\"LOG_LEVEL\", \"INFO\")\n\n\n"
            "settings = Settings()\n"
        ),
    },

    # -------------------- prompts: raw prompt template files --------------------
    "prompts": {
        "system_prompt.txt": "You are a helpful assistant for the Gen-AI-Learning project.\n",
        "rag_query_prompt.txt": (
            "Use the following context to answer the question.\n\n"
            "Context:\n{context}\n\n"
            "Question:\n{question}\n"
        ),
    },

    # -------------------- embeddings: generated/persisted vector data --------------------
    "embeddings": {".gitkeep": ""},

    # -------------------- notebooks: experiments --------------------
    "notebooks": {".gitkeep": ""},

    # -------------------- data --------------------
    "data/raw": {".gitkeep": ""},
    "data/processed": {".gitkeep": ""},

    # -------------------- models: locally cached / fine-tuned models --------------------
    "models": {".gitkeep": ""},

    # -------------------- logs --------------------
    "logs": {".gitkeep": ""},

    # -------------------- docs --------------------
    "docs": {".gitkeep": ""},

    # -------------------- scripts: one-off automation --------------------
    "scripts": {
        "setup_env.sh": (
            "#!/usr/bin/env bash\n"
            "# One-time environment setup for Gen-AI-Learning\n\n"
            "python3 -m venv .venv\n"
            "source .venv/bin/activate\n"
            "pip install -r requirements/requirements.txt\n"
            "pip install -r requirements/requirements-dev.txt\n"
            "cp .env.example .env\n"
            "echo \"Setup complete. Edit .env with your real API keys.\"\n"
        ),
    },

    # -------------------- config: non-secret app configuration --------------------
    "config": {
        "config.yaml": (
            "model:\n"
            "  default: claude-sonnet-4-6\n"
            "  temperature: 0.7\n"
            "  max_tokens: 1000\n\n"
            "rag:\n"
            "  chunk_size: 500\n"
            "  chunk_overlap: 50\n"
            "  top_k: 5\n"
        ),
    },

    # -------------------- tests --------------------
    "tests": {"__init__.py": PY_INIT},
    "tests/unit": {"__init__.py": PY_INIT},
    "tests/integration": {"__init__.py": PY_INIT},

    # -------------------- requirements --------------------
    "requirements": {
        "requirements.txt": (
            "anthropic\n"
            "openai\n"
            "python-dotenv\n"
            "chromadb\n"
            "tiktoken\n"
            "numpy\n"
            "pandas\n"
        ),
        "requirements-dev.txt": (
            "pytest\n"
            "ruff\n"
            "black\n"
            "ipykernel\n"
            "jupyter\n"
        ),
    },
}

# ---------------------------------------------------------------------------
# Root-level files
# ---------------------------------------------------------------------------

README_CONTENT = """# Gen-AI-Learning

A hands-on learning repository for exploring Generative AI concepts: LLM integration, prompt engineering, retrieval-augmented generation (RAG), embeddings, and building small end-to-end AI-powered applications.

## \U0001F3AF Overview

This repository is organized as a modular codebase for experimenting with and learning Generative AI techniques. It separates concerns into clear components: LLM client wrappers, prompt management, retrieval/embeddings for RAG, configuration, and tests — so each part can be built, tested, and understood independently.

### Objectives
1. Learn to structure a Gen-AI project with proper Git practices (branching, issue templates, PR templates, `.gitignore`, GitHub Actions)
2. Build reusable LLM client wrappers that are provider-agnostic
3. Implement prompt templating and management
4. Build a basic RAG pipeline (embeddings + vector store + retriever)
5. Practice safe handling of API keys and secrets via `.env`
6. Write unit and integration tests for AI-powered code

### \U0001F4CB Prerequisites

| Requirement | Specified Version / Component |
| :--- | :--- |
| OS / Environment | Windows 11 + WSL2 (Ubuntu) or macOS/Linux |
| Python | Python 3.10+ |
| Package Manager | `pip` (or `uv`, optional) |
| LLM Provider | Anthropic API key and/or OpenAI API key |
| Vector Store | ChromaDB (local, no external service required) |

## Setup and installation instructions

### \U0001F680 Quick Start

```bash
# Clone the repo and move into it
git clone <repo-url>
cd Gen-AI-Learning

# Set up Python virtual environment
python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\\Scripts\\activate

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
\u2502
\u251c\u2500\u2500 .github/
\u2502   \u251c\u2500\u2500 ISSUE_TEMPLATE/
\u2502   \u2502   \u251c\u2500\u2500 bug_report.md
\u2502   \u2502   \u2514\u2500\u2500 feature.md
\u2502   \u251c\u2500\u2500 PULL_REQUEST_TEMPLATE.md
\u2502   \u251c\u2500\u2500 workflows/
\u2502   \u2514\u2500\u2500 CODEOWNERS
\u2502
\u251c\u2500\u2500 src/
\u2502   \u251c\u2500\u2500 main.py                  # Application entry point
\u2502   \u251c\u2500\u2500 llm/
\u2502   \u2502   \u2514\u2500\u2500 client.py            # LLM provider wrapper (model-agnostic)
\u2502   \u251c\u2500\u2500 rag/
\u2502   \u2502   \u251c\u2500\u2500 retriever.py         # Retrieval logic for RAG
\u2502   \u2502   \u2514\u2500\u2500 vector_store.py      # Vector store wrapper (Chroma/FAISS/etc.)
\u2502   \u251c\u2500\u2500 prompts/
\u2502   \u2502   \u2514\u2500\u2500 loader.py            # Loads and formats prompt templates
\u2502   \u251c\u2500\u2500 config/
\u2502   \u2502   \u2514\u2500\u2500 settings.py          # Centralized settings, loaded from .env
\u2502   \u2514\u2500\u2500 utils/
\u2502       \u2514\u2500\u2500 logger.py            # Shared structured logger
\u2502
\u251c\u2500\u2500 prompts/                     # Raw prompt template files (.txt)
\u2502   \u251c\u2500\u2500 system_prompt.txt
\u2502   \u2514\u2500\u2500 rag_query_prompt.txt
\u2502
\u251c\u2500\u2500 embeddings/                  # Persisted vector store data (gitignored)
\u2502
\u251c\u2500\u2500 notebooks/                   # Jupyter notebooks for experiments
\u2502
\u251c\u2500\u2500 data/
\u2502   \u251c\u2500\u2500 raw/                     # Raw source data (gitignored)
\u2502   \u2514\u2500\u2500 processed/               # Processed/cleaned data (gitignored)
\u2502
\u251c\u2500\u2500 models/                      # Locally cached or fine-tuned models (gitignored)
\u2502
\u251c\u2500\u2500 logs/                        # Application logs (gitignored)
\u2502
\u251c\u2500\u2500 docs/                        # Project documentation
\u2502
\u251c\u2500\u2500 scripts/
\u2502   \u2514\u2500\u2500 setup_env.sh             # One-time environment setup script
\u2502
\u251c\u2500\u2500 config/
\u2502   \u2514\u2500\u2500 config.yaml              # Non-secret app configuration
\u2502
\u251c\u2500\u2500 tests/
\u2502   \u251c\u2500\u2500 unit/
\u2502   \u2514\u2500\u2500 integration/
\u2502
\u251c\u2500\u2500 requirements/
\u2502   \u251c\u2500\u2500 requirements.txt
\u2502   \u2514\u2500\u2500 requirements-dev.txt
\u2502
\u251c\u2500\u2500 .env.example                 # Template for environment variables
\u251c\u2500\u2500 .gitignore
\u251c\u2500\u2500 pyproject.toml
\u251c\u2500\u2500 setup.cfg
\u251c\u2500\u2500 LICENSE
\u2514\u2500\u2500 README.md
```

## \U0001F91D Contributing Guidelines

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
"""

ROOT_FILES = {
    "README.md": README_CONTENT,

    "pyproject.toml": (
        "[build-system]\n"
        "requires = [\"setuptools>=61.0\"]\n"
        "build-backend = \"setuptools.build_meta\"\n\n"
        "[project]\n"
        "name = \"gen-ai-learning\"\n"
        "version = \"0.1.0\"\n"
        "description = \"Experiments and learning projects in Generative AI\"\n"
        "requires-python = \">=3.10\"\n"
    ),

    "setup.cfg": (
        "[flake8]\n"
        "max-line-length = 100\n"
        "exclude = .venv,__pycache__,notebooks\n"
    ),

    # Real, filled-in example env file -- the actual .env (with real secrets)
    # stays out of git via .gitignore.
    ".env.example": (
        "# Copy this file to .env and fill in your real values.\n"
        "# Never commit the real .env file.\n\n"
        "# --- LLM provider keys ---\n"
        "ANTHROPIC_API_KEY=your_anthropic_api_key_here\n"
        "OPENAI_API_KEY=your_openai_api_key_here\n\n"
        "# --- Model defaults ---\n"
        "DEFAULT_MODEL=claude-sonnet-4-6\n\n"
        "# --- Vector store / RAG ---\n"
        "VECTOR_STORE_PATH=embeddings\n\n"
        "# --- Logging ---\n"
        "LOG_LEVEL=INFO\n"
    ),

    ".gitignore": (
        "__pycache__/\n"
        "*.pyc\n"
        ".env\n"
        ".venv/\n"
        "venv/\n"
        "logs/\n"
        "data/raw/\n"
        "data/processed/\n"
        "embeddings/\n"
        "models/\n"
        ".ipynb_checkpoints/\n"
        "*.egg-info/\n"
        ".pytest_cache/\n"
        ".DS_Store\n"
    ),
}


def write_file(path: str, content: str):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)
        print(f"  Created file: {path}")
    else:
        print(f"  Skipped (already exists): {path}")


def create_structure(base_path="."):
    for folder, files in PROJECT_STRUCTURE.items():
        dir_path = os.path.join(base_path, folder)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")

        if not files:
            write_file(os.path.join(dir_path, ".gitkeep"), "")
        else:
            for file_name, content in files.items():
                write_file(os.path.join(dir_path, file_name), content)

    for file_name, content in ROOT_FILES.items():
        write_file(os.path.join(base_path, file_name), content)


if __name__ == "__main__":
    create_structure(".")
    print("\nGen-AI-Learning project structure created successfully.")
