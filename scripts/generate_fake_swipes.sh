#!/bin/bash

set -e


echo -e \nGENERATE FAKE SWIPES IN SWIPE-SERVICE

echo -e "\nActivate venv ..."
source .venv/bin/activate

echo -e "\nRun swipe-service/app/utils/fake_data/main.py ..."
cd swipe-service/app
python3 -m utils.fake_data.main

echo -e "\nDeactivate venv ..."
deactivate

echo -e "\nFinish!\n"
