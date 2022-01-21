#!/usr/bin/env python
import sys
import re
import click
from sample_sheet import SampleSheet
import os
import logging


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
        project_outbox = os.path.join(outbox, project, 'shared')
        if not os.path.exists(project_outbox):
            logger.error(f"Could not find outbox folder for {project}. Please create it. Exiting.")
            sys.exit()


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
