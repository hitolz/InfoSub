from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import app_config
from app.util.errors import ConfigError

db = SQLAlchemy()
login_manager = LoginManager()


def create_app(config_name):
    if config_name not in app_config:
        raise ConfigError("{} is a wrong config name.".format(config_name))
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    from app.user import user_blueprint
    from app.information import info_blueprint
    from app.view import view_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(info_blueprint)
    app.register_blueprint(view_blueprint)

    db.init_app(app)
    login_manager.init_app(app)
    return app

