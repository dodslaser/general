#!/usr/bin/env python

import os
import sys
import click
import yaml
from tools.helpers import setup_logger

@click.command()
@click.option('--config-path', default='configs/wrapper_config.yaml',
              help='Path to wrapper config file')
def wrapper(config_path):
    ## Sanity check. Only run as root
    #if not os.geteuid() == 0:
    #    print("ERROR: You need to run this wrapper as root!")
    #    sys.exit()

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

    ## Move all research data

    ## Add demultiplexdir to demuxdir-runlist.txt

if __name__ == '__main__':
    wrapper()