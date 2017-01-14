#!/bin/bash
# XVWA Automatic Setup by Sanoop Thomas a.k.a @s4n7h0
# Project Repo : https://github.com/s4n7h0/xvwa
# License : GPLv2
# License URL : http://www.gnu.org/licenses/gpl-2.0.html


cat << "EOF"
__  __       __    __  _     __      _
\ \/ /\   /\/ / /\ \ \/_\   / _\ ___| |_ _   _ _ __
 \  /\ \ / /\ \/  \/ //_\\  \ \ / _ \ __| | | | '_ \
 /  \ \ V /  \  /\  /  _  \ _\ \  __/ |_| |_| | |_) |
/_/\_\ \_/    \/  \/\_/ \_/ \__/\___|\__|\__,_| .__/
                                              |_|
 >> Project Repo : https://github.com/s4n7h0/xvwa
 >> Scripted by : Sanoop Thomas aka @s4n7h0

EOF

function clone(){
	echo "Cloning latest version of XVWA from GitHub"
        git clone https://github.com/s4n7h0/xvwa.git $webroot/xvwa
        echo "Setting XVWA configuration"
	sudo chmod -R 777 $webroot/xvwa
        sed -i '2 c $XVWA_WEBROOT = "";' $webroot/xvwa/config.php
        sed -i '5 c $user = "'$uname'";' $webroot/xvwa/config.php
        sed -i '6 c $pass = "'$pass'";' $webroot/xvwa/config.php

        #creating database
        echo "Creating xvwa database"
        mysql -u $uname -p$pass -e "CREATE DATABASE IF NOT EXISTS xvwa"
        echo "XVWA Setup Finished Successfully. Happy hacking and happy learning !"
}


#checking mysql is installed
isMYSQL=$(apt-cache show mysql-server | grep 'Version');
if [[ $isMYSQL == *"No packages found"* ]]; then
	echo -n "MySQL Package Not Found. Do you want to install (Y/N)?"
	read mysql_flag
	if [ $mysql_flag == "Y" ] || [ $mysql_flag == "y" ]; then
		echo "Installing MySQL Server. This might take a while."
		sudo apt-get install mysql-server
	else
		echo "XVWA Setup Terminated. MySQL is a must requirement for XVWA to run"
		exit 0
	fi
else
	echo "MySQL found with "$isMYSQL
fi
#checking apache is installed
isApache=$(apt-cache show apache2 | grep 'Version');
if [[ $isApache == *"No packages found"* ]]; then
        echo -n "Apache Package Not Found. Do you want to install (Y/N)?"
	read apache_flag
	if [ $apache_flag == "Y" ] || [ $apache_flag == "y" ]; then
		echo "Installing Apache. This might take a while."
		sudo apt-get install apache2
	else
		echo "XVWA Setup Terminated. Apache is a must requirement for XVWA to run"
		exit 0
	fi
else
        echo "Apache found with "$isApache
fi

#asserting mysql and apache services
MYSQL=$(pgrep mysql | wc -l);
if [ "$MYSQL" -eq 0 ]; then
        echo "MySQL is down. Starting MySQL Service";
        sudo service mysql start
fi
APACHE=$(pgrep apache | wc -l);
if [ "$APACHE" -eq 0 ]; then
        echo "Apache is down. Starting Apache Service";
        sudo service apache2 start
fi

#configuring mysql and apache for xvwa
echo -n "Enter mysql username : "
read uname
echo -n "Enter mysql password : "
read pass
echo -n "Enter the full web root path : "
read webroot

#cloning latest version of XVWA from  GitHub
if [[ -d $webroot/xvwa ]]; then
	echo -n "Folder "$webroot"/xvwa already exists. Do you want to clean and build a fresh latest copy ? (Y/N)"
	read clean_flag
	if [ $clean_flag == "Y" ] || [ $clean_flag == "y"]; then
		echo "Cleaning up old copy"
		rm -rf $webroot/xvwa
		clone
	else
		echo "XVWA Setup Terminated."
	fi
else
	clone
fi
