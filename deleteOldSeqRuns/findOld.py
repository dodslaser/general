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
from itertools import dropwhile

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
def main(age, directory, investigatorlist, sheetname):
    # First get a list of what e-mail belongs to what person
    with open(investigatorlist) as f:
        mail_json = json.load(f)
        #bug(data)

    #Create a dict containing info on all runs
    data_owners = buildList(directory, sheetname)

    # Compile a list of everything that is old
    pi_old = sortOld(data_owners, age)
    #bug_d(pi_old)
    # Send an email to the owners
    for pi in pi_old.keys():
        mail_address = mail_json['investigators'][pi]['email']
        mail_subject = 'Automatisk borttagning av sekvensdata från /seqstore'
        mail_body = mailTemplate(pi_old)

        print(mail_address)
        print(mail_subject)
        print(mail_body)

    # for pi in pi_old.keys():
    #     name = data['investigators'][pi]['name']
    #     email = data['investigators'][pi]['email']
    #     #print("Hello " + name + " @ " + email)
    #     # bug(pi_old[pi])
    #     bug('---')
    #     bug(pi, 'pi')
    #     bug(pi_old[pi]['month'], 'm')
    #     bug(pi_old[pi]['week'], 'w')
    #     bug(pi_old[pi]['day'], 'd')

def mailTemplate(data):
        text = """\

        Detta är ett automatiskt mail som skickas då ni står som ägare för rå-sekvensdata som snart kommer att tas bort från filservern permanent.

        Dessa kommer automatiskt att tas bort om 10 dagar. Om ni inte har något behov av att spara dessa filer så behöver ni inte göra någonting. Om ni istället vill att vi spar dessa så kontakta oss så snart som möjligt.

        De prover som berörs är från körningen med ID <run name> och har följande sample IDn:
        <samples list>

        Med vänliga automatiska hälsningar,
        CGG Bioinformatik
        """

def sortOld(data_owners, age):
    pi_old_list = {}
    for pi in data_owners:
        old_list = defaultdict(dict)
        for run in data_owners[pi]:
            if data_owners[pi][run]['age'] > age+30:
                old_list['day'][run] = data_owners[pi][run]['samples']
            elif data_owners[pi][run]['age'] > age+20:
                old_list['week'][run] = data_owners[pi][run]['samples']
            elif data_owners[pi][run]['age'] > age:
                old_list['month'][run] = data_owners[pi][run]['samples']

        pi_old_list[pi] = old_list

    return pi_old_list

def buildList(directory, sheetname):
    #Get a list of all runs
    runs = []

    for path in os.listdir(directory):  #This is a kinda ugly way to get all the dirs
        full_path = os.path.join(directory, path)
        if os.path.isdir(full_path) and re.match("^[0-9]{6}_", path):  #Is dir and starts with 6 digits
            runs.append(path)

    #Go over each sequencing run one by one
    #Check how old they are, what samples are in it, and who owns the sample
    #Make a dictionary where each run/sample is tied to an owner
    topdict = defaultdict(dict)
    for run in runs:
        #Full path of the run
        run_path = os.path.join(directory, run)

        # What is the age of the run
        run_dict = runAge(run)

        # Who owns what sample
        sheetpath = os.path.join(run_path, sheetname)
        owner_dict = sampleOwners(sheetpath)

        #Build a dict containing all info combined
        for pi in owner_dict:
            topdict[pi][run] = {}
            topdict[pi][run]['age'] = run_dict[run]['age']
            # Add samples with specific ones tied to owner
            topdict[pi][run]['samples'] = list(owner_dict[pi])

    return topdict

def runAge(run):
    today = datetime.datetime.now()
    run_dict = {}

    run_date = datetime.datetime.strptime(run.split('_')[0], '%y%m%d')
    run_age = (today - run_date).days

    run_dict[run] = {}
    run_dict[run]['age'] = run_age

    return run_dict

def runSamples(run):
    samples = []
    for name in os.listdir(run):
        if os.path.isdir(os.path.join(run, name)):
            samples.append(name)
    return samples

def sampleOwners(sheetpath):
    with open(sheetpath, mode='r') as csv_file:
        csv_reader = csv.reader(csv_file)
        pairs = []
        # Read in each line and save info about sample and owner
        for row in dropwhile(isDataLine, csv_reader): # Skip until the line starts with [Data]
            next(csv_reader, None) #Skip table header
            for row in csv_reader:
                extract = [row[10].split('_')[0], row[0]]
                pairs.append(extract)

      # Load values into a dictionary
        owner_dict = defaultdict(list)
        for key, value in pairs:
            owner_dict[key].append(value)
        return owner_dict

def isDataLine(line):
    if line and line[0] == '[Data]':
        return False
    else:
        return True

def bug(str, mark='*'): #Mark more clearly what is a debug message
    print("** Debug (" + mark +"):", end=' ')
    print(str)

def bug_d(dict):
    print(json.dumps(dict, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()