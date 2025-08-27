#!/usr/bin/env bash
set -euxo pipefail

export FLASK_APP="app:create_app"

# Apply DB migrations (safe if already up-to-date)
flask db upgrade || true

# Start Gunicorn on Render’s port
exec gunicorn -k gthread -w ${WORKERS:-2} -b 0.0.0.0:${PORT:-10000} "app:create_app()"
