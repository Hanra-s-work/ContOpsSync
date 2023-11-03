#!/bin/bash

hl_true=0
hl_false=1
SUDO=sudo

function run_command {
    echo "Running command: $@"
    $@
}

function yes_no {
    while [ $hl_true -eq $hl_true ]; do
        read -p "$1 [(Y)es/(N)o]: " yn
        case $yn in
        [Yy]*) return $hl_true ;;
        [Nn]*) return $hl_false ;;
        *) echo "Please answer yes or no." ;;
        esac
    done
}

echo "This script will try to reset the kubernetes to it's default configuration (this might break your kubernetes configuration, a backup is recommended, use this program at your own risk): "
yes_no "Do you wish to reset your kubernetes cluster?"
RESPONSE=$?
if [ $RESPONSE -eq $hl_false ]; then
    echo "You have decided to leave your kubernetes unchanged"
    echo "Exiting program"
    exit $hl_success
fi
echo ""
echo "Program written by (c) Henry Letellier"
echo ""
echo "You have decided to try and reset your kubernetes configuration"
echo "This script will try to remove all the pods that have the Failed status"
run_command "$SUDO kubectl delete pods --selector=run=broken --field-selector=status.phase=Failed"
echo "Removing all created pods"
run_command "kubectl delete pods --all"
echo "Removing all services"
run_command "kubectl delete services --all"
echo "Removing all deployments"
run_command "kubectl delete deployments --all"
echo "Removing all statefulsets"
run_command "kubectl delete statefulsets --all"
echo "Removing all configmaps"
run_command "kubectl delete configmaps --all"
echo "Removing all secrets"
run_command "kubectl delete secrets --all"
echo "Removing all Persistent Volume Claim"
run_command "kubectl delete pvc --all"
echo "It is recommended to restart the service (rebooting your computer also works)"
yes_no "Do you wish to reboot your computer?"
RESPONSE=$?
if [ $RESPONSE -eq $hl_true ]; then
    echo "Rebooting your system."
    echo "End of program"
    reboot
fi
