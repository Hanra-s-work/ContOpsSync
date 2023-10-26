#!/bin/bash

configmap_filename=hello_world_no_docker.yaml

function run_command {
    echo "Running: $@"
    $@
}

alias kubectl="sudo kubectl"
echo "Welcome to hello world web no docker"
echo "Creating and saving configmap"
run_command "kubectl create configmap hello-world --from-file index.html > $configmap_filename"
echo "Deploying configmap"
run_command "kubectl apply -f $configmap_filename"
echo "Testing the deployment"
run_command curl localhost:80
echo "Written by (c) Henry Letellier"
