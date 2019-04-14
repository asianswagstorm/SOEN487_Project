import os
basedir = os.path.abspath(os.path.dirname(__file__))

class ServerPasswords():
    APPLICATION = 'APPLICATION_SERVER_PASSWORD'
    CACHE = 'CACHE_SERVER_PASSWORD'
    RESOURCE = 'RESOURCE_SERVER_PASSWORD' 

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'THIS_IS_A_VERY_DEEP_SECRET'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'AuthClients.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SERVER_AUTH_NAME = 'authentication'
    SERVER_AUTH_PASSWORD = 'AUTH_SERVER_PASSWORD'
    SERVER_PORT = 9000
    
class ProdConfig(Config):
    SERVER_AUTH_NAME = 'authentication'
    SERVER_AUTH_PASSWORD = 'AUTH_SERVER_PASSWORD'
    SERVER_PORT = 9000

class DevConfig(Config):
    DEBUG = True
    SERVER_AUTH_NAME = 'authentication'
    SERVER_AUTH_PASSWORD = 'AUTH_SERVER_PASSWORD'
    SERVER_PORT = 9000

class TestConfig(Config):
    TESTING = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'THIS_IS_A_VERY_DEEP_SECRET'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'test.db')
    SERVER_AUTH_NAME = 'authentication'
    SERVER_AUTH_PASSWORD = 'AUTH_SERVER_PASSWORD'
    SERVER_PORT = 9000