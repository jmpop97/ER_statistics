sudo cp -r ./ ../
sudo chmod +x ./test.sh

# edit crontab
crontab -l > cron_backup
ER_DIR_PATH=$(pwd)

current_time=$(date +"%Y-%m-%d %H:%M:%S")
next_time=$(date -d "$current_time + 1 minute" +"%Y-%m-%d %H:%M:%S")
next_hour=$(date -d "$next_time" +"%H")
next_minute=$(date -d "$next_time" +"%M")

# added environment path
echo "SHELL=/bin/bash" >> cron_backup
echo "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin" >> cron_backup
echo "ER_DIR_PATH=${ER_DIR_PATH}" >> cron_backup
# minute, hour, day, month, day of the week
# storage check every 30 minutes
echo "${next_minute} ${next_hour} * * * ${ER_DIR_PATH}/test.sh >> ${ER_DIR_PATH}/logs/test.log 2>&1" >> cron_backup
crontab cron_backup