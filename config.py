import os
from celery.schedules import crontab
from app.util.helper import str2bool


class Config(object):
    DEBUG = False
    TEST = False
    TRACER = False

    PROJECT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app")
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
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"
    CELERY_TASK_SERIALIZER = "json"
    CELERY_TASK_RESULT_EXPIRES = 3600
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_RESULT_SERIALIZER = 'json'

    CELERYBEAT_SCHEDULE = {
        'get_article_everyday': {
            'task': 'get_article_everyday',
            # 'schedule': timedelta(seconds=3),
            'schedule':crontab(hour=6)
        },
    }
    CELERY_TIMEZONE = 'UTC'


# development
class DevelopmentConfig(Config):
    DEBUG = True
    TEST = True
    TRACER = str2bool(os.getenv("TRACER"), default=False)
    SECRET_KEY = "THIS_A_KEY"
    SQLALCHEMY_RECORD_QUERIES = True


# production
class ProductionConfig(Config):
    SECRET_KEY = os.getenv("SECRET_KEY")
    TRACER = True


# testing
class TestingConfig(Config):
    TEST = True
    TRACER = True
    SECRET_KEY = "THIS_A_KEY"


def get_config_obj():
    RUNTIME = os.getenv("RUNTIME", "DEFAULT")
    return app_config.get(RUNTIME, TestingConfig)


app_config = {
    "DEVELOPMENT": DevelopmentConfig,
    "PRODUCTION": ProductionConfig,
    "TESTING": TestingConfig,
    "DEFAULT": TestingConfig,
}


def get_app_config():
    return app_config[os.getenv("RUNTIME", "DEFAULT")]
