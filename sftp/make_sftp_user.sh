#!/bin/bash

#Check that the script is executed on seqstore, otherwise quit
if [ "$(hostname)" != "seqstore.medair.lcl" ]; then
  echo "This script needs to be executed on seqstore. Quitting."
  exit 1
fi

