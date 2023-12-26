# DISK LIMIT percentage
CURRENT_PATH=$(pwd)
DISK_LIMIT=98;
DOCUMENT_DELETE_NUMBER=1000;

# get disk_used by df command
disk_used=$(df / | grep ^/ | awk '{print $5}');
# substring $
disk_used=${disk_used::-1};
# if DISK_LIMIT < disk_used
# then execute python ./delete_old_files.py $DOCUMENT_DELETE_NUMBER
# absolute path
test $DISK_LIMIT -lt $disk_used && nohup python ${CURRENT_PATH}/delete_old_files.py $DOCUMENT_DELETE_NUMBER &