#!/usr/bin/env bash
set -e

# Safe: apply migrations; ignore "already applied" cases
flask db upgrade || true

# Start gunicorn on the port Render provides
exec gunicorn -k gthread -w 2 -b 0.0.0.0:$PORT "app:create_app()"
