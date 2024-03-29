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
@click.option('-q', '--include-fastqc', is_flag=True, default=False,
              help='Include fastqc if exists?', show_default=True)
def main(demultiplexdir, outbox, include_fastqc):
    # Set up the logfile and start logging
    logger = setup_logger('mv_resproj')
    logger.info(f'Looking for data belonging to research projects in {demultiplexdir}.')

    try:
        transfers = move_data(demultiplexdir, outbox, logger, include_fastqc)
    except StopIteration as e:
        logger.warning(f'{e}')
    except Exception as e:
        logger.error(f'{e}')

    logger.info(f"Completed {sum(transfers.values())} transfers.")

def move_data(demultiplexdir, outbox, logger, include_fastqc = False):
    # Look for path to SampleSheet
    samplesheet_path = os.path.join(demultiplexdir, 'SampleSheet.csv')
    if not os.path.exists(samplesheet_path):
        raise StopIteration(f"No SampleSheet.csv @ {demultiplexdir}. Skipping run.")

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
    return_dict = {}
    for project, samples in projects.items():
        # Get name of run
        run_name = os.path.basename(os.path.normpath(demultiplexdir))
        project_outbox = os.path.join(outbox, project, 'shared')

        # Check that user has write permissions in project outbox
        if os.access(project_outbox, os.W_OK):
            logger.info(f"User {os.getlogin()} has write permissions in {project_outbox}. Proceeding.")
        else:
            raise PermissionError(f"User {os.getlogin()} has no write permission in {project_outbox}")

        #Check that there is an outbox for the project
        if not os.path.exists(project_outbox):
            logger.error(f"Could not find outbox folder for {project}. Please create it. Exiting.")
            raise FileNotFoundError(f"No outbox folder for {project}")

        # Make fastq folder if not existing
        fastq_outbox = os.path.join(project_outbox, run_name, 'fastq')
        if not os.path.exists(fastq_outbox):
            os.makedirs(fastq_outbox)

        # Transfer the fastq files
        logger.info(f"Copying {len(projects[project])} samples to {project_outbox}. Skipping existing.")
        return_dict[project] = 0

        # find all fastq files
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
            if include_fastqc:
                fastqc_files = glob.glob(os.path.join(demultiplexdir, 'fastqc/') + sample + "*_fastqc.zip")
                if len(fastqc_files) > 0:
                    #Make fast-QC folder if not existing
                    fastqc_outbox = os.path.join(project_outbox, run_name, 'fastqc')
                    os.makedirs(fastqc_outbox, exists_ok = True)

                    #Transfer fastq zip file
                    # Make the rsync command
                    rsync_cmd = ['rsync', '-P', '--ignore-existing', *fastqc_files, fastq_outbox]

                    # Transfer via rsync
                    rsync_results = subprocess.run(rsync_cmd)
                    if rsync_results.returncode != 0:
                        logger.warning(f"Problems copying fastQC files for sample {sample} via rsync.")

            return_dict[project] += 1

    return return_dict


if __name__ == '__main__':
    main()
