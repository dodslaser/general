#!/usr/bin/env python

import os
import click
import yaml
from tools.helpers import setup_logger, look_for_runs, gen_error_body, gen_success_body
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
    success_runs = {}
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

                    ## Process data, capture number of moved samples
                    try:
                        success_transfers = move_data(run, outfolder, logger)
                        success_runs[run] = success_transfers
                        with open(runlist, 'a') as prev:  # Add processed run to runlist
                            prev.write(os.path.basename(run) + '\n')
                    except StopIteration as e:
                        logger.info(f"{e}")
                    except Exception as e:
                        logger.error(f"{e}")
                        error_runs.append(run)

            ## Send e-mail if problems with runs
            if len(error_runs) > 0:
                recipient = config['error-email']['recipient']
                sender = config['error-email']['sender']
                subject = config['error-email']['subject']
                body = gen_error_body(error_runs, full_log_path)

                send_email(recipient, sender, subject, body)

    except SystemExit as e:
        print({e})

    #Send out success e-mail if any transfers were made
    if success_runs:
        recipient = config['success-email']['recipient']
        sender = config['success-email']['sender']
        subject = config['success-email']['subject']
        cc = config['success-email']['cc']
        body = gen_success_body(success_runs)

        send_email(recipient, sender, subject, body, cc_recipients = cc)


if __name__ == '__main__':
    wrapper()
