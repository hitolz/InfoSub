from flask import Flask

from config import app_config
from app.util.errors import ConfigError
from app.admin import admin
from app.extensions import db, login_manager


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

    from app.extensions import display_plan_type, display_play, display_user
    jinja_env = app.jinja_env
    jinja_env.filters['plan_type'] = display_plan_type
    jinja_env.filters['plan_name'] = display_play
    jinja_env.filters['user_type'] = display_user

    db.init_app(app)
    login_manager.init_app(app)

    admin.init_app(app)
    return app
