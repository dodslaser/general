#!/usr/bin/env python

import os
import click
import yaml
from tools.helpers import setup_logger, look_for_runs, gen_email_body
from move_researchdata import move_data
import sys
sys.path.append("..")
from CGG.tools.emailer import send_email
from CGG.tools.pidlock import PidFile

wrapper_path = os.path.abspath(os.path.dirname(__file__))

@click.command()
@click.option('--config-path', default=os.path.join(wrapper_path, 'configs/wrapper_config.yaml'),
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
    runlist = os.path.join(wrapper_path, config['previous_runs_file_path'])
    with open(runlist, 'r') as prev:
        previous_runs = [line.rstrip() for line in prev]

    ## Lock further calls to wrapper with PID lockfile to prevent multiple instances of script
    try:
        lockfilename = os.path.abspath(__file__)[:-3] + ".lock"
        with PidFile(lockfilename):
            ## Find all non processed demultiplex dirs, process them
            outfolder = config['outfolder']
            error_runs = []
            for instrument, demux_path in config['instrument_demux_paths'].items():
                runs = look_for_runs(demux_path)
                for run in runs:
                    if os.path.basename(run) in previous_runs:
                        continue  # skip previously processed

                    logger.info(f"Processing run: {run}.")

                    ## Process data
                    try:
                        move_data(run, outfolder, logger)
                        with open(runlist, 'a') as prev:  # Add processed run to runlist
                            prev.write(os.path.basename(run) + '\n')
                    except Exception as e:
                        error_runs.append(run)

            ## Send e-mail if problems with runs
            if len(error_runs) > 0:
                recipient = config['email']['recipient']
                sender = config['email']['sender']
                subject = config['email']['subject']
                body = gen_email_body(error_runs, full_log_path)

                send_email(recipient, sender, subject, body)

    except SystemExit as e:
        logger.error(f"{e}")

if __name__ == '__main__':
    wrapper()
