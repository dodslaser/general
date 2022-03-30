#!/usr/bin/env python

import os
import click
import yaml
from tools.helpers import setup_logger, look_for_runs
from move_researchdata import move_data

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
    logger = setup_logger('wrapper', os.path.join(log_path, 'move_research_data.log'))

    ## Read in demuxdir-runlist.txt
    runlist = config['previous_runs_file_path']
    with open(runlist, 'r') as prev:
        previous_runs = [line.rstrip() for line in prev]

    ## Find all non processed demultiplex dirs, process them
    for instrument, demux_path in config['instrument_demux_paths'].items():
        runs = look_for_runs(demux_path)
        for run in runs:
            if os.path.basename(run) in previous_runs:
                continue # skip previously processed

            logger.info(f"Processing run: {run}.")

            ## Process data
            outfolder = config['outfolder']
            error_runs = []
            try:
                move_data(run, outfolder, logger)
                with open(runlist, 'a') as prev:  # Add processed run to runlist
                    prev.write(os.path.basename(run))
            except Exception as e:
                error_runs.append(run)

            ## Send e-mail if problems with runs
            if len(error_runs) > 0:
                pass
               # print(error_runs)

if __name__ == '__main__':
    wrapper()