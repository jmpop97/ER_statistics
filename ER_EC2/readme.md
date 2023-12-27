after git clone

0. need install mongoDB to make EC2 as DB
    1) install python
        ```
        # python3 -> python
        sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10

        # pip3 -> pip
        sudo apt-get update
        sudo apt-get install -y python3-pip
        pip3 --version
        sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
        ```
    2) install mongoDB
        ```
        # UTC to KST
        sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
    
        # port forwarding
        sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 5000
        
        # Import the public key used by the package management system
        sudo apt-get install gnupg
        curl -fsSL https://pgp.mongodb.com/server-6.0.asc | \
        sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg \ --dearmor
        
        # Create a list file for MongoDB
        echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
        
        # Reload local package database
        sudo apt-get update

        # Install the MongoDB packages.
        sudo apt-get install -y mongodb
        ```
        start mongodb service
        ```
        sudo service mongod start
        sudo service mongod status
        ```
        setting mongoDB configuration
        ```
        sudo vim /etc/mongod.conf
        ```
        ```
        # network interfaces
        net:
        port: 27017
        bindIp: 0.0.0.0 # edit bindip

        security:
        authorization: enabled # enable security
        ```
    3) install requirements.txt
        ```pip install -r requirements.txt```


1. need to start as root
	```
    sudo su
	```    

2. create user in mongoDB to access

3. make setting directory and fiels to acces to DB
    ```
    mkdir setting
    sudo cp secret_db.json ER_statistics_path/setting
    ```
    ex) secrete_db.json file 
    ```
    {
    "EC2_DB_CONNECTION_STRING" : "encrypted_db_connection_string_read_write",
    "READ_EC2_DB_CONNECTION_STRING" : "encrypted_db_connection_string_read_only"
    }
    ```

4. copy files in /ER_statistics/ER_EC2 to /ER_statistics/
   	```
    cp -r ./ER_EC2 ./
    chmod +x init.sh
    # Automately add insert_to_mongoDB.sh and storage_check.sh to scheduler
    ./init.sh
   	```    
    
