#!/usr/bin/env python

import click
import os
import csv
from itertools import dropwhile
import glob

@click.command()
@click.option('-d', '--demultiplexdir', required=True,
              help='Path to demultiplex dir of run')
@click.option('-o', '--outdir', required=True,
              help='Path to output folder')
def main(demultiplexdir, outdir):
    #Set the path to the samplesheet
    samplesheet = os.path.join(demultiplexdir, 'SampleSheet.csv')
    
    #Collect which samples were found
    sample_list = []

    #Loop over the sample sheet and find all Pathology samples
    with open(samplesheet, mode='r') as f:
        csv_reader = csv.reader(f)
        next(dropwhile(isDataLine, csv_reader)) # Skip until the line starts with [Data]
        for row in csv_reader:
            department = row[9]
            #Choose only samples belonging to PAT
            if department == 'PAT':
                sample = row[1]
                #Append sample to sample list
                sample_list.append(sample)

    #Write some logging
    print("** LOG: Found the following samples belonging to PAT:")
    for sample in sample_list:
        print("\t" + sample)
    print ("** LOG: Making symlinks...", end="")

    #Make the symlinks for the samples
    for sample in sample_list:
        fastqs = allFastqs(demultiplexdir, sample)
        for fastq in fastqs:
            destPath = os.path.join(outdir, os.path.basename(fastq))
            if os.path.exists(destPath): #Skip if already there
                next
            else:
                os.symlink(fastq, destPath)

    print("done.")

def isDataLine(line):
    if line and line[0] == 'Sample_ID':
        return False
    else:
        return True

def allFastqs(demultiplexdir, sample):
    fastqPath = demultiplexdir + "/fastq/" + sample + "*.fastq.gz"
    fastqList = glob.glob(fastqPath)
    return fastqList


if __name__ == '__main__':
    main()
