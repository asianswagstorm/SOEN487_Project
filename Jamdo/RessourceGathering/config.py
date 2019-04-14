import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'resource'
    SERVER_AUTH_PASSWORD = 'RESOURCE_SERVER_PASSWORD'
    SERVER_PORT = 3000


class ProdConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'resource'
    SERVER_AUTH_PASSWORD = 'RESOURCE_SERVER_PASSWORD'
    SERVER_PORT = 3000


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'resource'
    SERVER_AUTH_PASSWORD = 'RESOURCE_SERVER_PASSWORD'
    SERVER_PORT = 3000

class TestConfig(Config):
    TESTING = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'resource'
    SERVER_AUTH_PASSWORD = 'RESOURCE_SERVER_PASSWORD'
    SERVER_PORT = 3000