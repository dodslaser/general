#!/usr/bin/env python

import os
import sys
import click
import yaml
import subprocess
from tools.helpers import setup_logger, look_for_runs

@click.command()
@click.option('--config-path', default='configs/wrapper_config.yaml',
              help='Path to wrapper config file')
def wrapper(config_path):
    ## Sanity check. Only run as root
    if not os.geteuid() == 0:
        print("ERROR: You need to run this wrapper as root!")
        sys.exit()

    ## Read in the config file
    with open(config_path, 'r') as conf:
        config = yaml.safe_load(conf)

    ## Initialise logging
    log_path = config['logpath']
    logger = setup_logger('wrapper', os.path.join(log_path, 'wopr_wrapper.log'))

    ## Read in demuxdir-runlist.txt
    runlist = config['previous_runs_file_path']
    with open(runlist, 'r') as prev:
        previous_runs = [line.rstrip() for line in prev]

    ## Find all non processed demultiplex dirs
    runs_to_process = []
    for instrument in config['instrument_demux_paths'].keys():
        demux_path = config['instrument_demux_paths'][instrument]
        ## Get all demultiplexed runs
        runs = look_for_runs(demux_path)
        for run in runs:
            if os.path.basename(run) in previous_runs:
                continue # skip previously processed
            else:
                runs_to_process.append(run)

    ## Move all research data
    if len(runs_to_process) > 0:
        logger.info(f"Found {len(runs_to_process)} run(s) to process")
    else:
        sys.exit()

    for run in runs_to_process:
        cmd_list = ['python','move_researchdata.py', '-d', run]
        subprocess.run(cmd_list)

    ## Add processed demultiplexdir to demuxdir-runlist.txt
    with open(runlist, 'a') as prev:
        for run in runs_to_process:
            prev.write(os.path.basename(run))

if __name__ == '__main__':
    wrapper()