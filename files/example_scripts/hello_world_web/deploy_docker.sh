#!/bin/bash

# Build docker image
docker pull hanralatalliard/hello-world-nginx:latest

# Set the namespace where you want to deploy the pod
NAMESPACE="hello-world-deployment-docker"

# Path to your Deployment YAML file
DEPLOYMENT_YAML="./hello-world-deployment-docker.yaml"

# Create the namespace if it doesn't exist
kubectl get namespace "$NAMESPACE" &>/dev/null || kubectl create namespace "$NAMESPACE"

# Create the deployment in the specified namespace
kubectl apply -f "$DEPLOYMENT_YAML" -n "$NAMESPACE"

# Check the status of the deployment
kubectl rollout status deployment/hello-world-deployment-docker -n "$NAMESPACE"
