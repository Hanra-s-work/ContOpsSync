#!/bin/bash

function run_command() {
 echo "Running: $@"
 $@
}

echo "Reference link: https://kubernetes.io/docs/tutorials/hello-minikube/"
echo ""
echo "1 creating a Deployment to manage a Pod"
echo "# Run a test container image that includes a webserver"
run_command sudo kubectl create deployment hello-node --image=registry.k8s.io/e2e-test-images/agnhost:2.39 -- /agnhost netexec --http-port=8080
echo "2 Viewing deployment"
run_command sudo kubectl get deployments
echo "3 Viewing the pods"
run_command sudo kubectl get pods
user_pods="$(kubectl get pods)"
echo "4 Viewing cluster events"
run_command sudo kubectl get events
echo "5 Viewing kubectl's configuration"
run_command sudo kubectl config view
echo "6 Viewing application logs"
echo "$user_pods"
read -p "Please enter the name of the pod you wish to view the logs for:" pod_name
run_command sudo kubectl logs "$pod_name"
echo "Script written by (c) Henry Letellier"
