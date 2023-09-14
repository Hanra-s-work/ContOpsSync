#!/bin/sh
TRUE=0
FALSE=1
MY_ENV="env"
FRESH_ENV=$FALSE
SYSTEM=$(uname --kernel-name)

if [ $SYSTEM == "Linux" ]; then
    MY_ENV='lenv'
elif [ $SYSTEM == "Darwin" ]; then
    MY_ENV='menv'
else
    echo "OS probably not supported"
    echo "This program has not been tested on your system"
    echo "Use this program at your own risk"
    MY_ENV="env"
fi

if [ ! -d $MY_ENV ]; then
    echo "Creating virtual environment"
    python3 -m venv $MY_ENV
    FRESH_ENV=$TRUE
fi

. ./$MY_ENV/bin/activate
if [ $FRESH_ENV -eq $TRUE ]; then
    echo "Updating pip"
    python3 -m pip install --upgrade pip
    echo "Updating dependencies"
    python3 ./install_ressources/install_libs.py
fi
echo "(c) Created by Henry Letellier"
echo "Running launching tool"
python3 ./src/main.py
echo "Deactivating virtual environment"
deactivate
