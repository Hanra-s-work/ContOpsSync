#!/bin/bash
echo "Script written by (c) Henry Letellier"

hl_true=0
hl_false=1
success=0
error=1
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

yes_no "Do you wish to install the nginx controller in your kubernetes environement?"
RESPONSE=$?
if [ $RESPONSE -eq $hl_false ]; then
    echo "You have decided not to install the nginx controller"
    echo "Exiting program"
    exit $success
fi

echo "Installing the 'nginx-ingress' manager"
echo "Creating the namespace 'nginx-ingress'"
run_command "$SUDO kubectl create namespace nginx-ingress"
if [ $? -ne $success ]; then
    echo "Failed to create the namespace 'nginx-ingress'"
    echo "Exiting program"
    exit $error
fi
echo "Installing nginx-ingress via the helm package manager"
install_helm_if_not_present
if [ $? -ne $success ]; then
    echo "Failed to install the helm manager"
    echo "Exiting program"
    exit $error
fi
echo "Adding the nginx repository to the helm manager"
run_command "$SUDO helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx"
if [ $? -ne $success ]; then
    echo "Failed to add the nginx repository to the helm manager"
    echo "Exiting program"
    exit $error
fi
echo "Updating the helm repository list"
run_command "$SUDO helm repo update"
if [ $? -ne $success ]; then
    echo "Failed to update the helm repository list"
    echo "Exiting program"
    exit $error
fi
echo "Installing the nginx controller"
run_command "$SUDO helm install nginx-ingress-controller nginx-stable/nginx-ingress --namespace nginx-ingress"
if [ $? -ne $success ]; then
    echo "Failed to install the nginx-ingress-controller"
    echo "Exiting program"
    exit $error
fi
echo "Checking if nginx-ingress is existent"
run_command "$SUDO kubectl get pods -n nginx-ingress"
if [ $? -ne $success ]; then
    echo "Failed to find nginx-ingress"
    echo "Exiting program"
    exit $error
fi
echo "Checking if nginx-ingress is running"
run_command "$SUDO kubectl get pods -n nginx-ingress | grep Running"
if [ $? -ne $success ]; then
    echo "Failed to find nginx-ingress running"
    echo "Exiting program"
    exit $error
fi
echo "Checking if nginx-ingress is ready"
run_command "$SUDO kubectl get pods -n nginx-ingress | grep 1/1"
if [ $? -ne $success ]; then
    echo "Failed to find nginx-ingress ready"
    echo "Exiting program"
    exit $error
fi
echo "Checking if nginx-ingress is available"
run_command "$SUDO kubectl get pods -n nginx-ingress | grep 1/1 | grep Running | grep 1/1"
if [ $? -ne $success ]; then
    echo "Failed to find nginx-ingress available"
    echo "Exiting program"
    exit $error
fi
echo "The nginx-ingress is successfully installed"
echo "Script written by (c) Henry Letellier"
