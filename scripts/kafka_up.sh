#!/bin/bash

set -e

echo -e "\nCheck if Kafka container is already running..."

container_status=$(docker ps -q -f "name=kafka")

if [ -n "$container_status" ]; then
    echo -e "Kafka container is already running. Skipping restart."
else
    echo -e "\nRestart kafka (docker-compose) ..."
    cd kafka
    docker compose down
    docker compose up -d
fi

echo -e "\nFinish!\n"
