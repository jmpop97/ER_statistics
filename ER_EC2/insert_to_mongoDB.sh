INSERT_DOCUMENT_NUMBER = 1000
DISK_LIMIT=90;
DOCUMENT_DELETE_NUMBER=1000;

# get disk_used by df command
disk_used=$(df / | grep ^/ | awk '{print $5}');
# substring $
disk_used=${disk_used::-1};
# if DISK_LIMIT > disk_used
# then execute python ./insert_mongoDB.py $INSERT_DOCUMENT_NUMBER to save game match datas.
test $DISK_LIMIT -gt $disk_used && python ./insert_mongoDB.py --n $INSERT_DOCUMENT_NUMBER