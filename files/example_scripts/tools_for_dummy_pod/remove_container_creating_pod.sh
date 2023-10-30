#!/bin/bash
function pause {
    read -p "Press enter to continue..."
}

echo "Running: sudo kubectl get pods -A -o wide | grep ContainerCreating"
echo "NAMESPACE                       NAME                                             READY   STATUS              RESTARTS        AGE     IP           NODE          NOMINATED NODE   READINESS GATES"
sudo kubectl get pods -A -o wide | grep ContainerCreating
echo "Please enter the name of the pod you wish to force delete:"
read POD_NAME
echo "Please enter the Namespace the pod belongs to:"
read NAMESPACE
echo "Running: sudo kubectl describe pod $POD_NAME -n $NAMESPACE"
sudo kubectl describe pod $POD_NAME -n $NAMESPACE
pause
echo "Running: sudo kubectl delete pod $POD_NAME"
sudo kubectl delete pod $POD_NAME
echo "Done"
echo "Running: sudo kubectl get pods -A -o wide | grep ContainerCreating"
echo "NAMESPACE                       NAME                                             READY   STATUS              RESTARTS        AGE     IP           NODE          NOMINATED NODE   READINESS GATES"
sudo kubectl get pods -A -o wide | grep ContainerCreating
