#!/usr/bin/env bash
# ./run.sh                                                → interactive bot (wizard)
# ./run.sh --style intraday --market stocks --symbol RELIANCE
# ./run.sh test                                           → run the test-suite
set -euo pipefail
cd "$(dirname "$0")"
VENV="${ABD_VENV:-$HOME/.venvs/abd-bot}"

if [ ! -x "$VENV/bin/python" ]; then
  echo "Pehle setup chalao: ./setup.sh" >&2
  exit 1
fi
if [ "${1:-}" = "test" ]; then
  shift
  exec "$VENV/bin/python" -m pytest "$@"
fi
exec "$VENV/bin/python" -m abd_bot "$@"
