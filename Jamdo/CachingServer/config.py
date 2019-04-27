import os

class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'application'
    SERVER_AUTH_PASSWORD = 'APPLICATION_SERVER_PASSWORD'
    SERVER_PORT = 5000

class ProdConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'caching'
    SERVER_AUTH_PASSWORD = 'CACHE_SERVER_PASSWORD'
    SERVER_PORT = 5000


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'caching'
    SERVER_AUTH_PASSWORD = 'CACHE_SERVER_PASSWORD'
    SERVER_PORT = 5000


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'caching'
    SERVER_AUTH_PASSWORD = 'CACHE_SERVER_PASSWORD'
    SERVER_PORT = 5000