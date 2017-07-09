import os


class Config(object):
    DEBUG = False
    TEST = False
    TRACER = os.getenv("TRACER", False)

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    DATABASE_USER = os.getenv("DATABASE_USER")
    DATABASE_PASS = os.getenv("DATABASE_PASS")
    DATABASE_URI = os.getenv("DATABASE_URI")
    DATABASE_PORT = 3306
    DATABASE_DB = os.getenv("DATABASE_DB", "info_sub")
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{USER}:{PASS}@{URI}:{PORT}/{DBNAME}?charset=utf8".format(
        USER=DATABASE_USER,
        PASS=DATABASE_PASS,
        URI=DATABASE_URI,
        PORT=DATABASE_PORT,
        DBNAME=DATABASE_DB,
    )


# development
class DevelopmentConfig(Config):
    DEBUG = True
    TEST = True
    SECRET_KEY = "THIS_A_KEY"
    SQLALCHEMY_RECORD_QUERIES = True


# production
class ProductionConfig(Config):
    SECRET_KEY = os.getenv("SECRET_KEY")
    TRACER = True


# testing
class TestingConfig(Config):
    TEST = True
    SECRET_KEY = "THIS_A_KEY"

app_config = {
    "DEVELOPMENT": DevelopmentConfig,
    "PRODUCTION": ProductionConfig,
    "TESTING": TestingConfig,
    "DEFAULT": TestingConfig,
}

