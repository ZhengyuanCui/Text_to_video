#!/usr/bin/env bash
set -e

echo "=== Installing project dependencies ==="
pip install -r /workspace/requirements.txt

echo "=== Installing development tools ==="
pip install black flake8 pytest ipython

echo "=== Installing HuggingFace CLI and Git LFS ==="
pip install huggingface_hub
apt-get update && apt-get install -y git-lfs
git lfs install

echo "=== Setting up helpful aliases ==="
echo "alias run-api='uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload'" >> ~/.bashrc
echo "alias run-worker='celery -A backend.app.worker.celery_app worker --loglevel=INFO --concurrency=1'" >> ~/.bashrc
