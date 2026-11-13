#!/bin/sh
set -eu

cd /app

if [ "${1:-}" = "uvicorn" ]; then
    alembic upgrade head
    python -m db.config.seed all
    python -c "import cli; cli.run()" currency_rates_update
fi

exec "$@"
