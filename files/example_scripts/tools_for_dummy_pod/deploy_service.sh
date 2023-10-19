#!/bin/bash

my_true=0
my_false=1

function run_command() {
 echo "Running command: $@"
 $@
}

echo "Ressource: https://kubernetes.io/docs/tutorials/hello-minikube/#create-a-service"
echo "1 Exposing the pod to the public"
run_command sudo kubectl expose deployment hello-node --type=LoadBalancer --port=8080
echo "2 viewing the service that was created"
run_command sudo kubectl get services
sleep 2s
echo "3 Accessing the service"
run_command sudo kubectl get services
cont=$my_true
while [ $cont -eq $my_true ]
do
 read -p "Please enter the 'EXTERNAL-IP' of the pod you wish to view (enter r to display available services, q to exit):" pod_ip
 if [ $pod_ip == "r" ] || [ $pod_ip == "R" ]
 then
  run_command sudo kubectl get services
  continue
 elif [ $pod_ip == "q" ] || [ $pod_ip == "Q" ]
 then
  cont=$my_false
  continue
 else
  read -p "Please enter the port number (from 'PORT(S)') on which to find the website (if it has already been specifiyed, just press enter):" ip_port
  if [ ${#ip_port} -ne 0 ]
  then
   ip_port=":$ip_port"
  fi
  data="$(wget $pod_ip$ip_port -q -O -)"
  echo "$data"
  continue
 fi
done
echo "Script created by (c) Henry Letellier"
