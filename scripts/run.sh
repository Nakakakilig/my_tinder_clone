#!/bin/bash

set -e

bash ./scripts/kafka_up.sh || { echo "kafka_up.sh failed"; exit 1; }
bash ./scripts/profile_db_up.sh || { echo "profile_db_up.sh failed"; exit 1; }
bash ./scripts/deck_db_up.sh || { echo "deck_db_up.sh failed"; exit 1; }
bash ./scripts/generate_fake_data.sh || { echo "generate_fake_data.sh failed"; exit 1; }
bash ./scripts/swipe_db_up.sh || { echo "swipe_db_up.sh failed"; exit 1; }
bash ./scripts/generate_fake_swipes.sh || { echo "generate_fake_swipes.sh failed"; exit 1; }
