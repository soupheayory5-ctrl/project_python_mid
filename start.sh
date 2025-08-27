#!/usr/bin/env bash
set -e

# ensure Flask knows which app to load
export FLASK_APP=${FLASK_APP:-app:create_app}

echo "Running migrations..."
flask db upgrade || true

echo "Starting gunicorn..."
exec gunicorn -k gthread -w 2 -b 0.0.0.0:$PORT "app:create_app()"
