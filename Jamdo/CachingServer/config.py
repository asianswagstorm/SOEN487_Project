class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
