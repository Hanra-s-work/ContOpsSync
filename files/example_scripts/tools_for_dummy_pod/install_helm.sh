#!/bin/bash
echo "Script written by (c) Henry Letellier"

hl_true=0
hl_false=1
success=0
error=1

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

function install_helm_if_not_present {
    echo "Checking if the helm manager is present"
    run_command "$SUDO helm version >/dev/null 2>&1"
    if [ $? -ne $success ]; then
        echo "Installing the helm manager"
        run_command "$SUDO curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3"
        if [ $? -ne $success ]; then return $?; fi
        run_command "$SUDO chmod 700 get_helm.sh"
        if [ $? -ne $success ]; then return $?; fi
        run_command "$SUDO ./get_helm.sh"
        if [ $? -ne $success ]; then return $?; fi
        run_command "$SUDO rm get_helm.sh"
        if [ $? -ne $success ]; then return $?; fi
        echo "Helm has successfully ben installed on your computer"
    fi
    return $success
}
function is_k3s_installed() {
    echo "Checking if k3s is installed"
    run_command "$SUDO k3s version >/dev/null 2>&1"
    if [ $? -ne $success ]; then return $hl_false; fi
    return $hl_true
}

is_k3s_installed
if [ $? -eq $hl_true ]; then
    echo "Adding path variable for the KUBECONFIG path"
    run_command export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
fi

echo "This script will help you install the helm deployer on your kubernetes infrastructure."
yes_no "Do you wish to install helm in your kubernetes environement?"
if [ $? -eq $hl_true ]; then
    install_helm_if_not_present
    STATUS=$?
    echo "Exiting program"
    exit $STATUS
else
    echo "You have decided not to install helm on your computer"
    echo "Exiting program"
    exit $success
fi
