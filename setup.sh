#!/usr/bin/env bash
# One-time setup.
# The venv lives outside the project because this folder's name contains ":" — Python refuses
# to create a venv there (":" is the PATH separator, so activation would break).
set -euo pipefail
VENV="${ABD_VENV:-$HOME/.venvs/abd-bot}"
PY="${PYTHON:-python3}"

"$PY" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install -r "$(dirname "$0")/requirements.txt"
echo "✅ Setup ho gaya. Ab chalao: ./run.sh"
