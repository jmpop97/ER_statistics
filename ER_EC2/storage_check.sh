# DISK LIMIT percentage
DISK_LIMIT=90;
DOCUMENT_DELETE_NUMBER=1000;

# get disk_used by df command
disk_used=$(df / | grep ^/ | awk '{print $5}');
# substring $
disk_used=${disk_used::-1};
# if DISK_LIMIT < disk_used
# then execute python ./delete_old_files.py $DOCUMENT_DELETE_NUMBER
test $DISK_LIMIT -lt $disk_used && python ./delete_old_files.py $DOCUMENT_DELETE_NUMBER