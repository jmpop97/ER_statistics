#!/bin/bash
status=$(sudo systemctl status mongod | grep "Active" | awk '{print $2}')
echo $status
if [ $status -ne "active" ]
then
  echo "systemctl status mongod is not working"
  exit(1)
fi
set_name=$1
host_ip_1=$2
host_ip_2=$3
host_ip_3=$4
mongo_conf="/etc/mongod.conf"
db_path=$(grep "dbPath" $mongo_conf | awk '$2')
port=$(grep "port" $mongo_conf | awk '$2')
echo $db_path
echo $port
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
status=$(sudo systemctl status mongod | grep "Active" | awk '{print $2}')
port=$(grep "port: " $mongo_conf | awk '$2')
port=${port:8}echo $status
if [ $status == "active" ]
then
  mongosh << EOF
  rs.initiate({
      _id : $set_name,
      members : [
          {_id : 0, host : $host_ip_1:$port},
          {_id : 1, host : $host_ip_2:$port},
          {_id : 2, host : $host_ip_3:$port},
      ]
  })
  rs.status
  exit
EOF
fi
