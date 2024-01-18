# ec2 inbound rule 처리
# cluster 내 ec2를 같은 보안 그룹으로 처리

#!/bin/bash
status=$(sudo systemctl status mongod | grep "Active" | awk '{print $2}')
echo $status
: << "END"
set_name=$2

mongo_conf="/etc/mongod.conf"
db_path=$(grep "dbPath" $mongo_conf | awk '$2')
echo $db_path
cp $mongo_conf $db_path/mongod_backup.conf
cat > $mongo_conf <<EOF
# mongod.conf

storage:
  dbPath: $db_path

systemLog:
  destination: file
  logAppend: true
  path: /var/log/mongodb/mongod.log

net:
  port: 27017
  bindIp: 0.0.0.0

processManagement:
  timeZoneInfo: /usr/share/zoneinfo

replication:
  replSetName: $set_name

security:
  authorization: enabled
  keyFile: ${db_path}/mongodb.key
EOF


openssl rand -base64 741 > ${dbPath}/mongodb.key
chmod 600 mongodb.key

sudo systemctl stop mongod
sudo systemctl start mongod

sudo systemctl stop mongod
sudo systemctl start mongod
status=$(grep "Active" sudo systemctl status mongod | awk '$2')

mongosh << EOF
rs.status
exit
EOF

# /etc/mongod.conf
storage:
    dbPath: /root/
replication:
    replSetName: "set_name"
security:
    authorization: enabled
    keyFile: ${dbPath}/mongodb.key

openssl rand -base64 741 > ${dbPath}/mongodb.key
chmod 600 mongodb.key


sudo systemctl stop mongod
sudo systemctl start mongod
sudo systemctl status mongod 

mongosh
echo "rs.initiate({
    _id : \"set_name\",
    members : [
        {_id : 0, host : \"<BindIp>:<Port>\"},
        {_id : 1, host : \"<BindIp>:<Port>\"},
        {_id : 2, host : \"<BindIp>:<Port>\"},
    ]
})"
rs.status