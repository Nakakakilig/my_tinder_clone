#!/bin/bash

set -e

echo -e SWIPE_DB_UP

echo -e "\nActivate venv ..."
source .venv/bin/activate

echo -e "\nRestart swipe-service (docker-compose) ..."
cd swipe-service
docker compose down
docker compose up -d

echo -e "\nRun alembic upgrade head ..."
cd app
sleep 3
alembic upgrade head

echo -e "\nDeactivate venv ..."
deactivate

echo -e "\nFinish!\n"
