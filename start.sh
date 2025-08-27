#!/usr/bin/env bash
set -e

export FLASK_APP=app:create_app

# apply DB migrations at boot (ignore “already applied”)
flask db upgrade || true

# IMPORTANT: Docker on Render expects port 10000
exec gunicorn -k gthread -w 2 -b 0.0.0.0:10000 "app:create_app()"
