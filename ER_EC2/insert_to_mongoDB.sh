#!/bin/bash
INSERT_DOCUMENT_NUMBER=1000
DISK_LIMIT=90;

# get disk_used by df command
disk_used=$(df / | grep ^/ | awk '{print $5}');
# substring $
disk_used=${disk_used::-1};

# need to move ER_DIR_PATH to use setting/secret.json
cd $ER_DIR_PATH

# if DISK_LIMIT > disk_used
# then execute python ./insert_mongoDB.py $INSERT_DOCUMENT_NUMBER to save game match datas.
test $DISK_LIMIT -gt $disk_used && nohup python ${ER_DIR_PATH}/insert_mongoDB.py --n $INSERT_DOCUMENT_NUMBER &