#!/usr/bin/env python

"""
A script that looks in a specified location and
finds directories older than a specified number
of days, and removes the directory.
Will also first send out an email to the owner to warn
"""

#Import libraries
import os
import click
from datetime import date

# Get arguments from the commandline
@click.command()
@click.option('-a', '--age', type=int, required=True, help='Age of dirs, in days, to be deleted')
@click.option('-d', '--directory', required=True, help='Path to directories')
def main (age, directory):
    to_remove = getOld(age, directory) #Get list of folders to delete
    print(to_remove)

def getOld (age, directory): #Check which folders are older than age
    today = date.today()
    old_dirs = []
    for name in os.listdir(directory):
        dirPath = directory + name
        filedate = date.fromtimestamp(os.path.getmtime(dirPath))
        if (today - filedate).days > age:
            old_dirs.append(dirPath)
    return old_dirs

if __name__ == '__main__':
    main()