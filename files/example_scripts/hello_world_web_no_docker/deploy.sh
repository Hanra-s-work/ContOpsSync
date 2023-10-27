#!/bin/bash

# alias kubectl="sudo kubectl"

port=8089
configmap_filename=hello-world-no-docker
configmap_filename_location="$configmap_filename.yaml"

function run_command {
    echo "Running: $@"
    $@
}

function normify_name {
    echo $1 | tr "_" "-" | sed "s/.\///g"
}

function write_to_file {
    local filename=$1
    local data=$2
    echo "$2"
    echo $data >>$filename
}

function dump_ingress_file {
    local port=$1
    local deployment_file_name=$2
    local configmap_filename=$3
    echo "writing to $configmap_filename"
    echo "" >$configmap_filename
    write_to_file $configmap_filename "---"
    write_to_file $configmap_filename "apiVersion: networking.k8s.io/v1"
    write_to_file $configmap_filename "kind: Ingress"
    write_to_file $configmap_filename "metadata:"
    write_to_file $configmap_filename "  name: $deployment_file_name"
    write_to_file $configmap_filename "  annotations:"
    write_to_file $configmap_filename "    spec.ingressClassName: "traefik""
    write_to_file $configmap_filename "spec:"
    write_to_file $configmap_filename "  rules:"
    write_to_file $configmap_filename "  - http:"
    write_to_file $configmap_filename "      paths:"
    write_to_file $configmap_filename "      - path: /"
    write_to_file $configmap_filename "        pathType: Prefix"
    write_to_file $configmap_filename "        backend:"
    write_to_file $configmap_filename "          service:"
    write_to_file $configmap_filename "            name: hello-world"
    write_to_file $configmap_filename "            port:"
    write_to_file $configmap_filename "              number: $port"
    write_to_file $configmap_filename ""
    write_to_file $configmap_filename "---"
    write_to_file $configmap_filename "apiVersion: v1"
    write_to_file $configmap_filename "kind: Service"
    write_to_file $configmap_filename "metadata:"
    write_to_file $configmap_filename "  name: hello-world"
    write_to_file $configmap_filename "spec:"
    write_to_file $configmap_filename "  ports:"
    write_to_file $configmap_filename "  - port: $port"
    write_to_file $configmap_filename "    protocol: TCP"
    write_to_file $configmap_filename "  selector:"
    write_to_file $configmap_filename "    app: hello-world"
    write_to_file $configmap_filename ""
    write_to_file $configmap_filename "---"
    write_to_file $configmap_filename "apiVersion: apps/v1"
    write_to_file $configmap_filename "kind: Deployment"
    write_to_file $configmap_filename "metadata:"
    write_to_file $configmap_filename "  name: hello-world-nginx"
    write_to_file $configmap_filename "spec:"
    write_to_file $configmap_filename "  selector:"
    write_to_file $configmap_filename "    matchLabels:"
    write_to_file $configmap_filename "      app: hello-world"
    write_to_file $configmap_filename "  replicas: 3"
    write_to_file $configmap_filename "  template:"
    write_to_file $configmap_filename "    metadata:"
    write_to_file $configmap_filename "      labels:"
    write_to_file $configmap_filename "        app: hello-world"
    write_to_file $configmap_filename "    spec:"
    write_to_file $configmap_filename "      containers:"
    write_to_file $configmap_filename "      - name: nginx"
    write_to_file $configmap_filename "        image: nginx"
    write_to_file $configmap_filename "        ports:"
    write_to_file $configmap_filename "        - containerPort: $port"
    write_to_file $configmap_filename "        volumeMounts:"
    write_to_file $configmap_filename "        - name: hello-world-volume"
    write_to_file $configmap_filename "          mountPath: /usr/share/nginx/html"
    write_to_file $configmap_filename "      volumes:"
    write_to_file $configmap_filename "      - name: hello-world-volume"
    write_to_file $configmap_filename "        configMap:"
    write_to_file $configmap_filename "          name: hello-world;47;118;0;32;1_"
    echo "File saved"

}

alias kubectl="sudo kubectl"
echo "Welcome to hello world web no docker"
# echo "Getting your web files for the ingress deployment"
# deployment_files=$(find . \( -iname "*.html" -o -iname '*.css' -o -iname '*.js' -type f \))
deployment_files=index.html
echo "Norming the names"
deployment_files=$(normify_name $deployment_files)
configmap_filename=$(normify_name $configmap_filename)
echo "Creating configmap"
run_command "sudo kubectl create configmap $configmap_filename --from-file $deployment_files"
echo "Getting configmap uptime"
run_command sudo kubectl get configmap $configmap_filename
echo "Saving configmap"
dump_ingress_file $port $deployment_file_name_location $configmap_filename
echo "Deploying configmap"
run_command "sudo kubectl apply -f $configmap_filename_location"
echo "Testing the deployment"
run_command curl localhost:$port
echo "Written by (c) Henry Letellier"
