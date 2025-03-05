#!/bin/bash

set -e


echo -e "\nRestart profile-service (docker-compose) ..."
cd profile-service
docker compose down
docker compose up -d

echo -e "\nActivate venv ..."
source .venv/bin/activate


echo -e "\nRun alembic upgrade head ..."
cd app
sleep 2
alembic upgrade head

echo -e "\nRun fake_data/main.py ..."
cd utils/fake_data
python main.py

echo -e "\nDeactivate venv ..."
deactivate

echo -e "\nFinish!"
