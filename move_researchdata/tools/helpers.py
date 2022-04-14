import logging
import glob
import os
import re

def setup_logger(name, log_path=None):
    """Initialise a log file using the logging package"""
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
    """Find all regular looking run folders at a given path"""
    found_paths = glob.glob(os.path.join(root_path, '*'))
    regex = '^[0-9]{6}_(?:NB|A)[0-9]*_[0-9]{4}_.{10}$' # NovaSeq & NextSeq
    return [path for path in found_paths if re.search(regex, os.path.basename(path))]

def gen_error_body(error_runs, log_path):
    body = '\n'. join(["While trying to move research data to their correct sFTP folder, "
                       "the following runs gave errors.",
                       "\n".join(error_runs),
                       '',
                       '',
                       f"Please see the complete log @ {log_path}.",
                       '',
                       "Kind regards,\nClinical Genomics IT-group."])

    return body

def gen_success_body(success_runs):
    #Create the greeting
    body = "The following runs were detected to contain research samples, " \
           "and the number of samples moved to outbox folder is as follows:\n\n"

    #Add all runs with research projects and number of samples
    for run in success_runs:
        body += f'{os.path.basename(run)}:\n'
        for project in success_runs[run]:
            body += f'{project} - {success_runs[run][project]} samples\n'
        body += '\n'

    #Slap on the signature
    body += "Kind regards,\nClinical Genomics Gothenburg."

    return body
