#!/usr/bin/env python

from tools.helpers import setup_logger

logger = setup_logger('wrapper', os.path.join(ROOT_LOGGING_PATH, 'wopr_wrapper.log'))

def wrapper():
    ## Read in the config file

    ## Read in demuxdir-runlist.txt

    ## Find all non processed demultiplex dirs

    ## Move all research data

    ## Add demultiplexdir to demuxdir-runlist.txt

if __name__ == '__main__':
    wrapper()