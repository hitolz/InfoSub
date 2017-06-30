from flask import Blueprint

user_blueprint = Blueprint("user", __name__, template_folder="templates", url_prefix='/user')

from .view import *
