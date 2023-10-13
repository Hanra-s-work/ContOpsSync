echo off
color 0A

set ERR=84
set SUCCESS=0
set PYTHON_VERSION=""
set ENV_NAME=wenv

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
    @REM %PYTHON_VERSION% install_ressources\install_libs.py
    echo "Creating environement"
    %PYTHON_VERSION% -m venv %ENV_NAME%
    echo "Activating environement"
    cmd /c "wenv\Scripts\activate & echo Updating the pip module & python -m pip install --upgrade pip & deactivate"
)

IF %ERRORLEVEL% EQU 84 (
    echo "Failed to install the dependencies, please make sure you are running this program in the same location as it's file."
    exit %ERR%
)

IF NOT EXIST "wenv" (
    echo "Failed to run the script, please make sure you are running this program in the same location as it's file."
    exit %ERR%
)

wenv\Scripts\activate &^
echo Installing the dependencies &^
pip3 install -r requirements.txt &^
echo Starting program &^
src\main.py &^
deactivate

