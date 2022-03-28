import logging

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    stream_handle = logging.StreamHandler()
    stream_handle.setLevel(logging.DEBUG)
    stream_handle.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(stream_handle)

    return logger

def look_for_runs(root_path):
    found_paths = glob.glob(os.path.join(root_path, '*'))
    regex = '^[0-9]{6}_A[0-9]{5}_[0-9]{4}_.{10}$'
    return [path for path in found_paths if re.search(regex, os.path.basename(path))]

