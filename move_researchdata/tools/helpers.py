import logging
import glob
import os
import re

def setup_logger(name, log_path=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handle = logging.StreamHandler()
    stream_handle.setLevel(logging.DEBUG)
    stream_handle.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s'))
    logger.addHandler(stream_handle)

    if log_path:
        file_handle = logging.FileHandler(log_path, 'a')
        file_handle.setLevel(logging.DEBUG)
        file_handle.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s'))
        logger.addHandler(file_handle)

    return logger

def look_for_runs(root_path):
    found_paths = glob.glob(os.path.join(root_path, '*'))
    regex = '^[0-9]{6}_(?:NB|A)[0-9]*_[0-9]{4}_.{10}$' # NovaSeq & NextSeq
    return [path for path in found_paths if re.search(regex, os.path.basename(path))]

