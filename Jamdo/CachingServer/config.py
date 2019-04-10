import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # SQLALCHEMY_DATABASE_URI = r"sqlite:///soen487.sqlite"
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'caching'
    SERVER_AUTH_PASSWORD = 'CACHE_SERVER_PASSWORD'
    SERVER_PORT = 8000
    
class ProdConfig(Config):
	SERVER_AUTH_NAME = 'caching'
	SERVER_AUTH_PASSWORD = 'CACHE_SERVER_PASSWORD'
	SERVER_PORT = 8000

class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super_secret_key'
    SERVER_AUTH_NAME = 'caching'
    SERVER_AUTH_PASSWORD = 'CACHE_SERVER_PASSWORD'
    SERVER_PORT = 8000
