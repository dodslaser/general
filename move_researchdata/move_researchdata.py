#!/usr/bin/env python

import os
import re
import sys
import glob
import subprocess
from collections import defaultdict

import click
from sample_sheet import SampleSheet
from tools.helpers import setup_logger

@click.command()
@click.option('-d', '--demultiplexdir', required=True, type=click.Path(exists=True),
              help='Path to demultiplex dir of run')
@click.option('-o', '--outbox', default='/seqstore/remote/outbox/research_projects',
              help='Path to outbox', show_default=True)
def main(demultiplexdir, outbox):
    # Set up the logfile and start logging
    logger = setup_logger('mv_resproj')
    logger.info(f'Looking for data belonging to research projects in {demultiplexdir}.')

    num_transfers = move_data(demultiplexdir, outbox, logger)

    logger.info(f"Completed {num_transfers} transfers.")

def move_data(demultiplexdir, outbox, logger):
    # Look for path to SampleSheet
    samplesheet_path = os.path.join(demultiplexdir, 'SampleSheet.csv')
    if not os.path.exists(samplesheet_path):
        logger.error(f'Could not SampleSheet.csv @ {demultiplexdir}')
        raise FileNotFoundError

    # Check that user has write permissions in outbox
    if os.access(outbox, os.W_OK):
        logger.info(f"User has write permissions in {outbox}. Proceeding.")
    else:
        logger.error(f"No write permissions in {outbox}. Exiting.")
        raise PermissionError


    # Parse samplesheet and look for data belonging to research projects
    sheet = SampleSheet(samplesheet_path)
    projects = defaultdict(list)
    for sample in sheet.samples:
        sample_name = sample['Sample_Name']
        sample_project = sample['Sample_Project']

        # Look for projects name matching regex
        research_regex = 'G[1-2][0-9]-[0-9]{3}'
        if re.search(research_regex, sample_project):
            projects[sample_project].append(sample_name)

    # Check how many samples there are
    num_samples = sum([len(x) for x in projects.values()])

    if num_samples > 0:
        logger.info(f"Found {num_samples} samples belonging to {len(projects)} research projects.")
    else:
        logger.info(f"Could not find any research samples in {demultiplexdir}. Exiting.")
        return

    # Check that there is an outbox folder for all projects
    for project, samples in projects.items():
        # Get name of run
        run_name = os.path.basename(os.path.normpath(demultiplexdir))
        project_outbox = os.path.join(outbox, project, 'shared')

        #Check that there is an outbox for the project
        if not os.path.exists(project_outbox):
            logger.error(f"Could not find outbox folder for {project}. Please create it. Exiting.")
            raise FileNotFoundError

        # Make fastq folder if not existing
        fastq_outbox = os.path.join(project_outbox, run_name, 'fastq')
        if not os.path.exists(fastq_outbox):
            os.makedirs(fastq_outbox)

        # Transfer the fastq files
        logger.info(f"Copying {len(projects[project])} samples to {project_outbox}. Skipping existing.")
        # find all fastq files
        successful_transfers = 0
        for sample in samples:
            fastq_files = glob.glob(os.path.join(demultiplexdir,'fastq/') + sample + "*.fastq.gz")
            #logger.info(f"Using rsync to transfer {len(fastq_files)} fastq files for {sample}.")

            # Make the rsync command
            rsync_cmd = ['rsync', '-P', '--ignore-existing', *fastq_files, fastq_outbox]

            # Transfer via rsync
            rsync_results = subprocess.run(rsync_cmd)
            if rsync_results.returncode != 0:
                logger.error(f"Problems copying fastq files for sample {sample} via rsync.")
                raise ConnectionError

            # If there are fastqc results, move them as well
            fastqc_files = glob.glob(os.path.join(demultiplexdir, 'fastqc/') + sample + "*_fastqc.zip")
            if len(fastqc_files) > 0:
                #Make fast-QC folder if not existing
                fastqc_outbox = os.path.join(project_outbox, run_name, 'fastqc')
                if not os.path.exists(fastqc_outbox):
                    os.makedirs(fastqc_outbox)

                #Transfer fastq zip file
                # Make the rsync command
                rsync_cmd = ['rsync', '-P', '--ignore-existing', *fastqc_files, fastq_outbox]

                # Transfer via rsync
                rsync_results = subprocess.run(rsync_cmd)
                if rsync_results.returncode != 0:
                    logger.warning(f"Problems copying fastQC files for sample {sample} via rsync.")

            successful_transfers += 1

    return successful_transfers


if __name__ == '__main__':
    main()
