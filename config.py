import logging
import os
from configparser import ConfigParser

DJANGO = 'django'
SECRET_KEY = 'secret_key'

EXCEPTION_TAG = 'exception_tag'

LOG = 'log'
FILE_NAME = 'filename'
ENABLE_SYS_LOG = 'enable_sys_log'
ENABLE_FILE_LOG = 'enable_file_log'
LEVEL = 'level'


SCHEDULER = 'scheduler'
HOUR_DURATION = 'hour_duration'





class Config:
    _instance = None

    @staticmethod
    def get_instance():
        if not Config._instance:
            Config._instance = Config()
        return Config._instance

    def __init__(self):
        self.config = ConfigParser()
        self.config.read('config.ini')

    def get_property(self, section, item):
        env_variable = "{}_{}".format(section, item)
        value = os.environ.get(env_variable)
        if not value:
            value = self.config.get(section, item)
        return value

    @property
    def django_secret_key(self):
        return self.get_property(DJANGO, SECRET_KEY)

    @property
    def log_file(self):
        return self.get_property(LOG, FILE_NAME)

    @property
    def enable_file_log(self):
        return self.get_property(LOG, ENABLE_FILE_LOG) == 'True'

    @property
    def enable_sys_log(self):
        return self.get_property(LOG, ENABLE_SYS_LOG) == 'True'

    @property
    def exception_tag(self):
        return self.get_property(LOG, EXCEPTION_TAG)

    @property
    def log_level(self):
        log_level = self.get_property(LOG, LEVEL)
        return logging.DEBUG if log_level == 'debug' else logging.INFO    
    
    @property
    def scheduler_hour_duration(self):
        return int(self.get_property(SCHEDULER, HOUR_DURATION))

    

if __name__ == '__main__':
    config = Config.get_instance()
