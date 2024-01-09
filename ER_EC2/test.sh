#!/bin/bash

# DISK LIMIT percentage
DISK_LIMIT=0;
# get disk_used by df command
disk_used=$(df / | grep ^/ | awk '{print $5}');
# substring $
disk_used=${disk_used::-1};

# need to move ER_DIR_PATH to use setting/secret.json
cd $ER_DIR_PATH

# if DISK_LIMIT < disk_used
test $DISK_LIMIT -lt $disk_used && nohup python ${ER_DIR_PATH}/test.py $INSERT_DOCUMENT_NUMBER &