import logging
import logging.handlers
import os
import sys
from datetime import datetime

from config import Config

config = Config.get_instance()
log_factory = {}


def get_logger(name) -> logging.Logger:
    if name not in log_factory:
        filename = config.log_file
        filename = datetime.now().strftime(filename + '_%d_%m_%Y.log')

        logger = logging.getLogger(name)
        logger.setLevel(config.log_level)

        log_format = '%(asctime)s  %(name)-20s [%(levelname)s] %(filename)s : %(funcName)s : [line %(lineno)s]' \
                     ' - %(message)s'
        formatter = logging.Formatter(log_format, datefmt='%a %d %b %Y %H:%M:%S')

        if config.enable_file_log:
            if not os.path.exists('log'):
                os.mkdir('log')
            handler = logging.handlers.RotatingFileHandler(filename, maxBytes=1024, backupCount=5)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        if config.enable_sys_log:
            stdout_handler = logging.StreamHandler()
            stdout_handler.setFormatter(formatter)
            logger.addHandler(stdout_handler)
        log_factory[name] = logger

    return log_factory[name]


def exception_logger(type, value, tb):
    logger = get_logger(config.exception_tag)
    logger.error("Uncaught exception: {0}".format(str(value)), exc_info=(type, value, tb))


sys.excepthook = exception_logger
