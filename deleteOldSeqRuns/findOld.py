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
import datetime
import csv
from collections import defaultdict
import json
import re

# Get arguments from the commandline
@click.command()
@click.option('-a', '--age', type=int, required=True,
              help='Age of dirs, in days, to be deleted')
@click.option('-d', '--directory', required=True,
              help='Path to directories')
@click.option('-s', '--sheetname', default="SampleSheet.csv",
              help='Name of file with ownership info of samples. default: "SampleSheet.csv')
@click.option('-i', '--investigatorlist', required=True,
              help='Path to json file with investigator e-mails')
def main (age, directory, investigatorlist, sheetname):
    # First get a list of what e-mail belongs to what person
    with open(investigatorlist) as f:
        data = json.load(f)

    #Get a list of all seq runs in directory
    #sheetname = 'SampleSheet.csv'  #For testing purposes only, remove this
    runs = []

    for path in os.listdir(directory):  #This is a kinda ugly way to get all the dirs
        #bug(path)
        full_path = os.path.join(directory, path)
        if os.path.isdir(full_path) and re.match("^[0-9]{6}_", path):  #Is dir and starts with 6 digits
            #bug(full_path)
            runs.append(path)
            #runs.append(full_path)

    #Go over each sequencing run one by one
    #owner_dict = {}

    for run in runs:
        #Full path of the run
        run_path = os.path.join(directory, run)
        #bug(run)
        # What is the age of the run
        owner_dict = runAge(age, run)
        #bug(owner_dict.keys())

        #What samples are in each run
        bug(run_path)
        run_samples = runSamples(run_path)
        bug(run_samples)

        to_remove = getOld(age, run_path)  #Paths to all samples
        to_remove_samples = list(map(lambda str: str.split('/')[-1], to_remove))  #List of the samples themselves
        #bug(to_remove_samples)
        #E-mail the people who have old samples
        # First make sure the SampleSheet.csv file exists
        if not os.path.exists(os.path.join(run_path, sheetname)):
            print("** ERROR: No " + sheetname + " @ " + run)
        else:
            # See who owes each sample in the run
            to_email = dirOwners(os.path.join(run_path, sheetname), to_remove_samples)
            #bug(to_email)

    # Send an email to the owners

    #bug(data['investigators']['CO']['email'])
    #autoMail(run, to_remove_samples, address)

def runAge (age, run):
    today = datetime.datetime.now()
    run_dict = {}

    run_date = datetime.datetime.strptime(run.split('_')[0], '%y%m%d')
    run_age = (today - run_date).days

    if run_age > age:
        run_dict[run] = {}
        run_dict[run]['age'] = run_age

        #bug(run_dict)

    return run_dict

def runSamples (run):
    samples = []
    for name in os.listdir(run):
        #bug(name)
        if os.path.isdir(os.path.join(run, name)):
            #bug(name)
            samples.append(name)

    return samples



def getOld (age, run):  #Check which folders are older than age, return name and age
    today = datetime.date.today()
    #old_dirs = [] #Initial, list based way
    old_dirs = {}
    for name in os.listdir(run):
        #bug(name)
        full_name = os.path.join(run, name)
        if os.path.isdir(full_name):
            filedate = datetime.date.fromtimestamp(os.path.getmtime(full_name))
            #bug("hej:")
            #bug(filedate)

            age_today = (today - filedate).days
            if age_today > age:
                old_dirs[name] = {'path': full_name, 'age': age_today}
                #old_dirs.append(full_name) #Used for using lists
    #bug(old_dirs)
    return old_dirs

def dirOwners (run, samples):  #Who owns what sample
    #bug(samples)
    with open(run, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        pairs = []
        # Read in each line and save info about sample and owner
        for row in csv_reader:
            if row and row[0] in samples:  #skip empty rows and rows without sample info
                extract = [row[10].split('_')[0], row[0]]
                pairs.append(extract)

   # Load values into a dictionary
    owner_dict = defaultdict(list)
    for key, value in pairs:
        owner_dict[key].append(value)

    return owner_dict

def bug (str): #Mark more clearly what is a debug message
    print("** Debug:", end=' ')
    print(str)

if __name__ == '__main__':
    main()