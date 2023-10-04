#!/bin/bash
echo "Updating system"
sudo apt update
echo "Upgrading system"
sudo apt full-upgrade
echo "Installing vsftpd"
sudo apt install vsftpd -y
echo "Enabeling vsftpd"
sudo systemctl start vsftpd
sudo systemctl enable vsftpd
sudo systemctl status vsftpd
# echo "enabeling ftp ports"
# sudo ufw allow 20/tcp
# sudo ufw allow 21/tcp
echo "Configuring vftpd"
CONFIG_FILE=/etc/vsftpd.conf
echo "Enabeling write to the config file"
sudo chmod 777 $CONFIG_FILE
echo "Owning the file"
sudo chown $USER:$USER $CONFIG_FILE
echo "Enabeling write"
sed -i '/^write_enable=/ s/#*\(.*\)/\1/' $CONFIG_FILE
echo "Exposing ftp on port 22"
sed -i '/^local_umask=/ s/#*\(.*\)/\1/' $CONFIG_FILE
echo "Setting the local user as the ftp root owner"
sed -i '/^chroot_local_user=/ s/#*\(.*\)/\1/' $CONFIG_FILE
echo "Disabeling anonymous login"
sed -i 's/^anonymous_enable=YES/anonymous_enable=NO/' $CONFIG_FILE
echo "Creating user token"
sudo echo "user_sub_token=\$USER" >>$CONFIG_FILE
echo "Setting the users home/FTP as the root's home"
sudo echo "local_root=/home/\$USER/FTP" >>$CONFIG_FILE
echo "Setting the file rights back to before"
sudo chmod 644 $CONFIG_FILE
echo "Setting the root as the owner of the file"
sudo chown root:root $CONFIG_FILE
echo "Creating FTP/my_files folder"
mkdir -p $HOME/FTP/my_files
echo "Setting the user as the owner of the FTP folder"
chown a-w $HOME/FTP
echo "Restating vsftpd service"
sudo service vsftpd restart
sudo systemctl status vsftpd
echo "Script created by (c) Henry Letellier"
