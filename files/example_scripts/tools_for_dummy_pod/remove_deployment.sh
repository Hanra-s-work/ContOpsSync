#!/bin/bash

function run_command() {
 echo "Running: $@"
 $@
}

echo "following tutorial: https://kubernetes.io/docs/tutorials/hello-minikube/#clean-up"
echo "Cleaning up the deployment"
echo "Listing current deployment"
run_command sudo kubectl get deployments
read -p "Enter the name of the deployment you wish to remove:" services_to_remove
echo "Removing deployment"
run_command sudo kubectl delete deployment $services_to_remove
echo "Script created by (c) Henry Letellier"


