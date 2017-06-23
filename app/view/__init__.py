from flask import Blueprint

view_blueprint = Blueprint("view", __name__)

from .index import *
from .login import *

