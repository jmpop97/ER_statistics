#!/bin/bash

#if you already installed postfix
sudo apt-get install postfix -y

sudo chmod +x ./storage_check.sh ./insert_to_mongoDB.sh

# edit crontab
crontab -l > cron_backup
ER_DIR_PATH=$(pwd)

# added environment path
echo "SHELL=/bin/bash" >> cron_backup
echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" >> cron_backup
echo "ER_DIR_PATH=${ER_DIR_PATH}" >> cron_backup
# minute, hour, day, month, day of the week
# storage check every 30 minutes
echo "*/30 * * * * ${ER_DIR_PATH}/storage_check.sh >> ${ER_DIR_PATH}/logs/storage_check.log 2>&1" >> cron_backup
# insert game match datas every day 00:00
echo "0 0 * * * ${ER_DIR_PATH}/insert_to_mongoDB.sh >> ${ER_DIR_PATH}/logs/insert_to_mongoDB.log 2>&1" >> cron_backup
# insert top ranking players
echo "0 9 * * * ${ER_DIR_PATH}/get_top_ranking_players.sh > ${ER_DIR_PATH}/logs/get_top_ranking_players.sh 2>&1" >> cron_backup
# editing crontab done
crontab cron_backup
