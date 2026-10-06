#!/bin/bash
set -e

if [ "$1" = "celery" ]; then
    echo "Starting Celery worker..."
    exec "$@"
else
    echo "Running migrations..."
    alembic upgrade head

    echo "Starting server..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000
fi
