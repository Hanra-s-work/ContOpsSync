#!/bin/env bash
my_true=0
my_false=1
my_env="lenv"
fresh_env=$my_false

function welcome_message() {
    echo "+=================================================+"
    echo "|                                                 |"
    echo "|          Welcome to Raspberry Tools             |"
    echo "|      The tool to help you set up clusters       |"
    echo "|                                                 |"
    echo "| This Script is a guide to help you easley set   |"
    echo "| up Kubernetes/Docker/Docker-Compose             |"
    echo "|                                                 |"
    echo "| This tool can also help you set up common tools |"
    echo "| like, Desktop Rancher, terraform.               |"
    echo "|                                                 |"
    echo "| This program was created by (c) Henry Letellier |"
    echo "|                                                 |"
    echo "| This program is provided as if and without any  |"
    echo "| warranty, use at your own risk.                 |"
    echo "|                                                 |"
    echo "| This program can be found on github under the   |"
    echo "| name: 'Hanra-s-work/ContOpsSync'.               |"
    echo "|                                                 |"
    echo "| The libraries used by this program have their   |"
    echo "| own license, you can check them on the renowned |"
    echo "| python package site: pypi.org.                  |"
    echo "| The names of the libaries used by this program  |"
    echo "| can be found in the file: 'requirements.txt'    |"
    echo "|                                                 |"
    echo "| This program is meant to be run on the target   |"
    echo "| machine, this it does not have any remote       |"
    echo "| comunication capabilities (appart from using    |"
    echo "| an internet connection).                        |"
    echo "|                                                 |"
    echo "| We hope our program simplifies your tasks and   |"
    echo "| brings you joy.                                 |"
    echo "+=================================================+"
}

function update_system() {
    echo "Updating system"
    sudo apt-get update
    sudo apt-get upgrade --with-new-pkgs -y
}

function install_python_pip() {
    sudo apt-get install python3-pip
    sudo apt install \
        libffi-dev \
        libbz2-dev \
        liblzma-dev \
        libsqlite3-dev \
        libncurses5-dev \
        libgdbm-dev \
        zlib1g-dev \
        libreadline-dev \
        libssl-dev \
        tk-dev \
        build-essential \
        libncursesw5-dev \
        libc6-dev \
        openssl \
        git
}

function has_python_pip() {
    python3 -m pip --version >/dev/null 2>&1
    status_python_pip=$?
    if [ $status_python_pip -ne 0 ]; then

    fi
}

function create_environement() {
    if [ ! -d $my_env ]; then
        echo "Creating virtual environment"
        python3 -m venv $my_env
        fresh_env=$my_true
    fi
}

function set_up_environement() {
    . ./$my_env/bin/activate
    if [ $fresh_env -eq $my_true ]; then
        echo "Updating pip"
        python3 -m pip install --upgrade pip
        echo "Updating dependencies"
        python3 -m pip install -r ./requirements.txt
    fi
}

function start_program() {
    chmod +x src/main.py
    echo "Starting program"
    python3 ./src/main.py $@
    return $?
}

function end_of_script() {
    echo "End of script"
    echo "Created by (c) Henry Letellier"
    exit $1
}

function main() {
    welcome_message
    update_system
    has_python_pip
    create_environement
    set_up_environement
    start_program "$@"
    end_of_script $?
}

main "$@"
