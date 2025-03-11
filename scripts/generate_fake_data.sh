#!/bin/bash

set -e


echo -e \nGENERATE FAKE DATA IN PROFILE-SERVICE
echo -e BUT YOU NEED RUN BOTH PROFILE-SERVICE AND DECK-SERVICE
echo -e SO KAFKA EVENTS COPY DATA TO DECK-SERVICE


echo -e "\nActivate venv ..."
source .venv/bin/activate

echo -e "\nRun profile-service/app/utils/fake_data/main.py ..."
cd profile-service
python app/utils/fake_data/main.py

echo -e "\nDeactivate venv ..."
deactivate

echo -e "\nFinish!\n"
