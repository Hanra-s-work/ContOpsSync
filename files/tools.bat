echo off
color 0A

set ERR=84
set SUCCESS=0
set PYTHON_VERSION=""

echo "(c) Created by Henry Letellier"

py --version > NUL 2> NUL
IF %ERRORLEVEL% EQU 0 (
    set PYTHON_VERSION=py
) ELSE (
    python --version > NUL 2>NUL
    IF %ERRORLEVEL% EQU 0 (
        set PYTHON_VERSION=python
    ) ELSE (
        python3 --version > NUL 2>NUL
        IF %ERRORLEVEL% EQU 0 (
            set PYTHON_VERSION=python3
        ) ELSE (
            echo "No python program found, please install python"
            exit %ERR%
        )
    )
)

IF NOT EXIST "wenv" (
    %PYTHON_VERSION% install_ressources\install_libs.py
)

IF %ERRORLEVEL% EQU 84 (
    echo "Failed to install the dependencies, please make sure you are running this program in the same location as it's file."
    exit %ERR%
)

IF NOT EXIST "wenv" (
    echo "Failed to run the script, please make sure you are running this program in the same location as it's file."
    exit %ERR%
)

echo "Starting program"
wenv\Scripts\activate &^
echo Starting program &^
src\main.py &^
deactivate

