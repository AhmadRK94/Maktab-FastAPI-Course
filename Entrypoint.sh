#!/bin/sh
set -e  # Exit immediately if a command fails

echo "Running Alembic migrations..."
alembic upgrade head

echo "Starting FastAPI app..."
exec uvicorn main:app --host 0.0.0.0 --port 8000
