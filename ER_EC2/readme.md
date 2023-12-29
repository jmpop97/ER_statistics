## After git clone

this manual is recommended for aws ec2 ubuntu instance

0. need install mongoDB to make EC2 as DB
    1) easily install by install_mongoDB.sh
        ```
        sudo chmod +x install_mongoDB.sh init_scheduler.sh
        ./install_mongoDB.sh
        ```

        if worked succesfully, then will print mongod service active
        jump to [v.setting mongoDB configuration](#setting-mongoDB-configuration)
    2) install python
        ```
        # python3 -> python
        sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10

        # pip3 -> pip
        sudo apt-get update
        sudo apt-get install -y python3-pip
        pip3 --version
        sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
        ```
    3) install mongoDB
        ```
        # UTC to KST(Option)
        sudo ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime
            
        # Import the public key used by the package management system
        sudo apt-get install gnupg
        curl -fsSL https://pgp.mongodb.com/server-6.0.asc | sudo gpg -o /usr/share/keyrings/mongodb-server-6.0.gpg --dearmor
        
        # Create a list file for MongoDB
        echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-6.0.gpg ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
        
        # Reload local package database
        sudo apt-get update

        # Install the MongoDB packages.
        sudo apt-get install -y mongodb
        ```
    4) start mongodb service
        ```
        sudo service mongod start
        sudo service mongod status
        ```
    5) ###### setting mongoDB configuration
        ```sudo vim /etc/mongod.conf```
        &nbsp;
        in /etc/mongod.conf
        ```
        # network interfaces
        net:
        port: 27017
        bindIp: 0.0.0.0 # edit bindip

        security:
        authorization: enabled # enable security
        ```
    6) edit EC2 inbound rule to connect to DB
        &nbsp;

1. create user in mongoDB to access
&nbsp;
2. make setting directory and files to acces to DB
&nbsp;
    (0) move files in ER_EC2
    ```
    cp -r ./ER_EC2 ./
    ```
    (1) make setting folder
    ```
    mkdir /path/to/ER_statistics/setting # don't expose
    ```
    (1) secrete.json file
    secrete.json file is for request ER api to server
    ```
    {
        "token":"your_ER_api_token"
    }
    ```
    
    (2) secrete_db.json file
    secrete_db.json file is used to access your mongoDB
    encrypt_connection_url.sh can encrypt your db connection url to make ER_statistics/setting/secret_db.json
    ```
    encrypt_connection_url.sh mongodb://<role1_read_write>:<ROLE1_PASSWORD>@<EC2_public_IPv4_DNS> mongodb://<role2_read>:<ROLE2_PASSWORD>@<EC2_public_IPv4_DNS>
    ``` 
    ```
    {
    "EC2_DB_CONNECTION_STRING" : "encrypted_db_connection_string_read_write",
    "READ_EC2_DB_CONNECTION_STRING" : "encrypted_db_connection_string_read_only"
    }
    ```

3. execute init_schduler.sh to use crontab to request apis everyday
   	```
    chmod +x init_scheduler.sh
    # Automately add insert_to_mongoDB.sh and storage_check.sh to scheduler
    ./init_scheduler.sh
   	```    
    
