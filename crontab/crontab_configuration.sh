#!/bin/bash

# Execute this script to configure your crontab to run the main.py script every Saturday at 00:00
CRONTAB_SCHEDULE="0 0 * * 6" # Every Saturday at 00:00
BOT_DIR="padel_7_booking_bot"
PYTHONPATH="/your/pyhon/path"

repo_dir=$(dirname "$(pwd)")
working_dir="${repo_dir}/${BOT_DIR}"
mkdir -p /var/logs/padel_booking_bot

(crontab -l ; echo "${CRONTAB_SCHEDULE} export PYTHONPATH=${PYTHONPATH} && cd ${working_dir} && /usr/bin/python3 main.py >> /var/logs/padel_booking_bot/bot.log 2>&1") | crontab -
