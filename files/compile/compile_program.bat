echo off
color 0A
cls
@REM Icon credits
echo "Designed by easy installation icons from Flaticon"
echo "https://www.flaticon.com/free-icon/easy-installation_4961662"
@REM Setup info
set PATH=%PATH%;%USERPROFILE%\AppData\Roaming\Python\Python311\Scripts
set SRC_DATA=assets
set COMPDIR=compDir

@REM Required environement
set SRC_ENV=..\requirements.txt
set DEST_ENV=requirements.txt
echo Copying the environement
copy %SRC_ENV% %DEST_ENV%
echo Creating the environement
py -m venv wenv
echo Installing dependencies
call wenv\Scripts\activate.bat
pip install -r %DEST_ENV%


@REM Required dependency
echo Installing pyinstaller
pip install pyinstaller

@REM Copying the data
echo Copying the data
rmdir /s /q %COMPDIR%
mkdir %COMPDIR%
xcopy /s/e %SRC_DATA% %COMPDIR%

set ICON=icon\easy-installation_favicon.ico
set SRC_PATH=src
set SRC_FILES=%SRC_PATH%\main.py
set DEST_PATH=%COMPDIR%\%SRC_PATH%
set BIN_NAME=setup
set BUILD=%SRC_DATA%\build

mkdir %DEST_PATH%
xcopy /s/e ..\%SRC_PATH% %DEST_PATH%
cd %COMPDIR%
echo Compiling
pyinstaller --onefile --icon %ICON% --name %BIN_NAME% --paths %SRC_PATH% --workpath %BUILD% %SRC_FILES%
echo Moving
move dist\* ..
cd ..
echo Cleaning
del %cd%\%COMPDIR%\%SRC_FILES%
deactivate
