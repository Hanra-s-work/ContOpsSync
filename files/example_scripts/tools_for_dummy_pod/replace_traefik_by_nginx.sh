#!/bin/bash

hl_success=0
SUDO=sudo
service_file_path="/etc/systemd/system"
traefik_yaml_location="/var/lib/rancher/k3s/server/manifests"
traefik_config="traefik.yaml"

function run_command {
    echo "Running command: $@"
    $@
}

function disable_traefik_if_present {
    config_file=$1
    echo "creating a backup of the service file"
    run_command "$SUDO cp $config_file $config_file.bak"
    if grep -q "traefik" "$config_file"; then
        sed -i 's/traefik/--disable traefik/' "$config_file"
    else
        sed -i 's/server.*/server  --disable traefik\\/' "$config_file"
    fi
}

echo "Removing traefik"
run_command $SUDO kubectl delete -f traefik.yaml
STATUS=$?
if [ $STATUS -ne $hl_success ]; then
    echo "Failed to remove traefik"
    echo "Attempting to remove traefik via helm charts"
    run_command $SUDO kubectl -n kube-system delete helmcharts.helm.cattle.io traefik
    if [ $? -ne $hl_success ]; then
        echo "Failed to remove traefik via helm charts"
        echo "Attempting to force remove traefik"
        echo "Moving $traefik_yaml_location/$traefik_config to $traefik_yaml_location/../$traefik_config"
        run_command $SUDO mv $traefik_yaml_location/$traefik_config ../
        echo "Attempting to remove traefik gracefully"
        run_command kubectl -n kube-system delete helmcharts.helm.cattle.io traefik --force
        if [ $? -ne $hl_success ]; then
            echo "Attempting to remove traefik without a grace period"
            run_command kubectl -n kube-system delete helmcharts.helm.cattle.io traefik --grace-period=0 --force
        fi
    fi
fi
if [ $? -ne $hl_success ]; then
    echo "Failed to remove traefik the conventional way, please refer to: 'http://web.archive.org/web/20230323022936/https://thehotelhero.com/k3s-uninstall-traefik-and-install-it-again' to try an remove traefik the unconventional way"
    echo "This is because the website does not always respond, at least is did not for me"
    exit 1
fi
echo "Stopping service"
read -p "Please enter the name of the service you are using to run kubernetes: " kube_service
run_command $SUDO systemctl stop $kube_service
if [ $? -ne $hl_success ]; then
    echo "Failed to stop kubernetes service"
    echo "Attempting to stop kubernetes service via service"
    run_command $SUDO service $kube_service
    if [ $? -ne $hl_success ]; then
        echo "Failed to stop Kubernetes"
        echo "Please follow tutorial at : http://web.archive.org/web/20230323022936/https://thehotelhero.com/k3s-uninstall-traefik-and-install-it-again"
        echo "Chapter: 'Now we have tried the conventional way to get rid of Traefik'"
        exit 1
    fi
fi
echo "Disabeling traefik if present"
disable_traefik_if_present $service_file_path/$kube_service
echo reloading the daemon
run_command $SUDO systemctl daemon-reload
echo "Starting $kube_service"
run_command $SUDO systemctl start $kube_service

echo "Installing nginx"
echo "Installing the regular way"
run_command $SUDO kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-0.32.0/deploy/static/provider/cloud/deploy.yaml
if [ $? -ne $hl_success ]; then
    echo "Failed to install nginx the regular way"
    echo "Attempting to install nginx via helm charts"
    run_command $SUDO kubectl create namespace ingress-nginx
    run_command $SUDO helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
    run_command $SUDO helm repo update
    run_command $SUDO helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx
    if [ $? -ne $hl_success ]; then
        echo "Failed to install nginx via helm charts"
        echo "Attempting to install nginx via k3s helm charts"
        run_command $SUDO kubectl create namespace ingress-nginx
        run_command $SUDO helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
        run_command $SUDO helm repo update
        run_command $SUDO helm install ingress-nginx ingress-nginx/ingress-nginx --namespace ingress-nginx --kubeconfig /etc/rancher/k3s/k3s.yaml
    fi
fi

echo "Verifying if it works"
run_command curl localhost
if [ $? -ne $hl_success ]; then
    echo "Attempting to check via pods"
    run_command kubectl get pods -n ingress-nginx
    if [ $? -ne $hl_success ]; then
        echo "Failed to verify if nginx works"
        echo "Attempting to verify if nginx works via helm charts"
        run_command $SUDO kubectl get pods -n ingress-nginx --kubeconfig /etc/rancher/k3s/k3s.yaml
        if [ $? -ne $hl_success ]; then
            echo "Failed to verify if nginx works via helm charts"
            echo "Attempting to verify if nginx works via k3s helm charts"
            run_command $SUDO kubectl get pods -n ingress-nginx --kubeconfig /etc/rancher/k3s/k3s.yaml
        fi
    fi
fi
