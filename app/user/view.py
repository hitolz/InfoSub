from flask import render_template
from app.user import user_blueprint


@user_blueprint.route("/")
def home():
    return render_template("dashboard.html")
