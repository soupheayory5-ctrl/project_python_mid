#!/usr/bin/env bash
set -e

# Needed for the CLI to find your factory
export FLASK_APP="app:create_app"

# Apply migrations (safe if already applied)
flask db upgrade || true

# Create or reset the admin if env vars are provided
if [[ -n "$ADMIN_USERNAME" && -n "$ADMIN_PASSWORD" ]]; then
  echo "Ensuring admin $ADMIN_USERNAME exists..."
  flask create-admin-if-missing "$ADMIN_USERNAME" "$ADMIN_PASSWORD" || true
fi

# Start gunicorn
exec gunicorn -k gthread -w ${WEB_CONCURRENCY:-2} -b 0.0.0.0:$PORT "app:create_app()"
