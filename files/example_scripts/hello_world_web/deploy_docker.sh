#!/bin/bash

# Set the namespace where you want to deploy the pod
NAMESPACE="hello-world-docker"

# Path to your Deployment YAML file
DEPLOYMENT_YAML="./hello-world-docker.yaml"

# Create the deployment in the specified namespace
kubectl apply -f "$DEPLOYMENT_YAML" -n "$NAMESPACE"

# Check the status of the deployment
kubectl rollout status deployment/hello-world-deployment -n "$NAMESPACE"
