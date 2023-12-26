sudo chmod +x ./storage_check.sh ./insert_to_mongoDB.sh
crontab -l > cron_backup
echo "0 0 * * * ./storage_check.sh" >> cron_backup
crontab cron_tabkup