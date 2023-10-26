#!/bin/bash
echo "Running: sudo kubectl get pods"
sudo kubectl get pods
echo "Please enter the name of the pod you wish to force delete:"
read POD_NAME
echo "Running: sudo kubectl delete pod $POD_NAME --grace-period=0 --force"
sudo kubectl delete pod $POD_NAME --grace-period=0 --force
echo "Done"
echo "Running: sudo kubectl get pods"
sudo kubectl get pods
