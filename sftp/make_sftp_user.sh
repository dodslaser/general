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

