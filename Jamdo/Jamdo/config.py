import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = r"sqlite:///soen487.sqlite"
    #SQLALCHEMY_DATABASE_URI = r"sqlite:///test_Users.sqlite" #manual test user
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'application'
    SERVER_AUTH_PASSWORD = 'APPLICATION_SERVER_PASSWORD'
    SERVER_PORT = 7000
    
class ProdConfig(Config):
	SERVER_AUTH_NAME = 'application'
	SERVER_AUTH_PASSWORD = 'APPLICATION_SERVER_PASSWORD'
	SERVER_PORT = 7000

class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'application'
    SERVER_AUTH_PASSWORD = 'APPLICATION_SERVER_PASSWORD'
    SERVER_PORT = 7000

class TestConfig(Config):
    TESTING = True
    SERVER_AUTH_NAME = 'application'
    SERVER_AUTH_PASSWORD = 'APPLICATION_SERVER_PASSWORD'
    SQLALCHEMY_DATABASE_URI = r"sqlite:///test_Users.sqlite"