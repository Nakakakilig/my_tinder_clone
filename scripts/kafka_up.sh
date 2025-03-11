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

    docker exec -it kafka-kafka-1 kafka-topics \
        --create --topic profile-events \
        --bootstrap-server localhost:9092 \
        # --partitions 1 --replication-factor 1
fi

echo -e "\nFinish!\n"
