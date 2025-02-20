#!/bin/bash

# Set color (not directly possible in Bash like in Batch)
echo -e "\e[32m" # Green text

# Icon credits
echo "Designed by easy installation icons from Flaticon"
echo "https://www.flaticon.com/free-icon/easy-installation_4961662"

# Setup info
export PATH="$PATH:$HOME/.local/bin"
SRC_DATA="assets"
COMPDIR="compDir"
ENV_NAME="uenv"

# Required environment
SRC_ENV="../requirements.txt"
DEST_ENV="requirements.txt"
echo "Copying the environment"
cp "$SRC_ENV" "$DEST_ENV"

echo "Creating the environment"
python3 -m venv $ENV_NAME

echo "Installing dependencies"
. ./$ENV_NAME/bin/activate
pip install -r "$DEST_ENV"

# Required dependency
echo "Installing pyinstaller"
pip install pyinstaller

# Copying the data
echo "Copying the data"
rm -rf "$COMPDIR"
mkdir -p "$COMPDIR"
cp -r "$SRC_DATA"/ "$COMPDIR/"

ICON="icon/easy-installation_favicon.ico"
SRC_PATH="src"
SRC_FILES="$SRC_PATH/main.py"
DEST_PATH="$COMPDIR/$SRC_PATH"
BIN_NAME="setup"
BUILD="$SRC_DATA/build"

mkdir -p "$DEST_PATH"
cp -r "../$SRC_PATH"/* "$DEST_PATH/"

cd "$COMPDIR" || exit

echo "Compiling"
pyinstaller --onefile --icon="$ICON" --name="$BIN_NAME" --paths="$SRC_PATH" --workpath="$BUILD" "$SRC_FILES"

echo "Moving"
cp -rf dist/* ..

cd ..

echo "Cleaning"
rm -f "$COMPDIR/$SRC_FILES"

deactivate
