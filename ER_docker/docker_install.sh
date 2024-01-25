sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get install docker-ce docker-ce-cli containerd.io
sudo systemctl status docker
status=$(sudo systemctl status docker | grep "Active" | awk '{print $2}')
if [ $status == 'active'  ]
then
        docker_result=$(sudo docker run hello-world | grep "Hello" | awk '{print $1}')
        if [ $docker_result == "Hello" ]
        then
                echo "==== Installing & Running Docker processed normally"
        else
                echo "==== Problem From Running Docker"
                exit(2)
        fi
else
        echo "==== Problem From Installing Docker"
        exit(1)
fi

