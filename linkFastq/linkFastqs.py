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
    #print(samplesheet)

    #Loop over the sample sheet and find all Pathology samples
    with open(samplesheet, mode='r') as f:
        csv_reader = csv.reader(f)
        #print(csv_reader)
        next(dropwhile(isDataLine, csv_reader)) # Skip until the line starts with [Data]
        for row in csv_reader:
            department = row[9]
            if department == 'PAT':
                sample = row[1]
                fastqs = allFastqs(demultiplexdir, sample)
                print(fastqs)
                for fastq in fastqs:
                    destPath = os.path.join(outdir, os.path.basename(fastq))
                    os.symlink(fastq, destPath)

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
