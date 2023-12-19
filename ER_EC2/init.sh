sudo chmod +x ./storage_check.sh ./insert_to_mongoDB.sh
crontab -l > cron_backup
# storage check every 30 minutes
echo "*/30 * * * * ./storage_check.sh" >> cron_backup
# insert game match datas every day 
echo "0 0 * * * python ./insert_mongoDB.py" >> cron_backup
crontab cron_backup