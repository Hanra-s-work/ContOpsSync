#!/bin/bash

# alias kubectl="sudo kubectl"

configmap_filename=hello_world_no_docker.yaml
configmap_locations="/var/lib/rancher/k3s/server/tls/etcd/"
configmap_filename_location=""

function run_command {
    echo "Running: $@"
    $@
}

alias kubectl="sudo kubectl"
echo "Welcome to hello world web no docker"
echo "Getting your web files for the ingress deployment"
deployment_files=$(find . \( -iname "*.html" -o -iname '*.css' -o -iname '*.js'-type f \))
echo "Creating configmap"
run_command "sudo kubectl create configmap $configmap_filename --from-file $deployment_files"
echo "Getting configmap uptime"
run_command sudo kubectl get configmap $configmap_filename
echo "Deploying configmap"
run_command "sudo kubectl apply -f $configmap_filename"
echo "Testing the deployment"
run_command curl localhost:80
echo "Written by (c) Henry Letellier"
