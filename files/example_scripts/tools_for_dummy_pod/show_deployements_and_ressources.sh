#!/bin/bash

my_true=0
my_false=1

function run_command() {
    echo "Running: $@"
    $@
}

echo "Reference link: https://kubernetes.io/docs/tutorials/hello-minikube/"
echo ""
echo "Viewing deployment"
run_command sudo kubectl get deployments
echo "Viewing the pods"
run_command sudo kubectl get pods
user_pods="$(sudo kubectl get pods)"
echo "Viewing cluster events"
run_command sudo kubectl get events
echo "Viewing kubectl's configuration"
run_command sudo kubectl config view
echo "Viewing application logs"
echo "$user_pods"
read -p "Please enter the name of the pod you wish to view the logs for:" pod_name
run_command sudo kubectl logs "$pod_name"
echo "Ressource: https://kubernetes.io/docs/tutorials/hello-minikube/#create-a-service"
echo "viewing the service that was created"
run_command sudo kubectl get services
sleep 2s
echo "Accessing the service"
run_command sudo kubectl get services
cont=$my_true
while [ $cont -eq $my_true ]; do
    read -p "Please enter the 'EXTERNAL-IP' of the pod you wish to view (enter r to display available services, q to exit):" pod_ip
    if [ $pod_ip == "r" ] || [ $pod_ip == "R" ]; then
        run_command sudo kubectl get services
        continue
    elif [ $pod_ip == "q" ] || [ $pod_ip == "Q" ]; then
        cont=$my_false
        continue
    else
        read -p "Please enter the port number (from 'PORT(S)') on which to find the website (if it has already been specifiyed, just press enter):" ip_port
        if [ ${#ip_port} -ne 0 ]; then
            ip_port=":$ip_port"
        fi
        data="$(wget $pod_ip$ip_port -q -O -)"
        echo "$data"
        continue
    fi
done
