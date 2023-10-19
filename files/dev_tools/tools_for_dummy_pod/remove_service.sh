#!/bin/bash

function run_command() {
 echo "Running: $@"
 $@
}

echo "following tutorial: https://kubernetes.io/docs/tutorials/hello-minikube/#clean-up"
echo "Cleaning up the service"
echo "Listing current services"
run_command sudo kubectl get services
read -p "Enter the name of the service you wish to remove:" services_to_remove
echo "Removing service"
run_command sudo kubectl delete service $services_to_remove
echo "Script created by (c) Henry Letellier"


