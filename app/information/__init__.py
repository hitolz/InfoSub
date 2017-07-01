from flask import Blueprint

info_blueprint = Blueprint("info", __name__, template_folder="templates", url_prefix='/info')

from .view import *


