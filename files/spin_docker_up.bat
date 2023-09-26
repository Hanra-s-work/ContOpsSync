echo off
color 0A
echo "stopping docker"
set DCONTAINER=fed
set DIMAGE=fedora:34
set BASH_PATH="/bin/bash"
docker stop %DCONTAINER%
docker rm %DCONTAINER%
docker run -it -v "C:\Users\Henry_PC\Documents\015_project_ov\shared\tools":"/mnt/" -d --name %DCONTAINER% %DIMAGE%
docker exec -it %DCONTAINER% %BASH_PATH% 