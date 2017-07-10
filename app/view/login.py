from flask import render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user

from app.view import view_blueprint
from app.user.form.login import LoginForm, RegisterForm
from app.services.user import get_user_by_username_or_email, create_user, init_user_plan
from app.util.captcha_tool import Captcha


@view_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    if current_user and current_user.is_authenticated:
        return redirect(url_for("user.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = get_user_by_username_or_email(form.username_or_email.data)
        login_user(user, form.remember.data)
        return redirect(url_for("user.home"))
    return render_template("login.html", form=form)


@view_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    if current_user and current_user.is_authenticated:
        return redirect(url_for("user.home"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = create_user(form.username.data, form.email.data, form.password.data)
        init_user_plan(user, form.coupon.data or None)
        login_user(user, remember=True)
        return redirect(url_for("user.home"))
    return render_template("register.html", form=form)


@view_blueprint.route("/captcha/<captcha_id>")
def get_captcha(captcha_id):
    captcha = Captcha()
    return captcha
    captcha = Captcha.get_by_captcha_id(captcha_id)


@view_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("view.login"))

