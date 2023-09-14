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

@REM Required dependency
@REM pip install pyinstaller

@REM Copying the data
echo Copying the data
rmdir /s /q %COMPDIR%
mkdir %COMPDIR%
xcopy /s/e %SRC_DATA% %COMPDIR%

@REM Program info
set ICON=icon\easy-installation_favicon.ico
set SRC_PATH=src
set SRC_FILES=%SRC_PATH%\setup.py
set BIN_NAME=setup
set BUILD=%SRC_DATA%\build

copy setup.py %cd%\%COMPDIR%\%SRC_FILES%
cd %COMPDIR%
echo Compiling
pyinstaller --onefile --icon %ICON% --name %BIN_NAME% --paths %SRC_PATH% --workpath %BUILD% %SRC_FILES%
echo Moving
move dist\* ..
cd ..
echo Cleaning
del %cd%\%COMPDIR%\%SRC_FILES%
