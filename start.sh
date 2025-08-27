#!/usr/bin/env bash
set -e

# Ensure env is loaded (Render sets these for you)
export FLASK_APP=${FLASK_APP:-app:create_app}
export FLASK_ENV=${FLASK_ENV:-production}

# Run migrations against Postgres
flask db upgrade || true

# Start Gunicorn
exec gunicorn -w 2 -k gthread -b 0.0.0.0:${PORT:-10000} "app:create_app()"
