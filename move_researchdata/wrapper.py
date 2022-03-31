#!/usr/bin/env python

import os
import click
import yaml
from tools.helpers import setup_logger, look_for_runs, gen_email_body
from move_researchdata import move_data
import sys
sys.path.append("..")
from CGG.tools.emailer import send_email

@click.command()
@click.option('--config-path', default='configs/wrapper_config.yaml',
              type=click.Path(exists=True), help='Path to wrapper config file')
def wrapper(config_path):
    ## Sanity check. Only run as root
    if not os.geteuid() == 0:
        sys.exit("ERROR: You need to run this wrapper as root!")

    ## Read in the config file
    with open(config_path, 'r') as conf:
        config = yaml.safe_load(conf)

    ## Initialise logging
    log_path = config['logpath']
    full_log_path = os.path.join(log_path, 'move_research_data.log')
    logger = setup_logger('wrapper', full_log_path)

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
                recipient = config['email']['recipient']
                sender = config['email']['sender']
                subject = config['email']['subject']
                body = gen_email_body(error_runs, full_log_path)

                send_email(recipient, sender, subject, body)

if __name__ == '__main__':
    wrapper()
