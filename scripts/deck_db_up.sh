#!/bin/bash

set -e

echo -e DECK_DB_UP

echo -e "\nActivate venv ..."
source .venv/bin/activate

echo -e "\nRestart deck-service (docker-compose) ..."
cd deck-service
docker compose down
docker compose up -d

echo -e "\nRun alembic upgrade head ..."
cd app
sleep 3
alembic upgrade head

echo -e "\nDeactivate venv ..."
deactivate

echo -e "\nFinish!\n"
