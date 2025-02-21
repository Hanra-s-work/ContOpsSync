#!/bin/env bash
TRUE=0
FALSE=1
ERROR=1
SUCCESS=0
MY_ENV="env"
FRESH_ENV=$FALSE
MAC_SYSTEM="$(uname)"
MY_SYSTEM="$(uname --kernel-name)"

MY_SYSTEM=$(echo "$MY_SYSTEM" | tr "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "abcdefghijklmnopqrstuvwxyz")
MAC_SYSTEM=$(echo "$MAC_SYSTEM" | tr "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "abcdefghijklmnopqrstuvwxyz")

E="$(python3 --version >/dev/null 2>&1)"
STATUS_PYTHON3=$?
E="$(python --version >/dev/null 2>&1)"
STATUS_PYTHON=$?
E="$(py --version >/dev/null 2>&1)"
STATUS_PY=$?
if [ $STATUS_PYTHON3 -ne 0 ] && [ $STATUS_PYTHON -ne 0 ] && [ $STATUS_PY -ne 0 ]; then
    echo "You do not have python installed, please install Python and relaunch this script"
    echo "Aborting program"
    exit $ERROR
fi

pip3 --version >/dev/null 2>&1
STATUS_PIP3=$?
pip --version >/dev/null 2>&1
STATUS_PIP=$?
python3 -m pip --version >/dev/null 2>&1
STATUS_PYTHON_PIP=$?
if [ $STATUS_PIP -ne 0 ] && [ $STATUS_PIP3 -ne 0 ] && [ $STATUS_PYTHON_PIP -ne 0 ]; then
    echo "You do not have pip installed, please install pip and relaunch this script"
    echo "Aborting program"
    exit $ERROR
fi

if [ "$MY_SYSTEM" == "linux" ] || [ "$MAC_SYSTEM" == "linux" ]; then
    MY_ENV='lenv'
elif [ "$MAC_SYSTEM" == "darwin" ]; then
    MY_ENV='menv'
else
    echo "OS probably not supported"
    echo "This program has not been tested on your system"
    echo "Use this program at your own risk"
    MY_ENV="env"
fi

if [ ! -d $MY_ENV ]; then
    echo "Giving execution rights to all the bash files contained in this program"
    chmod +x -R *.sh
    echo "Creating virtual environment"
    python3 -m venv $MY_ENV
    FRESH_ENV=$TRUE
fi

. ./$MY_ENV/bin/activate
if [ $FRESH_ENV -eq $TRUE ]; then
    echo "Updating pip"
    python3 -m pip install --upgrade pip
    echo "Updating dependencies"
    # python3 ./install_ressources/install_libs.py
    python3 -m pip install -r ./requirements.txt
fi
echo "(c) Created by Henry Letellier"
echo "Running launching tool"
python3 ./src/main.py $@
echo "Deactivating virtual environment"
deactivate
