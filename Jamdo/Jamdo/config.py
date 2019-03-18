class Config(object):
    SQLALCHEMY_DATABASE_URI = r"sqlite:///soen487.sqlite"
    
class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
