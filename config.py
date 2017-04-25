import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR_NAME = 'data'

class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    #
    DIR_BASE = BASE_DIR
    DIR_DATA = os.path.join(BASE_DIR, DATA_DIR_NAME)
    if not os.path.isdir(DIR_DATA):
        os.makedirs(DIR_DATA)

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True