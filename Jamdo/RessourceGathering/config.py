import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # SQLALCHEMY_DATABASE_URI = "sqlite:///SOEN487_A1.db"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'resource'
    SERVER_AUTH_PASSWORD = 'RESOURCE_SERVER_PASSWORD'
    SERVER_PORT = 5000


class ProdConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'resource'
    SERVER_AUTH_PASSWORD = 'RESOURCE_SERVER_PASSWORD'
    SERVER_PORT = 5000


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'resource'
    SERVER_AUTH_PASSWORD = 'RESOURCE_SERVER_PASSWORD'
    SERVER_PORT = 5000

class TestConfig(Config):
    TESTING = True
    # SQLALCHEMY_DATABASE_URI = "sqlite:///tests/test_SOEN487_A1.db"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'resource'
    SERVER_AUTH_PASSWORD = 'RESOURCE_SERVER_PASSWORD'
    SERVER_PORT = 5000