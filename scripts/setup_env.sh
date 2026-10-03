#!/usr/bin/env bash
# One-time environment setup for Gen-AI-Learning

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements/requirements.txt
pip install -r requirements/requirements-dev.txt
cp .env.example .env
echo "Setup complete. Edit .env with your real API keys."
