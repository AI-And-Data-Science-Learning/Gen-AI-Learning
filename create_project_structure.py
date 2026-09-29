#!/usr/bin/env python3
"""
create_project_structure.py

Creates a standard project directory structure for the repo.
Run this from the root of your project (where .git lives).

Usage:
    python create_project_structure.py
"""

import os

# Define the folder structure here.
# Each key is a directory path; each value is a list of placeholder files to create inside it.
PROJECT_STRUCTURE = {
    # Core application code
    "src": ["__init__.py", "main.py"],
    "src/utils": ["__init__.py"],
    "src/models": ["__init__.py"],
    "src/services": ["__init__.py"],
    "src/config": ["__init__.py"],

    # Gen-AI specific folders
    "prompts": [".gitkeep"],
    "embeddings": [".gitkeep"],
    "models": [".gitkeep"],

    # Tests
    "tests": ["__init__.py"],
    "tests/unit": ["__init__.py"],
    "tests/integration": ["__init__.py"],

    # Notebooks for experimentation
    "notebooks": [".gitkeep"],

    # Data folders
    "data/raw": [".gitkeep"],
    "data/processed": [".gitkeep"],
    "data/external": [".gitkeep"],

    # Docs
    "docs": [".gitkeep"],

    # Standalone scripts (one-off automation, data pulls, etc.)
    "scripts": [".gitkeep"],

    # App / env configuration
    "config": [".gitkeep"],

    # Logs (usually gitignored)
    "logs": [".gitkeep"],
}

# Top-level files to create if they don't already exist
ROOT_FILES = {
    "README.md": "# Project Title\n\nProject description goes here.\n",
    "requirements.txt": "",
    "requirements-dev.txt": "pytest\nblack\nflake8\n",
    "pyproject.toml": (
        "[build-system]\n"
        "requires = [\"setuptools>=61.0\"]\n"
        "build-backend = \"setuptools.build_meta\"\n\n"
        "[project]\n"
        "name = \"project-name\"\n"
        "version = \"0.1.0\"\n"
        "description = \"\"\n"
        "requires-python = \">=3.10\"\n"
    ),
    "setup.cfg": "",
    ".env.example": "# Copy this file to .env and fill in real values\nAPI_KEY=\n",
    ".gitignore": (
        "__pycache__/\n"
        "*.pyc\n"
        ".env\n"
        ".venv/\n"
        "venv/\n"
        "logs/\n"
        "data/raw/\n"
        "data/processed/\n"
        "data/external/\n"
        "embeddings/\n"
        "models/\n"
        ".ipynb_checkpoints/\n"
        "*.egg-info/\n"
        ".pytest_cache/\n"
    ),
}


def create_structure(base_path="."):
    for folder, files in PROJECT_STRUCTURE.items():
        dir_path = os.path.join(base_path, folder)
        os.makedirs(dir_path, exist_ok=True)
        print(f"Created directory: {dir_path}")

        for file_name in files:
            file_path = os.path.join(dir_path, file_name)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    pass
                print(f"  Created file: {file_path}")

    for file_name, content in ROOT_FILES.items():
        file_path = os.path.join(base_path, file_name)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(content)
            print(f"Created root file: {file_path}")
        else:
            print(f"Skipped (already exists): {file_path}")


if __name__ == "__main__":
    create_structure(".")
    print("\nProject structure created successfully.")