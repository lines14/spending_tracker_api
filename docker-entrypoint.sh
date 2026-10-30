#!/bin/sh
set -eu

cd /app

if [ "${1:-}" = "uvicorn" ]; then
    alembic upgrade head
fi

exec "$@"
