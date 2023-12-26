DISK_LIMIT=90;
DELETE_NUMBER=1000;

disk_used=$(df / | grep ^/ | awk '{print $5}');
disk_used=${disk_used::-1};
test $DISK_LIMIT -lt $disk_used && python ./delete_old_files.py $DELETE_NUMBER