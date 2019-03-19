class Config(object):
    SQLALCHEMY_DATABASE_URI = "sqlite:///SOEN487_A1.db"


class ProdConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///tests/test_SOEN487_A1.db"
