#!/usr/bin/env python

import os
import re
import sys
import glob
import logging
import subprocess

import click
from sample_sheet import SampleSheet

@click.command()
@click.option('-d', '--demultiplexdir', required=True,
              help='Path to demultiplex dir of run')
@click.option('-o', '--outbox', default='/seqstore/remote/outbox/research_projects',
              help='Path to outbox. Default: /seqstore/remote/outbox/research_projects')
def main(demultiplexdir, outbox):
    # Set up the logfile and start logging
    logger = setup_logger('mv_resproj')
    logger.info(f'Looking for data belonging to research projects in {demultiplexdir}.')

    # Check that the demultiplexdir exists
    if not os.path.exists(demultiplexdir):
        logger.error(f"The path {demultiplexdir} does not seem to exist.")
        sys.exit()

    # Look for path to SampleSheet
    samplesheet_path = os.path.join(demultiplexdir, 'SampleSheet.csv')
    if not os.path.exists(samplesheet_path):
        logger.error(f'Could not SampleSheet.csv @ {demultiplexdir}')
        sys.exit()

    # Check that user has write permissions in outbox
    if os.access(outbox, os.W_OK):
        logger.info(f"User has write permissions in {outbox}. Proceeding.")
    else:
        logger.error(f"No write permissions in {outbox}. Exiting.")
        sys.exit()


    # Parse samplesheet and look for data belonging to research projects
    sheet = SampleSheet(samplesheet_path)
    projects = {}
    for sample in sheet.samples:
        sample_name = sample['Sample_Name']
        sample_project = sample['Sample_Project']

        # Look for projects name matching regex
        research_regex = 'G[1-2][0-9]-[0-9]{3}'
        if re.search(research_regex, sample_project):
            if sample_project in projects:
                projects[sample_project].append(sample_name)
            else:
                projects[sample_project] = [sample_name]

    # Check how many samples there are
    num_samples = sum([len(x) for x in projects.values()])

    if num_samples > 0:
        logger.info(f"Found {num_samples} samples belonging to {len(projects)} research projects.")
    else:
        logger.info(f"Could not find any research samples in {demultiplexdir}. Exiting.")
        sys.exit()

    # Check that there is an outbox folder for all projects
    for project in projects:
        # Get name of run
        run_name = os.path.basename(os.path.normpath(demultiplexdir))
        project_outbox = os.path.join(outbox, project, 'shared')

        #Check that there is an outbox for the project
        if not os.path.exists(project_outbox):
            logger.error(f"Could not find outbox folder for {project}. Please create it. Exiting.")
            sys.exit()

        # Make fastq folder if not existing
        fastq_outbox = os.path.join(project_outbox, run_name, 'fastq')
        if not os.path.exists(fastq_outbox):
            os.mkdir(fastq_outbox)

        # Transfer the fastq files
        logger.info(f"Copying {len(projects[project])} samples to {project_outbox}. Skipping existing.")
        # find all fastq files
        for sample in projects[project]:
            fastq_files = glob.glob(os.path.join(demultiplexdir,'fastq/') + sample + "*.fastq.gz")
            #logger.info(f"Using rsync to transfer {len(fastq_files)} fastq files for {sample}.")

            # Make the rsync command
            rsync_cmd = ['rsync', '-P', '--ignore-existing']
            rsync_cmd.extend(fastq_files)
            rsync_cmd.append(fastq_outbox)

            # Transfer via rsync
            rsync_results = subprocess.run(rsync_cmd)
            if not rsync_results:
                logger.error(f"Problems copying fastq files for sample {sample} via rsync. Check the logs.")

            # If there are fastqc results, move them as well
            fastqc_files = glob.glob(os.path.join(demultiplexdir, 'fastqc/') + sample + "*_fastqc.zip")
            if len(fastqc_files) > 0:
                #Make fast-QC folder if not existing
                fastqc_outbox = os.path.join(project_outbox, run_name, 'fastqc')
                if not os.path.exists(fastqc_outbox):
                    os.mkdir(fastqc_outbox)

                #Transfer fastq zip file
                # Make the rsync command
                rsync_cmd = ['rsync', '-P', '--ignore-existing']
                rsync_cmd.extend(fastqc_files)
                rsync_cmd.append(fastqc_outbox)

                # Transfer via rsync
                rsync_results = subprocess.run(rsync_cmd)
                if not rsync_results:
                    logger.error(f"Problems copying fastQC files for sample {sample} via rsync. Check the logs.")

    logger.info(f"All transfers complete.")

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handle = logging.StreamHandler()
    stream_handle.setLevel(logging.DEBUG)
    stream_handle.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(stream_handle)

    return logger

if __name__ == '__main__':
    main()
