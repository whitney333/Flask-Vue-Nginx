#!/usr/bin/env bash
# Run the backend natively against Mongo through the docker ssh-tunnel.
# Usage: ./dev.sh            (from backend_rebuild/)
set -euo pipefail
cd "$(dirname "$0")"

docker compose -f ../docker-compose.yml up -d ssh-tunnel

if [ ! -d .venv ]; then
  echo "No .venv found. Create it with:" >&2
  echo "  /opt/homebrew/opt/python@3.11/bin/python3.11 -m venv .venv && .venv/bin/pip install -r requirements.txt pandas" >&2
  exit 1
fi

# Debug mode: auto-reload on file changes + interactive debugger.
# Uses the flask CLI so main.py's app.run(debug=False) is bypassed without editing shared code.
export FLASK_APP=main
export FLASK_ENV=development
export FLASK_DEBUG=1
exec .venv/bin/flask run --host 0.0.0.0 --port 5001
