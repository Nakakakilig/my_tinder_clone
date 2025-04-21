#!/usr/bin/env bash

set -e

echo "Run apply migrations ..."

source .venv/bin/activate
cd app
alembic upgrade head

echo "Migrations applied!"

exec "$@"
