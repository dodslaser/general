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
import csv

# Get arguments from the commandline
@click.command()
@click.option('-a', '--age', type=int, required=True, help='Age of dirs, in days, to be deleted')
@click.option('-d', '--directory', required=True, help='Path to directories')
#@click.option('-o','--owners', required=True, help='csv file of who owns what directory')
def main (age, directory):
    #Get a list of all seq runs in directory
    runs = []
    for path in os.listdir(directory):  #This is a kinda ugly way to get all the dirs
        #bug(path)
        full_path = os.path.join(directory, path)
        if os.path.isdir(full_path):
            #bug(full_path)
            runs.append(full_path)

    #Go over each sequencing run one by one
    for run in runs:
        bug(run)
        # Get a list of samples to be removed
        to_remove = getOld(age, run)
        # See who owes each samples that should be removed


    #Get the ownership information for all samples to be removed
    #to_email = dirOwners(owners)
    #bug(to_email)

def getOld (age, run):  #Check which folders are older than age
    today = date.today()
    old_dirs = []
    for name in os.listdir(run):
        full_name = os.path.join(run,name)
        if os.path.isdir(full_name):
            filedate = date.fromtimestamp(os.path.getmtime(full_name))
            if (today - filedate).days > age:
                old_dirs.append(full_name)
    return old_dirs
#
# def dirOwners (owners): #Who owns what folder
#     with open(owners, mode='r') as csv_file:
#         csv_reader = csv.reader(csv_file)
#         for row in csv_reader:
#             owner_dict = {row[0]:[row[1],row[2]]}
#             bug(owner_dict)
#
#     return owners



def bug (str): #Mark more clearly what is a debug message
    print("** Debug:", end=' ')
    print(str)

if __name__ == '__main__':
    main()