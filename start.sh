#!/usr/bin/env bash
set -e

# Ensure the persistent disk path exists
mkdir -p /var/data

# Let Flask know where the factory lives
export FLASK_APP=app:create_app

# Run DB migrations (safe to run every boot)
flask db upgrade || true

# Start the app with Gunicorn on the provided port
exec gunicorn "app:create_app()" -b 0.0.0.0:${PORT:-8000} --workers=2
