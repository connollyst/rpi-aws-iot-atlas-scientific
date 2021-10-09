import logging
import os


def get_logger(name):
    logger = logging.getLogger(name)
    log_level = os.getenv('LOG_LEVEL')
    if log_level is not None:
        if log_level == "Info":
            logger.setLevel(logging.INFO)
        if log_level == "Debug":
            logger.setLevel(logging.DEBUG)
        if log_level == "Warning":
            logger.setLevel(logging.WARNING)
        if log_level == "Error":
            logger.setLevel(logging.ERROR)
        if log_level == "Critical":
            logger.setLevel(logging.CRITICAL)
    else:
        logger.setLevel(logging.DEBUG)
    stream_formatter = logging.Formatter('%(asctime)s:%(levelname)s: %(message)s')
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)
    return logger
