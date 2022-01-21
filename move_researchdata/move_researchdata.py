#!/usr/bin/env python
import sys
import click
from sample_sheet import SampleSheet
import os
import logging


@click.command()
@click.option('-d', '--demultiplexdir', required=True,
              help='Path to demultiplex dir of run')
def main(demultiplexdir):
    # Set up the logfile and start logging
    logger = setup_logger('mv_resproj')
    logger.info(f'Looking for data belonging to research projects in {demultiplexdir}.')

    # Check that the demultiplexdir exists
    if not os.path.exists(demultiplexdir):
        logger.error(f"The path {demultiplexdir} does not seem to exist.")
        sys.exit()

    # Look for path to SampleSheet
    samplesheet_path = os.path.join(demultiplexdir, 'SampleSheet.csv')
    if os.path.exists(samplesheet_path):
        print("Found it")
    else:
        logger.error(f'Could not SampleSheet.csv @ {demultiplexdir}')
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
