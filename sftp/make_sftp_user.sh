#!/bin/bash

#Usage information
if [ "$#" -lt 2 ]; then
    echo "Usage: $(basename $0) <USERID> <ROOT FOLDER>"
    exit 1
fi

#Check that the script is executed on seqstore and as root, otherwise quit
if [ "$(hostname)" != "seqstore.medair.lcl" ]; then
  echo "This script needs to be executed on seqstore. Quitting."
  exit 1
fi
if [ "$(whoami)" != "root" ]; then
  echo "You need to execute this as root. Quitting"
  exit 1
fi

#Get some ARG vars
USERID=$1
ROOTFOLDER=$2

#Add new user
useradd \
  -d /home/chroot/$USERID \
  -s /sbin/nologin \
  -G sftponly $USERID \
  && mkdir -p /home/chroot/${USERID}/shared

#Make new project directory
mkdir -p ${ROOTFOLDER}/${USERID}/shared

#Mount bind the project folder to users home
mount --bind \
  ${ROOTFOLDER}/${USERID}/shared \
  /home/chroot/${USERID}/shared

#Make sure owner and permissions of chroot home is correct
chown root:root /home/chroot/${USERID}
chmod 755 /home/chroot/${USERID}

# Set unix as group owner and make sur permissions for shared folder is 775
chown root:unix ${ROOTFOLDER/${USERID}/shared
chmod 775 ${ROOTFOLDER/${USERID}/shared
chown root:unix /home/chroot/${USERID}/shared
chmod 775 /home/chroot/${USERID}/shared

#Generate a random password
PASS_KEY=$(openssl rand -base64 9)

#Set the password for new user
echo $PASS_KEY | passwd $USERID --stdin > /dev/null #Thrash STDOUT to make output clean

#Echo the username and key so it can be copied
echo -e "${USERID}\t${PASS_KEY}"
