from flask import render_template
from flask_login import login_required

from app.user import user_blueprint


@user_blueprint.route("/")
@login_required
def home():
    return render_template("dashboard.html", load_time=None)
