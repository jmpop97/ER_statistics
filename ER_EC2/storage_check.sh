#!/bin/bash

# DISK LIMIT percentage
DISK_LIMIT=98;
DOCUMENT_DELETE_NUMBER=100;

# get disk_used by df command
disk_used=$(df / | grep ^/ | awk '{print $5}');
# substring $
disk_used=${disk_used::-1};

# need to move ER_DIR_PATH to use setting/secret.json
cd $ER_DIR_PATH

# if DISK_LIMIT < disk_used
# then execute python ./delete_old_files.py $DOCUMENT_DELETE_NUMBER
# absolute path
test $DISK_LIMIT -lt $disk_used && nohup python ${ER_DIR_PATH}/delete_old_files.py --n $DOCUMENT_DELETE_NUMBER &