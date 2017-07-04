from datetime import datetime
from flask import render_template, abort, redirect, url_for
from flask_login import login_required, current_user, logout_user

from app.user import user_blueprint
from app.services.dashboard import get_dashboard_data
from .form.setting import UserInfoForm, UserPassEditForm, DeleteUserForm


@user_blueprint.route("/")
@login_required
def home():
    _start = datetime.now()
    plans = current_user.plans
    data = get_dashboard_data()
    _load_time = (datetime.now() - _start).microseconds * 0.000001
    return render_template("dashboard.html", data=data, plans=plans, load_time=_load_time)


@user_blueprint.route("/setting/<path>", methods=['GET', 'POST'])
@login_required
def setting(path):
    _start = datetime.now()
    form = None
    if path == "profile":
        form = UserInfoForm()
    elif path == "message":
        pass
    elif path == "account":
        form = UserPassEditForm()
    elif path == "delete":
        form = DeleteUserForm()
    else:
        abort(404)

    if form and form.validate_on_submit():
        if path == "profile":
            current_user.email = form.email.data
            current_user.update()
        elif path == "message":
            pass
        elif path == "account":
            current_user.update_password(form.new_password.data)
            logout_user()
            return redirect(url_for("view.login"))
        elif path == "delete":
            current_user.delete()
            return redirect(url_for("view.home"))

    if path == "profile":
        form.username.data = current_user.username
        form.email.data = current_user.email
    _load_time = (datetime.now() - _start).microseconds * 0.000001
    return render_template("setting/{}.html".format(path), form=form, load_time=_load_time)

